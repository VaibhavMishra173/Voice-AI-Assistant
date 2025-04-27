# import pytest
# from fastapi.testclient import TestClient
# from api.main import app

# client = TestClient(app)

# def test_voice_chat():
#     with open("tests/audio/Who is Alara .mp3", "rb") as audio_file:
#         response = client.post("/api/voice-chat", files={"audio_file": audio_file})
#         assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
#         assert response.headers["Content-Type"] == "audio/mpeg", "Expected audio response"

# TODO:
# Update as per new implementation