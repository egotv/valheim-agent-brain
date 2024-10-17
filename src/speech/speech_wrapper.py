from deepgram import DeepgramClient, PrerecordedOptions, ClientOptionsFromEnv, FileSource
from dotenv import load_dotenv
from cartesia import Cartesia
import os

load_dotenv()

# Set up Deepgram
deepgram: DeepgramClient = DeepgramClient("", ClientOptionsFromEnv())

cartesia: Cartesia = Cartesia(api_key=os.getenv("CARTEISA_API_KEY"))
