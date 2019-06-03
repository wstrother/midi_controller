from zsquirrel.entities import Layer
from zsquirrel.control.controllers import Trigger, Button
import mido

LOOP_BE1 = "LoopBe Internal MIDI 1"


class MidiLayer(Layer):
    def __init__(self, name):
        super(MidiLayer, self).__init__(name)

        self.port = mido.open_output(LOOP_BE1)
        self.message_dict = {}
        self.target_controller = None

        self.update_methods += [
            self.update_midi
        ]

    def send_message(self, **args):
        status = args.pop("status")
        message = mido.messages.Message(status, **args)
        self.port.send(message)
        print(message)

    def handle_button_midi(self, button):
        if button.last != button.get_value():
            data = self.message_dict[button.name]
            if button.held:
                self.send_message(**data["on"])

            else:
                self.send_message(**data["off"])

    def handle_axis_midi(self, axis):
        if axis.last != axis.get_value():
            data = self.message_dict[axis.name]
            value = (axis.get_value() + 1) / 2
            data["value"] = int((value * 127) // 1)

            self.send_message(**data)

    def update_midi(self):
        controller = self.target_controller
        if controller:
            devices = [d for d in controller.devices if d.name in self.message_dict]

            for d in devices:
                if type(d) is Button:
                    self.handle_button_midi(d)

                if type(d) is Trigger:
                    self.handle_axis_midi(d)
