import sqlite3
from datetime import datetime

DB_PATH = "logs/data.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        video_id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_name TEXT,
        timestamp TEXT,
        total_entries INTEGER,
        total_exits INTEGER,
        unique_people INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_id INTEGER,
        face_id TEXT,
        event TEXT,
        time TEXT,
        image_path TEXT
    )
    """)

    conn.commit()
    conn.close()

create_tables()

def create_video(video_name):
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO videos (video_name, timestamp, total_entries, total_exits, unique_people)
    VALUES (?, ?, 0, 0, 0)
    """, (video_name, timestamp))

    conn.commit()
    vid = cursor.lastrowid
    conn.close()
    return vid

def insert_event(video_id, face_id, event, image_path):
    conn = get_connection()
    cursor = conn.cursor()

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO events (video_id, face_id, event, time, image_path)
    VALUES (?, ?, ?, ?, ?)
    """, (video_id, face_id, event, time, image_path))

    conn.commit()
    conn.close()

def update_video_stats(video_id, entries, exits, unique_people):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE videos
    SET total_entries=?, total_exits=?, unique_people=?
    WHERE video_id=?
    """, (entries, exits, unique_people, video_id))

    conn.commit()
    conn.close()