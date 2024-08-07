from game.agent_command import AgentCommand
from game.game_state import GameState
from typing import List

PLAYER_SAID = 0
AGENT_SAID = 1

class ConversationLineEntry:

    def __init__(self, who_said: str, content: str, timestamp: float) -> None:
        self.who_said = who_said
        self.content = content
        self.timestamp = timestamp

    def __str__(self) -> str:
        return f"{self.who_said} said: {self.content}"

    def __repr__(self) -> str:
        return self.__str__()
   
# Filter by index of first who_said to last who_said
def filter_by_who_said(entries: List[ConversationLineEntry], who_said: str) -> List[ConversationLineEntry]:
    start_index = -1
    end_index = -1
    for index, entry in enumerate(entries):
        if entry.who_said == who_said:
            if start_index == -1:
                start_index = index
            end_index = index
    if start_index != -1 and end_index != -1:
        return entries[start_index-1:end_index + 1]
    return []

class AgentCommandEntry:

    def __init__(self, command: AgentCommand, timestamp: float) -> None:
        self.command = command
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return f"{self.command}"

class GameStateEntry:

    def __init__(self, game_state: GameState, timestamp: float) -> None:
        self.game_state = game_state
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return f"GameStateEntry(game_state={self.game_state}, timestamp={self.timestamp})"

# Reflection is what the agent synthesizes from the past few conversations, actions and game states
class ReflectionEntry:

    def __init__(self, reflection: str, timestamp: float) -> None:
        self.reflection = reflection
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return f"ReflectionEntry(reflection={self.reflection}, timestamp={self.timestamp})"
        