from dataclasses import dataclass
import xml.etree.ElementTree as etree
from prwg.language import Language
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

def _process_files_info(files_info: list[FileInfo], language: Language) -> str:
    imports_data: list[str] = []
    file_data: list[str] = []

    for file_info in files_info:
        if file_info.imports_data:
            imports_data.extend(file_info.imports_data)
        file_data.append(file_info.data)

    file_fixes = language.file_fixes()

    imports_data = list(set(imports_data))
    processed_data: list[str] = []

    if file_fixes.before_imports:
        processed_data.append("\n".join(file_fixes.pre_file_data))
        processed_data.append("\n".join(imports_data))
    else:
        processed_data.append("\n".join(imports_data))
        processed_data.append("\n".join(file_fixes.pre_file_data))

    processed_data.append("\n".join(file_data))
    processed_data.append("\n".join(file_fixes.post_file_data))

    return "\n".join(processed_data)

def process_registry(registry_path: Path, target_path: Path, language: Language):
    registry = etree.parse(registry_path)
    project_name = registry.getroot().get("name")

    files_info: dict[str, list[FileInfo]] = {}
    config = language.config()

    for handle in registry.findall("handle"):
        identifier = project_name
        if not config.group_files:
            identifier = handle.get("name")

        files_info.setdefault(identifier, []).append(get_handle_data(handle, language))

    for enum in registry.findall("enum"):
        identifier = project_name
        if not config.group_files:
            identifier = enum.get("name")

        files_info.setdefault(identifier, []).append(get_enum_data(enum, language))

    for file_identifier, file_info in files_info.items():
        file_path = target_path / f"{file_identifier}{config.extension}"

        with open(file_path, "w") as file:
            file.write(_process_files_info(file_info, language))