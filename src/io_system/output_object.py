from typing import List

from game.agent_command import AgentCommand

class OutputObject:
    
    def __init__(self, agent_commands: List[AgentCommand], agent_text_response: str) -> None:
        self.agent_commands = agent_commands
        self.agent_text_response = agent_text_response

    def __repr__(self) -> str:
        return f"OutputObject(agent_commands={self.agent_commands}, agent_text_response={self.agent_text_response})"