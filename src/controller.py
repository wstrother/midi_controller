from inputs import InputMapper
import json
import pygame


class Controller:
    def __init__(self, name):
        self.name = name
        self.devices = []

    def update(self):
        for d in self.devices:
            d.update()

    def add_device(self, name, mapping):
        self.devices.append(
            InputDevice(name, mapping)
        )

    def get_device(self, name):
        for d in self.devices:
            if d.name == name:
                return d

    def get_value(self, name):
        return self.get_device(name).value

    @staticmethod
    def load_controller(name, data, input_mapper):
        c = Controller(name)

        for d in data:
            mapping = input_mapper.get_from_json(d)

            c.add_device(
                d["name"], mapping
            )

        return c


class InputDevice:
    def __init__(self, name, mapping):
        self.name = name
        self.mapping = mapping
        self.value = None

    def update(self):
        self.value = self.mapping.get_value()


if __name__ == "__main__":
    file_name = input("Controller name")
    pygame.init()
    pygame.display.set_mode((800, 600))

    with open("controllers/" + file_name + ".json", "r") as file:
        controller_data = json.load(file)
        test_controller = Controller.load_controller(
            "test_controller", controller_data, InputMapper()
        )

        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            test_controller.update()
            A = test_controller.get_value("A")

            if A:
                print("A")
