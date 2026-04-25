from prwg_imdeathbang.data import *

type_dict: dict[str, str] = {
    "string": "const char*"
}

def get_export_define_data() -> str:
    data: list[str] = []
    data.append("#if defined(_WIN32)")
    data.append("    #define APIEXPORT __declspec(dllexport)")
    data.append("#else")
    data.append('    #define APIEXPORT __attribute__((visibility("default")))')
    data.append("#endif")
    return "\n".join(data) + "\n"

def get_handles_define_data(handles: list[Handle]) -> str:
    data: list[str] = []
    for handle in handles:
        data.append(f"typedef struct {handle.type}_T* {handle.type};")
    return "\n".join(data) + "\n"

def get_params_data(params: list[Param]) -> str:
    data: list[str] = []
    for param in params:
        data.append(f"    {param.type} {param.name}")
    return ",\n".join(data)

def get_handle_constructor_data(type: str, constructor: Constructor) -> str:
    data: list[str] = []
    if constructor.options == ConstructorOptions.RETURN_INSTANCE:
        data.append(f"APIEXPORT {type} {constructor.command}(")
        data.append(get_params_data(constructor.params))
    elif constructor.options == ConstructorOptions.RETURN_RESULT_OUT_INSTANCE:
        data.append(f"{constructor.result.type} {constructor.command}(")
        data.append(get_params_data(constructor.params) + ",")
        data.append(f"    {type}* {constructor.out_name}")
    else:
        data.append(f"void {constructor.command}(")
        data.append(get_params_data(constructor.params) + ",")
        data.append(f"    {type}* {constructor.out_name}")
    data.append(");")
    
    return "\n".join(data) + "\n"

def get_handle_destructor_data(type: str, name: str, destructor: Destructor) -> str:
    data: list[str] = []
    data.append(f"APIEXPORT void {destructor.name}(")
    if destructor.params:
        data.append(f"    {type} {name},")
        data.append(get_params_data(destructor.params))
    else:
        data.append(f"    {type} {name}")
    data.append(");")
    return "\n".join(data)

def get_handle_commands_data(type: str, name: str, commands: list[Command]) -> str:
    data: list[str] = []
    for command in commands:
        data.append(f"APIEXPORT {command.type} {command.name}(")
        data.append(f"    {type} {name},")
        data.append(get_params_data(command.params))
        data.append("); \n")
    return "\n".join(data)

def get_handle_property_commands_data(type: str, name: str, properties: list[Property]) -> str:
    data: list[str] = []
    for property in properties:
        data.append(f"APIEXPORT {property.type} {property.get_name}(")
        data.append(f"    {type} {name}")
        data.append(");\n")
        data.append(f"{property.type} {property.set_name}(")
        data.append(f"    {type} {name}")
        data.append(");")
    return "\n".join(data) + "\n"

def get_handles_data(handles: list[Handle]) -> str:
    data: list[str] = []
    for handle in handles:
        name = handle.name
        type = handle.type
        data.append(get_handle_constructor_data(type, handle.constructor))
        data.append(get_handle_destructor_data(type, name, handle.destructor))
        data.append(get_handle_commands_data(type, name, handle.commands))
        data.append(get_handle_property_commands_data(type, name, handle.properties))
    return "\n".join(data)

def get_enumerators_data(enumerators: list[Enumerator]) -> str:
    data: list[str] = []
    for enumerator in enumerators:
        data.append(f"    {enumerator.name} = {enumerator.value}")
    return ",\n".join(data)

def get_enum_data(enum: Enum) -> str:
    data: list[str] = []
    data.append(f"typedef enum {enum.name} {{")
    data.append(get_enumerators_data(enum.enumerators))
    data.append(f"}} {enum.name};")
    return "\n".join(data)
    

def get_enums_data(enums: list[Enum]) -> str:
    data: list[str] = []
    for enum in enums:
        data.append(get_enum_data(enum))
    return "\n".join(data) + "\n"

def get_start_cpp_data() -> str:
    data: list[str] = []
    data.append("#ifdef __cplusplus")
    data.append('extern "C" {')
    data.append("#endif")
    return "\n".join(data) + "\n"

def get_end_cpp_data() -> str:
    data: list[str] = []
    data.append("#ifdef __cplusplus")
    data.append("}")
    data.append("#endif")
    return "\n".join(data) + "\n"

def process_data(parsed_data: ParsedData):
    file_data: list[str] = []
    file_data.append(f"#pragma once\n")
    file_data.append(get_start_cpp_data())
    file_data.append(get_export_define_data())
    file_data.append(get_handles_define_data(parsed_data.handles))
    file_data.append(get_enums_data(parsed_data.enums))
    file_data.append(get_handles_data(parsed_data.handles))
    file_data.append(get_end_cpp_data())
    with open(f"{parsed_data.target_directory}/{parsed_data.project_name}.h", "w") as file:
        file.write("\n".join(file_data))