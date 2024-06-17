import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from flask import Flask, request, send_file
from flask_cors import CORS
from game.game_state import GameState
from brain.brain import Brain
from memory.memory_manager import MemoryManager
import speech.stt as stt
import speech.tts as tts

app = Flask(__name__)
CORS(app)

# Set up the variables
agent_brain = Brain()
memory_manager = MemoryManager()

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
    game_state = GameState.from_json(request_json.get('game_state'))

    # Get the audio file sent through the HTTP POST
    player_instruction_audio_file = request.files['player_instruction_audio_file']
    player_instruction_audio_file_path = f"audio_files/{player_id}_{timestamp}.wav"
    player_instruction_audio_file.save(player_instruction_audio_file_path)

    # Convert the audio file to text
    player_instruction = stt.transcribe_audio(player_instruction_audio_file_path)

    # Get the output
    output = agent_brain.generate_agent_output(player_instruction, game_state)

    # Speak the agent text response
    agent_text_response_audio_file_path = tts.synthesize_text(output.agent_text_response)

    # Return the output object (agent commands and agent text response audio file)
    return {
        "player_instruction_transcription": player_instruction,
        "agent_commands": list(map(lambda agent_command: agent_command.to_json(), output.agent_commands)),
        "agent_text_response": output.agent_text_response,
        "agent_text_response_audio_file_path": agent_text_response_audio_file_path
    }

@app.route('/get_audio_file', methods=['GET'])
def get_audio_file():

    # Get the path of the audio file
    audio_file_path = request.args.get('audio_file_path')

    # Return the audio file
    return send_file(audio_file_path)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')