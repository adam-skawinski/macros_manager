from customtkinter import (
    CTkToplevel,
    CTkEntry,
    CTkFrame,
    CTkLabel,
    IntVar,
    StringVar,
)
from gui.components.lists import ListHotKeyFrame
from gui.components.buttons import AddButton, CustomButton, EditButton
from gui.forms import KeyForm, WaitForm, TextForm, CMDForm
from logic.inputObjClass import InputCommand, InputKey, InputText, InputWait


class EditMacroLayout(CTkToplevel):
    def __init__(
        self,
        parent,
        geometry: str = "300x400",
        title: str = "Edit",
        macroId: int = 0,
        onClose=None,
        macros=None,
        guiModifyInput=None,
        guiRemoveInput=None,
        editName=None,
        editTrigger=None,
    ):
        super().__init__(parent)
        self.geometry(geometry)
        self.grab_set()

        self.onClose = onClose
        self.title(title)
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self.onWindowClose)

        self.guiModifyInput = guiModifyInput
        self.guiRemoveInput = guiRemoveInput
        self.editName = editName
        self.editTrigger = editTrigger

        self.macroId = macroId
        self.macro = macros[macroId] or None
        self.currentEditedLayout = -1
        self.currentEditedHotKey = 0
        self.varRatio = IntVar(value=1)
        self.varMacroName = StringVar(value=self.macro.name)
        self.varMacroTrigger = StringVar(
            value=(
                ""
                if self.macro.trigger == -1
                else str(self.macro.trigger).replace("'", "")
            )
        )
        self.currentForm = None
        """
        key form
        wait form
        text form 
        CMD form
        """

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=1)

        self.leftColumn = CTkFrame(self)
        self.addNewButton = AddButton(
            self.leftColumn, text="New", command=self.onClickAddButton
        )
        self.list = ListHotKeyFrame(
            self.leftColumn,
            headerText="Inputs list",
            items=self.macro.inputSequence,
            setCurrentEditedHotKey=self.setCurrentEditedHotKey,
            refreshList=self.refreshList,
            currentEditedHotKey=self.currentEditedHotKey,
            guiRemoveInput=self.guiRemoveInput,
            macroId=self.macroId,
        )
        self.rightColumn = CTkFrame(self)
        self.switch = CTkFrame(self.rightColumn)

        self.leftColumn.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.rightColumn.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.keyLayoutButton = CustomButton(
            self.switch,
            fg_color="#222",
            text_color="#fff",
            text="Key",
            width=100,
            command=lambda: self.onClickChoiseLayoutButton(0),
        )
        self.waitLayoutButton = CustomButton(
            self.switch,
            fg_color="#222",
            text_color="#fff",
            text="Wait",
            width=100,
            command=lambda: self.onClickChoiseLayoutButton(1),
        )
        self.textLayoutButton = CustomButton(
            self.switch,
            fg_color="#222",
            text_color="#fff",
            text="Text",
            width=100,
            command=lambda: self.onClickChoiseLayoutButton(2),
        )
        self.CMDLayoutButton = CustomButton(
            self.switch,
            fg_color="#222",
            text_color="#fff",
            text="CMD",
            width=100,
            command=lambda: self.onClickChoiseLayoutButton(3),
        )
        self.formContainer = CTkFrame(self.rightColumn)

        self.addEditButton = EditButton(
            self.rightColumn, text="Insert", command=self.onClickAddEditButton
        )

        self.nameFrame = CTkFrame(self.leftColumn)
        self.nameLabel = CTkLabel(self.nameFrame, text="Name: ")
        self.addNameButton = AddButton(
            self.nameFrame, command=self.onClickAddNameButton
        )
        self.nameEntry = CTkEntry(
            self.nameFrame, placeholder_text="Name", textvariable=self.varMacroName
        )

        self.triggerFrame = CTkFrame(self.leftColumn)
        self.triggerLabel = CTkLabel(self.triggerFrame, text="Trigger: ")
        self.addTriggerButton = AddButton(
            self.triggerFrame, command=self.onClickEditTriggerButton
        )
        self.triggerEntry = CTkEntry(
            self.triggerFrame,
            textvariable=self.varMacroTrigger,
        )
        vcmdTrigger = (self.register(self.validateTrigger), "%P")
        self.triggerEntry.configure(validate="key", validatecommand=vcmdTrigger)

        # left
        self.nameLabel.pack(side="left", expand=False, pady=5, padx=5)
        self.nameEntry.pack(side="left", expand=True, pady=5, padx=5)
        self.addNameButton.pack(side="left", expand=False, pady=5, padx=5)
        self.nameFrame.pack(fill="x", expand=False, pady=5, padx=5)

        self.triggerLabel.pack(side="left", expand=False, pady=5, padx=5)
        self.triggerEntry.pack(side="left", expand=True, pady=5, padx=5)
        self.addTriggerButton.pack(side="left", expand=False, pady=5, padx=5)
        self.triggerFrame.pack(fill="x", expand=False, pady=5, padx=5)

        self.list.pack(fill="both", expand=True)
        self.addNewButton.pack(fill="x")
        # right
        self.switch.pack(fill="y", anchor="center")
        self.keyLayoutButton.pack(side="left", padx=10, pady=10, anchor="center")
        self.waitLayoutButton.pack(side="left", padx=10, pady=10, anchor="center")
        self.textLayoutButton.pack(side="left", padx=10, pady=10, anchor="center")
        self.CMDLayoutButton.pack(side="left", padx=10, pady=10, anchor="center")

        self.formContainer.pack()
        self.addEditButton.pack(pady=10)

        self.setCurrentEditedLayout(0)  # set Key Form
        self.setCurrentEditedHotKey(-1)  # set on new input
    
    def validateTrigger(self, newText):
        if newText == "":
            return True
        elif len(newText) == 1:
            return newText.isalpha()
        else:
            return False

    def onClickAddNameButton(self):
        macroName = self.nameEntry.get().strip()
        if macroName != "":
            self.editName(self.macroId, macroName)

    def onClickEditTriggerButton(self):
        macroTrigger = self.triggerEntry.get().strip()
        self.editTrigger(self.macroId, macroTrigger)

    def onClickAddEditButton(self):
        if self.currentForm is None:
            return

        if isinstance(self.currentForm, KeyForm):
            keyInput = self.currentForm.getCapturedKey()
            if not keyInput:
                return
            pressType = self.currentForm.varRadio.get()
            self.guiModifyInput(
                0, self.macroId, self.currentEditedHotKey, keyInput, pressType
            )

        elif isinstance(self.currentForm, WaitForm):
            waitTimeInput = int(self.currentForm.entryWait.get().strip())
            if not waitTimeInput:
                return
            self.guiModifyInput(
                1, self.macroId, self.currentEditedHotKey, waitTimeInput
            )

        elif isinstance(self.currentForm, TextForm):
            textInput = self.currentForm.entryText.get().strip()
            if not textInput:
                return
            self.guiModifyInput(2, self.macroId, self.currentEditedHotKey, textInput)
        elif isinstance(self.currentForm, CMDForm):
            textInput = self.currentForm.boxText.get("0.0", "end").strip()
            if not textInput:
                return
            self.guiModifyInput(3, self.macroId, self.currentEditedHotKey, textInput)

        self.refreshList()
        self.setCurrentEditedHotKey(0)

    def onClickChoiseLayoutButton(self, layoutId):
        self.setCurrentEditedLayout(layoutId=layoutId)

    def setCurrentEditedLayout(self, layoutId, arg=""):
        if layoutId < 0:
            return

        self.currentEditedLayout = layoutId

        if self.currentForm is not None:
            self.currentForm.destroy()
            self.currentForm = None

        if layoutId == 0:
            self.currentForm = KeyForm(self.formContainer)
        elif layoutId == 1:
            self.currentForm = WaitForm(self.formContainer)
        elif layoutId == 2:
            self.currentForm = TextForm(self.formContainer)
        elif layoutId == 3:
            self.currentForm = CMDForm(self.formContainer, cmdText=arg)

        self.currentForm.pack(fill="both", expand=True)

    def onClickAddButton(self):
        self.setCurrentEditedHotKey(-1)
        self.setCurrentEditedLayout(0, arg="")
    def setCurrentEditedHotKey(self, hotKeyIndex):
        if hotKeyIndex == -1:
            self.currentEditedHotKey = -1
            self.setCurrentEditedLayout(0)
            self.refreshList()
            return

        if 0 <= hotKeyIndex < len(self.macro.inputSequence):
            hotkey = self.macro.inputSequence[hotKeyIndex]
            if isinstance(hotkey, InputKey):
                self.setCurrentEditedLayout(0)
            elif isinstance(hotkey, InputWait):
                self.setCurrentEditedLayout(1)
            elif isinstance(hotkey, InputText):
                self.setCurrentEditedLayout(2)
            elif isinstance(hotkey, InputCommand):
                self.setCurrentEditedLayout(3, arg=hotkey.string)
            else:
                self.setCurrentEditedLayout(0)
            self.currentEditedHotKey = hotKeyIndex
            self.refreshList()
        else:
            self.currentEditedHotKey = -1
            self.setCurrentEditedLayout(0)
            self.refreshList()

    def onWindowClose(self):
        if self.onClose is not None:
            self.onClose()
        self.destroy()

    def refreshList(self):
        self.list.currentEditedHotKey = self.currentEditedHotKey
        self.list._buildList()
