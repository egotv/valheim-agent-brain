from deepgram import DeepgramClient, PrerecordedOptions, ClientOptionsFromEnv, FileSource
from dotenv import load_dotenv

load_dotenv()

# Set up Deepgram
deepgram: DeepgramClient = DeepgramClient("", ClientOptionsFromEnv())