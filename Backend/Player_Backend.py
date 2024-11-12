from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S
from Backend import Play

def exp_till_lvup(player):
    level = int(player["Level"])

    if level > 5:
        exp_needed = level * 100 * 0.9
    elif level > 10:
        exp_needed = level * 100 * 0.8
    elif level > 15:
        exp_needed = level * 100 * 0.7
    elif level > 20:
        exp_needed = level * 100 * 0.6
    else:
        exp_needed = level * 100
    return  exp_needed

def update_character(txt_data, spells, npc, items):
    player_disc = {}
    spell_str = txt_data["Spells"]
    spell_list = spell_str.split(",,")
    for slot_spell in spell_list:
        if slot_spell != '' and slot_spell != "Empty":
            slot, spell = slot_spell.split("__")
            spells.selected_spell[int(slot)] = spell

    I.info.BACKPACK_CONTENT = {}
    backpack_str = txt_data["Backpack"]
    backpack_str_list = backpack_str.split(",,")
    for backpack_data in backpack_str_list:
        if backpack_data != {} and backpack_data != "Empty" and backpack_data != '':
            item, amount, posx, posy = backpack_data.split("__")
            Ff.add_to_backpack(item, amount, items, int(posx), int(posy))  # adds items from txt
    hp_by_race = {"Elf": 11,
                  "Human": 10}

    mana_by_race = {"Elf": 14,
                    "Human": 10}

    race = txt_data["Race"]
    level = txt_data["Level"]
    player_disc["hp"] = (int(txt_data["Health"]), int(hp_by_race[race] * level))
    player_disc["mana"] = (int(txt_data["Mana"]), int(mana_by_race[race] * level))

    if txt_data["DEATH_SAVE"] != 0 and txt_data["DEATH_SAVE"] != "":
        I.info.DEATH_SAVE = [txt_data["DEATH_SAVE"].split(":")[0], int(txt_data["DEATH_SAVE"].split(":")[1]), int(txt_data["DEATH_SAVE"].split(":")[2]), int(txt_data["DEATH_SAVE"].split(":")[3]), int(txt_data["DEATH_SAVE"].split(":")[4]), int(txt_data["DEATH_SAVE"].split(":")[5])]

    if I.info.DEATH_SAVE != 0 and I.info.DEATH_SAVE[5] == 0:
        I.info.ENTRY_POS = int(txt_data["Save_point"].split(":")[1]), int(txt_data["Save_point"].split(":")[2])
        I.info.OFFSCREEN = int(txt_data["Save_point"].split(":")[3]), int(txt_data["Save_point"].split(":")[4])
        player_disc["hp"] = 0, player_disc["hp"][1]
        player_disc["dead"] = True
    elif I.info.DEATH_SAVE != 0 and I.info.DEATH_SAVE[5] == 1:
        I.info.ENTRY_POS = int(txt_data["Spawn"].split(":")[1]), int(txt_data["Spawn"].split(":")[2])
        I.info.OFFSCREEN = int(txt_data["Spawn"].split(":")[3]), int(txt_data["Spawn"].split(":")[4])
        player_disc["hp"] = 0, player_disc["hp"][1]
        player_disc["dead"] = True
    else:
        I.info.ENTRY_POS = int(txt_data["Spawn"].split(":")[1]), int(txt_data["Spawn"].split(":")[2])
        I.info.OFFSCREEN = int(txt_data["Spawn"].split(":")[3]), int(txt_data["Spawn"].split(":")[4])
        player_disc["dead"] = False
    if txt_data["Titles"] == "," or txt_data["Titles"] == "":
        I.info.TITLES = []
    else:
        I.info.TITLES = txt_data["Titles"].split(",")
    player_disc["Gold"] = txt_data["Gold"]
    player_disc["Experience"] = txt_data["Experience"]
    player_disc["Level"] = txt_data["Level"]
    player_disc["Exhaustion"] = (int(txt_data["Exhaustion"]), 100)

    player_disc["Last_hit"] = I.pg.time.get_ticks()  # required to know when to start regenerating hp and mana
    player_disc["Save_point"] = txt_data["Save_point"]

    if txt_data["Quests"] != [""]:
        I.info.QUESTS = Ff.string_to_list(txt_data["Quests"])
    else:
        I.info.QUESTS = []
    # I.DialB.check_quest_completion()
    if txt_data["Completed_quests"] != [""]:
        I.info.COMPLETED_QUESTS = Ff.string_to_list(txt_data["Completed_quests"])
    else:
        I.info.COMPLETED_QUESTS = []

    dialog_id = txt_data["Dialog"].split(",,")
    for value in dialog_id:
        if value != "":
            key, id, friendlyness = value.split("__")
            npc[key]["dialog"].iteration = int(id)
            npc[key]["dialog"].friendlyness = int(friendlyness)

    I.info.CRIMINAL = {
        "Charge": "",
        "Fine": 0,
        "Prison_time": 0
    }
    if txt_data["Criminal"] != "":
        I.info.CRIMINAL = Ff.string_to_dict(txt_data["Criminal"])

    I.info.CONTAINERS = {}
    if txt_data["Containers"] != "":
        I.info.CONTAINERS = Ff.string_to_dict(txt_data["Containers"])


    return player_disc

