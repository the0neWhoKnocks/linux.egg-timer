from tkinter import StringVar, Variable
from tkinter.ttk import Spinbox

from customtkinter import CTkFont, CTkFrame, CTkLabel

from eggtimer.constants import (
  FONT__DEFAULT__FAMILY,
  FONT__DEFAULT__SIZE,
)


# TODO: custom SpinBox https://customtkinter.tomschimansky.com/tutorial/spinbox/
# https://tkdocs.com/shipman/spinbox.html
class BaseSpinBox(Spinbox):
    def __init__(self, parent: CTkFrame, to: int, textvariable: Variable) -> None:
        mono_font = CTkFont(family=FONT__DEFAULT__FAMILY, size=FONT__DEFAULT__SIZE)  # can't use a tuple, have to use CTkFont to ensure this non-CTk widget's text looks like the other widgets
        super().__init__(
          parent,
          font=mono_font,
          format="%02.0f",
          from_=00,
          increment=1,
          justify="center",
          state="normal",
          textvariable=textvariable,
          to=to,
          width=4,
          wrap=True,  # when the max/lowest is reached, wrap around to the next value
        )


class EditableTimer(CTkFrame):
    def __init__(self, parent: CTkFrame) -> None:
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="new", padx=5, pady=5)
        
        self.val_hours = StringVar(value="00")
        self.val_mins = StringVar(value="00")
        self.val_secs = StringVar(value="00")
        
        self.hours = BaseSpinBox(self, to=24, textvariable=self.val_hours)
        self.hours.grid(row=0, column=0)
        CTkLabel(self, text=":").grid(row=0, column=1)
        self.mins = BaseSpinBox(self, to=59, textvariable=self.val_mins)
        self.mins.grid(row=0, column=2)
        CTkLabel(self, text=":").grid(row=0, column=3)
        self.secs = BaseSpinBox(self, to=59, textvariable=self.val_secs)
        self.secs.grid(row=0, column=4)
    
    def reset_vals(self) -> None:
        self.hours.set("00")
        self.mins.set("00")
        self.secs.set("00")
