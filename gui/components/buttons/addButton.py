from .customButton import CustomButton


class AddButton(CustomButton):
    def __init__(self, parent, text:str="Add",width:int=100, command=None):
        super().__init__(
            parent,
            text=text,
            height=40,
            width=width,
            corner_radius=10,
            fg_color="#1A1",
            hover_color="#060",
            text_color="#222",
            command=command,
        )
