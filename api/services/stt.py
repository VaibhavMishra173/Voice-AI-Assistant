import whisper
from core.config import Config
from api.services.logging import get_logger

logger = get_logger()

model = None

def load_model():
    global model
    if model is None:
        logger.info(f"Loading Whisper model: {Config.WHISPER_MODEL}")
        model = whisper.load_model(Config.WHISPER_MODEL)

def transcribe(audio_path: str) -> str:
    if model is None:
        raise RuntimeError("Model not loaded. Call load_model() at startup.")
    logger.info(f"Transcribing audio file: {audio_path}")
    result = model.transcribe(audio_path)
    return result['text'].strip()
