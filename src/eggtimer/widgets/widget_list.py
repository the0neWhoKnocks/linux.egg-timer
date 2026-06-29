import tkinter as tk
import uuid
from tkinter import ttk

from eggtimer.constants import (
    MOUSE_SCROLL__DOWN,
    MOUSE_SCROLL__UP,
)


class WidgetList(ttk.Frame):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.widgets = {}
        
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create the internal frame that will hold your list of widgets
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Bind the internal frame configuration to update the canvas scroll region.
        # - This dynamically tells the canvas how far down the scroll bar thumb
        #   needs to stretch as row items are appended.
        self.scrollable_frame.bind(
            "<Configure>",
            lambda _ev: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        
        # Create a window inside the canvas to host the internal frame.
        # - Instead of packing or gridding your internal frame directly to a
        #   window, you drop it inside the `Canvas` space using this explicit
        #   vector layout method.
        self.canvas_frame_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Bind the canvas configuration to adjust the internal frame width to fill the window.
        # - The canvas layout binding runs a custom handler ensuring that row
        #   dimensions dynamically scale to match the window container sizing.
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Configure canvas scrolling behavior
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack layout elements
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for seamless scrolling
        # - `<MouseWheel> Hook`: Tkinter does not automatically hook up physical
        #   scroll wheels to scroll bars. Binding `yview_scroll` handles the
        #   operating system signals seamlessly.
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, ev: tk.Event) -> None:
        # Forces internal frame to stretch horizontally to match the canvas width
        self.canvas.itemconfig(self.canvas_frame_window, width=ev.width)

    def _on_mousewheel(self, ev: tk.Event) -> None:
        # Cross-platform mouse wheel scrolling support
        if ev.num == MOUSE_SCROLL__UP or ev.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif ev.num == MOUSE_SCROLL__DOWN or ev.delta < 0:
            self.canvas.yview_scroll(1, "units")
    
    def add_item(self, Class: tk.Tk, **kwargs) -> [str, tk.Tk]:  # noqa: ANN003, N803
        widget = Class(self.scrollable_frame, **kwargs)
        uid = uuid.uuid1().hex
        self.widgets[uid] = widget
        return uid, widget
    
    def remove_item(self, uid: str) -> None:
        widget = self.widgets[uid]
        widget.destroy()
        del self.widgets[uid]
