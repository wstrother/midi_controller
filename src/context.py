import json
from game import Game, Screen

CONTEXT = "context"
LAYERS = "layers"
SPRITES = "sprites"
NAME = "name"
CLASS = "class"
SET_ = "set_"
GROUP, GROUPS = "group", "groups"


class Context:
    def __init__(self, entities, interfaces):
        self.interfaces = []
        for i in interfaces:
            self.interfaces.append(i(self))

        self._class_dict = {
            e.__name__: e for e in entities
        }
        self.model = {}
        self.reset_model()

    def reset_model(self):
        self.model = {
            CONTEXT: self
        }
        self.model.update(self._class_dict)

    def get_value(self, value):
        if type(value) in (list, tuple):
            return [self.get_value(x) for x in value]

        elif type(value) is dict:
            for key in value:
                value[key] = self.get_value(key)

            return value

        else:
            return self.model.get(value, value)

    @staticmethod
    def load_json(file_name):
        if ".json" not in file_name:
            file_name += ".json"

        with open(file_name, "r") as file:
            data = json.load(file)

            return data

    def load_environment(self, file_name):
        data = self.load_json(file_name)

        self.populate(data)

    def populate(self, data):
        layers = data[LAYERS]
        sprites = data[SPRITES]

        entries = layers + sprites

        for e in entries:
            name = e[NAME]
            cls_name = e[CLASS]

            entity = self.model[cls_name](name)
            self.model[name] = entity

        self.set_attributes(*entries)

    def set_attributes(self, *entries):
        for e in entries:
            entity = self.model[e[NAME]]

            for attr in e:
                set_attr = SET_ + attr

                if hasattr(entity, set_attr):
                    value = e[attr]

                    if type(value) is list:
                        args = value
                    else:
                        args = [value]

                    if attr in (GROUP, GROUPS):
                        for g in args:
                            if g not in self.model:
                                self.model[g] = Group()

                    args = self.get_value(args)

                    if len(args) == 1 and args[0] is True:
                        args = []

                    getattr(entity, set_attr)(*args)

            self.apply_interfaces(entity, e)

    def apply_interfaces(self, entity, data):
        for i in self.interfaces:
            if i.name in data:
                i.apply_to_entity(entity, data[i.name])

    def start(self, size):
        game = Game(Screen(size), self.get_value("environment"))
        game.run_game()


class AppInterface:
    def __init__(self, context):
        self.name = self.__class__.__name__
        self.context = context

    def apply_to_entity(self, entity, data):
        for method_name in data:
            value = data[method_name]
            args = self.context.get_value(value)

            if args is True:
                args = []

            if type(args) is not list:
                args = [args]

            getattr(self, method_name)(entity, *args)


class Group:
    def __init__(self):
        self.sprites = []
