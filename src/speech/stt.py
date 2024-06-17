# Speech to text with whisper

import utils
from thinker.openai_wrapper import transcribe_audio as openai_transcribe_audio

def transcribe_audio(file_path: str, prompt: str="") -> str:

    # Transcribe the file with whisper-1 model
    transcription = openai_transcribe_audio(file_path, prompt=prompt)

    return transcription
