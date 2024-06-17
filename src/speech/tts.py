# Text-to-Speech (TTS) module for generating audio files using Deepgram API
import uuid

from deepgram import SpeakOptions
import speech.deepgram_wrapper as deepgram_wrapper

deepgram = deepgram_wrapper.deepgram

deepgram_options: SpeakOptions = SpeakOptions(
    model="aura-asteria-en",
    encoding="linear16",
    container="wav"
)

def synthesize_text(text: str) -> str:

    payload = {
        "text": text
    }

    random_filename = f"audio_files/response_{uuid.uuid4()}.wav"

    response = deepgram.speak.v("1").save(random_filename, payload, deepgram_options, timeout=15)
    response = response.to_dict()

    return random_filename