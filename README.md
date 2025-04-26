# 🧠 Fort Wise AI - Voice Assistant

A Voice AI Chatbot that takes voice input, retrieves knowledge via FAISS, and replies with voice using GPT-4o and OpenAI TTS.

## 🎯 Features

- Voice input (WAV/MP3)
- Whisper STT
- FAISS-powered semantic search
- GPT-4o for accurate, grounded answers
- OpenAI TTS for natural voice replies
- Context memory
- Streamlit UI + FastAPI API

## 🛠 Setup

```bash
git clone https://github.com/yourname/fort-wise-voice-ai.git
cd fort-wise-voice-ai
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install git+https://github.com/openai/whisper.git












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












# voice-assistant

A Voice AI Assistant that allows users to speak their questions and get spoken answers based on a `.txt` knowledge base using FAISS + OpenAI APIs.

---

## 📁 Folder Structure
```
voice-assistant/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── routes.py
│   ├── services/
│   │   ├── stt_service.py
│   │   ├── faiss_service.py
│   │   ├── llm_service.py
│   │   └── tts_service.py
│   └── utils/
│       ├── audio_utils.py
│       └── logger.py
├── ui/
│   └── streamlit_app.py
├── tests/
│   └── test_services.py
├── .env
├── requirements.txt
├── run.py
├── sample_data.txt
├── sample_audio.wav
└── README.md
```

---

## ✅ Setup Instructions

### 1. Clone and Install
```bash
git clone https://github.com/your-username/voice-assistant.git
cd voice-assistant
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Add Environment Variables
Create a `.env` file:
```
OPENAI_API_KEY=your-openai-key
AUDIO_INPUT_LIMIT_SECONDS=30
FAISS_INDEX_PATH=faiss_index/index.faiss
EMBEDDING_CSV_PATH=faiss_index/embeddings.csv
DATASET_PATH=sample_data.txt
```

### 3. Run Web UI (Streamlit)
```bash
streamlit run ui/streamlit_app.py
```

---

## 🌐 Streamlit UI
The app lets you:
- Upload an audio file (WAV)
- View transcribed text
- See retrieved document chunks
- Listen to the AI's voice response

---

## 🧪 Run Tests
```bash
pytest tests/
```

---

## 🎤 Sample Audio
Use the `sample_audio.wav` provided to test.

---

## 🧰 Sample `curl` Command (API alternative)
```bash
curl -X POST http://localhost:5000/ask \
  -F "audio=@sample_audio.wav"
```

---

## 📄 Notes & Improvements
- Supports follow-up questions via context memory (basic)
- Robust error handling and logging included
- Configurable via `.env`
- Streamlit UI for demo, easy to extend
- Deployment-ready backend with Flask

---

## 🚀 Next Steps (Planned)
- Dockerization
- Telegram bot version
- Production deployment on Render / Railway / GCP





















## Fort Wise Voice AI Assistant

### Setup
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
streamlit run ui/streamlit_app.py
```

### Docker
```bash
docker build -t fortwise-assistant .
docker run -p 5000:5000 --env-file .env fortwise-assistant
```

### Deployment Options
- **Render**: Add repo, configure Docker
- **Railway**: Docker project > connect GitHub > auto deploy
- **GCP**: Use Cloud Run for Docker

### Telegram Bot
- Bot listens to voice messages → sends to `/ask` → replies with audio
- See `telegram_bot/bot.py`

### Tests
Run with:
```bash
pytest tests/
```