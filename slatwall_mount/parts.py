#!/usr/bin/python3

from sdf import *

SLAT_PANEL_HEIGHT = 65
SLAT_GROOVE_DEPTH = 10
SLAT_LATCH_HEIGHT = 10
SLAT_LATCH_DEPTH = 5

PLATE_THICK = 6
PLATE_WIDTH = 39
PLATE_HEIGHT = SLAT_PANEL_HEIGHT + PLATE_THICK * 2

HOOK_WIDTH = 15
HOOK_FUDGE = 1.5  # Fudge factor for tension

PIN_RAD = 2.5
PIN_HEIGHT = PLATE_THICK

CONNECTOR_INLAY_SIZE = 5
CONNECTOR_TOLERANCE = 0.5

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

def create_connector_template(width, enlarge_by = 0):
    bar = box((width, CONNECTOR_INLAY_SIZE + enlarge_by, CONNECTOR_INLAY_SIZE + enlarge_by)).rotate(pi/4, X)
    
    # Add a little bump in the middle to fixate the connection.
    bar = bar | box((0.01, CONNECTOR_INLAY_SIZE + enlarge_by, CONNECTOR_INLAY_SIZE + enlarge_by)).dilate(CONNECTOR_TOLERANCE).rotate(pi/4, X)
    
    return bar & slab(z1 = CONNECTOR_INLAY_SIZE/2)

# Base platfrom with a hole and a mating pin for connecting other parts.
def create_platform_with_connectors(width):
    platform = create_platform(width)

    return platform | create_connector_template(width).translate((width/2, PLATE_HEIGHT/2, -CONNECTOR_INLAY_SIZE/2))


# Mount for Bosch 12V powertools.
def create_bosch12v_tool_holder():
    PLATE_WIDTH = 39

    # Triangular column with rounded edges, rotated.
    insert_template = equilateral_triangle().extrude(16).dilate(1).rotate(pi, Z).rotate(pi/6, X)

    # Outer shape of the tool insert.
    insert = insert_template.scale(9.75)

    # Add the outer shape of the insert to the platform (cutting the part that would stick out from behind before that).
    holder = create_platform(PLATE_WIDTH) | (insert.translate((PLATE_WIDTH/2, PLATE_HEIGHT/2, 0)) & slab(z1=1))

    # Subtract smaller insert shape to make it hollow.
    holder = holder - insert_template.scale(7).translate((PLATE_WIDTH/2, PLATE_HEIGHT/2, 0))
    
    return holder

# Vertical mount for Bosch 12V powertools.
def create_bosch12v_tool_vertical_holder():
    ledge_depth = 20

    # Triangular column with rounded edges, rotated.
    insert_template = equilateral_triangle().extrude(12).dilate(1).rotate(pi, Z).rotate(pi*2/5, X)

    # Outer shape of the tool insert.
    insert = insert_template.scale(9.75)

    # Add the outer shape of the insert to the platform (cutting the part that would stick out from behind before that).
    holder = create_platform(PLATE_WIDTH)
    holder = holder | box((PLATE_WIDTH, PLATE_THICK*2, PLATE_WIDTH)).translate((PLATE_WIDTH/2, 30, -PLATE_WIDTH/2))
    holder = holder | (insert.translate((PLATE_WIDTH/2, PLATE_HEIGHT/2, -20)) & slab(y0=30))

    # Subtract smaller insert shape to make it hollow.
    holder = holder - (insert_template.scale(7).translate((PLATE_WIDTH/2, PLATE_HEIGHT/2, -20)) & slab(z1=0))
    
    return holder

# Mount for the Bosch 12V charger.
def create_bosch12v_charger_mount():
    screw_rad = 2
    screw_head_recess_rad = 8
    screw_head_recess_depth = 4

    mount = create_platform(PLATE_WIDTH)

    screw_hole_offset = (PLATE_WIDTH/2, PLATE_HEIGHT*3/4, 0)

    # Through hole for the screw.
    mount = mount - cylinder(screw_rad).translate(screw_hole_offset)

    # Recess for the screw head.
    mount = mount - (cylinder(screw_head_recess_rad).translate(screw_hole_offset) - slab(z1=(PLATE_THICK - screw_head_recess_depth)))

    return mount

def create_bosch12v_battery_holder():
    template_scale_factor = 13.2
    base_thick = CONNECTOR_INLAY_SIZE + 2
    sleeve_height = 50

    # Triangular column with rounded edges, rotated.
    template = equilateral_triangle().extrude(10).dilate(1).rotate(pi, Z)#.rotate(pi*2/5, X)

    sleeve = template.scale(template_scale_factor) #- template.scale(template_scale_factor * 0.8)
    sleeve = sleeve & slab(z0=-sleeve_height)

    holder = sleeve.rotate(pi/6, X) & slab(z1=0)

    # Add ridges to the cutout template to create grooves in the sleeve.
    cutout = template | (rectangle(2.6).extrude(10).translate((0, -0.2, 0)))

    holder = holder - ((cutout & slab(z1 = -1)).scale(template_scale_factor * 0.8).rotate(pi/6, X) )

    # Subtract the connector template to create a female connection point to the base.
    connector_width = 100  # Can be bigger since we're subtracting it.
    holder = holder - create_connector_template(connector_width, CONNECTOR_TOLERANCE).translate((0, 0, -CONNECTOR_INLAY_SIZE/2))

    return holder



QUALITY = 25

#
# Uncomment the parts that need to be generated below.
#

# create_platform_with_connectors(PLATE_WIDTH).save('platform.stl', samples = 2**QUALITY)
# create_bosch12v_tool_holder().save('bosch12v_tool_holder.stl', samples = 2**QUALITY)
# create_bosch12v_tool_vertical_holder().save('bosch12v_tool_vertical_holder.stl', samples = 2**QUALITY)
# create_bosch12v_charger_mount().save('bosch12v_charger_mount.stl', samples = 2**QUALITY)
# create_bosch12v_battery_holder().save('bosch12v_battery_holder.stl', samples = 2**QUALITY)