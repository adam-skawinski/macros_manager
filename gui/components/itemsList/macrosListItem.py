from customtkinter import CTkFrame, CTkLabel
from gui.components.buttons import CustomButton, EditButton, DeleteButton


class MacrosListItem(CTkFrame):
    def __init__(
        self,
        parent,
        item,
        index=0,
        removeMacro=None,
        onRefreshMacrosList=None,
        onOpenEditAcroLayout=None,
    ):
        super().__init__(parent)
        self.item = item
        self.index = index
        self.removeMacro = removeMacro
        self.onRefreshMacrosList = onRefreshMacrosList
        self.onOpenEditAcroLayout = onOpenEditAcroLayout

        self.label = CTkLabel(self, text=item.name)
        self.label.pack(fill="x", side="left", expand=True)

        self.editButton = EditButton(
            self, command=self.__onClickEditButton
        )
        self.editButton.pack(side="left", pady=5, padx=5)

        self.deleteButton = DeleteButton(
            self, command=self.__onClickEditDelete
        )
        self.deleteButton.pack(side="left", pady=5, padx=5)

    def __onClickEditButton(self):
        if self.onOpenEditAcroLayout:
            self.onOpenEditAcroLayout(self.index)

    def __onClickEditDelete(self):
        if self.removeMacro:
            self.removeMacro(self.index)
        self.onRefreshMacrosList()
