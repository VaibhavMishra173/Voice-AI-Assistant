import streamlit as st
import requests
import tempfile
import os
from core.config import Config
from st_audiorec import st_audiorec

# Configuration
API_BASE_URL = Config.API_BASE_URL
API_URL = f"{API_BASE_URL}/chat/ask"

# Page setup
st.set_page_config(page_title="Fort Wise Voice Assistant", layout="wide")
st.title("🎙️ Fort Wise Voice AI Assistant")

# Initialize session states
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
    
if 'info_info' not in st.session_state:
    st.session_state.info_info = {"last_error": None, "last_file": None, "last_api_request": None}

if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None

# Function to send audio to backend
def send_to_backend(audio_data, filename="recorded_audio.wav", content_type="audio/wav"):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_data)
            temp_file_path = tmp_file.name
        
        with open(temp_file_path, "rb") as f:
            files = {"audio_file": (filename, f, content_type)}
            
            with st.spinner("Processing your question..."):
                response = requests.post(
                    API_URL, 
                    files=files,
                    headers={"X-Client-info": "streamlit-frontend"}
                )
        
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        if response.status_code == 200:
            question = response.headers.get("X-Question")
            answer = response.headers.get("X-Answer")
            
            st.session_state.conversation.append({
                "question": question,
                "answer": answer,
                "audio_response": response.content
            })
            
            return True
        else:
            st.error(f"API Error: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

# Layout
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📁 Upload an Audio File")
    
    uploaded_file = st.file_uploader("Upload MP3/WAV file (≤ 30s)", type=["wav", "mp3"])
    if uploaded_file:
        st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")
        if st.button("Process File", key="process_upload", type="primary"):
            content_type = "audio/wav" if uploaded_file.name.lower().endswith(".wav") else "audio/mp3"
            send_to_backend(uploaded_file.getvalue(), uploaded_file.name, content_type)
    
    st.markdown("---")
    st.subheader("🎤 Or Record Your Question")

    # New simple recording block
    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        st.audio(wav_audio_data, format="audio/wav")

        if st.button("Process Recording", key="process_recording", type="primary"):
            if send_to_backend(wav_audio_data, "recording.wav", "audio/wav"):
                st.success("Recording sent to assistant!")
                st.rerun()

        if st.button("Record Again", key="record_again"):
            st.rerun()

with col2:
    st.subheader("📝 Your Conversations")
    if st.button("Clear History", key="clear_history"):
        st.session_state.conversation = []
        
    if st.session_state.conversation:
        for idx, chat in enumerate(reversed(st.session_state.conversation)):
            with st.expander(f"🧠 Q: {chat['question'][:80] if chat['question'] else 'No question detected'}..."):
                st.markdown(f"**🧠 Question:** {chat['question']}")
                st.markdown(f"**💬 Answer:** {chat['answer']}")
                st.audio(chat['audio_response'], format="audio/mp3")
    else:
        st.info("No conversation history yet. Upload or record an audio to start!")
