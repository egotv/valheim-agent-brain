# This class exists to manage the player's instructions in the form of a stream, rather than them being disparate commands.
# We keep the last 15 seconds of instructions

from thinker.openai_wrapper import run

class Instruction:

    def __init__(self, timestamp: float, player_instruction: str):
        self.timestamp: float = timestamp
        self.player_instruction: str = player_instruction

    def to_json(self):
        return {
            "timestamp": self.timestamp,
            "player_instruction": self.player_instruction
        }
    
    def __repr__(self) -> str:
        return f"[{self.timestamp}] {self.player_instruction}"

class RollingPlayerInstructionManager:

    def __init__(self, player_id):
        self.player_id = player_id
        self.instructions = []

    def clear_all_instructions(self):
        self.instructions = []

    def clear_old_instructions(self, timestamp: float):
        self.instructions = [instruction for instruction in self.instructions if instruction.timestamp > timestamp - 15]

    def add_player_instruction(self, timestamp: float, player_instruction: str):
        self.instructions.append(Instruction(timestamp, player_instruction))
        self.clear_old_instructions(timestamp)

    def get_coherent_player_instruction(self) -> str:

        if len(self.instructions) == 0:
            return ""

        instructions_joined_by_newline = "\n".join([instruction.player_instruction for instruction in self.instructions])
        
        prompt = f"""

The following phrases are what a player says, transcribed by a speech-to-text API, broken up into 3-second segments with ends potentially overlapping.

{instructions_joined_by_newline}

Rewrite this into a coherent sentence without overlaps, correcting any words that could have been transcribed wrongly. 
Use the player's words as much as possible. Do not paraphrase. No inverted commas.

        """

        instruction = run(prompt, model='gpt-3.5-turbo')

        return instruction

    