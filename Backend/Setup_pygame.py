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

    I.info.SELECTED_CHARACTER = ""


def Set_up():
    icon_image = I.pg.image.load('static/images/Icon.png')
    I.pg.display.set_icon(icon_image)
    I.pg.init()  # initializes all game modules
    screen = I.pg.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))  # sets screen mode
    I.pg.display.set_caption('A Game')
    screen.fill('white')
    I.pg.display.flip()
    clock = I.pg.time.Clock()
    run_game(screen, clock)

def run_game(screen, clock):
    startup_clear()
    running = True  # if set to false game doesn't start and window doesn't open
    clicked_button = ""
    screen.fill("white")
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
                            Ff.button_click_render_down(screen, value, 1, S.PATHS["Empty_button_frame"])
                            Ff.display_text(screen, key, 30,
                                            (buttons[key + "_text"].left, buttons[key + "_text"].top * 1.005), "black")
                            clicked_button = key
                        elif key == "Start Game":
                            Ff.button_click_render_down(screen, value, 1, S.PATHS["Empty_button_frame"])
                            Ff.display_text(screen, key, 30,
                                            (buttons[key + "_text"].left, buttons[key + "_text"].top * 1.005), "black")
                            clicked_button = key
                        elif key == "Settings":
                            Ff.button_click_render_down(screen, value, 1, S.PATHS["Empty_button_frame"])
                            Ff.display_text(screen, key, 30,
                                            (buttons[key + "_text"].left, buttons[key + "_text"].top * 1.005), "black")
                            clicked_button = key
                        I.pg.display.flip()
            if event.type == I.pg.MOUSEBUTTONUP and (S.MAIN_MENU):
                pos = I.pg.mouse.get_pos()
                for key, value in buttons.items():
                    if value.collidepoint(pos[0], pos[1]) and not I.pg.mouse.get_pressed()[0]:
                        if key == "Exit" and clicked_button == key:
                            Ff.button_click_render_down(screen, value, 0, S.PATHS["Empty_button_frame"])
                            I.pg.display.flip()
                            running = False
                            S.MAIN_MENU = False
                        elif key == "Start Game" and clicked_button == key:
                            Ff.button_click_render_down(screen, value, 0, S.PATHS["Empty_button_frame"])
                            I.pg.display.flip()
                            S.MAIN_MENU = False
                            CB.Character_Selection(screen)

                            if S.PLAY:

                                with open('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", 'r') as file:
                                    lines = file.readlines()  # Read all lines into a list

                                # Get the last line
                                last_line = lines[-1].strip()  # Remove any trailing newline characters
                                # Check if the last line starts with "Spawn:"
                                if last_line.startswith("Spawn:"):
                                    map_name = last_line[7:].split(":")[0]
                                    I.info.ENTRY_POS = last_line[7:].split(":")[1:3]
                                    I.info.OFFSCREEN = last_line[7:].split(":")[3:5]

                                # map_name =
                                rooms = I.rooms.Room()
                                rooms.select_room(map_name)
                                I.info.CURRENT_ROOM = {"name": map_name, "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": rooms.type}
                                Play.Start(screen, clock, rooms)

                        elif key == "Settings" and clicked_button == key:
                            Ff.button_click_render_down(screen, value, 0, S.PATHS["Empty_button_frame"])
                            I.pg.display.flip()
                            S.MAIN_MENU = False
                            SB.Settings(screen)

                    elif clicked_button == key:
                        Ff.button_click_render_down(screen, value, 0, S.PATHS["Empty_button_frame"])
                        Ff.display_text(screen, key, 30, (buttons[key + "_text"].left, buttons[key + "_text"].top),
                                        "black")
                        I.pg.display.flip()
                        clicked_button = ""
        clock.tick(S.FRAMERATE)  # limits FPS to 60
        if S.RESTART:
            running = False
    if not S.RESTART:
        I.pg.quit()



