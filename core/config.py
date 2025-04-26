import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_CLOUD_CREDENTIALS_JSON = os.getenv("GOOGLE_CLOUD_CREDENTIALS_JSON")

    MAX_AUDIO_DURATION = int(os.getenv("MAX_AUDIO_DURATION", 30))
    USE_OPENAI_TTS = os.getenv("USE_OPENAI_TTS", "True") == "True"
    USE_OPENAI_STT = os.getenv("USE_OPENAI_STT", "True") == "True"

    DATA_PATH = os.getenv("DATA_PATH", "data/knowledge_base.txt")
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "data/faiss_index/index.faiss")

    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
    TTS_VOICE = os.getenv("TTS_VOICE", "alloy")

    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    CONTEXT_MEMORY_TURNS = os.getenv("CONTEXT_MEMORY_TURNS", 5)
    
