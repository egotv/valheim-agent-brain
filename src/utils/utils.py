from datetime import datetime
import wave
import discord
from io import BufferedIOBase
import pydub

NUMBER_OF_CHANNELS = 2
SAMPLE_WIDTH = 2
FRAME_RATE = 48000

def get_datetime() -> str:
    # Get the datetime up to the microsecond in YYYYMMDD_HHMMSSUUUUUU format
    return datetime.now().strftime("%Y%m%d_%H%M%S%f")

def save_wav_to_disk(new_file_path: str, file_pointer: BufferedIOBase):

    file_pointer.seek(0)

    # Open the output file
    with wave.open(new_file_path, 'wb') as outfile:

        # Set parameters for the output file
        outfile.setnchannels(NUMBER_OF_CHANNELS)
        outfile.setsampwidth(SAMPLE_WIDTH)
        outfile.setframerate(FRAME_RATE)
        outfile.setcomptype('NONE', 'not compressed')

        # Write audio data to the output file
        outfile.writeframes(file_pointer.read())

def reduce_wav_noise(file_path: str): # Reduce noise in the audio file with pydub

    # Load the audio file
    audio = pydub.AudioSegment.from_wav(file_path)

    # Reduce the noise in the audio file
    audio = audio.low_pass_filter(5000)
    audio = audio.high_pass_filter(200)

    # Save the audio file
    new_file_path = f"audio_files/reduced_noise_{get_datetime()}.wav"
    audio.export(new_file_path, format="wav")

    return new_file_path

def get_wav_duration_ms(file_path: str) -> float:

    # Load the audio file
    audio = pydub.AudioSegment.from_wav(file_path)

    # Get the duration of the audio file
    duration = len(audio)

    return duration

def get_wav_mean_loudness(file_path: str) -> float:

    # Load the audio file
    audio = pydub.AudioSegment.from_wav(file_path)

    # Get the mean amplitude of the audio file
    mean_loudness = audio.rms

    return mean_loudness

