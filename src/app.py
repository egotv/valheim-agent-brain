import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from flask import Flask, request
from flask_cors import CORS
from game.game_state import GameState
from brain.brain import Brain

app = Flask(__name__)
CORS(app)

agent_brain = Brain()

@app.route('/hello_world')
def hello_world():
    return "Hello, World!"

@app.route('/get_agent_output')
def get_agent_output():

    player_instruction = request.args.get('player_instruction')

    game_state = GameState() # TODO: Implement the game state

    output = agent_brain.generate_agent_output(player_instruction, game_state)

    return {
        "agent_commands": list(map(lambda agent_command: agent_command.to_json(), output.agent_commands)),
        "agent_text_response": output.agent_text_response
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0')