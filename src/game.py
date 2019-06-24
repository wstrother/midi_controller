import pygame
import sys
from constants import PYGAME_RECT, PYGAME_LINE, PYGAME_CIRCLE


class Game:
    def __init__(self, screen, env):
        self.screen = screen
        self.env = env

    def run_game(self):
        while True:
            self.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        self.env.update()
        self.screen.update()

        self.screen.draw(
            *self.env.get_graphics()
        )


class Screen:
    def __init__(self, size):
        self._screen = pygame.display.set_mode(size)

    def update(self):
        pygame.display.flip()
        self._screen.fill((0, 0, 0))

    def draw(self, *arg_sets):
        for arg_set in arg_sets:
            self.render(*arg_set)

    def render(self, obj, *args):
        if type(obj) is pygame.Surface:
            position = args[0]
            self.render_image(obj, position)

        else:
            self.render_geometry(obj, *args)

    def render_image(self, image, position):
        self._screen.blit(image, position)

    def render_geometry(self, method, *args):
        if method == PYGAME_RECT:
            pygame.draw.rect(self._screen, *args)

        if method == PYGAME_LINE:
            pygame.draw.line(self._screen, *args)

        if method == PYGAME_CIRCLE:
            pygame.draw.circle(self._screen, *args)
