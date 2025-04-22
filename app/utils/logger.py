import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice_ai")

def log_request(query):
    logger.info(f"Received query: {query}")

