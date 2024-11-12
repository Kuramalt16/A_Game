from Values import Settings as S
from utils import Frequent_functions as Ff, Imports as I
from Render import Character_selection_render as cr, Load_render as lr
def Character_Selection(screen):
    select = False
    clicked_button = ""
    screen.fill("white")
    I.pg.display.flip()
    buttons = cr.Char_Select(screen)
    while not select:
        if S.START_APP:
            buttons = cr.Char_Select(screen)
            S.START_APP = False
        for event in I.pg.event.get():
            if event.type == I.pg.QUIT:
                select = True
            pos = I.pg.mouse.get_pos()
            if event.type == I.pg.MOUSEBUTTONDOWN and not S.BUSY:
                for key, value in buttons.items():
                    if value.collidepoint(pos[0], pos[1]) and I.pg.mouse.get_pressed()[0]:
                        if key == "New" and cr.number_of_chars() < 9:
                            Ff.button_click_render_down(screen, value, 1, S.PATHS["Empty_button_frame"])
                            Ff.display_text(screen, key, 30, (buttons[key + "_text"].left, buttons[key + "_text"].top * 1.01), "black")
                            clicked_button = key
                        elif key == "Load" and cr.load_exists():
                            Ff.button_click_render_down(screen, value, 1, S.PATHS["Empty_button_frame"])
                            Ff.display_text(screen, key, 30, (buttons[key + "_text"].left, buttons[key + "_text"].top * 1.005), "black")
                            clicked_button = key
                        elif key == "Main Menu":
                            Ff.button_click_render_down(screen, value, 1, S.PATHS["Empty_button_frame"])
                            Ff.display_text(screen, key, 30, (buttons[key + "_text"].left, buttons[key + "_text"].top * 1.005), "black")
                            clicked_button = key
                        I.pg.display.flip()
            if event.type == I.pg.MOUSEBUTTONUP and not S.BUSY:
                for key, value in buttons.items():
                    if value.collidepoint(pos[0], pos[1]) and not I.pg.mouse.get_pressed()[0]:
                        if key == "New" and clicked_button == key:
                            Ff.button_click_render(screen, value, 0, "Empty")
                            Ff.display_text(screen, key, 30,(buttons[key + "_text"].left, buttons[key + "_text"].top), "black")
                            I.pg.display.flip()
                            S.BUSY = True
                            Create_Character(screen)

                            if I.info.SELECTED_CHARACTER != "":  # Runs the game without user needing to select the character again
                                S.PLAY = True
                                return

                        elif key == "Load" and clicked_button == key:
                            Ff.button_click_render(screen, value, 0, "Empty")
                            Ff.display_text(screen, key, 30,(buttons[key + "_text"].left, buttons[key + "_text"].top), "black")
                            I.pg.display.flip()
                            S.BUSY = True
                            show_load(screen)
                            select = True
                        elif key == "Main Menu" and clicked_button == key:
                            Ff.button_click_render(screen, value, 0, "Empty")
                            Ff.display_text(screen, key, 30, (buttons[key + "_text"].left, buttons[key + "_text"].top), "black")
                            I.pg.display.flip()
                            select = True
                    elif key == clicked_button:
                        Ff.button_click_render(screen, value, 0, "Empty")
                        Ff.display_text(screen, key, 30,(buttons[key + "_text"].left, buttons[key + "_text"].top), "black")
                        I.pg.display.flip()
                        clicked_button = ""

    S.MAIN_MENU = True
    S.START_APP = True


