import argparse
import logging
import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedTk

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


class EggTimer(ThemedTk):
    def __init__(self) -> None:
        super().__init__(theme="plastik")
        # print("Available themes:", self.get_themes())
        # Themes: adapta, alt, aquativo, arc, black, blue, breeze (KDE), clam, classic, clearlooks, default, elegance, equilux, itft1, keramik, kroc, plastik, radiance, scidblue, scidgreen, scidgrey, scidmint, scidpink, scidpurple, scidsand, smog, ubuntu, winxpblue, yaru (Ubuntu)
        self.title("Egg Timer")
        # self.geometry("400x300")  # Set the window size
        self.build_ui()
    
    @staticmethod
    def add_timer_to_list(cp: ColorPickerBtn, input: ttk.Entry, timer: EditableTimer, list: TimersList) -> None:  # noqa: A002
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
        create_form = TimerForm(self, btn_label="Add Timer", btn_handler=lambda: EggTimer.add_timer_to_list(
          cp=create_form.cp,
          input=create_form.input,
          timer=create_form.timer,
          list=timers_list,
        ))
        create_form.grid(row=0, column=0, sticky="NWE", padx=5, pady=5)
        
        self.rowconfigure(1, weight=1)
        timers_list = TimersList(self)
        timers_list.grid(row=1, column=0, sticky="NWSE", padx=5, pady=5)
        timers_list.configure(borderwidth=1, relief="sunken", height=200)


if __name__ == "__main__":
    app = EggTimer()
    app.mainloop()
