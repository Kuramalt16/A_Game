import os.path

from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S

S_LEFT = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 5)
S_TOP = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / 2.2)
S_F_WIDTH = S.SCREEN_WIDTH - (2 * S_LEFT)
S_F_HEIGHT = S.SCREEN_HEIGHT / 10 * 9

B_LEFT = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 6)
B_TOP1 = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / (10 / 3))
B_TOP2 = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / 10)
B_TOP3 = S.SCREEN_HEIGHT / 2 + (S.SCREEN_HEIGHT / 10)
BUTTON_WIDTH = S.SCREEN_WIDTH - (2 * B_LEFT)
BUTTON_HEIGHT = S.SCREEN_HEIGHT / 10

L_ARR_L = S_LEFT + S_F_WIDTH / 4 - S_F_WIDTH / 10
R_ARR_L = S_LEFT + S_F_WIDTH * 0.8
ARR_H = S_F_HEIGHT / 12
ARR_W = S_F_WIDTH / 20

body_sizes = [S_LEFT + S_F_WIDTH / 4, S_TOP + S_F_HEIGHT / 6, S_F_WIDTH / 2, S_F_HEIGHT / 2]

path = 'static/images/'

path_races = path + 'Race/'
def Char_Select(screen):
    buttons = {}
    frame_main_menu = Ff.add_image_to_screen(screen, path + 'Frame_main_menu.png', [S_LEFT, S_TOP, S_F_WIDTH, S_F_HEIGHT])
    buttons["New"] = Ff.add_image_to_screen(screen, path + 'Empty.png', [B_LEFT, B_TOP1, BUTTON_WIDTH, BUTTON_HEIGHT])
    if number_of_chars() > 9:
        color = "grey"
    else:
        color = "black"
    buttons["New_text"] = Ff.display_text(screen, "New", 30, (B_LEFT + BUTTON_WIDTH / 2.5, B_TOP1 + BUTTON_HEIGHT / 4), color)
    buttons["New"] = buttons["New"].union(buttons["New_text"])

    buttons["Load"] = Ff.add_image_to_screen(screen, path + 'Empty.png',[B_LEFT, B_TOP2, BUTTON_WIDTH, BUTTON_HEIGHT])
    if load_exists():
        color = "black"
    else:
        color = "grey"
    buttons["Load_text"] = Ff.display_text(screen, "Load", 30, (B_LEFT + BUTTON_WIDTH / 2.5, B_TOP2 + BUTTON_HEIGHT / 4), color)
    buttons["Load"] = buttons["Load"].union(buttons["Load_text"])

    buttons["Main Menu"] = Ff.add_image_to_screen(screen, path + 'Empty.png',[B_LEFT, B_TOP3, BUTTON_WIDTH, BUTTON_HEIGHT])
    buttons["Main Menu_text"] = Ff.display_text(screen, "Main Menu", 30, (B_LEFT + BUTTON_WIDTH / 4, B_TOP3 + BUTTON_HEIGHT / 4), "black")
    buttons["Main Menu"] = buttons["Main Menu"].union(buttons["Main Menu_text"])
    I.pg.display.flip()
    return buttons

def number_of_chars():
    entries = os.listdir("static/data/created_characters/")

    # Filter out only directories
    folders = [entry for entry in entries if os.path.isdir(os.path.join("static/data/created_characters/", entry))]

    # Return the count of directories
    return len(folders)

def load_exists():
    return os.path.exists("static/data/created_characters/")

