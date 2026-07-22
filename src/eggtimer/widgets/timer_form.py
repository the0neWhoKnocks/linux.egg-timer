import logging
from tkinter import END
from typing import TYPE_CHECKING

from customtkinter import (
    CTkButton,
    CTkEntry,
    CTkFrame,
    CTkLabel,
)

from eggtimer.constants import (
    BTN_WIDTH,
    FONT__ICONS__FAMILY,
    FONT__ICONS__SIZE,
    ICON__ADD,
    ICON__SAVE,
    LOGGER_NAMESPACE,
)

from .color_picker_btn import ColorPickerBtn
from .timer_editable import EditableTimer

if TYPE_CHECKING:
    from collections.abc import Callable
    
    from eggtimer.__main__ import EggTimer

log = logging.getLogger(LOGGER_NAMESPACE)


class TimerForm(CTkFrame):
    def __init__(self, parent: EggTimer, add_handler: Callable, save_handler: Callable) -> None:
        super().__init__(parent)
        self.root = parent
        self.uid = None
        
        self.cp = ColorPickerBtn(self, pick_handler=lambda c: log.info("User chose color '%s' for timer", c))
        self.cp.grid(row=0, column=0)
        self.label = CTkLabel(self, text="Name:")
        self.label.grid(row=0, column=1)
        self.input = CTkEntry(self)
        self.input.grid(row=0, column=2)
        self.timer = EditableTimer(self)
        self.timer.grid(row=0, column=3)
        self.add_btn = CTkButton(self,
          font=(FONT__ICONS__FAMILY, FONT__ICONS__SIZE),
          text=ICON__ADD,
          width=BTN_WIDTH,
          command=add_handler,
        )
        self.add_btn.grid(row=0, column=4)
        self.save_btn = CTkButton(self,
          font=(FONT__ICONS__FAMILY, FONT__ICONS__SIZE),
          text=ICON__SAVE,
          width=BTN_WIDTH,
          command=lambda: save_handler(self.uid),
        )
        self.save_btn.grid(row=0, column=5)
        self.save_btn.grid_remove()  # hide it
    
    def edit(self, uid: str) -> None:
        conf = self.root.app_config.data["timers"][uid]
        self.uid = uid
        
        self.cp.set_color(conf["color"])
        self.input.set(conf["name"])
        self.timer.val_hours.set(conf["hours"])
        self.timer.val_mins.set(conf["mins"])
        self.timer.val_secs.set(conf["secs"])
        self.add_btn.grid_remove()  # hide
        self.save_btn.grid()  # show
    
    def get_color(self) -> str:
        return self.cp.color
    
    def get_form_data(self) -> tuple[str, str, str, str, str]:
        name = self.get_name()
        hrs, mins, secs = self.get_time()
        color = self.get_color()
        return color, name, hrs, mins, secs
    
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
        
        if self.uid:
            self.add_btn.grid()  # show
            self.save_btn.grid_remove()  # hide
            self.uid = None
