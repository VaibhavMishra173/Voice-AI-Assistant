import streamlit as st
import requests
import tempfile
import os
import json
import base64
from io import BytesIO
from pydub import AudioSegment
from core.config import Config

API_BASE_URL = Config.API_BASE_URL
API_URL = f"{API_BASE_URL}/chat/ask"

st.set_page_config(page_title="Fort Wise Voice Assistant", layout="centered")
st.title("🎙️ Fort Wise Voice AI Assistant")

# Initialize session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
    
# Initialize debug state
if 'debug_info' not in st.session_state:
    st.session_state.debug_info = {"last_error": None, "last_file": None}

# Initialize recording state
if 'recorded_audio' not in st.session_state:
    st.session_state.recorded_audio = None
    st.session_state.recorded_format = None
    st.session_state.recording_needs_processing = False

# Function to handle file upload and API call
def process_audio_file(audio_file_path, filename):
    try:
        st.session_state.debug_info["last_file"] = audio_file_path
        
        # Check file exists and has content
        if not os.path.exists(audio_file_path):
            st.error(f"File doesn't exist: {audio_file_path}")
            return
            
        file_size = os.path.getsize(audio_file_path)
        if file_size == 0:
            st.error("Audio file is empty")
            return
            
        st.write(f"Sending file: {filename} ({file_size} bytes)")
        
        # Determine content type
        content_type = "audio/wav" if filename.lower().endswith(".wav") else "audio/mp3"
        
        with open(audio_file_path, "rb") as f:
            files = {
                "audio_file": (filename, f, content_type)
            }
            st.write(f"Sending with content type: {content_type}")
            
            with st.spinner("Processing your question..."):
                response = requests.post(
                    API_URL, 
                    files=files,
                    headers={"X-Client-Debug": "streamlit-frontend"}
                )
        
        if response.status_code == 200:
            question = response.headers.get("X-Question")
            answer = response.headers.get("X-Answer")
            
            # Save to conversation history
            st.session_state.conversation.append({
                "question": question,
                "answer": answer
            })
            
            # Display the audio response
            st.audio(response.content, format="audio/mp3")
            
            # Display the text response
            st.subheader("🧠 Transcribed Question:")
            st.markdown(f"**{question}**")
            
            st.subheader("💬 Assistant Answer:")
            st.markdown(answer)
            
            return True
        else:
            st.error(f"API Error: {response.status_code}\n{response.text}")
            st.session_state.debug_info["last_error"] = response.text
            return False
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        st.session_state.debug_info["last_error"] = str(e)
        return False

# Display previous conversation
if st.session_state.conversation:
    with st.expander("View Conversation History", expanded=False):
        for i, exchange in enumerate(st.session_state.conversation):
            st.markdown(f"**User:** {exchange['question']}")
            st.markdown(f"**Assistant:** {exchange['answer']}")
            st.markdown("---")

# Option 1: Native browser recorder (most reliable)
st.subheader("🎤 Record your question")

