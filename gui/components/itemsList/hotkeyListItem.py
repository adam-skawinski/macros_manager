from customtkinter import CTkFrame, CTkLabel
from gui.components.buttons import CustomButton
from gui.components.buttons import EditButton, DeleteButton
from logic import inputObjClass


class HotKeyListItem(CTkFrame):
    def __init__(
        self,
        parent,
        item,
        index=None,
        setCurrentEditedHotKey=None,
        currentEditedHotKey=None,
        guiRemoveInput=None,
        macroId=None,
        refreshList=None,
    ):
        super().__init__(parent)

        self.currentEditedHotKey = currentEditedHotKey
        self.macroId = macroId

        self.setCurrentEditedHotKey = setCurrentEditedHotKey
        self.guiRemoveInput = guiRemoveInput
        self.refreshList = refreshList

        self.index = index
        self.__setActivateColorFg()
        self.label = CTkLabel(self, text=self.__encodeText(item=item))
        self.label.pack(side="left", expand=True)
        # F41
        self.deleteButton = DeleteButton(self, command=self.__onClickDeleteButton)
        self.editButton = EditButton(self, command=self.__onClickEditButton)
        self.editButton.pack(side="left", pady=5, padx=5)
        self.deleteButton.pack(side="left", pady=5, padx=5)
        self.isActive = False

    def friendlyKeyName(self, keyName):
        mapping = {
            "Key.ctrl_l": "ctrl (L)",
            "Key.ctrl_r": "ctrl (R)",
            "Key.alt_l": "alt (L)",
            "Key.alt_r": "alt (R)",
            "Key.shift_l": "shift (L)",
            "Key.shift_r": "shift (R)",
        }
        keyName = str(keyName).replace("'","")
        if len(keyName) == 1 and keyName.isalnum():
            return keyName
        return mapping.get(keyName, keyName)

    def __encodeText(self, item):
        if isinstance(item, inputObjClass.InputKey):
            keyLabel = self.friendlyKeyName(item.key)
            stateLabel = "Press" if item.state else "Release"
            return f"{keyLabel} ({stateLabel})"
        if isinstance(item, inputObjClass.InputWait):
            return f"{item.time} ms"
        if isinstance(item, inputObjClass.InputText):
            return f"{item.string}"
        if isinstance(item, inputObjClass.InputCommand):
            if len(item.string) > 10:
                return f"(CMD) {item.string}"[:10] + "..."
            return f"(CMD) {item.string}"

    def __onClickEditButton(self):
        self.setCurrentEditedHotKey(self.index)

    def __onClickDeleteButton(self):
        self.guiRemoveInput(self.macroId, self.index)
        self.refreshList()
        self.setCurrentEditedHotKey(-1)

    def __setActivateColorFg(self):
        if self.currentEditedHotKey == self.index:
            self.configure(fg_color="#555")
        else:
            self.configure(fg_color="#222")
