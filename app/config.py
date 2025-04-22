import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_CLOUD_CREDENTIALS_JSON = os.getenv("GOOGLE_CLOUD_CREDENTIALS_JSON")
    MAX_AUDIO_DURATION = int(os.getenv("MAX_AUDIO_DURATION", 30))
    USE_OPENAI_TTS = os.getenv("USE_OPENAI_TTS", "True") == "True"
    USE_OPENAI_STT = os.getenv("USE_OPENAI_STT", "True") == "True"
    DATA_PATH = os.getenv("DATA_PATH")
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH")

