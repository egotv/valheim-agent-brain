import os
from openai import OpenAI
from dotenv import load_dotenv
import utils.utils as utils

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def run(prompt: str, model="gpt-4o", temperature=1.0) -> str:

    utils.log_timestamp(marker="OpenAI Completions Start")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    result = response.choices[0].message.content
    utils.log_timestamp(marker=f"OpenAI Completions End ({result})")

    return result

def transcribe_audio(file_path: str, prompt: str="") -> str:
    
    audio_file= open(file_path, "rb")

    utils.log_timestamp(marker="OpenAI Transcription Start")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        language="en",
        file=audio_file,
        prompt=prompt
    )
    result = transcription.text
    utils.log_timestamp(marker=f"OpenAI Transcription End ({result})")

    return result