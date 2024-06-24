from abc import ABC, abstractmethod
import re
from typing import List, Callable
from threading import Thread

from io_system.input_object import InputObject
from io_system.output_object import OutputObject

class Thinker(ABC):

    @abstractmethod
    def think(self, input: InputObject) -> OutputObject:
        pass

    @staticmethod
    def validate_actions_response(response: str) -> bool:

        if response is None:
            return False

        pattern = r"^\d+(,\d+)*$"
        result = re.match(pattern, response)

        return (result is not None)


