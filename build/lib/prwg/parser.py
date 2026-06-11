from prwg.language import *
from pathlib import Path
import xml.etree.ElementTree as etree
from dataclasses import dataclass

@dataclass
class RegistryInfo:
    namespace: str
    diminutive: str

@dataclass
class EnumInfo:
    value: int
    name: str

@dataclass
class ResultInfo:
    success: EnumInfo
    enums: list[EnumInfo]

@dataclass
class ModuleInfo:
    imports_data: set[str]

def _registry_info(root: etree.Element) -> RegistryInfo:
    namespace = root.get("namespace")
    diminutive = root.get("diminutive")

    return RegistryInfo(namespace, diminutive)

def _enum_info(enum: etree.Element) -> EnumInfo:
    value = int(enum.get("value"))
    name = enum.get("name")

    return EnumInfo(value, name)

def _result(result: etree.Element, language: Language, registry_info: RegistryInfo) -> ModuleInfo:
    success = _enum_info(result.find("success"))

    enums: list[EnumInfo] = []
    for enum in result.findall("enum"):
        enums.append(_enum_info(enum))

    module_name = language.assemble_module_name([registry_info.diminutive, "result"])
    imports = language.result_imports()

    return ModuleInfo(imports)

def process_modules(modules: list[ModuleInfo]) -> str:
    imports_data: set[str] = set()

    for module in modules:
        imports_data |= module.imports_data

    return "\n".join(imports_data)

def start(registry_path: Path, target_path: Path, language: Language):
    registry = etree.parse(registry_path)
    
    registry_info = _registry_info(registry.getroot())
    modules_info: dict[str, list[ModuleInfo]] = {}

    result_key = language.assemble_file_name([registry_info.diminutive, "result"])
    result = _result(registry.find("result"), language, registry_info)

    modules_info.setdefault(result_key, []).append(result)

    extension = language.extension()
    for key, modules in modules_info.items():
        with open(f"{target_path / (key + extension)}", "w") as file:
            file.write(process_modules(modules))
    