from abc import ABC, abstractmethod

class Language(ABC):

    @abstractmethod
    def identifier(self) -> str:
        """
        Unique identifier for this language.
        """
        pass

    @abstractmethod
    def extension(self) -> str:
        """
        Extension of the language files.
        (.c, .cs, .py, etc)
        """
        pass

    @abstractmethod
    def group(self) -> bool:
        """
        Gets if all the files will group in a single file under the
        name of the project or every file will have its own name.
        """
        pass

    @abstractmethod
    def pre_file(self) -> tuple[list[str], bool]:
        """
        Gets a list of information that on every language file and
        if it should go before the imports or not.
        """
        pass