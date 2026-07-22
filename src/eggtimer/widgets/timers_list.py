import asyncio
import logging
import threading
import uuid
from time import localtime, strftime
from typing import TYPE_CHECKING

from customtkinter import CTkScrollableFrame
from desktop_notifier import DesktopNotifier, Icon, Urgency
from playsound3 import playsound

from eggtimer.constants import (
  APP_DIR,
  APP_NAME,
  APP_NAME_FORMATTED,
  LOGGER_NAMESPACE,
)

from .timer import Timer

if TYPE_CHECKING:
    from eggtimer.__main__ import EggTimer

log = logging.getLogger(LOGGER_NAMESPACE)


class TimersList(CTkScrollableFrame):
    def __init__(self, parent: EggTimer) -> None:
        super().__init__(parent)
        self.alarm = None
        self.alarm_sound = None
        self.completed_timers = {}
        self.root = parent
        self.timers = {}
        
        self.load_saved_timers()
    
    def add_timer(self,  # noqa: PLR0913
      color: str, name: str, hrs: str, mins: str, secs: str,
      *, uid: str | None = None,
    ) -> str:
        uid = uuid.uuid1().hex if uid is None else uid
        
        timer = Timer(self,
          root=self.root,
          color=color,
          delete_handler=lambda: self.remove_timer(uid),
          done_handler=lambda: asyncio.run(self.notify_user(name, uid)),
          edit_handler=lambda: self.edit_timer(uid),
          name=name,
          hours=hrs,
          minutes=mins,
          seconds=secs,
          stop_handler=lambda: self.handle_timer_stop(uid),
        )
        self.timers[uid] = timer
        
        log.info("Added Timer: %s, %s, [%s:%s:%s]", color, name, hrs, mins, secs)
        
        return uid
    
    def edit_timer(self, uid: str) -> None:
        self.root.timer_form.edit(uid)
    
    def handle_timer_stop(self, uid: str) -> None:
        if uid in self.completed_timers:
            del self.completed_timers[uid]
        
        if len(self.completed_timers) == 0:
            self.stop_signal.set()
    
    def load_saved_timers(self) -> None:
        # `data` and `timers` won't exist on first run
        try:
            for uid, timer in self.root.app_config.data["timers"].items():
                self.add_timer(
                  color=timer["color"],
                  name=timer["name"],
                  hrs=timer["hours"],
                  mins=timer["mins"],
                  secs=timer["secs"],
                  uid=uid,
                )
        except KeyError:
            pass
    
    async def notify_user(self, timer_name: str, uid: str) -> None:
        notifier = DesktopNotifier(
          app_name=APP_NAME,
          app_icon=Icon(name=APP_NAME),  # icon won't show up until launcher and icon are installed on system
        )
        
        await notifier.send(
          title=APP_NAME_FORMATTED,
          message=f'Timer "{timer_name}" completed at {strftime("%I:%M", localtime())}',
          timeout=3,  # seconds
          urgency=Urgency.Normal,
        )
        
        self.completed_timers[uid] = True
        
        if self.alarm is None:
            self.play_alarm()
    
    def play_alarm(self) -> None:
        def play(exit_event: threading.Event) -> None:
            while not exit_event.is_set():
                # If `block` is set a User can't stop immediately, so set the
                # `timeout` to roughly the length of the sound and the gap you
                # want between playing.
                self.alarm_sound = playsound(f"{APP_DIR}/assets/alarm.wav", block=False)
                if exit_event.wait(timeout=2):
                    break
            
            self.alarm = None
            log.info("Alarm stopped")
        
        self.stop_signal = threading.Event()
        self.alarm = threading.Thread(name="Alarm", target=play, args=(self.stop_signal,))
        self.alarm.start()
    
    def remove_timer(self, uid: str) -> None:
        timer = self.timers[uid]
        timer_name = timer.name
        timer.destroy()
        del self.timers[uid]
        del self.root.app_config.data["timers"][uid]
        self.root.app_config.save()
        log.info("Removed Timer: %s", timer_name)
