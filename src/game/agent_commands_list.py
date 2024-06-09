from typing import List
import time

from game.agent_command import AgentCommand

class AgentCommandsList:
    
    def __init__(self, commands: List[AgentCommand], timestamp: float=time.time()) -> None:
        self.commands = commands
        self.timestamp = timestamp