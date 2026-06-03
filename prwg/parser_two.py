from dataclasses import dataclass
import xml.etree.ElementTree as etree
from prwg.language import *
from pathlib import Path
from typing import Callable

@dataclass
class InsideData:
    statement_data: str
    outside_data: list[str]

@dataclass
class ModuleInfo:
    imports_data: set[str]
    statement_data: str | None
    outside_data: list[str]
    declaration_data: list[str]

@dataclass
class FileInfo:
    modules_info: list[ModuleInfo]

@dataclass
class ParamInfo:
    type: str
    name: str

def _param_declaration(params: list[ParamInfo], spaces: int, extractor: Callable[[str, str], str]) -> list[str]:
    param_declaration: list[str] = []

    for index, param in enumerate(params):
        comma = ","
        if index == len(params) - 1:
            comma = ""

        param_declaration.append(f"{" " * spaces}{extractor(param.type, param.name)}{comma}")

    return param_declaration

def _extract_types[T](objects: list[T], extractor: Callable[[T], str]) -> set[str]:
    types: set[str] = set()

    for object in objects:
        type = extractor(object)
        types.add(type)
    
    return types

def _params_info(params: list[etree.Element]):
    params_info: list[ParamInfo] = []

    for param in params:
        type = param.get("type")
        name = param.get("name")

        param_info = ParamInfo(type, name)
        params_info.append(param_info)

    return params_info

def _out_info(constructor: etree.Element | None) -> OutInfo | None:
    out = constructor.find("out")

    if out is None:
        return None
    
    result = constructor.find("result")
    name = out.get("name")

    if result is None:
        return OutInfo(name, None)
    
    success = result.get("success")
    type = result.get("type")
    result_info = ResultInfo(success, type)

    return OutInfo(name, result_info)

def _constructor_info(constructor: etree.Element) -> ConstructorInfo:
    command = constructor.get("command")
    params_info = _params_info(constructor.findall("param"))
    out_info = _out_info(constructor)

    return ConstructorInfo(command, params_info, out_info)

def _destructor_info(destructor: etree.Element) -> DestructorInfo:
    command = destructor.get("command")
    params_info = _params_info(destructor.findall("param"))

    return DestructorInfo(command, params_info)

def _properties_info(properties: list[etree.Element]) -> list[PropertyInfo]:
    properties_info: list[PropertyInfo] = []

    for property in properties:
        type = property.get("type")
        name = property.get("name")
        get_command_name = property.find("get").get("name")
        set_command_name = property.find("set").get("name")

        property_info = PropertyInfo(type, name, get_command_name, set_command_name)
        properties_info.append(property_info)

    return properties_info

def _commands_info(commands: list[etree.Element]) -> list[CommandInfo]:
    commands_info: list[CommandInfo] = []

    for command in commands:
        type = command.get("type")
        name = command.get("name")
        params_info = _params_info(command.findall("param"))

        command_info = CommandInfo(type, name, params_info)
        commands_info.append(command_info)

    return commands_info

def _handle_info(handle: etree.Element) -> HandleInfo:
    type = handle.get("type")
    name = handle.get("name")

    constructor_info = _constructor_info(handle.find("constructor"))
    destructor_info = _destructor_info(handle.find("destructor"))
    properties_info = _properties_info(handle.findall("property"))
    commands_info = _commands_info(handle.findall("command"))

    return HandleInfo(type, name, constructor_info, destructor_info, properties_info, commands_info)

def _get_handle_data(handle: etree.Element, language: Language) -> ModuleInfo:
    types: set[str] = set()

    type = handle.get("type")
    pepe = language.pepe()

    declaration = language.handle_declaration(type)

    handle_info = _handle_info(handle)
    contents_data: list[str] = language.handle_contents(handle_info)

    pre_

    types |= _extract_types(handle_info.constructor_info.params, lambda x: x.type)
    types |= _extract_types(handle_info.destructor_info.params, lambda x: x.type)
    types |= _extract_types(handle_info.properties_info, lambda x: x.type)
    types |= _extract_types(handle_info.commands_info, lambda x: x.type)

    if pepe.handle_data_location == DataLocation.OUTSIDE_MODULE:
        statement_data = f"{declaration}{pepe.statement_end}"
        return ModuleInfo(language.imports_data(types), statement_data, contents_data, [])
    
    declaration_data: list[str] = []
    declaration_data.append(f"{declaration} {pepe.code_block_start}")

    for row_data in contents_data:
        declaration_data.append(f"{4 * " "}{row_data}")

    declaration_data.append(f"{pepe.code_block_end}")
    return ModuleInfo(language.imports_data(types), None, [], declaration_data)

def _get_enum_data(enum: etree.Element, language: Language) -> ModuleInfo:
    types: set[str] = set()
    data: list[str] = []

    type = enum.get("type")
    types.add(type)

    return ModuleInfo(language.imports_data(types), None, data, [])

def _add_block(data: list[str], block: list[str], joiner: str = "\n"):
    if block:
        data.append(joiner.join(block))

def _process_module_info(modules_info: list[ModuleInfo], language: Language) -> str:
    imports_data: list[str] = []

    statement_data: list[str] = []
    declarations_data: list[str] = []
    outside_data: list[str] = []

    for module_info in modules_info:
        if declarations_data and module_info.declaration_data:
            declarations_data.append("")
        declarations_data.extend(module_info.declaration_data)
        outside_data.extend(module_info.outside_data)
        imports_data.extend(module_info.imports_data)

        if module_info.statement_data:
            statement_data.append(module_info.statement_data)

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

    _add_block(data, statement_data)
    _add_block(data, declarations_data)
    _add_block(data, outside_data)
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