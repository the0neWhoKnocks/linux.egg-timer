from time import time
from typing import TYPE_CHECKING

from customtkinter import (
    CTk,
    CTkButton,
    CTkFrame,
    CTkImage,
    CTkLabel,
    CTkScrollableFrame,
)
from PIL import Image

from eggtimer.constants import APP_DIR

if TYPE_CHECKING:
    from collections.abc import Callable
    from tkinter import Event

X_SPACING = 5
colors = {
  "play": "green",
  "stop": "red",
}


class Timer(CTkFrame):
    @staticmethod
    def scale_img(sheet: Image.Image, x_ndx: int) -> CTkImage:
        def icon_coords(x_ndx: int, y_ndx: int) -> tuple[int, int, int, int]:
            icon_size = 50
            left = x_ndx * icon_size
            top = y_ndx * icon_size
            right = (x_ndx * icon_size) + icon_size
            bottom = (y_ndx * icon_size) + icon_size
            
            return left, top, right, bottom
        
        return CTkImage(
          light_image=sheet.crop(icon_coords(x_ndx, y_ndx=0)),
          dark_image=sheet.crop(icon_coords(x_ndx, y_ndx=1)),
          size=(25, 25),
        )
    
    def __init__(  # noqa: PLR0913
        self,
        parent: CTkScrollableFrame,
        *,
        root: CTk,
        color: str,
        name: str,
        hours: str,
        minutes: str,
        seconds: str,
        delete_handler: Callable,
        done_handler: Callable,
        stop_handler: Callable,
    ) -> None:
        super().__init__(parent, border_width=1)
        
        self.start_time_str = f"{hours}:{minutes}:{seconds}"
        self.total_secs = float((int(hours) * 3600) + (int(minutes) * 60) + int(seconds))
        
        self.color = color
        self.completed = False
        self.delete_handler = delete_handler
        self.done_handler = done_handler
        self.name = name
        self.render_loop = None
        self.root = root
        self.running = False
        self.stop_handler = stop_handler
        
        self.build_ui()
    
    def build_ui(self) -> None:
        icons_sprite_sheet = Image.open(f"{APP_DIR}/assets/icons/app/icons.png")
        self.icons = {
          "play": self.scale_img(x_ndx=0, sheet=icons_sprite_sheet),
          "stop": self.scale_img(x_ndx=1, sheet=icons_sprite_sheet),
        }
        
        self.pack(fill="x", pady=2, padx=X_SPACING)
        self.color_chip = CTkLabel(self,
          corner_radius=5,
          fg_color=self.color,
          text="",
          width=20,
        )
        self.color_chip.pack(side="left", padx=2, pady=2)
        self.label = CTkLabel(self, text=self.name)
        self.label.pack(side="left", padx=X_SPACING)
        # TODO: add Edit button
        self.delete_btn = CTkButton(self,
          text="Delete",
          command=self.delete_timer,
        )
        self.delete_btn.pack(side="right", padx=X_SPACING)
        self.timer_toggle = CTkButton(self,
          text="",
          image=self.icons["play"],
          fg_color=colors["play"],
          border_color="#000000",
          width=30,
          command=self.toggle_timer_btn,
        )
        self.timer_toggle.pack(side="right", padx=X_SPACING, pady=2)
        self.time = CTkLabel(self, text=self.start_time_str)
        self.time.pack(side="right", padx=X_SPACING)
    
    def delete_timer(self, _ev: Event | None = None) -> None:
        if self.render_loop is not None:
            self.root.after_cancel(self.render_loop)
        
        self.delete_handler()
    
    def render(self) -> None:
        if not self.running and not self.completed:
            return
        
        current_time = time()
        remaining_time = self.end_time - current_time
        
        seconds = int(remaining_time)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        self.time.configure(text=f"{hours:02}:{minutes:02}:{seconds:02}")
        
        if remaining_time > 0:
            self.render_loop = self.root.after(100, self.render)  # check in milliseconds so the UI responds quickly to clicks
        else:
            self.completed = True
            self.done_handler()
    
    def toggle_timer_btn(self, _ev: Event | None = None) -> None:
        self.running = not self.running
        
        if self.running:
            self.timer_toggle.configure(
              fg_color=colors["stop"],
              image=self.icons["stop"],
            )
            
            self.start_time = time()
            self.end_time = self.start_time + self.total_secs
            
            self.render()
        else:
            self.timer_toggle.configure(
              fg_color=colors["play"],
              image=self.icons["play"],
            )
            
            self.time.configure(text=self.start_time_str)
            
            self.stop_handler()
