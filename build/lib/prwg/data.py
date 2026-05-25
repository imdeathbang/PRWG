from dataclasses import dataclass
from enum import Enum, auto

class InitializeInfo:
    target_directory: str = None
    registry_path: str = None
    language: str = None

    def is_complete(self) -> bool:
        if not self.language:
            return False
        if not self.target_directory:
            return False
        if not self.registry_path:
            return False
        return True
    
@dataclass
class Result:
    type: str
    success: str

class ConstructorOptions(Enum):
    RETURN_RESULT_OUT_INSTANCE = auto()
    RETURN_INSTANCE = auto()
    OUT_INSTANCE = auto()

@dataclass
class Param:
    type: str
    name: str

@dataclass
class Constructor:
    command: str
    params: list[Param]
    out_name: str
    result: Result | None
    options: ConstructorOptions

@dataclass
class Destructor:
    command: str
    params: list[Param]

@dataclass
class Property:
    type: str
    name: str
    get_name: str
    set_name: str

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
class ParsedEnum:
    type: str
    name: str
    enumerators: list[Enumerator]

@dataclass
class ParsedData:
    handles: list[Handle]
    enums: list[ParsedEnum]
    target_directory: str
    project_name: str