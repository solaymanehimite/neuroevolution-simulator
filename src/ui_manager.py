import pygame
from panel import Panel


def render_info_panel(font: pygame.font.Font):
    return lambda panel: panel.render_text(font,
                                           "hello world",
                                           pygame.Color(255, 255, 255),
                                           pygame.Vector2(10, 10))


class UiManager:

    def __init__(self):
        self.font = pygame.font.Font("../res/Monocraft.ttf", 18)
        self.char_width, self.char_height = self.font.size("A")
        self.line_spacing = 4

        self.info_panel = Panel(pygame.Vector2(0, 0), pygame.Vector2(
            200, 400), pygame.Color(20, 20, 20)) \
            .set_render_function(render_info_panel(self.font))

    def toggle_info_panel(self):
        if self.info_panel.target_position.x == -200:
            self.info_panel.target_position.x = 0
        else:
            self.info_panel.target_position.x = -200

    def render(self, surface: pygame.Surface):
        self.info_panel.render(surface)
        self.render_mouse(surface)

    def update(self):
        self.info_panel.update()

    def render_text(self, surface: pygame.Surface, text: str,
                    position: pygame.Vector2, color: pygame.Color):
        render = self.font.render(text, False, color, (0, 0, 0))
        surface.blit(render, position)

    def render_mouse(self, surface: pygame.Surface):
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())

        mouse_points = [
            mouse_position,
            pygame.Vector2(mouse_position.x + 12, mouse_position.y + 12),
            pygame.Vector2(mouse_position.x, mouse_position.y + 17),
        ]

        pygame.draw.polygon(
            surface,
            (0, 0, 0),
            mouse_points,
        )
        pygame.draw.polygon(
            surface,
            (255, 255, 255),
            mouse_points,
            1,
        )
