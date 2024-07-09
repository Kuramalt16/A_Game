from utils import Imports as I, Frequent_functions as Ff
from Testing import test as T
from Values import Settings as S
from Render import Main_Menu_render as mr
from Backend import Settings_backend as SB, Character_selection_backend as CB, Play


def startup_clear():
    if I.os.path.exists(S.CHAR_SAVE_PATH):
        if not I.os.listdir(S.CHAR_SAVE_PATH):
            # if there is no data in save_file then removes the directory
            I.os.rmdir(S.CHAR_SAVE_PATH)

    I.TD.Name = ""
    I.TD.Gender = ""
    I.TD.Age = ""
    I.TD.Race = ""
    I.TD.Skin = {}
    I.TD.Appearance = {}
    I.TD.Appearance_color = {}
    I.TD.Char_Rect = 0

class Set_up():

    startup_clear()
    I.pg.init()  # initializes all game modules
    screen = I.pg.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))  # sets screen mode
    I.pg.display.set_caption('A Game')
    screen.fill('white')
    I.pg.display.flip()
    clock = I.pg.time.Clock()
    running = True  # if set to false game doesn't start and window doesn't open
    clicked_button = ""
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.QUIT:
                running = False
            if S.START_APP:
                buttons = mr.Main_menu(screen)
                S.START_APP = False
            if event.type == I.pg.MOUSEBUTTONDOWN and (S.MAIN_MENU):
                pos = I.pg.mouse.get_pos()
                for key, value in buttons.items():
                    if value.collidepoint(pos[0], pos[1]) and I.pg.mouse.get_pressed()[0]:
                        if key == "Exit":
                            value = Ff.button_click_render(screen, value, 1, key)
                            I.pg.display.flip()
                            clicked_button = key
                        elif key == "Start_game":
                            value = Ff.button_click_render(screen, value, 1, key)
                            I.pg.display.flip()
                            clicked_button = key
                        elif key == "Settings":
                            value = Ff.button_click_render(screen, value, 1, key)
                            I.pg.display.flip()
                            clicked_button = key
            if event.type == I.pg.MOUSEBUTTONUP and (S.MAIN_MENU):
                pos = I.pg.mouse.get_pos()
                for key, value in buttons.items():
                    if value.collidepoint(pos[0], pos[1]) and not I.pg.mouse.get_pressed()[0]:
                        if key == "Exit" and clicked_button == key:
                            value = Ff.button_click_render(screen, value, 0, key)
                            I.pg.display.flip()
                            running = False
                            S.MAIN_MENU = False
                        elif key == "Start_game" and clicked_button == key:
                            value = Ff.button_click_render(screen, value, 0, key)
                            I.pg.display.flip()
                            S.MAIN_MENU = False
                            CB.Character_Selection(screen)
                            if S.PLAY:
                                Play.Start(screen, clock)
                        elif key == "Settings" and clicked_button == key:
                            value = Ff.button_click_render(screen, value, 0, key)
                            I.pg.display.flip()
                            S.MAIN_MENU = False
                            SB.Settings(screen)

                    elif clicked_button == key:
                        value = Ff.button_click_render(screen, value, 0, clicked_button)
                        I.pg.display.flip()
                        clicked_button = ""
        clock.tick(S.FRAMERATE)  # limits FPS to 60
        if S.RESTART:
            running = False
    if not S.RESTART:
        I.pg.quit()



