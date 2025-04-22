import tempfile
from pydub import AudioSegment

def save_temp_audio(file):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio = AudioSegment.from_file(file)
    audio.export(tmp.name, format="wav")
    return tmp.name

