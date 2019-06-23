import sys

import pygame
from zsquirrel.constants import PYGAME_RECT, PYGAME_LINE, PYGAME_CIRCLE
from zsquirrel.game import Screen
from zsquirrel.resources import Image


class PygameScreen(Screen):
    """
    This is the default Screen subclass that provides a wrapper for the
    Pygame.display module as a backend. The render_graphics() method also
    implements additional methods that help extend the Pygame.draw's
    'rect', 'line' and 'circle' rendering functions.
    The Image object, imported from the ZSquirrel Resources also functions
    as a wrapper for the Pygame.surface module's Surface object, extending
    some of it's methods, as well as other new methods for convenience.
    """
    def __init__(self, size):
        """
        Initializes the Pygame.display module which creates the render Surface
        for the game's graphics.
        :param size: a tuple of integers (width, height)
        """
        super(PygameScreen, self).__init__(size)
        self._screen = pygame.display.set_mode(size)

    def refresh(self):
        """
        Clears the Pygame.event queue by calling the get() method, as well as
        checking for pygame.QUIT events (from closing the display window.)
        Also calls the Pygame.display.flip() method and fills display surface
        with black by default before rendering of each frame.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()
        self._screen.fill((0, 0, 0))

    def render_graphics(self, obj, *args):
        """
        The PygameScreen object helps identify objects passed to it by the Environment
        object and pass them to the appropriate rendering method used by the graphical
        backend -- in this case Pygame's 'surface' and 'draw' modules.
        :param obj: a generic variable to reprsent the type of object to be rendered
        :param args: an indefinite collection of parameters to be passes to various
            other methods, such as Pygame.draw's
        """
        render_graphics(self._screen, obj, *args)


def render_graphics(surface, obj, *args):
    if type(surface) is Image:
        surface = surface.pygame_surface

    if type(obj) is Image:  # the Image object from the resources module, which
                            # functions partially as a wrapper for Pygame's 'Surface"
                            # object.
        position = args[0]
        render_image(surface, obj.pygame_surface, position)

    else:
        render_geometry(surface, obj, *args)


def render_image(surface, image, position):

    surface.blit(image, position)


def render_geometry(surface, method, *args):
    if method == PYGAME_RECT:
        pygame.draw.rect(surface, *args)

    if method == PYGAME_LINE:
        pygame.draw.line(surface, *args)

    if method == PYGAME_CIRCLE:
        pygame.draw.circle(surface, *args)
