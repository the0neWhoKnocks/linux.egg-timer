import tkinter as tk
import tkinter.font as tk_font
from tkinter import ttk


class EditableTimer(ttk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="new", padx=5, pady=5)
        
        normal_font = tk_font.Font(family="Ubuntu Mono", size=12, weight=tk_font.NORMAL)
        spinbox_config = {
          "font": normal_font,
          "format": "%02.0f",
          "from_": 00,
          "increment": 1,
          "justify": "center",
          "state": "normal",
          "width": 4,
          "wrap": True,  # when the max/lowest is reached, wrap around to the next value
        }
        
        self.val_hours = tk.StringVar(value="00")
        self.val_mins = tk.StringVar(value="00")
        self.val_secs = tk.StringVar(value="00")
        
        self.hours = ttk.Spinbox(self, to=24, textvariable=self.val_hours, **spinbox_config)
        self.hours.grid(row=0, column=0)
        ttk.Label(self, text=":").grid(row=0, column=1)
        self.mins = ttk.Spinbox(self, to=59, textvariable=self.val_mins, **spinbox_config)
        self.mins.grid(row=0, column=2)
        ttk.Label(self, text=":").grid(row=0, column=3)
        self.secs = ttk.Spinbox(self, to=59, textvariable=self.val_secs, **spinbox_config)
        self.secs.grid(row=0, column=4)
    
    def reset_vals(self) -> None:
        self.hours.set("00")
        self.mins.set("00")
        self.secs.set("00")
