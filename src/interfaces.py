from context import AppInterface
from inputs import InputMapper
from controller import Controller
from sprites import ButtonSprite, LatchSprite, MeterSprite, FaderSprite, TextSprite
from os.path import join
import constants as con


class UiInterface(AppInterface):
    @staticmethod
    def set_text(sprite, text, color, font):
        sprite.set_text(text)
        sprite.set_color(*color)
        sprite.set_font(*font)
        sprite.set_graphics()

    @staticmethod
    def set_rect_graphics(sprite, color, size):
        sprite.set_size(*size)
        sprite.set_color(*color)
        sprite.set_graphics()

    @staticmethod
    def set_button_graphics(sprite, color, radius):
        sprite.set_color(*color)
        sprite.set_radius(radius)
        sprite.set_graphics()

    @staticmethod
    def set_meter_graphics(sprite, colors, size):
        sprite.set_colors(*colors)
        sprite.set_size(*size)
        sprite.set_graphics()

    @staticmethod
    def arrange_sprites(sprites, position, margin):
        x, y = position
        mx, my = margin

        for sprite in sprites:
            sprite.set_position(x, y)
            x += mx
            y += my

    def label_sprites(self, sprites, color, font):
        for sprite in sprites:
            name = sprite.name
            label = TextSprite("Label for {}".format(name))
            self.set_text(
                label, name, color, font
            )
            label.set_group(sprite.group)
            w, h = label.size
            x, y = sprite.position
            label.set_position(x, y - h)


class ControllerInterface(AppInterface):
    def load_controllers(self, layer, *names):
        controllers = []
        im = InputMapper()

        for name in names:
            data = self.context.load_json(
                join(con.CONTROLLERS, name)
            )
            controllers.append(
                Controller.load_controller(name, data, im)
            )

        layer.set_controllers(*controllers)


