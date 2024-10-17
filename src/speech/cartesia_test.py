from cartesia import Cartesia
import os
import wave
import numpy as np

from dotenv import load_dotenv

load_dotenv()

client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))

# Get all available voices
voices = client.voices.list()
# print(voices)

# Get a specific voice
voice = client.voices.get(id="a0e99841-438c-4a64-b679-ae501e7d6091")
# print("The embedding for", voice["name"], "is", voice["embedding"])

# You can check out our models at https://docs.cartesia.ai/getting-started/available-models
model_id = "sonic-english"

# You can find the supported `output_format`s at https://docs.cartesia.ai/reference/api-reference/rest/stream-speech-server-sent-events
output_format = {
    "container": "raw",
    "encoding": "pcm_s16le",  # Change this to 16-bit PCM
    "sample_rate": 44100,
}

rate = 44100
transcript = "Hello, how are you today?"

# Open a new WAV file for writing
with wave.open("output.wav", "wb") as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes per sample for int16
    wav_file.setframerate(rate)

    # Generate and stream audio
    for output in client.tts.sse(
        model_id=model_id,
        transcript=transcript,
        voice_embedding=voice["embedding"],
        stream=True,
        output_format=output_format,
    ):
        buffer = output["audio"]
        
        # Convert the buffer to a numpy array of int16
        audio_data = np.frombuffer(buffer, dtype=np.int16)
        
        # Write the audio data to the WAV file
        wav_file.writeframes(audio_data.tobytes())

print("Audio saved to output.wav")
