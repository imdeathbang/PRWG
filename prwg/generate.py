import prwg.loader as loader
import prwg.parser as parser
import prwg.cli as cli
from pathlib import Path

def main():
    path = Path(__file__).parent / "languages"
    cli_info = cli.start(loader.languages(path))

    # parser.process_registry(
    #     cli_info.registry_path,
    #     cli_info.target_path,
    #     cli_info.language
    # )
