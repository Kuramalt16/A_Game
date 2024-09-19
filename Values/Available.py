
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
        "Green": (0, 200, 0, 255),
        "Blue": (0, 0, 200, 255),
        "Sky-Blue": (50, 100, 200, 255),
        "Yellow": (200, 200, 0, 255),
        "Magenta": (250, 0, 250, 255),
        "Dark_Green": (10, 50, 10, 255),
        "Dark_Orange": (200, 100, 0, 255),
        "Gold": (200, 150, 0, 255),
        "Silver": (165, 169, 180, 255),
        "Lime": (165, 169, 0, 255),
        "Light_Blue": (0, 100, 200, 255),
        "Silk-Purple": (100, 100, 200, 255),
        "Teal": (0, 128, 128, 255),
        "Pink": (254, 192, 203, 255),
        }

SKIN_COLORS = {
            "Original": (255, 205, 210, 255),
            "light-skinned": (250, 200, 154, 255),
            "Gold": (199, 150, 0, 255),
            "Black": (60, 50, 20, 255),

            }

SKIN2_COLORS = {
                "Original": (239, 154, 154, 255),
                "light-skinned": (200, 150, 100, 255),
                "Gold": (149, 150, 0, 255),
                "Black": (30, 20, 10, 255),
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
    "Slee": 3,
    "Pant": 5,
    "Shoe": 3
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

DROPS = {
    "Slime_S": ("Slime Ball", 1, 3),
    "Pig": [("Meat0", 1, 2), ("Meat1", 1, 3)],
    "Skeleton" : []
         }   # Key: Mob that drops : value: tuple(name of item, amount of item, chance of item, write only the denominator of fraction 1/x)

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

COMMANDS = ["TOGGLE GOD_MODE", "TELEPORT", "ROOM"]