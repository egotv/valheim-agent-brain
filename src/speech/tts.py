# Text-to-Speech (TTS) module for generating audio files using Deepgram API
import uuid

from deepgram import SpeakOptions
import speech.speech_wrapper as speech_wrapper

import utils.utils as utils
from utils.analytics import log_async
import numpy as np
import wave

deepgram = speech_wrapper.deepgram
cartesia = speech_wrapper.cartesia

def synthesize_text(text: str, voice_name: str) -> str:

    payload = {
        "text": text
    }

    deepgram_options: SpeakOptions = SpeakOptions(
        model=f"aura-{voice_name}-en",
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

def synthesize_text_cartesia(text: str, voice_name: str) -> str:
    random_file_id = uuid.uuid4()
    random_filename = f"audio_files/response_{random_file_id}.wav"

    start_timestamp = utils.get_timestamp()

    voice_name = "Barbershop Man"
    voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
    voice = cartesia.voices.get(id=voice_id)

    model_id = "sonic-english"

    output_format = {
    "container": "raw",
    "encoding": "pcm_s16le",  # Change this to 16-bit PCM
    "sample_rate": 44100,
    }

    rate = 44100

    try:
        # Open a new WAV file for writing
        with wave.open(random_filename, "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample for int16
            wav_file.setframerate(rate)

            # Generate and stream audio
            for output in cartesia.tts.sse(
                model_id=model_id,
                transcript=text,
                voice_embedding=voice["embedding"],
                stream=True,
                output_format=output_format,
            ):
                buffer = output["audio"]
                
                # Convert the buffer to a numpy array of int16
                audio_data = np.frombuffer(buffer, dtype=np.int16)
                
                # Write the audio data to the WAV file
                wav_file.writeframes(audio_data.tobytes())
        time_elapsed = utils.get_timestamp() - start_timestamp
        log_async("CARTESIA_TTS_LATENCY", f"{time_elapsed}")
    
    except Exception as e:
        print(f"Exception: {e}")
        log_async("CARTESIA_ERROR", f"Exception: {e}")

    print(f"Audio saved to {random_filename}")
    return random_file_id


if __name__ == "__main__":
    synthesize_text_cartesia("Hello, how are you?", "Barbershop Man")
