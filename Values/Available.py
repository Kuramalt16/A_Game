
RACE = ["Human", "Elf"]

DEFAULT_TEMP = {"Eyes": (33, 150, 243, 255),
                "Skin": (255, 205, 210, 255),
                "Skin2": (239, 154, 154, 255),
                "Color_Hair": (237, 28, 36, 255),
                "Color_Shir": (238, 28, 36, 255),
                "Color_Pant": (240, 28, 36, 255),
                "Color_Shoe": (239, 28, 36, 255)
           }

EYE_COLORS = {
        "Original": (33, 150, 243, 255),
        "Black": (1, 1, 1, 255),
        "White": (250, 250, 250, 255),
        "Red": (200, 0, 0, 255),

        "Lime": (165, 169, 0, 255),
        "Green": (0, 200, 0, 255),
        "Green1": (45, 150, 57, 255),
        "Dark_Green": (10, 50, 10, 255),

        "Blue": (0, 0, 200, 255),
        "Sky-Blue": (50, 100, 200, 255),
        "Light_Blue": (0, 100, 200, 255),
        "Teal": (0, 128, 128, 255),

        "Light Yellow": (229, 203, 133, 255),
        "Yellow": (200, 200, 0, 255),
        "Gold": (200, 150, 0, 255),

        "Magenta": (250, 0, 250, 255),
        "Silk-Purple": (100, 100, 200, 255),
        "Pink": (254, 192, 203, 255),

        "Dark_Orange": (200, 100, 0, 255),
        "Orange": (204, 121, 32, 255),
        "Light Orange": (214, 159, 10, 255),

        "Silver": (165, 169, 180, 255),

        }

SKIN_COLORS = {
            "Original": (255, 205, 210, 255),
            "lightskinned": (250, 200, 154, 255),
            "Goldskin": (199, 150, 0, 255),
            "brownskin": (60, 50, 20, 255),
            "grayskin": (96, 93, 68, 255),
            "Iceskin": (234, 232, 194, 255),
            "Darkskin": (114, 78, 81, 255),
            "greenskin": (31, 53, 44, 255),
            "whiteskin": (162, 168, 170, 255),


            }

SKIN2_COLORS = {
                "Original": (239, 154, 154, 255),
                "lightskinned": (200, 150, 100, 255),
                "Goldskin": (149, 150, 0, 255),
                "brownskin": (30, 20, 10, 255),
                "grayskin": (66, 63, 58, 255),
                "Iceskin": (174, 172, 184, 255),
                "Darkskin": (84, 58, 61, 255),
                "greenskin": (21, 43, 34, 255),
                "whiteskin": (132, 138, 160, 255),

}

HAIR_COLORS = {}

for color_name, color_value in EYE_COLORS.items():
    if color_name == "Original":
        HAIR_COLORS[color_name] = (237, 28, 36, 255)
    else:
        r, g, b, a = color_value
        HAIR_COLORS[color_name] = (r + 1, g, b, a)

SHIRT_COLORS = {}
for color_name, color_value in EYE_COLORS.items():
    if color_name == "Original":
        SHIRT_COLORS[color_name] = (238, 28, 36, 255)
    else:
        r, g, b, a = color_value
        SHIRT_COLORS[color_name] = (r, g + 1, b, a)

PANTS_COLORS = {}
for color_name, color_value in EYE_COLORS.items():
    if color_name == "Original":
        PANTS_COLORS[color_name] = (240, 28, 36, 255)
    else:
        r, g, b, a = color_value
        PANTS_COLORS[color_name] = (r, g, b + 1, a)


SHOE_COLORS = {}
for color_name, color_value in EYE_COLORS.items():
    if color_name == "Original":
        SHOE_COLORS[color_name] = (239, 28, 36, 255)
    else:
        r, g, b, a = color_value
        SHOE_COLORS[color_name] = (r + 1, g + 1, b, a)


color_mappings = {
    "Eyes": EYE_COLORS,
    "Skin": SKIN_COLORS,
    "Skin2": SKIN2_COLORS,
    "Color_Hair": HAIR_COLORS,
    "Color_Shir": SHIRT_COLORS,
    "Color_Pant": PANTS_COLORS,
    "Color_Shoe": SHOE_COLORS
}

