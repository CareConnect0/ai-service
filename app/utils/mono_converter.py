from pydub import AudioSegment
import io

def convert_audio_to_mono(input_bytes: bytes) -> bytes:
    audio = AudioSegment.from_file(io.BytesIO(input_bytes), format="wav")
    mono_audio = audio.set_channels(1)

    out_io = io.BytesIO()
    mono_audio.export(out_io, format="wav")
    return out_io.getvalue()
