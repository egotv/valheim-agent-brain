from typing import Dict
from memory.rolling_player_instruction import RollingPlayerInstructionManager

class MemoryManager:

    def __init__(self):
        self.rolling_player_instruction_sets: Dict[str, RollingPlayerInstructionManager] = {} # Key: player_id, Value: RollingPlayerInstruction

    def add_player_instruction(self, player_id: str, player_instruction: str, timestamp: float) -> bool:
        
        if player_id not in self.rolling_player_instruction_sets:
            self.rolling_player_instruction_sets[player_id] = RollingPlayerInstructionManager(player_id)

        self.rolling_player_instruction_sets[player_id].add_player_instruction(timestamp, player_instruction)
        has_player_finished_speaking = self.rolling_player_instruction_sets[player_id].has_player_finished_speaking()

        return has_player_finished_speaking

    def get_coherent_player_instruction(self, player_id: str) -> str:

        if player_id not in self.rolling_player_instruction_sets:
            return None

        return self.rolling_player_instruction_sets[player_id].get_coherent_player_instruction()

