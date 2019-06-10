from zsquirrel.ui.hud_interface import HudInterface
from app.sprites.hud_sprites import ButtonSprite, AxisSprite, FaderSprite


class MidiHudInterface(HudInterface):
    def __init__(self, *args):
        super(MidiHudInterface, self).__init__(*args)

        self.init_order += [
            self.add_midi_huds.__name__,
            self.set_hud_listeners.__name__
        ]

    def set_midi_interface(self, layer, file_name, index):
        controller = self.get_value("environment").controllers[index]
        data = self.context.load_resource(file_name)

        layer.message_dict = data
        layer.target_controller = controller

    def set_hud_listeners(self, layer, file_name):
        data = self.context.load_resource(file_name)

        for name in data:
            sprite = self.get_value(name)
            listeners = data[name]

            prefix = ""

            if isinstance(sprite, ButtonSprite):
                prefix = "button_"

            if isinstance(sprite, AxisSprite):
                prefix = "meter_"

            for event in listeners:
                response = listeners[event]
                response["name"] = "midi_message"
                self.add_hud_listener(
                    sprite, layer,
                    prefix + event,
                    response.copy())

    @staticmethod
    def add_hud_listener(sprite, layer, name, response):
        print(sprite)
        sprite.add_listener({
            "name": name,
            "target": layer,
            "response": response
        })

    def add_midi_huds(self, layer, *huds):
        for hud in huds:
            self.set_hud_items(layer, *hud)

    def set_hud_items(self, layer, position, index, margin, width, *sprites):
        x, y = position

        last_w = 0
        last_h = 0

        for sprite in sprites:
            hud = self.get_item_as_sprite([sprite.name, sprite])
            hud.set_group(layer.groups[0])
            sprite.set_controller(layer, index)

            self.set_container_image(hud)

            x += (last_w + margin)
            if (x + hud.size[0]) > width + position[0]:
                x = position[0]
                y += (last_h + margin)

            hud.set_position(x, y)
            last_w = hud.size[0]
            last_h = max(last_h, hud.size[1])

    @staticmethod
    def set_device(sprite, device_name, *args):
        if isinstance(sprite, AxisSprite):
            axis, sign = args[0], 0
            if len(args) > 1:
                sign = args[1]
            sprite.set_axis(axis)
            sprite.set_sign(sign)

            if len(args) > 2:
                threshold = 1
                rate = args[2]

                if len(args) == 4:
                    threshold = args[3]

                if isinstance(sprite, FaderSprite):
                    sprite.set_rate(rate)
                    sprite.set_threshold(threshold)

            sprite.set_device_name(device_name)

        if isinstance(sprite, ButtonSprite):
            if args:
                sprite.set_dpad_direction(args[0])

            sprite.set_device_name(device_name)