def level_up(player, gifs):
    exp = exp_till_lvup(player)
    if player["Experience"] >= exp:
        player["Experience"] = 0
        player["Level"] = 1 + int(player["Level"])
        player["hp"] = player["hp"][1], player["hp"][1]
        player["mana"] = player["mana"][1], player["mana"][1]
        gifs["Level up"].Start_gif("Level up", [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2, S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7])

def update_equipment_var(key, value):
    if key[0] < 0:
        I.info.EQUIPED[I.info.equipment[key]] = value, I.info.EQUIPED[I.info.equipment[key]][1]

def update_character_stats(file_path, player_data, selected_spells, npc):
    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Update the Level and Experience lines
    for i, line in enumerate(lines):
        if line.startswith('Level:'):
            lines[i] = f'Level: {player_data["Level"]}\n'
        elif line.startswith('Experience:'):
            lines[i] = f'Experience: {player_data["Experience"]}\n'
        elif line.startswith('Health:'):
            lines[i] = f'Health: {player_data["hp"][0]}\n'
        elif line.startswith('Mana:'):
            lines[i] = f'Mana: {player_data["mana"][0]}\n'
        elif line.startswith('Exhaustion:'):
            lines[i] = f'Exhaustion: {player_data["Exhaustion"][0]}\n'
        elif line.startswith('Gold'):
            lines[i] = f'Gold: {player_data["Gold"]}\n'
        elif line.startswith('Last Save:'):
            time = I.datetime.now()
            time = time.strftime("%Y/%m/%d %H:%M")
            lines[i] = f'Last Save: {time}\n'
        elif line.startswith('Backpack:') and I.info.BACKPACK_CONTENT != {}:
            backpack_str = ""
            for item, (amount, posx, posy) in I.info.BACKPACK_CONTENT.items():
                backpack_str += item + "__" + str(amount) + "__" + str(posx) + "__" + str(posy) + ",,"
            lines[i] = f'Backpack: {backpack_str}\n'

        elif line.startswith('Spells:') and selected_spells != {}:
            spell_str = ""
            for slot, spell in selected_spells.items():
                spell_str += str(slot) + "__" + str(spell) + ",,"
            lines[i] = f'Spells: {spell_str}\n'
        elif line.startswith('Spells:') and selected_spells != {}:
            spell_str = ""
            for slot, spell in selected_spells.items():
                spell_str += str(slot) + "__" + str(spell) + ",,"
            lines[i] = f'Spells: {spell_str}\n'

        elif line.startswith('Dialog:') and npc != 0:
            dialog_str = ""
            for npc_name in npc.keys():
                dialog_str += npc_name + "__" + str(npc[npc_name]["dialog"].iteration) + "__" + str(npc[npc_name]["dialog"].friendlyness) + ",,"
            lines[i] = f'Dialog: {dialog_str}\n'

        elif line.startswith('Quests:'):
            if I.info.QUESTS != []:
                quest_str = Ff.list_to_string(I.info.QUESTS)
            else:
                quest_str = '[]'
            lines[i] = f'Quests: {quest_str}\n'

        elif line.startswith('Completed_quests:'):
            if I.info.COMPLETED_QUESTS != []:
                quest_str = Ff.list_to_string(I.info.COMPLETED_QUESTS)
            else:
                quest_str = '[]'
            lines[i] = f'Completed_quests: {quest_str}\n'

        elif line.startswith('Spawn:'):
            spawn_str = I.info.CURRENT_ROOM["name"] + ":" + str(I.info.ENTRY_POS[0]) + ":" + str(I.info.ENTRY_POS[1]) + ":" + str(I.info.OFFSCREEN[0]) + ":" + str(I.info.OFFSCREEN[1])
            lines[i] = f'Spawn: {spawn_str}\n'
        elif line.startswith('Titles:'):
            titles = I.info.TITLES
            titles_str = ",".join(I.info.TITLES)
            lines[i] = f'Titles: {titles_str}\n'
        elif line.startswith("DEATH_SAVE:"):
            if I.info.DEATH_SAVE == 0:
                death_save_str = "0"
            else:
                death_save_str = str(I.info.DEATH_SAVE[0]) + ":" + str(I.info.DEATH_SAVE[1]) + ":" + str(I.info.DEATH_SAVE[2]) + ":" + str(I.info.DEATH_SAVE[3]) + ":" + str(I.info.DEATH_SAVE[4]) + ":" + str(I.info.DEATH_SAVE[5])
            lines[i] = f'DEATH_SAVE: {death_save_str}\n'
        elif line.startswith('Containers:'):
            container_str = Ff.dict_to_string(I.info.CONTAINERS)
            lines[i] = f'Containers: {container_str}\n'
        elif line.startswith('Criminal:'):
            criminal_str = Ff.dict_to_string(I.info.CRIMINAL)
            lines[i] = f'Criminal: {criminal_str}\n'


    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

