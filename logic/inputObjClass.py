class InputKey:
    def __init__(self, key, state):
        self.key = key
        self.state = state

class InputWait:
    def __init__(self, time):
        self.time = time

class InputText:
    def __init__(self, string):
        self.string = string

class InputCommand:
    def __init__(self, string):
        self.string = string