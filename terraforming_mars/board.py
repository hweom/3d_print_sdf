#!/usr/bin/python3

from sdf import *

# Global parameters.
TOLERANCE = 0.3

TRAY_DEPTH = 3
TRAY_RAD = 2

CUBE_SIDE = 8.3 + TOLERANCE
CUBE_MARGIN = 1
CUBE_TEXT_HEIGHT = CUBE_SIDE * 0.6

RESOURCE_CUBES_WIDTH = (CUBE_SIDE + CUBE_MARGIN) * 6 - CUBE_MARGIN
RESOURCE_CUBES_HEIGHT = (CUBE_SIDE + CUBE_MARGIN) * 2 - CUBE_MARGIN
CREDIT_CUBES_WIDTH = (CUBE_SIDE + CUBE_MARGIN) * 6 - CUBE_MARGIN
CREDIT_CUBES_HEIGHT = (CUBE_SIDE + CUBE_MARGIN) * 3 - CUBE_MARGIN

TRAY_WIDTH = max(RESOURCE_CUBES_WIDTH, CREDIT_CUBES_WIDTH)
TRAY_HEIGHT = TRAY_WIDTH * 0.7

BOARD_MARGIN = 3
BOARD_WIDTH = TRAY_WIDTH * 3 + BOARD_MARGIN * 4
BOARD_HEIGHT = (TRAY_HEIGHT + CUBE_MARGIN + max(RESOURCE_CUBES_HEIGHT, CREDIT_CUBES_HEIGHT)) * 2 + BOARD_MARGIN * 3

ICON_WIDTH = 10
ICON_HEIGHT = 10


SYMBOL_DEPTH = 1
FONT = '/usr/share/fonts/noto/NotoSans-Regular.ttf'

BOARD_THICK = TRAY_DEPTH + SYMBOL_DEPTH + 2

# Constructs a tray template that can be used to subtract from the board.
# Returned object has upper left corner at (0, 0).
def tray(t):
    w = t['width']
    h = t['height']
    return (
        rounded_box((w, h, TRAY_DEPTH * 2), 2).translate((w/2, h/2, 0)) |
        image(t['icon'], ICON_WIDTH, ICON_HEIGHT).extrude(SYMBOL_DEPTH * 2).translate((w/2, h/2, -TRAY_DEPTH))
    )

def cube_slot(number):
    number_str = '{}'.format(number)
    w, h = measure_text(FONT, number_str)
    text_scale = CUBE_TEXT_HEIGHT / h
    return (
        box((CUBE_SIDE, CUBE_SIDE, TRAY_DEPTH * 2)) | 
        text(FONT, number_str).extrude(SYMBOL_DEPTH * 2 / text_scale).scale(text_scale).translate((0, 0, -TRAY_DEPTH))
    ).translate((CUBE_SIDE/2, CUBE_SIDE/2, 0))

def cube_slot_string(numbers):
    cubes = []
    offset = 0
    for n in numbers:
        cubes.append(cube_slot(n).translate((offset, 0, 0)))
        offset += CUBE_SIDE + CUBE_MARGIN
    return union(*cubes)

def resource_cubes():
    return (
        cube_slot_string([0, 1, 2, 3, 4, 5]).translate((0, CUBE_SIDE + CUBE_MARGIN, 0)) |
        cube_slot_string([6, 7, 8, 9, 10, 20])
    )
    
def credit_cubes():
    return (
        cube_slot_string([-6, -5, -4, -3, -2, -1]).translate((0, (CUBE_SIDE + CUBE_MARGIN) * 2, 0)) |
        cube_slot_string([0, 1, 2, 3, 4, 5]).translate((0, CUBE_SIDE + CUBE_MARGIN, 0)) |
        cube_slot_string([6, 7, 8, 9, 10, 20])
    )

QUALITY = 30

CREDITS_TRAY = {
    'name': 'credits',
    'icon': 'credits.png',
    'width': TRAY_WIDTH,
    'height': TRAY_HEIGHT,
}
IRON_TRAY = {
    'name': 'iron',
    'icon': 'iron.png',
    'width': TRAY_WIDTH,
    'height': TRAY_HEIGHT,
}
TITAN_TRAY = {
    'name': 'titan',
    'icon': 'titan.png',
    'width': TRAY_WIDTH,
    'height': TRAY_HEIGHT,
}
GREEN_TRAY = {
    'name': 'green',
    'icon': 'leaf.png',
    'width': TRAY_WIDTH,
    'height': TRAY_HEIGHT,
}
ENERGY_TRAY = {
    'name': 'energy',
    'icon': 'energy.png',
    'width': TRAY_WIDTH,
    'height': TRAY_HEIGHT,
}
HEAT_TRAY = {
    'name': 'heat',
    'icon': 'heat.png',
    'width': TRAY_WIDTH,
    'height': TRAY_HEIGHT,
}

# Board bottom left corner is at (0, 0).
board = rounded_box((BOARD_WIDTH, BOARD_HEIGHT, BOARD_THICK), 2).translate((BOARD_WIDTH/2, BOARD_HEIGHT/2, -TRAY_DEPTH))

offset = BOARD_MARGIN
for t in [CREDITS_TRAY, IRON_TRAY, TITAN_TRAY]:
    board -= tray(t).translate((offset, BOARD_HEIGHT - TRAY_HEIGHT - BOARD_MARGIN, 0))
    if t['name'] == 'credits':
        board -= credit_cubes().translate((offset, BOARD_HEIGHT - TRAY_HEIGHT - CREDIT_CUBES_HEIGHT - BOARD_MARGIN * 2, 0))
    else:
        board -= resource_cubes().translate((offset, BOARD_HEIGHT - TRAY_HEIGHT - RESOURCE_CUBES_HEIGHT - BOARD_MARGIN * 2, 0))

    offset += TRAY_WIDTH + BOARD_MARGIN

offset = BOARD_MARGIN
for t in [GREEN_TRAY, ENERGY_TRAY, HEAT_TRAY]:
    board -= tray(t).translate((offset, BOARD_MARGIN, 0))
    board -= resource_cubes().translate((offset, TRAY_HEIGHT + BOARD_MARGIN * 2, 0))

    offset += TRAY_WIDTH + BOARD_MARGIN

# Opening between energy and heat trays.
board -= rounded_box((TRAY_WIDTH/3, TRAY_WIDTH/3, TRAY_DEPTH * 2), 2).rotate(pi/4, Z).translate((TRAY_WIDTH*2 + BOARD_MARGIN, BOARD_MARGIN + TRAY_HEIGHT/2, 0))

board.save('board.stl', samples = 2**QUALITY)

# resource_cubes().save('cube.stl', samples = 2**QUALITY)