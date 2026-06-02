from dataclasses import dataclass
import xml.etree.ElementTree as etree
from prwg.language import *
from pathlib import Path

@dataclass
class ModuleInfo:
    imports_data: set[str]
    data: list[str]

@dataclass
class FileInfo:
    modules_info: list[ModuleInfo]

@dataclass
class ParamInfo:
    type: str
    name: str

def _get_params_types(params: list[etree.Element]) -> set[str]:
    types: set[str] = set()

    for param in params:
        type = param.get("type")
        types.add(type)

    return types

def _get_handle_data(handle: etree.Element, language: Language) -> ModuleInfo:
    types: set[str] = set()
    data: list[str] = []

    type = handle.get("type")
    pepe = language.pepe()

    declaration = language.handle_declaration(type)
    spaces = 0

    if pepe.declaration_enroll:
        data.append(f"{declaration} {pepe.code_block_start}")
        spaces = 4
    else:
        data.append(f"{declaration}{pepe.statement_end}")
        
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


    if pepe.declaration_enroll:
        data.append(f"{pepe.code_block_end}")

    return ModuleInfo(language.imports_data(types), data)

def _get_enum_data(enum: etree.Element, language: Language) -> ModuleInfo:
    types: set[str] = set()
    data: list[str] = []

    type = enum.get("type")
    types.add(type)

    return ModuleInfo(language.imports_data(types), data)

def _add_block(data: list[str], block: list[str]):
    if block:
        data.append("\n".join(block))

def _process_module_info(modules_info: list[ModuleInfo], language: Language) -> str:
    imports_data: list[str] = []
    module_data: list[str] = []

    for module_info in modules_info:
        imports_data.extend(module_info.imports_data)
        module_data.extend(module_info.data)

    file_fixes = language.file_fixes()
    pre_file_data, position = file_fixes.pre_file

    imports_data = list(set(imports_data))
    data: list[str] = []

    if position == FixPosition.BEFORE_IMPORTS:
        _add_block(data, pre_file_data)
        _add_block(data, imports_data)
    else:
        _add_block(data, imports_data)
        _add_block(data, pre_file_data)

    _add_block(data, module_data)
    _add_block(data, file_fixes.post_file_data)

    return "\n\n".join(data)

def process_registry(registry_path: Path, target_path: Path, language: Language):
    registry = etree.parse(registry_path)
    project_name = registry.getroot().get("name")

    files_info: dict[str, FileInfo] = {}
    config = language.config()

    for handle in registry.findall("handle"):
        identifier = project_name
        if config.group_files == GroupFiles.DEDICATED:
            identifier = handle.get("type")

        file_info = files_info.setdefault(identifier, FileInfo([]))
        file_info.modules_info.append(_get_handle_data(handle, language))

    for enum in registry.findall("enum"):
        identifier = project_name
        if config.group_files == GroupFiles.DEDICATED:
            identifier = enum.get("name")

        file_info = files_info.setdefault(identifier, FileInfo([]))
        file_info.modules_info.append(_get_enum_data(enum, language))

    for identifier, file_info in files_info.items():
        file_path = target_path / f"{identifier}{config.extension}"

        with open(file_path, "w") as file:
            file.write(_process_module_info(file_info.modules_info, language))