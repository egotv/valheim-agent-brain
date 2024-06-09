import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from flask import Flask, request
from flask_cors import CORS
from game.game_state import GameState
from brain.brain import Brain
from memory.memory_manager import MemoryManager

app = Flask(__name__)
CORS(app)

# Set up the variables
agent_brain = Brain()
memory_manager = MemoryManager()

@app.route('/hello_world')
def hello_world():
    return "Hello, World!"

@app.route('/post_player_instruction', methods=['POST'])
def post_player_instruction():

    # Get request arguments
    player_id = request.args.get('player_id')
    player_this_instruction = request.args.get('player_instruction')
    timestamp = request.args.get('timestamp', time.time(), float)

    # Player has finished speaking if the instruction is empty string
    if player_this_instruction == "" and memory_manager.does_player_have_instructions(player_id):

        game_state = memory_manager.get_game_state(player_id)
        coherent_player_instruction = memory_manager.get_coherent_player_instruction(player_id)
        memory_manager.clear_all_instructions(player_id)

        output = agent_brain.generate_agent_output(coherent_player_instruction, game_state)
        memory_manager.set_agent_commands(player_id, output.agent_commands)

        return {
            "coherent_player_instruction": coherent_player_instruction,
            "agent_commands": list(map(lambda agent_command: agent_command.to_json(), output.agent_commands)),
            "agent_text_response": output.agent_text_response
        }

    # Player has not finished speaking
    elif player_this_instruction != "":
        memory_manager.add_player_instruction(player_id, player_this_instruction, timestamp)

    # Nothing to return
    return {
        "coherent_player_instruction": None,
        "agent_commands": None,
        "agent_text_response": None
    }
    
@app.route('/post_game_state', methods=['POST'])
def post_game_state():

    request_json = request.get_json()

    player_id = request_json['player_id']
    memory_manager.set_game_state(player_id, GameState.from_json(request_json['game_state']))

    return {
        "success": True
    }

@app.route('/get_agent_commands')
def get_agent_commands():

    player_id = request.args.get('player_id')
    agent_commands_list = memory_manager.get_agent_commands(player_id)
    
    return {
        "agent_commands": list(map(lambda agent_command: agent_command.to_json(), agent_commands_list.commands)),
        "timestamp": agent_commands_list.timestamp
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0')