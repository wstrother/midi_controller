from context import Context
from entities import Layer
from sprites import TextSprite, RectSprite, ButtonSprite, LatchSprite, MeterSprite, FaderSprite
from interfaces import UiInterface, ControllerInterface, MidiInterface
import pygame

pygame.init()


if __name__ == "__main__":
    con = Context([
        Layer,
        TextSprite,
        RectSprite,
        ButtonSprite,
        LatchSprite,
        MeterSprite,
        FaderSprite
    ], [
        UiInterface,
        ControllerInterface,
        MidiInterface
    ])
    con.populate({
        "layers": [
            {
                "name": "environment",
                "class": "Layer",
                "groups": "sprite_group",
                "ControllerInterface": {
                    "load_controllers": ["64_controller", "rockband_controller"]
                },
                "MidiInterface": {
                    "load_midi_controllers": ["64_a"]
                }
            }
        ],

        "sprites": [
            {
                "name": "test sprite",
                "class": "TextSprite",
                "group": "sprite_group",
                "UiInterface": {
                    "set_text": [
                        "Hello",
                        [255, 255, 255],
                        [20, "Verdana", True]
                    ]
                }
            }
        ]
    })
    con.start((800, 600))
