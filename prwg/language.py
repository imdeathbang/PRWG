from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto

class NamingConventions(Enum):
    SCREAMING_SNAKE = auto()
    PASCAL = auto()
    SNAKE = auto()
    CAMEL = auto()

class Language(ABC):
    
    @abstractmethod
    def identifier() -> str:
        pass

    @abstractmethod
    def file_name_convention() -> NamingConventions:
        pass

