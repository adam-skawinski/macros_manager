from customtkinter import CTkButton


class CustomButton(CTkButton):
    def __init__(
        self,
        parent,
        text: str = "Button text",
        fg_color: str = "blue",
        width: int = 50,
        height:int = 40,
        corner_radius=10,
        text_color="#222",
        hover_color="#555",
        command=None,
    ):
        super().__init__(
            parent,
            text=text,
            fg_color=fg_color,
            width=width,
            height=height,
            corner_radius=corner_radius,
            text_color=text_color,
            hover_color=hover_color,
            command=command,
        )
