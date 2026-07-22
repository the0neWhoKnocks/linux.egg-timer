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
    FONT__DEFAULT__FAMILY,
    FONT__DEFAULT__SIZE,
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
        self.title(APP_NAME_FORMATTED)
        # self.geometry("600x300")  # Set the window size, or eclude this and let it auto-size based on content.
        
        set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "gold", "green", "dark-blue" | https://github.com/TomSchimansky/CustomTkinter/tree/master/customtkinter/assets/themes
        DrawEngine.preferred_drawing_method = "font_shapes"  # "circle_shapes", "font_shapes", "polygon_shapes"
        ThemeManager.theme["CTkFont"]["family"] = FONT__DEFAULT__FAMILY  # set a global font for theme | https://github.com/TomSchimansky/CustomTkinter/blob/master/customtkinter/assets/themes/dark-blue.json
        ThemeManager.theme["CTkFont"]["size"] = FONT__DEFAULT__SIZE
        # print( tkinter.font.families() )  # NOTE: Uncomment to view the names of loaded fonts
        
        self.app_config = Config(name=APP_NAME)
        
        self.build_ui()
    
    def add_timer_to_list(self) -> None:
        color, name, hrs, mins, secs = self.timer_form.get_form_data()
        args = {
          "color": color,
          "name": name,
          "hrs": hrs,
          "mins": mins,
          "secs": secs,
        }
        
        if self.timer_filled_out(name, hrs, mins, secs):
            uid = self.timers_list.add_timer(**args)
            self.save_timer(**args, uid=uid)
            self.timer_form.reset()
    
    def build_ui(self) -> None:
        self.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=0)
        self.timers_list = TimersList(self)
        self.timer_form = TimerForm(self,
          add_handler=self.add_timer_to_list,
          save_handler=self.update_timer,
        )
        self.timer_form.grid(row=0, column=0, sticky="NWE", padx=5, pady=5)
        
        self.rowconfigure(1, weight=1)
        self.timers_list.grid(row=1, column=0, sticky="NWSE", padx=5, pady=5)
        self.timers_list.configure(border_width=1, height=200)
    
    def save_timer(self, *, color: str, hrs: str, mins: str, name: str, secs: str, uid: str) -> None:  # noqa: PLR0913
        if "timers" not in self.app_config.data:
            self.app_config.data["timers"] = {}
        
        self.app_config.data["timers"][uid] = {
            "color": color,
            "hours": hrs,
            "mins": mins,
            "name": name,
            "secs": secs,
        }
        self.app_config.save()
    
    @staticmethod
    def timer_filled_out(name: str, hrs: str, mins: str, secs: str) -> bool:
        return bool(name and f"{hrs}{mins}{secs}" != "000000")
    
    def update_timer(self, uid: str) -> None:
        color, name, hrs, mins, secs = self.timer_form.get_form_data()
        args = {
          "color": color,
          "name": name,
          "hrs": hrs,
          "mins": mins,
          "secs": secs,
        }
        
        if self.timer_filled_out(name, hrs, mins, secs):
            self.save_timer(**args, uid=uid)
            self.timers_list.timers[uid].update_timer(**args)
            self.timer_form.reset()


if __name__ == "__main__":
    app = EggTimer()
    app.mainloop()
