from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, conf=0.5)

        detections = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])

                # Only detect PERSON (fallback mode)
                if cls != 0:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                detections.append(([x1, y1, x2 - x1, y2 - y1], conf, "person"))

        return detections