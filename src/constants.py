# context keys
CONTEXT = "context"
LAYERS = "layers"
SPRITES = "sprites"
NAME = "name"
CLASS = "class"
SET_ = "set_"
GROUP, GROUPS = "group", "groups"
JSON = ".json"
SIZE = "size"
CONTROLLERS = "controllers"
ENV = "environment"


# event keys
EVENT_NAME = "name"
EVENT_TRIGGER = "trigger"
EVENT_TARGET = "target"
EVENT_RESPONSE = "response"
ON_ = "on_"

# midi
PORT = "midi_port"
MIDI = "midi"
NOTE_NAMES = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
]
MIDI_CC_MAX = 127

# pygame
PYGAME_RECT = "rect"
PYGAME_LINE = "line"
PYGAME_CIRCLE = "circle"

# controller / inputs
STICK_DEAD_ZONE = 0.5
AXIS_MIN = 0.9

BUTTON_MAP = "button_map_button"
BUTTON_MAP_KEY = "button_map_key"
BUTTON_MAP_HAT = "button_map_hat"
BUTTON_MAP_AXIS = "button_map_axis"
AXIS_MAP = "axis_map"

K_ = "K_"
AXIS = "axis"
SIGN = "sign"
POSITION = "position"
DIAGONAL = "diagonal"
ID_NUM = "id_num"
MAP_TYPE = "map_type"
JOY_DEVICE = "joy_device"

# GUI
TEXT_KEY = "text_color"
FONT_KEY = "font"
TEXT_COLOR = 255, 255, 255
FONT = 12, "Verdana", True

BUTTON_COLOR = 0, 0, 255
PC_BUTTON_COLOR = 0, 255, 255
BUTTON_RADIUS = 20

METER_SIZE = 100, 20
FILL_COLOR = 0, 255, 0
EMPTY_COLOR = 0, 125, 0

# MIDI interface
DEFAULTS = "defaults"
CONTROLLER_NAME = "controller_name"
STATUS = "status"
CHANNEL = "channel"
DEVICE = "device"

NOTE_COLOR_KEY = "note_color"
NOTE_R_KEY = "note_radius"
NOTE_CHANNEL = "note_channel"
NOTES = "notes"
NOTE = "note"
NOTE_ON = "note_on"
NOTE_OFF = "note_off"
NOTES_M_KEY = "note_margin"
NOTES_POS_KEY = "note_position"
NOTES_MARGIN = 75, 0
NOTES_POS = 10, 100

SPRITE_TYPE = "type"
LATCH = "latch"
BUTTON = "button"
ON = "on"
OFF = "off"

CC_COLOR_KEY = "cc_colors"
CC_SIZE_KEY = "cc_size"
CC_CHANNEL = "cc_channel"
CC_KEY = "cc"
CC_STATUS = "control_change"
CONTROL = "control"
CC_POS_KEY = "cc_position"
CC_M_KEY = "cc_margin"
CC_POS = 10, 300
CC_MARGIN = 0, 50

METER = "meter"
MTR_SIGN = "sign"
MTR_RANGE = "range"

FADER = "fader"
FADER_RATE = "fader_rate"
FADER_THRESH = "fader_threshold"
RATE = "rate"
THRESH = "threshold"

PC_COLOR_KEY = "pc_color"
PC_R_KEY = "pc_radius"
PC_CHANNEL = "pc_channel"
PC_KEY = "pc"
PC_STATUS = "program_change"
PROGRAM = "program"
PC_POS_KEY = "pc_position"
PC_M_KEY = "pc_margin"
PC_POS = 10, 200
PC_MARGIN = 75, 0

MIDI_MESSAGE = "midi_message"
BUTTON_ON = "button_on"
BUTTON_OFF = "button_off"
METER_CHANGE = "meter_change"
