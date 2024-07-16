
SELECTED_CHARACTER = ""

DATA = {}

TICK = 50

FAST = 1

START_POS = [330, 0]

CURRENT_STANCE = 0
LAST_ORIENT = ["Front.png", "_Walk.png", "_Walk1.png"]

HARVESTABLE = {}
ENTERABLE = ["House_1", "Church_1"]

BACKPACK_CONTENT = {}
BACKPACK_COORDINATES_X = {}
BACKPACK_COORDINATES_Y = {}

SPELLBOOK_CONTENT = {
    # Name : # Damage range # Type # How it's visualised # mana cost # knockback # level
    # "Magic Bolt": ("1d4 Force LINE 5 3 1", 0, 0),
    # "Fire Bolt": ("1d4 Fire LINE 5 1 1", 2, 0),
    # "Cold Bolt": ("1d4 Cold LINE 5 0 1", 4, 0),

                     }
SPELLBOOK_COORDINATES_X = {}
SPELLBOOK_COORDINATES_Y = {}


TEXT = []

HARVESTED_OBJECTS = {
    "Bush_S_2": []
}
# CONSUMABLE = ["Light Berries"]

EQUIPED = {"Hand1": 0,
           "Hand2": 0,
           "Legs": 0,
           "Arms": 0,
           "Feet": 0,
           "Head": 0,
           }
Mob_possition = 0

COMBAT_RECT = 0