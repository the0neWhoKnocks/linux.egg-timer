import logging
from tkinter import END
from typing import TYPE_CHECKING

from customtkinter import (
    CTk,
    CTkButton,
    CTkEntry,
    CTkFrame,
    CTkLabel,
)

from eggtimer.constants import LOGGER_NAMESPACE

from .color_picker_btn import ColorPickerBtn
from .timer_editable import EditableTimer

if TYPE_CHECKING:
    from collections.abc import Callable

log = logging.getLogger(LOGGER_NAMESPACE)


class TimerForm(CTkFrame):
    def __init__(self, parent: CTk, btn_label: str, btn_handler: Callable) -> None:
        super().__init__(parent)
        self.cp = ColorPickerBtn(self, pick_handler=lambda c: log.info("User chose color '%s' for timer", c))
        self.cp.grid(row=0, column=0)
        self.label = CTkLabel(self, text="Name:")
        self.label.grid(row=0, column=1)
        self.input = CTkEntry(self)
        self.input.grid(row=0, column=2)
        self.timer = EditableTimer(self)
        self.timer.grid(row=0, column=3)
        self.btn = CTkButton(self, text=btn_label, command=btn_handler)
        self.btn.grid(row=0, column=4)
    
    def get_color(self) -> str:
        return self.cp.color
    
    def get_name(self) -> str:
        return self.input.get()
    
    def get_time(self) -> tuple[str, str, str]:
        hours = self.timer.val_hours.get()
        mins = self.timer.val_mins.get()
        secs = self.timer.val_secs.get()
        return (hours, mins, secs)
    
    def reset(self) -> None:
        self.input.delete(0, END)
        self.timer.reset_vals()
