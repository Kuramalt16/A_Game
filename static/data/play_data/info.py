
SELECTED_CHARACTER = ""

DATA = {}

TICK = 50

FAST = 0

SPAWN_POINT = [330, 1]

ENTRY_POS = [510, 370]
# START_POS = (141, 70)
CURRENT_STANCE = 0
LAST_ORIENT = ["Front.png", "_Walk.png", "_Walk1.png"]

HARVESTABLE = {}
ENTERABLE = [] # Place holder for places that can be entered

BACKPACK_CONTENT = {}
BACKPACK_COORDINATES_X = {}
BACKPACK_COORDINATES_Y = {}

SPELLBOOK_CONTENT = {}
SPELLBOOK_COORDINATES_X = {}
SPELLBOOK_COORDINATES_Y = {}

OFFSCREEN = (0, 0)

Player_rect = 0

TEXT = [] # place holder for displayable text on the screen

HARVESTED_OBJECTS = {} # Place holder for harvested decoration lists which contain rects

COMBAT_RECT = 0

CURRENT_ROOM = ""

APPLIANCE_CLICK = ""

EQUIPED = {
    "Sword": 0,
    "Axe": 0,
    "Picaxe": 0,
}

equipment = {
    (-8, 8): "Sword",
    (-6, 8): "Axe",
    (-4, 8): "Picaxe",
    (-2, 0): "Bow",
    (-2, 2): "Cape",
    (-2, 4): "",
    (-2, 6): "",
    (-2, 8): "R_Ring",
    (-10, 0): "Helmet",
    (-10, 2): "Chestplate",
    (-10, 4): "Leggings",
    (-10, 6): "Boots",
    (-10, 8): "L_Ring",
}

Temp_variable_holder = []