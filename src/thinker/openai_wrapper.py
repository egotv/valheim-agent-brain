import os
from openai import OpenAI
from dotenv import load_dotenv
import utils.utils as utils
from utils.analytics import log_async

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
lemonfox_client = OpenAI(
    api_key=os.environ.get("LEMONFOX_API_KEY"),
    base_url="https://api.lemonfox.ai/v1",
)


def run(prompt: str, model="gpt-4o", temperature=0.9) -> str:

    start_timestamp = utils.get_timestamp()

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    result = response.choices[0].message.content

    time_elapsed = utils.get_timestamp() - start_timestamp
    log_async("OPENAI_CHAT_LATENCY", f"{time_elapsed}")
    log_async("OPENAI_CHAT_RESPONSE", f"{response}")
    log_async("OPENAI_CHAT_PROMPT", f"{prompt}")

    return result


def transcribe_audio(file_path: str, prompt: str = "") -> str:

    start_timestamp = utils.get_timestamp()

    audio_file = open(file_path, "rb")

    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        language="en",
        file=audio_file,
        prompt=prompt
    )
    result = transcription.text

    time_elapsed = utils.get_timestamp() - start_timestamp
    log_async("OPENAI_AUDIO_LATENCY", f"{time_elapsed}")

    return result


def transcribe_audio_lemonfox(file_path: str, prompt: str = "") -> str:

    start_timestamp = utils.get_timestamp()

    audio_file = open(file_path, "rb")

    transcription = lemonfox_client.audio.transcriptions.create(
        model="whisper-1",
        language="en",
        file=audio_file,
    )
    result = transcription.text

    time_elapsed = utils.get_timestamp() - start_timestamp
    log_async("LEMONFOX_AUDIO_LATENCY", f"{time_elapsed}")

    return result
