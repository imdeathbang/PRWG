from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ParamInfo:
    type: str
    name: str

@dataclass
class ConstructorInfo:
    params: list[ParamInfo]

@dataclass
class HandleInfo:
    name: str

@dataclass
class RegistryInfo:
    namespace: str
    diminutive: str
    prefix: str

class Language(ABC):
    
    @abstractmethod
    def identifier() -> str:
        pass