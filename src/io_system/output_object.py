from typing import List

from game.agent_command import AgentCommand

class OutputObject:
    
    def __init__(self, agent_commands: List[AgentCommand]):
        self.agent_commands = agent_commands

    def __repr__(self) -> str:
        return "\n".join(map(lambda agent_command: agent_command.__repr__(), self.agent_commands))