clothing_count = {
    "Hair": 6,
    "Shir": 6,
    "Slee": 4,
    "Pant": 5,
    "Shoe": 4
}

NOTES = {
    "C1": 32.70,
    "C#1": 34.65,
    "D1": 36.71,
    "D#1": 38.89,
    "E1": 41.20,
    "F1": 43.65,
    "F#1": 46.25,
    "G1": 49.00,
    "G#1": 51.91,
    "A1": 55.00,
    "A#1": 58.27,
    "B1": 61.74,
    "C2": 65.41,
    "C#2": 69.30,
    "D2": 73.42,
    "D#2": 77.78,
    "E2": 82.41,
    "F2": 87.31,
    "F#2": 92.50,
    "G2": 98.00,
    "G#2": 103.83,
    "A2": 110.00,
    "A#2": 116.54,
    "B2": 123.47,
    "C3": 130.81,
    "C#3": 138.59,
    "D3": 146.83,
    "D#3": 155.56,
    "E3": 164.81,
    "F3": 174.61,
    "F#3": 185.00,
    "G3": 196.00,
    "G#3": 207.65,
    "A3": 220.00,
    "A#3": 233.08,
    "B3": 246.94,
    "C4": 261.63,
    "C#4": 277.18,
    "D4": 293.66,
    "D#4": 311.13,
    "E4": 329.63,
    "F4": 349.23,
    "F#4": 369.99,
    "G4": 392.00,
    "G#4": 415.30,
    "A4": 440.00,
    "A#4": 466.16,
    "B4": 493.88,
    "C5": 523.25,
    "C#5": 554.37,
    "D5": 587.33,
    "D#5": 622.25,
    "E5": 659.25,
    "F5": 698.46,
    "F#5": 739.99,
    "G5": 783.99
}


background_music = [
    ((NOTES["C4"], NOTES["C3"]), 500),
    ((NOTES["G4"], NOTES["C3"]), 500),
    ((NOTES["E4"], NOTES["C3"]), 500),
    ((NOTES["C5"], NOTES["C3"]), 500),

    ((NOTES["C4"], NOTES["C3"]), 500),
    ((NOTES["G4"], NOTES["C3"]), 500),
    ((NOTES["E4"], NOTES["C3"]), 500),
    ((NOTES["C5"], NOTES["C3"]), 500),

    ((NOTES["C4"], NOTES["F3"]), 500),
    ((NOTES["G4"], NOTES["F3"]), 500),
    ((NOTES["E4"], NOTES["F3"]), 500),
    ((NOTES["C5"], NOTES["F3"]), 500),

    ((NOTES["C4"], NOTES["F3"]), 500),
    ((NOTES["G4"], NOTES["F3"]), 500),
    ((NOTES["E4"], NOTES["F3"]), 500),
    ((NOTES["C5"], NOTES["F3"]), 500),

    ((NOTES["C4"], NOTES["E3"]), 500),
    ((NOTES["G4"], NOTES["E3"]), 500),
    ((NOTES["E4"], NOTES["E3"]), 500),
    ((NOTES["C5"], NOTES["E3"]), 500),

    ((NOTES["C4"], NOTES["E3"]), 500),
    ((NOTES["G4"], NOTES["E3"]), 500),
    ((NOTES["E4"], NOTES["E3"]), 500),
    ((NOTES["C5"], NOTES["E3"]), 500),

    ((NOTES["C4"], NOTES["G3"]), 500),
    ((NOTES["G4"], NOTES["G3"]), 500),
    ((NOTES["E4"], NOTES["G3"]), 500),
    ((NOTES["C5"], NOTES["G3"]), 500),

    ((NOTES["C4"], NOTES["G3"]), 500),
    ((NOTES["G4"], NOTES["G3"]), 500),
    ((NOTES["E4"], NOTES["G3"]), 500),
    ((NOTES["C5"], NOTES["G3"]), 500),
]
dead_music = [
    ((NOTES["C4"], NOTES["C3"]), 1000),
    ((NOTES["C4"], NOTES["C3"]), 1000),
    ((NOTES["D4"], NOTES["C3"]), 1000),
    ((NOTES["D4"], NOTES["C3"]), 1000),

    ((NOTES["C4"], NOTES["F3"]), 1000),
    ((NOTES["C4"], NOTES["F3"]), 1000),
    ((NOTES["D4"], NOTES["F3"]), 1000),
    ((NOTES["D4"], NOTES["F3"]), 1000),
]

