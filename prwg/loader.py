from prwg.language import Language
from importlib import util
from pathlib import Path

def _language(path: Path) -> Language | None:
    file_name = path.stem

    spec = util.spec_from_file_location(file_name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for name in dir(module):
        obj = getattr(module, name)
        
        if isinstance(obj, type) and issubclass(obj, Language) and obj is not Language:
            return obj()
        
    return None

def languages(path: Path) -> list[Language]:
    languages: list[Language] = []

    for language_path in path.glob("*.py"):
        language = _language(language_path)

        if language is not None:
            languages.append(language)

    return languages