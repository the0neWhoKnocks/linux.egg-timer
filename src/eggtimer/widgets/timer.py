import tkinter as tk
from tkinter import ttk


class Timer(ttk.Frame):
    def __init__(  # noqa: PLR0913
        self,
        parent: tk.Tk,
        *,
        color: str,
        name: str,
        hours: str,
        minutes: str,
        seconds: str,
        delete_handler: callable | None = None,
    ) -> None:
        super().__init__(parent, borderwidth=1, padding=5, relief="solid")
        self.pack(fill="x", pady=2, padx=5)
        self.name = name
        self.color_chip = tk.Canvas(self, width=30, height=30, bg=color)
        self.color_chip.pack(side="left", padx=5)
        self.label = ttk.Label(self, text=name)
        self.label.pack(side="left", padx=5)
        self.time = ttk.Label(self, text=f"{hours}:{minutes}:{seconds}")
        self.time.pack(side="left", padx=5)
        self.delete_btn = ttk.Button(self, text="Delete", command=delete_handler)
        self.delete_btn.pack(side="left", padx=5)
