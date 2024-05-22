from flask import Flask, request

from brain import Brain
from game.game_state import GameState

app = Flask(__name__)

agent_brain = Brain()

@app.route('/get_agent_commands')
def get_agent_commands():
    
    # Get the player instruction from the query string
    player_instruction = request.args.get('player_instruction')

    # Agent commands
    agent_commands = agent_brain.generate_agent_commands(player_instruction, GameState())

    # Return the agent commands
    return list(map(lambda c: str(c), agent_commands))

if __name__ == '__main__':
    app.run()