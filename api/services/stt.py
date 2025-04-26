import whisper
from core.config import Config
from api.services.logging import get_logger

logger = get_logger()

_model = None

def load_model():
    global _model
    if _model is None:
        logger.info(f"Loading Whisper model: {Config.WHISPER_MODEL}")
        _model = whisper.load_model(Config.WHISPER_MODEL)
    return _model

def transcribe(audio_path: str) -> str:
    model = load_model()
    logger.info(f"Transcribing audio file: {audio_path}")
    result = model.transcribe(audio_path)
    return result['text'].strip()
