from zsquirrel.ui.hud_interface import HudInterface
from app.sprites.hud_sprites import ButtonSprite, AxisSprite, FaderSprite


class MidiHudInterface(HudInterface):
    def set_midi_interface(self, layer, file_name, index):
        controller = self.get_value("environment").controllers[index]
        data = self.context.load_resource(file_name)

        layer.message_dict = data
        layer.target_controller = controller

    def set_hud_items(self, layer, index, margin, width, *sprites):
        x, y = 0, 0

        last_w = 0
        last_h = 0

        for sprite in sprites:
            hud = self.get_item_as_sprite([sprite.name, sprite])
            hud.set_group(layer.groups[0])
            sprite.set_controller(layer, index)

            self.set_container_image(hud)

            x += (last_w + margin)
            if (x + hud.size[0]) > width:
                x = 0
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

