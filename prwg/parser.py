from prwg.language import *
from pathlib import Path
import xml.etree.ElementTree as etree

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

def _result_info(result: etree.Element) -> ResultInfo:
    success = _enum_info(result.find("success"))

    enums: list[EnumInfo] = []
    for enum in result.findall("enum"):
        enums.append(_enum_info(enum))

    return ResultInfo(success, enums)

def start(registry_path: Path, target_path: Path, language: Language):
    registry = etree.parse(registry_path)
    
    registry_info = _registry_info(registry.getroot())
    result_info = _result_info(registry.find("result"))

    modules_info: dict[str, list[ModuleInfo]] = {}

    file_name_convention = language.file_name_convention()
    modules_info.setdefault(file_name_convention([]))
    