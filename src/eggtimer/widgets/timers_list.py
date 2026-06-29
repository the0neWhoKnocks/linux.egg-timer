import logging
from typing import TYPE_CHECKING

from eggtimer.constants import LOGGER_NAMESPACE

from .timer import Timer
from .widget_list import WidgetList

if TYPE_CHECKING:
    import tkinter as tk

log = logging.getLogger(LOGGER_NAMESPACE)


class TimersList(WidgetList):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
    
    def add_timer(self, color: str, name: str, hrs: str, mins: str, secs: str) -> None:
        uid, timer = self.add_item(
            Timer,
            color=color,
            name=name,
            hours=hrs,
            minutes=mins,
            seconds=secs,
        )
        timer.delete_btn.configure(command=lambda: self.remove_timer(uid))
        log.info("Added Timer: %s, %s, [%s:%s:%s]", color, name, hrs, mins, secs)
    
    def remove_timer(self, uid: str) -> None:
        timer_name = self.widgets[uid].name
        self.remove_item(uid)
        log.info("Removed Timer: %s", timer_name)
