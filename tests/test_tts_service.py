from app.services.tts_service import text_to_speech

def test_tts():
    path = text_to_speech("Test audio generation")
    assert path.endswith(".wav")


