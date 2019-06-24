import json

import constants as con
from game import Game, Screen


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
            con.CONTEXT: self
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
        if con.JSON not in file_name:
            file_name += con.JSON

        with open(file_name, "r") as file:
            data = json.load(file)

            return data

    def load_environment(self, file_name):
        data = self.load_json(file_name)

        self.populate(data)

    def populate(self, data):
        layers = data[con.LAYERS]
        sprites = data[con.SPRITES]

        entries = layers + sprites

        for e in entries:
            name = e[con.NAME]
            cls_name = e[con.CLASS]

            entity = self.model[cls_name](name)
            self.model[name] = entity

        self.set_attributes(*entries)

    def set_attributes(self, *entries):
        for e in entries:
            entity = self.model[e[con.NAME]]

            for attr in e:
                set_attr = con.SET_ + attr

                if hasattr(entity, set_attr):
                    value = e[attr]

                    if type(value) is list:
                        args = value
                    else:
                        args = [value]

                    if attr in (con.GROUP, con.GROUPS):
                        for g in args:
                            if g not in self.model:
                                self.model[g] = Group(g)

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
        game = Game(Screen(size), self.get_value(con.ENV))
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
    def __init__(self, name):
        self.name = name
        self.sprites = []
