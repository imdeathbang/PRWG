from prwg_imdeathbang.data import *

def get_param_marshaling(param: Param) -> str:
    type = param.type
    if type == "bool":
        return "[MarshalAs(UnmanagedType.I1)] "
    return ""

def get_params_data(params: list[Param], spaces: int = 4, declare: bool = True, connector = ", ", marshal = True) -> str:
    data: list[str] = []
    if not declare:
        for param in params:
            data.append(f"{param.name}")
        return connector.join(data)

    if connector == ", ":
        connector = ",\n"

    for param in params:
        marshaling = ""
        if marshal:
            marshaling = get_param_marshaling(param)
        data.append(f"{" " * spaces}{marshaling}{param.type} {param.name}")
    return connector.join(data)

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
    constructor = handle.constructor
    data.append(f"    {get_library_import(library_name, constructor.params)}")
    if constructor.options == ConstructorOptions.RETURN_INSTANCE:
        data.append(f"    private static partial IntPtr {constructor.command}(")
        data.append(get_params_data(constructor.params, spaces=8))
    elif constructor.options == ConstructorOptions.RETURN_RESULT_OUT_INSTANCE:
        result = constructor.result
        data.append(f"    private static partial {result.type} {constructor.command}(")
        params = constructor.params.copy()
        params.append(Param("out IntPtr", "handle"))
        data.append(get_params_data(params, spaces=8))
    else:
        result = constructor.result
        data.append(f"    private static partial {result.type} {constructor.command}(")
        params = constructor.params.copy()
        params.append(Param("out IntPtr", "handle"))
        data.append(get_params_data(params, spaces=8))
    data.append("    );\n")
    for command in handle.commands:
        data.append(f'    {get_library_import(library_name, command.params, command.type)}')
        data.append(f"    private static partial {command.type} {command.name}(")
        params: list[Param] = [Param("IntPtr", handle.name)] + command.params
        data.append(get_params_data(params, spaces=8))
        data.append("    );\n")
    for property in handle.properties:
        data.append(f'    {get_library_import(library_name, return_type=property.type)}')
        data.append(f"    private static partial {property.type} {property.get_name}(")
        data.append(f"        IntPtr {handle.name}")
        data.append("    );\n")
        return_param = Param(property.type, property.name)
        data.append(f'    {get_library_import(library_name, [return_param])}')
        data.append(f"    private static partial void {property.set_name}(")
        params: list[Param] = [Param("IntPtr", handle.name), Param(property.type, property.name)]
        data.append(get_params_data(params, spaces=8))
        data.append("    );\n")
    return "\n".join(data)

def get_constructor_data(handle: Handle) -> str:
    data: list[str] = []
    constructor = handle.constructor
    data.append(f"    public {handle.type}( ")
    data.append(get_params_data(constructor.params, spaces=8))
    data.append("    ) {")
    if constructor.options == ConstructorOptions.RETURN_INSTANCE:
        params_data = get_params_data(constructor.params, spaces=0, declare=False)
        data.append(f"        _handle = {constructor.command}({params_data});")
        data.append("        if (_handle == IntPtr.Zero) {")
        data.append('            throw new InvalidOperationException("Handle is NULL")')
        data.append("        }")
    elif constructor.options == ConstructorOptions.RETURN_RESULT_OUT_INSTANCE:
        result = constructor.result
        params = constructor.params.copy()
        params.append(Param("", "out IntPtr handle"))
        params_data = get_params_data(params, spaces=0, declare=False)
        data.append(f"        {result.type} result = {constructor.command}({params_data});")
        data.append(f"        if (result != {result.type}.{result.success}) {{")
        data.append("            throw new InvalidOperationException(result.ToString());")
        data.append("        }")
        data.append("        _handle = handle;")
    else:
        params = constructor.params.copy() + Param("", "out IntPtr handle")
        params_data = get_params_data(params, spaces=0, declare=False)
        data.append(f"        {constructor.command}({params_data});")
        data.append("        if (handle == IntPtr.Zero) {")
        data.append('            throw new InvalidOperationException("Handle is NULL")')
        data.append("        }")
        data.append("        _handle = handle;")
    data.append("    }")
    return "\n".join(data)

def get_members_data(handle: Handle) -> str:
    data: list[str] = []
    data.append(f"    private IntPtr _handle;")
    return "\n".join(data) + "\n"

def get_enumerators_data(enumerators: list[Enumerator]) -> str:
    data: list[str] = []
    for enumerator in enumerators:
        data.append(f"    {enumerator.name} = {enumerator.value}")
    return ",\n".join(data)

def get_enum_data(library_name: str, enum: Enum) -> str:
    data: list[str] = []
    data.append(f"namespace {library_name};\n")
    data.append(f"public enum {enum.name} : {enum.type} {{")
    data.append(get_enumerators_data(enum.enumerators))
    data.append("}")
    return "\n".join(data)

def get_commands_data(handle: Handle) -> str:
    data: list[str] = []

    for command in handle.commands:
        pascal_name = command.name[0].upper() + command.name[1:]
        data.append(f"    public {command.type} {pascal_name}(")
        data.append(get_params_data(command.params, spaces=8, marshal=False))
        data.append("    ) {")
        params: list[Param] = [Param("", "handle")] + command.params
        param_data = get_params_data(params, spaces=0, declare=False)
        data.append(f"        {command.name}({param_data});")
        data.append("    }")

    return "\n".join(data)

def get_handle_data(library_name: str, handle: Handle) -> str:
    data: list[str] = []
    data.append("using System.Runtime.InteropServices;")
    data.append("using System.Runtime.CompilerServices;\n")
    data.append(f"namespace {library_name};\n")
    data.append(f"public partial class {handle.type} {{\n")
    data.append(get_interop_commands_data(library_name, handle))
    data.append(get_members_data(handle))
    data.append(get_constructor_data(handle))
    data.append(get_commands_data(handle))
    data.append("}")
    return "\n".join(data)

def process_handle(library_name: str, target_directory: str, handle: Handle):
    with open(f"{target_directory}/{handle.type}.cs", "w") as file:
        file.write(get_handle_data(library_name, handle))

def process_enum(library_name: str, target_directory: str, enum: Enum):
    with open(f"{target_directory}/{enum.name}.cs", "w") as file:
        file.write(get_enum_data(library_name, enum))

def process_data(parsed_data: ParsedData):
    for handle in parsed_data.handles:
        process_handle(parsed_data.project_name, parsed_data.target_directory, handle)
    for enum in parsed_data.enums:
        process_enum(parsed_data.project_name, parsed_data.target_directory, enum)

def get_type_dict() -> dict[str, str]:
    return {
        "string": "string"
    }