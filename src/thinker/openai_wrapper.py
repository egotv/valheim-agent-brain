import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def run(prompt: str, model="gpt-4o", temperature=1.0) -> str:

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )

    return response.choices[0].message.content

def transcribe_audio(file_path: str, prompt: str="") -> str:
    
    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        language="en",
        file=audio_file,
        prompt=prompt
    )

    return transcription.text