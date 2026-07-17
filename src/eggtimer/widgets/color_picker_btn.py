from tkinter import Canvas, colorchooser
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from tkinter import Event, Tk

from eggtimer.constants import MOUSE_BTN__LEFT


class ColorPickerBtn(Canvas):
    def __init__(self, parent: Tk, w: int = 30, h: int = 25, color_hex: str = "#00C487", pick_handler: Callable | None = None) -> None:
        super().__init__(parent, width=w, height=h)
        self.w = w
        self.h = h
        self.color = color_hex
        self.handler = pick_handler
        self.bind(MOUSE_BTN__LEFT, self.handle_click)
        self.render()
    
    def handle_click(self, _ev: Event) -> None:
        rgb, hex = colorchooser.askcolor(title="Pick Color", color=self.color)  # noqa: A001, RUF059
        if hex:
            self.color = hex
            self.render()
            if self.handler:
                self.handler(self.color)
    
    def render(self) -> None:
        bw = 1
        self.create_rectangle(0 + bw, 0 + bw, self.w - bw, self.h - bw, fill="#CCCCCC", outline="#666666", width=bw)
        offset = 4
        self.create_rectangle(offset + bw, offset + bw, self.w - (offset + bw), self.h - (offset + bw), fill=self.color, outline="#000000", width=bw)
