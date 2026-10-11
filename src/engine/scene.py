import threading
import tkinter

import pygame as pg
import tkinter as tk

from tkinter import filedialog, ttk, messagebox
from pathlib import Path

from src.ui.button import Button



class Scene:
    def __init__(self):
        self.win = pg.display.get_surface()
        self.tilemap = None
        self.tilemap_settings = None

        # Hidden Tkinter root
        self.root = tk.Tk()
        self.root.withdraw()

        self.load_tilemap_button = Button(
            (self.win.get_width() // 2 - 64,
             self.win.get_height() // 2 - 32),
            (128, 64),
            text="Load Tilemap",
            function=self.select_tilemap,
        )

    def select_tilemap(self):
        path = filedialog.askopenfilename(
            parent=self.root,
            title="Select Tilemap",
            filetypes=[("PNG images", "*.png")],
        )

        if not path:
            return

        self.show_tilemap_options(path)

    def show_tilemap_options(self, path):
        popup = tk.Toplevel(self.root)
        popup.title("Tilemap Import Settings")
        popup.geometry("350x320")
        popup.resizable(False, False)

        # Bring the popup to the front
        popup.update_idletasks()
        popup.lift()
        popup.focus_force()
        popup.grab_set()

        tk.Label(
            popup,
            text=f"Selected: {path.split('/')[-1]}",
            wraplength=320,
        ).pack(pady=10)

        fields = {}

        defaults = {
            "Tile Width": "16",
            "Tile Height": "16",
            "Spacing": "0",
            "Margin": "0",
        }

        for label, default in defaults.items():
            row = tk.Frame(popup)
            row.pack(fill="x", padx=20, pady=5)

            tk.Label(row, text=label, width=14, anchor="w").pack(
                side="left"
            )

            entry = ttk.Entry(row)
            entry.insert(0, default)
            entry.pack(side="right", expand=True, fill="x")

            fields[label] = entry

        def import_tilemap():
            try:
                settings = {
                    key: int(entry.get())
                    for key, entry in fields.items()
                }

                if (
                        settings["Tile Width"] <= 0
                        or settings["Tile Height"] <= 0
                        or settings["Spacing"] < 0
                        or settings["Margin"] < 0
                ):
                    raise ValueError

            except ValueError:
                from tkinter import messagebox
                messagebox.showerror(
                    "Invalid Settings",
                    "Enter positive tile dimensions and "
                    "non-negative spacing and margin.",
                    parent=popup,
                )
                return

            self.tilemap = pg.transform.scale(pg.image.load(path).convert_alpha(), self.win.get_size())
            self.tilemap_settings = settings

            print("Tilemap loaded:", path)
            print("Settings:", settings)

            popup.grab_release()
            popup.destroy()

            self.root.destroy()

        buttons = tk.Frame(popup)
        buttons.pack(pady=20)

        ttk.Button(
            buttons,
            text="Cancel",
            command=popup.destroy,
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Import",
            command=import_tilemap,
        ).pack(side="left", padx=5)

        tk.mainloop()

    def handle_events(self, event):
        pass

    def update(self, dt):
        pass

    def render(self):
        if not self.tilemap:
            self.load_tilemap_button.render(self.win)

        if self.tilemap is not None:
            self.win.blit(self.tilemap, (0, 0))

