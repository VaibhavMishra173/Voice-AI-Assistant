import streamlit as st
import requests
import tempfile
import os
import base64
from core.config import Config

# Configuration
API_BASE_URL = Config.API_BASE_URL
API_URL = f"{API_BASE_URL}/chat/ask"

# Page setup
st.set_page_config(page_title="Fort Wise Voice Assistant", layout="wide")
st.title("🎙️ Fort Wise Voice AI Assistant")

# Initialize session states
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
    
if 'debug_info' not in st.session_state:
    st.session_state.debug_info = {"last_error": None, "last_file": None, "last_api_request": None}

if 'recorded_audio' not in st.session_state:
    st.session_state.recorded_audio = None
    st.session_state.recorded_format = None
    st.session_state.recording_needs_processing = False

# Function to handle file upload and API call
def process_audio_file(audio_data, filename, content_type="audio/wav"):
    """Process audio data and send to API. Works with file data or bytes."""
    try:
        file_suffix = ".wav" if content_type == "audio/wav" else ".mp3"
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp_file:
            if isinstance(audio_data, bytes):
                tmp_file.write(audio_data)
            else:
                tmp_file.write(audio_data.getvalue())
            temp_file_path = tmp_file.name
        
        st.session_state.debug_info["last_file"] = temp_file_path
        
        if not os.path.exists(temp_file_path):
            st.error(f"Failed to create temporary file")
            return False
            
        file_size = os.path.getsize(temp_file_path)
        if file_size == 0:
            st.error("Audio file is empty")
            return False
            
        st.session_state.debug_info["last_api_request"] = {
            "url": API_URL,
            "file_name": filename,
            "content_type": content_type,
            "file_size": file_size
        }
        
        with open(temp_file_path, "rb") as f:
            files = {"audio_file": (filename, f, content_type)}
            
            with st.spinner("Processing your question..."):
                response = requests.post(
                    API_URL, 
                    files=files,
                    headers={"X-Client-Debug": "streamlit-frontend"}
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
            
            st.success("Response received!")
            return True
        else:
            st.error(f"API Error: {response.status_code}\n{response.text}")
            st.session_state.debug_info["last_error"] = response.text
            return False
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        st.session_state.debug_info["last_error"] = str(e)
        return False

# Create a layout
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📁 Upload an Audio File")
    
    upload_col1, upload_col2 = st.columns([3, 1])
    
    with upload_col1:
        uploaded_file = st.file_uploader("Upload MP3/WAV file (≤ 30s)", type=["wav", "mp3"])
    
    with upload_col2:
        if uploaded_file:
            st.write("File ready!")
            if st.button("Process File", key="process_upload", type="primary"):
                content_type = "audio/wav" if uploaded_file.name.lower().endswith(".wav") else "audio/mp3"
                process_audio_file(uploaded_file, uploaded_file.name, content_type)
    
    st.markdown("---")
    st.subheader("🎤 Or Record Your Question")

    # Placeholder for recording controls and audio playback
    audio_placeholder = st.empty()

    # Using st.components.v1.html to render the custom HTML
    audio_html = """
    <div style="text-align:center;">
      <button id="recordButton" style="padding:10px 20px; font-size:16px;">Start Recording</button>
      <button id="stopButton" style="padding:10px 20px; font-size:16px; display:none;">Stop Recording</button>
      <br><br>
      <audio id="audioPlayback" controls style="width:100%; display:none;"></audio>
    </div>

    <script>
    let mediaRecorder;
    let audioChunks = [];
    const recordButton = document.getElementById('recordButton');
    const stopButton = document.getElementById('stopButton');
    const audioPlayback = document.getElementById('audioPlayback');

    recordButton.onclick = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);

            audioPlayback.src = audioUrl;
            audioPlayback.style.display = 'block';

            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = () => {
                const base64data = reader.result.split(',')[1];
                const streamlitInput = window.parent;
                streamlitInput.postMessage(
                    {type: 'streamlit:recording', data: base64data}, '*'
                );
            };
        };

        mediaRecorder.start();
        recordButton.style.display = 'none';
        stopButton.style.display = 'inline';
    };

    stopButton.onclick = () => {
        mediaRecorder.stop();
        recordButton.style.display = 'inline';
        stopButton.style.display = 'none';
    };
    </script>
    """

    # Rendering the HTML with streamlit.components.v1
    st.components.v1.html(audio_html, height=400)

    # Capture base64 encoded audio data from the browser and process it
    recorded_base64 = st.text_input("Recording", key="recording_base64", value="")

    if recorded_base64:
        decoded_audio = base64.b64decode(recorded_base64)
        st.audio(decoded_audio, format="audio/wav")
        
        if st.button("Send Recording to Backend"):
            with st.spinner("Sending recording..."):
                process_audio_file(decoded_audio, "recorded_audio.wav", content_type="audio/wav")

with col2:
    st.subheader("📝 Your Conversations")
    if st.button("Clear History", key="clear_history"):
        st.session_state.conversation = []
        
    if st.session_state.conversation:
        for idx, chat in enumerate(reversed(st.session_state.conversation)):
            with st.expander(f"🧠 Q: {chat['question'][:80]}..."):
                st.markdown(f"**🧠 Question:** {chat['question']}")
                st.markdown(f"**💬 Answer:** {chat['answer']}")
                st.audio(chat['audio_response'], format="audio/mp3")
    else:
        st.info("No conversation history yet. Upload or record an audio to start!")
