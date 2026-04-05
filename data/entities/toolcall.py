class ToolCall:
    def __init__(self, function_name, function_description, parameters, parameters_description):
        self.function_name = function_name
        self.function_description = function_description
        self.parameters = parameters
        self.parameters_description = parameters_description