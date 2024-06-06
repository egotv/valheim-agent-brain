import os
from dotenv import load_dotenv
import re

from thinker.thinker import Thinker
from io_system.input_object import InputObject
from io_system.output_object import OutputObject
from game.agent_command import AgentCommand
from thinker.openai_wrapper import run

load_dotenv()

class OpenaiThinker(Thinker):

    def __init__(self) -> None:
        self.game_name = os.environ.get("GAME_NAME")

    def think(self, input: InputObject) -> OutputObject:
        
        # Given a set of input (player instruction, game state), determine a set of actions to take for the agent
        actions_prompt = self.generate_actions_prompt(input)
        text_response_prompt = self.generate_text_response_prompt(input)

        # Get the actions
        actions_raw = run(actions_prompt)
        if not self.validate_actions_response(actions_raw):
            actions_raw = None

        # Split the response by new line and remove any empty strings
        if actions_raw is None:
            actions = []
        else:
            action_codes_str = list(filter(None, actions_raw.split("\n")))
            action_codes = list(map(lambda action_code_str: int(action_code_str), action_codes_str))
            actions = list(map(lambda action_code: AgentCommand(action_code, AgentCommand.get_action_str_from_code(action_code)), action_codes))

        # Get the text response (TODO: The text response should include the actions taken by the agent)
        text_response = run(text_response_prompt)

        # Return the set of actions
        return OutputObject(actions, text_response)
    
    def generate_actions_prompt(self, input: InputObject) -> str:
        
        return f"""
        
You are an AI agent who is a virtual companion for a player playing {self.game_name}.

The player has just given you the following instruction:
{input.player_instruction}

The current state of the game is as follows:
{input.game_state}

You are required to generate a set of actions that the agent should take in response to the player instruction and the game state.
The actions that you can take are as follows:

1. Follow the player
2. Get wood
3. Get stone

Please generate a set of actions that the agent should take in response to the player instruction and the game state. 
Output the action codes in the following format as illustrated in the example below.
Do not include any additional information in the output, only the action codes.

Example:

1
3

        """
    
    def generate_text_response_prompt(self, input: InputObject) -> str:

        return f"""

You are an AI agent who is a virtual companion for a player playing {self.game_name}.

The player has just given you the following instruction:
{input.player_instruction}

Respond to the player in a fun and playful manner. Tease the player a little bit, but also provide them with some useful information.
Respond in less than 15 words.

        """
    
    def validate_actions_response(self, response: str) -> bool:

        pattern = r'^(0|[1-9]\d*)(?:\r?\n|$)+'
        if re.fullmatch(pattern, response):
            return True
        else:
            return False
