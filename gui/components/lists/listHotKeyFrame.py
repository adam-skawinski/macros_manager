from customtkinter import CTkFrame, CTkLabel, CTkScrollableFrame
from gui.components.itemsList import HotKeyListItem


class ListHotKeyFrame(CTkFrame):
    def __init__(
        self,
        parent,
        items=None,
        headerText="Custom list frame",
        setCurrentEditedHotKey=None,
        currentEditedHotKey=None,
        guiRemoveInput=None,
        macroId=None,
        refreshList=None,
    ):
        super().__init__(parent)
        self.headerText = headerText
        self.items = items
        self.setCurrentEditedHotKey = setCurrentEditedHotKey
        self.currentEditedHotKey = currentEditedHotKey
        self.macroId = macroId

        self.refreshList=refreshList
        self.guiRemoveInput = guiRemoveInput

        self.header = CTkLabel(
            self, text=headerText, font=("Arial", 40), bg_color="#222"
        )
        self.header.pack(side="top", fill="x")

        self.scrollableList = CTkScrollableFrame(self)
        self.scrollableList.pack(side="top", fill="both", expand=True)

        self._buildList()

    def _itemFactory(self, parent, item, index):
        return HotKeyListItem(
            parent=parent,
            item=item,
            index=index,
            setCurrentEditedHotKey=self.setCurrentEditedHotKey,
            currentEditedHotKey=self.currentEditedHotKey,
            guiRemoveInput=self.guiRemoveInput,
            macroId = self.macroId,
            refreshList=self.refreshList
        )

    def _buildList(self):
        for widget in self.scrollableList.winfo_children():
            widget.destroy()

        for index, item in enumerate(self.items):
            widget = self._itemFactory(self.scrollableList, item, index=index)
            widget.pack(fill="x", ipady=3, pady=5, padx=2)

    def addItem(self, item):
        self.items.append(item)
        self._buildList()

    def updateItems(self, new_items: list):
        self.items = new_items
        self._buildList()
