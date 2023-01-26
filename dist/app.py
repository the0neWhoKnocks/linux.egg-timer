#!/usr/bin/python3

import json
import os
import pathlib
import sys

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('XApp', '1.0')
from gi.repository import Gdk, Gio, GLib, Gtk, XApp

APPLICATION_ID = 'com.nox.eggtimer'
DIR_NAME = os.path.dirname(__file__)
STYLE_SHEET_PATH = os.path.join(DIR_NAME, 'app.css')
PATH__CONFIG_DIR = os.path.join(GLib.get_user_config_dir(), 'eggtimer')
PATH__CONFIG_FILE = os.path.join(PATH__CONFIG_DIR, 'config.json');

class Application(Gtk.Application):

  def __init__(self):
    super(Application, self).__init__(
      application_id=APPLICATION_ID,
      flags=Gio.ApplicationFlags.FLAGS_NONE,
    )
    self.statusIcon = None
  
  
  def loadConfig(self):
    conf = pathlib.Path(PATH__CONFIG_FILE)
    
    if conf.is_file():
      with open(PATH__CONFIG_FILE, 'r') as file:
        self.config = json.load(file)
    else:
      self.config = {}
      self.saveConfig()
  
  
  def saveConfig(self):
    with open(PATH__CONFIG_FILE, 'w') as file:
      json.dump(self.config, file, sort_keys=True, indent=2)
  
  
  def do_activate(self):
    Gtk.Application.do_activate(self)
    
    pathlib.Path(PATH__CONFIG_DIR).mkdir(parents=True, exist_ok=True) # `mkdir -p` equivelant
    self.loadConfig()
    
    self.createStatusIcon()
    
    provider = Gtk.CssProvider()
    provider.load_from_path(STYLE_SHEET_PATH)
    
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, 600)
    
    self.hold() # prevents app from closing after start
  
  
  def createStatusIcon(self):
    self.statusIcon = XApp.StatusIcon()
    self.statusIcon.set_name('egg-timer')
    self.statusIcon.set_icon_name('document-open-recent')
    self.statusIcon.set_tooltip_text('%s\n<i>%s</i>\n<i>%s</i>' % (
      'Egg Timer',
      'Left-click to view timers',
      'Right-click to open menu'
    ))
    self.statusIcon.set_visible(True)
    self.statusIcon.connect('button-release-event', self.handleTrayBtnRelease)
  
  
  def handleTrayBtnRelease(self, icon, x, y, button, time, panel_position):
    match button:
      case 1: # left-click
        print('open timers')
        
      case 3: # right-click
        menu = Gtk.Menu()
        sep = Gtk.SeparatorMenuItem()
        
        # TODO: if there are saved timers, add them at the top of the list
        # iterate each item
        #  item = Gtk.MenuItem(label='Start Timer: <NAME>')
        #  item.connect('activate', self.handleTimerStartClick)
        #  menu.append(item)
        # add a separator
        # menu.append(sep)
        
        item = Gtk.MenuItem(label='Create Timer')
        item.connect('activate', self.createTimer)
        menu.append(item)
        
        menu.append(sep)
        
        item = Gtk.MenuItem(label='Quit')
        item.connect('activate', self.quitApp)
        menu.append(item)
        
        menu.show_all()
        
        # haven't found a way to get the menu's width to properly center it, so
        # just hardcoding for now.
        menuOffset = 0
        if panel_position == Gtk.PositionType.BOTTOM or panel_position == Gtk.PositionType.TOP:
          menuOffset = 30
        
        self.statusIcon.popup_menu(menu, x-menuOffset, y, button, time, panel_position)
  
  
  def saveTimer(self, name, hours, mins, color):
    if 'timers' not in self.config:
      self.config['timers'] = []
    
    colorTuple=eval(color.to_string().replace('rgb', ''))
    colorHex = '#{:02x}{:02x}{:02x}'.format(*colorTuple)
    
    self.config['timers'].append({
      'color': colorHex,
      'hours': int(hours),
      'mins': int(mins),
      'name': name
    })
    
    self.saveConfig()
  
  
  def createTimer(self, *args):
    dialog = Gtk.Dialog()
    dialog.set_icon_name('document-open-recent')
    dialog.set_title('Create a Timer')
    
    grid = Gtk.Grid.new()
    grid.set_name('createTimerDialogContent')
    
    nameLabel = Gtk.Label.new('Timer Name:  ')
    nameInput = Gtk.Entry.new()
    grid.attach(nameLabel, 0, 0, 1, 1)
    grid.attach(nameInput, 1, 0, 1, 1)
    
    hrsLabel = Gtk.Label.new('Hours:  ')
    hrsLabel.set_xalign(1)
    hrsInput = Gtk.SpinButton.new_with_range(0, 23, 1)
    grid.attach(hrsLabel, 0, 1, 1, 1)
    grid.attach(hrsInput, 1, 1, 1, 1)
    
    minsLabel = Gtk.Label.new('Minutes:  ')
    minsLabel.set_xalign(1)
    minsInput = Gtk.SpinButton.new_with_range(0, 59, 1)
    grid.attach(minsLabel, 0, 2, 1, 1)
    grid.attach(minsInput, 1, 2, 1, 1)
    
    clrLabel = Gtk.Label.new('Color:  ')
    clrLabel.set_xalign(1)
    defaultColor = Gdk.RGBA()
    defaultColor.parse('#00C487')
    clrBtn = Gtk.ColorButton.new_with_rgba(defaultColor)
    grid.attach(clrLabel, 0, 3, 1, 1)
    grid.attach(clrBtn, 1, 3, 1, 1)
    
    dialogBody = dialog.get_content_area()
    dialogBody.pack_start(grid, True, True, 0)
    
    dialog.get_action_area().set_layout(Gtk.ButtonBoxStyle.EXPAND)
    
    dialog.add_button('Cancel', 0)
    dialog.add_button('Create', 1)
    
    def handleCreateDialogResponse(_dialog, code):
      match code:
        case 1:
          self.saveTimer(
            nameInput.get_text(),
            hrsInput.get_value(),
            minsInput.get_value(),
            clrBtn.get_rgba()
          )
      _dialog.close()
    
    dialog.connect('response', handleCreateDialogResponse)
    
    dialog.show_all()
  
  
  def quitApp(self, *args):
    # TODO: kill any running timers
    # for timer in self.timers:
    #   timer.destroy()
    self.quit()


if __name__ == '__main__':
  eggTimer = Application()
  eggTimer.run(sys.argv)
