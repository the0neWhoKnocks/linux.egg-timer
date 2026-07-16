# Monkey-patch for customtkinter. It was referencing an old module that can't be upgraded.
# This forces Python to map the old namespace to the correct new location before customtkinter attempts to look for it.
import collections
import collections.abc
collections.Sequence = collections.abc.Sequence

import argparse
import logging
import tkinter as tk
# from tkinter import ttk

import customtkinter
from customtkinter import (
  CTkButton,
  CTkFont,
  DrawEngine,
  FontManager,
)
# from ttkthemes import ThemedTk

# TODO may need to update widget paths to be relative (just a leading dot)?
# from .widgets import (
#     ColorPickerBtn,
#     EditableTimer,
#     TimerForm,
#     TimersList,
# )

# TODO I installed tkinter but it didn't update pyproject or uv.lock. I can't use
# `uv add` because it doesn't seem to allow for specifying the module install path.

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


# class EggTimer(ThemedTk):
class EggTimer(customtkinter.CTk):
    def __init__(self) -> None:
        # super().__init__(theme="plastik")
        super().__init__()
        # print("Available themes:", self.get_themes())
        # Themes: adapta, alt, aquativo, arc, black, blue, breeze (KDE), clam, classic, clearlooks, default, elegance, equilux, itft1, keramik, kroc, plastik, radiance, scidblue, scidgreen, scidgrey, scidmint, scidpink, scidpurple, scidsand, smog, ubuntu, winxpblue, yaru (Ubuntu)
        self.title("Egg Timer")
        # self.geometry("400x300")  # Set the window size
        # self.build_ui()
        
        print( tk.font.families() )
        
        # https://github.com/TomSchimansky/CustomTkinter/discussions/2156
        # customtkinter.FontManager.load_font("./eggtimer/assets/FantasqueSansMNerdFontMono-Regular.ttf")
        customtkinter.FontManager.load_font("/usr/share/fonts/truetype/FantasqueSansMNerdFontMono-Regular.ttf")
        self.defaultFont = customtkinter.CTkFont(family="FantasqueSansM Nerd Font Mono", size=18)
        self.configure(font=self.defaultFont)
        # DrawEngine.preferred_drawing_method = "polygon_shapes"
        # DrawEngine.preferred_drawing_method = "font_shapes"
        DrawEngine.preferred_drawing_method = "circle_shapes"
        button = CTkButton(self, text="My Button", font=("FantasqueSansM Nerd Font Mono", 24), command=lambda: print("click"))
        button.pack(padx=20, pady=20)
    
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
