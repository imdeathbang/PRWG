from prwg.language import Language
from importlib import util
from pathlib import Path

def load_language(language_path: Path) -> Language | None:
    language_name = language_path.stem

    spec = util.spec_from_file_location(language_name, language_path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, Language) and obj is not Language:
            return obj()
        
    return None

def load_languages(folder_path: Path) -> list[Language]:
    languages: list[Language] = []

    for language_path in folder_path.glob("*.py"):
        language = load_language(language_path)
        if language is not None:
            languages.append(language)

    return languages