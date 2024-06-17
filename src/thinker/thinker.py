from abc import ABC, abstractmethod
import re

from io_system.input_object import InputObject
from io_system.output_object import OutputObject

class Thinker(ABC):

    @abstractmethod
    def think(self, input: InputObject) -> OutputObject:
        pass

    @staticmethod
    def validate_actions_response(response: str) -> bool:

        pattern = r'^(0|[1-9]\d*)(?:\r?\n|$)+'
        if re.fullmatch(pattern, response):
            return True
        else:
            return False
