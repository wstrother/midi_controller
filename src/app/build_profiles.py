import pygame
import json
from sys import argv

pygame.init()


def get_profile_device(name, cls, mapping):
    return {
        "name": name,
        "class": cls,
        "mapping": mapping
    }


def get_axis_event(num):
    return {
        "status": "control_change", "control": num
    }


def get_button_event(num):
    return {
        "on": {"status": "note_on", "note": 60 + num},
        "off": {"status": "note_off", "note": 60 + num}
    }


def get_axis_mapping(joy_name, axis_num, joy_num):
    return ["axis_map", axis_num, joy_name, joy_num, 1]


def get_button_mapping(joy_name, button_num, joy_num):
    return ["button_map_button", button_num, joy_name, joy_num]


def build_profile(joystick):
    devices = []
    midi = {}
    joy_name = joystick.get_name()
    joy_id = joystick.get_id()

    def add_device(n, c, m):
        devices.append(get_profile_device(
            n, c, m
        ))

    for i in range(joystick.get_numaxes()):
        d_name = "Axis {}".format(i)
        add_device(
            d_name,
            "trigger",
            get_axis_mapping(joy_name, i, joy_id)
        )

        midi[d_name] = get_axis_event(i)

    for i in range(joystick.get_numbuttons()):
        d_name = "Button {}".format(i)
        add_device(
            d_name,
            "button",
            get_button_mapping(joy_name, i, joy_id)
        )

        midi[d_name] = get_button_event(i)

    return devices, midi


if __name__ == "__main__":
    if len(argv) > 1:
        controller_name = argv[1]
    else:
        controller_name = "new"

    for j in range(pygame.joystick.get_count()):
        m_file = open(controller_name + "_midi.json", "w")
        c_file = open(controller_name + "_controller.json", "w")

        joy = pygame.joystick.Joystick(j)
        joy.init()

        c, m = build_profile(joy)
        print(
            json.dumps(c, indent=2)
        )
        json.dump(c, c_file, indent=2)
        json.dump(m, m_file, indent=2)

        c_file.close()
        m_file.close()
