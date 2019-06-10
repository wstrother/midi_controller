# import mido
# from sys import argv
# import pygame

from zsquirrel.context import Context
from zsquirrel.game import Game
from zsquirrel.entities import Layer, Sprite
from zsquirrel.control.controller_interface import ControllerInterface
from app.interfaces.midi_hud_interface import MidiHudInterface
from app.layers.midi_layer import MidiLayer
from app.sprites.hud_sprites import AxisSprite, FaderSprite, ButtonSprite, LatchSprite
from app.pygame_screen import PygameScreen


SCREEN_SIZE = 800, 600

if __name__ == "__main__":
    # pygame.init()

    entities = [
        Layer,
        MidiLayer,
        Sprite,
        AxisSprite,
        ButtonSprite,
        LatchSprite,
        FaderSprite
    ]
    interfaces = [
        ControllerInterface,
        MidiHudInterface
    ]

    c = Context.get_default_context(
        Game(
            screen=PygameScreen(SCREEN_SIZE)
            # clock=pygame.time.Clock(),
            # frame_rate=60
        ),
        entities,
        interfaces
    )
    c.load_environment("main_menu.json")
    c.run_game()


# LOOP_BE1 = "LoopBe Internal MIDI 1"
#
# message = mido.Message
# print(mido.get_output_names())
#
# if __name__ == "__main__":
#     if len(argv) > 1:
#         device_name = " ".join(argv[1:])
#     else:
#         device_name = LOOP_BE1
#
#     with mido.open_output(device_name) as port:
#         while True:
#             arg = input("")
#             if arg != "e":
#                 port.send(
#                     message('note_on', note=60)
#                 )
#             else:
#                 port.send(
#                     message('note_off', note=60)
#                 )
