# Text-to-Speech (TTS) module for generating audio files using Deepgram API
import uuid

from deepgram import SpeakOptions
import speech.deepgram_wrapper as deepgram_wrapper

import utils.utils as utils

deepgram = deepgram_wrapper.deepgram

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

    utils.log_timestamp(marker=f"Deepgram TTS Start ({text})")

    response = deepgram.speak.v("1").save(random_filename, payload, deepgram_options, timeout=15)
    response = response.to_dict()
    
    utils.log_timestamp(marker="Deepgram TTS End")

    return random_file_id