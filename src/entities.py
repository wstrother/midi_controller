import mido
import constants as con


class Entity:
    def __init__(self, name):
        self.name = name
        self.listeners = []

        self.update_methods = []

    def handle_event(self, event):
        if type(event) is str:
            event = {con.EVENT_NAME: event}

        # print("{} handled {}".format(
        #     self.name, event[EVENT_NAME]
        # ))

        self.do_event_method(event)
        self.check_listeners(event)

    def check_listeners(self, event):
        for l in self.listeners:
            if l[con.EVENT_NAME] == event[con.EVENT_NAME]:
                target = l[con.EVENT_TARGET]
                response = l[con.EVENT_RESPONSE]
                response[con.EVENT_TRIGGER] = event

                target.handle_event(response)

    def do_event_method(self, event):
        m = getattr(self, con.ON_ + event[con.EVENT_NAME], None)

        if m:
            m(event)

    def update(self):
        for m in self.update_methods:
            m()


class Layer(Entity):
    def __init__(self, name):
        super(Layer, self).__init__(name)

        self.groups = []
        self.controllers = []
        self.port = None

        self.update_methods += [
            self.update_controllers,
            self.update_sprites
        ]

    def send_message(self, **args):
        if self.port:
            status = args.pop("status")
            message = mido.messages.Message(status, **args)
            self.port.send(message)
            print(message)

    def set_midi_port(self, name):
        self.port = mido.open_output(name)

    def set_groups(self, *groups):
        for g in groups:
            self.groups.append(g)

    def set_controllers(self, *controllers):
        for c in controllers:
            self.controllers.append(c)

    def get_controller(self, name):
        for c in self.controllers:
            if c.name == name:
                return c

    def get_sprites(self):
        sprites = []

        for g in self.groups:
            sprites += g.sprites

        return sprites

    def get_graphics(self):
        args = []

        for sprite in self.get_sprites():
            args += sprite.get_graphics()

        return args

    def update_sprites(self):
        for sprite in self.get_sprites():
            sprite.update()

    def update_controllers(self):
        for c in self.controllers:
            c.update()

    def on_midi_message(self, event):
        trigger = event["trigger"]

        keys = "name", "trigger"
        msg = {
            k: event[k] for k in event if k not in keys
        }
        msg.update({
            k: trigger[k] for k in trigger if k not in keys
        })

        self.send_message(**msg)


class Sprite(Entity):
    def __init__(self, name):
        super(Sprite, self).__init__(name)

        self.size = 0, 0
        self.position = 0, 0

        self.group = None
        self.graphics = None
        self._controller = None

    @property
    def controller(self):
        layer, index = self._controller

        return layer.controllers[index]

    def move(self, dx, dy):
        x, y = self.position
        x += dx
        y += dy
        self.set_position(dx, dy)

    def set_position(self, x, y):
        self.position = x, y

    def set_size(self, w, h):
        self.size = w, h

    def set_group(self, group):
        self.group = group
        group.sprites.append(self)

    def set_controller(self, layer, index):
        self._controller = layer, index

    def get_graphics(self):
        if self.graphics:
            return self.graphics.get_args()

        else:
            return []
