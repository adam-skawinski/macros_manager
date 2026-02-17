class Macro:
    def __init__(self, name, inputSequence=None, trigger=-1):
        if inputSequence is None:
            inputSequence = []
        self.name = name
        self.inputSequence = inputSequence
        self.trigger = trigger