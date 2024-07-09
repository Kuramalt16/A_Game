from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S
from Testing import test as T

B_LEFT = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 6)
B_TOP1 = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / (10 / 3))
B_TOP2 = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / 10)
B_TOP3 = S.SCREEN_HEIGHT / 2 + (S.SCREEN_HEIGHT / 10)

M_LEFT = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 5)
M_TOP = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / 2.2)

MENU_WIDTH = S.SCREEN_WIDTH - (2 * M_LEFT)
MENU_HEIGHT = S.SCREEN_HEIGHT / 10 * 9

BUTTON_WIDTH = S.SCREEN_WIDTH - (2 * B_LEFT)
BUTTON_HEIGHT = S.SCREEN_HEIGHT / 10


def Main_menu(screen):
    screen.fill('white')
    I.pg.display.flip()
    frame_main_menu = Ff.add_image_to_screen(screen, 'static/images/Frame_main_menu.png', [M_LEFT, M_TOP, MENU_WIDTH, MENU_HEIGHT])
    I.pg.display.update(frame_main_menu)
    b_start_game = Ff.add_image_to_screen(screen, 'static/images/Start_game.png', [B_LEFT, B_TOP1, BUTTON_WIDTH, BUTTON_HEIGHT])
    I.pg.display.update(b_start_game)
    b_settings = Ff.add_image_to_screen(screen, 'static/images/Settings.png', [B_LEFT, B_TOP2, BUTTON_WIDTH, BUTTON_HEIGHT])
    I.pg.display.update(b_settings)
    b_exit = Ff.add_image_to_screen(screen, 'static/images/Exit.png', [B_LEFT, B_TOP3, BUTTON_WIDTH, BUTTON_HEIGHT])
    I.pg.display.update(b_exit)

    buttons = {"Start_game": b_start_game, "Settings": b_settings, "Exit": b_exit}
    return buttons


