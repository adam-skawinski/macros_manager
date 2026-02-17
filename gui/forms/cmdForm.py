from customtkinter import CTkFrame, CTkLabel, CTkTextbox


class CMDForm(CTkFrame):
    def __init__(self, parent, cmdText="(EMPTY)"):
        super().__init__(parent)
        self.labelCmd = CTkLabel(self, text=f"Current command: {cmdText}")
        self.labelText = CTkLabel(self, text="CMD Form")
        self.boxText = CTkTextbox(
            self, width=400, height=200
        )
        self.boxText.insert("1.0", cmdText)
        self.labelText.pack(pady=5)
        self.labelCmd.pack(pady=5)
        self.boxText.pack(pady=5)
