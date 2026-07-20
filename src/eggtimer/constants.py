from pathlib import Path

from customtkinter import FontManager

MODULE_DIR = Path(__file__).resolve().parent

LOGGER_NAMESPACE = "eggtimer"
MOUSE_BTN__LEFT = "<Button-1>"  # https://stackoverflow.com/a/32289245/5156659
MOUSE_SCROLL__DOWN = 5
MOUSE_SCROLL__UP = 4

FontManager.load_font(f"{MODULE_DIR}/assets/FantasqueSansMNerdFontMono-Regular.ttf")
FONT__MONO__FAMILY = "FantasqueSansM Nerd Font Mono"
FONT__MONO__SIZE = 18
