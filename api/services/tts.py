import os
import openai
import tempfile
from core.config import Config
from api.services.logging import get_logger

logger = get_logger()

openai.api_key = Config.OPENAI_API_KEY

def synthesize_speech(text: str, voice: str = None) -> str:
    voice = voice or Config.TTS_VOICE
    logger.info(f"Generating speech using OpenAI TTS with voice: {voice}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        response.stream_to_file(temp_audio.name)

        logger.info(f"Saved synthesized audio to: {temp_audio.name}")
        return temp_audio.name
