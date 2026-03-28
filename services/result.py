class Result:
    def __init__(self, _type):
        self._type = _type
    
class ErrorResult(Result):
    def __init__(self, error_text):
        super().__init__("ErrorResult")
        self.error_text = error_text