def Create_Character(screen):
    character, arrow_value = create_char_init()
    cancel = False
    d = I.CharacterData()
    for trait in character.keys():
        save = False
        if cancel:
            break
        text_buffer = ""
        screen.fill("white")
        extra = ""
        if trait == "Clothes":
            extra = arrow_value["Turn"]
        # character[trait] = cr.Character_creation(screen, trait, extra)
        character[trait] = cr.new_character_creation(screen, trait, extra, d)
        while not save and not cancel:
            for event in I.pg.event.get():
                pos = I.pg.mouse.get_pos()
                if event.type == I.pg.MOUSEBUTTONDOWN:
                    clicked_button = handle_mouse_button_down(screen, character, trait, pos)
                elif event.type == I.pg.MOUSEBUTTONUP:
                    save, cancel, arrow_value = handle_mouse_button_up(screen, character, trait, pos, clicked_button, text_buffer, arrow_value, d)
                elif event.type == I.pg.TEXTINPUT and trait in ["Name", "Age"]:
                    length = 0
                    for text in text_buffer:
                        if text in "wmxQRO":
                            length += 2
                        elif text in "il":
                            length += 0.3
                        elif text in "ft":
                            length += 0.5
                        else:
                            length += 1
                    if length < 10:
                        text_buffer += event.text
                    character[trait] = cr.Character_creation(screen, trait, text_buffer)
                elif event.type == I.pg.KEYDOWN and trait in ["Name", "Age"]:
                    text_buffer, save = handle_keydown(event, text_buffer, trait, character, screen)
                I.pg.display.flip()
    if not cancel:
        # Save_Character(character, screen)
        Save_Character_Dict(d, screen, character)
    S.BUSY = False
    S.START_APP = True

def take_pictures(value, screen, side):
    sub_surface = screen.subsurface(I.TD.Char_Rect)
    I.os.makedirs('static/data/created_characters/' + value["Name"], exist_ok=True)
    I.pg.image.save(sub_surface, "static/data/created_characters/" + value["Name"] + "/" + value["Name"] + side + ".png")
    Ff.remove_white_pixels("static/data/created_characters/" + value["Name"] + "/" + value["Name"] + side + ".png")
    if side == "Front":
        now = I.datetime.now()
        with open("static/data/created_characters/" + value["Name"] + "/" + value["Name"] + ".txt", 'w') as file:
            file.write("Name: " + value["Name"] + "\n\n" +
                       "Gender: " + value["Gender"] + "\n" +
                       "Age: " + value["Age"] + "\n" +
                       "Race: " + str(value["Race"].split("_")[0]) + "\n\n" +
                       "Eyes: " + str(value["Skin"]["Eyes"]) + "\n" +
                       "Skin: " + str(value["Skin"]["Skin"]) + "\n" +
                       "Skin2: " + str(value["Skin"]["Skin2"]) + "\n\n" +
                       "Hair: " + str(value["Clothes"]["Hair"]) + "\n" +
                       "Shir: " + str(value["Clothes"]["Shir"]) + "\n" +
                       "Pant: " + str(value["Clothes"]["Pant"]) + "\n" +
                       "Shoe: " + str(value["Clothes"]["Shoe"]) + "\n\n" +
                       "Color_Hair: " + str(value["Clothes"]["Color_Hair"]) + "\n" +
                       "Color_Shir: " + str(value["Clothes"]["Color_Shir"]) + "\n" +
                       "Color_Pant: " + str(value["Clothes"]["Color_Pant"]) + "\n" +
                       "Color_Shoe: " + str(value["Clothes"]["Color_Shoe"]) + "\n\n" +

                       "Last Save: " + str(now.strftime('%Y/%m/%d %H:%M')) + "\n\n" +

                       "\n\n" +

                       "Level: " + "1" + "\n" +
                       "Experience: " + "0" + "\n" +
                       "Health: " + "10" + "\n" +
                       "Mana: " + "10" + "\n" +
                       "Exhaustion: " + "100" + "\n\n" +
                       "Gold: " + "0" + "\n\n" +
                       "Alignment: " + "Unaligned" + "\n\n" +
                       "Class: " + "Not trained" + "\n\n" +
                       "Backpack: " + "Gold__0__0__0" + "\n\n" +
                       "Spells: " + "" + "\n\n" +
                       "Dialog: " + "" + "\n\n" +
                       "Quests: " + "[]" + "\n\n" +
                       "Completed_quests: " + "[]" + "\n\n" +
                       "Containers: " + "" + "\n\n" +
                       "Titles: " + "" + "\n\n" +
                       "Save_point: " + "Village_10_10:330:1:0:0" + "\n\n" +
                       "DEATH_SAVE: " + "" + "\n\n" +
                       "Criminal: " + "" + "\n\n" +
                       "Spawn: " + "Village_10_10:330:1:0:0"
                       )

