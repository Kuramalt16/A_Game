
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