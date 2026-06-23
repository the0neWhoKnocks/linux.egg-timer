#!/usr/bin/env python3

import argparse
import json
import logging
import os
import pathlib
import subprocess  # noqa: S404
import threading
import time
from ast import literal_eval
from datetime import timedelta

import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
gi.require_version("PangoCairo", "1.0")
gi.require_version("XApp", "1.0")
from gi.repository import (  # noqa: E402
    Gdk,
    Gio,
    GLib,
    Gtk,
    Pango,
    XApp,
)

parser = argparse.ArgumentParser(
    prog="Egg Timer",
    description="An App to create and run multiple timers.",
)
parser.add_argument(
    "-l",
    "--loglevel",
    default="warning",
    help="Provide logging level. Example: --loglevel debug",
)
args = parser.parse_args()


logging.basicConfig(
    format="[%(name)s][%(levelname)s] %(message)s",
    level=args.loglevel.upper(),
)
log = logging.getLogger("eggtimer")


APPLICATION_ID = "com.nox.eggtimer"
DIR_NAME = os.path.dirname(__file__)
ICON__EXTERNAL = "eggtimer"
ICON__TRAY_ON = "eggtimer-on-symbolic"
ICON__TRAY_OFF = "eggtimer-off-symbolic"
MODIFIER__TIMER_DONE = "done"
MOUSE_BTN__LEFT = 1
MOUSE_BTN__RIGHT = 3
STYLE_SHEET_PATH = os.path.join(DIR_NAME, "app.css")
PATH__CONFIG_DIR = os.path.join(GLib.get_user_config_dir(), "eggtimer")
PATH__CONFIG_FILE = os.path.join(PATH__CONFIG_DIR, "config.json")


class Dialog(Gtk.Dialog):
    def __init__(self) -> None:
        super().__init__()
        self.set_icon_name(ICON__EXTERNAL)
        
        # add a styling class to the body
        content_area = self.get_content_area()
        self.body = Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
        content_area.pack_start(self.body, expand=True, fill=True, padding=0)
        style_ctx = self.body.get_style_context()
        style_ctx.add_class("eggtimer-dialog__body")
        
        # make the buttons stretch to fill available area.
        # NOTE: There's the `get_action_area` method which gets the same element,
        # but it also outputs a deprecation warning, so doing this for now.
        self.action_area.set_layout(Gtk.ButtonBoxStyle.EXPAND)

    def set_body(self, content: Gtk.Widget) -> None:
        self.body.pack_start(content, expand=True, fill=True, padding=0)


