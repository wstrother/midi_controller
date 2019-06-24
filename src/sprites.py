from entities import Sprite
from graphics import TextGraphics, ButtonGraphics, AxisGraphics
from pygame.font import Font, match_font
from constants import MIDI_CC_MAX


class TextSprite(Sprite):
    def __init__(self, name):
        super(TextSprite, self).__init__(name)

        self.text = ""
        self.font = None
        self.color = None

    def set_text(self, text):
        self.text = text

    def set_color(self, r, g, b):
        self.color = r, g, b

    def set_font(self, size, *args):
        self.font = Font(match_font(*args), size)

    def set_graphics(self):
        self.graphics = TextGraphics(self)
        self.set_size(*self.graphics.image.get_size())


class MidiHudSprite(Sprite):
    def __init__(self, name):
        super(MidiHudSprite, self).__init__(name)

        self.device_name = ""

    def set_device_name(self, name):
        self.device_name = name

    def get_device_value(self):
        if self.controller:
            return self.controller.get_value(self.device_name)


class ButtonSprite(MidiHudSprite):
    def __init__(self, name):
        super(ButtonSprite, self).__init__(name)

        self.radius = 1
        self.last = None
        self.color = None
        self.on = False

        self.update_methods += [
            self.update_button,
            self.update_button_events
        ]

    def set_graphics(self):
        self.graphics = ButtonGraphics(self)

    def set_radius(self, r):
        self.radius = r
        self.set_size(2 * r, 2 * r)

    def set_color(self, r, g, b):
        self.color = r, g, b

    def update_button(self):
        v = self.get_device_value()

        self.on = bool(v)

    def update_button_events(self):
        last, on = self.last, self.on

        if last != on:
            if on:
                self.handle_event("button_on")

            if not on:
                self.handle_event("button_off")

        self.last = on


class LatchSprite(ButtonSprite):
    def __init__(self, name):
        super(LatchSprite, self).__init__(name)

        self.held = 0

    def update_button(self):
        v = self.get_device_value()

        if v:
            self.held += 1
        else:
            self.held = 0

        if self.held == 1:
            self.on = not self.on


class MeterSprite(MidiHudSprite):
    def __init__(self, name):
        super(MeterSprite, self).__init__(name)

        self.colors = None, None
        self.meter_value = 0
        self.sign = 1
        self.range = 0

        self.last = 0

        self.update_methods += [
            self.update_meter,
            self.update_meter_events
        ]

    def set_graphics(self):
        self.graphics = AxisGraphics(self)

    def set_colors(self, fill, empty):
        self.colors = fill, empty

    def set_sign(self, s):
        self.sign = s

    def set_range(self, r):
        self.range = r

    def get_device_value(self):
        if type(self.device_name) is str:
            return super(MeterSprite, self).get_device_value()

        else:
            up, down = self.device_name
            up = self.controller.get_value(up)
            down = self.controller.get_value(down)

            down *= -1

            return up + down

    def update_meter(self):
        v = self.get_device_value() * self.sign
        r = self.range

        if r == 0:
            m = (v + 1) / 2
        else:
            if r > 0:
                if v < 0:
                    v = 0
            elif r < 0:
                if v > 0:
                    v = 0
            m = v

        self.meter_value = abs(m) * MIDI_CC_MAX

    def update_meter_events(self):
        last, current = int(self.last), int(self.meter_value)

        if last != current:
            self.handle_event({
                "name": "meter_change",
                "value": current
            })

            self.last = self.meter_value


class FaderSprite(MeterSprite):
    def __init__(self, name):
        super(FaderSprite, self).__init__(name)

        self.threshold = 0
        self.rate = 1

    def set_rate(self, r):
        self.rate = r

    def set_threshold(self, t):
        self.threshold = t

    def update_meter(self):
        v = self.get_device_value()

        if abs(v) > self.threshold:
            dv = v * self.rate

            self.meter_value += dv

            if self.meter_value > MIDI_CC_MAX:
                self.meter_value = MIDI_CC_MAX

            if self.meter_value < 0:
                self.meter_value = 0
