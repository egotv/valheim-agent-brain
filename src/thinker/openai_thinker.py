import os
from dotenv import load_dotenv
from typing import List

from thinker.thinker import Thinker
from io_system.input_object import InputObject
from io_system.output_object import OutputObject
from game.agent_command import AgentCommand
from thinker.openai_wrapper import run

load_dotenv()

class OpenaiThinker(Thinker):

    def __init__(self) -> None:
        self.game_name = "Valheim"

    def think(self, input: InputObject) -> OutputObject:
        
        # Get actions
        actions = self.get_actions(input)

        # Get the text response
        text_response = self.get_text_response(input, actions)

        # Return the set of actions
        return OutputObject(actions, text_response)
    
    def get_actions(self, input: InputObject) -> List[AgentCommand]:
        
         # Given a set of input (player instruction, game state), determine a set of actions to take for the agent
        actions_prompt = self.generate_actions_prompt(input)

        # Get the actions
        actions_raw = run(actions_prompt)
        if not Thinker.validate_actions_response(actions_raw):
            actions_raw = None

        # Split the response by new line and remove any empty strings
        if actions_raw is None:
            actions = []
        else:
            action_codes_str = list(filter(None, actions_raw.split(",")))
            action_codes = list(map(lambda action_code_str: int(action_code_str), action_codes_str))
            actions = list(map(lambda action_code: AgentCommand(action_code, AgentCommand.get_action_str_from_code(action_code)), action_codes))

        return actions
    
    def get_text_response(self, input: InputObject, actions: List[AgentCommand]) -> str:

        # Get the text response
        input = InputObject(input.player_instruction, input.game_state, input.player_memory, actions)
        text_response_prompt = self.generate_text_response_prompt(input)
        text_response = run(text_response_prompt)

        return text_response
    
    def get_crafting_recipes(self, input: InputObject) -> List[str]:
        pass
    
    def generate_actions_prompt(self, input: InputObject) -> str:
        
        return f"""
        
You are an AI agent who is a virtual companion for a player playing {self.game_name}.

The player has just given you the following instruction:
{input.player_instruction}

The current state of the game is as follows:
{input.game_state}

You are required to generate an action that the agent should take in response to the player instruction and the game state.
The actions that you can take are as follows:

1. StartFollowingPlayer
2. StartAttacking
3. StartHarvesting
4. StartPatrolling

Please generate zero or one action that the agent should take in response to the player instruction and the game state. 
If you do not want to take any actions, please enter NO_ACTIONS.
Output the action code in the following format as illustrated in the example below.
Do not include any additional information in the output, only the action code.

Example 1:
4

Example 2 (no actions):
NO_ACTIONS

        """
    
    def generate_text_response_prompt(self, input: InputObject) -> str:

        return f"""

You are an AI agent who is a virtual companion for a player playing {self.game_name}.

The player has just given you the following instruction:
{input.player_instruction}

The history of the last five exchanges between the player and the agent is as follows:
{input.player_memory.get_last_n_conversation_lines(10)}

The current state of the game is as follows:
{input.game_state}

You are performing the following actions in response to the player instruction and the game state:
{input.agent_commands}

Respond to the player in a fun and playful manner. Tease the player a little bit, but also provide them with some useful information.
Respond in less than 15 words.

        """