COMMANDS = ["TOGGLE GOD_MODE", "TELEPORT", "ROOM", "SET TIME", "GET"]

DUST_COLORS = {"blue": (0, 0, 255, 255),
               "red": (255, 0, 0, 255),
               "green": (0, 255, 0, 255),
               "yellow": (255, 255, 0, 255),
               "light yellow": (220, 245, 122, 255),
               "white": (255, 255, 255, 255),
               "pale green": (152, 251, 152, 255),
               "light purple": (102, 102, 153, 255),
               "purple": (85, 85, 170, 255),
               }

POTIONS = {
    "SOUR": "Exhaustion",
    "SWEET": "Health",
    "BITTER": "Mana",
    "TASTELESS": "NoEffect",
    "MILD": "Strength",
    "STICKY": "Damage Health",
    "SHARP": "Damage Health",
}
POTION_COLORS = {
    "Pale Green": "Potion_Damage Health",
    "Light Yellow": "Potion_Exhaustion",
    "Brown": "Potion_Speed",
    "Light Purple": "Potion_Strength",
    "Blue": "Potion_Mana",
    "Sage": "Potion_Slow",
    "Light Blue": "Potion_Mana_Regeneration",
}

CRAFTING_DICT = \
    {
        "Iron Sword Blade Cast":
            {
                (-2, 4): "Clay",
                (-4, 4): "Clay",
                (-6, 4): "Clay",
                (-2, 6): "Clay",
                (-4, 6): "Wooden Sword",
                (-6, 6): "Clay",
                (-2, 8): "Clay",
                (-4, 8): "Clay",
                (-6, 8): "Clay"
            },
        "Iron Picaxe Blade Cast":
            {
                (-4, 4): "Clay",
                (-6, 4): "Clay",
                (-8, 4): "Clay",
                (-2, 6): "Clay",
                (-4, 6): "Light Wood Plank",
                (-6, 6): "Light Wood Plank",
                (-8, 6): "Light Wood Plank",
                (-10, 6): "Clay",
                (-4, 8): "Clay",
                (-6, 8): "Clay",
                (-8, 8): "Clay",
            },
        "Iron Shovel Blade Cast":
            {
                (-4, 4): 'Clay',
                (-6, 6): 'Clay',
                (-2, 6): 'Clay',
                (-4, 8): 'Clay',
                (-2, 8): 'Clay',
                (-6, 8): 'Clay',
                (-4, 6): 'Light Wood Plank'
            },
        "Iron Axe Blade Cast":
            {
                (-2, 6): 'Clay',
                (-2, 4): 'Clay',
                (-2, 8): 'Clay',
                (-4, 8): 'Clay',
                (-6, 6): 'Clay',
                (-4, 4): 'Clay',
                (-4, 6): 'Light Wood Plank'
            },
        "Sword Handle Cast":
            {
                (-2, 6): 'Clay',
                (-4, 4): 'Clay',
                (-6, 4): 'Clay',
                (-8, 4): 'Clay',
                (-10, 6): 'Clay',
                (-8, 8): 'Clay',
                (-4, 8): 'Clay',
                (-6, 10): 'Clay',
                (-4, 6): 'Light Wood Plank',
                (-6, 6): 'Light Wood Plank',
                (-8, 6): 'Light Wood Plank',
                (-6, 8): 'Light Wood Plank'
            },

# wooden
        "2**Light Wood Plank":
            {
                (-2, 4): ("Light Wood")
            },
        "Wooden Dagger":
            {
                (-2, 4): "Light Wood Plank",
                (-2, 6): "Stick"
            },
        "Wooden Axe":
            {
                (-4, 4): "Light Wood Plank",
                (-2, 6): 'Light Wood Plank',
                (-4, 6): 'Light Wood Plank',
                (-2, 8): 'Stick',
                (-2, 10): 'Stick'
            },
        "Wooden Sword":
            {
                (-2, 4): 'Light Wood Plank',
                (-2, 6): 'Light Wood Plank',
                (-2, 8): 'Light Wood Plank',
                (-2, 10): 'Stick',
                (-2, 12): 'Stick'
            },
        "Wooden Picaxe":
            {
                (-2, 4): 'Light Wood Plank',
                (-4, 4): 'Light Wood Plank',
                (-4, 6): 'Stick',
                (-4, 8): 'Stick',
                (-6, 4): 'Light Wood Plank'
            },
        "Wooden Shovel":
            {
                (-2, 4): 'Light Wood Plank',
                (-2, 6): 'Stick',
                (-2, 8): 'Stick'
            },
        "Wooden Hoe":
            {
                (-2, 4): "Light Wood Plank",
                (-4, 4): "Light Wood Plank",
                (-2, 6): "Stick",
                (-2, 8): "Stick",
            },
# Iron
        "Iron Dagger":
            {
                (-2, 4): "Iron",
                (-2, 6): "Stick"
            },
        "Iron Sword":
            {
                (-2, 4): 'Iron Sword Blade',
                (-2, 6): 'Iron Sword Handle',
            },
        "Iron Axe":
            {
                (-2, 4): "Iron Axe Blade",
                (-2, 6): 'Stick',
                (-2, 8): 'Stick',
            },
        "Iron Picaxe":
            {
                (-2, 4): "Iron Picaxe Blade",
                (-2, 6): 'Stick',
                (-2, 8): 'Stick',
            },
        "Iron Shovel":
            {
                (-2, 4): "Iron Shovel Blade",
                (-2, 6): 'Stick',
                (-2, 8): 'Stick',
            },
        "Iron Hoe":
            {
                (-2, 4): "Iron Hoe Blade",
                (-2, 6): "Stick",
                (-2, 8): "Stick",
            },
#         "Iron Ring":
#             {
#                 (-2, 6): 'Iron',
#                 (-4, 4): 'Iron',
#                 (-4, 8): 'Iron',
#                 (-6, 6): 'Iron'
#             },

# Magnesium
        "Magnesium Dagger":
            {
                (-2, 4): "Magnesium",
                (-2, 6): "Stick"
            },
        "Magnesium Sword":
            {
                (-2, 4): 'Magnesium Sword Blade',
                (-2, 6): 'Magnesium Sword Handle',
            },
        "Magnesium Axe":
            {
                (-2, 4): "Magnesium Axe Blade",
                (-2, 6): 'Stick',
                (-2, 8): 'Stick',
            },
        "Magnesium Picaxe":
            {
                (-2, 4): "Magnesium Picaxe Blade",
                (-2, 6): 'Stick',
                (-2, 8): 'Stick',
            },
        "Magnesium Shovel":
            {
                (-2, 4): "Magnesium Shovel Blade",
                (-2, 6): 'Stick',
                (-2, 8): 'Stick',
            },
#         "Magnesium Ring":
#             {
#                 (-2, 6): 'Magnesium',
#                 (-4, 4): 'Magnesium',
#                 (-4, 8): 'Magnesium',
#                 (-6, 6): 'Magnesium'
#             },
# Obsidian
        "Obsidian Dagger":
            {
                (-2, 4): "Obsidian Shard",
                (-2, 6): "Slime Ball",
                (-2, 8): "Stick"
            },
        # "Obsidian Axe":
        #     {
        #         (-4, 4): "Obsidian Shard",
        #         (-2, 6): 'Obsidian Shard',
        #         (-4, 6): 'Obsidian Shard',
        #         (-2, 8): 'Stick',
        #         (-2, 10): 'Stick'
        #     },
        # "Obsidian Sword":
        #     {
        #         (-2, 4): 'Obsidian Shard',
        #         (-2, 6): 'Obsidian Shard',
        #         (-2, 8): 'Obsidian Shard',
        #         (-2, 10): 'Stick',
        #         (-2, 12): 'Stick'
        #     },
        # "Obsidian Picaxe":
        #     {
        #         (-2, 4): 'Obsidian Shard',
        #         (-4, 4): 'Obsidian Shard',
        #         (-4, 6): 'Stick',
        #         (-4, 8): 'Stick',
        #         (-6, 4): 'Obsidian Shard'
        #     },
        # "Obsidian Ring":
        #     {
        #         (-2, 6): 'Obsidian Shard',
        #         (-4, 4): 'Obsidian Shard',
        #         (-4, 8): 'Obsidian Shard',
        #         (-6, 6): 'Obsidian Shard'
        #     },
 # Glass
        "Glass Sword":
            {
                (-2, 4): "Glass Sword Blade",
                (-2, 6): "Glass Sword Handle",
            },
        "Glass Axe":
            {
                (-2, 4): "Glass Axe Blade",
                (-2, 6): 'Stick',
                (-2, 8): 'Stick',
            },
        "Glass Picaxe":
            {
                (-2, 4): "Glass Picaxe Blade",
                (-2, 6): 'Stick',
                (-2, 8): 'Stick',
            },
        "Glass Shovel":
            {
                (-2, 4): "Glass Shovel Blade",
                (-2, 6): 'Stick',
                (-2, 8): 'Stick',
            },

    }
