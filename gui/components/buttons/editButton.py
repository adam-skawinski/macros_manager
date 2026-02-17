from .customButton import CustomButton

class EditButton(CustomButton):
    def __init__(self, parent, text:str="Edit", command=None):
        super().__init__(
            parent,
            text=text,
            height=40,
            corner_radius=10,
            fg_color="#F91",
            hover_color="#A40",
            text_color="#222",
            command=command,
        )