def Save_Character_Dict(d, screen, character):
    save_dic = {0: "Front", 1: "Front1", 2: "Front2", 3: "Left", 4: "Left1", 5: "Left2", 6: "Back", 7: "Back1", 8: "Back2", 9: "Right", 10: "Right1", 11: "Right2"}
    for turn, orientation in save_dic.items():
        screen.fill("white")

        for key, color in I.A.DEFAULT_TEMP.items():
            d.classic_coloring_tool(key, color, 0)
        for key, value in I.TD.Appearance.items():
            d.clothing_select(key, value)
        d.update_orientation(turn, 1)
        Ff.draw_character(screen, d, I.TD.Gender, I.TD.Race.split("_")[0], [])
        take_pictures(character, screen, orientation)
    I.info.SELECTED_CHARACTER = I.TD.Name
def Save_temp_Character(value):
    value["Skin"] = {"Eyes": I.A.DEFAULT_TEMP["Eyes"], "Skin": I.A.DEFAULT_TEMP["Skin"],"Skin2": I.A.DEFAULT_TEMP["Skin2"]}
    I.TD.Gender = value["Gender"]
    I.TD.Name = value["Name"]
    I.TD.Age = value["Age"]
    I.TD.Race = value["Race"]
    I.TD.Skin = value["Skin"]
    if value["Clothes"] != "":
        I.TD.Appearance_color = value["Clothes"]

def handle_mouse_button_down(screen, character, trait, pos):
    for key, value in character[trait].items():
        if value.collidepoint(pos) and I.pg.mouse.get_pressed()[0]:
            if key not in ["ENTER", "Body"]:
                # deals with all keys apart texted buttons
                Ff.button_click_render_down(screen, value, 1, S.PATHS[key])
                return key
            elif key == "ENTER":
                # deals with texted buttons
                Ff.button_click_render_down(screen, value, 1, S.PATHS[key])
                Ff.display_text(screen, key, 30,(character[trait][key].left * 1.1, character[trait][key].top * 1.025 + 2),"black")
                return key
    return ""

