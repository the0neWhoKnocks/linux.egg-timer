import argparse
import logging

from customtkinter import (
    CTk,
    DrawEngine,
    ThemeManager,
    set_default_color_theme,
)

from eggtimer.constants import (
    APP_NAME,
    APP_NAME_FORMATTED,
    FONT__MONO__FAMILY,
    FONT__MONO__SIZE,
)
from eggtimer.util import Config
from eggtimer.widgets import (
    TimerForm,
    TimersList,
)

parser = argparse.ArgumentParser(
    prog=APP_NAME_FORMATTED,
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
        
        self.app_config = Config(name=APP_NAME)
        
        self.title(APP_NAME_FORMATTED)
        self.geometry("600x300")  # Set the window size
        
        self.build_ui()
    
    def add_timer_to_list(self) -> None:
        name = self.create_form.get_name()
        hrs, mins, secs = self.create_form.get_time()
        
        if name and f"{hrs}{mins}{secs}" != "000000":
            self.timers_list.add_timer(
              color=self.create_form.get_color(),
              name=name,
              hrs=hrs, mins=mins, secs=secs,
            )
            self.create_form.reset()
    
    def build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=0)
        self.timers_list = TimersList(self)
        self.create_form = TimerForm(self, btn_label="Add Timer", btn_handler=self.add_timer_to_list)
        self.create_form.grid(row=0, column=0, sticky="NWE", padx=5, pady=5)
        
        self.rowconfigure(1, weight=1)
        self.timers_list.grid(row=1, column=0, sticky="NWSE", padx=5, pady=5)
        self.timers_list.configure(border_width=1, height=200)


if __name__ == "__main__":
    app = EggTimer()
    app.mainloop()
