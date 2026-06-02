from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto

class GroupFiles(Enum):
    UNIQUE = auto()
    DEDICATED = auto()

@dataclass
class FileConfig:
    group_files: GroupFiles
    extension: str

class FixPosition(Enum):
    BEFORE_IMPORTS = auto()
    AFTER_IMPORTS = auto()

@dataclass
class FileFixes:
    pre_file: tuple[list[str], FixPosition]
    post_file_data: list[str]

@dataclass
class Handle:
    type: str
    name: str

@dataclass
class Pepe:
    declaration_enroll: bool
    code_block_start: str
    code_block_end: str
    statement_end: str

class Language(ABC):

    @abstractmethod
    def identifier(self) -> str:
        """
        Unique identifier for this language.
        """
        pass

    @abstractmethod
    def config(self) -> FileConfig:
        """
        Gets the configuration set for this language.
        """
        pass

    @abstractmethod
    def file_fixes(self) -> FileFixes:
        """
        Gets the pre and post data for each language
        file. Choose if you need the pre data to go
        before the imports.
        """
        pass

    @abstractmethod
    def imports_data(self, types: set[str]) -> set[str]:
        """
        Gets the imports data of a file containing the passed
        types.
        """
        pass

    @abstractmethod
    def pepe(self) -> Pepe:
        """
        TODO
        """
        pass

    @abstractmethod
    def handle_declaration(self, type: str) -> str:
        """
        TODO
        """
        pass

    @abstractmethod
    def handle_data(self) -> list[str]:
        """
        TODO
        """
        pass