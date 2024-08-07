from typing import List

from game.game_state import GameState
from memory.memory_manager import PlayerMemory
from game.agent_command import AgentCommand

class InputObject:
    
    def __init__(self, player_instruction: str, game_state: GameState, player_memory: PlayerMemory, personality: str, agent_name: str, retrieved_lists: dict={}, retrieved_knowledge: str="", agent_commands: List[AgentCommand]=None):

        self.player_instruction = player_instruction
        self.game_state = game_state
        self.player_memory = player_memory
        self.personality = personality
        self.retrieved_lists = retrieved_lists
        self.retrieved_knowledge = retrieved_knowledge
        self.agent_commands = agent_commands
        self.agent_name = agent_name
    