def Character_creation(screen, option, extra):
    buttons = {}
    profile = {2: "_Back", 3: "_Side", 1: "_Side1", 0: ""}
    if option != "save":
        frame_main_menu = Ff.add_image_to_screen(screen, path + 'Frame_main_menu.png', [S_LEFT, S_TOP, S_F_WIDTH, S_F_HEIGHT])
    if option == "Gender":
        buttons["Boy"] = Ff.add_image_to_screen(screen, path + 'Boy.png',[frame_main_menu.right - frame_main_menu.w * 0.4 , frame_main_menu.top + frame_main_menu.h * 0.3, S_F_WIDTH / 3, S_F_HEIGHT / 3])
        buttons["Girl"] = Ff.add_image_to_screen(screen, path + 'Girl.png',[frame_main_menu.left + frame_main_menu.w * 0.1 , frame_main_menu.top + frame_main_menu.h * 0.35, S_F_WIDTH / 3, S_F_HEIGHT / 3])
    elif option == "Name":
        if extra.isalpha():
            if I.os.path.exists('static/data/created_characters/' + extra):
                Ff.display_text(screen, "CHARACTER ALREADY EXISTS", 16, (S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 4),"black")
            else:
                Ff.display_text(screen, "HIT ENTER AFTER COMPLETION", 16,(S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 4), "black")
                buttons["ENTER"] = Ff.add_image_to_screen(screen, path + 'Empty.png',[frame_main_menu.left + frame_main_menu.w * 0.25,frame_main_menu.top + frame_main_menu.h * 0.7, S_F_WIDTH / 2,S_F_HEIGHT / 10])
                Ff.display_text(screen, "ENTER", 30, (buttons["ENTER"].left + buttons["ENTER"].left / 10, buttons["ENTER"].top * 1.025), "black")
        Ff.display_text(screen, "NAME: ", 30, (S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 2), "black")
        Ff.display_text(screen, extra, 30, (S.SCREEN_WIDTH / 2.2, S.SCREEN_HEIGHT / 2), "black")
    elif option == "Age":
        if extra.isdigit():
            Ff.display_text(screen, "HIT ENTER AFTER ENTERING", 16,(S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 4), "black")
            Ff.display_text(screen, "CHARACTER'S AGE", 16,(S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 3), "black")
            buttons["ENTER"] = Ff.add_image_to_screen(screen, path + 'Empty.png',[frame_main_menu.left + frame_main_menu.w * 0.25,frame_main_menu.top + frame_main_menu.h * 0.7, S_F_WIDTH / 2,S_F_HEIGHT / 10])
            Ff.display_text(screen, "ENTER", 30, (buttons["ENTER"].left + buttons["ENTER"].left / 10, buttons["ENTER"].top * 1.025), "black")
        else:
            Ff.display_text(screen, "TYPE ONLY NUMBERS", 16,(S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 4), "black")
        Ff.display_text(screen, "AGE: ", 30, (S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 2), "black")
        Ff.display_text(screen, extra, 30, (S.SCREEN_WIDTH / 2.2, S.SCREEN_HEIGHT / 2), "black")
    elif option == "Race":
        left = frame_main_menu.left + frame_main_menu.w / 12
        top = frame_main_menu.top + frame_main_menu.h / 12
        for race in I.A.RACE:
            buttons[race + "_" + I.TD.Gender] = Ff.add_image_to_screen(screen, S.PATHS[race + "_" + I.TD.Gender],[left, top, S_F_WIDTH / 4, S_F_HEIGHT / 4])
            text = Ff.display_text(screen, race, 10, (left, buttons[race + "_" + I.TD.Gender].bottom), "black")
            left += frame_main_menu.w / 3
            I.pg.display.update(text)
            I.pg.display.update(buttons[race + "_" + I.TD.Gender])
    elif option == "Skin":
        if extra != "":
            # d = I.CharacterData()
            # d.update_orientation(extra)
            # Ff.draw_character(screen, d, I.TD.Gender, I.TD.Race.split("_")[0], [])
        # else:
            # Ff.draw_character(screen, I.CharacterData(), I.TD.Gender, I.TD.Race.split("_")[0], []) # takes 24.5 ms max Fuck

            buttons["Body"] = Ff.add_image_to_screen(screen, S.PATHS[I.TD.Race], body_sizes)  # takes 0.67 ms max

        for key, color in I.A.DEFAULT_TEMP.items():
            if key in ["Eyes", "Skin", "Skin2"]:
                iteration = Ff.find_iteration(list(I.A.color_mappings.get(key, {}).values()), key)
                if iteration != None:
                # d = I.CharacterData()
                # d.classic_coloring_tool(key, color, 1)
                # Ff.draw_character(screen, d, I.TD.Gender, I.TD.Race.split("_")[0], key)  # takes 24.5 ms max Fuck

                    Ff.Coloring_tool(screen, buttons["Body"], key, iteration, 1)

        buttons = generate_arrow_buttons(option, buttons, screen)
    elif option == "Clothes":

        if extra != "":
            buttons["Body"] = Ff.add_image_to_screen(screen, S.PATHS[I.TD.Race + profile[extra]], body_sizes)
        else:
            buttons["Body"] = Ff.add_image_to_screen(screen, S.PATHS[I.TD.Race], body_sizes)

        # 182 ms
        for key in I.TD.Skin.keys():  # colors the skin and eyes of the previously chosen colors
            iteration = Ff.find_iteration(list(I.A.color_mappings.get(key, {}).values()), key)
            if iteration != None:
                Ff.Coloring_tool(screen, buttons["Body"], key, iteration, 1)

        # 0.9 ms; 2.4 ms if flipping side
        for key, value in I.TD.Appearance.items():
            Ff.styling_tool_path(key, screen, buttons["Body"], value, profile[extra])


        # 233 ms
        for key, value in I.TD.Appearance_color.items():
            if "Color" in key and "Right" not in key:
                name = key[:10]
                iteration = Ff.find_iteration(list(I.A.color_mappings.get(name, {}).values()), name)
                if iteration != None:
                    Ff.Coloring_tool(screen, buttons["Body"], name, iteration, 1)

        # 5 ms
        buttons = generate_arrow_buttons(option, buttons, screen)
    if option == "save":
        screen.fill("white")
        buttons["Body"] = Ff.add_image_to_screen(screen, S.PATHS[I.TD.Race + profile[extra]], body_sizes)
        for key in I.TD.Skin.keys():  # colors the skin and eyes of the previously chosen colors
            iteration = Ff.find_iteration(list(I.A.color_mappings.get(key, {}).values()), key)
            Ff.Coloring_tool(screen, buttons["Body"], key, iteration, 1)

        for key, value in I.TD.Appearance.items():
            if profile[extra] == "_Back" and key != "Hair":
                profile[extra] = ""
            Ff.styling_tool_path(key, screen, buttons["Body"], value, profile[extra])
        for key, value in I.TD.Appearance_color.items():
            if "Color" in key:
                name = key[:10]
                iteration = Ff.find_iteration(list(I.A.color_mappings.get(name, {}).values()), name)
                if iteration != None:
                    Ff.Coloring_tool(screen, buttons["Body"], name, iteration, 1)
        I.TD.Char_Rect = buttons["Body"]
    else:
        buttons["Back"] = Ff.add_image_to_screen(screen, path + 'Back.png',[frame_main_menu.left + frame_main_menu.w * 0.25 , frame_main_menu.top + frame_main_menu.h * 0.8, S_F_WIDTH / 2, S_F_HEIGHT / 10])
    I.pg.display.flip()
    return buttons

