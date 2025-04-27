# 🧠 Fort Wise Voice AI Assistant

A powerful **Voice-to-Voice Assistant powered by Whisper, FAISS, GPT-4o, and TTS** that takes voice input, retrieves knowledge via FAISS, answers using **GPT-4o**, and responds back with natural **TTS (Text-to-Speech)** audio.  
Built with **FastAPI** for the backend and **Streamlit** for a simple web UI.

---

## 🌟 Features

- 🎹 Voice Input (WAV/MP3) using **Whisper** STT
- 🔎 Semantic Search using **FAISS**
- 🧠 Response Generation with **GPT-4o**
- 👤 Voice Output via **OpenAI TTS**
- 🧠 Context Memory for follow-up conversations
- 🌐 Streamlit-based Web UI
- 🚀 FastAPI-powered REST API
- ✅ Unit-tested for reliability
- 🐳 Dockerized for easy deployment

---

## 🐳 Quickstart with Docker (Recommended)

Build and run the app with Docker Compose:

```bash
docker-compose up --build
```

Access the backend API:  
➡️ `http://localhost:8000`

Access the Streamlit UI:  
➡️ `http://localhost:8501`

> **Note**: Make sure you configure your `.env` file correctly before building the Docker image!

If you make changes to the code, rebuild the containers:

```bash
docker-compose down
docker-compose up --build
```

---

## 📁 Folder Structure

```
Voice-AI-Assistant/
├── api/
│   ├── main.py
│   ├── routes/
│   └── services/
├── core/
│   ├── config.py
│   └── utils/
├── data/
│   ├── knowledge_base.txt
│   └── faiss_index/
├── telegram_bot/
│   └── bot.py
├── tests/
│   ├── test_*.py
│   └── audio/
├── ui/
│   └── streamlit_app.py
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
├── run.py
└── run.sh
```

---

## 🧪 Manual Setup Instructions (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/VaibhavMishra173/Voice-AI-Assistant.git
cd Voice-AI-Assistant
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install git+https://github.com/openai/whisper.git
```

### 4. Configure Environment Variables

Create a `.env` file based on `.env.example`:

```
# API Keys
OPENAI_API_KEY=your_openai_api_key_here

# Google Cloud TTS (optional for future)
GOOGLE_CLOUD_CREDENTIALS_JSON=path/to/your/credentials.json

# App Config
MAX_AUDIO_DURATION=30
USE_OPENAI_TTS=True
USE_OPENAI_STT=True

# Path Configs
DATA_PATH=data/knowledge_base.txt
FAISS_INDEX_PATH=data/faiss_index/index.faiss

# Models
MODEL_NAME=gpt-4o
WHISPER_MODEL=base
TTS_VOICE=alloy  # Options: echo, fable, onyx, nova, shimmer
CONTEXT_MEMORY_TURNS=15

# URLs
API_BASE_URL=http://localhost:8000
# IMPORTANT: For Docker, use service name instead of localhost
# API_BASE_URL=http://voice-ai-fastapi:8000
```

---

## 🚀 Running the Application Locally

### 1. Start Backend API (FastAPI)

```bash
uvicorn api.main:app --reload
```

Access the backend at:  
➡️ `http://127.0.0.1:8000`

---

### 2. Start Web UI (Streamlit)

```bash
streamlit run ui/streamlit_app.py
```

Access the UI at:  
➡️ `http://localhost:8501`

In the UI you can:
- Upload or record voice input
- View the transcription
- See relevant document retrieval
- Hear the AI's voice reply

---

## 💪 Running Tests

Run all unit tests:

```bash
pytest tests/
```

---

## 📡 API Example Usage

Send an audio file to the backend:

```bash
curl -X POST http://127.0.0.1:8000/chat/ask \
  -F "audio=@sample_audio.wav" \
  -H "accept: application/json"
```

---

## 🤖 Telegram Bot (Optional, In Progress)

- Listens for voice messages.
- Sends them to your backend `/chat/ask` API.
- Replies with generated audio responses.

Run the bot:

```bash
python telegram_bot/bot.py
```

---

## 📄 Notes & Improvements

- Multi-turn conversation with context memory.
- Full error handling and centralized logging.
- Easily configurable via `.env`.
- Backend ready for production deployment.
- **Planned Features:**
  - Production deployment (Render / Railway / GCP)
  - Better long-context memory
  - Multilingual support
  - Real-time streaming conversations

---

## ❤️ Credits

- [OpenAI](https://openai.com/) — Whisper, GPT-4o, TTS APIs
- [FAISS](https://github.com/facebookresearch/faiss) — Nearest Neighbor Search
- [Streamlit](https://streamlit.io/) — Web UI Framework
- [FastAPI](https://fastapi.tiangolo.com/) — API Framework

---

## 📬 Contact

For any issues, questions, or contributions:  
📧 vaibhavmishra173@gmail.com  
🔗 [GitHub Profile](https://github.com/VaibhavMishra173)

---

# 🚀 Let's build the future of voice-first AI assistants!

