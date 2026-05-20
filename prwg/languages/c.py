from prwg.language import Language

class C(Language):

    def extension(self):
        return ".c"
    
    def identifier(self):
        return "C"
    
    def group(self):
        return True