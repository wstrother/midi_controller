from context import AppInterface
from inputs import CONTROLLERS, InputMapper
from entities import EVENT_NAME, EVENT_TRIGGER, EVENT_RESPONSE, EVENT_TARGET
from controller import Controller
from sprites import ButtonSprite, LatchSprite, MeterSprite, FaderSprite
from os.path import join

TEXT_COLOR = 255, 255, 255
FONT = 20, "Verdana", True

BUTTON_COLOR = 0, 0, 255
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

CC_CHANNEL = "cc_channel"
CC_KEY = "cc"
CC_STATUS = "control_change"
CONTROL = "control"
METER_TYPE = "type"
METER = "meter"
FADER = "fader"
FADER_RATE = "fader_rate"

PC_CHANNEL = "pc_channel"
PC_KEY = "pc"
PC_STATUS = "program_change"
PC_LATCH = "pc"
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

    def add_midi_cc(self, layer, c_index, group, data, position, margin):
        x, y = position
        mx, my = margin

        for cc in data[CC_KEY]:
            meter_type = cc.get(METER_TYPE, METER)
            name = "CC sprite {}".format(cc[CONTROL])

            if meter_type == FADER:
                sprite = FaderSprite(name)
            else:
                sprite = MeterSprite(name)

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

