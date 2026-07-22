from tkinter import Canvas, Event
from typing import TYPE_CHECKING

from CTkColorPicker import AskColor

if TYPE_CHECKING:
    from collections.abc import Callable
    
    from customtkinter import CTkFrame

from eggtimer.constants import MOUSE_BTN__LEFT


class ColorPickerBtn(Canvas):
    def __init__(self, parent: CTkFrame, w: int = 30, h: int = 25, color_hex: str = "#00C487", pick_handler: Callable | None = None) -> None:
        super().__init__(parent, width=w, height=h)
        self.w = w
        self.h = h
        self.color = color_hex
        self.handler = pick_handler
        self.bind(MOUSE_BTN__LEFT, self.handle_click)
        self.render()
    
    def handle_click(self, _ev: Event) -> None:
        result = AskColor(
          initial_color=self.color,
          title="Pick Timer Color",
        )
        color = result.get()
        
        if color:
            self.set_color(color)
            
            if self.handler:
                self.handler(self.color)
    
    def render(self) -> None:
        bw = 1
        self.create_rectangle(0 + bw, 0 + bw, self.w - bw, self.h - bw, fill="#CCCCCC", outline="#666666", width=bw)
        offset = 4
        self.create_rectangle(offset + bw, offset + bw, self.w - (offset + bw), self.h - (offset + bw), fill=self.color, outline="#000000", width=bw)
    
    def set_color(self, color: str) -> None:
        self.color = color
        self.render()
