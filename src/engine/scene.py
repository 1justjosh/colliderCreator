import pygame as pg

class Scene:
    def __init__(self):
        self.win = pg.display.get_surface()

    def handle_events(self, event): ...

    def update(self, dt): ...

    def render(self): ...