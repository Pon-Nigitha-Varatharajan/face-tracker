import cv2
import os
from datetime import datetime

def save_image(face_id, image, event):
    folder = f"logs/{event}s"
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"{folder}/{face_id}_{timestamp}.jpg"

    cv2.imwrite(path, image)
    return path