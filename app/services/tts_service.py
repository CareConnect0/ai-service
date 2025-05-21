from gtts import gTTS
import io

def tts_stream(text: str):
    # TTS 객체 생성
    tts = gTTS(text, lang='ko')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    def generate():
        while chunk := mp3_fp.read(1024):
            yield chunk

    return generate()
