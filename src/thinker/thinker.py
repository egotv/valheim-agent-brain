from abc import ABC, abstractmethod
import re
from typing import List, Callable
from threading import Thread

from io_system.input_object import InputObject
from io_system.output_object import OutputObject
from game.agent_command import AgentCommand

class Thinker(ABC):

    @abstractmethod
    def think(self, input: InputObject) -> OutputObject:
        pass
    
    @staticmethod
    def validate_raw_response(response: str) -> bool:
        
        if response is None:
            return False
        
        pattern = r"^\[ACTIONS\]\s\d+(,\d+)*\s*\[TEXT RESPONSE\]\s.*$"
        result = re.match(pattern, response)

        return (result is not None)
    
    @staticmethod
    def get_actions_from_raw_response(raw_response: str) -> List[AgentCommand]:

        actions_str = raw_response.split("[ACTIONS]")[1].split("[TEXT RESPONSE]")[0]
        actions_int = list(map(int, actions_str.split(",")))

        if len(actions_int) == 1 and actions_int[0] == 0:
            actions_int = []

        actions = list(map(lambda action_code: AgentCommand(action_code, AgentCommand.get_action_str_from_code(action_code)), actions_int))
        
        return actions
    
    @staticmethod
    def get_text_response_from_raw_response(raw_response: str) -> str:
        
        text_response = raw_response.split("[TEXT RESPONSE]")[1]
        
        return text_response



