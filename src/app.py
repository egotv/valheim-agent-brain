import sys
import os
import time
import base64
import uuid
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from flask import Flask, request, send_file
from flask_cors import CORS
from game.game_state import GameState
from brain.brain import Brain
from memory.memory_manager import MemoryManager
import speech.stt as stt
import speech.tts as tts
import memory.log_components as lc
from thinker.claude_thinker import ClaudeThinker
from thinker.openai_thinker import OpenaiThinker
from utils.analytics import log_async

load_dotenv()

app = Flask(__name__)
CORS(app)

# Set up the variables
if os.getenv("THINKER_AI_TOOLKIT") == "claude":
    thinker_class = ClaudeThinker
elif os.getenv("THINKER_AI_TOOLKIT") == "openai":
    thinker_class = OpenaiThinker
else:
    raise ValueError("THINKER_AI_TOOLKIT environment variable must be either 'claude' or 'openai'")

agent_brain = Brain(thinker_class=thinker_class)

# Set up the folder for audio files
os.makedirs("audio_files", exist_ok=True)
for file in os.listdir("audio_files"):
    os.remove(os.path.join("audio_files", file))

@app.route('/hello_world')
def hello_world():
    return "Hello, World!"

@app.route('/instruct_agent', methods=['POST'])
def instruct_agent():

    # Get request arguments
    request_json = request.get_json()
    player_id = request_json['player_id']
    timestamp = request_json.get('timestamp', time.time())
    game_state = GameState.from_json(request_json['game_state'])
    personality = request_json.get('personality', "")
    voice = request_json.get('voice', "asteria")

    # Get the audio file sent through the HTTP POST request
    player_instruction_audio_file_encoded_string = request_json['player_instruction_audio_file_base64']
    player_instruction_audio_file_decoded_bytes = base64.b64decode(player_instruction_audio_file_encoded_string.encode("utf-8"))

    # Save the audio file to the audio_files folder
    player_instruction_audio_file_id = uuid.uuid4()
    player_instruction_audio_file_path = os.path.join("audio_files", f"instruction_{player_instruction_audio_file_id}.wav")
    with open(player_instruction_audio_file_path, "wb") as file:
        file.write(player_instruction_audio_file_decoded_bytes)

    # Convert the audio file to text
    player_instruction = stt.transcribe_audio(player_instruction_audio_file_path)

    # Log the request into the analytics system
    request_dict = {
        "player_id": player_id,
        "timestamp": timestamp,
        "player_instruction": player_instruction,
        "game_state": game_state,
        "personality": personality,
        "voice": voice
    }
    log_async("PLAYER_REQUEST", str(request_dict))

    # Get the output
    output = agent_brain.generate_agent_output(player_instruction, game_state, personality, agent_brain.get_memory_manager().get_player_memory(player_id))

    # Speak the agent text response
    agent_text_response_audio_file_id = tts.synthesize_text(output.agent_text_response, voice)

    # Log this exchange
    agent_brain.get_memory_manager().get_player_memory(player_id).log_conversation(lc.PLAYER_SAID, player_instruction, timestamp)
    agent_brain.get_memory_manager().get_player_memory(player_id).log_conversation(lc.AGENT_SAID, output.agent_text_response, timestamp)
    agent_brain.get_memory_manager().get_player_memory(player_id).log_agent_commands(output.agent_commands, timestamp)
    agent_brain.get_memory_manager().get_player_memory(player_id).log_game_state(game_state, timestamp)

    # Return the output object (agent commands and agent text response audio file)
    output = {
        "player_id": player_id,
        "timestamp": timestamp,
        "player_instruction_transcription": player_instruction,
        "agent_commands": list(map(lambda agent_command: agent_command.to_json(), output.agent_commands)),
        "agent_text_response": output.agent_text_response,
        "agent_text_response_audio_file_id": agent_text_response_audio_file_id,
        "thinker_ai_toolkit": os.getenv("THINKER_AI_TOOLKIT"),
        "personality": personality,
        "voice": voice
    }

    # Log the output into the analytics system
    log_async("AGENT_RESPONSE", str(output))

    return output

@app.route('/get_audio_file', methods=['GET'])
def get_audio_file():

    # Get the ID of the audio file
    audio_file_id = request.args.get('audio_file_id')
    audio_file_path = f"audio_files/response_{audio_file_id}.wav"

    # Return the audio file (quick fix on fly machines)
    fly_path = '/workspace/' + audio_file_path
    local_path = '../' + audio_file_path

    if os.path.exists(fly_path):
        return send_file(fly_path)
    else:
        return send_file(local_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0')