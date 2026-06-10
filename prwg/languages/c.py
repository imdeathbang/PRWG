import prwg.language as language

class C(language.Language):

    def identifier(self):
        return "C"
    
    def file_name_convention():
        return language.NamingConventions.SNAKE
