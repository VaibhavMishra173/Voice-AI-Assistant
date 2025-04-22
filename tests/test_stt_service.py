from app.services.stt_service import transcribe_audio

def test_transcription():
    text = transcribe_audio("sample.wav")
    assert isinstance(text, str)
    assert len(text) > 0

