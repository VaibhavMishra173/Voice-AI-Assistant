import wave
from pydub import AudioSegment


def validate_audio_duration(file_path: str, max_duration: int):
    with wave.open(file_path, 'r') as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        if duration > max_duration:
            raise ValueError(f"Audio is too long ({duration:.2f}s > {max_duration}s)")

def convert_audio(filepath: str) -> str:
    output_path = filepath.replace(".mp3", ".wav").replace(".ogg", ".wav")
    audio = AudioSegment.from_file(filepath)
    audio.set_frame_rate(16000).set_channels(1).export(output_path, format="wav")
    return output_path
