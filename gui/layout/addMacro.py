from customtkinter import CTkToplevel, CTkEntry, CTkLabel
from gui.components.buttons import AddButton


class AddMacroLayout(CTkToplevel):
    def __init__(
        self,
        parent,
        geometry: str = "400x400",
        title: str = "Title",
        onClose=None,
        onAdd=None,
        onRefreshMacrosList=None
    ):
        super().__init__(parent)
        self.geometry(geometry)
        self.grab_set()

        self.onClose = onClose
        self.onAdd = onAdd
        self.onRefreshMacrosList = onRefreshMacrosList

        self.title(title)
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self.onWindowClose)

        self.labelName = CTkLabel(self, text="Name")
        self.labelName.pack(anchor="center")

        self.entryName = CTkEntry(self, placeholder_text="Enter name...")
        self.entryName.pack(anchor="center")
        self.entryName.bind("<KeyRelease>", self.checkEntry)

        self.addButton = AddButton(self, text="Add", command=self.submit)
        self.addButton.configure(state="disabled")
        self.addButton.pack(anchor="center", pady=10)

    def checkEntry(self, event=None):
        text = self.entryName.get().strip()
        if text:
            self.addButton.configure(state="normal")
        else:
            self.addButton.configure(state="disabled")

    def submit(self):
        if self.entryName.get():
            self.onAdd(self.entryName.get())
            self.onRefreshMacrosList()
            if self.onClose is not None:
                self.onClose()
            self.destroy()

    def onWindowClose(self):
        if self.onClose is not None:
            self.onClose()
        self.destroy()
