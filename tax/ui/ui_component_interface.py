from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable


class InputTypes(Enum):
    Input = 'input'
    Select = 'select'


class UiComponentInterface(ABC):
    def __init__(self, name: str = None, label: str = None, cast: Callable = None, validator: Callable = None):
        self.name = name
        self.label = label
        self.cast = cast
        self.validator = validator

    @abstractmethod
    def get_default_value(self):
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass
