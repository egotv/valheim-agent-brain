from typing import Dict, List
import time
from threading import Thread

from game.agent_command import AgentCommand
from game.game_state import GameState
from memory.log_components import ConversationLineEntry, AgentCommandEntry, GameStateEntry, ReflectionEntry
from thinker.openai_wrapper import run
from utils.analytics import log_async

class PlayerMemory:

    def __init__(self):

        self.conversation_log: List[ConversationLineEntry] = []
        self.agent_commands_log: List[AgentCommandEntry] = []
        self.game_states_log: List[GameStateEntry] = []
        self.reflections_log: List[ReflectionEntry] = []
        self.total_number_of_conversation_entries = 0

    def log_conversation(self, who_said: int, content: str, timestamp: float=time.time()) -> None:
        self.conversation_log.append(ConversationLineEntry(who_said, content, timestamp))
        self.total_number_of_conversation_entries += 1
        self.limit_to_n_items(100)

    def log_agent_commands(self, commands: List[AgentCommand], timestamp: float=time.time()) -> None:
        for command in commands:
            self.agent_commands_log.append(AgentCommandEntry(command, timestamp))
        self.limit_to_n_items(100)

    def log_game_state(self, game_state: GameState, timestamp: float=time.time()) -> None:
        self.game_states_log.append(GameStateEntry(game_state, timestamp))
        self.limit_to_n_items(100)

    # TODO: disable reflection for now
    def should_synthesize_reflection(self) -> bool:
        return False
        # return self.total_number_of_conversation_entries > 0 and self.total_number_of_conversation_entries % 10 == 0

    def synthesize_reflection(self) -> str:

        # Call the LLM to generate a reflection
        prompt = f"""

Generate a reflection based on the past few conversations, actions and game states.
The purpose of the reflection is to help the agent in the future remembers important information and make better decisions.
Keep the reflection to within 25 words.

Conversations:
{self.get_last_n_conversation_lines(10)}

Actions:
{self.get_last_n_agent_commands(5)}

Game States:
{self.get_last_n_game_states(5)}

        """

        reflection = run(prompt)

        log_async("REFLECTION", reflection)

        return reflection
    
    def async_synthesize_log_reflection(self) -> None: # Separate thread

        def synthesize_log_reflection() -> None:
            reflection = self.synthesize_reflection()
            self.log_reflection(reflection)

        t = Thread(target=synthesize_log_reflection)
        t.start()
    
    def log_reflection(self, reflection: str, timestamp: float=time.time()) -> None:
        self.log_reflection.append(ReflectionEntry(reflection, timestamp))
        self.limit_to_n_items(100)

    def get_last_n_conversation_lines(self, n: int) -> List[ConversationLineEntry]:
        return self.conversation_log[-n:]
    
    def get_last_n_agent_commands(self, n: int) -> List[AgentCommandEntry]:
        return self.agent_commands_log[-n:]
    
    def get_last_n_game_states(self, n: int) -> List[GameStateEntry]:
        return self.game_states_log[-n:]
    
    def get_last_n_reflections(self, n: int) -> List[ReflectionEntry]:
        return self.reflections_log[-n:]
    
    def limit_to_n_items(self, n: int):
        self.conversation_log = self.conversation_log[-n:]
        self.agent_commands_log = self.agent_commands_log[-n:]
        self.game_states_log = self.game_states_log[-n:]
        self.reflections_log = self.reflections_log[-n:]
    
class MemoryManager:

    def __init__(self):

        self.player_memories: Dict[str, PlayerMemory] = {}

    def get_player_memory(self, player_id: str) -> PlayerMemory:

        if player_id not in self.player_memories:
            self.player_memories[player_id] = PlayerMemory()
            
        return self.player_memories[player_id]

    


