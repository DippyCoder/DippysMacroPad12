import board

from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.extensions.led import LED
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.keys import KC, make_key
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.layers import Layers
from kmk.modules.macros import Macros, Press, Release, Tap, Delay
from kmk.scanners import DiodeOrientation

keyboard = KMKKeyboard()

# --- Macros Setup ---
macros = Macros()
keyboard.modules.append(macros)

# --- Display Setup ---
keyboard.SCL = board.D5
keyboard.SDA = board.D4

PROFILE_NAMES = ['P1', 'Undefined 2', 'Undefined 3', 'Undefined 4']
current_layer = 0

def get_profile_line():
    indicators = []
    for i in range(4):
        if i == current_layer:
            indicators.append('[P{}]'.format(i + 1))
        else:
            indicators.append(' P{} '.format(i + 1))
    return ' '.join(indicators)

display = Display(
    display=SSD1306(sda=board.D4, scl=board.D5),
    entries=[
        TextEntry(text="DMP12 V2", x=64, y=10, x_anchor='M', y_anchor='M'),
        TextEntry(text=PROFILE_NAMES[0], x=64, y=35, x_anchor='M', y_anchor='M'),
        TextEntry(text=get_profile_line(), x=64, y=55, x_anchor='M', y_anchor='M'),
    ],
    height=64,
)
keyboard.extensions.append(display)

# --- LED & RGB Setup ---
led = LED(led_pin=[board.D0], brightness=100, animation_mode=AnimationModes.BREATHING, animation_speed=0.4)
keyboard.extensions.append(led)

underglow = RGB(
    pixel_pin=board.D10,
    num_pixels=15,
    val_limit=100,
    val_default=100,
    default_color=(128, 0, 128),
    animation_mode=AnimationModes.BREATHING,
    animation_speed=1,
)
keyboard.extensions.append(underglow)

frontglow = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    default_color=(128, 0, 128),
    animation_mode=AnimationModes.STATIC,
)
keyboard.extensions.append(frontglow)

# --- Modules ---
layers_ext = Layers()
keyboard.modules.append(layers_ext)

media_keys = MediaKeys()
keyboard.extensions.append(media_keys)

# --- Hardware Pins ---
keyboard.col_pins = (board.D6, board.D8, board.D9)
keyboard.row_pins = (board.D7, board.D3, board.D2, board.D1)
keyboard.diode_orientation = DiodeOrientation.ROW2COL

media_keys = MediaKeys()
keyboard.extensions.append(media_keys)

def update_display():
    display.entries[1] = TextEntry(text=PROFILE_NAMES[current_layer], x=64, y=35, x_anchor='M', y_anchor='M')
    display.entries[2] = TextEntry(text=get_profile_line(), x=64, y=55, x_anchor='M', y_anchor='M')

def prev_profile(key, keyboard, *args):
    global current_layer
    current_layer = (current_layer - 1) % 4
    keyboard.active_layers = [current_layer]
    update_display()

def next_profile(key, keyboard, *args):
    global current_layer
    current_layer = (current_layer + 1) % 4
    keyboard.active_layers = [current_layer]
    update_display()

def to_profile_0(key, keyboard, *args):
    global current_layer
    current_layer = 0
    keyboard.active_layers = [current_layer]
    update_display()

PREV = make_key(names=('PREV',), on_press=prev_profile)
NEXT = make_key(names=('NEXT',), on_press=next_profile)
TO_0 = make_key(names=('TO_0',), on_press=to_profile_0)

keyboard.keymap = [
    # Profile 1: Test1
    [
        KC.A, KC.B, KC.C,
        KC.D, KC.E, KC.F,
        KC.G, KC.H, KC.I,
        PREV, TO_0, NEXT,
    ],
    # Profile 2: Undefined 1
    [
        KC.NONE, KC.NONE, KC.NONE,
        KC.NONE, KC.NONE, KC.NONE,
        KC.NONE, KC.NONE, KC.NONE,
        PREV, TO_0, NEXT,
    ],
    # Profile 3: Undefined 2
    [
        KC.NONE, KC.NONE, KC.NONE,
        KC.NONE, KC.NONE, KC.NONE,
        KC.NONE, KC.NONE, KC.NONE,
        PREV, TO_0, NEXT,
    ],
    # Profile 4: Undefined 3
    [
        KC.NONE, KC.NONE, KC.NONE,
        KC.NONE, KC.NONE, KC.NONE,
        KC.NONE, KC.NONE, KC.NONE,
        PREV, TO_0, NEXT,
    ],
]

if __name__ == '__main__':
    keyboard.go()