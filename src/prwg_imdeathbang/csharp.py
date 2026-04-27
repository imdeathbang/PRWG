from prwg_imdeathbang.data import *

def get_params_data(params: list[Param]) -> str:
    data: list[str] = []
    for param in params:
        data.append(f"    {param.type} {param.name}")
    return ",\n".join(data)

def get_library_import(library_name, params: list[Param]) -> str:
    data: list[str] = []
    data.append(f'{library_name}')
    for param in params:
        if param.type == "string":
            data.append("StringMarshalling = StringMarshalling.Utf16")
    return f'[LibraryImport({", ".join(data)})]'

def get_interop_commands_data(library_name: str, handle: Handle) -> str:
    data: list[str] = []
    for command in handle.commands:
        data.append(f'    {get_library_import(library_name, command.params)}')
        data.append(f"    private static partial {command.type} {command.name}(")
        data.append(f"    {handle.type} {handle.name}")
        data.append(get_params_data(command.params))
        data.append("    );\n")
    for property in handle.properties:
        data.append(f'    {get_library_import(library_name, property.params)}')
        data.append(f"    private static partial {property.type} {property.get_name}(")
        data.append(f"        {handle.type} {handle.name}")
        data.append("    );\n")
        data.append(f'    {get_library_import(library_name, property.params)}')
        data.append(f"    private static partial void {property.get_name}(")
        data.append(f"        {handle.type} {handle.name}")
        data.append(f"        {property.type} {property.name}")
        data.append("    );\n")
    return "\n".join(data)

def get_handle_data(library_name: str, handle: Handle) -> str:
    data: list[str] = []
    data.append("using System.Runtime.InteropServices;\n")
    data.append(f"public partial class {handle.type} {{\n")
    data.append(get_interop_commands_data(library_name, handle))
    data.append("}")
    return "\n".join(data)

def process_handle(library_name: str, target_directory: str, handle: Handle):
    with open(f"{target_directory}/{handle.type}.cs", "w") as file:
        file.write(get_handle_data(library_name, handle))

def process_data(parsed_data: ParsedData):
    for handle in parsed_data.handles:
        process_handle(parsed_data.project_name, parsed_data.target_directory, handle)

def get_type_dict() -> dict[str, str]:
    return {
        "string": "string"
    }