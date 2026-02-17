import os
from json import JSONDecodeError

# import inputObjClass
import logic
from os import system  # cls :*
from logic.macroObjClass import Macro
from logic.inputObjClass import InputKey, InputText, InputWait, InputCommand
import re  # regex
from pynput import keyboard  # input handler
from pynput.mouse import Button, Controller as MouseController
import time
import jsonpickle
import subprocess
import joblib


class Main:
    def __init__(self):
        self.version = 0.5
        self.editedMacro = -1
        self.queue = []
        self.registeredMacros = []
        self.queueActive = False
        self.keyInput = keyboard.Controller()
        self.mouseInput = MouseController()
        self.baseDir = os.path.dirname(os.path.abspath(__file__))
        self.macrosDir = os.path.join(self.baseDir, "Macros")
        self.modelCmdValidPath = os.path.join(
            self.baseDir, "ML\\trainedModels\\randomforest_cmd_pipeline.joblib"
        )
        self.listener = keyboard.Listener(
            on_press=self.onPress, on_release=self.onRelease
        )
        self.listenerActive = False
        self.readConfig()
        # self.mainMenu("") #TODO: for debug

    # Config handlers

    def readConfig(self):
        if not os.path.exists(self.macrosDir):
            os.mkdir(self.macrosDir, "Macros")
        index = 0

        exists = True
        while exists:
            macroPath = os.path.join(self.macrosDir, f"Macro{index}.json")
            if os.path.exists(macroPath):
                with open(macroPath, "r") as macroFile:
                    try:
                        obj = jsonpickle.decode(macroFile.read())
                        self.registeredMacros.append(obj)
                        macroFile.close()
                        index = index + 1
                    except JSONDecodeError:
                        macroFile.close()
                        self.cfgClearRemove(index)

            else:
                exists = False

    def cfgClearRemove(self, id):
        if os.path.isfile(self.macrosDir + f"/Macro{id}.json"):
            os.remove(self.macrosDir + f"/Macro{id}.json")
            while os.path.isfile(self.macrosDir + f"/Macro{id + 1}.json"):
                os.renames(
                    self.macrosDir + f"/Macro{id + 1}.json",
                    self.macrosDir + f"/Macro{id}.json",
                )
                id = id + 1
        else:
            print("Error: Macro file not found.")

    def saveConfig(self):
        for i in range(len(self.registeredMacros)):
            with open(self.macrosDir + f"/Macro{i}.json", "w+") as macroFile:
                obj = self.registeredMacros[i]
                encodedObj = jsonpickle.encode(obj)
                macroFile.write(encodedObj)
                macroFile.close()

    def cfgUpdateMacro(self, id):
        with open(self.macrosDir + f"/Macro{id}.json", "w+") as macroFile:
            obj = self.registeredMacros[id]
            encodedObj = jsonpickle.encode(obj)
            macroFile.write(encodedObj)
            macroFile.close()

    # Command Handler
    def runMacros(self):
        if self.listenerActive:
            self.listener.stop()
        else:
            self.listener = keyboard.Listener(
                on_press=self.onPress, on_release=self.onRelease
            )
            self.listener.start()

        self.listenerActive = not self.listenerActive

    def readCommand(self):
        print("")
        command = input("> ").strip()
        if self.editedMacro == -1:
            if re.search(
                "^(add){1}\\s([a-z]|[0-9]){3,16}$", str(command).lower()
            ):  # name cannot be shorter than 3 and longer than 16 characters
                name = command.split(" ")[1]
                self.addMacro(name)

            elif re.search("^(edit){1}\\s([0-9])+$", str(command).lower()):
                id = int(command.split(" ")[1])
                if len(self.registeredMacros) > id:
                    self.editedMacro = id
                    self.editMenu(id, "")

            elif re.search("^(remove|delete){1}\\s([0-9])+$", str(command).lower()):
                id = int(command.split(" ")[1])
                if len(self.registeredMacros) > id:
                    self.removeMacro(id)
            elif re.search("^shutdown$", str(command).lower()):
                print("Closing the program")
            elif re.search("^run$", str(command).lower()):
                print("Macros active")
                with keyboard.Listener(
                    on_press=self.onPress, on_release=self.onRelease
                ) as listener:
                    listener.join()
            else:
                self.clearConsole()
                self.mainMenu("Invalid command: " + str(command))

        else:

            obj = self.registeredMacros[self.editedMacro]
            if re.search(
                "^add{1}$", str(command).lower()
            ):  # name cannot be shorter than 3 and longer than 16 characters
                self.modifyInput(self.editedMacro, -1)

            elif re.search("^(edit){1}\\s([0-9])+$", str(command).lower()):
                id = int(command.split(" ")[1])
                if len(obj.inputSequence) > id:
                    self.modifyInput(self.editedMacro, id)

            elif re.search("^(remove|delete){1}\\s([0-9])+$", str(command).lower()):
                id = int(command.split(" ")[1])
                if len(obj.inputSequence) > id:
                    self.removeInput(self.editedMacro, id)

            elif re.search("^(setTrigger|trigger)$", str(command).lower()):
                key = input("Key >> ")
                obj = self.registeredMacros[self.editedMacro]
                obj.trigger = keyboard.KeyCode.from_char(key)
                self.registeredMacros[self.editedMacro] = obj
                self.cfgUpdateMacro(self.editedMacro)
                self.editMenu(
                    self.editedMacro,
                    "Successfully changed macro trigger to: " + str(key),
                )
            elif re.search("^done$", str(command).lower()):
                self.editedMacro = -1
                self.mainMenu("Saved macro settings.")
            elif re.search("^shutdown$", str(command).lower()):
                print("Closing the program")
            else:
                self.clearConsole()
                self.editMenu(self.editedMacro, "Invalid command: " + str(command))

    def editTrigger(self, macrosId, key):
        obj = self.registeredMacros[macrosId]
        obj.trigger = keyboard.KeyCode.from_char(key)
        self.registeredMacros[macrosId] = obj
        self.cfgUpdateMacro(macrosId)

    def editName(self, macrosId, newName):
        obj = self.registeredMacros[macrosId]
        obj.name = newName
        self.registeredMacros[macrosId] = obj
        self.cfgUpdateMacro(macrosId)

    # Menu

    def mainMenu(self, err):
        print("Macro editor - build " + str(self.version))
        print("| ID | Nazwa | Trigger |")
        print("------------------------")
        print("")
        if len(self.registeredMacros) > 0:
            for i in range(len(self.registeredMacros)):
                macroObj = self.registeredMacros[i]
                trigger = macroObj.trigger
                if trigger == -1:
                    trigger = "Brak"
                print(
                    "| "
                    + str(i)
                    + " | "
                    + str(macroObj.name)
                    + " | "
                    + str(trigger)
                    + " |"
                )

        else:
            print("- No macros registered - ")
        print("")
        if err != "":
            print(err)

        self.readCommand()

    def editMenu(self, id, err):
        obj = self.registeredMacros[id]
        print("Macro: " + str(obj.name))
        for i in range(len(obj.inputSequence)):
            cInput = obj.inputSequence[i]
            printStr = "| " + str(i) + " | "
            if isinstance(cInput, logic.inputObjClass.InputKey):
                if cInput.state == 1:
                    printStr = printStr + "Press"
                else:
                    printStr = printStr + "Release"
                printStr = printStr + " | " + str(cInput.key) + " |"
            elif isinstance(cInput, logic.inputObjClass.InputWait):
                printStr = printStr + "Wait | " + str(cInput.time) + "ms |"
            elif isinstance(cInput, logic.inputObjClass.InputText):
                printStr = printStr + "TypeText | " + str(cInput.string) + " |"
            elif isinstance(cInput, logic.inputObjClass.InputCommand):
                printStr = printStr + "Command | " + str(cInput.string) + " |"

            print(printStr)

        print("")
        if err != "":
            print(err)
        self.readCommand()

    # Simple hooks for add/remove of Macro obj

    def addMacro(self, name):
        self.registeredMacros.append(Macro(str(name)))
        self.cfgUpdateMacro(len(self.registeredMacros) - 1)
        # self.mainMenu("Macro successfully added: " + str(name)) #TODO: for debug

    def removeMacro(self, id):
        name = Macro(self.registeredMacros[id]).name
        self.registeredMacros.pop(id)
        self.cfgClearRemove(id)
        # self.mainMenu("Macro successfully removed: " + str(name)) #TODO: for debug

    # Modifying (or adding if invalid ID)
    def validCmdPrompt(self, cmd):
        print("COMMAND:", cmd)
        modelClf = joblib.load(self.modelCmdValidPath)
        isDangerous = modelClf.predict([cmd])[0]
        if isDangerous:
            print("Dangerous!!!")
        else:
            print("Safe :)")
        return isDangerous

    def guiModifyInput(
        self, inputType=0, macroId=0, hotKeyId=-1, arg1=1, state=0
    ):  # - id of edited sequence step, -1 for adding new.

        if inputType <= 3 and inputType >= 0:
            if inputType == 0:
                if arg1 == "LCTRL":
                    newInput = logic.inputObjClass.InputKey(keyboard.Key.ctrl_l, state)
                elif arg1 == "RCTRL":
                    newInput = logic.inputObjClass.InputKey(keyboard.Key.ctrl_r, state)

                elif arg1 == "LALT":
                    newInput = logic.inputObjClass.InputKey(keyboard.Key.alt_l, state)
                elif arg1 == "RALT":
                    newInput = logic.inputObjClass.InputKey(keyboard.Key.alt_r, state)

                elif arg1 == "LSHIFT":
                    newInput = logic.inputObjClass.InputKey(keyboard.Key.shift_l, state)
                elif arg1 == "RSHIFT":
                    newInput = logic.inputObjClass.InputKey(keyboard.Key.shift_r, state)

                else:
                    newInput = logic.inputObjClass.InputKey(
                        keyboard.KeyCode.from_char(arg1), state
                    )

            elif inputType == 1:
                newInput = logic.inputObjClass.InputWait(arg1)

            elif inputType == 2:
                newInput = logic.inputObjClass.InputText(arg1)

            elif inputType == 3:
                self.validCmdPrompt(arg1)
                newInput = logic.inputObjClass.InputCommand(arg1)

            obj = self.registeredMacros[macroId]

            if hotKeyId == -1:
                obj.inputSequence.append(newInput)
                self.registeredMacros[macroId] = obj
                self.cfgUpdateMacro(macroId)
            else:
                obj.inputSequence[hotKeyId] = newInput
                self.registeredMacros[macroId] = obj
                self.cfgUpdateMacro(macroId)

    def modifyInput(
        self, macroId=-1, id=-1
    ):  # - id of edited sequence step, -1 for adding new.
        inputType = int(input("Input Type (0: Key, 1: Wait, 2: Insert text) >> "))
        newInput = ""
        if inputType <= 3 and inputType >= 0:
            if inputType == 0:
                key = input("Key >> ")
                state = int(input("Keystate (1: Press/0: Release)>> "))

                if key == "LCTRL":
                    newInput = logic.inputObjClass.InputKey(keyboard.Key.ctrl_l, state)
                elif key == "RCTRL":
                    newInput = logic.inputObjClass.InputKey(keyboard.Key.ctrl_r, state)

                elif key == "LALT":
                    newInput = logic.inputObjClass.InputKey(keyboard.Key.alt_l, state)
                elif key == "RALT":
                    newInput = logic.inputObjClass.InputKey(keyboard.Key.alt_r, state)

                elif key == "LSHIFT":
                    newInput = logic.inputObjClass.InputKey(keyboard.Key.shift_l, state)
                elif key == "RSHIFT":
                    newInput = logic.inputObjClass.InputKey(keyboard.Key.shift_r, state)

                elif key == "LMB":
                    newInput = logic.inputObjClass.InputKey(Button.left, state)
                elif key == "RMB":
                    newInput = logic.inputObjClass.InputKey(Button.right, state)
                else:
                    newInput = logic.inputObjClass.InputKey(
                        keyboard.KeyCode.from_char(key), state
                    )

            elif inputType == 1:
                timeout = int(input("Timeout >> "))
                newInput = logic.inputObjClass.InputWait(timeout)
            elif inputType == 2:
                text = input("Enter text>> ")
                newInput = logic.inputObjClass.InputText(text)
            elif inputType == 3:
                cmd = input("Enter command>> ")
                newInput = logic.inputObjClass.InputCommand(cmd)

            obj = self.registeredMacros[macroId]
            if id == -1:
                obj.inputSequence.append(newInput)
                self.registeredMacros[macroId] = obj
                print("x")
                self.cfgUpdateMacro(macroId)
                self.editMenu(macroId, "Imput added successfully")
            else:
                obj.inputSequence[id] = newInput
                self.registeredMacros[macroId] = obj
                self.cfgUpdateMacro(macroId)
                self.editMenu(macroId, "Imput edited successfully")
        else:

            if id == -1:
                self.editMenu(macroId, "Failed to add input: incorrect type.")
            else:
                self.editMenu(macroId, "Failed to edit input: incorrect type.")

    def guiRemoveInput(self, macroId=-1, hotKeyId=-1):
        if hotKeyId != -1:
            obj = self.registeredMacros[macroId]
            obj.inputSequence.pop(hotKeyId)
            self.cfgUpdateMacro(macroId)

    def removeInput(self, macroId=-1, hotKeyId=-1):
        if hotKeyId != -1:
            obj = self.registeredMacros[macroId]
            obj.inputSequence.pop(hotKeyId)
            print("Input no. " + str(hotKeyId) + " removed successfully")
            self.cfgUpdateMacro(macroId)
        else:
            print("incorrect sequence")
        self.editMenu(macroId, ".")

    # Utils

    def clearConsole(self):
        system("cls")

    # Execution

    def queueManager(self):
        if self.queueActive == False:
            self.queueActive = True
            if len(self.queue) > 0:
                self.executeSequence(
                    self.queue.pop(0)
                )  # pop removes (id) element from list, and returns it as return of a call.
            else:
                self.queueActive = False

    def executeSequence(self, seq):
        for x in seq:
            if isinstance(x, logic.inputObjClass.InputKey):
                if x.state == 1:

                    if isinstance(x.key, Button):
                        self.mouseInput.press(x.key)
                    else:
                        self.keyInput.press(x.key)
                else:
                    if isinstance(x.key, Button):
                        self.mouseInput.release(x.key)
                    else:
                        self.keyInput.release(x.key)

            elif isinstance(x, logic.inputObjClass.InputWait):
                time.sleep(x.time * 0.001)
            elif isinstance(x, logic.inputObjClass.InputText):
                try:
                    self.keyInput.type(x.string)
                except:
                    print("Invalid character found in type-sequence")

            elif isinstance(x, logic.inputObjClass.InputCommand):
                try:
                    self.executeCommandInput(x.string)
                except Exception as e:
                    print("Invalid character found in command", e)
            else:
                print("Invalid Input Object registered.")

        if len(self.queue) > 0:
            self.executeSequence(self.queue.pop(0))
        else:
            self.queueActive = False

    def onPress(self, key):
        # print("Pressed key: " + str(key))
        for i in range(len(self.registeredMacros)):
            macro = self.registeredMacros[i]
            if macro.trigger == key:
                # print("true")
                self.queue.append(macro.inputSequence)
                if self.queueActive == False:
                    self.queueManager()

    def onRelease(self, key):
        return
        # print("Released key: "+str(key)) #Placeholder

    def executeCommandInput(self, cmd):
        try:
            run = subprocess.run(
                cmd,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
            )
            print(run.stdout)
            return [run.stdout, run.stderr]
        except subprocess.CalledProcessError as e:
            print("Command failed!")
            print("Return code:", e.returncode)
            print("Output:", e.output)
            print("Error:", e.stderr)


Main()
