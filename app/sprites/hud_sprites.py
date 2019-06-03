from zsquirrel.constants import PYGAME_CIRCLE
from zsquirrel.utils.geometry import Rect
from zsquirrel.graphics import GeometryGraphics
from zsquirrel.ui.ui_interface import UiSprite


class ButtonGraphics(GeometryGraphics):
    def __init__(self, entity, button):
        super(ButtonGraphics, self).__init__(entity)
        self.button = button
        self.color = 255, 0, 0

    def get_graphics(self, offset=None):
        r = self.entity.radius
        pos = r, r

        if self.button.get_value() == 1:
            self.items = [
                (PYGAME_CIRCLE, self.color, pos, r)
            ]
        else:
            self.items = [
                (PYGAME_CIRCLE, self.color, pos, r, 2)
            ]

        return super(ButtonGraphics, self).get_graphics(offset=offset)


class ButtonSprite(UiSprite):
    def __init__(self, name, button):
        super(ButtonSprite, self).__init__(name)

        self.radius = 12
        self.button = button
        self.graphics = ButtonGraphics(self, button)
        self.set_size(2 * self.radius, 2 * self.radius)


class AxisGraphics(GeometryGraphics):
    def __init__(self, entity, trigger):
        super(AxisGraphics, self).__init__(entity)

        self.trigger = trigger
        self.fill_color = 0, 255, 0
        self.fill_rect = Rect((0, 0), (0, 0))
        self.empty_color = 255, 0, 0
        self.empty_rect = Rect((0, 0), (0, 0))

        self.items = [
            (self.fill_rect, self.fill_color),
            (self.empty_rect, self.empty_color)
        ]

    def get_graphics(self, offset=None):
        r = (self.trigger.get_value() + 1) / 2
        w, h = self.entity.size
        fill_w = (r * w) // 1
        empty_w = w - fill_w

        self.fill_rect.size = fill_w, h
        self.empty_rect.size = empty_w, h
        self.empty_rect.position = fill_w, 0

        return super(AxisGraphics, self).get_graphics(offset=offset)


class AxisSprite(UiSprite):
    def __init__(self, name, trigger):
        super(AxisSprite, self).__init__(name)

        self.trigger = trigger
        self.graphics = AxisGraphics(self, trigger)
        self.set_size(50, 15)
