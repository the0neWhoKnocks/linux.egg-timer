from tkinter import Canvas
from typing import TYPE_CHECKING

from customtkinter import (
    CTkButton,
    CTkFrame,
    CTkLabel,
    CTkScrollableFrame,
)

if TYPE_CHECKING:
    from collections.abc import Callable


class Timer(CTkFrame):
    def __init__(  # noqa: PLR0913
        self,
        parent: CTkScrollableFrame,
        *,
        color: str,
        name: str,
        hours: str,
        minutes: str,
        seconds: str,
        delete_handler: Callable | None = None,
    ) -> None:
        super().__init__(parent, border_width=1)
        self.pack(fill="x", pady=2, padx=5)
        self.name = name
        self.color_chip = Canvas(self, width=30, height=30, bg=color)
        self.color_chip.pack(side="left", padx=5)
        self.label = CTkLabel(self, text=name)
        self.label.pack(side="left", padx=5)
        self.time = CTkLabel(self, text=f"{hours}:{minutes}:{seconds}")
        self.time.pack(side="left", padx=5)
        self.delete_btn = CTkButton(self, text="Delete", command=delete_handler)
        self.delete_btn.pack(side="left", padx=5)
