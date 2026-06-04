from dataclasses import dataclass
import prwg.language_loader as language_loader
from prwg.language import Language
from pathlib import Path
import argparse

@dataclass
class CliInfo:
    registry_path: Path
    target_path: Path
    language: str

def start() -> CliInfo:
    languages = language_loader.instantiate_languages()
    identifier_language: dict[str, Language] = {}

    for language in languages:
        identifier_language[language.identifier()] = language

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("registry_path")
    argument_parser.add_argument("target_path")
    argument_parser.add_argument("language", choices=list(identifier_language.keys()))

    args = argument_parser.parse_args()
    registry_path = Path(args.registry_path)
    target_path = Path(args.target_path)
    language_identifier = args.language

    language = identifier_language.get(language_identifier)
    if language is None:
        raise argparse.ArgumentError(None, "Not supported language selected")

    return CliInfo(registry_path, target_path, language)