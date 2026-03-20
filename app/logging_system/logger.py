from loguru import logger

logger.add("logs/events.log", rotation="1 MB")

def log_event(face_id, event):
    logger.info(f"{event} - {face_id}")