def generate_arrow_buttons(option, buttons, screen):
    if option == "Clothes":
        buttons["Hair_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png",[L_ARR_L, body_sizes[1] * 0.8, ARR_W, ARR_H])
        # buttons["Hair_Left"] = Ff.add_image_to_screen_dif_rect(screen, path + "Left_arrow.png",[L_ARR_L, body_sizes[1] * 0.8, ARR_W, ARR_H], (ARR_W * 0.8, ARR_H * 0.8))
        buttons["Hair_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png",[R_ARR_L, body_sizes[1] * 0.8, ARR_W, ARR_H])
        buttons["Shir_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png",[L_ARR_L, body_sizes[1] * 1.4, ARR_W, ARR_H])
        buttons["Shir_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png",[R_ARR_L, body_sizes[1] * 1.4, ARR_W, ARR_H])
        buttons["Slee_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png",[L_ARR_L, body_sizes[1] * 1.8, ARR_W, ARR_H])
        buttons["Slee_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png",[R_ARR_L, body_sizes[1] * 1.8, ARR_W, ARR_H])
        buttons["Pant_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png",[L_ARR_L, body_sizes[1] * 2.3, ARR_W, ARR_H])
        buttons["Pant_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png",[R_ARR_L, body_sizes[1] * 2.3, ARR_W, ARR_H])
        buttons["Shoe_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png",[L_ARR_L, body_sizes[1] * 2.8, ARR_W, ARR_H])
        buttons["Shoe_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png",[R_ARR_L, body_sizes[1] * 2.8, ARR_W, ARR_H])
        buttons["Color_Hair_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png", [L_ARR_L - 50, body_sizes[1] * 0.8, ARR_W, ARR_H])
        buttons["Color_Hair_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png", [R_ARR_L + 50, body_sizes[1] * 0.8, ARR_W, ARR_H])
        buttons["Color_Shir_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png",[L_ARR_L - 50, body_sizes[1] * 1.4, ARR_W, ARR_H])
        buttons["Color_Shir_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png",[R_ARR_L + 50, body_sizes[1] * 1.4, ARR_W, ARR_H])
        buttons["Color_Pant_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png",[L_ARR_L - 50, body_sizes[1] * 2.3, ARR_W, ARR_H])
        buttons["Color_Pant_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png",[R_ARR_L + 50, body_sizes[1] * 2.3, ARR_W, ARR_H])
        buttons["Color_Shoe_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png",[L_ARR_L - 50, body_sizes[1] * 2.8, ARR_W, ARR_H])
        buttons["Color_Shoe_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png",[R_ARR_L + 50, body_sizes[1] * 2.8, ARR_W, ARR_H])
        buttons["Turn_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png",[L_ARR_L, S_TOP + S_F_HEIGHT * 0.7, ARR_W,ARR_H])
        buttons["Turn_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png",[R_ARR_L, S_TOP + S_F_HEIGHT * 0.7, ARR_W,ARR_H])
        buttons["ENTER"] = Ff.add_image_to_screen(screen, path + 'Empty.png',[S_LEFT + S_F_WIDTH * 0.25, S_TOP + S_F_HEIGHT * 0.7, S_F_WIDTH / 2,S_F_HEIGHT / 10])
        Ff.display_text(screen, "ENTER", 30,(buttons["ENTER"].left + buttons["ENTER"].left / 10, buttons["ENTER"].top * 1.025), "black")
    else:
        buttons["Skin_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png", [L_ARR_L, body_sizes[1] * 2, ARR_W, ARR_H])
        buttons["Skin_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png", [R_ARR_L, body_sizes[1] * 2, ARR_W, ARR_H])
        buttons["Eyes_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png",[L_ARR_L, body_sizes[1], ARR_W, ARR_H])
        buttons["Eyes_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png",[R_ARR_L, body_sizes[1], ARR_W, ARR_H])
        buttons["ENTER"] = Ff.add_image_to_screen(screen, path + 'Empty.png',[S_LEFT + S_F_WIDTH * 0.25, S_TOP + S_F_HEIGHT * 0.7, S_F_WIDTH / 2,S_F_HEIGHT / 10])
        Ff.display_text(screen, "ENTER", 30, (buttons["ENTER"].left + buttons["ENTER"].left / 10, buttons["ENTER"].top * 1.025), "black")
        buttons["Turn_Left"] = Ff.add_image_to_screen(screen, path + "Left_arrow.png", [L_ARR_L, S_TOP + S_F_HEIGHT * 0.7, ARR_W, ARR_H])
        buttons["Turn_Right"] = Ff.add_image_to_screen(screen, path + "Right_arrow.png", [R_ARR_L, S_TOP + S_F_HEIGHT * 0.7, ARR_W, ARR_H])

    return buttons

