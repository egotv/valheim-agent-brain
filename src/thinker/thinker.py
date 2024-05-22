from abc import ABC, abstractmethod

from io_system.input_object import InputObject
from io_system.output_object import OutputObject

class Thinker(ABC):

    @abstractmethod
    def think(self, input: InputObject) -> OutputObject:
        pass