def handle_mouse_button_up(screen, character, trait, pos, clicked_button, text_buffer, arrow_value, d):
    save = False
    cancel = False
    for key, value in character[trait].items():
        if value.collidepoint(pos) and not I.pg.mouse.get_pressed()[0]:
            if "Left" in key and clicked_button == key or "Right" in key and clicked_button == key:
                if "Left" in key:
                    # Left Arrow
                    name = key[:-5]
                    arrow_value[name] += 1
                else:
                    # Right Arrow
                    name = key[:-6]
                    arrow_value[name] -= 1
                if name == "Skin":
                    # two colors need changing
                    if arrow_value[name] > len(I.A.color_mappings.get(name, {}).values())-1:
                        arrow_value[name] = 0
                    if arrow_value[name] < 0:
                        arrow_value[name] = len(I.A.color_mappings.get(name, {}).values()) - 1
                    I.A.DEFAULT_TEMP[name] = list(I.A.color_mappings.get(name, {}).values())[arrow_value[name]]
                    I.A.DEFAULT_TEMP[name+"2"] = list(I.A.color_mappings.get(name+"2", {}).values())[arrow_value[name]]
                    cr.new_character_creation(screen, trait, arrow_value["Turn"], d)
                elif name in ["Hair", "Shir", "Pant", "Shoe", "Slee"]:
                    # Change clothes
                    # 0.85 ms

                    # arrow_value[name], dont_use = Ff.styling_tool(name, screen, character[trait]["Body"], arrow_value[name])
                    # 438 ms improved to 188 ms
                    # character[trait] = cr.Character_creation(screen, trait, arrow_value["Turn"])

                    if arrow_value[name] > I.A.clothing_count[name]:
                        arrow_value[name] = 0
                    elif arrow_value[name] < 0:
                        arrow_value[name] = I.A.clothing_count[name]

                    I.TD.Appearance[name] = arrow_value[name]
                    character[trait] = cr.new_character_creation(screen, trait, "", d)
                    # 7.3 us
                    Save_temp_Character(character)
                    # overall 672 ms sec
                elif name == "Turn":
                    # arrow_value[name] = (arrow_value[name] + 12) % 12
                    arrow_value[name] = (arrow_value[name] + 4) % 4
                    d.orientation = arrow_value[name]
                    character[trait] = cr.new_character_creation(screen, trait, d.orientation, d)
                    # character[trait] = cr.Character_creation(screen, trait, arrow_value[name])
                else:
                    # single color change
                    if arrow_value[name] > len(I.A.color_mappings.get(name, {}).values()) - 1:
                        arrow_value[name] = 0
                    elif arrow_value[name] < 0:
                        arrow_value[name] = len(I.A.color_mappings.get(name, {}).values()) - 1
                    I.A.DEFAULT_TEMP[name] = list(I.A.color_mappings.get(name, {}).values())[arrow_value[name]]
                    cr.new_character_creation(screen, trait, "", d)

                    # arrow_value[name] = Ff.Coloring_tool(screen, character[trait]["Body"], name, arrow_value[name], 0) # takes 1.5 ms fuck. this is faster.

                Ff.button_click_render_down(screen, value, 0, S.PATHS[key])
            elif key not in ["ENTER", "Back"] and clicked_button == key:
                # Possibly could be removed if used with enter instead. check out whenever
                character[trait] = key
                Save_temp_Character(character)
                save = True
                Ff.button_click_render_down(screen, value, 0, S.PATHS[key])
            elif key == "Back" and clicked_button == key:
                cancel = True
                Ff.button_click_render_down(screen, value, 0, S.PATHS[key])
            elif key == "ENTER" and clicked_button == key:
                # Only comes here when clicked enter
                Ff.button_click_render_down(screen, value, 0, S.PATHS[key])
                Ff.display_text(screen, key, 30, (character[trait]["ENTER"].left + character[trait]["ENTER"].left / 10,character[trait]["ENTER"].top * 1.025), "black")
                if trait in ["Name", "Age"]:
                    # Saves name and age
                    character[trait] = text_buffer
                elif trait in ["Clothes"]:
                    character[trait] = {"Hair": "Hair_" + str(arrow_value["Hair"]),
                                        "Shir": "Shir_" + str(arrow_value["Shir"]),
                                        "Pant": "Pant_" + str(arrow_value["Pant"]),
                                        "Shoe": "Shoe_" + str(arrow_value["Shoe"]),
                                        "Color_Hair": I.A.DEFAULT_TEMP["Color_Hair"],
                                        "Color_Shir": I.A.DEFAULT_TEMP["Color_Shir"],
                                        "Color_Pant": I.A.DEFAULT_TEMP["Color_Pant"],
                                        "Color_Shoe": I.A.DEFAULT_TEMP["Color_Shoe"],
                                        }
                Save_temp_Character(character)
                save = True
        elif key == clicked_button:
            if clicked_button != "ENTER":
                Ff.button_click_render_down(screen, value, 0, S.PATHS[key])
            else:
                Ff.button_click_render_down(screen, value, 0, S.PATHS[key])
                Ff.display_text(screen, key, 30, (character[trait]["ENTER"].left + character[trait]["ENTER"].left / 10,character[trait]["ENTER"].top * 1.025), "black")
            clicked_button = ""
    return save, cancel, arrow_value

def handle_keydown(event, text_buffer, trait, character, screen):
    if event.key == I.pg.K_RETURN or event.key == I.pg.K_KP_ENTER:
        if trait == "Age" and text_buffer.isdigit():
            character[trait] = text_buffer
            return text_buffer, True
        elif trait == "Name" and text_buffer.isalpha():
            character[trait] = text_buffer
            if I.os.path.exists('static/data/created_characters/' + text_buffer):
                return text_buffer, False
            else:
                return text_buffer, True
    elif event.key == I.pg.K_BACKSPACE:
        text_buffer = text_buffer[:-1]
        character[trait] = cr.Character_creation(screen, trait, text_buffer)
        return text_buffer, False
    return text_buffer, False

def create_char_init():
    I.A.DEFAULT_TEMP = S.DEFAULT.copy()
    I.TD.Appearance = {}
    character = {"Gender": "",
                 "Name": "",
                 "Age": "",
                 "Race": "",
                 "Skin": "",
                 "Clothes": ""}
    arrow_value = {"Eyes": 0,
                   "Skin": 0,
                   "Shoe": 0,
                   "Shir": 0,
                   "Slee": 0,
                   "Pant": 0,
                   "Hair": 0,
                   "Color_Hair": 0,
                   "Color_Shir": 0,
                   "Color_Pant": 0,
                   "Color_Shoe": 0,
                   "Turn": 0}
    return character, arrow_value

