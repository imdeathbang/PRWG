from dataclasses import dataclass
from enum import Enum as enum
from typing import Callable

class InitializeInfo:
    language: str = None
    target_directory: str = None
    registry_path: str = None
    project_name: str = None

    def is_complete(self) -> bool:
        if not self.language:
            return False
        if not self.target_directory:
            return False
        if not self.registry_path:
            return False
        if not self.project_name:
            return False
        return True
    
@dataclass
class Result:
    type: str
    success: str

class ConstructorOptions(enum):
    RETURN_INSTANCE = 0
    OUT_INSTANCE = 1
    RETURN_RESULT_OUT_INSTANCE = 0

@dataclass
class Constructor:
    command: str
    params: list[Param]
    out_name: str
    result: Result | None
    options: ConstructorOptions

@dataclass
class Destructor:
    name: str
    params: list[Param]

@dataclass
class Property:
    type: str
    name: str
    get_name: str
    set_name: str

@dataclass
class Param:
    type: str
    name: str

@dataclass
class Command:
    type: str
    name: str
    params: list[Param]

@dataclass
class Handle:
    type: str
    name: str
    constructor: Constructor
    destructor: Destructor
    properties: list[Property]
    commands: list[Command]

@dataclass
class Enumerator:
    name: str
    value: str

@dataclass
class Enum:
    name: str
    enumerators: list[Enumerator]

@dataclass
class ParsedData:
    handles: list[Handle]
    enums: list[Enum]
    target_directory: str
    project_name: str

@dataclass
class LanguageData:
    process_function: Callable[[ParsedData], None]
    type_dictionary: dict[str, str]