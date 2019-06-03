from zsquirrel.ui.hud_interface import HudInterface
from zsquirrel.control.controllers import Button, Trigger
from app.sprites.hud_sprites import ButtonSprite, AxisSprite


class MidiHudInterface(HudInterface):
    def set_midi_interface(self, layer, file_name, index):
        controller = self.get_value("environment").controllers[index]
        data = self.context.load_resource(file_name)

        layer.message_dict = data
        layer.target_controller = controller

    def get_item_as_sprite(self, item):
        if type(item) is Button:
            return ButtonSprite(str(item), item)

        if type(item) is Trigger:
            return AxisSprite(str(item), item)

        return super(MidiHudInterface, self).get_item_as_sprite(item)

    def set_midi_hud(self, layer, index):
        controller = layer.controllers[index]
        group = layer.groups[0]

        y = 5

        for d in controller.devices:
            sprite = self.get_item_as_sprite(
                [d.name, d]
            )
            sprite.set_group(group)
            self.set_container_image(sprite)
            sprite.set_position(5, y + 5)
            sprite.on_change_position()
            sprite.on_change_size()

            y += 50
