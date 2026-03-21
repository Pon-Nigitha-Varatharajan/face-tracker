import cv2
import os
from datetime import datetime

def save_image(face_id, image, event):

    date_folder = datetime.now().strftime("%Y-%m-%d")

    # ✅ Correct folder structure
    if event == "ENTRY":
        folder = f"logs/entries/{date_folder}"
    elif event == "EXIT":
        folder = f"logs/exits/{date_folder}"
    else:
        folder = f"logs/others/{date_folder}"

    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{folder}/{face_id}_{timestamp}.jpg"

    cv2.imwrite(filename, image)

    return filename  # ✅ IMPORTANT (you missed earlier sometimes)