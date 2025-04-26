import pytest
from api.services import tts
from api.services import tts
import os

def test_tts_generation():
    text = "Hello! This is a test from Fort Wise AI."
    audio_path = tts.synthesize_speech(text)
    assert os.path.exists(audio_path)
    assert audio_path.endswith(".mp3")


def test_synthesize_speech():
    text = "Fort Wise AI is a platform for AI-assisted decision making."
    audio_path = tts.synthesize_speech(text)
    assert audio_path.endswith(".mp3"), f"Expected MP3 file, but got {audio_path}"
