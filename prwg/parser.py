import xml.etree.ElementTree as etree
from dataclasses import dataclass
from prwg.language import *
from pathlib import Path

@dataclass
class RegistryInfo:
    namespace: str
    diminutive: str

@dataclass
class ModuleInfo:
    imports_data: set[str]

def _assemble_container(container: ContainerInfo, data: list[str]):
    result = container.pre

    if data:
        result += "\n    " + (container.joiner + "\n    ").join(data)
    if container.end:
        result += container.end

    return result

def _registry_info(root: etree.Element) -> RegistryInfo:
    namespace = root.get("namespace")
    diminutive = root.get("diminutive")

    return RegistryInfo(namespace, diminutive)

def _enum_info(enum: etree.Element) -> tuple[int, str]:
    value = int(enum.get("value"))
    name = enum.get("name")

    return (value, name)

def _result(result: etree.Element, language: Language, registry_info: RegistryInfo) -> ModuleInfo:
    data: list[str] = []
    value, name = _enum_info(result.find("success"))
    data.append(language.assemble_enum(name, value))

    for enum in result.findall("enum"):
        value, name = _enum_info(enum)
        data.append(language.assemble_enum(name, value))

    module_name = language.assemble_module_name([registry_info.diminutive, "result"])

    container = _assemble_container(language.result_container(module_name), data)

    imports = language.result_imports()
    return ModuleInfo(imports)

def _process_modules(modules: list[ModuleInfo]) -> str:
    imports_data: set[str] = set()

    for module in modules:
        imports_data |= module.imports_data

    return "\n".join(imports_data)

def start(registry_path: Path, target_path: Path, language: Language):
    registry = etree.parse(registry_path)
    
    registry_info = _registry_info(registry.getroot())
    modules_info: dict[str, list[ModuleInfo]] = {}

    result = _result(registry.find("result"), language, registry_info)

    result_key = language.assemble_file_name([registry_info.diminutive, "result"])
    modules_info.setdefault(result_key, []).append(result)

    extension = language.extension()
    for key, modules in modules_info.items():
        with open(f"{target_path / (key + extension)}", "w") as file:
            file.write(_process_modules(modules))
    