def new_character_creation(screen, option, extra, d):
    buttons = {}
    frame_main_menu = Ff.add_image_to_screen(screen, path + 'Frame_main_menu.png',[S_LEFT, S_TOP, S_F_WIDTH, S_F_HEIGHT])
    if option == "Gender":
        buttons["Boy"] = Ff.add_image_to_screen(screen, path + 'Boy.png',[frame_main_menu.right - frame_main_menu.w * 0.4 , frame_main_menu.top + frame_main_menu.h * 0.3, S_F_WIDTH / 3, S_F_HEIGHT / 3])
        buttons["Girl"] = Ff.add_image_to_screen(screen, path + 'Girl.png',[frame_main_menu.left + frame_main_menu.w * 0.1 , frame_main_menu.top + frame_main_menu.h * 0.35, S_F_WIDTH / 3, S_F_HEIGHT / 3])
    elif option == "Name":
        if extra.isalpha():
            if I.os.path.exists('static/data/created_characters/' + extra):
                Ff.display_text(screen, "CHARACTER ALREADY EXISTS", 16, (S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 4),"black")
            else:
                Ff.display_text(screen, "HIT ENTER AFTER COMPLETION", 16,(S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 4), "black")
                buttons["ENTER"] = Ff.add_image_to_screen(screen, path + 'Empty.png',[frame_main_menu.left + frame_main_menu.w * 0.25,frame_main_menu.top + frame_main_menu.h * 0.7, S_F_WIDTH / 2,S_F_HEIGHT / 10])
                Ff.display_text(screen, "ENTER", 30, (buttons["ENTER"].left + buttons["ENTER"].left / 10, buttons["ENTER"].top * 1.025), "black")
        Ff.display_text(screen, "NAME: ", 30, (S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 2), "black")
        Ff.display_text(screen, extra, 30, (S.SCREEN_WIDTH / 2.2, S.SCREEN_HEIGHT / 2), "black")
    elif option == "Age":
        if extra.isdigit():
            Ff.display_text(screen, "HIT ENTER AFTER COMPLETION", 16,(S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 4), "black")
            buttons["ENTER"] = Ff.add_image_to_screen(screen, path + 'Empty.png',[frame_main_menu.left + frame_main_menu.w * 0.25,frame_main_menu.top + frame_main_menu.h * 0.7, S_F_WIDTH / 2,S_F_HEIGHT / 10])
            Ff.display_text(screen, "ENTER", 30, (buttons["ENTER"].left + buttons["ENTER"].left / 10, buttons["ENTER"].top * 1.025), "black")
        else:
            Ff.display_text(screen, "TYPE ONLY NUMBERS", 16,(S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 4), "black")
        Ff.display_text(screen, "AGE: ", 30, (S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 2), "black")
        Ff.display_text(screen, extra, 30, (S.SCREEN_WIDTH / 2.2, S.SCREEN_HEIGHT / 2), "black")
    elif option == "Race":
        left = frame_main_menu.left + frame_main_menu.w / 12
        top = frame_main_menu.top + frame_main_menu.h / 12
        for race in I.A.RACE:
            buttons[race + "_" + I.TD.Gender] = Ff.add_image_to_screen(screen, S.PATHS[race + "_" + I.TD.Gender],[left, top, S_F_WIDTH / 4, S_F_HEIGHT / 4])
            text = Ff.display_text(screen, race, 10, (left, buttons[race + "_" + I.TD.Gender].bottom), "black")
            left += frame_main_menu.w / 3
            I.pg.display.update(text)
            I.pg.display.update(buttons[race + "_" + I.TD.Gender])

    elif option == "Skin":
        # d.update_orientation(extra)
        for key, color in I.A.DEFAULT_TEMP.items():
            d.classic_coloring_tool(key, color, 0)
        d.update_orientation(extra, 0)
        Ff.draw_character(screen, d, I.TD.Gender, I.TD.Race.split("_")[0], [])
        buttons = generate_arrow_buttons(option, buttons, screen)

    elif option == "Clothes":
        # d.update_orientation(extra)
        for key, color in I.A.DEFAULT_TEMP.items():
            d.classic_coloring_tool(key, color, 0)
        for key, value in I.TD.Appearance.items():
            d.clothing_select(key, value)
        d.update_orientation(extra, 0)
        Ff.draw_character(screen, d, I.TD.Gender, I.TD.Race.split("_")[0], [])
        buttons = generate_arrow_buttons(option, buttons, screen)
    I.TD.Char_Rect = [S_LEFT + S_F_WIDTH / 4, S_TOP + S_F_HEIGHT / 10, S_F_WIDTH / 2, S_F_HEIGHT / 1.5]
    buttons["Back"] = Ff.add_image_to_screen(screen, path + 'Back.png',[frame_main_menu.left + frame_main_menu.w * 0.25,frame_main_menu.top + frame_main_menu.h * 0.8, S_F_WIDTH / 2,S_F_HEIGHT / 10])
    I.pg.display.flip()
    return buttons