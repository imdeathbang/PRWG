import prwg.language_loader as language_loader
import prwg.language as language
import prwg.language_parser as parser
import prwg.cli as cli
from pathlib import Path

def main():
    cli_info = cli.start()

    # parser.process_registry(
    #     cli_info.registry_path,
    #     cli_info.target_path,
    #     cli_info.language
    # )
