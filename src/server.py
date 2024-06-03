from flask import Flask, request

from brain import Brain
from game.game_state import GameState

app = Flask(__name__)

agent_brain = Brain()

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
    app.run()