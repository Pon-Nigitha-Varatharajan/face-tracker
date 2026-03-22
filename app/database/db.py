import sqlite3
from datetime import datetime

# Path to SQLite database file
DB_PATH = "logs/data.db"


def get_connection():
    """
    Create and return a database connection.
    check_same_thread=False allows usage across multiple threads (e.g., Streamlit).
    """
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def create_tables():
    """
    Create required tables if they do not already exist.

    Tables:
    - videos: Stores summary of each processed video
    - events: Stores entry/exit logs for each detected person
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Table to store video-level analytics
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

    # Table to store individual entry/exit events
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
    """
    Insert a new video record into the database.

    Args:
        video_name (str): Name of the input video file

    Returns:
        int: Generated video_id for tracking events
    """
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO videos (video_name, timestamp, total_entries, total_exits, unique_people)
    VALUES (?, ?, 0, 0, 0)
    """, (video_name, timestamp))

    conn.commit()
    video_id = cursor.lastrowid
    conn.close()

    return video_id


def insert_event(video_id, face_id, event, image_path):
    """
    Insert an entry or exit event into the database.

    Args:
        video_id (int): Associated video ID
        face_id (str): Recognized face ID or track ID
        event (str): Type of event ("ENTRY" or "EXIT")
        image_path (str): Path to saved cropped image
    """
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
    """
    Update summary statistics for a processed video.

    Args:
        video_id (int): Video identifier
        entries (int): Total entry count
        exits (int): Total exit count
        unique_people (int): Unique visitor count
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE videos
    SET total_entries=?, total_exits=?, unique_people=?
    WHERE video_id=?
    """, (entries, exits, unique_people, video_id))

    conn.commit()
    conn.close()