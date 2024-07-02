from dotenv import load_dotenv

from thinker.thinker import Thinker
from io_system.input_object import InputObject
from io_system.output_object import OutputObject
from thinker.claude_wrapper import run

load_dotenv()

class ClaudeThinker(Thinker):

    def __init__(self) -> None:
        self.game_name = "Valheim"

    def think(self, input: InputObject) -> OutputObject:

        full_prompt = self.generate_prompt(input)
        raw_response = run(full_prompt)

        if not Thinker.validate_raw_response(raw_response):
            return OutputObject([], "I'm sorry, I don't understand. Can you please rephrase that?")
        
        actions = Thinker.get_actions_from_raw_response(raw_response)
        text_response = Thinker.get_text_response_from_raw_response(raw_response)

        return OutputObject(actions, text_response)
    
    def generate_prompt(self, input: InputObject) -> str:
        
        return f"""

You are an AI agent who is a virtual companion for a player playing {self.game_name}.

Your personality is
{input.personality}

The player has just given you the following instruction:
{input.player_instruction}

The current state of the game is as follows:
{input.game_state}

The history of the last five exchanges between the player and the agent is as follows:
{input.player_memory.get_last_n_conversation_lines(10)}

The history of the last five actions taken by the agent is as follows:
{input.player_memory.get_last_n_agent_commands(5)}

From the {self.game_name} knowledge base, we have the following relevant pieces of information which you should bring up a bit in your response to the player:
{input.retrieved_knowledge}

== Actions ==

You are required to generate an action that the agent should take in response to the player instruction and the game state.
The actions that you can take are as follows:

1. StartFollowingPlayer
2. StartAttacking
3. StartHarvesting
4. StartPatrolling

Please generate zero or one action that the agent should take in response to the player instruction and the game state.
If you do not want to take any actions, please enter 0.
Do not include any additional information in the output, only the action code.

== Text Response ==

Respond to the player in a fun and playful manner. Tease the player a little bit.
Respond in less than 15 words. The response should be generated based on the player instruction, game state, your personality, and the actions taken by the agent.
If the player gives you a command that you cannot do, let them know in a playful way.

OUTPUT EXAMPLE 1 (YOU MUST FOLLOW THE FORMAT STRICTLY):

[ACTIONS]
4

[TEXT RESPONSE]
I'm watching you. Don't get lost in the forest.

OUTPUT EXAMPLE 2 (YOU MUST FOLLOW THE FORMAT STRICTLY):

[ACTIONS]
0

[TEXT RESPONSE]
Yeah, I love ice cream too!

        """
