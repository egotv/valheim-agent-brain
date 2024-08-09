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
from utils.analytics import log_async

class Brain:

    def __init__(self, thinker_class: Type[Thinker]=OpenaiThinker) -> None:
        self.thinker: Thinker = thinker_class()
        self.memory_manager = MemoryManager()
        self.knowledge_base = KnowledgeBaseSystem()

    def get_memory_manager(self) -> MemoryManager:
        return self.memory_manager
    
    def get_knowledge_base(self) -> KnowledgeBaseSystem:
        return self.knowledge_base

    def generate_agent_output(self, player_instruction: str, game_state: GameState, personality: str, player_memory: PlayerMemory, agent_name: str) -> OutputObject:
        
        retrieved_knowledge = json.dumps(self.knowledge_base.lookup_knowledge_base(player_instruction))
        log_async("RETRIEVED_KNOWLEDGE", retrieved_knowledge)

        retrieved_items_list = self.knowledge_base.get_all_items()
        retrieved_monsters_list = self.knowledge_base.get_monsters()
        retrieved_resources_list = self.knowledge_base.get_resources()
        retrieved_lists = {
            "items": retrieved_items_list,
            "monsters": retrieved_monsters_list,
            "resources": retrieved_resources_list
        }

        input = InputObject(player_instruction, game_state, player_memory, personality, agent_name, retrieved_lists=retrieved_lists, retrieved_knowledge=retrieved_knowledge)
        output = self.thinker.think(input)

        return output
