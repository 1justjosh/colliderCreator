from src.engine.scene import Scene
from src.engine.settings import *

import pygame as pg


class Window:
    def __init__(self):
        pg.init()

        self.display = pg.display.set_mode(RES)
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()

        self.scene = Scene()

        self.running = True

    def handle_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            self.scene.handle_events(event)

    def update(self):
        dt = self.clock.tick(FPS_CAP) / 1000

        self.scene.update(dt)

    def render(self):
        self.display.fill(BG_COLOR)

        self.scene.render()

        pg.display.flip()

    def run(self):
        while self.running:
            self.handle_event()
            self.update()
            self.render()