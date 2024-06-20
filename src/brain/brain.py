from typing import List

from game.game_state import GameState
from game.agent_command import AgentCommand
from memory.memory_manager import PlayerMemory, MemoryManager
from thinker.openai_thinker import OpenaiThinker
from io_system.input_object import InputObject
from io_system.output_object import OutputObject

class Brain:

    def __init__(self) -> None:
        self.thinker = OpenaiThinker()
        self.memory_manager = MemoryManager()

    def get_memory_manager(self) -> MemoryManager:
        return self.memory_manager

    def generate_agent_output(self, player_instruction: str, game_state: GameState, player_memory: PlayerMemory) -> OutputObject:
        
        input = InputObject(player_instruction, game_state, player_memory)
        output = self.thinker.think(input)

        return output
