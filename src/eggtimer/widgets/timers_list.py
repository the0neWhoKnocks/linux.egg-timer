import logging
import uuid

from customtkinter import CTk, CTkScrollableFrame

from eggtimer.constants import LOGGER_NAMESPACE

from .timer import Timer

log = logging.getLogger(LOGGER_NAMESPACE)


class TimersList(CTkScrollableFrame):
    def __init__(self, parent: CTk) -> None:
        super().__init__(parent)
        self.timers = {}
    
    def add_timer(self, color: str, name: str, hrs: str, mins: str, secs: str) -> None:
        timer = Timer(self, color=color, name=name, hours=hrs, minutes=mins, seconds=secs)
        uid = uuid.uuid1().hex
        self.timers[uid] = timer
        timer.delete_btn.configure(command=lambda: self.remove_timer(uid))
        log.info("Added Timer: %s, %s, [%s:%s:%s]", color, name, hrs, mins, secs)
    
    def remove_timer(self, uid: str) -> None:
        timer = self.timers[uid]
        timer_name = timer.name
        timer.destroy()
        del self.timers[uid]
        log.info("Removed Timer: %s", timer_name)
