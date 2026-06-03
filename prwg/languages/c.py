import prwg.language as language

class C(language.Language):

    def identifier(self):
        return "C"

    def config(self):
        return language.FileConfig(
            language.GroupFiles.UNIQUE,
            ".h"
        )
    
    def file_fixes(self):
        pre_file_data = []
        pre_file_data.append("#pragma once\n")
        pre_file_data.append("#ifdef __cplusplus")
        pre_file_data.append('extern "C" {')
        pre_file_data.append("#endif\n")
        pre_file_data.append("#if defined(_WIN32)")
        pre_file_data.append("    #define APIEXPORT __declspec(dllexport)")
        pre_file_data.append("#else")
        pre_file_data.append('    #define APIEXPORT __attribute((visibility("default")))')
        pre_file_data.append("#endif")

        post_file_data = []
        post_file_data.append("#ifdef __cplusplus")
        post_file_data.append("}")
        post_file_data.append("#endif")

        return language.FileFixes(
            (pre_file_data, language.FixPosition.BEFORE_IMPORTS),
            post_file_data,
        )
    
    def imports_data(self, types):
        imports: set[str] = set()
        if "bool" in types:
            imports.add("#include <stdbool.h>")
        return imports
    
    def pepe(self):
        return language.Pepe(
            False,
            "{",
            "}",
            ";"
        )

    def handle_declaration(self, type):
        return f"typedef struct {type}_T* {type}"
    
    def handle_data(self, handle_info):
        return ["//Pepe"]