class EggTimer(Gtk.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id=APPLICATION_ID,
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self.config = {}
        self.completed_timers = {}
        self.playing_sound = False
        self.status_icon = None
        self.running_timers = {}
        self.running_timers_menu = None
        self.timers_menu_open = False
        self.timers_running = False
    
    @staticmethod
    def set_label_font(
        lbl: Gtk.Label,
        family: str | None = None,
        size: int | None = None,
        weight: int | None = None,
    ) -> None:
        fd = Pango.FontDescription.new()
        
        if family is not None:
            fd.set_family(family)
        
        if size is not None:
            fd.set_size(Pango.SCALE * size)
        
        if weight is not None:
            fd.set_weight(weight)
        
        font = Pango.AttrFontDesc.new(fd)
        attrs = Pango.AttrList.new()
        attrs.insert(font)
        lbl.set_attributes(attrs)
    
    @staticmethod
    def set_timer_text(timer: dict) -> None:
        remaining_secs = timer[0] - timer[1]
        timer[2]["display"]["label"].set_text(str(timedelta(seconds=remaining_secs)))

    def create_status_icon(self) -> None:
        self.status_icon = XApp.StatusIcon()
        self.status_icon.set_icon_name(ICON__TRAY_OFF)
        self.status_icon.set_visible(True)
        self.status_icon.connect("button-release-event", self.handle_tray_btn_release)

    def create_timer(self, _item: Gtk.MenuItem) -> None:
        self.open_timer_editor()

    def do_activate(self) -> None:
        Gtk.Application.do_activate(self)
        
        pathlib.Path(PATH__CONFIG_DIR).mkdir(parents=True, exist_ok=True)
        self.load_config()
        
        self.create_status_icon()
        
        provider = Gtk.CssProvider()
        provider.load_from_path(STYLE_SHEET_PATH)
        
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            600,
        )

        self.hold()  # prevents app from closing after start

    def handle_timer_start_click(self, _menu_item: Gtk.MenuItem, timer_dict: dict) -> None:
        total_secs = ((timer_dict["hours"] * 60) + timer_dict["mins"]) * 60
        timer_name = timer_dict["name"]
        self.running_timers[timer_name] = [total_secs, 0, {"color": timer_dict["color"]}]
        self.run_timers()
        log.info('Timer "%s" Started', timer_name)

    def handle_timer_stop_click(self, _menu_item: Gtk.MenuItem, timer_name: str) -> None:
        if timer_name in self.running_timers:
            del self.running_timers[timer_name]
        
        if timer_name in self.completed_timers:
            del self.completed_timers[timer_name]
        
        if self.timers_menu_open is True:
            self.running_timers_menu.deactivate()
        
        if len(self.running_timers) == 0:
            self.status_icon.set_icon_name(ICON__TRAY_OFF)

    def handle_timer_edit_click(self, _menu_item: Gtk.MenuItem, timer_dict: dict, ndx: int) -> None:
        self.open_timer_editor(timer_dict=timer_dict, timer_ndx=ndx)

    def handle_timer_delete_click(self, _menu_item: Gtk.MenuItem, timer_dict: dict, ndx: int) -> None:
        dialog = Dialog()
        dialog.set_title("Delete Timer")
        dialog.add_button("Cancel", 0)
        dialog.add_button("Delete", 1)
        
        timer_name = timer_dict["name"]
        text = Gtk.Label.new(f'Are you sure you want to delete the\ntimer for "{timer_name}"?')
        dialog.set_body(text)
        
        def handle_response(diag: Gtk.Dialog, code: int) -> None:
            if code == 1:
                self.handle_timer_stop_click(None, timer_name)
                del self.config["timers"][ndx]
                self.save_config()
            
            diag.close()
        
        dialog.connect("response", handle_response)
        dialog.show_all()

    def handle_timers_menu_close(self, _menu: Gtk.Menu) -> None:
        self.timers_menu_open = False

    def handle_tray_btn_release(  # noqa: C901, PLR0914, PLR0915
        self,
        _icon: XApp.StatusIcon,
        x: int,
        y: int,
        button: int,
        ev_time: int,
        panel_pos: int,
    ) -> None:
        icon_width = 20  # this is just a guess
        
        if button == MOUSE_BTN__LEFT:
            self.running_timers_menu = Gtk.Menu.new()
            self.running_timers_menu.set_reserve_toggle_size(False)
            
            running_count = len(self.running_timers)
            if running_count:
                for ndx, timer_name in enumerate(self.running_timers):
                    timer = self.running_timers[timer_name]
                    
                    item = Gtk.MenuItem.new()
                    ctx = item.get_style_context()
                    ctx.add_class("eggtimer-running-timer")
                    
                    if timer[0] == timer[1]:
                        ctx.add_class(MODIFIER__TIMER_DONE)
                    
                    grid = Gtk.Grid.new()
                    item.add(grid)
                    
                    if ndx > 0:
                        ctx.add_class("has--sep")
                    
                    css_item_name = f"timer_{ndx}"
                    color_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
                    css_provider = Gtk.CssProvider.new()
                    css = f".for--{css_item_name} {{ background-color: {timer[2]['color']}; }}"
                    css_provider.load_from_data(bytes(css.encode()))
                    ctx = color_box.get_style_context()
                    ctx.add_class("eggtimer-running-timer__color")
                    ctx.add_class(f"for--{css_item_name}")
                    ctx.add_provider(css_provider, 601)
                    grid.attach(color_box, 0, 0, 1, 2)
                    
                    name_label = Gtk.Label.new(timer_name)
                    ctx = name_label.get_style_context()
                    ctx.add_class("eggtimer-running-timer__name-label")
                    EggTimer.set_label_font(name_label, family="Ubuntu Mono", size=14, weight=Pango.Weight.BOLD)
                    grid.attach(name_label, 1, 0, 1, 1)
                    
                    time_label = Gtk.Label.new("00:00:00")
                    time_label.set_hexpand(True)
                    time_label.set_halign(Gtk.Align.CENTER)
                    ctx = time_label.get_style_context()
                    ctx.add_class("eggtimer-running-timer__time-label")
                    EggTimer.set_label_font(time_label, family="Ubuntu Mono", size=24)
                    grid.attach(time_label, 1, 0 + 1, 1, 1)
                    timer[2]["display"] = {"label": time_label, "menu_item": item}
                    EggTimer.set_timer_text(timer)
                    
                    item.connect("activate", self.handle_timer_stop_click, timer_name)
                    item.set_tooltip_text("Click to Stop Timer")
                    
                    self.running_timers_menu.append(item)
                
                self.running_timers_menu.show_all()
                self.running_timers_menu.connect("deactivate", self.handle_timers_menu_close)
                
                self.status_icon.popup_menu(self.running_timers_menu, x, y, button, ev_time, panel_pos)
                menu_offset = 0
                if panel_pos in {Gtk.PositionType.BOTTOM, Gtk.PositionType.TOP}:
                    # can't center a menu without first displaying it
                    menu_width = self.running_timers_menu.get_allocated_width()
                    menu_offset = (menu_width / 2) - icon_width
                    self.status_icon.popup_menu(self.running_timers_menu, x - menu_offset, y, button, ev_time, panel_pos)
                
                self.timers_menu_open = True
        
        elif button == MOUSE_BTN__RIGHT:
            menu = Gtk.Menu.new()
            menu.set_reserve_toggle_size(False)
            
            if "timers" in self.config:
                for ndx, timer_dict in enumerate(self.config["timers"]):
                    timer_name = timer_dict["name"]
                    
                    timer_item = Gtk.MenuItem.new_with_label(
                        f"{str(timer_dict['hours']).rjust(2, '0')}:{str(timer_dict['mins']).rjust(2, '0')} | {timer_name}",
                    )
                    sub_menu = Gtk.Menu.new()
                    
                    if timer_name in self.running_timers or timer_name in self.completed_timers:
                        stop_item = Gtk.MenuItem.new_with_label("Stop")
                        stop_item.connect("activate", self.handle_timer_stop_click, timer_name)
                        sub_menu.append(stop_item)
                    else:
                        start_item = Gtk.MenuItem.new_with_label("Start")
                        start_item.connect("activate", self.handle_timer_start_click, timer_dict)
                        sub_menu.append(start_item)
                    
                    edit_item = Gtk.MenuItem.new_with_label("Edit")
                    edit_item.connect("activate", self.handle_timer_edit_click, timer_dict, ndx)
                    sub_menu.append(edit_item)
                    
                    delete_item = Gtk.MenuItem.new_with_label("Delete")
                    delete_item.connect("activate", self.handle_timer_delete_click, timer_dict, ndx)
                    sub_menu.append(delete_item)
                    
                    timer_item.set_submenu(sub_menu)
                    menu.append(timer_item)
                
                menu.append(Gtk.SeparatorMenuItem.new())
            
            item = Gtk.MenuItem.new_with_label("Create Timer")
            item.connect("activate", self.create_timer)
            menu.append(item)
            
            menu.append(Gtk.SeparatorMenuItem.new())
            
            item = Gtk.MenuItem.new_with_label("Quit")
            item.connect("activate", self.quit_app)
            menu.append(item)
            
            menu.show_all()
            
            self.status_icon.popup_menu(menu, x, y, button, ev_time, panel_pos)
            menu_offset = 0
            if panel_pos in {Gtk.PositionType.BOTTOM, Gtk.PositionType.TOP}:
                # can't center a menu without first displaying it
                menu_width = menu.get_allocated_width()
                menu_offset = (menu_width / 2) - icon_width
                self.status_icon.popup_menu(menu, x - menu_offset, y, button, ev_time, panel_pos)

    def load_config(self) -> None:
        conf = pathlib.Path(PATH__CONFIG_FILE)
        
        if conf.is_file():
            with open(PATH__CONFIG_FILE, encoding="utf-8") as file:
                self.config = json.load(file)
        else:
            self.save_config()

    def notify_user(self, timer_name: str) -> None:
        timestamp = time.strftime("%I:%M", time.localtime())
        msg = f'Timer \\"{timer_name}\\" completed at {timestamp}'
        subprocess.run(  # noqa: S603
            ["/usr/bin/notify-send", "-t", "3000", "--hint=int:transient:1", '--app-name="Egg Timer"', f"--icon={ICON__EXTERNAL}", f'"{msg}"'],
            check=True,
        )
        
        self.completed_timers[timer_name] = True
        
        if not self.playing_sound:
            self.play_sound()

    def open_timer_editor(self, timer_dict: dict | None = None, timer_ndx: int | None = None) -> None:
        dialog = Dialog()
        title = "Create a Timer" if timer_dict is None else "Edit Timer"
        dialog.set_title(title)
        
        grid = Gtk.Grid.new()
        
        name_label = Gtk.Label.new("Timer Name:  ")
        name_input = Gtk.Entry.new()
        if timer_dict is not None:
            name_input.set_text(timer_dict["name"])
        grid.attach(name_label, 0, 0, 1, 1)
        grid.attach(name_input, 1, 0, 1, 1)
        
        hrs_label = Gtk.Label.new("Hours:  ")
        hrs_label.set_xalign(1)
        hrs_input = Gtk.SpinButton.new_with_range(0, 23, 1)
        if timer_dict is not None:
            hrs_input.set_value(timer_dict["hours"])
        grid.attach(hrs_label, 0, 1, 1, 1)
        grid.attach(hrs_input, 1, 1, 1, 1)
        
        mins_label = Gtk.Label.new("Minutes:  ")
        mins_label.set_xalign(1)
        mins_input = Gtk.SpinButton.new_with_range(0, 59, 1)
        if timer_dict is not None:
            mins_input.set_value(timer_dict["mins"])
        grid.attach(mins_label, 0, 2, 1, 1)
        grid.attach(mins_input, 1, 2, 1, 1)
        
        clr_label = Gtk.Label.new("Color:  ")
        clr_label.set_xalign(1)
        default_color = Gdk.RGBA()
        default_color.parse("#00C487")
        if timer_dict is not None:
            default_color.parse(timer_dict["color"])
        clr_btn = Gtk.ColorButton.new_with_rgba(default_color)
        grid.attach(clr_label, 0, 3, 1, 1)
        grid.attach(clr_btn, 1, 3, 1, 1)
        
        dialog.set_body(grid)
        
        dialog.add_button("Cancel", 0)
        submit_btn_label = "Create" if timer_dict is None else "Update"
        dialog.add_button(submit_btn_label, 1)
        
        def handle_create_dialog_response(diag: Gtk.Dialog, code: int) -> None:
            if code == 1:
                self.save_timer(
                    name_input.get_text(),
                    hrs_input.get_value(),
                    mins_input.get_value(),
                    clr_btn.get_rgba(),
                    timer_ndx=timer_ndx,
                )
            
            diag.close()
        
        dialog.connect("response", handle_create_dialog_response)
        dialog.show_all()

    def play_sound(self) -> None:
        self.playing_sound = True
        
        def play() -> None:
            while len(self.completed_timers):
                subprocess.run(  # noqa: S603
                    ["/usr/bin/aplay", "--quiet", "--nonblock", f"{DIR_NAME}/complete.wav"],
                    check=True,
                )
                time.sleep(1)
            
            self.playing_sound = False
            log.info("Sound stopped")
        
        thread = threading.Thread(daemon=True, name="Alarm", target=play)
        thread.start()

    def quit_app(self, _item: Gtk.MenuItem) -> None:
        # TODO: kill any running timers
        # for timer in self.timers:
        #   timer.destroy()
        self.quit()

    def run_timers(self) -> None:  # noqa: C901
        def tick() -> None:
            time.sleep(1)
            
            completed_timers = []
            
            for timer_name, timer in self.running_timers.items():
                if timer[1] < timer[0]:  # timer not done
                    timer[1] += 1
                    
                    if self.timers_menu_open is True and "display" in timer[2]:
                        EggTimer.set_timer_text(timer)
                    
                    if timer[0] == timer[1]:
                        log.info('Timer "%s" has finished', timer_name)
                        completed_timers.append(timer_name)
                    else:
                        log.info("%s: %s | %s", timer_name, timer[0], timer[1])
            
            # since dict's can't have items removed within a for loop
            if len(completed_timers) > 0:
                for timer_name in completed_timers:
                    if "display" in self.running_timers[timer_name][2]:
                        menu_item = self.running_timers[timer_name][2]["display"]["menu_item"]
                        ctx = menu_item.get_style_context()
                        ctx.add_class(MODIFIER__TIMER_DONE)
                    
                    self.notify_user(timer_name)

        def check_timers() -> None:
            while self.timers_running:
                if len(self.completed_timers) < len(self.running_timers):
                    tick()
                else:
                    log.info("All timers have finished")
                    self.timers_running = False
        
        if self.timers_running is not True:
            self.timers_running = True
            self.status_icon.set_icon_name(ICON__TRAY_ON)
            thread = threading.Thread(daemon=True, name="Timer", target=check_timers)
            thread.start()

    def save_config(self) -> None:
        with open(PATH__CONFIG_FILE, mode="w", encoding="utf-8") as file:
            json.dump(self.config, file, sort_keys=True, indent=2)

    def save_timer(self, name: str, hours: int, mins: int, color: Gdk.RGBA, timer_ndx: int | None = None) -> None:
        if "timers" not in self.config:
            self.config["timers"] = []
        
        color_tuple = literal_eval(color.to_string().replace("rgb", ""))
        color_hex = "#{:02x}{:02x}{:02x}".format(*color_tuple)
        
        timer_dict = {
            "color": color_hex,
            "hours": int(hours),
            "mins": int(mins),
            "name": name,
        }
        
        if timer_ndx is None:
            self.config["timers"].append(timer_dict)
        else:
            self.config["timers"][timer_ndx] = timer_dict
        
        self.save_config()


if __name__ == "__main__":
    egg_timer = EggTimer()
    egg_timer.run()
