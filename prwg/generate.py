from prwg.data import *
import prwg.parser as parser
import argparse

def build(window_data: InitializeInfo):
    pass

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