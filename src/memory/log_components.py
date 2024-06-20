from game.agent_command import AgentCommand
from game.game_state import GameState

PLAYER_SAID = 0
AGENT_SAID = 1

class ConversationLineEntry:

    def __init__(self, who_said: int, content: str, timestamp: float) -> None:
        self.who_said = who_said
        self.content = content
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return f"ConversationLineEntry(who_said={self.who_said}, content={self.content}, timestamp={self.timestamp})"

class AgentCommandEntry:

    def __init__(self, command: AgentCommand, timestamp: float) -> None:
        self.command = command
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return f"AgentCommandEntry(command={self.command}, timestamp={self.timestamp})"

class GameStateEntry:

    def __init__(self, game_state: GameState, timestamp: float) -> None:
        self.game_state = game_state
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return f"GameStateEntry(game_state={self.game_state}, timestamp={self.timestamp})"
        