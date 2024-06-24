from typing import Dict, List
import time

from game.agent_command import AgentCommand
from game.game_state import GameState
from memory.log_components import ConversationLineEntry, AgentCommandEntry, GameStateEntry

class PlayerMemory:

    def __init__(self):

        self.conversation_log: List[ConversationLineEntry] = []
        self.agent_commands_log: List[AgentCommandEntry] = []
        self.game_states_log: List[GameStateEntry] = []

    def log_conversation(self, who_said: int, content: str, timestamp: float=time.time()) -> None:
        self.conversation_log.append(ConversationLineEntry(who_said, content, timestamp))
        self.limit_to_n_items(100)

    def log_agent_commands(self, commands: List[AgentCommand], timestamp: float=time.time()) -> None:
        for command in commands:
            self.agent_commands_log.append(AgentCommandEntry(command, timestamp))
        self.limit_to_n_items(100)

    def log_game_state(self, game_state: GameState, timestamp: float=time.time()) -> None:
        self.game_states_log.append(GameStateEntry(game_state, timestamp))
        self.limit_to_n_items(100)

    def get_last_n_conversation_lines(self, n: int) -> List[ConversationLineEntry]:
        return self.conversation_log[-n:]
    
    def get_last_n_agent_commands(self, n: int) -> List[AgentCommandEntry]:
        return self.agent_commands_log[-n:]
    
    def get_last_n_game_states(self, n: int) -> List[GameStateEntry]:
        return self.game_states_log[-n:]
    
    def limit_to_n_items(self, n: int):
        self.conversation_log = self.conversation_log[-n:]
        self.agent_commands_log = self.agent_commands_log[-n:]
        self.game_states_log = self.game_states_log[-n:]
    
class MemoryManager:

    def __init__(self):

        self.player_memories: Dict[str, PlayerMemory] = {}

    def get_player_memory(self, player_id: str) -> PlayerMemory:

        if player_id not in self.player_memories:
            self.player_memories[player_id] = PlayerMemory()
            
        return self.player_memories[player_id]

    


