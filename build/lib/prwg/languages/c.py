import prwg.language as language

class C(language.Language):

    def identifier(self):
        return "C"
    
    def extension(self):
        return ".c"
    
    def assemble_file_name(self, words: list[str]):
        return "_".join(words)
    
    def assemble_module_name(self, words):
        return "".join(word.capitalize() for word in words)
    
    def assemble_enum(self, name, value):
        return f"{name} {value}"
    
    def result_imports(self):
        return set()
    
    def result_container(self, name):
        return language.ContainerInfo(
            f"typedef enum {name} {{",
            ",",
            f"}} {name}"
        )