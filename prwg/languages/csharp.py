from prwg.language import Language

class CSharp(Language):

    def extension(self):
        return ".c"
    
    def identifier(self):
        return "CSharp"
    
    def group(self):
        return False