from prwg_imdeathbang.data import *

def get_params_data(params: list[Param], spaces: int = 4, declare: bool = True) -> str:
    data: list[str] = []
    if not declare:
        for param in params:
            data.append(f"{param.name}")
        return ", ".join(data)

    for param in params:
        data.append(f"{" " * spaces}{param.type} {param.name}")
    return ",\n".join(data)

def get_library_import(library_name, params: list[Param] = [], return_type: str = "") -> str:
    data: list[str] = []
    data.append(f'"{library_name}"')
    for param in params:
        if param.type == "string":
            data.append("StringMarshalling = StringMarshalling.Utf16")
    if return_type == "string":
        data.append("StringMarshalling = StringMarshalling.Utf16")
    return_marshal = ""
    if return_type == "bool":
        return_marshal = "\n[return: MarshalAs(UnmanagedType.I1)]"
    call_convention = "[UnmanagedCallConv(CallConvs = new Type[] { typeof(CallConvCdecl) })]\n    "
    return f'{call_convention}[LibraryImport({", ".join(data)})]{return_marshal}'


def get_interop_commands_data(library_name: str, handle: Handle) -> str:
    data: list[str] = []
    for command in handle.commands:
        data.append(f'    {get_library_import(library_name, command.params, command.type)}')
        data.append(f"    private static partial {command.type} {command.name}(")
        data.append(f"    IntPtr {handle.name}")
        data.append(get_params_data(command.params))
        data.append("    );\n")
    for property in handle.properties:
        data.append(f'    {get_library_import(library_name, return_type=property.type)}')
        data.append(f"    private static partial {property.type} {property.get_name}(")
        data.append(f"        IntPtr {handle.name}")
        data.append("    );\n")
        return_param = Param(property.type, property.name)
        data.append(f'    {get_library_import(library_name, [return_param])}')
        data.append(f"    private static partial void {property.set_name}(")
        data.append(f"        IntPtr {handle.name},")
        data.append(f"        {property.type} {property.name}")
        data.append("    );\n")
    return "\n".join(data)

def get_constructor_data(handle: Handle) -> str:
    data: list[str] = []
    constructor = handle.constructor
    data.append(f"    public {handle.type}({get_params_data(constructor.params, spaces=0)}) {{")
    if constructor.options == ConstructorOptions.RETURN_INSTANCE:
        params_data = get_params_data(constructor.params, spaces=0, declare=False)
        data.append(f"    handle = {constructor.command}({params_data});")
    elif constructor.options == ConstructorOptions.RETURN_RESULT_OUT_INSTANCE:
        pass
    else:
        pass
    data.append("    }")
    return "\n".join(data)

def get_members_data(handle: Handle) -> str:
    data: list[str] = []
    data.append(f"    IntPtr handle;")
    return "\n".join(data)

def get_handle_data(library_name: str, handle: Handle) -> str:
    data: list[str] = []
    data.append("using System.Runtime.InteropServices;")
    data.append("using System.Runtime.CompilerServices;\n")
    data.append(f"public partial class {handle.type} {{\n")
    data.append(get_interop_commands_data(library_name, handle))
    data.append(get_members_data(handle))
    data.append(get_constructor_data(handle))
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