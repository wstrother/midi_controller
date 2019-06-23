from zsquirrel.constants import PYGAME_CIRCLE
from zsquirrel.utils.geometry import Rect
from zsquirrel.graphics import GeometryGraphics
from zsquirrel.ui.ui_interface import UiSprite
from zsquirrel.control.controllers import Trigger, Button
from zsquirrel.utils.meters import Meter


class MidiHudSprite(UiSprite):
    def __init__(self, name):
        super(MidiHudSprite, self).__init__(name)

        self.device_name = ""

    def set_device_name(self, name):
        self.device_name = name

    @property
    def device(self):
        if self.controller:
            return self.controller.get_device(self.device_name)


class ButtonGraphics(GeometryGraphics):
    def __init__(self, entity):
        super(ButtonGraphics, self).__init__(entity)
        self.color = 255, 0, 0

    def get_graphics(self, offset=None):
        r = self.entity.radius
        pos = r, r

        if self.entity.get_button_value() == 1:
            self.items = [
                (PYGAME_CIRCLE, self.color, pos, r)
            ]
        else:
            self.items = [
                (PYGAME_CIRCLE, self.color, pos, r, 2)
            ]

        return super(ButtonGraphics, self).get_graphics(offset=offset)


class ButtonSprite(MidiHudSprite):
    def __init__(self, name):
        super(ButtonSprite, self).__init__(name)

        self.radius = 12
        self.graphics = ButtonGraphics(self)
        self.set_size(2 * self.radius, 2 * self.radius)

        self.on = False
        self.last = False
        self.dpad = False

        self.update_methods += [
            self.update_button,
            self.update_button_events
        ]

    def set_dpad_direction(self, d):
        self.dpad = d

    def set_color(self, color):
        self.graphics.color = color

    def set_radius(self, r):
        self.radius = r
        self.set_size(2 * r, 2 * r)

    def get_button_value(self):
        return self.on

    def update_button(self):
        if self.device:
            value = self.device.get_value()

            if self.dpad:
                dx, dy = self.dpad
                x, y = value
                x = round(x)
                y = round(y)
                self.on = (dx, dy) == (x, y)

            else:
                self.on = bool(value)

    def update_button_events(self):
        last, on = self.last, self.on
        if last != on:
            if on:
                self.handle_event("button_on")
            else:
                self.handle_event("button_off")

        self.last = on


class LatchSprite(ButtonSprite):
    def update_button(self):
        if self.device_name:
            value = self.device.held

            if value == 1:
                self.on = not self.on


class AxisGraphics(GeometryGraphics):
    def __init__(self, entity):
        super(AxisGraphics, self).__init__(entity)

        self.fill_color = 0, 255, 0
        self.fill_rect = Rect((0, 0), (0, 0))
        self.empty_color = 255, 0, 0
        self.empty_rect = Rect((0, 0), (0, 0))

        self.items = [
            (self.fill_rect, self.fill_color),
            (self.empty_rect, self.empty_color)
        ]

    def get_graphics(self, offset=None):
        r = self.entity.get_axis_value()
        w, h = self.entity.size
        fill_w = (r * w) // 1
        empty_w = w - fill_w

        self.fill_rect.size = fill_w, h
        self.empty_rect.size = empty_w, h
        self.empty_rect.position = fill_w, 0

        return super(AxisGraphics, self).get_graphics(offset=offset)


class AxisSprite(MidiHudSprite):
    def __init__(self, name):
        super(AxisSprite, self).__init__(name)

        self.meter = Meter("MIDI meter", 127)
        self.last = 0
        self.graphics = AxisGraphics(self)
        self.set_size(50, 15)

        self.sign = 0
        self.axis = "x"

        self.update_methods += [
            self.update_meter,
            self.update_meter_events
        ]

    def set_sign(self, value):
        self.sign = value

    def set_axis(self, axis):
        self.axis = axis

    def set_color(self, color):
        self.graphics.fill_color = color

    def get_axis_value(self):
        return self.meter.get_ratio()

    def update_meter(self):
        axis, sign = self.axis, self.sign

        if self.device:
            x, y = self.device.get_value()
            value = {"x": x, "y": y}[axis]

            if sign is 0:                   # sign = 0
                value = (value + 1) / 2     # -1 ... 1 == 0 ... 127
            else:
                if sign < 0:                # sign = -1
                    value *= -1             # -1 ... 0 == 0 ... 127 || 0 ... 1 == 0

                if value < 0:               # sign = 1
                    value = 0               # -1 ... 0 == 0 || 0 ... 1 == 0 ... 127

            self.meter.value = 127 * value

    def update_meter_events(self):
        last, current = self.last, int(self.meter.value)

        if last != current:
            # print("handling meter change")

            self.handle_event({
                "name": "meter_change",
                "value": current,
                "lerp": False
            })

        self.last = current


class FaderSprite(AxisSprite):
    def __init__(self, name):
        super(FaderSprite, self).__init__(name)

        self.sign = 1
        self.threshold = 1
        self.rate = 1

    def set_rate(self, rate):
        self.rate = rate

    def set_threshold(self, t):
        self.threshold = t

    def update_meter(self):
        axis, sign = self.axis, self.sign
        rate, threshold = self.rate, self.threshold

        if self.device:
            x, y = self.device.get_value()
            value = {"x": x, "y": y}[axis]

            if abs(value) >= threshold:
                value *= sign
                value *= rate * (abs(value) / threshold)

                if value > 0:
                    self.handle_event("meter_up")

                if value < 0:
                    self.handle_event("meter_down")

                self.meter.value += value
                # print("\t\t VALUE CHANGE", value)
                # print("\t\t", self.device.get_value())

    # def update_meter_events(self):
    #     # print(self.device.get_value())
    #     last, current = self.last, int(self.meter.value)
    #     super(FaderSprite, self).update_meter_events()
    #
    #     if last > current:
    #         # print("handling meter down")
    #         self.handle_event("meter_down")
    #
    #     if last < current:
    #         # print("handling meter up")
    #         self.handle_event("meter_up")
