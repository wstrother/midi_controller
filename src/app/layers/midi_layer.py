from zsquirrel.entities import Layer
import mido

LOOP_BE1 = "LoopBe Internal MIDI 1"


class MidiLayer(Layer):
    def __init__(self, name):
        super(MidiLayer, self).__init__(name)

        self.port = mido.open_output(LOOP_BE1)

    def send_message(self, **args):
        status = args.pop("status")
        message = mido.messages.Message(status, **args)
        self.port.send(message)
        print(message)

    def on_midi_message(self):
        event = self.event
        trigger = event["trigger"]

        keys = "name", "trigger", "timer", "duration", "lerp"
        msg = {
            k: event[k] for k in event if k not in keys
        }
        msg.update({
            k: trigger[k] for k in trigger if k not in keys
        })

        self.send_message(**msg)
