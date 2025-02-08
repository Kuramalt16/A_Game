from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S
from Testing import test as T

def Main_menu(screen):
    # screen.fill('white')
    buttons = {}
    b_left = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 6)
    b_top1 = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / (10 / 4))
    b_top2 = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / (10 / 2))
    b_top3 = S.SCREEN_HEIGHT / 2
    b_top4 = S.SCREEN_HEIGHT / 2 + (S.SCREEN_HEIGHT / 5)

    BUTTON_WIDTH = S.SCREEN_WIDTH - (2 * b_left)
    BUTTON_HEIGHT = S.SCREEN_HEIGHT / 8
    m_left = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 5)
    m_top = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / 2.2)
    m_width = S.SCREEN_WIDTH - (2 * (S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 5)))
    m_height = S.SCREEN_HEIGHT / 10 * 9
    frame_main_menu = Ff.add_image_to_screen(screen, S.PATHS["Small_frame"], [m_left, m_top, m_width, m_height])
    if I.info.SELECTED_CHARACTER == "":
        buttons["Start Game"] = Ff.add_image_to_screen(screen, S.PATHS["Empty_button_frame"], [b_left, b_top1, BUTTON_WIDTH, BUTTON_HEIGHT])
        # buttons["Start Game_text"] = Ff.display_text(screen, "Start Game", 30, (b_left + BUTTON_WIDTH / 4, b_top1 + BUTTON_HEIGHT / 3), "black")
        buttons["Start Game_text"] = Ff.display_wraped_text(screen, "Start Game", buttons["Start Game"].w, (b_left + BUTTON_WIDTH / 4, b_top1 + BUTTON_HEIGHT / 3), "black")
    else:
        buttons["Resume Game"] = Ff.add_image_to_screen(screen, S.PATHS["Empty_button_frame"], [b_left, b_top1, BUTTON_WIDTH, BUTTON_HEIGHT])
        buttons["Resume Game_text"] = Ff.display_wraped_text(screen, "Resume Game", buttons["Resume Game"].w, (b_left + BUTTON_WIDTH / 6, b_top1 + BUTTON_HEIGHT / 3), "black")

    buttons["Settings"] = Ff.add_image_to_screen(screen, S.PATHS["Empty_button_frame"], [b_left, b_top2, BUTTON_WIDTH, BUTTON_HEIGHT])
    buttons["Settings_text"] = Ff.display_wraped_text(screen, "Settings", buttons["Settings"].w, (b_left + BUTTON_WIDTH / 3, b_top2 + BUTTON_HEIGHT / 3), "black")
    if I.info.SELECTED_CHARACTER == "":
        buttons["Update"] = Ff.add_image_to_screen(screen, S.PATHS["Empty_button_frame"], [b_left, b_top3, BUTTON_WIDTH, BUTTON_HEIGHT])
        buttons["Update_text"] = Ff.display_wraped_text(screen, "Update", buttons["Update"].w, (b_left + BUTTON_WIDTH / 3, b_top3 + BUTTON_HEIGHT / 3), "black")

    if I.info.SELECTED_CHARACTER == "":
        buttons["Exit"] = Ff.add_image_to_screen(screen, S.PATHS["Empty_button_frame"], [b_left, b_top4, BUTTON_WIDTH, BUTTON_HEIGHT])
        buttons["Exit_text"] = Ff.display_wraped_text(screen, "Exit", buttons["Exit"].w, (b_left + BUTTON_WIDTH / 2.3, b_top4 + BUTTON_HEIGHT / 3), "black")
    else:
        buttons["Main Menu"] = Ff.add_image_to_screen(screen, S.PATHS["Empty_button_frame"],[b_left, b_top4, BUTTON_WIDTH, BUTTON_HEIGHT])
        buttons["Main Menu_text"] = Ff.display_wraped_text(screen, "Main Menu", buttons["Main Menu"].w,(b_left + BUTTON_WIDTH / 3.5, b_top4 + BUTTON_HEIGHT / 3), "black")

    return buttons


