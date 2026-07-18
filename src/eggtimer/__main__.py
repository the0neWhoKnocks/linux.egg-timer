import argparse
import logging
import tkinter as tk

from customtkinter import (
    CTk,
    CTkEntry,
    DrawEngine,
    ThemeManager,
    set_default_color_theme,
)

from eggtimer.constants import FONT__MONO__FAMILY, FONT__MONO__SIZE
from eggtimer.widgets import (
    ColorPickerBtn,
    EditableTimer,
    TimerForm,
    TimersList,
)

parser = argparse.ArgumentParser(
    prog="Egg Timer",
    description="An App to create and run multiple timers.",
)
parser.add_argument(
    "-l",
    "--loglevel",
    default="warning",
    help="Provide logging level. Example: --loglevel=debug",
)
args = parser.parse_args()

# Set up base logger that all files within module will inherit from
logging.basicConfig(
    format="[%(name)s][%(levelname)s] %(message)s",
    level=args.loglevel.upper(),
)


class EggTimer(CTk):
    def __init__(self) -> None:
        super().__init__()
        
        set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "gold", "green", "dark-blue" | https://github.com/TomSchimansky/CustomTkinter/tree/master/customtkinter/assets/themes
        DrawEngine.preferred_drawing_method = "font_shapes"  # "circle_shapes", "font_shapes", "polygon_shapes"
        ThemeManager.theme["CTkFont"]["family"] = FONT__MONO__FAMILY  # set a global font for theme | https://github.com/TomSchimansky/CustomTkinter/blob/master/customtkinter/assets/themes/dark-blue.json
        ThemeManager.theme["CTkFont"]["size"] = FONT__MONO__SIZE
        # print( tk.font.families() )
        
        self.title("Egg Timer")
        self.geometry("400x300")  # Set the window size
        
        self.build_ui()
    
    @staticmethod
    def add_timer_to_list(cp: ColorPickerBtn, input: CTkEntry, timer: EditableTimer, list: TimersList) -> None:  # noqa: A002
        name = input.get()
        if name:
            list.add_timer(
              color=cp.color,
              name=name,
              hrs=timer.val_hours.get(),
              mins=timer.val_mins.get(),
              secs=timer.val_secs.get(),
            )
            input.delete(0, tk.END)
            timer.reset_vals()
    
    def build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        timers_list = TimersList(self)
        create_form = TimerForm(self, btn_label="Add Timer", btn_handler=lambda: EggTimer.add_timer_to_list(
          cp=create_form.cp,
          input=create_form.input,
          timer=create_form.timer,
          list=timers_list,
        ))
        create_form.grid(row=0, column=0, sticky="NWE", padx=5, pady=5)
        
        self.rowconfigure(1, weight=1)
        timers_list.grid(row=1, column=0, sticky="NWSE", padx=5, pady=5)
        timers_list.configure(border_width=1, height=200)


if __name__ == "__main__":
    app = EggTimer()
    app.mainloop()
