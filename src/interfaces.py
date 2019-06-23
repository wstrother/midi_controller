from context import AppInterface
from inputs import CONTROLLERS, InputMapper
from entities import EVENT_NAME, EVENT_TRIGGER, EVENT_RESPONSE, EVENT_TARGET
from controller import Controller
from sprites import ButtonSprite, LatchSprite, MeterSprite, FaderSprite
from os.path import join

TEXT_COLOR = 255, 255, 255
FONT = 20, "Verdana", True

BUTTON_COLOR = 0, 0, 255
PC_BUTTON_COLOR = 0, 255, 255
BUTTON_RADIUS = 20

METER_SIZE = 100, 20
FILL_COLOR = 0, 255, 0
EMPTY_COLOR = 255, 0, 0


class UiInterface(AppInterface):
    @staticmethod
    def set_text(sprite, text, color, font):
        sprite.set_text(text)
        sprite.set_color(*color)
        sprite.set_font(*font)
        sprite.set_graphics()

    @staticmethod
    def set_rect_graphics(sprite, color, size, position):
        sprite.set_size(*size)
        sprite.set_position(*position)
        sprite.set_color(*color)
        sprite.set_graphics()

    @staticmethod
    def set_button_graphics(sprite, color, radius, position):
        sprite.set_color(*color)
        sprite.set_radius(radius)
        sprite.set_position(*position)
        sprite.set_graphics()

    @staticmethod
    def set_meter_graphics(sprite, colors, size, position):
        sprite.set_colors(*colors)
        sprite.set_size(*size)
        sprite.set_position(*position)
        sprite.set_graphics()


class ControllerInterface(AppInterface):
    def load_controllers(self, layer, *names):
        controllers = []
        im = InputMapper()

        for name in names:
            data = self.context.load_json(
                join(CONTROLLERS, name)
            )
            controllers.append(
                Controller.load_controller(name, data, im)
            )

        layer.set_controllers(*controllers)


MIDI = "midi"
CONTROLLER_NAME = "controller_name"
STATUS = "status"
CHANNEL = "channel"
DEVICE = "device"

NOTE_CHANNEL = "note_channel"
NOTES = "notes"
NOTE = "note"
NOTE_ON = "note_on"
NOTE_OFF = "note_off"
SPRITE_TYPE = "type"
LATCH = "latch"
BUTTON = "button"
ON = "on"
OFF = "off"

CC_CHANNEL = "cc_channel"
CC_KEY = "cc"
CC_STATUS = "control_change"
CONTROL = "control"

METER = "meter"
SIGN = "sign"
RANGE = "range"

FADER = "fader"
FADER_RATE = "fader_rate"
FADER_THRESH = "fader_threshold"
RATE = "rate"
THRESH = "threshold"

PC_CHANNEL = "pc_channel"
PC_KEY = "pc"
PC_STATUS = "program_change"
PROGRAM = "program"

MIDI_MESSAGE = "midi_message"
BUTTON_ON = "button_on"
BUTTON_OFF = "button_off"
METER_CHANGE = "meter_change"


