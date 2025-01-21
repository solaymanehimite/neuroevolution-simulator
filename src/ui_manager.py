import pygame
from pygame import Color, Vector2
from panel import Panel


class UiManager:

    def __init__(self):
        self.font = pygame.font.Font("../res/Monocraft.ttf", 18)
        self.char_width, self.char_height = self.font.size("A")
        self.line_spacing = 4

        self.simulation_info = {}

        self.info_panel = Panel(Vector2(0, 0), Vector2(220, 200),
                                Color(20, 20, 20)) \
            .set_render_function(self.render_info_panel)

    def toggle_info_panel(self):
        if self.info_panel.target_position.x == -220:
            self.info_panel.target_position.x = 0
        else:
            self.info_panel.target_position.x = -220

    def render_info_panel(self, panel: Panel):
        panel.render_text(self.font, "INFO", Color(
            255, 255, 255), Vector2(10, 10))
        panel.render_text(self.font, self.get_render_text("Generation:", self.simulation_info['gen'], 16), Color(
            255, 255, 255), Vector2(10, 10 + (self.char_height + self.line_spacing) * 2))
        panel.render_text(self.font, self.get_render_text("Succes :", f"{self.simulation_info['scs']}%", 16), Color(
            255, 255, 255), Vector2(10, 10 + (self.char_height + self.line_spacing) * 3))
        panel.render_text(self.font, self.get_render_text("Average :", self.simulation_info['scr'], 16), Color(
            255, 255, 255), Vector2(10, 10 + (self.char_height + self.line_spacing) * 4))

    def get_render_text(self, text_1: str, text_2: str, w: int):
        return text_1 + "".join([" " for i in range(w - len(str(text_1)) - len(str(text_2)))]) + str(text_2)

    def render(self, surface: pygame.Surface):
        self.info_panel.render(surface)
        self.render_mouse(surface)

    def update(self):
        self.info_panel.update()

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
