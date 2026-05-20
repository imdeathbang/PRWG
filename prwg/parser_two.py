from dataclasses import dataclass
import xml.etree.ElementTree as etree
from prwg.language import Language
from pathlib import Path

@dataclass
class FileInfo:
    imports_data: list[str]
    data: str

def get_handle_data(handle: etree.Element, language: Language) -> FileInfo:
    imports_data: list[str] = []
    data: list[str] = []



    return FileInfo(imports_data, "\n".join(data))

def get_enum_data(enum: etree.Element, language: Language) -> FileInfo:
    ...

def _process_files_info(files_info: list[FileInfo], language: Language) -> str:
    imports_data: list[str] = []
    file_data: list[str] = []

    for file_info in files_info:
        if file_info.imports_data:
            imports_data.extend(file_info.imports_data)
        file_data.append(file_info.data)

    imports_data = list(set(imports_data))

    pre_file, before_imports = language.pre_file()

    processed_data: list[str] = []

    if before_imports:
        processed_data.append(pre_file)
        processed_data.append("\n".join(imports_data))
    else:
        processed_data.append("\n".join(imports_data))
        processed_data.append(pre_file)

    processed_data.append("\n".join(file_data))
    processed_data.append(language.post_file())

    return "\n".join(processed_data)

def process_registry(registry_path: Path, target_path: Path, language: Language):
    registry = etree.parse(registry_path)
    project_name = registry.getroot().get("name")

    extension = language.extension()
    group_files = language.group()

    files_info: dict[str, list[FileInfo]] = {}

    for handle in registry.findall("handle"):
        identifier = project_name
        if not group_files:
            identifier = handle.get("name")

        files_info.setdefault(identifier, []).append(get_handle_data(handle, language))

    for enum in registry.findall("enum"):
        identifier = project_name
        if not group_files:
            identifier = enum.get("name")

        files_info.setdefault(identifier, []).append(get_enum_data(enum, language))

    for file_identifier, file_info in files_info.items():
        file_path = target_path / f"{file_identifier}{extension}"

        with open(file_path, "w") as file:
            file.write(_process_files_info(file_info, language))