from typing import Dict, List
import time

from memory.rolling_player_instruction import RollingPlayerInstructionManager
from game.agent_command import AgentCommand
from game.agent_commands_list import AgentCommandsList
from game.game_state import GameState

class MemoryManager:

    def __init__(self):

        self.rolling_player_instruction_sets: Dict[str, RollingPlayerInstructionManager] = {} # Key: player_id, Value: RollingPlayerInstruction
        self.agent_commands_sets: Dict[str, AgentCommandsList] = {} # Key: player_id, Value: List[AgentCommand]
        self.game_state_sets: Dict[str, GameState] = {} # Key: player_id, Value: GameState

    def add_player_instruction(self, player_id: str, player_instruction: str, timestamp: float):
        
        if player_id not in self.rolling_player_instruction_sets:
            self.rolling_player_instruction_sets[player_id] = RollingPlayerInstructionManager(player_id)

        self.rolling_player_instruction_sets[player_id].add_player_instruction(timestamp, player_instruction)

    def get_coherent_player_instruction(self, player_id: str) -> str:

        if player_id not in self.rolling_player_instruction_sets:
            return None

        return self.rolling_player_instruction_sets[player_id].get_coherent_player_instruction()
    
    def clear_all_instructions(self, player_id: str):
        if player_id in self.rolling_player_instruction_sets:
            self.rolling_player_instruction_sets[player_id].clear_all_instructions()

    def does_player_have_instructions(self, player_id: str) -> bool:
        return player_id in self.rolling_player_instruction_sets and len(self.rolling_player_instruction_sets[player_id].instructions) > 0
    
    def set_agent_commands(self, player_id: str, agent_commands: List[AgentCommand]):
        self.agent_commands_sets[player_id] = AgentCommandsList(agent_commands)

    def get_agent_commands(self, player_id: str) -> AgentCommandsList:
        return self.agent_commands_sets.get(player_id, AgentCommandsList([], time.time()))
    
    def set_game_state(self, player_id: str, game_state: GameState):
        self.game_state_sets[player_id] = game_state

    def get_game_state(self, player_id: str) -> GameState:
        return self.game_state_sets.get(player_id, GameState("No game state available"))
    


