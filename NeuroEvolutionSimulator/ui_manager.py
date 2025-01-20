import pygame


class UiManager:

    def __init__(self):
        self.font = pygame.font.Font("res/Monocraft.ttf", 18)
        self.char_width, self.char_height = self.font.size("A")
        self.line_spacing = 4

    def render(self, surface: pygame.Surface):
        self.render_mouse(surface)

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
