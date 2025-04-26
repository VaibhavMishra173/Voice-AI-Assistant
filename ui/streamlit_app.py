import streamlit as st
import requests
import tempfile
import os
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
import numpy as np
import wave
from core.config import Config
from pydub import AudioSegment

API_BASE_URL = Config.API_BASE_URL
API_URL = f"{API_BASE_URL}/chat/ask"

st.set_page_config(page_title="Fort Wise Voice Assistant", layout="centered")
st.title("🎙️ Fort Wise Voice AI Assistant")

st.subheader("🎤 Record Your Question (Beta)")

# Record from mic
class AudioProcessor:
    def __init__(self) -> None:
        self.audio_frames = []

    def recv_audio(self, frame: av.AudioFrame) -> av.AudioFrame:
        pcm = frame.to_ndarray().flatten().astype(np.int16).tobytes()
        self.audio_frames.append(pcm)
        return frame

audio_processor = AudioProcessor()

webrtc_ctx = webrtc_streamer(
    key="audio-recorder",
    mode=WebRtcMode.SENDONLY,
    media_stream_constraints={"audio": True, "video": False},  # No ClientSettings now
    audio_receiver_size=256,
    audio_processor_factory=lambda: audio_processor,
)

recorded_audio_path = None

if webrtc_ctx.state.playing:
    st.info("Recording... Click Stop when done.")
elif audio_processor.audio_frames:
    st.success("Recording finished.")
    # Save audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        with wave.open(f, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(48000)
            wf.writeframes(b"".join(audio_processor.audio_frames))
        recorded_audio_path = f.name

# Or upload manually
st.subheader("📁 Or Upload an Audio File")
uploaded_file = st.file_uploader("Upload MP3/WAV file (≤ 30s)", type=["wav", "mp3"])

audio_to_send = recorded_audio_path

# Validate file type before sending
if uploaded_file:
    file_type = uploaded_file.type
    st.write(f"Uploaded file type: {file_type}")  # Debugging step to see MIME type
    
    if file_type not in ["audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp3"]:
        st.error("Invalid file type. Only WAV or MP3 files are supported.")
    else:
        # Convert MP3 to WAV if uploaded file is MP3
        if file_type == "audio/mpeg" or uploaded_file.name.endswith(".mp3"):
            st.write("Converting MP3 to WAV...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as mp3_file:
                mp3_file.write(uploaded_file.read())
                mp3_path = mp3_file.name
                
                # Convert MP3 to WAV using pydub
                wav_path = mp3_path.replace(".mp3", ".wav")
                audio = AudioSegment.from_mp3(mp3_path)
                audio.export(wav_path, format="wav")
                audio_to_send = wav_path
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(uploaded_file.read())
                audio_to_send = temp_audio.name

# Ensure the file has the correct content type and send the request
if audio_to_send:
    with st.spinner("Thinking..."):
        with open(audio_to_send, "rb") as f:
            file_contents = f.read()
            
        # Determine the correct content type based on file extension
        if audio_to_send.endswith('.wav'):
            content_type = 'audio/wav'
        elif audio_to_send.endswith('.mp3'):
            content_type = 'audio/mp3'
        else:
            content_type = 'audio/wav'  # Default fallback
            
        files = {
            "audio_file": (
                os.path.basename(audio_to_send),  # Filename
                file_contents,                    # File content
                content_type                      # Content type
            )
        }
        
        response = requests.post(API_URL, files=files)


        if response.status_code == 200:
            st.success("Got response!")

            question = response.headers.get("X-Question")
            answer = response.headers.get("X-Answer")

            if question:
                st.subheader("🧠 Transcribed Question:")
                st.markdown(f"**{question}**")

            if answer:
                st.subheader("💬 Assistant Answer:")
                st.markdown(answer)

            # Play back audio
            st.audio(response.content, format="audio/mp3")

        else:
            st.error(f"API Error: {response.status_code}\n{response.text}")

    os.remove(audio_to_send)