def show_load(screen):
    cancel = False
    select = False
    key_check = ""
    buttons = lr.load_data(screen)
    while not cancel and not select:
        for event in I.pg.event.get():
            pos = I.pg.mouse.get_pos()
            if event.type == I.pg.MOUSEBUTTONDOWN:
                for key, rect in buttons.items():
                    if rect.collidepoint(pos) and I.pg.mouse.get_pressed()[0]:
                        if key in ["Back"]:
                            key_check = key
                            Ff.button_click_render_down(screen, buttons[key], 1, S.PATHS[key])
                        else:
                            key_check = key
                            Ff.button_click_render_down(screen, buttons[key], 1, 'static/data/created_characters/' + key + "/" + key + "Front.png")
                        I.pg.display.flip()
            elif event.type == I.pg.MOUSEBUTTONUP:
                for key, rect in buttons.items():
                    if rect.collidepoint(pos) and not I.pg.mouse.get_pressed()[0]:
                        if key == key_check:
                            if key == "Back":
                                Ff.button_click_render_down(screen, buttons[key], 0, S.PATHS["Back"])
                                cancel = True
                            else:
                                # characters
                                Ff.button_click_render_down(screen, buttons[key], 0,'static/data/created_characters/' + key + "/" + key + "Front.png")
                                select = True
                                I.info.SELECTED_CHARACTER = key
                            key_check = ""
                    elif key == key_check:
                        if key in ["Back"]:
                            Ff.button_click_render_down(screen, buttons[key], 0, S.PATHS["Back"])
                        else:
                            Ff.button_click_render_down(screen, buttons[key], 0,'static/data/created_characters/' + key + "/" + key + "Front.png")
                        key_check = ""
                    I.pg.display.flip()


    screen.fill("white")
    I.pg.display.flip()
    if select:
        buttons = lr.char_data(screen)
        I.pg.display.flip()
        while select and not cancel:
            for event in I.pg.event.get():
                pos = I.pg.mouse.get_pos()
                if event.type == I.pg.MOUSEBUTTONDOWN:
                    for key, rect in buttons.items():
                        if rect.collidepoint(pos) and I.pg.mouse.get_pressed()[0]:
                            if key in ["Back"]:
                                key_check = key
                                Ff.button_click_render_down(screen, buttons[key], 1, S.PATHS[key])
                            elif key == "Delete":
                                key_check = key
                                Ff.button_click_render_down(screen, buttons[key], 1, S.PATHS[key])
                                Ff.display_text(screen, key, 30, (buttons["Delete"].left + buttons["Delete"].left / 7, buttons["Delete"].top * 1.025), "Red" )
                            else:
                                lr.render_face(screen, 1)
                                key_check = key
                                # render character based on their allignment
                            I.pg.display.flip()
                elif event.type == I.pg.MOUSEBUTTONUP:
                    for key, rect in buttons.items():
                        if rect.collidepoint(pos) and not I.pg.mouse.get_pressed()[0]:
                            if key == key_check:
                                if key == "Back":
                                    Ff.button_click_render_down(screen, buttons[key], 0, S.PATHS[key])
                                    cancel = True
                                    I.info.SELECTED_CHARACTER = ""

                                elif key == "Delete":
                                    Ff.button_click_render_down(screen, buttons[key], 0, S.PATHS[key])
                                    Ff.display_text(screen, key, 30, (buttons["Delete"].left + buttons["Delete"].left / 7, buttons["Delete"].top * 1.025),"Red")
                                    cancel = True
                                    I.shutil.rmtree('static/data/created_characters/' + I.info.SELECTED_CHARACTER)
                                    I.info.SELECTED_CHARACTER = ""
                                elif key == I.info.SELECTED_CHARACTER:
                                    select = False
                                    S.PLAY = True
                                key_check = ""
                        elif key == key_check:
                            if key in ["Back"]:
                                Ff.button_click_render_down(screen, buttons[key], 0, S.PATHS[key])
                            elif key == "Delete":
                                Ff.button_click_render_down(screen, buttons[key], 0, S.PATHS[key])
                                Ff.display_text(screen, key, 30, (buttons["Delete"].left + buttons["Delete"].left / 7, buttons["Delete"].top * 1.025),"Red")
                            key_check = ""
                        I.pg.display.flip()


    S.BUSY = False
    S.START_APP = True
