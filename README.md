🎯 Intelligent Face Tracker with Auto-Registration & Visitor Counting

⸻

📌 Overview

This project is an AI-powered real-time system that detects, tracks, and recognizes faces from video streams to accurately count unique visitors.

It automatically:
	•	Detects people using YOLO
	•	Tracks them across frames using DeepSORT
	•	Recognizes faces using InsightFace
	•	Registers new faces with unique IDs
	•	Logs ENTRY and EXIT events with images
	•	Stores all data in both filesystem and database

⸻

🚀 Features

👤 Detection & Tracking
	•	YOLOv8 for real-time person detection
	•	DeepSORT for multi-object tracking
	•	Handles multiple people simultaneously

🧠 Face Recognition
	•	InsightFace (ArcFace embeddings)
	•	Automatic face registration
	•	Unique ID assignment (F1, F2…)

📊 Visitor Counting
	•	Counts unique visitors accurately
	•	Avoids duplicate counting using tracking + recognition

📸 Logging System

Each event (ENTRY / EXIT) stores:
	•	Cropped face image
	•	Timestamp
	•	Face ID
	•	Event type

Stored in:

logs/entries/YYYY-MM-DD/
logs/exits/YYYY-MM-DD/
logs/data.db
logs/events.log

🖥️ Streamlit Dashboard (Bonus)
	•	Live video feed
	•	Real-time metrics (entries, exits, unique visitors)
	•	Event logs
	•	Image previews
	•	History view

⸻

🏗️ System Architecture

                ┌────────────────────┐
                │   Video Input      │
                │ (File / RTSP)      │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ YOLOv8 Detection   │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ DeepSORT Tracking  │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ Face Recognition   │
                │ (InsightFace)      │
                └─────────┬──────────┘
                          ↓
                ┌────────────────────┐
                │ ID Assignment &    │
                │ Auto Registration  │
                └─────────┬──────────┘
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Image Logs   │  │ SQLite DB    │  │ events.log   │
└──────────────┘  └──────────────┘  └──────────────┘
                          ↓
                ┌────────────────────┐
                │ Streamlit UI       │
                └────────────────────┘


⸻

🧠 AI Planning

Step 1: Problem Understanding
	•	Detect faces in real-time
	•	Track them reliably
	•	Count unique visitors without duplication

Step 2: Model Selection
	•	YOLOv8 → fast detection
	•	DeepSORT → stable tracking
	•	InsightFace → high accuracy face embeddings

Step 3: System Design
	•	Modular architecture
	•	Separation of detection, tracking, recognition, and logging
	•	SQLite for lightweight database

Step 4: Optimization
	•	Frame skipping to reduce computation
	•	Crop validation to prevent errors
	•	Efficient logging system

⸻

⚡ Compute Estimation

Component	CPU Usage	GPU Usage
YOLOv8	Medium	High
DeepSORT	Low	Low
InsightFace	Medium	Medium
Overall	Moderate	Optional GPU

👉 Runs on CPU, faster with GPU acceleration

⸻

📂 Repository Structure

app/
├── detection/
│   └── yolo_detector.py
│
├── tracking/
│   └── tracker.py
│
├── recognition/
│   └── face_recognizer.py
│
├── logging_system/
│   ├── logger.py
│   └── image_logger.py
│
├── database/
│   ├── db.py
│
├── config/
│   └── config.json
│
├── main.py
├── streamlit_app.py

logs/
├── entries/
├── exits/
├── data.db
├── events.log


⸻

⚙️ Configuration (config.json)

{
  "yolo_model": "yolov8n.pt",
  "frame_skip": 5,
  "exit_frames": 30,
  "similarity_threshold": 0.6
}


⸻

▶️ How to Run

1️⃣ Clone Repository

git clone <your-repo-link>
cd <project-folder>

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Run Application

streamlit run streamlit_app.py


⸻

🎥 Input Options
	•	Upload video file
	•	RTSP camera stream (used in evaluation)

⸻

📊 Output
	•	Real-time detection with IDs
	•	Entry & Exit counts
	•	Unique visitor count
	•	Image logs stored locally
	•	Database records for each event

⸻

⚠️ Assumptions
	•	Face visibility improves recognition accuracy
	•	One track ID corresponds to one person
	•	Exit is determined when a person is not detected for N frames

⸻

👩‍💻 Author

Pon Nigitha V

⸻

🔗 Hackathon Note

This project is a part of a hackathon run by https://katomaran.com
:::

⸻

