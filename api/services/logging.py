from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO", format="{time} {level} {message}")

def get_logger():
    return logger
