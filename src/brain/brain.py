from typing import List, Type
import json

from game.game_state import GameState
from game.agent_command import AgentCommand
from memory.memory_manager import PlayerMemory, MemoryManager
from thinker.thinker import Thinker
from thinker.openai_thinker import OpenaiThinker
from io_system.input_object import InputObject
from io_system.output_object import OutputObject
from brain.knowledge_base import KnowledgeBaseSystem

class Brain:

    def __init__(self, thinker_class: Type[Thinker]=OpenaiThinker) -> None:
        self.thinker: Thinker = thinker_class()
        self.memory_manager = MemoryManager()
        self.knowledge_base = KnowledgeBaseSystem()

    def get_memory_manager(self) -> MemoryManager:
        return self.memory_manager
    
    def get_knowledge_base(self) -> KnowledgeBaseSystem:
        return self.knowledge_base

    def generate_agent_output(self, player_instruction: str, game_state: GameState, player_memory: PlayerMemory) -> OutputObject:
        
        retrieved_knowledge = json.dumps(self.knowledge_base.lookup_knowledge_base(player_instruction))
        print(retrieved_knowledge, flush=True)

        input = InputObject(player_instruction, game_state, player_memory, retrieved_knowledge=retrieved_knowledge)
        output = self.thinker.think(input)

        return output
