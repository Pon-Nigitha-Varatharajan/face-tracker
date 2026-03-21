import cv2
import json
import os

from detection.yolo_detector import YOLODetector
from tracking.tracker import Tracker
from recognition.face_recognizer import FaceRecognizer
from logging_system.logger import log_event
from logging_system.image_logger import save_image
from database.db import create_video, insert_event, update_video_stats


def run(video_source, streamlit_callback=None):

    # Load config
    with open("app/config/config.json") as f:
        config = json.load(f)

    cap = cv2.VideoCapture(video_source)

    detector = YOLODetector(config["yolo_model"])
    tracker = Tracker()
    recognizer = FaceRecognizer(config["similarity_threshold"])

    frame_skip = config["frame_skip"]
    exit_frames = config["exit_frames"]

    frame_count = 0

    active_tracks = set()
    last_seen = {}
    track_to_face = {}

    # 🔥 CHANGE: track unique persons instead of faces
    unique_persons = set()
    captured_ids = set()

    video_id = create_video(os.path.basename(video_source))

    entry_count = 0
    exit_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        frame_count += 1

        if frame_count % frame_skip != 0:
            continue

        detections = detector.detect(frame)
        tracks = tracker.update(detections, frame)

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id

            l, t, r, b = map(int, track.to_ltrb())

            h, w, _ = frame.shape
            l, t = max(0, l), max(0, t)
            r, b = min(w, r), min(h, b)

            crop = frame[t:b, l:r]

            # ❗ Skip invalid crops
            if crop is None or crop.size == 0:
                continue

            h_crop, w_crop = crop.shape[:2]
            if h_crop < 20 or w_crop < 20:
                continue

            # ---------------- FACE RECOGNITION ----------------
            if track_id not in track_to_face:
                face_id = recognizer.recognize(crop)
                if face_id:
                    track_to_face[track_id] = face_id

            face_id = track_to_face.get(track_id)

            # 🔥 IMPORTANT: Always assign display ID
            display_id = face_id if face_id else f"T{track_id}"

            # ---------------- ENTRY ----------------
            if track_id not in active_tracks:
                active_tracks.add(track_id)
                entry_count += 1

                # 🔥 ALWAYS count person
                unique_persons.add(display_id)

                img = save_image(display_id, crop, "entry")

                log_event(video_id, display_id, "ENTRY")
                insert_event(video_id, display_id, "ENTRY", img)

            last_seen[track_id] = frame_count

            # ---------------- DRAW ----------------
            cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
            cv2.putText(frame, display_id, (l, t - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # ---------------- EXIT ----------------
        for tid in list(active_tracks):
            if frame_count - last_seen.get(tid, 0) > exit_frames:

                exit_count += 1

                face_id = track_to_face.get(tid)
                display_id = face_id if face_id else f"T{tid}"

                img = save_image(display_id, frame, "exit")

                log_event(video_id, display_id, "EXIT")
                insert_event(video_id, display_id, "EXIT", img)

                active_tracks.remove(tid)
                track_to_face.pop(tid, None)

        # ---------------- CALLBACK ----------------
        if streamlit_callback:
            streamlit_callback(
                frame,
                video_id,
                entry_count,
                exit_count,
                unique_persons   # 🔥 UPDATED
            )

    update_video_stats(
        video_id,
        entry_count,
        exit_count,
        len(unique_persons)   # 🔥 UPDATED
    )

    cap.release()
    return video_id