# Custom HTML/JS component for reliable audio recording
recorder_component = st.components.v1.html("""
<div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px;">
    <div style="margin-bottom: 10px;">
        <button id="recordButton" style="background-color: #ff4b4b; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
            Start Recording
        </button>
        <button id="stopButton" style="background-color: #4b4bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; display: none;">
            Stop Recording
        </button>
    </div>
    <div id="recordingStatus" style="margin-top: 10px; color: #666;">Ready to record</div>
    <audio id="audioPlayback" controls style="margin-top: 10px; display: none;"></audio>
    <div id="downloadContainer" style="margin-top: 10px; display: none;">
        <a id="downloadLink" download="recording.wav">Download</a>
        <button id="sendButton" style="background-color: #4CAF50; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; margin-left: 10px;">
            Send Recording
        </button>
    </div>
    <div id="debug" style="color: gray; font-size: 12px; margin-top: 5px;"></div>
</div>

<script>
    // Audio recorder setup
    let mediaRecorder;
    let audioChunks = [];
    let audioBlob;
    let audioUrl;
    let recordButton = document.getElementById('recordButton');
    let stopButton = document.getElementById('stopButton');
    let audioPlayback = document.getElementById('audioPlayback');
    let downloadLink = document.getElementById('downloadLink');
    let downloadContainer = document.getElementById('downloadContainer');
    let recordingStatus = document.getElementById('recordingStatus');
    let sendButton = document.getElementById('sendButton');
    let debug = document.getElementById('debug');
    
    // Function to get supported mime type
    function getSupportedMimeType() {
        const types = [
            'audio/webm',
            'audio/webm;codecs=opus',
            'audio/ogg;codecs=opus',
            'audio/mp3',
            'audio/wav'
        ];
        
        for (const type of types) {
            if (MediaRecorder.isTypeSupported(type)) {
                return type;
            }
        }
        
        return '';
    }
    
    // Convert blob to base64
    function blobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }
    
    // Record button click handler
    recordButton.onclick = async function() {
        try {
            recordingStatus.textContent = 'Requesting microphone access...';
            debug.textContent = '';
            
            // Request microphone access
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: { 
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                }
            });
            
            // Get supported format
            const mimeType = getSupportedMimeType();
            debug.textContent = `Using format: ${mimeType}, Sample rate: ${new AudioContext().sampleRate}Hz`;
            
            // Create media recorder
            mediaRecorder = new MediaRecorder(stream, { mimeType });
            audioChunks = [];
            
            // Setup data collection
            mediaRecorder.ondataavailable = function(e) {
                audioChunks.push(e.data);
            };
            
            // Setup recording stop handler
            mediaRecorder.onstop = function() {
                // Create audio blob
                audioBlob = new Blob(audioChunks, { type: mimeType });
                audioUrl = URL.createObjectURL(audioBlob);
                
                // Update UI
                audioPlayback.src = audioUrl;
                audioPlayback.style.display = 'block';
                downloadLink.href = audioUrl;
                downloadContainer.style.display = 'block';
                recordingStatus.textContent = 'Recording complete. You can play it back, download it, or send it.';
                
                // Calculate size
                const sizeKb = Math.round(audioBlob.size / 1024);
                debug.textContent += `, Size: ${sizeKb}KB`;
                
                // Release microphone
                stream.getTracks().forEach(track => track.stop());
            };
            
            // Start recording
            mediaRecorder.start();
            recordingStatus.textContent = 'Recording... (speak now)';
            
            // Update UI
            recordButton.style.display = 'none';
            stopButton.style.display = 'inline-block';
            audioPlayback.style.display = 'none';
            downloadContainer.style.display = 'none';
            
        } catch (err) {
            recordingStatus.textContent = 'Error accessing microphone';
            debug.textContent = `Error: ${err.message}`;
        }
    };
    
    // Stop button handler
    stopButton.onclick = function() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            recordButton.style.display = 'inline-block';
            stopButton.style.display = 'none';
        }
    };
    
    // Send button handler
    sendButton.onclick = async function() {
        if (audioBlob) {
            try {
                recordingStatus.textContent = 'Preparing to send recording...';
                
                // Convert blob to base64
                const base64Data = await blobToBase64(audioBlob);
                
                // Send the recording to Streamlit
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: {
                        action: 'audio_recorded',
                        format: mediaRecorder.mimeType || 'audio/wav',
                        data: base64Data
                    }
                }, '*');
                
                recordingStatus.textContent = 'Recording sent! Processing...';
                downloadContainer.style.display = 'none';
                audioPlayback.style.display = 'none';
            } catch (err) {
                recordingStatus.textContent = 'Error sending recording';
                debug.textContent = `Send error: ${err.message}`;
            }
        }
    };
</script>
""", height=250)

# Create a container for the send button area
send_container = st.container()

# Handle recording callback from JS component
if st.session_state.get('_component_value') is not None:
    component_value = st.session_state['_component_value']
    
    if component_value.get('action') == 'audio_recorded':
        # Extract audio data and format
        audio_data = component_value.get('data')
        audio_format = component_value.get('format', 'audio/wav')
        
        if audio_data:
            # Store in session state for processing
            st.session_state.recorded_audio = audio_data
            st.session_state.recorded_format = audio_format
            st.session_state.recording_needs_processing = True
            
            # Reset component value
            st.session_state['_component_value'] = None
            st.experimental_rerun()

