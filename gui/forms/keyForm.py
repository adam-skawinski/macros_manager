from customtkinter import CTkFrame, CTkLabel, CTkRadioButton, CTkButton, IntVar

class KeyForm(CTkFrame):
    SPECIAL_KEYS = {
        "Control_L": "LCTRL",
        "Control_R": "RCTRL",
        "Button1": "LMB",
        "Button3": "RMB",
    }

    def __init__(self, parent):
        super().__init__(parent)
        self.varRadio = IntVar(value=1)
        self.captured_key = None

        self.labelTitle = CTkLabel(self, text="Key Form")

        self.labelKeyValue = CTkLabel(self, text="Press a key...")

        self.radioPress = CTkRadioButton(self, variable=self.varRadio, value=1, text="Press")
        self.radioRelease = CTkRadioButton(self, variable=self.varRadio, value=0, text="Release")

        self.captureButton = CTkButton(self, text="Start capture", command=self.startCapture)
        self.captureActive = False

        self.labelTitle.pack(pady=5)
        self.labelKeyValue.pack(pady=5)
        self.radioPress.pack(pady=5)
        self.radioRelease.pack(pady=5)
        self.captureButton.pack(pady=10)

    def startCapture(self):
        toplevel = self.winfo_toplevel()
        if not self.captureActive:
            self.captureActive = True
            self.labelKeyValue.configure(text="Press any key...")
            self.captureButton.configure(text="Stop capture")
            toplevel.bind("<Key>", self.onKeyPress)
            toplevel.focus_set()
        else:
            self.captureActive = False
            self.captureButton.configure(text="Start capture")
            toplevel.unbind("<Key>")

    def onKeyPress(self, event):
        key_name = event.keysym
        mapped_key = self.SPECIAL_KEYS.get(key_name, key_name)
        self.captured_key = mapped_key
        self.labelKeyValue.configure(text=mapped_key)
        self.startCapture()  # wyłącz nasłuchiwanie
        print(self.captured_key)

    def getCapturedKey(self):
        return self.captured_key

    def setKey(self, key_name):
        self.captured_key = key_name
        self.labelKeyValue.configure(text=key_name)