class MidiInterface(UiInterface):
    def load_midi_controllers(self, layer, *names):
        for name in names:
            data = self.context.load_json(join(MIDI, name))

            self.add_midi_hud(layer, data)

    def add_midi_hud(self, layer, data):
        group = layer.groups[0]
        controller = layer.get_controller(data[CONTROLLER_NAME])
        c_index = layer.controllers.index(controller)

        self.add_midi_notes(
            layer, c_index, group, data,
            (10, 100), (50, 0)
        )

        self.add_midi_cc(
            layer, c_index, group, data,
            (10, 200), (0, 25)
        )

        self.add_midi_pc(
            layer, c_index, group, data,
            (120, 200), (0, 50)
        )

    def add_midi_pc(self, layer, c_index, group, data, position, margin):
        x, y = position
        mx, my = margin

        for pc in data[PC_KEY]:
            d = data[PC_KEY][pc]
            if type(d) is int:
                d = {PROGRAM: d}

            button_type = d.get(SPRITE_TYPE, BUTTON)
            if PROGRAM not in d:
                d[PROGRAM] = "{}/{}".format(d[ON], d[OFF])
            name = "PC sprite {}".format(d[PROGRAM])

            if button_type == LATCH:
                sprite = LatchSprite(name)
                on_d = {
                    PROGRAM: d[ON],
                    CHANNEL: d.get(CHANNEL, data.get(PC_CHANNEL, 0))
                }
                off_d = {
                    PROGRAM: d[OFF],
                    CHANNEL: d.get(CHANNEL, data.get(PC_CHANNEL, 0))
                }

                self.add_pc_listener(
                    sprite, layer, on_d, off_d
                )

            else:
                sprite = ButtonSprite(name)
                if CHANNEL not in d and PC_CHANNEL in data:
                    d[CHANNEL] = data[PC_CHANNEL]

                self.add_pc_listener(
                    sprite, layer, d
                )

            sprite.set_group(group)
            sprite.set_controller(layer, c_index)
            sprite.set_device_name(pc)

            self.set_button_graphics(
                sprite, PC_BUTTON_COLOR, BUTTON_RADIUS, (x, y)
            )

            x += mx
            y += my

    def add_midi_cc(self, layer, c_index, group, data, position, margin):
        x, y = position
        mx, my = margin

        for cc in data[CC_KEY]:
            meter_type = cc.get(SPRITE_TYPE, METER)
            name = "CC sprite {}".format(cc[CONTROL])

            if meter_type == FADER:
                sprite = FaderSprite(name)

                rate = cc.get(RATE, data.get(FADER_RATE, False))
                if rate:
                    sprite.set_rate(rate)

                threshold = cc.get(THRESH, data.get(FADER_THRESH, False))
                if threshold:
                    sprite.set_threshold(threshold)

            else:
                sprite = MeterSprite(name)

                sign = cc.get(SIGN, False)
                if sign:
                    sprite.set_sign(sign)

                r = cc.get(RANGE, False)
                if r:
                    sprite.set_range(r)

            d = {
                CONTROL: cc[CONTROL],
                CHANNEL: cc.get(CHANNEL, data.get(CC_CHANNEL, 0))
            }
            self.add_cc_listener(
                sprite, layer, d
            )

            sprite.set_group(group)
            sprite.set_controller(layer, c_index)
            sprite.set_device_name(cc[DEVICE])

            self.set_meter_graphics(
                sprite, (FILL_COLOR, EMPTY_COLOR), METER_SIZE, (x, y)
            )

            x += mx
            y += my

    def add_midi_notes(self, layer, c_index, group, data, position, margin):
        x, y = position
        mx, my = margin

        for note in data[NOTES]:
            sprite = ButtonSprite(note + " button sprite")

            d = data[NOTES][note]
            if type(d) is int:
                d = {NOTE: d}
            if CHANNEL not in d and NOTE_CHANNEL in data:
                d[CHANNEL] = data[NOTE_CHANNEL]

            self.add_note_listener(sprite, layer, d)

            sprite.set_group(group)
            sprite.set_controller(layer, c_index)
            sprite.set_device_name(note)

            self.set_button_graphics(
                sprite, BUTTON_COLOR, BUTTON_RADIUS, (x, y)
            )

            x += mx
            y += my

    @staticmethod
    def add_cc_listener(sprite, layer, data):
        listener = {
            EVENT_NAME: METER_CHANGE,
            EVENT_TARGET: layer,
            EVENT_RESPONSE: {
                EVENT_NAME: MIDI_MESSAGE,
                STATUS: CC_STATUS
            }
        }
        listener[EVENT_RESPONSE].update(data)
        sprite.listeners.append(listener)

    @staticmethod
    def add_pc_listener(sprite, layer, on_data, off_data=None):
        button_on = {
            EVENT_NAME: BUTTON_ON,
            EVENT_TARGET: layer,
            EVENT_RESPONSE: {
                EVENT_NAME: MIDI_MESSAGE,
                STATUS: PC_STATUS
            }
        }
        button_on[EVENT_RESPONSE].update(on_data)
        sprite.listeners.append(button_on)

        if off_data:
            button_off = {
                EVENT_NAME: BUTTON_OFF,
                EVENT_TARGET: layer,
                EVENT_RESPONSE: {
                    EVENT_NAME: MIDI_MESSAGE,
                    STATUS: PC_STATUS
                }
            }
            button_off[EVENT_RESPONSE].update(off_data)
            sprite.listeners.append(button_off)

    @staticmethod
    def add_note_listener(sprite, layer, data):
        note_on = {
            EVENT_NAME: BUTTON_ON,
            EVENT_TARGET: layer,
            EVENT_RESPONSE: {
                EVENT_NAME: MIDI_MESSAGE,
                STATUS: NOTE_ON,
            }
        }
        note_on[EVENT_RESPONSE].update(data)

        note_off = {
            EVENT_NAME: BUTTON_OFF,
            EVENT_TARGET: layer,
            EVENT_RESPONSE: {
                EVENT_NAME: MIDI_MESSAGE,
                STATUS: NOTE_OFF,
            }
        }
        note_off[EVENT_RESPONSE].update(data)

        sprite.listeners += [note_on, note_off]

