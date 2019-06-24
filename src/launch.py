from context import Context
from entities import Layer
from sprites import TextSprite, ButtonSprite, LatchSprite, MeterSprite, FaderSprite
from interfaces import UiInterface, ControllerInterface, MidiInterface
from sys import argv
import constants as con
import pygame

pygame.init()


if __name__ == "__main__":
    context = Context([
        Layer,
        TextSprite,
        ButtonSprite,
        LatchSprite,
        MeterSprite,
        FaderSprite
    ], [
        UiInterface,
        ControllerInterface,
        MidiInterface
    ])

    controllers, midi = [], []
    size = 0, 0
    port = None

    if len(argv) > 1:
        file_name = argv[1]
        try:
            data = context.load_json(file_name)
            controllers = data[con.CONTROLLERS]
            midi = data[con.MIDI]
            size = data[con.SIZE]
            port = data[con.PORT]

        except KeyError as e:
            print(e)
            print("\n\nBad JSON file")
            print("Please include '{}', '{}', '{}', and '{}' keys".format(
                con.CONTROLLERS, con.MIDI, con.SIZE, con.PORT
            ))
            exit()
        except FileNotFoundError as e:
            print(e)
            print("\n\nNo such JSON file")
            exit()

    else:
        print("Please provide file_name")
        exit()

    context.populate({
        con.LAYERS: [
            {
                con.NAME: con.ENV,
                con.CLASS: Layer.__name__,
                con.GROUPS: "Sprite Group",
                con.PORT: port,

                ControllerInterface.__name__: {
                    ControllerInterface.load_controllers.__name__: controllers
                },

                MidiInterface.__name__: {
                    MidiInterface.load_midi_controllers.__name__: midi
                }
            }
        ],

        con.SPRITES: []
    })

    context.start(size)
