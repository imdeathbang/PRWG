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
class Pepe:
    module_enroll: bool
    code_block_start: str
    code_block_end: str
    statement_end: str

@dataclass
class ParamInfo:
    type: str
    name: str

@dataclass
class ResultInfo:
    success: str
    type: str

@dataclass
class OutInfo:
    name: str
    result_info: ResultInfo | None

@dataclass
class ConstructorInfo:
    command: str
    params: list[ParamInfo]
    out_info: OutInfo | None

@dataclass
class DestructorInfo:
    command: str
    params: list[ParamInfo]

@dataclass
class PropertyInfo:
    type: str
    name: str
    get_command_name: str
    set_command_name: str

@dataclass
class CommandInfo:
    type: str
    name: str
    params: list[ParamInfo]

@dataclass
class HandleInfo:
    type: str
    name: str
    constructor_info: ConstructorInfo
    destructor_info: DestructorInfo
    properties_info: list[PropertyInfo]
    commands_info: list[CommandInfo]

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
    def handle_data(self, handle_info: HandleInfo) -> list[str]:
        """
        TODO
        """
        pass