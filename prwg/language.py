from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto

class NamingConventions(Enum):
    SCREAMING_SNAKE = auto()
    PASCAL = auto()
    SNAKE = auto()
    CAMEL = auto()

@dataclass
class ContainerInfo:
    pre: str
    joiner: str
    end: str

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
    def assemble_enum(self, name: str, value: str):
        pass

    @abstractmethod
    def result_imports(self) -> set[str]:
        pass

    @abstractmethod
    def result_pre(self, name: str) -> str:
        pass

    @abstractmethod
    def result_container(self, name: str) -> ContainerInfo:
        pass

