from pathlib import Path

from customtkinter import FontManager

APP_DIR = Path(__file__).resolve().parent

APP_NAME = "eggtimer"
APP_NAME_FORMATTED = "Egg Timer"
LOGGER_NAMESPACE = APP_NAME
MOUSE_BTN__LEFT = "<Button-1>"  # https://stackoverflow.com/a/32289245/5156659
MOUSE_SCROLL__DOWN = 5
MOUSE_SCROLL__UP = 4

FontManager.load_font(str(APP_DIR / "assets" / "FantasqueSansMNerdFontMono-Regular.ttf"))
FONT__MONO__FAMILY = "FantasqueSansM Nerd Font Mono"
FONT__MONO__SIZE = 18
