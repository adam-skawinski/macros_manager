from customtkinter import CTkFrame, CTkLabel, CTkEntry

class WaitForm(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.labelWait = CTkLabel(self, text="Wait Form")

        vcmd = (self.register(self.validateInt), "%P")

        self.entryWait = CTkEntry(self, placeholder_text="Enter wait time (ms)")
        self.entryWait.configure(validate="key", validatecommand=vcmd)

        self.labelWait.pack(pady=5)
        self.entryWait.pack(pady=5)

    def validateInt(self, newText):
        if newText == "":
            return True
        return newText.isdigit()