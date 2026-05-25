from dataclasses import dataclass
import xml.etree.ElementTree as etree
from prwg.language import *
import prwg.language as language
from pathlib import Path

@dataclass
class FileInfo:
    imports_data: set[str]
    data: str

def _get_params_types(params: list[etree.Element]) -> set[str]:
    types: set[str] = set()

    for param in params:
        type = param.get("type")
        types.add(type)

    return types

def get_handle_data(handle: etree.Element, language: Language) -> FileInfo:
    types: set[str] = set()
    data: list[str] = []

    constructor = handle.find("constructor")

    constructor_params = constructor.findall("param")
    types |= _get_params_types(constructor_params)

    destructor = handle.find("destructor")

    destructor_params = destructor.findall("param")
    types |= _get_params_types(destructor_params)

    properties = handle.findall("property")
    for property in properties:
        type = property.get("type")
        types.add(type)

    commands = handle.findall("command")
    for command in commands:
        type = command.get("type")
        types |= _get_params_types(command.findall("param"))

    return FileInfo(language.imports_data(types), "\n".join(data))

def get_enum_data(enum: etree.Element, language: Language) -> FileInfo:
    types: set[str] = set()
    data: list[str] = []

    type = enum.get("type")
    types.add(type)

    return FileInfo(language.imports_data(types), "\n".join(data))

def _block_connectors(block: list[str]) -> list[str]:
    if block:
        return block + ["\n"]
    return block

def _process_files_info(files_info: list[FileInfo], language: Language) -> str:
    imports_data: list[str] = []
    file_data: list[str] = []

    for file_info in files_info:
        if file_info.imports_data:
            imports_data.extend(file_info.imports_data)
        file_data.append(file_info.data)

    file_fixes = language.file_fixes()
    pre_file_data, position = file_fixes.pre_file

    imports_data = list(set(imports_data))
    processed_data: list[str] = []

    if position == FixPosition.BEFORE_IMPORTS:
        processed_data.extend(_block_connectors(pre_file_data))
        processed_data.extend(_block_connectors(imports_data))
    else:
        processed_data.extend(_block_connectors(imports_data))
        processed_data.extend(_block_connectors(pre_file_data))

    processed_data.extend(_block_connectors(file_data))
    processed_data.extend(_block_connectors(file_fixes.post_file_data))

    return "".join(processed_data)

def process_registry(registry_path: Path, target_path: Path, language: Language):
    registry = etree.parse(registry_path)
    project_name = registry.getroot().get("name")

    files_info: dict[str, list[FileInfo]] = {}
    config = language.config()

    for handle in registry.findall("handle"):
        identifier = project_name
        if config.group_files == GroupFiles.DEDICATED:
            identifier = handle.get("name")

        files_info.setdefault(identifier, []).append(get_handle_data(handle, language))

    for enum in registry.findall("enum"):
        identifier = project_name
        if config.group_files == GroupFiles.DEDICATED:
            identifier = enum.get("name")

        files_info.setdefault(identifier, []).append(get_enum_data(enum, language))

    for identifier, file_info in files_info.items():
        file_path = target_path / f"{identifier}{config.extension}"

        with open(file_path, "w") as file:
            file.write(_process_files_info(file_info, language))