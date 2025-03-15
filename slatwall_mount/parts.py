#!/usr/bin/python3

from sdf import *

SLAT_PANEL_HEIGHT = 65
SLAT_GROOVE_DEPTH = 10
SLAT_LATCH_HEIGHT = 10
SLAT_LATCH_DEPTH = 5

PLATE_THICK = 6
PLATE_WIDTH = 40
PLATE_HEIGHT = SLAT_PANEL_HEIGHT + PLATE_THICK * 2

HOOK_WIDTH = 15
HOOK_FUDGE = 1.5  # Fudge factor for tension

# Base mounting platform.
def create_platform(width):
    # Make the hook edges fully round.
    hook_smooth_rad = max(SLAT_LATCH_DEPTH/2, 0.01)

    hook_tooth = box(a=(0,0,0), b=(width, SLAT_LATCH_HEIGHT + PLATE_THICK - hook_smooth_rad * 2, SLAT_LATCH_DEPTH - hook_smooth_rad * 2)) \
        .dilate(hook_smooth_rad) \
        .translate((0, hook_smooth_rad, SLAT_GROOVE_DEPTH - SLAT_LATCH_DEPTH + hook_smooth_rad * 2 - HOOK_FUDGE))
    hook_tooth = hook_tooth & slab(x0=0, x1=width)
    hook = box(a=(0,0,0), b=(width, PLATE_THICK, SLAT_GROOVE_DEPTH - HOOK_FUDGE))
    hook |= hook_tooth

    clamp = box(a=(0,0,0), b=(width, PLATE_THICK, SLAT_GROOVE_DEPTH))
    clamp = clamp - capped_cylinder(0, X*width, SLAT_GROOVE_DEPTH/2).translate((0, PLATE_THICK*1.7, SLAT_GROOVE_DEPTH/4))
    clamp = clamp | capped_cylinder(0, X*width, SLAT_GROOVE_DEPTH/2).translate((0, PLATE_THICK*0.275, SLAT_GROOVE_DEPTH*3/4))
    clamp = clamp & slab(y0=0)
    clamp = clamp & slab(z1=SLAT_GROOVE_DEPTH)

    mount = box(a=(0, 0, 0), b=(width, PLATE_HEIGHT, PLATE_THICK))
    mount |= hook.translate((0, PLATE_HEIGHT - PLATE_THICK, PLATE_THICK))
    mount |= clamp.translate((0, 0, PLATE_THICK))

    return mount

# Mount for Bosch 12V powertools.
def create_bosch12v_tool_holder():
    platform_width = 39

    # Triangular column with rounded edges, rotated.
    insert_template = equilateral_triangle().extrude(16).dilate(1).rotate(pi, Z).rotate(pi/6, X)

    # Outer shape of the tool insert.
    insert = insert_template.scale(9.75)

    # Add the outer shape of the insert to the platform (cutting the part that would stick out from behind before that).
    holder = create_platform(platform_width) | (insert.translate((platform_width/2, PLATE_HEIGHT/2, 0)) & slab(z1=1))

    # Subtract smaller insert shape to make it hollow.
    holder = holder - insert_template.scale(7).translate((platform_width/2, PLATE_HEIGHT/2, 0))
    
    return holder

# Vertical mount for Bosch 12V powertools.
def create_bosch12v_tool_vertical_holder():
    platform_width = 39
    ledge_depth = 20

    # Triangular column with rounded edges, rotated.
    insert_template = equilateral_triangle().extrude(12).dilate(1).rotate(pi, Z).rotate(pi*2/5, X)

    # Outer shape of the tool insert.
    insert = insert_template.scale(9.75)

    # Add the outer shape of the insert to the platform (cutting the part that would stick out from behind before that).
    holder = create_platform(platform_width)
    holder = holder | box((platform_width, PLATE_THICK*2, platform_width)).translate((platform_width/2, 30, -platform_width/2))
    holder = holder | (insert.translate((platform_width/2, PLATE_HEIGHT/2, -20)) & slab(y0=30))

    # Subtract smaller insert shape to make it hollow.
    holder = holder - (insert_template.scale(7).translate((platform_width/2, PLATE_HEIGHT/2, -20)) & slab(z1=0))
    
    return holder


QUALITY = 25

#
# Uncomment the parts that need to be generated below.
#

# create_bosch12v_tool_holder().save('bosch12v_tool_holder.stl', samples = 2**QUALITY)
# create_bosch12v_tool_vertical_holder().save('bosch12v_tool_vertical_holder.stl', samples = 2**QUALITY)