from time import time
from typing import TYPE_CHECKING

from customtkinter import (
    CTkButton,
    CTkFrame,
    CTkLabel,
)

from eggtimer.constants import (
    BTN_WIDTH,
    FONT__ICONS__FAMILY,
    FONT__ICONS__SIZE,
    ICON__DELETE,
    ICON__EDIT,
    ICON__PLAY,
    ICON__STOP,
)
from eggtimer.widgets import DigitalDisplay

if TYPE_CHECKING:
    from collections.abc import Callable
    from tkinter import Event
    
    from eggtimer.__main__ import EggTimer
    from eggtimer.widgets import TimersList

X_SPACING = 5
colors = {
  "play": "green",
  "stop": "red",
}


class Timer(CTkFrame):
    def __init__(  # noqa: PLR0913
        self,
        parent: TimersList,
        *,
        root: EggTimer,
        color: str,
        name: str,
        hours: str,
        minutes: str,
        seconds: str,
        delete_handler: Callable,
        done_handler: Callable,
        edit_handler: Callable,
        stop_handler: Callable,
    ) -> None:
        super().__init__(parent, border_width=1)
        
        self.set_time_vals(hours, minutes, seconds)
        
        self.color = color
        self.completed = False
        self.delete_handler = delete_handler
        self.done_handler = done_handler
        self.edit_handler = edit_handler
        self.name = name
        self.render_loop = None
        self.root = root
        self.running = False
        self.stop_handler = stop_handler
        
        self.build_ui()
    
    def build_ui(self) -> None:
        self.pack(fill="x", pady=2, padx=X_SPACING)
        self.color_chip = CTkLabel(self,
          corner_radius=5,
          fg_color=self.color,
          text="",
          width=20,
        )
        self.color_chip.pack(side="left", padx=2, pady=2)
        self.timer_toggle = CTkButton(self,
          font=(FONT__ICONS__FAMILY, FONT__ICONS__SIZE),
          text=ICON__PLAY,
          fg_color=colors["play"],
          border_color="#000000",
          width=BTN_WIDTH,
          command=self.toggle_timer_btn,
        )
        self.timer_toggle.pack(side="left", padx=X_SPACING, pady=2)
        self.time = DigitalDisplay(self, self.root, top_txt=self.start_time_str)
        self.time.pack(side="left", padx=X_SPACING)
        self.label = CTkLabel(self, text=self.name)
        self.label.pack(side="left", padx=X_SPACING)
        self.delete_btn = CTkButton(self,
          font=(FONT__ICONS__FAMILY, FONT__ICONS__SIZE),
          text=ICON__DELETE,
          width=BTN_WIDTH,
          command=self.delete_timer,
        )
        self.delete_btn.pack(side="right", padx=X_SPACING)
        self.edit_btn = CTkButton(self,
          font=(FONT__ICONS__FAMILY, FONT__ICONS__SIZE),
          text=ICON__EDIT,
          width=BTN_WIDTH,
          command=self.edit_timer,
        )
        self.edit_btn.pack(side="right", padx=X_SPACING)
    
    def delete_timer(self, _ev: Event | None = None) -> None:
        if self.render_loop is not None:
            self.root.after_cancel(self.render_loop)
        
        self.delete_handler()
    
    def edit_timer(self, _ev: Event | None = None) -> None:
        self.edit_handler()
    
    def render(self) -> None:
        if not self.running and not self.completed:
            return
        
        current_time = time()
        remaining_time = self.end_time - current_time
        
        seconds = int(remaining_time)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        self.time.update_prop(text=f"{hours:02}:{minutes:02}:{seconds:02}")
        
        if remaining_time > 0:
            self.render_loop = self.root.after(100, self.render)  # check in milliseconds so the UI responds quickly to clicks
        else:
            self.completed = True
            self.time.blink_start()
            self.done_handler()
    
    def set_time_vals(self, hours: str, minutes: str, seconds: str) -> None:
        self.start_time_str = f"{hours}:{minutes}:{seconds}"
        self.total_secs = float((int(hours) * 3600) + (int(minutes) * 60) + int(seconds))
    
    def toggle_timer_btn(self, _ev: Event | None = None) -> None:
        self.running = not self.running
        
        if self.running:
            self.timer_toggle.configure(
              fg_color=colors["stop"],
              text=ICON__STOP,
            )
            
            self.start_time = time()
            self.end_time = self.start_time + self.total_secs
            
            self.render()
        else:
            self.timer_toggle.configure(
              fg_color=colors["play"],
              text=ICON__PLAY,
            )
            
            self.time.blink_stop()
            self.time.update_prop(text=self.start_time_str)
            
            self.stop_handler()
      
    def update_timer(self, *, color: str, name: str, hrs: str, mins: str, secs: str) -> None:
        self.set_time_vals(hrs, mins, secs)
        self.color_chip.configure(fg_color=color)
        self.label.configure(text=name)
        self.time.update_prop(text=self.start_time_str)