WALKING_COLORS = \
    {
    (70, 70, 70, 255): "Pavement",
    (180, 180, 180, 255): "Pavement",
    (0, 0, 0, 255): "Pavement",
    (97, 125, 32, 255): "Grass-Pavement", # grass/pavement mix
    (77, 105, 12, 255): "Grass-Flakes", # grass/pavement mix
    (137, 176, 46, 255): "Grass",
    (152, 179, 44, 255): "Grass",
    (76, 104, 11, 255): "Grass",
    (154, 181, 45, 255): "Grass",
    (255, 255, 0, 255): "Flash",
    (254, 224, 130, 255): "Sand",
    (240, 225, 113, 255): "Sand",
    (255, 152, 0, 255): "Sand-Flakes",
    (255, 193, 7, 255): "Sand-Flakes",
    (222, 206, 104, 255): "Sand-Grass",
    (179, 152, 80, 255): "Sand-Wet",
    (168, 141, 66, 255): "Sand-Pavement",
    (214, 186, 103, 255): "Sand-Deck",
    (204, 177, 98, 255): "Sand-Wet",
    (102, 53, 33, 255): "Deck",
    (230, 156, 124, 255): "Deck",
    (125, 72, 50, 255): "Deck",
    (204, 130, 98, 255): "Deck",
    (181, 110, 80, 255): "Deck",
    (0, 172, 193, 255): "Water",
    (163, 146, 47, 255): "SandClay-Pavement",
    (115, 101, 23, 255): "SandClay-Pavement",
    (194, 178, 78, 255): "Clay",
    (230, 219, 142, 255): "Clay",
    (89, 79, 26, 255): "SandClay-Pavement",
    (64, 55, 12, 255): "Clay-Stairs",
    (235, 216, 94, 255): "Clay-Stairs",
    (207, 185, 66, 255): "Clay-Stairs",
    (240, 227, 134, 255): "Clay-Flakes",
    (168, 157, 81, 255): "Clay-Flakes",
    (66, 66, 66, 255): "Rock",
    (97, 97, 97, 255): "Rock",
    (117, 117, 117, 255): "Rock",
    (189, 189, 189, 255): "Rock",
    (97, 61, 36, 255): "FencePost",
    (138, 166, 133, 255): "Dark Grass-Pavement",
    (137, 165, 132, 255): "Dark Grass-Pavement",
    (133, 156, 34, 255): "Stuffed Grass",
    (245, 228, 156, 255): "Tree Leaves", # ship this
    }
QUEST_SHOW_MARKS = {}

MAPS = {}