class MidiInterface(UiInterface):
    def load_midi_controllers(self, layer, *names):
        for name in names:
            data = self.context.load_json(join(con.MIDI, name))
            data = self.get_defaults(data)

            self.add_midi_hud(layer, data)

    @staticmethod
    def get_note_name(value):
        octave = value // 12

        return "{} {}".format(
            con.NOTE_NAMES[value % 12],
            octave
        )

    def get_defaults(self, data):
        try:
            defaults = self.context.load_json(con.DEFAULTS)
        except FileNotFoundError:
            return data

        for key in defaults:
            if key not in data:
                data[key] = defaults[key]

        return data

    def add_midi_hud(self, layer, data):
        group = layer.groups[-1]
        controller = layer.get_controller(data[con.CONTROLLER_NAME])
        c_index = layer.controllers.index(controller)

        note_sprites = []
        cc_sprites = []
        pc_sprites = []

        self.add_midi_notes(layer, data, note_sprites)
        self.add_midi_cc(layer, data, cc_sprites)
        self.add_midi_pc(layer, data, pc_sprites)

        for sprite in note_sprites + cc_sprites + pc_sprites:
            sprite.set_group(group)
            sprite.set_controller(layer, c_index)

        self.set_midi_graphics(
            note_sprites, self.set_button_graphics,
            [data.get(con.NOTE_COLOR_KEY, con.BUTTON_COLOR),
             data.get(con.NOTE_R_KEY, con.BUTTON_RADIUS)],
            data.get(con.NOTES_POS_KEY, con.NOTES_POS),
            data.get(con.NOTES_M_KEY, con.NOTES_MARGIN)
        )

        self.set_midi_graphics(
            cc_sprites, self.set_meter_graphics,
            [data.get(con.CC_COLOR_KEY, [con.FILL_COLOR, con.EMPTY_COLOR]),
             data.get(con.CC_SIZE_KEY, con.METER_SIZE)],
            data.get(con.CC_POS_KEY, con.CC_POS),
            data.get(con.CC_M_KEY, con.CC_MARGIN)
        )

        self.set_midi_graphics(
            pc_sprites, self.set_button_graphics,
            [data.get(con.PC_COLOR_KEY, con.PC_BUTTON_COLOR),
             data.get(con.PC_R_KEY, con.BUTTON_RADIUS)],
            data.get(con.PC_POS_KEY, con.PC_POS),
            data.get(con.PC_M_KEY, con.PC_MARGIN)
        )

        self.label_sprites(
            note_sprites + cc_sprites + pc_sprites,
            data.get(con.TEXT_KEY, con.TEXT_COLOR),
            data.get(con.FONT_KEY, con.FONT)
        )

    def set_midi_graphics(self, sprites, method, args, position, margin):
        for sprite in sprites:
            method(
                sprite, *args
            )

        self.arrange_sprites(sprites, position, margin)

    def add_midi_pc(self, layer, data, sprites):
        for pc in data[con.PC_KEY]:
            d = data[con.PC_KEY][pc]
            if type(d) is int:
                d = {con.PROGRAM: d}

            button_type = d.get(con.SPRITE_TYPE, con.BUTTON)
            if con.PROGRAM not in d:
                d[con.PROGRAM] = "{}/{}".format(d[con.ON], d[con.OFF])
            name = "PC {}".format(d[con.PROGRAM])

            if button_type == con.LATCH:
                sprite = LatchSprite(name)
                on_d = {
                    con.PROGRAM: d[con.ON],
                    con.CHANNEL: d.get(con.CHANNEL, data.get(con.PC_CHANNEL, 0))
                }
                off_d = {
                    con.PROGRAM: d[con.OFF],
                    con.CHANNEL: d.get(con.CHANNEL, data.get(con.PC_CHANNEL, 0))
                }

                self.add_pc_listener(
                    sprite, layer, on_d, off_d
                )

            else:
                sprite = ButtonSprite(name)
                if con.CHANNEL not in d and con.PC_CHANNEL in data:
                    d[con.CHANNEL] = data[con.PC_CHANNEL]

                self.add_pc_listener(
                    sprite, layer, d
                )

            sprite.set_device_name(pc)
            sprites.append(sprite)

    def add_midi_cc(self, layer, data, sprites):
        for cc in data[con.CC_KEY]:
            meter_type = cc.get(con.SPRITE_TYPE, con.METER)
            name = "CC {}".format(cc[con.CONTROL])

            if meter_type == con.FADER:
                sprite = FaderSprite(name)

                rate = cc.get(con.RATE, data.get(con.FADER_RATE, False))
                if rate:
                    sprite.set_rate(rate)

                threshold = cc.get(con.THRESH, data.get(con.FADER_THRESH, False))
                if threshold:
                    sprite.set_threshold(threshold)

            else:
                sprite = MeterSprite(name)

                sign = cc.get(con.MTR_SIGN, False)
                if sign:
                    sprite.set_sign(sign)

                r = cc.get(con.MTR_RANGE, False)
                if r:
                    sprite.set_range(r)

            d = {
                con.CONTROL: cc[con.CONTROL],
                con.CHANNEL: cc.get(con.CHANNEL, data.get(con.CC_CHANNEL, 0))
            }
            self.add_cc_listener(
                sprite, layer, d
            )

            sprite.set_device_name(cc[con.DEVICE])
            sprites.append(sprite)

    def add_midi_notes(self, layer, data, sprites):
        for note in data[con.NOTES]:
            d = data[con.NOTES][note]
            if type(d) is int:
                d = {con.NOTE: d}
            if con.CHANNEL not in d and con.NOTE_CHANNEL in data:
                d[con.CHANNEL] = data[con.NOTE_CHANNEL]

            sprite = ButtonSprite(self.get_note_name(d[con.NOTE]))

            self.add_note_listener(sprite, layer, d)

            sprite.set_device_name(note)
            sprites.append(sprite)

    @staticmethod
    def add_cc_listener(sprite, layer, data):
        listener = {
            con.EVENT_NAME: con.METER_CHANGE,
            con.EVENT_TARGET: layer,
            con.EVENT_RESPONSE: {
                con.EVENT_NAME: con.MIDI_MESSAGE,
                con.STATUS: con.CC_STATUS
            }
        }
        listener[con.EVENT_RESPONSE].update(data)
        sprite.listeners.append(listener)

    @staticmethod
    def add_pc_listener(sprite, layer, on_data, off_data=None):
        button_on = {
            con.EVENT_NAME: con.BUTTON_ON,
            con.EVENT_TARGET: layer,
            con.EVENT_RESPONSE: {
                con.EVENT_NAME: con.MIDI_MESSAGE,
                con.STATUS: con.PC_STATUS
            }
        }
        button_on[con.EVENT_RESPONSE].update(on_data)
        sprite.listeners.append(button_on)

        if off_data:
            button_off = {
                con.EVENT_NAME: con.BUTTON_OFF,
                con.EVENT_TARGET: layer,
                con.EVENT_RESPONSE: {
                    con.EVENT_NAME: con.MIDI_MESSAGE,
                    con.STATUS: con.PC_STATUS
                }
            }
            button_off[con.EVENT_RESPONSE].update(off_data)
            sprite.listeners.append(button_off)

    @staticmethod
    def add_note_listener(sprite, layer, data):
        note_on = {
            con.EVENT_NAME: con.BUTTON_ON,
            con.EVENT_TARGET: layer,
            con.EVENT_RESPONSE: {
                con.EVENT_NAME: con.MIDI_MESSAGE,
                con.STATUS: con.NOTE_ON,
            }
        }
        note_on[con.EVENT_RESPONSE].update(data)

        note_off = {
            con.EVENT_NAME: con.BUTTON_OFF,
            con.EVENT_TARGET: layer,
            con.EVENT_RESPONSE: {
                con.EVENT_NAME: con.MIDI_MESSAGE,
                con.STATUS: con.NOTE_OFF,
            }
        }
        note_off[con.EVENT_RESPONSE].update(data)

        sprite.listeners += [note_on, note_off]

