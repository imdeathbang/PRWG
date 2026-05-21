from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class LanguageConfig:
    group_files: bool
    extension: str

@dataclass
class FileFixes:
    post_file_data: list[str]
    pre_file_data: list[str]
    before_imports: bool = True

class Language(ABC):

    @abstractmethod
    def identifier(self) -> str:
        """
        Unique identifier for this language.
        """
        pass

    @abstractmethod
    def config(self) -> LanguageConfig:
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