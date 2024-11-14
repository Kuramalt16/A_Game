from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S
from Testing import test as T

B_LEFT = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 6)
B_TOP1 = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / (10 / 4))
B_TOP2 = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / (10 / 2))
B_TOP3 = S.SCREEN_HEIGHT / 2
B_TOP4 = S.SCREEN_HEIGHT / 2 + (S.SCREEN_HEIGHT / 5)

M_LEFT = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 5)
M_TOP = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / 2.2)

MENU_WIDTH = S.SCREEN_WIDTH - (2 * M_LEFT)
MENU_HEIGHT = S.SCREEN_HEIGHT / 10 * 9

BUTTON_WIDTH = S.SCREEN_WIDTH - (2 * B_LEFT)
BUTTON_HEIGHT = S.SCREEN_HEIGHT / 8


def Main_menu(screen):
    # screen.fill('white')
    buttons = {}
    I.pg.display.flip()
    frame_main_menu = Ff.add_image_to_screen(screen, S.PATHS["Small_frame"], [M_LEFT, M_TOP, MENU_WIDTH, MENU_HEIGHT])
    I.pg.display.update(frame_main_menu)
    if I.info.SELECTED_CHARACTER == "":
        buttons["Start Game"] = Ff.add_image_to_screen(screen, S.PATHS["Empty_button_frame"], [B_LEFT, B_TOP1, BUTTON_WIDTH, BUTTON_HEIGHT])
        buttons["Start Game_text"] = Ff.display_text(screen, "Start Game", 30, (B_LEFT + BUTTON_WIDTH / 4, B_TOP1 + BUTTON_HEIGHT / 3), "black")
        I.pg.display.update(buttons["Start Game"])
    else:
        buttons["Resume Game"] = Ff.add_image_to_screen(screen, S.PATHS["Empty_button_frame"], [B_LEFT, B_TOP1, BUTTON_WIDTH, BUTTON_HEIGHT])
        buttons["Resume Game_text"] = Ff.display_text(screen, "Resume Game", 30, (B_LEFT + BUTTON_WIDTH / 6, B_TOP1 + BUTTON_HEIGHT / 3), "black")
        I.pg.display.update(buttons["Resume Game"])

    buttons["Settings"] = Ff.add_image_to_screen(screen, S.PATHS["Empty_button_frame"], [B_LEFT, B_TOP2, BUTTON_WIDTH, BUTTON_HEIGHT])
    buttons["Settings_text"] = Ff.display_text(screen, "Settings", 30, (B_LEFT + BUTTON_WIDTH / 3, B_TOP2 + BUTTON_HEIGHT / 3), "black")
    I.pg.display.update(buttons["Settings"])
    if I.info.SELECTED_CHARACTER == "":
        buttons["Update"] = Ff.add_image_to_screen(screen, S.PATHS["Empty_button_frame"], [B_LEFT, B_TOP3, BUTTON_WIDTH, BUTTON_HEIGHT])
        buttons["Update_text"] = Ff.display_text(screen, "Update", 30, (B_LEFT + BUTTON_WIDTH / 3, B_TOP3 + BUTTON_HEIGHT / 3), "black")
        I.pg.display.update(buttons["Update"])

    if I.info.SELECTED_CHARACTER == "":
        buttons["Exit"] = Ff.add_image_to_screen(screen, S.PATHS["Empty_button_frame"], [B_LEFT, B_TOP4, BUTTON_WIDTH, BUTTON_HEIGHT])
        buttons["Exit_text"] = Ff.display_text(screen, "Exit", 30, (B_LEFT + BUTTON_WIDTH / 2.3, B_TOP4 + BUTTON_HEIGHT / 3), "black")
        I.pg.display.update(buttons["Exit"])
    else:
        buttons["Main Menu"] = Ff.add_image_to_screen(screen, S.PATHS["Empty_button_frame"],[B_LEFT, B_TOP4, BUTTON_WIDTH, BUTTON_HEIGHT])
        buttons["Main Menu_text"] = Ff.display_text(screen, "Main Menu", 30,(B_LEFT + BUTTON_WIDTH / 3.5, B_TOP4 + BUTTON_HEIGHT / 3), "black")
        I.pg.display.update(buttons["Main Menu"])

    return buttons


