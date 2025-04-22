# Voice-AI-Assistant

# Voice AI Assistant for Fort Wise AI

## Features
- Voice Input (STT with Whisper)
- Semantic Search using FAISS
- Answer generation with GPT-4
- Voice Output (OpenAI TTS)
- Context Memory for follow-ups
- REST API (Flask)

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env  # then update it
python run.py
```

## Test
```bash
pytest tests/
```

## API Usage
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -F "audio=@sample.wav" \
  -H "accept: application/json"
```
