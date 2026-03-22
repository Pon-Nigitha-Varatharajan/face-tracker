from loguru import logger

logger.add("logs/events.log", rotation="1 MB")

def log_event(video_id, face_id, event, extra=""):
    logger.info(f"{video_id}|{event}|{face_id}|{extra}")