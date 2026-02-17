from .customButton import CustomButton


class DeleteButton(CustomButton):
    def __init__(self, parent, text:str="Delete", command=None):
        super().__init__(
            parent,
            text=text,
            height=40,
            corner_radius=10,
            fg_color="#F41",
            hover_color="#a41",
            text_color="#222",
            command=command,
        )