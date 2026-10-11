import pygame as pg

from src.ui.ui_node import UI_Node, FONT


class Button(UI_Node):
    def __init__(
        self,
        pos,
        size,
        function=None,
        text="",
        text_color=(255, 255, 255),
        bg_color=(50, 50, 50),
        hover_color=(80, 80, 80),
        border_radius=12,
    ):
        self.pos = pos
        self.size = size
        self.function = function
        self.function_running = False

        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.border_radius = border_radius

        self.text_image = FONT.render(
            self.text, True, self.text_color
        )

        self.image = pg.Surface(self.size, pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft=self.pos)

        self.hovered = False
        self.update_cursor = False

        self.draw()

    def draw(self):
        self.image.fill((0, 0, 0, 0))

        color = self.hover_color if self.hovered else self.bg_color

        pg.draw.rect(
            self.image,
            color,
            self.image.get_rect(),
            border_radius=self.border_radius,
        )

        text_rect = self.text_image.get_rect(
            center=(self.size[0] // 2, self.size[1] // 2)
        )
        self.image.blit(self.text_image, text_rect)

    def render(self, surface):
        self.rect.topleft = self.pos

        mouse_pos = pg.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        # Use a hand pointer when hovering
        if self.hovered:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)

            if pg.mouse.get_pressed()[0] and not self.function_running:
                if self.function:
                    self.function_running = True
                    self.function()

            if not pg.mouse.get_pressed()[0]:
                self.function_running = False

        else:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

        self.draw()
        surface.blit(self.image, self.rect)
