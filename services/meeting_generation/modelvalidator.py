from .. import result

class ModelValidator:
    def __init__(self, connect_string):
        self.connect_string = connect_string
        
    def establish_connection(self):
        return True
    
    def validate_prompt(self, text):
        return True
    