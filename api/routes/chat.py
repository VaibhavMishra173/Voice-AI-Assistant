from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
import os
from api.services import stt, tts, llm, vector_search
from api.services.memory import SessionMemory
from core.utils.audio_utils import validate_audio_duration, convert_audio
from core.config import Config
from api.services.logging import get_logger

router = APIRouter()
logger = get_logger()
memory = SessionMemory()

@router.post("/ask")
async def chat_ask(audio_file: UploadFile = File(...)):
    if audio_file.content_type not in ["audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp3"]:
        raise HTTPException(status_code=400, detail="Only WAV or MP3 files are supported")

    temp_audio_path = None
    converted_path = None
    try:
        # Save uploaded file temporarily
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(await audio_file.read())
            temp_audio_path = temp_audio.name

        # Convert to proper format if needed (e.g., MP3 -> WAV)
        converted_path = convert_audio(temp_audio_path)

        # Optional: Check audio duration limit
        validate_audio_duration(converted_path, Config.MAX_AUDIO_DURATION)

        logger.info("Transcribing audio...")
        question = stt.transcribe(converted_path)

        if not question:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

        logger.info(f"User said: {question}")

        # Retrieve memory context and docs
        memory_context = memory.get_formatted_context()
        docs = vector_search.query_faiss(question)

        logger.info("Generating answer...")
        answer = llm.generate_answer(question, docs, memory_context)

        logger.info(f"AI Answer: {answer}")

        # Save to memory
        memory.add_turn(question, answer)

        # TTS synthesis
        audio_response_path = tts.synthesize_speech(answer)

        return FileResponse(
            path=audio_response_path,
            media_type="audio/mpeg",
            filename="response.mp3",
            headers={
                "X-Question": question,
                "X-Answer": answer
            }
        )

    except Exception as e:
        logger.exception("Error in /chat/ask endpoint")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    finally:
        # Clean up all temp files
        for f in [temp_audio_path, converted_path]:
            if f and os.path.exists(f):
                os.remove(f)
