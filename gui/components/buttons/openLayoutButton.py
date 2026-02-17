from .customButton import CustomButton


class OpenLayoutButton(CustomButton):
    def __init__(
        self,
        parent,
        text: str = "Button",
        fg_color: str = "#0f0",
        width: int = 50,
        height: int = 40,
        command=None,
    ):
        super().__init__(
            parent,
            text=text,
            width=width,
            height=height,
            corner_radius=10,
            hover_color="#555",
            fg_color=fg_color,
            text_color="#222",
            command=command,
        )
