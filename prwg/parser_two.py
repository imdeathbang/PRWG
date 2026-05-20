import xml.etree.ElementTree as etree
from prwg.language import Language
from pathlib import Path

def get_handle_data(handle: etree.Element, language: Language) -> str:
    ...

def get_enum_data(enum: etree.Element, language: Language) -> str:
    ...

def process_registry(registry_path: Path, target_path: Path, language: Language):
    registry = etree.parse(registry_path)
    project_name = registry.getroot().get("name")

    extension = language.extension()
    group_files = language.group()

    file_data: dict[str, list[str]] = {}

    for handle in registry.findall("handle"):
        identifier = project_name
        if not group_files:
            identifier = handle.get("name")

        file_data.setdefault(identifier, []).append(get_handle_data(handle, language))

    for enum in registry.findall("enum"):
        identifier = project_name
        if not group_files:
            identifier = enum.get("name")

        file_data.setdefault(identifier, []).append(get_enum_data(enum, language))

    for file_identifier, file_data in file_data.items():
        file_path = target_path / f"{file_identifier}{extension}"

        with open(file_path, "w") as file:
            file.write("\n".join(file_data))