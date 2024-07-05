from abc import ABC, abstractmethod
import re
from typing import List, Callable
from threading import Thread
import json

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
        
        pattern = r'\[ACTIONS\]\s*\[\s*(((".*?")(\s*,\s*)?)*)\s*\]\s*\[TEXT RESPONSE\]\s*(.*)'
        result = re.match(pattern, response)

        return (result is not None)
    
    @staticmethod
    def get_actions_from_raw_response(raw_response: str) -> List[AgentCommand]:

        actions_str = raw_response.split("[ACTIONS]")[1].split("[TEXT RESPONSE]")[0]

        print(actions_str)

        actions_array = json.loads(actions_str)

        actions = []

        for action in actions_array:

            # Split the action string into category, action, and parameters
            # The action string looks like this: "Category_Action(parameter1, parameter2, ...)"
            category, action_parameters = action.split("_")
            action, parameters = action_parameters.split("(")
            parameters = parameters[:-1].split(", ")

            # Remove "" or '' from the parameters
            for i in range(len(parameters)):
                if (parameters[i][0] == "\"" and parameters[i][-1] == "\"") or (parameters[i][0] == "'" and parameters[i][-1] == "'"):
                    parameters[i] = parameters[i][1:-1]

            # Create an AgentCommand object
            agent_command = AgentCommand(category, action, parameters)
            actions.append(agent_command)
        
        return actions
    
    @staticmethod
    def get_text_response_from_raw_response(raw_response: str) -> str:
        
        text_response = raw_response.split("[TEXT RESPONSE]")[1]
        
        return text_response


    



