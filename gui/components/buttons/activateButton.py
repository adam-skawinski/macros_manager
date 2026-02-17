from .customButton import CustomButton


class ActivateButton(CustomButton):
    def __init__(self, parent, text: str = "Button", command=None):


        super().__init__(
            parent,
            text=text,
            height=40,
            corner_radius=10,
            fg_color="#232",
            hover_color="#060",
            text_color="#fff",
            command=self.onClick,
        )
        self.activated = False
        self.userCommand = command

    def onClick(self):
        self.activated = not self.activated

        if self.activated:
            self.configure(fg_color="#0f0")
            self.configure(text="Deactivate")
            self.configure(text_color="#222")
        else:
            self.configure(text="Activate")
            self.configure(fg_color="#232")
            self.configure(text_color="#fff")

        if self.userCommand:
            self.userCommand()
