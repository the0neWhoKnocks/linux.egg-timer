from pathlib import Path

from customtkinter import FontManager

APP_DIR = Path(__file__).resolve().parent

APP_NAME = "eggtimer"
APP_NAME_FORMATTED = "Egg Timer"
BTN_WIDTH = 30
LOGGER_NAMESPACE = APP_NAME
MOUSE_BTN__LEFT = "<Button-1>"  # https://stackoverflow.com/a/32289245/5156659
MOUSE_SCROLL__DOWN = 5
MOUSE_SCROLL__UP = 4

# Download font from: https://github.com/FortAwesome/Font-Awesome/releases (Currently: 7.3.1) (Choose the `desktop` version)
# Look for icon names: https://fontawesome.com/search?q=edit&ic=free-collection
# - Make sure the version drop-down is set to the version of the font you downloaded.
# - Click an icon > Click the' Copy Unicode' and 'Copy Glyph' buttons. Some of the Unicode characters may not be 4 characters - in that case, pad with leading zeros.
ICON__ADD = "\u002b"     # + | plus
ICON__CANCEL = "\uf00d"  #  | xmark
ICON__DELETE = "\uf1f8"  #  | trash
ICON__EDIT = "\uf044"    #  | pen-to-square
ICON__PLAY = "\uf04b"    #  | play
ICON__SAVE = "\uf0c7"    #  | save
ICON__STOP = "\uf04d"    #  | stop

FontManager.load_font(str(APP_DIR / "assets" / "fonts" / "FantasqueSansMNerdFontMono-Regular.ttf"))
FONT__DEFAULT__FAMILY = "FantasqueSansM Nerd Font Mono"
FONT__DEFAULT__SIZE = 22
FontManager.load_font(str(APP_DIR / "assets" / "fonts" / "Font-Awesome-7-Free-Solid-900.otf"))
FONT__ICONS__FAMILY = "Font Awesome 7 Free"
FONT__ICONS__SIZE = 14
FontManager.load_font(str(APP_DIR / "assets" / "fonts" / "DigitalDisplayRegular-ODEO.ttf"))
FONT__TIMER__FAMILY = "Digital Display"
FONT__TIMER__SIZE = 22
