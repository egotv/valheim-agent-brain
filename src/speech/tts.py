# Text-to-Speech (TTS) module for generating audio files using Deepgram API
import uuid

from deepgram import SpeakOptions
import speech.speech_wrapper as speech_wrapper

import utils.utils as utils
from utils.analytics import log_async

import pyaudio

deepgram = speech_wrapper.deepgram
cartesia = speech_wrapper.cartesia

def synthesize_text(text: str, voice: str) -> str:

    payload = {
        "text": text
    }

    deepgram_options: SpeakOptions = SpeakOptions(
        model=f"aura-{voice}-en",
        encoding="linear16",
        container="wav"
    )

    random_file_id = uuid.uuid4()
    random_filename = f"audio_files/response_{random_file_id}.wav"

    start_timestamp = utils.get_timestamp()

    try:
        response = deepgram.speak.v("1").save(random_filename, payload, deepgram_options, timeout=15)
        response = response.to_dict()
        log_async("DEEPGRAM_RESPONSE", f"{response}")
        
        time_elapsed = utils.get_timestamp() - start_timestamp
        log_async("DEEPGRAM_TTS_LATENCY", f"{time_elapsed}")

    except Exception as e:
        print(f"Exception: {e}")
        log_async("DEEPGRAM_ERROR", f"Exception: {e}")

    return random_file_id

def synthesize_text_cartesia(text: str, voice: str) -> str:
    
    random_file_id = uuid.uuid4()
    random_filename = f"audio_files/response_{random_file_id}.wav"

    start_timestamp = utils.get_timestamp()

    voice_name = "Barbershop Man"
    voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
    voice = cartesia.voices.get(id=voice_id)

    model_id = "sonic-english"

    output_format = {
        "container": "raw",
        "encoding": "pcm_f32le",
        "sample_rate": 44100,
    }

    p = pyaudio.PyAudio()
    rate = 44100

    stream = None

    # Generate and stream audio
    for output in cartesia.tts.sse(
        model_id=model_id,
        transcript=text,
        voice_embedding=voice["embedding"],
        stream=True,
        output_format=output_format,
    ):
        buffer = output["audio"]

        if not stream:
            stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=True)

        # Write the audio data to the stream
        stream.write(buffer)

    stream.stop_stream()
    stream.close()
    p.terminate()

    return random_file_id


if __name__ == "__main__":
    synthesize_text_cartesia("Hello, how are you?", "Barbershop Man")
