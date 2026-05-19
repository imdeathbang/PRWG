from prwg.languages.language import Language
import prwg.parser as parser
from importlib import util
from pathlib import Path
from prwg.data import *

import argparse

def build(window_data: InitializeInfo):
    pass

def load_language(path: Path) -> Language:
    spec = util.spec_from_file_location(path.stem, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, Language) and obj is not Language:
            return obj()
    return None

def load_languages(languages_folder: Path) -> list[Language]:
    languages: list[Language] = []
    for file_path in languages_folder.glob("*.py"):
        languages.append(load_language(file_path))
    return languages

def main():
    parser = argparse.ArgumentParser()
    init_info = InitializeInfo()
    parser.add_argument("target_directory")
    parser.add_argument("registry_path")
    parser.add_argument("language")

    args = parser.parse_args()
    init_info.target_directory = args.target_directory
    init_info.registry_path = args.registry_path
    init_info.language = args.language