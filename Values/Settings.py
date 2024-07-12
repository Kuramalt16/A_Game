

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = SCREEN_WIDTH * 9 / 16

# Full screen checkbox value and full screen marker
FULLSCREEN = False
FULLSCREEN_CH = False

# holds percentage value between max and min Screen_width. at max resolution screen width = 1280 at min 680
RESOLUTION = (SCREEN_WIDTH - 680) * 1 / 600

# Framerate
FRAMERATE = 60  #Default 60

#  back-end values
# IMPORTANT DON'T CHANGE CONTROLS WHICH SCREEN IS LOCKED OR UNLOCKED
START_APP = True
MAIN_MENU = True
BUSY = False

PLAY = False # once set to True starts the game.

# IMPORTANT DON'T CHANGE SPECIFIES THE FIRST COLOR EACH OBJECT STARTS AT WONT BE ABLE TO CHANGE COLORS IF CHANGED
DEFAULT = {"Eyes": (33, 150, 243, 255),
           "Skin": (255, 205, 210, 255),
           "Skin2": (239, 154, 154, 255),
           "Color_Hair": (237, 28, 36, 255),
           "Color_Shir": (238, 28, 36, 255),
           "Color_Pant": (240, 28, 36, 255),
           "Color_Shoe": (239, 28, 36, 255),
           "Backpack_Empty": (181, 110, 80, 255)
           }


# When set to True will restart the app
RESTART = False

# paths
PATHS = {
    "Girl": 'static/images/Girl.png',
    "Boy": 'static/images/Boy.png',
    "Human_Girl": 'static/images/Race/Human/Girl/Human_Girl.png',
    "Human_Girl_Back": 'static/images/Race/Human/Girl/Human_Girl_Back.png',
    "Human_Girl_Side1": 'static/images/Race/Human/Girl/Human_Girl_Side1.png',
    "Human_Girl_Side": 'static/images/Race/Human/Girl/Human_Girl_Side.png',
    "Elf_Girl": 'static/images/Race/Elf/Girl/Elf_Girl.png',
    "Elf_Girl_Back": 'static/images/Race/Elf/Girl/Elf_Girl_Back.png',
    "Elf_Girl_Side1": 'static/images/Race/Elf/Girl/Elf_Girl_Side1.png',
    "Elf_Girl_Side": 'static/images/Race/Elf/Girl/Elf_Girl_Side.png',
    "Human_Boy": 'static/images/Race/Human/Boy/Human_Boy.png',
    "Human_Boy_Back": 'static/images/Race/Human/Boy/Human_Boy_Back.png',
    "Human_Boy_Side1": 'static/images/Race/Human/Boy/Human_Boy_Side1.png',
    "Human_Boy_Side": 'static/images/Race/Human/Boy/Human_Boy_Side.png',
    "Elf_Boy": 'static/images/Race/Elf/Boy/Elf_Boy.png',
    "Elf_Boy_Back": 'static/images/Race/Elf/Boy/Elf_Boy_Back.png',
    "Elf_Boy_Side1": 'static/images/Race/Elf/Boy/Elf_Boy_Side1.png',
    "Elf_Boy_Side": 'static/images/Race/Elf/Boy/Elf_Boy_Side.png',
    "ENTER": 'static/images/Empty.png',
    "Delete": 'static/images/Empty.png',
    "Back": 'static/images/Back.png',
    "Eyes_Right": 'static/images/Right_arrow.png',
    "Skin_Right": 'static/images/Right_arrow.png',
    "Skin2_Right": 'static/images/Right_arrow.png',
    "Turn_Right": 'static/images/Right_arrow.png',
    "Hair_Right": 'static/images/Right_arrow.png',
    "Slee_Right": 'static/images/Right_arrow.png',
    "Shir_Right": 'static/images/Right_arrow.png',
    "Pant_Right": 'static/images/Right_arrow.png',
    "Shoe_Right": 'static/images/Right_arrow.png',
    "Color_Hair_Right": 'static/images/Right_arrow.png',
    "Color_Shir_Right": 'static/images/Right_arrow.png',
    "Color_Pant_Right": 'static/images/Right_arrow.png',
    "Color_Shoe_Right": 'static/images/Right_arrow.png',
    "Eyes_Left": 'static/images/Left_arrow.png',
    "Skin_Left": 'static/images/Left_arrow.png',
    "Skin2_Left": 'static/images/Left_arrow.png',
    "Turn_Left": 'static/images/Left_arrow.png',
    "Hair_Left": 'static/images/Left_arrow.png',
    "Slee_Left": 'static/images/Left_arrow.png',
    "Shir_Left": 'static/images/Left_arrow.png',
    "Pant_Left": 'static/images/Left_arrow.png',
    "Shoe_Left": 'static/images/Left_arrow.png',
    "Color_Hair_Left": 'static/images/Left_arrow.png',
    "Color_Shir_Left": 'static/images/Left_arrow.png',
    "Color_Pant_Left": 'static/images/Left_arrow.png',
    "Color_Shoe_Left": 'static/images/Left_arrow.png',
         }

PLAYING_PATH = {
    "Backpack_Empty": 'static/images/Playing/Backpack_Empty.png',
    "Char_bar": "static/images/Playing/Char_bar.png",
    "Grave": "static/images/Playing/Grave.png",
    "Dead": "static/images/Playing/Dead/Dead_",
    "Portal": "static/images/Playing/Portal/Portal_",
    "Sign": "static/images/Playing/Sign.png",
    "Luna": "static/images/Playing/NPC/Luna/Luna_",
    "Bear": "static/images/Playing/NPC/Bear/Bear_",
}
ITEM_PATHS = {
    "Light Berries": 'static/images/Items/Light Berries.png',
    "Slime Ball": 'static/images/Items/Slime Ball.png',

}
DECOR_PATH = {
    "Grass":    'static/images/Background/Grass.png',
    "Bush_S_1": 'static/images/Background/Bushes/Bush_S_1.png',
    "Bush_S_2": 'static/images/Background/Bushes/Bush_S_2.png',
    "Tree_T_1": 'static/images/Background/Trees/Tree_T_1.png',
    "House_1":  'static/images/Background/House/House_1.png',
    "Church_1":  'static/images/Background/House/Church_1.png',
}
MOB_PATH = {
    "Slime_S": ('static/images/Mobs/Ooze/Slime_S/', 10),
}
COMBAT_PATH = {
    "Blunt": ('static/images/Combat/Blunt/Blunt_', 11)
}
CHAR_SAVE_PATH = 'static/data/created_characters'


# Gif maker
GIF_DICT = {"Walk": "_Walk, Front, _Walk1, Front",
            "_Back_Walk": "_Back_Walk, Back, _Back_Walk1, Back",
            "_Side_Walk": "_Side_Walk, Side, _Side_Walk1, Side",
            "_Side_Walk11": "_Side_Walk11, Side1, _Side_Walk12, Side1"}



# Dummy Values
DUMMY_VALUE1 = 0
DUMMY_VALUE2 = 0