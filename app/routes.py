from flask import Blueprint, request, jsonify, send_file
from app.services.stt_service import transcribe_audio
from app.services.search_service import search_knowledge_base
from app.services.llm_service import generate_answer
from app.services.tts_service import text_to_speech
from app.utils.audio_utils import save_temp_audio
from app.utils.logger import log_request
from app.services.context_memory import get_conversation_context, update_context
import os

bp = Blueprint('api', __name__)

@bp.route('/ask', methods=['POST'])
def ask():
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({"error": "No audio file provided"}), 400

    save_path = save_temp_audio(audio_file)
    query = transcribe_audio(save_path)
    log_request(query)

    past_context = get_conversation_context()
    retrieved_chunks = search_knowledge_base(query)
    answer = generate_answer(query, retrieved_chunks, past_context)
    update_context(query, answer)

    audio_response_path = text_to_speech(answer)
    return send_file(audio_response_path, mimetype='audio/wav')

