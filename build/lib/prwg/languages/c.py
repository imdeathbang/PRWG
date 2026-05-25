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
        pre_file_data.append("Somos")

        post_file_data = []
        post_file_data.append("Peru")

        return language.FileFixes(
            (pre_file_data, language.FixPosition.BEFORE_IMPORTS),
            post_file_data,
        )
    
    def imports_data(self, types):
        imports: set[str] = set()
        if "bool" in types:
            imports.add("#include <stdbool.h>")
        return imports