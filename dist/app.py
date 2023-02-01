#!/usr/bin/env python3

from datetime import timedelta
import argparse
import json
import logging
import os
import pathlib
import subprocess
import threading
import time

import gi
gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')
gi.require_version('XApp', '1.0')
from gi.repository import Gdk, Gio, GLib, Gtk, Pango, XApp


parser = argparse.ArgumentParser(
  prog = 'Egg Timer',
  description = 'An App to create and run multiple timers.',
)
parser.add_argument(
  '-l',
  '--loglevel',
  default='warning',
  help='Provide logging level. Example: --loglevel debug'
)
args = parser.parse_args()


logging.basicConfig(
  format = '[%(name)s][%(levelname)s] %(message)s',
  level = args.loglevel.upper()
)
log = logging.getLogger('eggtimer')


APPLICATION_ID = 'com.nox.eggtimer'
DIR_NAME = os.path.dirname(__file__)
ICON__EXTERNAL = 'eggtimer-on-symbolic'
ICON__TRAY_ON = 'eggtimer-on-symbolic'
ICON__TRAY_OFF = 'eggtimer-off-symbolic'
MODIFIER__TIMER_DONE = 'done'
STYLE_SHEET_PATH = os.path.join(DIR_NAME, 'app.css')
PATH__CONFIG_DIR = os.path.join(GLib.get_user_config_dir(), 'eggtimer')
PATH__CONFIG_FILE = os.path.join(PATH__CONFIG_DIR, 'config.json');


class Dialog(Gtk.Dialog):
  def __init__(self):
    super(Dialog, self).__init__()
    self.set_icon_name(ICON__EXTERNAL)
    
    # add a styling class to the body
    contentArea = self.get_content_area()
    self.body = Gtk.Box.new(Gtk.Orientation.VERTICAL, 10)
    contentArea.pack_start(self.body, True, True, 0)
    styleCtx = self.body.get_style_context()
    styleCtx.add_class('eggtimer-dialog__body')
    
    # make the buttons stretch to fill available area.
    # NOTE: There's the `get_action_area` method which gets the same element,
    # but it also outputs a deprecation warning, so doing this for now.
    self.action_area.set_layout(Gtk.ButtonBoxStyle.EXPAND)
  
  
  def setBody(self, content):
    self.body.pack_start(content, True, True, 0)


