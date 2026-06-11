import prwg.language as language

class CSharp(language.Language):

    def identifier(self):
        return "CSharp"
    
    def extension(self):
        return ".cs"
    
    def assemble_file_name(self, words):
        return "".join([word.capitalize() for word in words])
    
    def assemble_module_name(self, words):
        return "".join([word.capitalize() for word in words])
    
    def result_imports(self):
        imports: set[str] = set()
        imports.add("from enum import Enum, auto")

        return imports
