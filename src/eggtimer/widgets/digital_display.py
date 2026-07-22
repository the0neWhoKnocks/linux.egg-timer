import threading
from typing import TYPE_CHECKING

from customtkinter import CTkCanvas, CTkFont, CTkFrame

from eggtimer.constants import (
    FONT__TIMER__FAMILY,
    FONT__TIMER__SIZE,
)

if TYPE_CHECKING:
    from eggtimer.__main__ import EggTimer


class DigitalDisplay(CTkFrame):
    def __init__(self,  # noqa: PLR0913
      parent: CTkFrame,
      root: EggTimer,
      *,
      bg_color: str = "#000000",
      btm_txt: str = "88:88:88",
      btm_txt_color: str = "#444444",
      top_txt: str = "00:00:00",
      top_txt_color: str = "#EEEEEE",
    ) -> None:
        super().__init__(parent, fg_color=bg_color, corner_radius=8)
        
        self.root = root
        self.bg_color = bg_color
        self.btm_txt = btm_txt
        self.btm_txt_color = btm_txt_color
        self.top_txt = top_txt
        self.top_txt_color = top_txt_color
        
        self.build_ui()
    
    def blink_start(self) -> None:
        blink_speed = 1
        
        def play(exit_event: threading.Event) -> None:
            while not exit_event.is_set():
                self.canvas.itemconfig(self.top_txt_el, state="hidden")
                if exit_event.wait(timeout=blink_speed):
                    break
                self.canvas.itemconfig(self.top_txt_el, state="normal")
                if exit_event.wait(timeout=blink_speed):
                    break
            
            self.canvas.itemconfig(self.top_txt_el, state="normal")
        
        self.stop_signal = threading.Event()
        thread = threading.Thread(name="Blink", target=play, args=(self.stop_signal,))
        thread.start()
    
    def blink_stop(self) -> None:
        self.stop_signal.set()
    
    def build_ui(self) -> None:
        # Initialize the canvas with temporary dimensions (e.g., 1x1 pixel)
        self.canvas = CTkCanvas(self,
          bg=self.bg_color,
          highlightthickness=0,
          width=1,
          height=1,
        )
        self.canvas.pack(padx=6, pady=6)  # Padding handles background margins

        font = CTkFont(family=FONT__TIMER__FAMILY, size=FONT__TIMER__SIZE)

        # Add the bottom text
        btm_txt_el = self.canvas.create_text(
          0, 0,
          text=self.btm_txt,
          fill=self.btm_txt_color,
          font=font,
          anchor="nw",  # Anchor North-West makes calculating width easy
        )

        # Force Tkinter to calculate the text object metrics
        self.root.update_idletasks()

        # Extract bounding box measurements: (x1, y1, x2, y2)
        bbox = self.canvas.bbox(btm_txt_el)
        txt_width = bbox[2] - bbox[0]
        txt_height = bbox[3] - bbox[1]

        # Apply calculated text size directly to the canvas configuration
        self.canvas.configure(width=txt_width, height=txt_height)

        # Add overlay text exactly centered over the new canvas dimensions
        self.top_txt_el = self.canvas.create_text(
          txt_width // 2, txt_height // 2,
          text=self.top_txt,
          fill=self.top_txt_color,
          font=font,
          anchor="center",
        )

        # Reposition the bottom text to the center so it aligns with the overlay
        self.canvas.coords(btm_txt_el, txt_width // 2, txt_height // 2)
        self.canvas.itemconfig(btm_txt_el, anchor="center")
    
    def update_prop(self, *, text: str) -> None:
        if text:
            self.canvas.itemconfig(self.top_txt_el, text=text)
