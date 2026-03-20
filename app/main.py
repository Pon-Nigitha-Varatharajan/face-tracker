import cv2
from detection.yolo_detector import YOLODetector

def run():
    cap = cv2.VideoCapture("data/video1.mp4")

    detector = YOLODetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = detector.detect(frame)

        # Draw bounding boxes
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                if conf > 0.5 and int(box.cls[0]) == 0:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow("YOLO Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()