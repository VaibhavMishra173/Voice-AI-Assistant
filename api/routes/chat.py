import streamlit as st
import requests
import tempfile
import os

API_URL = "http://localhost:8000/chat/ask"

st.set_page_config(page_title="Fort Wise Voice Assistant", layout="centered")
st.title("🎙️ Fort Wise Voice AI Assistant")

st.subheader("🎤 Record Your Question (Beta)")

# Record from mic
class AudioRecorderCallback:
    def __init__(self):
        self.audio_frames = []

    def __call__(self, frame):
        pcm = frame.to_ndarray().flatten().astype(np.int16).tobytes()
        self.audio_frames.append(pcm)

callback = AudioRecorderCallback()

webrtc_ctx = webrtc_streamer(
    key="audio-recorder",
    mode=WebRtcMode.SENDONLY,
    in_audio=True,
    out_audio=False,
    client_settings=ClientSettings(media_stream_constraints={"audio": True, "video": False}),
    audio_receiver_size=256,
    on_audio_frame=callback,
)

recorded_audio_path = None

if webrtc_ctx.state.playing:
    st.info("Recording... Click Stop when done.")
elif callback.audio_frames:
    st.success("Recording finished.")
    # Save audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        with wave.open(f, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(48000)
            wf.writeframes(b"".join(callback.audio_frames))
        recorded_audio_path = f.name

# Or upload manually
st.subheader("📁 Or Upload an Audio File")
uploaded_file = st.file_uploader("Upload MP3/WAV file (≤ 30s)", type=["wav", "mp3"])

audio_to_send = recorded_audio_path

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_file.read())
        audio_to_send = temp_audio.name

if audio_to_send:
    with st.spinner("Thinking..."):
        # Explicitly set the content type here
        with open(audio_to_send, "rb") as f:
            files = {
                "audio_file": ("question_audio.mp3", f, "audio/mpeg")  # Explicit content type
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
