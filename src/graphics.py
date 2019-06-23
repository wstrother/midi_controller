from game import PYGAME_RECT, PYGAME_CIRCLE
from pygame import Rect

MIDI_CC_MAX = 127


class TextGraphics:
    def __init__(self, entity):
        self.entity = entity
        self.image = None
        self.set_image()

    def get_image(self):
        color = self.entity.color
        text = self.entity.text
        font = self.entity.font

        return font.render(text, 1, color)

    def set_image(self):
        self.image = self.get_image()
        self.entity.set_size(*self.image.get_size())

    def get_args(self):
        args = [
            (self.image, self.entity.position)
        ]

        return args


class GeometryGraphics:
    def __init__(self, entity):
        self.entity = entity
        self.items = []

    def get_args(self):
        return self.items


class ButtonGraphics(GeometryGraphics):
    def get_args(self):
        r = self.entity.radius
        color = self.entity.color
        x, y = self.entity.position
        pos = r + x, r + y

        if self.entity.on:
            self.items = [
                (PYGAME_CIRCLE, color, pos, r)
            ]
        else:
            self.items = [
                (PYGAME_CIRCLE, color, pos, r, 2)
            ]

        return super(ButtonGraphics, self).get_args()


class AxisGraphics(GeometryGraphics):
    def __init__(self, entity):
        super(AxisGraphics, self).__init__(entity)

        self.fill_rect = Rect((0, 0), (1, 1))
        self.empty_rect = Rect((0, 0), (1, 1))

    def get_args(self):
        fill_color, empty_color = self.entity.colors
        r = self.entity.meter_value / MIDI_CC_MAX
        w, h = self.entity.size
        x, y = self.entity.position

        fill_w = (r * w) // 1
        empty_w = w - fill_w

        self.fill_rect.size = fill_w, h
        self.fill_rect.topleft = x, y
        self.empty_rect.size = empty_w, h
        self.empty_rect.topleft = x + fill_w, y

        self.items = [
            (PYGAME_RECT, fill_color, self.fill_rect),
            (PYGAME_RECT, empty_color, self.empty_rect)
        ]

        return super(AxisGraphics, self).get_args()
