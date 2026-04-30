import xml.etree.ElementTree as etree
from prwg_imdeathbang.data import *
import argparse
import prwg_imdeathbang.c as c
import prwg_imdeathbang.csharp as csharp

def parse_params(params: list[etree.Element], type_dict: dict[str, str]) -> list[Param]:
    parsed: list[Param] = []
    for param in params:
        type = param.get("type")
        type = type_dict.get(type, type)
        name = param.get("name")
        parsed.append(Param(type, name))
    return parsed

def parse_result(result: etree.Element | None) -> Result | None:
    if result is None:
        return None
    type = result.get("type")
    name = result.get("success")
    return Result(type, name)

def parse_handle_constructor(constructor: etree.Element, type_dict: dict[str, str]) -> Constructor:
    command = constructor.get("command")
    params = parse_params(constructor.findall("param"), type_dict)
    options = ConstructorOptions.RETURN_INSTANCE
    out_name = ""
    out = constructor.find("out")
    if out is not None:
        out_name = out.get("name")
        options = ConstructorOptions.OUT_INSTANCE
    result = parse_result(constructor.find("result"))
    if result is not None:
        options = ConstructorOptions.RETURN_RESULT_OUT_INSTANCE
    return Constructor(command, params, out_name, result, options)

def parse_handle_destructor(destructor: etree.Element, type_dict: dict[str, str]) -> Destructor:
    name = destructor.get("command")
    params = parse_params(destructor.findall("param"), type_dict)
    return Destructor(name, params)

def parse_handle_properties(properties: list[etree.Element], type_dict: dict[str, str]) -> list[Property]:
    parsed: list[Property] = []
    for property in properties:
        type = property.get("type")
        type = type_dict.get(type, type)
        name = property.get("name")
        get_name = property.find("get").get("name")
        set_name = property.find("set").get("name")
        parsed.append(Property(type, name, get_name, set_name))
    return parsed

def parse_handle_commands(commands: list[etree.Element], type_dict: dict[str, str]) -> list[Command]:
    parsed: list[Command] = []
    for command in commands:
        type = command.get("type")
        type = type_dict.get(type, type)
        name = command.get("name")
        params = parse_params(command.findall("param"), type_dict)
        parsed.append(Command(type, name, params))
    return parsed

def parse_handle(handle: etree.Element, type_dict: dict[str, str]) -> Handle:
    type = handle.get("type")
    name = handle.get("name")
    constructor = parse_handle_constructor(handle.find("constructor"), type_dict)
    destructor = parse_handle_destructor(handle.find("destructor"), type_dict)
    properties = parse_handle_properties(handle.findall("property"), type_dict)
    commands = parse_handle_commands(handle.findall("command"), type_dict)
    return Handle(type, name, constructor, destructor, properties, commands)

def parse_enumerators(enumerators: list[etree.Element]) -> list[Enumerator]:
    parsed: list[Enumerator] = []
    for enumerator in enumerators:
        name = enumerator.get("name")
        value = enumerator.get("value")
        parsed.append(Enumerator(name, value))
    return parsed

def parse_enum(enum: etree.Element, type_dict: dict[str, str]) -> Enum:
    type = enum.get("type")
    type = type_dict.get(type, type)
    name = enum.get("name")
    enumerators = parse_enumerators(enum.findall("enumerator"))
    return Enum(type, name, enumerators)

def parse_registry(window_data: InitializeInfo, type_dict: dict[str, str]) -> ParsedData:
    registry = etree.parse(window_data.registry_path)
    project_name = registry.getroot().get("name")
    handles: list[Handle] = []
    enums: list[Enum] = []
    for handle in registry.findall("handle"):
        handles.append(parse_handle(handle, type_dict))
    for enum in registry.findall("enum"):
        enums.append(parse_enum(enum, type_dict))
    return ParsedData(handles, enums, window_data.target_directory, project_name)

def build(window_data: InitializeInfo, registered_languages: dict[str, LanguageData]):
    language_data = registered_languages[window_data.language]
    parsed_data = parse_registry(window_data, language_data.type_dictionary)
    language_data.process_function(parsed_data)

def main():
    registered_languages: dict[str, LanguageData] = {}
    registered_languages["C"] = LanguageData(c.process_data, c.get_type_dict())
    registered_languages["CSharp"] = LanguageData(csharp.process_data, csharp.get_type_dict())

    parser = argparse.ArgumentParser()
    init_info = InitializeInfo()
    parser.add_argument("language")
    parser.add_argument("target_directory")
    parser.add_argument("registry_path")

    args = parser.parse_args()
    init_info.language = args.language
    init_info.target_directory = args.target_directory
    init_info.registry_path = args.registry_path

    build(init_info, registered_languages)