def walking(dx, dy, collide, data, decorations, rooms, screen):
    if not collide[0] or collide[0] in ["Portal", "Plant bed", "gap"]:
        regular_walking(data, dx, dy)
    elif collide[0] not in ["mob_collide"]: # Collisions made specificly for mobs and decor. but currently just decor
        # I.T.Make_rect_visible(sub_screen, me, "blue")
        if rooms.type == "Village":
            me_left = I.pg.Rect(148 + I.info.OFFSCREEN[0] / 4, 82 + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 400, S.SCREEN_HEIGHT / 150) # black
            me_right = I.pg.Rect(159 + I.info.OFFSCREEN[0] / 4, 82 + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 400, S.SCREEN_HEIGHT / 150) # purple
            me_up = I.pg.Rect(152 + I.info.OFFSCREEN[0] / 4, 80 + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 200, S.SCREEN_HEIGHT / 300) # white
            me_down = I.pg.Rect(152 + I.info.OFFSCREEN[0] / 4, 90 + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 200, S.SCREEN_HEIGHT / 300) # orange
        else:
            # me = I.pg.Rect(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 24 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 16 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 24,S.SCREEN_HEIGHT / 12)
            x = S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 24 + I.info.OFFSCREEN[0]
            y = S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 16 + I.info.OFFSCREEN[1]
            me_left = I.pg.Rect(x + 5, y + 26, S.SCREEN_WIDTH / 150, S.SCREEN_HEIGHT / 30)  # black
            me_right = I.pg.Rect(x + 45, y + 26, S.SCREEN_WIDTH / 150, S.SCREEN_HEIGHT / 30)  # purple
            me_up = I.pg.Rect(x + 18, y - 10, S.SCREEN_WIDTH / 50, S.SCREEN_HEIGHT / 100)  # white
            me_down = I.pg.Rect(x + 18, y + 50, S.SCREEN_WIDTH / 50, S.SCREEN_HEIGHT / 100)  # orange

        I.T.Make_rect_visible(screen, me_left, "black")
        I.T.Make_rect_visible(screen, me_right, "purple")
        I.T.Make_rect_visible(screen, me_up, "white")
        I.T.Make_rect_visible(screen, me_down, "orange")
        if isinstance(collide[1], list):
            handle_colliding_with_polygon(me_up, me_down, me_left, me_right, collide, dx, dy, data)

        handle_rect_colliding(me_up, me_down, me_left, me_right, collide, dx, dy, data, decorations)

    elif collide[0] == "mob_collide":
        # if collide is mob
        I.MB.hit_by_mob_walking(data, collide)

