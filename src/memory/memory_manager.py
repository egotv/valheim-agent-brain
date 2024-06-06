from typing import Dict
from memory.rolling_player_instruction import RollingPlayerInstructionManager

class MemoryManager:

    def __init__(self):
        self.rolling_player_instruction_sets: Dict[str, RollingPlayerInstructionManager] = {} # Key: player_id, Value: RollingPlayerInstruction

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

