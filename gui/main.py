from customtkinter import CTk
import customtkinter as ctk_tk

from gui.components.buttons import OpenLayoutButton, ActivateButton
from gui.layout import AddMacroLayout, EditMacroLayout
from gui.components.lists import ListMacrosFrame
from logic.main import Main as MacrosManager


class App(CTk):
    """
    It's a custom main view.
    """

    def __init__(self, title: str = "Title"):

        super().__init__(
            fg_color="#222",
        )
        ctk_tk.set_appearance_mode("dark")
        self.macrosManager = MacrosManager()
        self.macrosList = self.macrosManager.registeredMacros

        self.title(title)
        self.geometry("400x600")

        self.currentLayoutPopup = None

        self.listMacrosFrame = ListMacrosFrame(
            parent=self,
            headerText="Macros",
            items=self.macrosList,
            removeMacro=self.macrosManager.removeMacro,
            onRefreshMacrosList=self.refreshMacrosList,
            onOpenEditAcroLayout = self.openEditMacroLayout
        )
        self.listMacrosFrame.pack(fill="both", expand=True, pady=5)

        self.addButton = OpenLayoutButton(
            self, text="Add", command=self.openAddMacroLayout
        )
        self.addButton.pack(side="top", fill="x", padx=50, pady=5)

        self.activateButton = ActivateButton(
            self, text="Activate", command=self.macrosManager.runMacros
        )
        self.activateButton.pack(side="top", fill="x", padx=50, pady=20)
        self.mainloop()

    def refreshMacrosList(self):
        self.macrosList = self.macrosManager.registeredMacros
        self.listMacrosFrame.updateItems(self.macrosManager.registeredMacros)

    def onLayoutClosed(self):
        self.currentLayoutPopup = None
        self.refreshMacrosList()

    def openEditMacroLayout(self, macrosId=0):
        if self.currentLayoutPopup is not None:
            return
        self.currentLayoutPopup = EditMacroLayout(
            self,
            geometry="900x700",
            title="Edit",
            onClose=self.onLayoutClosed,
            macroId=macrosId,
            macros=self.macrosManager.registeredMacros,
            guiModifyInput=self.macrosManager.guiModifyInput,
            guiRemoveInput=self.macrosManager.guiRemoveInput,
            editName = self.macrosManager.editName,
            editTrigger = self.macrosManager.editTrigger
            
        )

    def openAddMacroLayout(self):
        if self.currentLayoutPopup is not None:
            return

        self.currentLayoutPopup = AddMacroLayout(
            self,
            geometry="200x200",
            title="Add",
            onClose=self.onLayoutClosed,
            onAdd=self.macrosManager.addMacro,
            onRefreshMacrosList=self.refreshMacrosList,
        )