def regular_walking(data, dx, dy):
    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
        if I.info.OFFSCREEN[0] in [0, 3, -3]:
            # if no collisions walk properly. move screen in x axis
            data["Zoom_rect"].x += dx * I.info.FAST
            data["Zoom_rect"].y += 0
        else:
            data["Zoom_rect"].x += 0
            data["Zoom_rect"].y += 0
        if I.info.OFFSCREEN[1] in [0, 3, -3]:
            # if no collisions walk properly. move screen in y axis
            data["Zoom_rect"].x += 0
            data["Zoom_rect"].y += dy * I.info.FAST
        else:
            data["Zoom_rect"].x += 0
            data["Zoom_rect"].y += 0
    else:
        data["Zoom_rect"].x += 0
        data["Zoom_rect"].y += 0

def update_char_bar(screen, data, gifs, items, rooms, clock, spells, npc):
    rect = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Char_bar"], [0, 0, S.SCREEN_WIDTH / 8, S.SCREEN_HEIGHT / 8])

    # start gifs if player dead
    if data["Player"]["hp"][0] <= 0 and not data["Player"]["dead"]:
        data["Player"]["dead"] = data["Zoom_rect"].copy()
        data["Player"]["dead"].x += I.info.OFFSCREEN[0] / 4
        data["Player"]["dead"].y += I.info.OFFSCREEN[1] / 4
        gifs["Ghost"].Start_gif("Ghost",[S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2, S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7])
        gifs["Portal"].Start_gif("Portal", [I.info.SPAWN_POINT[0] + 30, I.info.SPAWN_POINT[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7])
        spawn_point = data["Player"]["Save_point"].split(":")
        I.info.DEATH_SAVE = [I.info.CURRENT_ROOM["name"], data["Player"]["dead"][0], data["Player"]["dead"][1], I.info.OFFSCREEN[0], I.info.OFFSCREEN[1], 0]
        data["Zoom_rect"].x = int(spawn_point[1])
        data["Zoom_rect"].y = int(spawn_point[2])
        rooms.select_room(spawn_point[0])
        update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"], spells.selected_spell, npc)
        I.info.CURRENT_ROOM = {"name": spawn_point[0], "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": "Village"}
        # Play.Start(screen, clock, rooms)
        I.info.RESET = True

    elif data["Player"]["hp"][0] <= 0 and data["Player"]["dead"]:
        data["Player"]["dead"] = data["Zoom_rect"].copy()
        data["Player"]["dead"].x += I.info.OFFSCREEN[0] / 4
        data["Player"]["dead"].y += I.info.OFFSCREEN[1] / 4
        gifs["Ghost"].Start_gif("Ghost", [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2, S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7])
        gifs["Portal"].Start_gif("Portal", [I.info.SPAWN_POINT[0] + 30, I.info.SPAWN_POINT[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7])
        I.info.OFFSCREEN = (0, 0)
        data["Player"]["hp"] = 1, data["Player"]["hp"][1]

    # display Hp
    I.pg.draw.rect(screen, "black", (rect.w * 0.1, rect.h * 0.56, rect.w * 0.8, rect.h * 0.08))
    remainder = data["Player"]["hp"][0] / data["Player"]["hp"][1]
    I.pg.draw.rect(screen, "red", (rect.w * 0.1, rect.h * 0.56, rect.w * 0.8 * remainder, rect.h * 0.08))

    # display Mp
    I.pg.draw.rect(screen, "black", (rect.w * 0.1, rect.h * 0.82, rect.w * 0.8, rect.h * 0.08))
    remainder = data["Player"]["mana"][0] / data["Player"]["mana"][1]
    I.pg.draw.rect(screen, "blue", (rect.w * 0.1, rect.h * 0.82, rect.w * 0.8 * remainder, rect.h * 0.08))

    options = ["Sword", "Axe", "Picaxe"]
    position = {
        "Sword": (15, 11),
        "Axe": (66, 11),
        "Picaxe": (118, 11),
                }
    speeds = [I.info.COMBAT_RECT[1], I.info.AXE[1], I.info.PICAXE[1]]
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    for i in range(len(options)):
        if I.info.EQUIPED[options[i]][0] != 0:
            content = I.info.EQUIPED[options[i]][0]
            Ff.add_image_to_screen(screen, items.item_dict[content.split("|")[0]]["path"], [position[options[i]][0], position[options[i]][1], item_w, item_h])
            if speeds[i] != 0:
                if I.info.EQUIPED[options[i]][1] == 27:
                    I.info.EQUIPED[options[i]] = I.info.EQUIPED[options[i]][0], 26
                cover = I.pg.Surface((item_w, I.info.EQUIPED[options[i]][1]), I.pg.SRCALPHA)
                cover.fill((0, 0, 0, 128))
                screen.blit(cover, (position[options[i]][0], position[options[i]][1]))

def interract(collide, data, gifs, items, screen, songs, spells, clock, rooms, npc, decorations):
    if collide[0] != False:
        if collide[0] in I.info.HARVESTABLE.keys() and not data["Player"]["dead"]:
            if any(collide[1] == t[0] for t in I.info.HARVESTED_OBJECTS.get(collide[0])):
                Ff.display_text_player("Nothing found", 500)
                pass
            else:
                item = I.info.HARVESTABLE[collide[0]]
                values = items.item_dict[item]["Aquire"].split(",,")
                amount = I.random.randint(int(values[1]), int(values[2]))
                I.QB.tutorial_berry_get(item)
                I.IB.add_dropped_items_to_var(item, amount, rooms, collide[1], data, "decor")
                duration = int(values[3])
                #  Handle registering items that were taken, used in not allowing collection of too many items from single bush
                harvested_obj_rect = decorations.decor_dict[collide[0]][collide[2]]["rect"]
                if I.info.HARVESTED_OBJECTS.get(collide[0]) == []:
                    # Ff.update_map_view(collide[2], collide[0] + "_Harvested", (harvested_obj_rect.x, harvested_obj_rect.y), "add")
                    Ff.update_map_view(collide[2], collide[0], (harvested_obj_rect.x, harvested_obj_rect.y), "remove")
                    Ff.update_map_view(collide[2], collide[0] + "_Harvested", (harvested_obj_rect.x, harvested_obj_rect.y), "add")
                    I.info.HARVESTED_OBJECTS[collide[0]] = [(collide[2], duration, I.info.CURRENT_ROOM["name"])]

                else:
                    Ff.update_map_view(collide[2], collide[0], (harvested_obj_rect.x, harvested_obj_rect.y), "remove")
                    Ff.update_map_view(collide[2], collide[0] + "_Harvested", (harvested_obj_rect.x, harvested_obj_rect.y), "add")
                    existing_values = I.info.HARVESTED_OBJECTS.get(collide[0], [])
                    existing_values.append((collide[2], duration, I.info.CURRENT_ROOM["name"]))
                    I.info.HARVESTED_OBJECTS[collide[0]] = existing_values
                # Ff.display_text_player("Recieved " + str(amount) + " " + str(item), 5000)
                return
        elif "door" in collide[0]:
            door_effect = decorations.decor_dict[collide[0]][collide[2]]["effect"]
            if "LOCKED" in door_effect and "UNLOCKED" not in door_effect:
                action_string = decorations.decor_dict[collide[0]]["action"]
                locked_str_id = action_string.find("LOCKED")
                locked_string = action_string[locked_str_id:].split(",,")[0]
                day_night_str_id = locked_string.find("DAY_NIGHT:")
                difficulty_id = locked_string.find("DIFF:")
                day_night = int(locked_string[day_night_str_id:].split(",")[0].split(":")[1])
                difficulty = int(locked_string[difficulty_id:].split(",")[0].split(":")[1])
                if day_night < I.info.DIM:
                    decorations.decor_dict[collide[0]][collide[2]]["effect"] = "LOCKED"
                    I.TB.handle_unlocking_door(difficulty, collide, screen, clock, decorations)
                else:
                    decorations.decor_dict[collide[0]][collide[2]]["effect"] = "UNLOCKED"
                    if "ENTERABLE" not in decorations.decor_dict[collide[0]]["action"]:
                        """means door is internal, like in House1B1"""
                        Ff.update_map_view(collide[2], collide[0], (collide[1].x, collide[1].y), "remove")
                        Ff.update_map_view(collide[2], collide[0] + "_open", (collide[1].x, collide[1].y), "add")
                    else:
                        gifs[collide[0]].Start_gif("Door", 0)
                        I.info.DOOR_CLICK = 0, collide[0]
            else:
                decorations.decor_dict[collide[0]][collide[2]]["effect"] = "UNLOCKED"
                if "ENTERABLE" not in decorations.decor_dict[collide[0]]["action"]:
                    """means door is internal, like in House1B1"""
                    Ff.update_map_view(collide[2], collide[0], (collide[1].x, collide[1].y), "remove")
                    Ff.update_map_view(collide[2], collide[0] + "_open", (collide[1].x, collide[1].y), "add")
                else:
                    gifs[collide[0]].Start_gif("Door", 0)
                    I.info.DOOR_CLICK = 0, collide[0]
        elif collide[0] == "Portal":
            Ff.display_text_player("Reviving, dont move", 3000)
        elif collide[0] == "Grave":
            Ff.display_text_player("Was Purgatory Fun? :)", 10000)
            data["Player"]["dead"] = False
            data["Player"]["hp"] = (data["Player"]["hp"][1], data["Player"]["hp"][1])
            gifs["Ghost"].start_gif = False
            I.info.DEATH_SAVE = 0
        elif collide[0] == "Sign":
            I.DialB.init_dialog("Sign", data["Player"], screen, npc, items, decorations, data, gifs, rooms, clock, spells)
        elif collide[0] in npc.keys():
            I.DialB.init_dialog(collide[0], data["Player"], screen, npc, items, decorations, data, gifs, rooms, clock, spells)
        elif decorations.decor_dict.get(collide[0]) != None:
            I.CB.handle_container_click(decorations, collide, screen, items, data, rooms)
            if "Appliance" in decorations.decor_dict[collide[0]]["type"]:
                I.AB.handle_appliances(items, screen, gifs, data, decorations, rooms, collide)
            elif "PLANT" in decorations.decor_dict[collide[0]]["action"]:
                if I.info.EQUIPED["Sword"][0] != 0 and "PLANTABLE" in items.item_dict[I.info.EQUIPED["Sword"][0].split("|")[0]]["Properties"]:
                    plant = items.item_dict[I.info.EQUIPED["Sword"][0].split("|")[0]]["Properties"].replace("PLANTABLE(", "").replace(")", "").split(",,,")[0].split(",,")
                    time = plant[1].replace("TIME:", "")
                    plant = plant[0].replace("PLANT:", "")
                    decorations.decor_dict[collide[0]][collide[1]]["effect"] = "PLANTED:" + plant + ":" + time + ":" + time
                    I.th.start_thread(time, "planting", decorations)
                    Ff.remove_from_backpack(I.info.EQUIPED["Sword"][0], 1)
                    I.BB.update_equiped()
            elif "NPC_Mob" in decorations.decor_dict[collide[0]]["type"]:
                I.DialB.init_dialog(collide[0], data["Player"], screen, npc, items, decorations, data, gifs, rooms, clock, spells)
            else:
                print("some other decor", collide)
                print("some other decor", decorations.decor_dict[collide[0]])
        else:
            print("no interraction available", collide)

def Get_walking_on(rooms, data):
    if rooms.size == ["1", "1", "1", "1"]:
        clean_surface = data["Image"].subsurface(data["Zoom_rect"]).copy()
        scaled_image = I.pg.transform.scale(clean_surface, data["Window size"])
        foot_possision = (int(600 + I.info.OFFSCREEN[0]), int(370 + I.info.OFFSCREEN[1]))
        if foot_possision[1] > 718:
            foot_possision = foot_possision[0], 718
        # I.T.Make_rect_visible(screen, (foot_possision[0], foot_possision[1], 10, 10), "red")
        color = tuple(scaled_image.get_at(foot_possision))
        if I.A.WALKING_COLORS.get(color) != None and I.info.WALKING_ON != "Mob":
            I.info.WALKING_ON = I.A.WALKING_COLORS[color]
            # print(I.info.WALKING_ON, color)
        else:
            print(color, " doesnt exist")


def handle_colliding_with_polygon(me_up, me_down, me_left, me_right, collide, dx, dy, data):
    if Ff.rect_polygon_collision(me_left, collide[1]) != False:
        print("colliding left")
        if dx != 1:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0] - dx * 3 * I.info.FAST, I.info.OFFSCREEN[1])
    elif dx != 1:
        regular_walking(data, dx, 0)

    if Ff.rect_polygon_collision(me_right, collide[1]) != False:
        print("colliding right")
        if dx != -1:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0] - dx * 3 * I.info.FAST, I.info.OFFSCREEN[1])
    elif dx != -1:
        regular_walking(data, dx, 0)

    if Ff.rect_polygon_collision(me_up, collide[1]) != False:
        print("colliding up")
        if dy != 1:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0], I.info.OFFSCREEN[1] - dy * 3 * I.info.FAST)
    elif dy != 1:
        regular_walking(data, 0, dy)

    if Ff.rect_polygon_collision(me_down, collide[1]) != False:
        print("colliding down")
        if dy != -1:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0], I.info.OFFSCREEN[1] - dy * 3 * I.info.FAST)
    elif dy != -1:
        regular_walking(data, 0, dy)


def handle_rect_colliding(me_up, me_down, me_left, me_right, collide, dx, dy, data, decorations):
    if me_left.collidelist(decorations.displayed_rects) != -1:
        if dx != 1:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0] - dx * 3 * I.info.FAST, I.info.OFFSCREEN[1])
    elif dx != 1:
        regular_walking(data, dx, 0)

    if me_right.collidelist(decorations.displayed_rects) != -1:
        if dx != -1:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0] - dx * 3 * I.info.FAST, I.info.OFFSCREEN[1])
    elif dx != -1:
        regular_walking(data, dx, 0)

    if me_up.collidelist(decorations.displayed_rects) != -1:
        if dy != 1:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0], I.info.OFFSCREEN[1] - dy * 3 * I.info.FAST)
    elif dy != 1:
        regular_walking(data, 0, dy)

    if me_down.collidelist(decorations.displayed_rects) != -1:
        if dy != -1:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0], I.info.OFFSCREEN[1] - dy * 3 * I.info.FAST)
    elif dy != -1:
        regular_walking(data, 0, dy)