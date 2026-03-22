🎯 Intelligent Face Tracker with Auto-Registration & Visitor Counting

⸻

📌 Overview

This project is an AI-powered real-time system that detects, tracks, and recognizes people from video streams to accurately count unique visitors.

The system:
	•	Detects people using YOLOv8
	•	Tracks them using DeepSORT
	•	Recognizes faces using InsightFace
	•	Automatically assigns unique IDs
	•	Logs ENTRY and EXIT events with images
	•	Stores logs in filesystem + database
	•	Provides a live dashboard using Streamlit

⸻

🚀 Features

👤 Detection & Tracking
	•	Real-time person detection using YOLOv8
	•	Multi-object tracking using DeepSORT
	•	Works with video files and RTSP streams

🧠 Face Recognition & Auto Registration
	•	InsightFace for high-accuracy embeddings
	•	Automatic face registration (no manual dataset required)
	•	Unique ID generation (F1, F2…)

📊 Unique Visitor Counting
	•	Counts each person only once
	•	Avoids duplicate counting using tracking + recognition

📸 Logging System

Each ENTRY / EXIT event stores:
	•	Cropped image
	•	Timestamp
	•	Person ID
	•	Event type

Stored in:

logs/
├── entries/YYYY-MM-DD/
├── exits/YYYY-MM-DD/
├── data.db
└── events.log

🖥️ Streamlit Dashboard 
	•	Live video stream
	•	Real-time metrics (entries, exits, unique visitors)
	•	Recent detections with images
	•	Historical data view

⸻

🏗️ System Architecture

        Video Input (File / RTSP)
                    │
                    ▼
            YOLOv8 Detection
                    │
                    ▼
            DeepSORT Tracking
                    │
                    ▼
        Face Recognition (InsightFace)
                    │
                    ▼
      ID Assignment & Registration
                    │
                    ▼
       Image logs,SQLite db,events.log
                    │
                    ▼
              Streamlit UI

The system follows a modular pipeline architecture ensuring scalability and separation of concerns.

⸻

📂 Repository Structure

face-tracker/
│
├── app/
│   ├── detection/
│   │   └── yolo_detector.py
│   │
│   ├── tracking/
│   │   └── tracker.py
│   │
│   ├── recognition/
│   │   └── face_recognizer.py
│   │
│   ├── logging_system/
│   │   ├── logger.py
│   │   └── image_logger.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   └── queries.py
│   │
│   ├── config/
│   │   └── config.json
│   │
│   ├── main.py
│   └── streamlit_app.py
│
├── logs/
│   ├── entries/
│   ├── exits/
│   ├── data.db
│   └── events.log
│
└── README.md
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

1️⃣ Clone the Repository

git clone <https://github.com/Pon-Nigitha-Varatharajan/face-tracker>
cd face-tracker

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Run the Application

streamlit run app/streamlit_app.py


⸻

🎥 Input Options
	•	Upload video file
	•	RTSP stream

⸻

📊 Output
	•	Real-time person detection with ID
	•	Entry & Exit counts
	•	Unique visitor count
	•	Saved images of detections
	•	Database records for all events

⸻

🧠 AI Planning

Step 1: Problem Understanding
	•	Detect people in real-time
	•	Track consistently
	•	Count unique visitors without duplication

Step 2: Model Selection
	•	YOLOv8 → fast detection
	•	DeepSORT → stable tracking
	•	InsightFace → accurate recognition

Step 3: System Design
	•	Modular architecture
	•	Separate detection, tracking, recognition, logging
	•	SQLite for lightweight storage

Step 4: Optimization
	•	Frame skipping to reduce computation
	•	Crop validation to avoid errors
	•	Efficient logging pipeline

⸻

⚠️ Assumptions
	•	Faces are visible for recognition
	•	One track ID corresponds to one person
	•	Exit occurs when a person disappears for N frames
	•	Lighting conditions may affect accuracy

⸻

🎥 Demo Video

https://www.loom.com/share/d90161c596024cf0ac9a28fe2c856a49

⸻

👩‍💻 Author

Pon Nigitha V

⸻

🔗 Hackathon Note

This project is a part of a hackathon run by https://katomaran.com
:::

⸻
