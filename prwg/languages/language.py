from abc import ABC, abstractmethod

class Language(ABC):

    @abstractmethod
    def extension(self) -> str:
        pass

    @abstractmethod
    def identifier(self) -> str:
        pass

    @abstractmethod
    def group(self) -> bool:
        pass