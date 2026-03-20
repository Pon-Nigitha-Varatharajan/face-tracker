import cv2
from detection.yolo_detector import YOLODetector
from tracking.tracker import Tracker
from recognition.face_recognizer import FaceRecognizer

def run():
    cap = cv2.VideoCapture("data/video1.mp4")

    detector = YOLODetector()
    tracker = Tracker()
    recognizer = FaceRecognizer()

    frame_count = 0
    frame_skip = 5  # process every 5th frame

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize for speed
        frame = cv2.resize(frame, (640, 480))

        frame_count += 1

        # Skip frames for performance
        if frame_count % frame_skip != 0:
            cv2.imshow("Tracking", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        results = detector.detect(frame)

        detections = []

        # Convert YOLO output → DeepSORT format
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])

                # Only detect persons
                if conf > 0.5 and cls == 0:
                    w = x2 - x1
                    h = y2 - y1
                    detections.append(([x1, y1, w, h], conf, 'person'))

        # Update tracker
        tracks = tracker.update(detections, frame)

        # Draw tracking + recognition
        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            l, t, r, b = map(int, track.to_ltrb())

            # Crop person region
            person_crop = frame[t:b, l:r]

            if person_crop.size == 0:
                continue

            # Detect face inside person
            faces = recognizer.app.get(person_crop)

            face_id = "Unknown"

            if len(faces) > 0:
                face = faces[0]
                embedding = recognizer.get_embedding(face)
                face_id = recognizer.recognize(embedding)

            # Draw bounding box + face ID
            cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
            cv2.putText(frame, f"{face_id}", (l, t - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Tracking + Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()