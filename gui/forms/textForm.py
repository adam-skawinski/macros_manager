from customtkinter import CTkFrame, CTkLabel, CTkEntry

class TextForm(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.labelText = CTkLabel(self, text="Text Form")
        self.entryText = CTkEntry(self, placeholder_text="Enter text")
        self.labelText.pack(pady=5)
        self.entryText.pack(pady=5)
