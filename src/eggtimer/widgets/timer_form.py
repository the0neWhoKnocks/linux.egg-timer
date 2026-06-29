import logging
import tkinter as tk
from tkinter import ttk

from eggtimer.constants import LOGGER_NAMESPACE

from .color_picker_btn import ColorPickerBtn
from .timer_editable import EditableTimer

log = logging.getLogger(LOGGER_NAMESPACE)


class TimerForm(ttk.Frame):
    def __init__(self, parent: tk.Tk, btn_label: str, btn_handler: callable) -> None:
        super().__init__(parent)
        self.cp = ColorPickerBtn(self, pick_handler=lambda c: log.info("User chose color '%s' for timer", c))
        self.cp.grid(row=0, column=0)
        self.label = ttk.Label(self, text="Name:")
        self.label.grid(row=0, column=1)
        self.input = ttk.Entry(self)
        self.input.grid(row=0, column=2)
        self.timer = EditableTimer(self)
        self.timer.grid(row=0, column=3)
        self.btn = ttk.Button(self, text=btn_label, command=btn_handler)
        self.btn.grid(row=0, column=4)
