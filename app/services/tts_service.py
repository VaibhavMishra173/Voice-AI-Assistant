import openai
from app.config import Config
import tempfile

openai.api_key = Config.OPENAI_API_KEY

def text_to_speech(text):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    response.stream_to_file(tmp.name)
    return tmp.name