# Process the recording if needed
if st.session_state.recording_needs_processing:
    with st.spinner("Processing your recording..."):
        try:
            # Extract the base64 data part
            base64_str = st.session_state.recorded_audio
            if ',' in base64_str:
                base64_str = base64_str.split(',', 1)[1]
                
            # Decode the base64 data
            audio_data = base64.b64decode(base64_str)
            
            # Get format info
            format_type = st.session_state.recorded_format
            file_suffix = ".wav"
            if "webm" in format_type.lower():
                file_suffix = ".webm"
            elif "ogg" in format_type.lower():
                file_suffix = ".ogg"
            elif "mp3" in format_type.lower():
                file_suffix = ".mp3"
            
            # Save to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp_file:
                tmp_file.write(audio_data)
                temp_file_path = tmp_file.name
            
            # Process the file
            filename = f"browser-recording{file_suffix}"
            process_audio_file(temp_file_path, filename)
            
            # Clean up
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                
            # Reset state
            st.session_state.recorded_audio = None
            st.session_state.recorded_format = None
            st.session_state.recording_needs_processing = False
            
        except Exception as e:
            st.error(f"Error processing recorded audio: {str(e)}")
            st.session_state.debug_info["last_error"] = str(e)
            
            # Show the error in debug
            with st.expander("Debug Error Information", expanded=True):
                st.write("### Error Details")
                st.write(str(e))
                if st.session_state.recorded_format:
                    st.write(f"Format: {st.session_state.recorded_format}")
                if st.session_state.recorded_audio:
                    audio_preview = st.session_state.recorded_audio[:100] + "..." if len(st.session_state.recorded_audio) > 100 else st.session_state.recorded_audio
                    st.write(f"Audio data preview: {audio_preview}")
            
            # Reset state
            st.session_state.recording_needs_processing = False

# Option 2: File upload
st.subheader("📁 Or Upload an Audio File")
uploaded_file = st.file_uploader("Upload MP3/WAV file (≤ 30s)", type=["wav", "mp3"])

if uploaded_file:
    try:
        # Save the file locally
        file_suffix = ".wav" if uploaded_file.name.lower().endswith(".wav") else ".mp3"
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_file_path = tmp_file.name
            
        # Process the file
        process_success = process_audio_file(temp_file_path, uploaded_file.name)
        
        # Clean up
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
    
    except Exception as e:
        st.error(f"Error processing uploaded file: {str(e)}")

# Debug section
with st.expander("Debug Information", expanded=False):
    st.write("### Debug Info")
    st.json(st.session_state.debug_info)
    
    if st.button("Test API Connection"):
        try:
            # Simple ping test - Use a more specific endpoint for future, if going serverless
            test_endpoints = [f"{API_BASE_URL}"]
            for endpoint in test_endpoints:
                try:
                    st.write(f"Testing endpoint: {endpoint}")
                    response = requests.get(endpoint, timeout=5)
                    st.write(f"Status: {response.status_code}")
                    st.write(f"Response: {response.text[:500]}..." if len(response.text) > 500 else response.text)
                except Exception as e:
                    st.write(f"Failed: {str(e)}")
        except Exception as e:
            st.error(f"API Connection Error: {str(e)}")
    
    # Add a direct base64 sender for troubleshooting
    st.write("### Direct Audio Test")
    if st.session_state.recorded_audio and st.button("Show Last Recording Info"):
        st.write(f"Format: {st.session_state.recorded_format}")
        preview_len = min(200, len(st.session_state.recorded_audio))
        st.write(f"Data (first {preview_len} chars): {st.session_state.recorded_audio[:preview_len]}...")
    
    st.write("### Audio Test")
    test_recording = st.file_uploader("Upload test audio file", type=["wav", "mp3"], key="debug_uploader")
    
    if test_recording and st.button("Send Test File"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(test_recording.getvalue())
            test_file_path = tmp_file.name
            
        try:
            # Manually construct request for debugging
            with open(test_file_path, "rb") as f:
                content_type = "audio/wav" if test_recording.name.lower().endswith(".wav") else "audio/mp3"
                files = {"audio_file": (test_recording.name, f, content_type)}
                
                st.write(f"Sending file with content type: {content_type}")
                response = requests.post(API_URL, files=files)
                
                st.write(f"Status Code: {response.status_code}")
                st.write(f"Headers: {dict(response.headers)}")
                
                if response.status_code == 200:
                    st.audio(response.content, format="audio/mp3")
                else:
                    st.write(f"Error Response: {response.text}")
        except Exception as e:
            st.error(f"Debug request error: {str(e)}")
        finally:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)