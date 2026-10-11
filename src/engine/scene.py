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
        self.tilemap_scale_by = []
        self.tilemap_settings = None

        self.hover_surface = None
        self.hover_surface_size = None

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

            image = pg.image.load(path).convert_alpha()

            scale_x = self.win.get_width() / image.get_width()
            scale_y = self.win.get_height() / image.get_height()

            self.tilemap_scale_by = [scale_x, scale_y]

            self.tilemap = pg.transform.scale(
                image,
                self.win.get_size()
            )
            self.tilemap_settings = settings

            scaled_tile_width = settings["Tile Width"] * scale_x
            scaled_tile_height = settings["Tile Height"] * scale_y

            self.hover_surface_size = (
                round(scaled_tile_width),
                round(scaled_tile_height)
            )

            self.hover_surface = pg.Surface(
                self.hover_surface_size,
                pg.SRCALPHA
            )

            self.hover_surface.fill((200, 200, 200, 150))

            print("Tilemap loaded:", path)
            print("Settings:", settings)

            popup.grab_release()
            popup.destroy()

            self.root.destroy()

            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

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

            tile_height = self.tilemap_settings["Tile Height"]
            tile_width = self.tilemap_settings["Tile Width"]

            scaled_tile_width = tile_width * self.tilemap_scale_by[0]
            scaled_tile_height = tile_height * self.tilemap_scale_by[1]

            rows = (self.tilemap.get_height() // tile_height) * self.tilemap_scale_by[1]
            cols = (self.tilemap.get_width() // tile_width) * self.tilemap_scale_by[0]

            for row in range(int(rows) + 1):
                y = int(row * scaled_tile_height)

                pg.draw.line(
                    self.win,
                    (10, 10, 10),
                    (0, y),
                    (self.win.get_width(), y)
                )

            for col in range(int(cols) + 1):
                x = int(col * scaled_tile_width)

                pg.draw.line(
                    self.win,
                    (10, 10, 10),
                    (x, 0),
                    (x, self.win.get_height())
                )

            mouse_pos = pg.mouse.get_pos()

            #
            # tile_hovered_w = int(mouse_pos[0] // scaled_tile_width)
            # tile_hovered_h = int(mouse_pos[1] // scaled_tile_height)
            #
            # x1 = round(tile_hovered_w * scaled_tile_width)
            # y1 = round(tile_hovered_h * scaled_tile_height)
            # x2 = round((tile_hovered_w + 1) * scaled_tile_width)
            # y2 = round((tile_hovered_h + 1) * scaled_tile_height)
            #
            #
            #
            # self.hover_surface.fill((200, 200, 200, 150))  # RGBA; 100 = transparency level
            #
            # self.win.blit(self.hover_surface, (x1, y1))