class Application(Gtk.Application):

  def __init__(self):
    super(Application, self).__init__(
      application_id=APPLICATION_ID,
      flags=Gio.ApplicationFlags.FLAGS_NONE,
    )
    self.completedTimers = {}
    self.playingSound = False
    self.statusIcon = None
    self.runningTimers = {}
    self.runningTimersMenu = None
    self.timersMenuOpen = False
    self.timersRunning = False
  
  
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
    self.statusIcon.set_icon_name(ICON__TRAY_OFF)
    self.statusIcon.set_visible(True)
    self.statusIcon.connect('button-release-event', self.handleTrayBtnRelease)
  
  
  def playSound(self):
    self.playingSound = True
    
    def play():
      while len(self.completedTimers):
        subprocess.run(f"aplay --quiet --nonblock {DIR_NAME}/complete.wav", shell=True, check=True)
        time.sleep(1)
      
      self.playingSound = False
      log.info('Sound stopped')
    
    thread = threading.Thread(daemon=True, target=play)
    thread.start()
  
  
  def notifyUser(self, timerName):
    timestamp = time.strftime("%I:%M", time.localtime())
    msg = f"Timer \\\"{timerName}\\\" completed at {timestamp}"
    subprocess.run(f"notify-send -t 3000 --hint=\"int:transient:1\" --app-name=\"Egg Timer\" --icon={ICON__EXTERNAL} \"{msg}\"", shell=True, check=True)
    
    self.completedTimers[timerName] = True
    
    if not self.playingSound: self.playSound()
  
  
  def runTimers(self):
    def tick():
      time.sleep(1)
      
      completedTimers = []
      
      for timerName in self.runningTimers:
        timer = self.runningTimers[timerName]
        
        if timer[1] < timer[0]: # timer not done
          timer[1] += 1
          
          if self.timersMenuOpen == True and 'display' in timer[2]:
            self.setTimerText(timer)
          
          if timer[0] == timer[1]:
            log.info(f"Timer \"{timerName}\" has finished")
            completedTimers.append(timerName)
          else:
            log.info(f"{timerName}: {timer[0]} | {timer[1]}")
      
      # since dict's can't have items removed within a for loop
      if len(completedTimers):
        for timerName in completedTimers:
          menuItem = self.runningTimers[timerName][2]['display']['menuItem']
          ctx = menuItem.get_style_context()
          ctx.add_class(MODIFIER__TIMER_DONE)
          self.notifyUser(timerName)
      
      if len(self.completedTimers) < len(self.runningTimers):
        tick()
      else:
        log.info('All timers have finished')
        self.timersRunning = False
    
    
    if self.timersRunning != True:
      self.timersRunning = True
      self.statusIcon.set_icon_name(ICON__TRAY_ON)
      thread = threading.Thread(daemon=True, target=tick)
      thread.start()
      log.info('Timers Started')
  
  
  def handleTimerStartClick(self, menuItem, timerDict):
    totalSecs = ((timerDict['hours'] * 60) + timerDict['mins']) * 60
    self.runningTimers[ timerDict['name'] ] = [totalSecs, 0, { 'color': timerDict['color'] }]
    self.runTimers()
  
  
  def handleTimerStopClick(self, menuItem, timerName):
    if timerName in self.runningTimers: del self.runningTimers[timerName]
    if timerName in self.completedTimers: del self.completedTimers[timerName]
    
    if self.timersMenuOpen == True:
      self.runningTimersMenu.deactivate()
    
    if len(self.runningTimers) == 0:
      self.statusIcon.set_icon_name(ICON__TRAY_OFF)
  
  
  def handleTimerEditClick(self, menuItem, timerDict, ndx):
    self.openTimerEditor(
      timerDict=timerDict,
      timerNdx=ndx
    )
  
  
  def handleTimerDeleteClick(self, menuItem, timerDict, ndx):
    dialog = Dialog()
    dialog.set_title('Delete Timer')
    dialog.add_button('Cancel', 0)
    dialog.add_button('Delete', 1)
    
    timerName = timerDict['name']
    text = Gtk.Label.new(f"Are you sure you want to delete the\ntimer for \"{timerName}\"?")
    dialog.setBody(text)
    
    def handleResponse(_dialog, code):
      if code == 1:
        self.handleTimerStopClick(None, timerName)
        del self.config['timers'][ndx]
        self.saveConfig()
        
      _dialog.close()
    
    dialog.connect('response', handleResponse)
    dialog.show_all()
  
  
  def setFont(self, lbl, family = None, size = None, weight = None):
    fd = Pango.FontDescription.new()
    if family is not None: fd.set_family(family)
    if size is not None: fd.set_size(Pango.SCALE * size)
    if weight is not None: fd.set_weight(weight)
    font = Pango.AttrFontDesc.new(fd)
    attrs = Pango.AttrList.new()
    attrs.insert(font)
    lbl.set_attributes(attrs)
  
  
  def setTimerText(self, timer):
    remainingSecs = timer[0] - timer[1]
    timer[2]['display']['label'].set_text( str(timedelta(seconds=remainingSecs)) )
  
  
  def handleTimersMenuClose(self, menu):
    self.timersMenuOpen = False
  
  
  def handleTrayBtnRelease(self, icon, x, y, button, time, panel_position):
    iconWidth = 20 # this is just a guess
    
    if button == 1: # left-click
      self.runningTimersMenu = Gtk.Menu.new()
      self.runningTimersMenu.set_reserve_toggle_size(False)
      
      runningCount = len(self.runningTimers)
      if runningCount:
        for ndx, timerName in enumerate(self.runningTimers):
          timer = self.runningTimers[timerName]
          
          item = Gtk.MenuItem.new()
          ctx = item.get_style_context()
          ctx.add_class('eggtimer-running-timer')
          if timer[0] == timer[1]: ctx.add_class(MODIFIER__TIMER_DONE)
          
          grid = Gtk.Grid.new()
          item.add(grid)
          
          if ndx > 0: ctx.add_class('has--sep')
          
          cssItemName = f"timer_{ndx}"
          colorBox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
          cssProvider = Gtk.CssProvider.new()
          css = f".for--{cssItemName} {{ background-color: {timer[2]['color']}; }}"
          cssProvider.load_from_data(bytes(css.encode()))
          ctx = colorBox.get_style_context()
          ctx.add_class('eggtimer-running-timer__color')
          ctx.add_class(f"for--{cssItemName}")
          ctx.add_provider(cssProvider, 601)
          grid.attach(colorBox, 0, 0, 1, 2)
          
          nameLabel = Gtk.Label.new(timerName)
          ctx = nameLabel.get_style_context()
          ctx.add_class('eggtimer-running-timer__name-label')
          self.setFont(nameLabel, family = 'Ubuntu Mono', size = 14, weight = Pango.Weight.BOLD)
          grid.attach(nameLabel, 1, 0, 1, 1)
          
          timeLabel = Gtk.Label.new('00:00:00')
          timeLabel.set_hexpand(True)
          timeLabel.set_halign(Gtk.Align.CENTER)
          ctx = timeLabel.get_style_context()
          ctx.add_class('eggtimer-running-timer__time-label')
          self.setFont(timeLabel, family = 'Ubuntu Mono', size = 24)
          grid.attach(timeLabel, 1, 0 + 1, 1, 1)
          timer[2]['display'] = { 'label': timeLabel, 'menuItem': item }
          self.setTimerText(timer)
          
          item.connect('activate', self.handleTimerStopClick, timerName)
          item.set_tooltip_text('Click to Stop Timer')
          
          self.runningTimersMenu.append(item)
      
        self.runningTimersMenu.show_all()
        self.runningTimersMenu.connect('deactivate', self.handleTimersMenuClose)
        
        self.statusIcon.popup_menu(self.runningTimersMenu, x, y, button, time, panel_position)
        menuOffset = 0
        if panel_position == Gtk.PositionType.BOTTOM or panel_position == Gtk.PositionType.TOP:
          # can't center a menu without first displaying it
          menuWidth = self.runningTimersMenu.get_allocated_width()
          menuOffset = (menuWidth/2) - iconWidth
          self.statusIcon.popup_menu(self.runningTimersMenu, x - menuOffset, y, button, time, panel_position)
        
        self.timersMenuOpen = True
        
    elif button == 3: # right-click
      menu = Gtk.Menu.new()
      menu.set_reserve_toggle_size(False)
      
      if 'timers' in self.config:
        for ndx, timerDict in enumerate(self.config['timers']):
          timerName = timerDict['name']
          
          timerItem = Gtk.MenuItem.new_with_label(f"{str(timerDict['hours']).rjust(2, '0')}:{str(timerDict['mins']).rjust(2, '0')} | {timerName}")
          subMenu = Gtk.Menu.new()
          
          if timerName in self.runningTimers or timerName in self.completedTimers:
            stopItem = Gtk.MenuItem.new_with_label('Stop')
            stopItem.connect('activate', self.handleTimerStopClick, timerName)
            subMenu.append(stopItem)
          else:
            startItem = Gtk.MenuItem.new_with_label('Start')
            startItem.connect('activate', self.handleTimerStartClick, timerDict)
            subMenu.append(startItem)
          
          editItem = Gtk.MenuItem.new_with_label('Edit')
          editItem.connect('activate', self.handleTimerEditClick, timerDict, ndx)
          subMenu.append(editItem)
          
          deleteItem = Gtk.MenuItem.new_with_label('Delete')
          deleteItem.connect('activate', self.handleTimerDeleteClick, timerDict, ndx)
          subMenu.append(deleteItem)
          
          timerItem.set_submenu(subMenu)
          menu.append(timerItem)
        
        menu.append(Gtk.SeparatorMenuItem.new())
      
      item = Gtk.MenuItem.new_with_label('Create Timer')
      item.connect('activate', self.createTimer)
      menu.append(item)
      
      menu.append(Gtk.SeparatorMenuItem.new())
      
      item = Gtk.MenuItem.new_with_label('Quit')
      item.connect('activate', self.quitApp)
      menu.append(item)
      
      menu.show_all()
      
      self.statusIcon.popup_menu(menu, x, y, button, time, panel_position)
      menuOffset = 0
      if panel_position == Gtk.PositionType.BOTTOM or panel_position == Gtk.PositionType.TOP:
        # can't center a menu without first displaying it
        menuWidth = menu.get_allocated_width()
        menuOffset = (menuWidth/2) - iconWidth
        self.statusIcon.popup_menu(menu, x - menuOffset, y, button, time, panel_position)
  
  
  def saveTimer(self, name, hours, mins, color, timerNdx=None):
    if 'timers' not in self.config:
      self.config['timers'] = []
    
    colorTuple=eval(color.to_string().replace('rgb', ''))
    colorHex = '#{:02x}{:02x}{:02x}'.format(*colorTuple)
    
    timerDict = {
      'color': colorHex,
      'hours': int(hours),
      'mins': int(mins),
      'name': name
    }
    
    if timerNdx is None:
      self.config['timers'].append(timerDict)
    else:
      self.config['timers'][timerNdx] = timerDict
    
    self.saveConfig()
  
  
  def openTimerEditor(self, timerDict=None, timerNdx=None):
    dialog = Dialog()
    title = 'Create a Timer' if timerDict is None else 'Edit Timer'
    dialog.set_title(title)
    
    grid = Gtk.Grid.new()
    
    nameLabel = Gtk.Label.new('Timer Name:  ')
    nameInput = Gtk.Entry.new()
    if timerDict is not None: nameInput.set_text(timerDict['name'])
    grid.attach(nameLabel, 0, 0, 1, 1)
    grid.attach(nameInput, 1, 0, 1, 1)
    
    hrsLabel = Gtk.Label.new('Hours:  ')
    hrsLabel.set_xalign(1)
    hrsInput = Gtk.SpinButton.new_with_range(0, 23, 1)
    if timerDict is not None: hrsInput.set_value(timerDict['hours'])
    grid.attach(hrsLabel, 0, 1, 1, 1)
    grid.attach(hrsInput, 1, 1, 1, 1)
    
    minsLabel = Gtk.Label.new('Minutes:  ')
    minsLabel.set_xalign(1)
    minsInput = Gtk.SpinButton.new_with_range(0, 59, 1)
    if timerDict is not None: minsInput.set_value(timerDict['mins'])
    grid.attach(minsLabel, 0, 2, 1, 1)
    grid.attach(minsInput, 1, 2, 1, 1)
    
    clrLabel = Gtk.Label.new('Color:  ')
    clrLabel.set_xalign(1)
    defaultColor = Gdk.RGBA()
    defaultColor.parse('#00C487')
    if timerDict is not None: defaultColor.parse(timerDict['color'])
    clrBtn = Gtk.ColorButton.new_with_rgba(defaultColor)
    grid.attach(clrLabel, 0, 3, 1, 1)
    grid.attach(clrBtn, 1, 3, 1, 1)
    
    dialog.setBody(grid)
    
    dialog.add_button('Cancel', 0)
    submitBtnLabel = 'Create' if timerDict is None else 'Update'
    dialog.add_button(submitBtnLabel, 1)
    
    def handleCreateDialogResponse(_dialog, code):
      if code == 1:
        self.saveTimer(
          nameInput.get_text(),
          hrsInput.get_value(),
          minsInput.get_value(),
          clrBtn.get_rgba(),
          timerNdx=timerNdx
        )
      
      _dialog.close()
    
    dialog.connect('response', handleCreateDialogResponse)
    
    dialog.show_all()
  
  
  def createTimer(self, *args):
    self.openTimerEditor()
  
  
  def quitApp(self, *args):
    # TODO: kill any running timers
    # for timer in self.timers:
    #   timer.destroy()
    self.quit()


if __name__ == '__main__':
  eggTimer = Application()
  eggTimer.run()
