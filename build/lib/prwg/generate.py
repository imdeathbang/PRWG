import prwg.language_loader as language_loader
import prwg.parser_two as parser
import prwg.cli as cli
from pathlib import Path

def main():
    languages_path = Path(__file__).parent / "languages"
    languages = language_loader.languages(languages_path)
    cli_info = cli.start(languages)

    parser.process_registry(
        cli_info.registry_path,
        cli_info.target_path,
        cli_info.language_identifier
    )
