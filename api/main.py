from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat
from api.services.logging import get_logger

logger = get_logger()

app = FastAPI(
    title="Voice AI Assistant",
    description="Voice-to-voice assistant powered by Whisper, FAISS, GPT-4o, and TTS",
    version="1.0.0"
)

# Allow frontend (Streamlit or web client)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat")

@app.get("/")
def root():
    logger.info("Health check pinged")
    return {"message": "Voice AI Assistant is running."}
