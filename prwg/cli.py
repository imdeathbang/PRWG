from dataclasses import dataclass
from prwg.language import Language
from pathlib import Path
import argparse

@dataclass
class CliInfo:
    registry_path: Path
    target_path: Path
    language: Language

def start_cli(languages: list[Language]) -> CliInfo:
    language_identifiers: list[str] = []

    for language in languages:
        language_identifiers.append(language.identifier())

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("registry_path")
    argument_parser.add_argument("target_path")
    argument_parser.add_argument("language", choices=language_identifiers)

    args = argument_parser.parse_args()
    registry_path = Path(args.registry_path)
    target_path = Path(args.target_path)
    language_name = args.language

    for language in languages:
        if language.identifier() == language_name:
            return CliInfo(registry_path, target_path, language)
        
    raise argparse.ArgumentError(None, "Invalid language selected")