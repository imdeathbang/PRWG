from abc import ABC, abstractmethod
from enum import Enum, auto

class NamingConventions(Enum):
    SCREAMING_SNAKE = auto()
    PASCAL = auto()
    SNAKE = auto()
    CAMEL = auto()

class Language(ABC):
    
    @abstractmethod
    def identifier(self) -> str:
        pass

    @abstractmethod
    def extension(self) -> str:
        pass

    @abstractmethod
    def assemble_file_name(self, words: list[str]) -> str:
        pass

    @abstractmethod
    def assemble_module_name(self, words: list[str]) -> str:
        pass

    @abstractmethod
    def result_imports(self) -> set[str]:
        pass

