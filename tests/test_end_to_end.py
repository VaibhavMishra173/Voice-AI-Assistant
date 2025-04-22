import requests

def test_api():
    with open("sample.wav", "rb") as f:
        response = requests.post("http://127.0.0.1:8000/ask", files={"audio": f})
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'audio/wav'
