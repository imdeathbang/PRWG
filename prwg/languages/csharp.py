import prwg.language as language

class CSharp(language.Language):

    def identifier(self):
        return "CSharp"
    
    def config(self):
        return language.FileConfig(
            language.GroupFiles.DEDICATED,
            ".cs"
        )

    def file_fixes(self):
        pre_file_data = []
        pre_file_data.append("namespace velix;")

        post_file_data = []

        return language.FileFixes(
            (pre_file_data, language.FixPosition.BEFORE_IMPORTS),
            post_file_data,
        )
    
    def imports_data(self, types):
        imports: set[str] = set()
        imports.add("using System.Runtime.InteropServices;")
        imports.add("using System.Runtime.CompilerServices;")
        return imports
    
    def pepe(self):
        return language.Pepe(
            True,
            "{",
            "}",
            ";"
        )
    
    def handle_declaration(self, type):
        return f"public partial class {type}"
    
    def handle_data(self, handle_info):
        return ["//Pepesillo"]