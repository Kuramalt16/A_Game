
SELECTED_CHARACTER = ""

DATA = {}

TICK = 100

FAST = 1

SPAWN_POINT = [330, 1]

ENTRY_POS = [180, 370]
# START_POS = (141, 70)
CURRENT_STANCE = 0
LAST_ORIENT = ["Front.png", "_Walk.png", "_Walk1.png"]

HARVESTABLE = {}
ENTERABLE = [] # Place holder for places that can be entered

BACKPACK_CONTENT = {} # changes values in add to backpack, remove from backpack and in backpack when items are switching possisions
BACKPACK_COORDINATES_X = {}
BACKPACK_COORDINATES_Y = {}

CONTAINERS = {}

SPELLBOOK_CONTENT = {}
SPELLBOOK_COORDINATES_X = {}
SPELLBOOK_COORDINATES_Y = {}

SHOP_CONTENT = {}
SHOP_COORDINATES_X = {}
SHOP_COORDINATES_Y = {}

LAST_ORIENTAION = (0,0)
OFFSCREEN = (0, 0)

Player_rect = 0

TEXT = [] # place holder for displayable text on the screen

HARVESTED_OBJECTS = {} # Place holder for harvested decoration lists which contain rects

COMBAT_RECT = [0, 0] # rect, time
AXE = [0, 0]  # rect, time
PICAXE = [0, 0]  # rect, time
POS_CHANGE = (0, 0)  # Last orientation, type of strike

BASE_ATTACKING_SPEED = 500  # time used for timer to reset. multiplied by the weapon speed
BASE_ATTACKING_DAMAGE = 1  # damage used for damaging mobs
BASE_KNOCKBACK = 1 # how many steps mobs get knocked back

CURRENT_ROOM = ""  # data used for knowing which room is currently used. after mobs start reziding in buildings this will stop

APPLIANCE_CLICK = [""]  # for furnace to know when it was clicked and able to play the gif
DOOR_CLICK = 90, ""  # for doors when to open. the 90 is because i need a big value and then decreese from some other set value. and char value is for which building it was.

EQUIPED = {  # USED to know what is equiped on the char
    "Sword": (0, 27),
    "Axe": (0, 27),
    "Picaxe": (0, 27),
}

equipment = {  # equipment posisions with block tuple in inventory
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

# CONVERSATION = 0

QUESTS = 0  # obtained quests
COMPLETED_QUESTS = 0  # completed quests. removes data from previous variable

FOLLOWER = {
    "Name": "",
    "current_pos": (0,0),
    "target_pos": (0,0),
    "orientation": [],
    "aggressive": {
        "attack": False,
        "mob": 0,
        "mob_pos": (0,0),
        "class": 0}
            }  # [Name: str, current_pos: tuple, target_pos: tuple, orientation: tuple_list, agressive]

MAP_CHANGE = {}