import pytest
from api.services import stt
from api.services import stt

def test_transcription_on_sample():
    sample_audio = "tests/assets/sample.wav"
    text = stt.transcribe(sample_audio)
    assert isinstance(text, str)
    assert len(text) > 0

def test_transcribe_audio():
    audio_path = "data/sample_question.wav"
    transcription = stt.transcribe_audio(audio_path)
    assert transcription == "What does Fort Wise do?", f"Expected 'What does Fort Wise do?' but got {transcription}"
