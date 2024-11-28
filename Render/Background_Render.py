from utils import Frequent_functions as Ff, Imports as I
from Values import Settings as S
from Backend import Play

B_Left = 0
B_Top = 0
B_W = S.SCREEN_WIDTH
B_H = S.SCREEN_HEIGHT

def read_txt_file(path):
    data_dict = {}
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Convert tuples to actual tuples
                if value.startswith("(") and value.endswith(")"):
                    value = tuple(map(int, value[1:-1].split(',')))

                # Convert numeric values
                elif value.isdigit():
                    value = int(value)

                # Convert floating point values
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        pass

                data_dict[key] = value

    return data_dict

def Start(mob, decorations, spells, rooms, npc, items, gifs):
    data = {}
    txt_data = read_txt_file('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt")
    data["Player"] = I.PB.update_character(txt_data, spells, npc, items)
    if I.info.CURRENT_ROOM["Mobs"]:
        monster_count = {}
        for key, current_mob in mob.items():
            monster_count[current_mob.name] = current_mob.count

    data["Window size"] = (B_W, B_H)  # Defines the size of the window (The rest is black)
    data["Zoom"] = (B_W / 4, B_H / 4)  # Defines how zoomed in to the picture the view is
    if rooms.size == ["1", "1", "1", "1"]:
        values = rooms.name.split("_")
        data["Zoom"] = (B_W / 4, B_H / 4)  # Defines how zoomed in to the picture the view is
        data["Image"] = I.pg.image.load(S.local_path + "/static/images/Background/" + rooms.background + "_" + values[1] + "_" + values[2] + ".png").convert_alpha()  # uploads the background image with transparent convert
    else:
        data["Zoom"] = (B_W / 15, B_H / 15)  # Defines how zoomed in to the picture the view is
        data["Image"] = I.pg.image.load(S.DECOR_PATH[rooms.background]).convert_alpha()  # uploads the background image with transparent convert

    data["Image_rect"] = data["Image"].get_rect()  # Gets the rect of image
    data["Zoom_rect"] = I.pg.Rect(I.info.ENTRY_POS[0], I.info.ENTRY_POS[1], *data["Zoom"])  # creates a rect based on zoomed in picture (basicly makes a window)
    # I.S.LayeredGroup = I.S.LayeredGroup()
    decorate_from_db(rooms, decorations)
    if I.info.CURRENT_ROOM["Mobs"]:
        for key in monster_count:
            data[key] = I.MB.generate_mobs(mob[key], data["Image_rect"].size, gifs)
    data["Queue_to_be_removed"] = I.queue.Queue()

    # image_data["Church_1"] = place_decor_by_coordinates(200, 280, S.DECOR_PATH["Church_1"], (2, 2), (2, 2))
    return data

# def Update(data, decorations, gifs: dict, rooms, clock, screen, spells, npc, mob, songs, items):
#     data["Zoom_rect"].x = max(0, min(data["Zoom_rect"].x, data["Image_rect"].width - data["Zoom"][0]))
#     data["Zoom_rect"].y = max(0, min(data["Zoom_rect"].y, data["Image_rect"].height - data["Zoom"][1]))
#     I.info.Player_rect = I.pg.Rect(148 + I.info.OFFSCREEN[0] / 4, 80 + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 60)  # Player rect (if it gets hit with other rect. colide is set to True
#     removable_list = []
#     collide = [False]
#     sub_image = data["Image"].subsurface(data["Zoom_rect"]).copy()
#     new_subimage = I.pg.Surface([data["Zoom_rect"][2], data["Zoom_rect"][3]], I.pg.SRCALPHA, 32).convert_alpha()
#     sub_image = (sub_image, new_subimage)
#     mob_screen = (I.pg.Surface([data["Zoom_rect"][2], data["Zoom_rect"][3]], I.pg.SRCALPHA, 32).convert_alpha(),
#                   I.pg.Surface([data["Zoom_rect"][2], data["Zoom_rect"][3]], I.pg.SRCALPHA, 32).convert_alpha())
#
#     decor_screen = (I.pg.Surface([data["Zoom_rect"][2], data["Zoom_rect"][3]], I.pg.SRCALPHA, 32).convert_alpha(),
#                     I.pg.Surface([data["Zoom_rect"][2], data["Zoom_rect"][3]], I.pg.SRCALPHA, 32).convert_alpha())
#
#
#
#
#     I.S.LayeredGroup.update()
#     I.S.LayeredGroup.draw_sub_image(sub_image[0], data)
#
#
#     handle_screen_blits(sub_image, mob_screen, decor_screen, screen, data, "lower")
#
#     dx, dy = Play.keypress_handle(screen, data, songs, items, spells, gifs, rooms, clock, decorations)
#
#
#     I.PB.walking(dx, dy, collide, data, decorations, rooms, screen)
#
#     I.S.Player_sprite.update_player(dx, dy)
#     I.S.LayeredGroup.draw_player(screen)
#
#     return collide

def New_Update(data, decorations, gifs: dict, rooms, clock, screen, spells, npc, mob, songs, items):
    data["Zoom_rect"].x = max(0, min(data["Zoom_rect"].x, data["Image_rect"].width - data["Zoom"][0]))
    data["Zoom_rect"].y = max(0, min(data["Zoom_rect"].y, data["Image_rect"].height - data["Zoom"][1]))
    I.info.Player_rect = I.pg.Rect(148 + I.info.OFFSCREEN[0] / 4, 80 + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 60)  # Player rect (if it gets hit with other rect. colide is set to True
    removable_list = []
    collide = [False]
    sub_image = data["Image"].subsurface(data["Zoom_rect"]).copy()
    new_subimage = I.pg.Surface([data["Zoom_rect"][2], data["Zoom_rect"][3]], I.pg.SRCALPHA, 32).convert_alpha()
    sub_image = (sub_image, new_subimage)
    mob_screen = (I.pg.Surface([data["Zoom_rect"][2], data["Zoom_rect"][3]], I.pg.SRCALPHA, 32).convert_alpha(), I.pg.Surface([data["Zoom_rect"][2], data["Zoom_rect"][3]], I.pg.SRCALPHA, 32).convert_alpha())
    decor_screen = (I.pg.Surface([data["Zoom_rect"][2], data["Zoom_rect"][3]], I.pg.SRCALPHA, 32).convert_alpha(), I.pg.Surface([data["Zoom_rect"][2], data["Zoom_rect"][3]], I.pg.SRCALPHA, 32).convert_alpha())

    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
        collide = handle_outside_render(data, decorations, removable_list, items, spells, npc, screen, clock, gifs, rooms, collide, sub_image, mob, songs, decor_screen) # takes 6 ms
        collide = render_bacground_decor(sub_image[0], decorations, data, collide, "outside", rooms, npc, spells)
    else:
        door = render_house(screen, data, rooms)
        collide = render_bacground_decor(screen, decorations, data, collide, "inside", rooms, npc, spells)
        screen2 = I.pg.Surface([S.SCREEN_WIDTH, S.SCREEN_HEIGHT], I.pg.SRCALPHA, 32).convert_alpha()
        screen1 = screen.copy()
        sub_image = (screen1, screen2)
        collide = handle_interior_visualisation(decorations, sub_image, data, gifs, rooms, clock, npc, spells, collide, screen, items)
        handle_dark_rooms_render(sub_image, rooms, decorations)
        house_border_rect = interior_border_rect(decorations)
        # I.T.Make_rect_visible(screen, house_border_rect[0], "green")
        # I.T.Make_rect_visible(screen, house_border_rect[1], "green")
        # I.T.Make_rect_visible(screen, house_border_rect[2], "green")
        # I.T.Make_rect_visible(screen, house_border_rect[3], "green")

        me = I.pg.Rect(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 25 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 10 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 22, S.SCREEN_HEIGHT / 8)
        handle_stepping_on_rect(me, door, data, screen, clock, spells, "Return", rooms, npc)
        if I.info.RESET:
            return collide
        collide = handle_stepping_on_rect(me, house_border_rect, data, 0, 0, collide, "Collide_list", rooms, decorations)

    if mob != {}:
        collide = handle_mob_render(collide, mob_screen, data, mob, gifs, songs, decorations, items, rooms, spells, npc)

    I.GB.drop_charges_for_dying(data)

    I.TB.handle_hammer_hits(items, decorations, rooms, data)

    collide = handle_death_visualisation(sub_image[0], data, gifs, collide, decorations)

    I.SB.cast_spell_handle(sub_image[0], data, spells, gifs, mob, songs, decorations, items, rooms, screen)

    render_folower(sub_image[0], gifs, data, decorations, mob, items, rooms)

    handle_tutorial(sub_image, data, screen, npc, items, decorations, gifs, rooms, clock, spells, mob)

    I.TB.handle_shovel_digging(decorations, items, rooms, data, collide, sub_image[0])

    render_light(sub_image[0], decorations, rooms, data) # takes aprox 0.1 ms or something

    handle_screen_blits(sub_image, mob_screen, decor_screen, screen, data, "lower")
    # if S.DUMMY_VALUE1 != []:
    #     for x, y in S.DUMMY_VALUE1:
    #         print(x, y, data["Zoom_rect"])
    #         I.pg.draw.rect(sub_image[1], "red", I.pg.Rect(x - data["Zoom_rect"].w / 2, y - data["Zoom_rect"].h / 2, 100, 100))
            # I.T.Make_rect_visible(sub_image[1], (x, y, 100, 100), "red")
    dx, dy = Play.keypress_handle(screen, data, songs, items, spells, gifs, rooms, clock, decorations)

    if S.GOD_MODE:
        collide = [False]

    I.QB.handle_quest_mark_render(sub_image[1], npc, decorations, gifs, rooms, data)

    I.QB.set_quest_mark_complete(rooms)

    """if not in village just makes sure you dont hit stuff"""

    I.PB.walking(dx, dy, collide, data, decorations, rooms, screen)

    render_strikes(screen, gifs, 0, items)

    render_char(dx, dy, screen, gifs, data, decorations, collide)

    render_levelup(gifs, screen)

    render_strikes(screen, gifs, 1, items)

    handle_render_dropped_items(sub_image[1], items, data, rooms)


    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
        handle_screen_blits(sub_image, mob_screen, decor_screen, screen, data,"upper")
    else:
        screen.blit(mob_screen[1], (0, 0))
        screen.blit(decor_screen[1], (0, 0))
        screen.blit(sub_image[1], (0, 0))

    I.MapB.add_map_to_maps(rooms, decorations)


    if data["Player"]["dead"] and collide[0] == "mob":  # dont hit mobs when u dead
        collide = [False]

    if removable_list != []:
        for option, id in removable_list:
            del decorations.decor_dict[option][id]

    handle_map_walk(data, rooms, screen, clock, spells, npc, mob, decorations, items)

    return collide

def handle_stepping_on_rect(me, rect, data, screen, clock, extra, action, rooms, npc_or_decorations):
    if "Return" in action:
        if rect != None: # for instances when the door rect doesn't exist (Prison)
            spells = extra
            if me.colliderect(rect):
                # I.info.ENTRY_POS = [510, 370]
                I.GB.restore_guard_decor(rooms)
                rooms.select_room("Village_10_10")
                I.info.CURRENT_ROOM = {"name": "Village_10_10", "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": rooms.type}
                I.PB.update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"], spells.selected_spell, npc_or_decorations)
                # Play.Start(screen, clock, rooms)
                I.info.RESET = True

    if "Collide_list" in action:
        if me.collidelistall(rect) and extra == [False]:
            colision_id = me.collidelistall(rect) # returns list of rect id's
            extra = ("border", rect[colision_id[0]].left, rect[colision_id[0]].top)
        return extra
    # if "Conversation" in action:
    #     for option in rect.keys():
    #         if "NPC" in rect[option]["action"]:
    #             for decor_key in rect[option].keys():
    #                 if decor_key in range(0,99):
    #                     npc_rect = rect[option][decor_key]["rect"]
    #                     big_npc_rect = I.pg.Rect(npc_rect.x - npc_rect.w / 2, npc_rect.y - npc_rect.h / 2, npc_rect.w * 2, npc_rect.h * 2)
    #                     if me.colliderect(big_npc_rect):
    #                         return extra
    #     return extra
        # if rect

# def handle_mob_render(collide, sub_image, data, mob_dict, gifs, song, decorations, items, rooms, spells, npc):
#     for mob in mob_dict.values():
#         for current_mob in mob.mobs:
#             if not current_mob["decor"]:
#                 mob_gif = current_mob["gif_frame"][0]
#                 if mob_gif >= len(current_mob["rect"]):
#                     continue
#                 mob_rect = current_mob["rect"][mob_gif]
#                 mob_x = mob_rect.x - data["Zoom_rect"].x
#                 mob_y = mob_rect.y - data["Zoom_rect"].y
#             else:
#                 """Guards, in the future other npcs"""
#                 if decorations.decor_dict[mob.name]["type"] == "NPC_Mob":
#                     I.GB.guard_allignment_change(mob, current_mob)
#                 mob_gif = 0
#                 mob_rect = current_mob["rect"][mob_gif]
#                 if decorations.decor_dict[mob.name].get(current_mob["id"]) != None:
#                     mob_x = decorations.decor_dict[mob.name][current_mob["id"]]["rect"].x - data["Zoom_rect"].x
#                     mob_y = decorations.decor_dict[mob.name][current_mob["id"]]["rect"].y - data["Zoom_rect"].y
#             rect = I.pg.Rect(mob_x, mob_y, mob_rect.w, mob_rect.h)
#             mob_collision = rect.collidelistall(decorations.displayed_rects_full)
#             if mob_collision != []:
#                 # if mob_y - mob_rect.h / 2 <= decor_rect.y:
#                 if rect.y <= decorations.displayed_rects_full[mob_collision[0]].y + decorations.displayed_rects_full[mob_collision[0]].h / 2:
#                     I.MB.update_mob_health(rect, current_mob, sub_image[0])
#                     image = current_mob["image"][mob_gif]
#                     sub_image[0].blit(image, (mob_x, mob_y))
#                     I.MB.handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items, rooms)
#                     I.MB.handle_damage_type_visualisation(sub_image[0], current_mob, gifs, (mob_x, mob_y), data, mob, decorations, items, rooms)
#                 else:
#                     I.MB.update_mob_health(rect, current_mob, sub_image[1])
#                     image = current_mob["image"][mob_gif]
#                     sub_image[1].blit(image, (mob_x, mob_y))
#                     I.MB.handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items, rooms)
#                     I.MB.handle_damage_type_visualisation(sub_image[1], current_mob, gifs, (mob_x, mob_y), data, mob, decorations, items, rooms)
#             else:
#                 I.MB.update_mob_health(rect, current_mob, sub_image[0])
#                 image = current_mob["image"][mob_gif]
#                 sub_image[0].blit(image, (mob_x, mob_y))
#                 I.MB.handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items, rooms)
#                 I.MB.handle_damage_type_visualisation(sub_image[0], current_mob, gifs, (mob_x, mob_y), data, mob, decorations, items, rooms)
#             if I.info.Player_rect.colliderect(rect) and not current_mob["decor"]:
#                 collide = ('mob', mob_rect)
#             if I.info.Player_rect.colliderect(rect) and current_mob["allignment"] in [6, 8, 9] and not data["Player"]["dead"]:
#                 if "Guard" in mob.name and I.info.CRIMINAL["Charge"] != "" and npc[mob.name]["dialog"].iteration == 0:
#                     collide = (mob.name, current_mob, mob_rect)
#                 elif I.GB.reset_guard_mob_to_decor(current_mob, mob):
#                     """if the mob attacking is not a guard"""
#                     collide = ('mob_collide', current_mob, mob_rect.x, mob_rect.y)
#                     data["Player"]["Last_hit"] = I.pg.time.get_ticks()
#                     data["Player"]["hp"] = data["Player"]["hp"][0] - int(current_mob["damage"][0]), data["Player"]["hp"][1]
#                     if data["Player"]["hp"][0] <= 0:
#                         data["Player"]["killer"] = mob.name
#             I.MB.handle_mob_speed(data, current_mob, decorations, mob, mob_dict, items, gifs, spells, rooms)
#     return collide

def handle_mob_render(collide, mob_image, data, mob_dict, gifs, song, decorations, items, rooms, spells, npc):
    for mob in mob_dict.values():
        for current_mob in mob.mobs:
            if not current_mob["decor"]:
                mob_gif = current_mob["gif_frame"][0]
                if mob_gif >= len(current_mob["rect"]):
                    continue
                mob_rect = current_mob["rect"][mob_gif]
                mob_x = mob_rect.x - data["Zoom_rect"].x
                mob_y = mob_rect.y - data["Zoom_rect"].y
            else:
                """Guards, in the future other npcs"""
                if decorations.decor_dict[mob.name]["type"] == "NPC_Mob":
                    I.GB.guard_allignment_change(mob, current_mob)
                mob_gif = 0
                mob_rect = current_mob["rect"][mob_gif]


                if decorations.decor_dict[mob.name].get(current_mob["id"]) != None:
                    mob_x = decorations.decor_dict[mob.name][current_mob["id"]]["rect"].x - data["Zoom_rect"].x
                    mob_y = decorations.decor_dict[mob.name][current_mob["id"]]["rect"].y - data["Zoom_rect"].y
                if any(r.x != mob_x or r.y != mob_y for r in current_mob["rect"]):
                    for i in range(0, len(current_mob["rect"])):
                        current_mob["rect"][i] = I.pg.Rect(decorations.decor_dict[mob.name][current_mob["id"]]["rect"].x, decorations.decor_dict[mob.name][current_mob["id"]]["rect"].y, mob_rect.w, mob_rect.h)

            rect = I.pg.Rect(mob_x, mob_y, mob_rect.w, mob_rect.h)
            if rect.y - rect.h / 2 <= 79 + I.info.OFFSCREEN[1] / 4:
                I.MB.update_mob_health(rect, current_mob, mob_image[0])
                image = current_mob["image"][mob_gif]
                if current_mob["flip"] == "left":
                    image = I.pg.transform.flip(image, 1,0)
                mob_image[0].blit(image, (mob_x, mob_y))
                I.MB.handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items, rooms)
                I.MB.handle_damage_type_visualisation(mob_image[0], current_mob, gifs, (mob_x, mob_y), data, mob, decorations, items, rooms)
            else:
                I.MB.update_mob_health(rect, current_mob, mob_image[1])
                image = current_mob["image"][mob_gif]
                if current_mob["flip"] == "left":
                    image = I.pg.transform.flip(image, 1,0)
                mob_image[1].blit(image, (mob_x, mob_y))
                I.MB.handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items, rooms)
                I.MB.handle_damage_type_visualisation(mob_image[1], current_mob, gifs, (mob_x, mob_y), data, mob, decorations, items, rooms)
            if I.info.Player_rect.colliderect(rect) and not current_mob["decor"]:
                collide = ('mob', mob_rect)
            if I.info.Player_rect.colliderect(rect) and current_mob["allignment"] in [6, 8, 9] and not data["Player"]["dead"]:
                if "Guard" in mob.name and I.info.CRIMINAL["Charge"] != "" and npc[mob.name]["dialog"].iteration == 0:
                    collide = (mob.name, current_mob, mob_rect)
                elif I.GB.reset_guard_mob_to_decor(current_mob, mob):
                    """if the mob attacking is not a guard"""
                    collide = ('mob_collide', current_mob, mob_rect.x, mob_rect.y)
                    data["Player"]["Last_hit"] = I.pg.time.get_ticks()
                    data["Player"]["hp"] = data["Player"]["hp"][0] - int(current_mob["damage"][0]), data["Player"]["hp"][1]
                    if data["Player"]["hp"][0] <= 0:
                        data["Player"]["killer"] = mob.name
            I.MB.handle_mob_speed(data, current_mob, decorations, mob, mob_dict, items, gifs, spells, rooms)
    return collide



def handle_death_visualisation(sub_image, data, gifs, collide, decorations):
    if data["Player"]["dead"]:
        me = I.pg.Rect(150, 85, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
        dead_disc = {"Portal": render_gif_on_subimage(sub_image, (S.SCREEN_WIDTH / 16, S.SCREEN_HEIGHT / 10), (I.info.SPAWN_POINT[0] * 1.8 - data["Zoom_rect"].x , I.info.SPAWN_POINT[1] + 10 * 16 - data["Zoom_rect"].y), gifs["Portal"]),
                     "Sign": render_on_subimage(sub_image, (S.SCREEN_WIDTH / 90, S.SCREEN_HEIGHT / 40), S.PLAYING_PATH["Sign"],(I.info.SPAWN_POINT[0] * 1.6 - data["Zoom_rect"].x, I.info.SPAWN_POINT[1] + 10 * 10 - data["Zoom_rect"].y))
                     }
        decorations.displayed_rects.append(dead_disc["Sign"])
        dead_list = list(dead_disc.values())
        if I.info.Player_rect.collidelistall(dead_list):
            keys = list(dead_disc.keys())
            key = keys[I.info.Player_rect.collidelistall(dead_list)[0]]
            collide = (key, dead_disc[key])
        if I.info.CURRENT_ROOM["name"] == I.info.DEATH_SAVE[0]:
            grave = render_on_subimage(sub_image, (S.SCREEN_WIDTH / 60, S.SCREEN_HEIGHT / 30), S.PLAYING_PATH["Grave"], (int(I.info.DEATH_SAVE[1]) - data["Zoom_rect"].x + me.x, int(I.info.DEATH_SAVE[2]) - data["Zoom_rect"].y + me.y))
            decorations.displayed_rects.append(grave)
            if I.info.Player_rect.colliderect(grave):
                collide = ("Grave", grave)
    return collide

def handle_interior_visualisation(decorations, sub_image, data, gifs, rooms, clock, npc, spells, collide, screen, items):
    me = I.pg.Rect(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 24 + I.info.OFFSCREEN[0],S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 14 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 24, S.SCREEN_HEIGHT / 12)
    # character_path = 'static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER
    # path = character_path + I.info.LAST_ORIENT[0]
    # player_image = I.pg.image.load(path)
    # player_mask = I.pg.mask.from_surface(player_image)
    # I.T.Make_rect_visible(sub_image[1], me, "blue")
    # collide = [False]
    decorations.displayed_rects = []
    decorations.displayed_rects_full = []


    update_decor_dict(decorations, gifs, rooms, items)
    decor_options = rooms.decor
    all_decorations_displayed = []
    decorations.names_with_id = {}

    for option in decor_options:
        for id in decorations.decor_dict[option].keys():
            if isinstance(id, str) or "WALK" in decorations.decor_dict[option]["action"]:
                continue
            all_decorations_displayed.append((option, id))
            decor = decorations.decor_dict[option][id]
            # Gets x, y position of decoration
            rect = I.pg.Rect(decor["rect"].x, decor["rect"].y, decor["rect"].w, decor["rect"].h)
            image_rect = decor["image"].get_rect()
            decorations.names_with_id[len(decorations.displayed_rects_full)] = option, id
            decorations.displayed_rects_full.append(rect)
            """Gets x, y position of decoration"""

            display_decor_hp(decor, rect, sub_image[1], rooms)
            # I.pg.draw.line(sub_image[1], "green" ,(100,I.info.OFFSCREEN[1] + 340), (1100,I.info.OFFSCREEN[1] + 340), 2)
            # I.pg.draw.line(sub_image[1], "red" ,(100,I.info.OFFSCREEN[1] + 350), (1100,I.info.OFFSCREEN[1] + 350), 2)

            if rect.y + rect.h > I.info.OFFSCREEN[1] + 340:
                if I.info.APPLIANCE_CLICK[0] == "":
                    if option in list(gifs.keys()) and option not in ["Furnace", "Blast Furnace", "Melter"]:
                        if I.info.DOOR_CLICK != (90, "") and I.info.DOOR_CLICK[0] < gifs[I.info.DOOR_CLICK[1]].frame_count and "ENTERABLE" in decorations.decor_dict[option]["action"]:
                            handle_opening_doors(gifs, sub_image[1], rect, rooms, npc, data, spells, sub_image[1], clock)
                        else:
                            render_gif_on_subimage(sub_image[1], (image_rect.w, image_rect.h), (rect.x, rect.y), gifs[option])
                    else:
                        sub_image[1].blit(decor["image"], (rect.x, rect.y))
                elif I.info.APPLIANCE_CLICK[0] in ["Furnace", "Blast Furnace", "Melter"]:
                    if option in list(gifs.keys()):
                        render_gif_on_subimage(sub_image[1], (image_rect.w, image_rect.h), (rect.x, rect.y), gifs[option])
                    else:
                        sub_image[1].blit(decor["image"], (rect.x, rect.y))
                # I.T.Make_rect_visible(sub_image[1], rect, "green")
            # elif rect.y <= I.info.OFFSCREEN[1] + 350:
            else:
                if I.info.APPLIANCE_CLICK[0] == "":
                    if option in list(gifs.keys()) and option not in ["Furnace", "Blast Furnace", "Melter"]:
                        if I.info.DOOR_CLICK != (90, "") and I.info.DOOR_CLICK[0] < gifs[I.info.DOOR_CLICK[1]].frame_count and "ENTERABLE" in decorations.decor_dict[option]["action"]:
                            handle_opening_doors(gifs, sub_image[0], rect, rooms, npc, data, spells, sub_image[0], clock)
                        else:
                            render_gif_on_subimage(sub_image[0], (image_rect.w, image_rect.h), (rect.x, rect.y), gifs[option])
                    else:
                        sub_image[0].blit(decor["image"], (rect.x, rect.y))
                elif I.info.APPLIANCE_CLICK[0] in ["Furnace", "Blast Furnace", "Melter"]:
                    if option in list(gifs.keys()):
                        render_gif_on_subimage(sub_image[0], (image_rect.w, image_rect.h), (rect.x, rect.y), gifs[option])
                    else:
                        sub_image[0].blit(decor["image"], (rect.x, rect.y))
                # I.T.Make_rect_visible(sub_image[0], rect, "red")


            if "Wall" in option:
                adjusted_rect = I.pg.Rect(rect.x, rect.y + rect.h / 4, rect.w, rect.h - rect.h / 4)
            else:
                adjusted_rect = I.pg.Rect(rect.x, rect.y + rect.h / 2, rect.w, rect.h - rect.h / 2)
            # I.T.Make_rect_visible(sub_image[1], adjusted_rect, "red")

            decorations.displayed_rects.append(adjusted_rect)
            if me.colliderect(rect):
                for collision in me.collidelistall(decorations.displayed_rects):
                    name = all_decorations_displayed[collision][0]
                    id_2 = all_decorations_displayed[collision][1]
                    rect_2 = decorations.decor_dict[name][id_2]["rect"]
                    type = decorations.decor_dict[name]["type"]
                    if type in ["NPC", "Appliance"]:
                        rect = I.pg.Rect(rect_2.x, rect_2.y, rect_2.w, rect_2.h)
                        collide = (name, rect, id_2)

                if "door" in option:
                    collide = I.PB.handle_interior_door_collision(collide, option, decorations, id, me, all_decorations_displayed, rect, adjusted_rect)
                if collide == [False]:
                    img_rect = decor["image"].get_rect()
                    new_rect = rect.x, rect.y, img_rect.w, img_rect.h
                    collide = (option, new_rect, id)
    return collide

def render_strikes(screen, gifs, lock, items):
    # types = ["Slashing", "Blunt", "Piercing"]
    types = ["Slashing", "Piercing", "Blunt"]
    for type in types:
        if gifs[type + " Strike"].start_gif:
            if I.info.POS_CHANGE[0] == 0 or I.info.POS_CHANGE[0] == I.info.LAST_ORIENT[0]:
                frame = gifs[type + " Strike"].next_frame(1).copy()
                chosen_weapon = 0
                color = (50, 50, 50, 0)
                for key, (weapon, num) in I.info.EQUIPED.items():
                    if num < 27:
                        chosen_weapon = weapon
                if chosen_weapon != 0:
                    color = Ff.get_property(chosen_weapon, items, "COLOR")
                    if not isinstance(color, tuple):
                        color = (50, 50, 50, 0)
                """Gray weapon: (50, 50, 50, 0)"""
                """red weapon: (50, 255, 255, 0)"""
                """glass weapon: (255, 0, 0, 0)"""
                """obsidian weapon: (100, 250, 100, 0)"""
                frame.fill(color, special_flags=I.pg.BLEND_RGBA_SUB)

                pos = {"Slashing":
                           {"Front.png": (560 + I.info.OFFSCREEN[0], 340 + I.info.OFFSCREEN[1], 0, 1, 100, 50),
                            "Back.png": (560 + I.info.OFFSCREEN[0], 280 + I.info.OFFSCREEN[1], 0, 0, 100, 50),
                            "Left.png": (540 + I.info.OFFSCREEN[0], 310 + I.info.OFFSCREEN[1], 0, 0, 50, 50),
                            "Right.png": (640 + I.info.OFFSCREEN[0], 310 + I.info.OFFSCREEN[1], 1, 0, 50, 50)
                            },
                       "Piercing":
                           {"Front.png": (590 + I.info.OFFSCREEN[0], 340 + I.info.OFFSCREEN[1], 0, 1, 50, 100),
                            "Back.png": (590 + I.info.OFFSCREEN[0], 280 + I.info.OFFSCREEN[1], 0, 0, 50, 100),
                            "Left.png": (550 + I.info.OFFSCREEN[0], 310 + I.info.OFFSCREEN[1], 0, 0, 50, 50),
                            "Right.png": (630 + I.info.OFFSCREEN[0], 310 + I.info.OFFSCREEN[1], 1, 0, 50, 50)
                            },
                       "Blunt":
                           {"Front.png": (590 + I.info.OFFSCREEN[0], 340 + I.info.OFFSCREEN[1], 0, 1, 50, 50),
                            "Back.png": (590 + I.info.OFFSCREEN[0], 280 + I.info.OFFSCREEN[1], 0, 0, 50, 50),
                            "Left.png": (550 + I.info.OFFSCREEN[0], 310 + I.info.OFFSCREEN[1], 0, 0, 50, 50),
                            "Right.png": (630 + I.info.OFFSCREEN[0], 310 + I.info.OFFSCREEN[1], 1, 0, 50, 50)
                            },

                       }

                if I.info.LAST_ORIENT[0] == "Front.png" and lock == 1 or I.info.LAST_ORIENT[0] == "Back.png" and lock == 0: # IF YOU ARE FACING FRONT AND display_strikes IS AFTER display_char OR IF YOU ARE FACING BACK AND display_strikes IS BEFORE display_char THEN TRUE
                    frame = I.pg.transform.flip(frame, pos[type][I.info.LAST_ORIENT[0]][2], pos[type][I.info.LAST_ORIENT[0]][3])
                    scaled_image = I.pg.transform.scale(frame, pos[type][I.info.LAST_ORIENT[0]][4:6])
                    screen.blit(scaled_image, pos[type][I.info.LAST_ORIENT[0]][0:2])
                elif I.info.LAST_ORIENT[0] in ["Left.png", "Right.png"]:
                    frame = I.pg.transform.rotate(frame, 90)
                    frame = I.pg.transform.flip(frame, pos[type][I.info.LAST_ORIENT[0]][2], pos[type][I.info.LAST_ORIENT[0]][3])
                    scaled_image = I.pg.transform.scale(frame, pos[type][I.info.LAST_ORIENT[0]][4:6])
                    screen.blit(scaled_image, pos[type][I.info.LAST_ORIENT[0]][0:2])
                I.info.POS_CHANGE = I.info.LAST_ORIENT[0], type + " Strike"
    # return frame # for testing

def render_folower(sub_image, gifs, data, decorations, mob, items, rooms):
    if I.info.FOLLOWER["Name"] != "":
        if rooms.size == ["1", "1", "1", "1"]:
            size1 = 24
            size2 = 18
        else:
            size1 = 80
            size2 = 60
        # folower default hp 20, default damage = 1, default speed = 2
        # mob[I.info.FOLLOWER[0]] = I.mob_data.Mob(name=I.info.FOLLOWER[0], exp=0, hp=20, allignment=4, count=1, damage=1, speed=1)
        dxdy = (0, 0)
        orientation = {
            (0, 0): "",
            (1, 0): "_Right",
            (-1, 0): "_Left",
            (0, 1): "_Front",
            (0, -1): "_Back",
            (1, -1): "_Back",
            (-1, -1): "_Back",
            (1, 1): "_Front",
            (-1, 1): "_Front"
        }
        # folower_path = "static/images/Playing/NPC/" + I.info.FOLLOWER[0] + "_walk/" + I.info.FOLLOWER[0] + orientation[dxdy] + ".png"
        end_pos = I.info.FOLLOWER["target_pos"]
        initial_pos = I.info.FOLLOWER["current_pos"]

        if end_pos != (0, 0):
            if I.info.FOLLOWER["aggressive"]["attack"]:
                end_pos = I.info.FOLLOWER["aggressive"]["mob_pos"][0:2]
                if initial_pos == end_pos:
                    """Folower hits mob"""
                    if I.info.FOLLOWER["aggressive"]["mob"]["hp"][0] > 0:
                        """ only deals damage if the mob isnt dead """
                        I.info.FOLLOWER["aggressive"]["class"].deal_damage(I.info.FOLLOWER["aggressive"]["mob"], data["Player"], "Follower", items, gifs, rooms, data)
                    I.info.FOLLOWER["aggressive"]["attack"] = False

            I.info.FOLLOWER["current_pos"] = Ff.move_closer(initial_pos, end_pos, 1, decorations.displayed_rects, sub_image, data, 1)

            # print(initial_pos, end_pos, I.info.FOLLOWER[1])
            dxdy = (initial_pos[0] - I.info.FOLLOWER["current_pos"][0]) * -1, (initial_pos[1] - I.info.FOLLOWER["current_pos"][1]) * -1
            dxdy = max(-1, min(int(dxdy[0]), 1)), max(-1, min(int(dxdy[1]), 1))
            I.info.FOLLOWER["orientation"].append(dxdy)
            if len(I.info.FOLLOWER["orientation"]) > 10:
                I.info.FOLLOWER["orientation"] = I.info.FOLLOWER["orientation"][1:]
                dxdy = Ff.get_most_often_tuple(I.info.FOLLOWER["orientation"])


        if orientation[dxdy] in ["_Right", "_Left"]:
            rect = I.pg.Rect(I.info.FOLLOWER["current_pos"][0] - data["Zoom_rect"].x, I.info.FOLLOWER["current_pos"][1] - data["Zoom_rect"].y, size1, size1)
        else:
            rect = I.pg.Rect(I.info.FOLLOWER["current_pos"][0] - data["Zoom_rect"].x, I.info.FOLLOWER["current_pos"][1] - data["Zoom_rect"].y, size2, size2)
        # I.T.Make_rect_visible(sub_image, rect, "red")
        render_gif_on_subimage(sub_image, (rect.w, rect.h), (rect.x, rect.y), gifs[I.info.FOLLOWER["Name"] + orientation[dxdy]])

def handle_tutorial(sub_image, data, screen, npc, items, decorations, gifs, rooms, clock, spells, mobs):
    lines = []
    if I.info.tutorial_flag == 1:
        lines.append(I.pg.Rect(420 - data["Zoom_rect"].x, 150 - data["Zoom_rect"].y, 140, 1))
        # I.T.Make_rect_visible(sub_image[0], lines[0], "red")
        lines.append(I.pg.Rect(420 - data["Zoom_rect"].x, 10 - data["Zoom_rect"].y, 1, 140))
        # I.T.Make_rect_visible(sub_image[0], lines[1], "red")
        lines.append(I.pg.Rect(560 - data["Zoom_rect"].x, 10 - data["Zoom_rect"].y, 1, 140))
        # I.T.Make_rect_visible(sub_image[0], lines[2], "red")
        # print(I.info.Player_rect.collidelistall(lines))
        if I.info.Player_rect.collidelistall(lines) != []:
            I.DialB.init_dialog("Tutorial Man", data["Player"], screen, npc, items, decorations, data, gifs, rooms, clock, spells, mobs)
            I.info.tutorial_flag = 0

def render_char(dx, dy, screen, gifs, data, decorations, collide):
    character_path = 'static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER
    dx, dy = I.PB.handle_walking_through_interior_doors(collide, dx, dy)
    dxdy = (dx, dy)
    orientation = {
        (0, 0): "Stand",
        (1, 0): "Right",
        (-1, 0): "Left",
        (0, 1): "Front",
        (0, -1): "Back",
        (1, -1): "Back",
        (-1, -1): "Back",
        (1, 1): "Front",
        (-1, 1): "Front"
    }
    orientation_images = {
        "Front": ["Front.png", "Front1.png", "Front2.png"],
        "Back": ["Back.png", "Back1.png", "Back2.png"],
        "Right": ["Right.png", "Right1.png", "Right2.png"],
        "Left": ["Left.png", "Left1.png", "Left2.png"]
    }
    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
        if data["Zoom_rect"].x in [0, -1, 1, 680, 681, 679]:
            I.info.OFFSCREEN = I.info.OFFSCREEN[0] + dx * 3 * I.info.FAST, I.info.OFFSCREEN[1]
        else:
            I.info.OFFSCREEN = (0, I.info.OFFSCREEN[1])
        if data["Zoom_rect"].y in [0, -1, 1, 820, 821, 819]:
            I.info.OFFSCREEN = I.info.OFFSCREEN[0], I.info.OFFSCREEN[1] + dy * 3 * I.info.FAST
        else:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0],  0)
    else:
        I.info.OFFSCREEN = I.info.OFFSCREEN[0] + dx * 3 * I.info.FAST, I.info.OFFSCREEN[1] + dy * 3 * I.info.FAST
    if gifs["Ghost"].start_gif:
        frame = gifs["Ghost"].next_frame(-1)
        frame = I.pg.transform.scale(frame, (S.SCREEN_WIDTH / 18, S.SCREEN_HEIGHT / 7))
        screen.blit(frame, [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + I.info.OFFSCREEN[1]])
    else:
        if I.info.COMBAT_RECT[0] != 0 or I.info.AXE[0] != 0 or I.info.PICAXE[0] != 0:
            if dx == 0 and dy == 0:
                for key, value in orientation.items():
                    if value == I.info.LAST_ORIENT[0].split(".")[0]:
                        dx = key[0]
                        dy = key[1]
                        break
                character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + dx * 5 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + dy * 5 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]  # Attacking
            else:
                character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + dx * 10 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + dy * 10 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]
        else:
            character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]  # STANDING STILL

        if S.GOD_MODE and I.info.CURRENT_ROOM["name"] == "House1B1":
            decor = "Wall_vertical"
            # Ff.add_image_to_screen(screen, decorations.decor_dict[decor]["path"],[S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + I.info.OFFSCREEN[1], decorations.decor_dict[decor][0]["rect"].w, decorations.decor_dict[decor][0]["rect"].h * 0.9])  # walking possision could be legs spread
        else:
            orient = orientation[dxdy]
            if orient in orientation_images:
                images = orientation_images[orient]
                if I.info.CURRENT_STANCE == 0 or I.info.CURRENT_STANCE == 2:
                    Ff.add_image_to_screen(screen, character_path + images[0], character_center_pos) # walking possision could be legs spread
                elif I.info.CURRENT_STANCE == 1:
                    Ff.add_image_to_screen(screen, character_path + images[1], character_center_pos) # walking possision could be legs spread diferently
                else:
                    Ff.add_image_to_screen(screen, character_path + images[2], character_center_pos) # walking possision could be no legs spread
                I.info.LAST_ORIENT = orientation_images[orient]
            else:
                Ff.add_image_to_screen(screen, character_path + I.info.LAST_ORIENT[0], character_center_pos) # STANDING STILL

def render_on_subimage(sub_image, size, path, pos):
    image = I.pg.image.load(path).convert_alpha()
    image = I.pg.transform.scale(image, (size[0], size[1]))
    sub_image.blit(image, pos)
    return I.pg.Rect(pos[0], pos[1], size[0], size[1])

def place_decor_by_coordinates(x, y, path, scale, rect_scale):
    items = {}
    image = I.pg.image.load(path).convert_alpha()
    rect = image.get_rect(topleft=(x, y))
    image = I.pg.transform.scale(image, (rect.w * scale[0], rect.h * scale[1]))
    rect.w = rect.w * rect_scale[0]
    rect.h = rect.h * rect_scale[1]
    items[0] = {"image": image, "rect": rect}
    return items

def render_gif_on_subimage(sub_image, size, pos, gif):
    if gif.repeat == 0:
        repeat = 0
    else:
        repeat = -1
    frame = gif.next_frame(repeat)
    frame = I.pg.transform.scale(frame, (size[0], size[1]))
    sprite = I.S.Sprite(frame, I.pg.Rect(pos[0], pos[1], size[0], size[1]))
    if isinstance(sub_image, I.pg.surface.Surface):
        sub_image.blit(frame, pos)
    else:
        sub_image.add(sprite)
    return I.pg.Rect(pos[0], pos[1], size[0], size[1])

def render_light(screen, decorations, rooms, data):
    for decoration in rooms.decor:
        if "LIGHT SOURCE" in decorations.decor_dict[decoration]["action"]:
            radius = decorations.decor_dict[decoration]["action"].find("LIGHT SOURCE")
            radius = int(decorations.decor_dict[decoration]["action"][radius:].split(",,")[0].split(":")[1])
            radius_2 = int(radius * 0.5)

            if rooms.type not in ["House", "Prison"]:
                radius = int(radius / 4)
                radius_2 = int(radius / 4)

            if I.info.LIGHT[0] == 0:
                I.info.LIGHT[0] = Ff.create_light_mask(radius_2, (10, 10, 10))
            if I.info.LIGHT[1] == 0:
                I.info.LIGHT[1] = Ff.create_light_mask(radius, (20, 20, 20))

            if rooms.type in ["House", "Prison"]:
                dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)
                dim_surface.fill((0, 0, 0, rooms.light))
                screen.blit(dim_surface, (0, 0))
            for id in decorations.decor_dict[decoration].keys():
                if isinstance(id, int):
                    light_source_x = decorations.decor_dict[decoration][id]["rect"].x + decorations.decor_dict[decoration][id]["rect"].w / 2
                    light_source_y = decorations.decor_dict[decoration][id]["rect"].y + decorations.decor_dict[decoration][id]["rect"].h / 2
                    if rooms.type in ["House", "Prison"]:
                        screen.blit(I.info.LIGHT[0], (light_source_x - radius_2, light_source_y - radius_2),special_flags=I.pg.BLEND_RGBA_ADD)
                        screen.blit(I.info.LIGHT[1], (light_source_x - radius, light_source_y - radius),special_flags=I.pg.BLEND_RGBA_ADD)
                    else:
                        screen.blit(I.info.LIGHT[0], (light_source_x - radius_2 - data["Zoom_rect"].x, light_source_y - radius_2 - data["Zoom_rect"].y),special_flags=I.pg.BLEND_RGBA_ADD)
                        screen.blit(I.info.LIGHT[1], (light_source_x - radius - data["Zoom_rect"].x, light_source_y - radius - data["Zoom_rect"].y),special_flags=I.pg.BLEND_RGBA_ADD)

def render_house(screen, data, rooms):

    door_rect = None
    screen.fill("black")
    tile_pos = (S.SCREEN_WIDTH * float(rooms.size[0]), S.SCREEN_HEIGHT * float(rooms.size[1]), S.SCREEN_WIDTH * float(rooms.size[2]), S.SCREEN_HEIGHT * float(rooms.size[3]))
    Ff.add_image_to_screen(screen, S.DECOR_PATH[rooms.background], tile_pos)

    if rooms.type not in ["Prison"] and "B1" not in rooms.name:
        door_rect = I.pg.Rect(S.SCREEN_WIDTH * 0.45, S.SCREEN_HEIGHT * 0.875, S.SCREEN_WIDTH * 0.11, S.SCREEN_HEIGHT * 0.025)
        I.T.Make_rect_visible(screen, door_rect, (45, 19, 4, 255))
    return door_rect

def interior_border_rect(decorations):
    left = S.SCREEN_WIDTH * 0.1
    top = S.SCREEN_HEIGHT * 0.05
    width = S.SCREEN_WIDTH * 0.8
    height = S.SCREEN_HEIGHT * 0.85

    if I.info.CURRENT_ROOM["Type"] == "Prison":
        left = S.SCREEN_WIDTH * 0.33
        top = S.SCREEN_HEIGHT * 0.28
        width = S.SCREEN_WIDTH * 0.33
        height = S.SCREEN_HEIGHT * 0.43

    right = left + width
    bottom = top + height

    top_rect = I.pg.Rect(left, top, right - left, 30) # top
    right_rect = I.pg.Rect(right,top, 30, bottom - top) # right
    left_rect = I.pg.Rect(left, top, 30, bottom - top) # left
    bottom_rect = I.pg.Rect(left, bottom, right - left, 30) # bottom

    decorations.displayed_rects.append(top_rect)
    decorations.displayed_rects.append(right_rect)
    decorations.displayed_rects.append(left_rect)
    decorations.displayed_rects.append(bottom_rect)
    return [top_rect, right_rect, left_rect, bottom_rect]

def decorate_from_db(rooms, decorations):
    for decor_name in rooms.decor:
        path = decorations.decor_dict[decor_name]["path"]
        health = decorations.decor_dict[decor_name]["health"]
        action = decorations.decor_dict[decor_name]["action"]
        if decor_name in ["Furnace", "Blast Furnace"]:
            path += "out.png"
        elif path[-1] == "_":
            path += "0.png"
        if rooms.data.get(decor_name) == None:
            continue
        # print(rooms.data[decor_name])
        for i in range(0, len(rooms.data[decor_name])):
            image, rect = decorations.place_decor_by_coordinates(rooms.data[decor_name][i]["x"], rooms.data[decor_name][i]["y"], path, (rooms.data[decor_name][i]["img_x"], rooms.data[decor_name][i]["img_y"]), (rooms.data[decor_name][i]["rect_x"], rooms.data[decor_name][i]["rect_y"]))
            # dec_sprite = I.S.create_sprite_decoration(decor_name, i, image, rect, "", health, action, path)
            # I.S.LayeredGroup.add(dec_sprite, layer=5)
            # DecorationGroup.add(dec_sprite)

            if "LOCKED" in decorations.decor_dict[decor_name]["action"]:
                action_string = decorations.decor_dict[decor_name]["action"]
                locked_str_id = action_string.find("LOCKED")
                locked_string = action_string[locked_str_id:].split(",,")[0]
                day_night_str_id = locked_string.find("DAY_NIGHT:")
                difficulty_id = locked_string.find("DIFF:")
                day_night = int(locked_string[day_night_str_id:].split(",")[0].split(":")[1])
                if day_night < I.info.DIM:
                    decorations.decor_dict[decor_name][i] = {"name": decor_name, "id": i, "image": image, "rect": rect, "effect": "LOCKED", "health": health}
                else:
                    decorations.decor_dict[decor_name][i] = {"name": decor_name, "id": i, "image": image, "rect": rect, "effect": "UNLOCKED", "health": health}
            else:
                decorations.decor_dict[decor_name][i] = {"name": decor_name, "id": i, "image": image, "rect": rect, "effect": "", "health": health}

def render_lower_upper_decor(option, gifs, new_subimage, rect, rooms, clock, screen, decor, decorations, data, spells, npc):
    if option in list(gifs.keys()):
        if "door" not in option and "Wave" not in option:
            # Display all gifs appart from door and wave.
            size = decor["image"].get_rect()
            render_gif_on_subimage(new_subimage, (size.w, size.h), (rect.x, rect.y), gifs[option])
        elif "Wave" in option:
            if gifs[option].pause == 0:
                render_gif_on_subimage(new_subimage, (rect.w, rect.h), (rect.x, rect.y), gifs[option])
            if gifs[option].current_frame == 0 and gifs[option].pause == 0 and option in ["Wave1", "Wave4"]:
                gifs[option].pause = 1
                # I.pg.time.set_timer(I.pg.USEREVENT + 11, 2000)
                I.th.start_thread(5000, "waves", gifs)
        elif I.info.DOOR_CLICK != (90, "") and I.info.DOOR_CLICK[0] < gifs[I.info.DOOR_CLICK[1]].frame_count and I.info.DOOR_CLICK[1] == option:
            handle_opening_doors(gifs, new_subimage, rect, rooms, npc, data, spells, screen, clock)
    else:
        # size = decor["image"].get_rect()
        #
        # decor["image"] = I.pg.transform.scale(decor["image"], (size.w, size.h))
        sprite = I.S.Sprite(decor["image"], rect)
        new_subimage.add(sprite)
        # new_subimage.blit(decor["image"], (rect.x, rect.y))

def handle_giant_tree(name, decorations, rect, sub_image, collide):
    adjusted_rect = I.pg.Rect(rect.x, rect.y + rect.h * 0.75, rect.w, rect.h * 0.15)
    second_rect = I.pg.Rect(rect.x + rect.w * 0.35, rect.y + rect.h * 0.5, rect.w * 0.3, rect.h * 0.3)
    # I.T.Make_rect_visible(sub_image[0], second_rect, "red")
    # I.T.Make_rect_visible(sub_image[0], adjusted_rect, "blue")
    decorations.displayed_rects.append(second_rect)
    if I.info.Player_rect.colliderect(second_rect):
        collide = (name, adjusted_rect)
    return collide, adjusted_rect

def handle_map_walk(data, rooms, screen=0, clock=0, spells=0, npc=0, mob=0, decorations=0, items=0):
    if rooms.type in ["Village"]:
        room_change = 0, 0
        if I.info.OFFSCREEN[0] != 0:
            if data["Zoom_rect"].x + I.info.OFFSCREEN[0] / 3 < data["Zoom"][0] * -0.65:
                # print("Went LEFT", data["Zoom_rect"].x + I.info.OFFSCREEN[0] / 3, data["Zoom"][0] * -0.65)
                room_change = -1, 0
            elif data["Zoom_rect"].x + I.info.OFFSCREEN[0] / 3 > S.SCREEN_WIDTH * 0.7:

                # print("Went RIGHT", data["Zoom_rect"].x + I.info.OFFSCREEN[0] / 3, S.SCREEN_WIDTH * 0.7)
                room_change = 1, 0
        elif I.info.OFFSCREEN[1] != 0:
            if data["Zoom_rect"].y + I.info.OFFSCREEN[1] / 3 < data["Zoom"][1] * -0.65:
                # print("Went UP", data["Zoom_rect"].y + I.info.OFFSCREEN[1] / 3)
                room_change = 0, -1
            elif data["Zoom_rect"].y + I.info.OFFSCREEN[1] / 3 > S.SCREEN_HEIGHT + data["Zoom"][1] * 1.2:
                # print("Went DOWN", data["Zoom_rect"].y + I.info.OFFSCREEN[1] / 3)
                room_change = 0, 1
        if room_change != (0, 0):
            name = I.info.CURRENT_ROOM["name"]
            values = name.split("_")
            name = values[0] + "_" + str(int(values[1]) + room_change[0]) + "_" + str(int(values[2]) + room_change[1])
            I.GB.restore_guard_decor(rooms)
            rooms.select_room(name)
            I.info.CURRENT_ROOM = {"name": name, "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": "Village"}
            if I.info.DEATH_SAVE != 0:
                I.info.DEATH_SAVE = I.info.DEATH_SAVE[0], I.info.DEATH_SAVE[1], I.info.DEATH_SAVE[2], I.info.DEATH_SAVE[3], I.info.DEATH_SAVE[4],  1

            if screen != 0:
                I.PB.update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt",data["Player"], spells.selected_spell, npc)
                I.info.RESET = True
                # Play.Start(screen, clock, rooms)
                # decorations, gifs, items, spells, mob, npc, songs, dim_surface, collide, pressed, data = Play.reset(rooms, screen)

def display_decor_hp(decor, rect, sub_image, rooms):
    if int(decor["health"].split(",,")[1].split(",")[0]) < int(decor["health"].split(",,")[1].split(",")[1]):
        if rooms.size == ["1", "1", "1", "1"]:
            height = 1
        else:
            height = 3
        hp_rect1 = (rect.x, rect.y - rect.h * 0.2, rect.w, height)
        remainder_hp = float(decor["health"].split(",,")[1].split(",")[0]) / float(decor["health"].split(",,")[1].split(",")[1])
        hp_rect2 = (rect.x, rect.y - rect.h * 0.2, rect.w * remainder_hp, height)
        if isinstance(sub_image, I.pg.surface.Surface):
            I.pg.draw.rect(sub_image, "red", hp_rect1)
            I.pg.draw.rect(sub_image, "green", hp_rect2)
        else:
            image1 = I.pg.Surface((rect.w, height))
            image2 = I.pg.Surface((rect.w * remainder_hp, height))
            image1.fill("red")
            image2.fill("green")
            sprite1 = I.S.Sprite(image1, hp_rect1)
            sprite2 = I.S.Sprite(image2, hp_rect2)
            sub_image.add(sprite1)
            sub_image.add(sprite2)


def process_decor(option, gifs, sub_image, rect, rooms, clock, screen, decor, decorations, data, spells, npc, collide, id):
    render_lower_upper_decor(option, gifs, sub_image, rect, rooms, clock, screen, decor, decorations, data, spells, npc)

    adjusted_rect = I.pg.Rect(rect.x, rect.y + rect.h / 2, rect.w, rect.h - rect.h / 2)

    if option == "Tree_SB_1":
        collide, adjusted_rect = handle_giant_tree(option, decorations, rect, sub_image, collide)


    if decorations.decor_dict[option]["type"] == "House":
        adjusted_rect = I.pg.Rect(rect.x, rect.y + rect.h / 2, rect.w, rect.h - rect.h / 2 - 1)

    if decor["image"].get_rect().h == adjusted_rect.h:
        adjusted_rect = I.pg.Rect(adjusted_rect.x, adjusted_rect.y - adjusted_rect.h, adjusted_rect.w,
                                  adjusted_rect.h * 2)
    display_decor_hp(decor, rect, sub_image, rooms)

    if "Wave" not in option:
        decorations.displayed_rects.append(adjusted_rect)  # Add to the list of displayed rectangles

    if I.info.Player_rect.colliderect(adjusted_rect):
        collide = (option, rect, id)

    return collide

def handle_opening_doors(gifs, new_subimage, rect, rooms, npc, data, spells, screen, clock):
    if I.pg.time.get_ticks() - gifs[I.info.DOOR_CLICK[1]].frame_time > gifs[I.info.DOOR_CLICK[1]].delay:
        I.info.DOOR_CLICK = I.info.DOOR_CLICK[0] + 1, I.info.DOOR_CLICK[1]
    render_gif_on_subimage(new_subimage, (rect.w, rect.h), (rect.x, rect.y), gifs[I.info.DOOR_CLICK[1]])
    if I.info.DOOR_CLICK[0] == gifs[I.info.DOOR_CLICK[1]].frame_count:
        building = I.info.DOOR_CLICK[1].split("_")[0]
        gifs[I.info.DOOR_CLICK[1]].start_gif = False
        gifs[I.info.DOOR_CLICK[1]].current_frame = 0
        I.info.DOOR_CLICK = 90, ""  # RESET I.info.DOOR_CLICK
        if rooms.room_dict.get(building) != None:
            I.GB.restore_guard_decor(rooms)
            rooms.select_room(building)
            I.info.CURRENT_ROOM = {"name": building, "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": "House"}
            I.info.ENTRY_POS = (1, 1)
            I.info.OFFSCREEN = (25, 250)
            I.PB.update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"], spells.selected_spell, npc)
            # Play.Start(screen, clock, rooms)
            I.info.RESET = True
        else:
            print("ROOM DOESN'T EXIST")

def handle_outside_render(data, decorations, removable_list, items, spells, npc, screen, clock, gifs, rooms, collide, sub_image, mob, songs, decor_screen):

    decorations.displayed_rects = []  # List to keep track of displayed rectangles
    decorations.displayed_rects_full = []  # List to keep track of displayed rectangles
    decorations.names_with_id = {}
    update_decor_dict(decorations, gifs, rooms, items)
    decor_options = rooms.decor
    for option in decor_options:
        for id in decorations.decor_dict[option].keys():
            if isinstance(id, str) or "WALK" in decorations.decor_dict[option]["action"]:
                continue

            decor = decorations.decor_dict[option][id]

            # Gets x, y position of decoration
            decor_x = decor["rect"].x - data["Zoom_rect"].x
            decor_y = decor["rect"].y - data["Zoom_rect"].y
            rect = I.pg.Rect(decor_x, decor_y, decor["rect"].w, decor["rect"].h)
            decorations.displayed_rects_full.append(rect)
            decorations.names_with_id[len(decorations.displayed_rects_full)] = (option, id)

            if I.pg.math.Vector2(145 - rect.x, 80 - rect.y).length() and "MOB SPAWN_DISTANCE" in decorations.decor_dict[option]["action"]:
                word, distance = decorations.decor_dict[option]["action"].split(":")
                if int(distance) > I.pg.math.Vector2(145 - rect.x, 80 - rect.y).length():
                    Ff.update_map_view(id, option, gifs, "remove_gif", rooms.name)
                    temp_rect = rect.x + data["Zoom_rect"].x, rect.y + data["Zoom_rect"].y, rect.w, rect.h
                    if (id, option, temp_rect, "decor-decor") not in list(data["Queue_to_be_removed"].queue):
                        data["Queue_to_be_removed"].put((id, option.replace("Hidden", "Raising"), temp_rect, "decor-decor"))



            if option == "Water Elemental_Raising" and gifs[option].start_gif:
                Ff.update_map_view(id, option, gifs, "remove_gif", rooms.name)
                gifs[option].repeat = 0
                temp_rect = rect.x + data["Zoom_rect"].x, rect.y + data["Zoom_rect"].y, rect.w, rect.h

                if (id, option, temp_rect, "decor-mob:Water Elemental") not in list(data["Queue_to_be_removed"].queue):
                    data["Queue_to_be_removed"].put((id, option, temp_rect, "decor-mob:Water Elemental"))



            if int(decor["health"].split(",,")[1].split(",")[0]) == 0:  # if decor is without health dont display it.
                # removable_list.append((option, id))
                I.TB.handle_axe_rewards(decorations, option, items, rooms, data, id)
                Ff.update_map_view(id, option, (0, 0, 0, 0), "remove", rooms.name)
                continue

            I.TB.handle_axe_chopping(rect, option, decorations.decor_dict, id, items, gifs, data)

            I.TB.handle_picaxe_chopping(rect, option, decorations.decor_dict, id, items)

            # Check and process decorations in the upper part of the screen
            if decor_y - rect.h / 2 <= 79 + I.info.OFFSCREEN[1] / 4:
                collide = process_decor(option, gifs, I.S.Sub_image1, rect, rooms, clock, screen, decor, decorations, data, spells, npc, collide, id)
                I.SB.spell_effect_render_on_decor(decor_screen[0], decor, gifs, data)

            if decor_y + rect.h / 2 >= 84 + I.info.OFFSCREEN[1] / 4:
                collide = process_decor(option, gifs, I.S.Sub_image2, rect, rooms, clock, screen, decor, decorations, data, spells, npc, collide, id)
                I.SB.spell_effect_render_on_decor(decor_screen[1], decor, gifs, data)


            collide = render_dam_border(rooms, data, decorations, collide)

            if collide[0] != False and "Wave" in collide[0]:
                collide = [False]

    return collide

def render_dam_border(rooms, data, decorations, collide):
    if rooms.type == "Village" and rooms.name == "Village_10_9":
        border1 = I.pg.Rect(467 - data["Zoom_rect"].x, 174 - data["Zoom_rect"].y, 44, 10)
        # I.T.Make_rect_visible(sub_image[0], border1, "red")
        decorations.displayed_rects.append(border1)

        border2 = I.pg.Rect(462 - data["Zoom_rect"].x, 174 - data["Zoom_rect"].y, 10, 190)
        # I.T.Make_rect_visible(sub_image[0], border2, "yellow")
        decorations.displayed_rects.append(border2)

        border3 = I.pg.Rect(505 - data["Zoom_rect"].x, 174 - data["Zoom_rect"].y, 10, 88)
        # I.T.Make_rect_visible(sub_image[0], border3, "yellow")
        decorations.displayed_rects.append(border3)

        border4 = I.pg.Rect(505 - data["Zoom_rect"].x, 292 - data["Zoom_rect"].y, 195, 10)
        # I.T.Make_rect_visible(sub_image[0], border4, "red")
        decorations.displayed_rects.append(border4)

        border5 = I.pg.Rect(505 - data["Zoom_rect"].x, 292 - data["Zoom_rect"].y, 10, 70)
        # I.T.Make_rect_visible(sub_image[0], border5, "yellow")
        decorations.displayed_rects.append(border5)

        border6 = I.pg.Rect(505 - data["Zoom_rect"].x, 258 - data["Zoom_rect"].y, 195, 10)
        # I.T.Make_rect_visible(sub_image[0], border6, "red")
        decorations.displayed_rects.append(border6)

        border7 = I.pg.Rect(695 - data["Zoom_rect"].x, 264 - data["Zoom_rect"].y, 10, 40)
        # I.T.Make_rect_visible(sub_image[0], border7, "yellow")
        decorations.displayed_rects.append(border7)

        border8 = I.pg.Rect(905 - data["Zoom_rect"].x, 340 - data["Zoom_rect"].y, 95, 10)
        # I.T.Make_rect_visible(sub_image[0], border8, "yellow")
        decorations.displayed_rects.append(border8)

        border9 = I.pg.Rect(705 - data["Zoom_rect"].x, 338 - data["Zoom_rect"].y, 200, 10)
        # I.T.Make_rect_visible(sub_image[0], border9, "yellow")
        decorations.displayed_rects.append(border9)

        border10 = I.pg.Rect(505 - data["Zoom_rect"].x, 336 - data["Zoom_rect"].y, 200, 10)
        # I.T.Make_rect_visible(sub_image[0], border10, "yellow")
        decorations.displayed_rects.append(border10)

        border11 = I.pg.Rect(400 - data["Zoom_rect"].x, 310 - data["Zoom_rect"].y, 70, 10)
        # I.T.Make_rect_visible(sub_image[0], border11, "yellow")
        decorations.displayed_rects.append(border11)

        border12 = I.pg.Rect(200 - data["Zoom_rect"].x, 308 - data["Zoom_rect"].y, 200, 10)
        # I.T.Make_rect_visible(sub_image[0], border12, "yellow")
        decorations.displayed_rects.append(border12)

        border13 = I.pg.Rect(0 - data["Zoom_rect"].x, 306 - data["Zoom_rect"].y, 200, 10)
        # I.T.Make_rect_visible(sub_image[0], border13, "yellow")
        decorations.displayed_rects.append(border13)

        rect_list = [border1, border2, border3, border4, border5, border6, border7, border8, border9, border10, border11, border12, border13]
        collide_id = I.info.Player_rect.collidelistall(rect_list)
        if collide_id != []:
            # print(collide_id)
            collide = ("border", rect_list[collide_id[0]])

    return collide

def update_decor_dict(decorations, gifs, rooms, items):
    remove_list = []

    """if remove_gif, waits for the gif to hti repeat == 1 if gif_ended waits for start_gif = False"""
    if I.info.MAP_CHANGE.get(rooms.name) != None and I.info.MAP_CHANGE[rooms.name].get("add") != None:
        for decor_name in I.info.MAP_CHANGE[rooms.name]["add"].keys():
            if decorations.decor_dict.get(decor_name) != None:
                """decoration exists in decor_dict"""
                for id, rect in I.info.MAP_CHANGE[rooms.name]["add"][decor_name].items():
                    if decorations.decor_dict[decor_name].get(id) == None:
                        """item doesn't exist on the map"""
                        path = decorations.decor_dict[decor_name]["path"]
                        if path[-1] == "_":
                            gifs[decor_name].Start_gif(decor_name, rect)
                            path += "0.png"
                        health = decorations.decor_dict[decor_name]["health"]
                        image = I.pg.image.load(path).convert_alpha()
                        if rooms.size == ['1','1','1','1']:
                            coordinates = rooms.room_dict[rooms.name]["coordinates"]
                            decor = rooms.room_dict[rooms.name]["decor"].split(", ")
                            coordinate_per_decor = coordinates.split(",,,")
                            for i in range(0, len(coordinate_per_decor)):
                                if decor[i].strip() == decor_name.replace("_Harvested", ""):
                                    decor_coordinates = coordinate_per_decor[i].strip().split(",,")
                                    image_rect = image.get_rect()
                                    if len(decor_coordinates) - 1 >= id:
                                        """coordinates exist in room in db"""
                                        rect2 = decor_coordinates[id].split(",")
                                    else:
                                        """new item being created coordinates don't exist in room db"""
                                        """made when one decor turns to another, pvz plant bed to tree reducing size of y coordinate so a tree wouldnt be placed lower than the plant bed"""
                                        sizes = decor_coordinates[0].split(",")[2:]
                                        rect2 = (rect[0], int(rect[1]) - (int(image_rect[3]) * int(sizes[3])) / 2 , sizes[0], sizes[1], sizes[2], sizes[3])
                                    new_rect = I.pg.Rect(int(rect2[0]), int(rect2[1]), image_rect[2] * int(rect2[2]), image_rect[3] * int(rect2[3]))
                                    if (rect[2], rect[3]) == (new_rect[2], new_rect[3]):
                                        """if the sizes of the new calculated rect and the original one are matching dont need to change the Y coordinate"""
                                        new_rect.y = rect[1]
                                    image = I.pg.transform.scale(image, (image_rect[2] * int(rect2[2]), image_rect[3] * int(rect2[3])))
                                    decorations.decor_dict[decor_name][id] = {"name": decor_name, "id": id, "image": image, "rect": new_rect, "effect": "", "health": health}
                                    break
                                elif len(coordinate_per_decor) == i+1:
                                    """item was not declared in the room, new item"""
                                    if decorations.decor_dict[decor_name].get(id) == None:
                                        """item doesn;t exist in the room"""
                                        rect = I.pg.Rect(rect)
                                        decorations.decor_dict[decor_name][id] = {"name": decor_name, "id": id, "image": image, "rect": rect, "effect": "", "health": health}
                            # img_rect = image.get_rect(topleft=(rect[0], rect[1]))
                            # if len(rect) > 2:
                            #     img_rect.w = rect[2]
                            #     img_rect.h = rect[3]
                            #     image = I.pg.transform.scale(image, (rect[2], rect[3]))
                            # decorations.decor_dict[decor_name][id] = {"name": decor_name, "id": id, "image": image, "rect": img_rect, "effect": "", "health": health}
                        else:
                            coordinates = rooms.room_dict[rooms.name]["coordinates"]
                            decor = rooms.room_dict[rooms.name]["decor"].split(", ")
                            coordinate_per_decor = coordinates.split(",,,")
                            for i in range(0, len(coordinate_per_decor)):
                                if decor[i].strip() == decor_name.replace("_Harvested", ""):
                                    decor_coordinates = coordinate_per_decor[i].strip().split(",,")
                                    rect2 = decor_coordinates[id].split(",")
                                    image_rect = image.get_rect()
                                    new_rect = I.pg.Rect(int(rect2[0]), int(rect2[1]), image_rect[2] * int(rect2[4]), image_rect[3] * int(rect2[5]))
                                    image = I.pg.transform.scale(image, (image_rect[2] * int(rect2[2]), image_rect[3] * int(rect2[3])))
                                    decorations.decor_dict[decor_name][id] = {"name": decor_name, "id": id, "image": image, "rect": new_rect, "effect": "", "health": health}
                                    break
                                elif len(coordinate_per_decor) == i+1:
                                    """item was not declared in the room, new item"""
                                    if decorations.decor_dict[decor_name].get(id) == None:
                                        """item doesn;t exist in the room"""
                                        rect = I.pg.Rect(rect)
                                        image = I.pg.transform.scale(image, (rect[2], rect[3])) # did this cuz prizon guard is tiny
                                        decorations.decor_dict[decor_name][id] = {"name": decor_name, "id": id, "image": image, "rect": rect, "effect": "", "health": health}

                        if decor_name not in rooms.decor:
                            rooms.decor.append(decor_name)
                            # print(decorations.decor_dict[decor_name][id], "was added")
            else:
                """decoration doesn't exist in decor_dict, creating key"""
                # old_name_split = option.split("_") # if its a tree this helps, if its a potion, this is bad
                # old_name = old_name_split[0] + "_" + old_name_split[1] + "_" + old_name_split[2]
                old_name = decor_name.replace("_Harvested","")
                if decorations.decor_dict.get(old_name) != None:
                    """old name exists, using it's data"""
                    decor_data = decorations.decor_dict[old_name]
                    if "HARVESTABLE" in decor_data["action"]:
                    # if "Tree" in old_name or "Flower_Pot" in old_name:
                        new_path = decor_data["path"].replace(".png", "")
                        new_path += "_" + "Harvested" + ".png"
                        action = decor_data["action"].copy()
                    decorations.decor_dict[decor_name] = {
                        'action': action,
                        'health': decor_data["health"],
                        'type': decor_data["type"],
                        'path': new_path}
                else:
                    print("doesn't exist: ", decor_name, "creating it")
    if I.info.MAP_CHANGE.get(rooms.name) != None and I.info.MAP_CHANGE[rooms.name].get("remove") != None:
        for decor_name in I.info.MAP_CHANGE[rooms.name]["remove"].keys():
            if decor_name not in list(I.info.MAP_CHANGE[rooms.name]["add"].keys()):
                """decor was not created previously by this function"""
                for id in I.info.MAP_CHANGE[rooms.name]["remove"][decor_name]:
                    if decorations.decor_dict[decor_name].get(id) != None:
                        del decorations.decor_dict[decor_name][id]
            else:
                """decor may have been previously created by this function"""
                for id in I.info.MAP_CHANGE[rooms.name]["remove"][decor_name]:
                    if id in list(I.info.MAP_CHANGE[rooms.name]["add"][decor_name].keys()):
                        """decor was created by this function, removing from list and removing decor"""
                        remove_list.append((rooms.name, "add", decor_name, id))
                        remove_list.append((rooms.name, "remove", decor_name, id))
                        del decorations.decor_dict[decor_name][id]
                    else:
                        if decorations.decor_dict[decor_name].get(id) != None:
                            del decorations.decor_dict[decor_name][id]
        # I.info.MAP_CHANGE[rooms.name]["remove"] = {}
    if I.info.MAP_CHANGE.get(rooms.name) != None and I.info.MAP_CHANGE[rooms.name].get("remove_gif") != None:
        # remove_list = []
        for gif_name in I.info.MAP_CHANGE[rooms.name]["remove_gif"].keys():
            for id in I.info.MAP_CHANGE[rooms.name]["remove_gif"][gif_name]:
                if gifs[gif_name].repeat == 1:
                    # gifs[gif_name].start_gif = False
                    if decorations.decor_dict[gif_name].get(id) != None:
                        del decorations.decor_dict[gif_name][id]
                # remove_list.append(gif_name)
        # for name in remove_list:
        #     del I.info.MAP_CHANGE["remove_gif"][rooms.name][name]
    if I.info.MAP_CHANGE.get(rooms.name) != None and I.info.MAP_CHANGE[rooms.name].get("add_bypassed") != None:
        for decor_name in I.info.MAP_CHANGE[I.info.CURRENT_ROOM["name"]]["add_bypassed"].keys():
            if decorations.decor_dict.get(decor_name) != None:
                for id, rect in I.info.MAP_CHANGE[I.info.CURRENT_ROOM["name"]]["add_bypassed"][decor_name].items():
                    if decorations.decor_dict[decor_name].get(id) == None:
                        path = decorations.decor_dict[decor_name]["path"]
                        health = decorations.decor_dict[decor_name]["health"]
                        image = I.pg.image.load(path).convert_alpha()
                        if rooms.size != ['1','1','1','1']:
                            image = I.pg.transform.scale(image, (rect[2] * 4, rect[3] * 4))
                        img_rect = image.get_rect(topleft=(rect[0], rect[1]))
                        if len(rect) > 2:
                            img_rect.w = rect[2]
                            img_rect.h = rect[3]
                            image = I.pg.transform.scale(image, (rect[2], rect[3]))
                        print("placed down:", decor_name, id, "at",  img_rect)
                        decorations.decor_dict[decor_name][id] = {"name": decor_name, "id": id, "image": image, "rect": img_rect, "effect": "", "health": health}
                        if decor_name not in rooms.decor:
                            rooms.decor.append(decor_name)
            else:
                """decoration doesn't exist in decor_dict, creating key"""
                # old_name_split = option.split("_") # if its a tree this helps, if its a potion, this is bad
                # old_name = old_name_split[0] + "_" + old_name_split[1] + "_" + old_name_split[2]
                old_name = decor_name.replace("_Harvested","")
                if decorations.decor_dict.get(old_name) != None:
                    """old name exists, using it's data"""
                    decor_data = decorations.decor_dict[old_name]
                    if "HARVESTABLE" in decor_data["action"]:
                    # if "Tree" in old_name or "Flower_Pot" in old_name:
                        new_path = decor_data["path"].replace(".png", "")
                        new_path += "_" + "Harvested" + ".png"
                    decorations.decor_dict[decor_name] = {
                        'action': decor_data["action"],
                        'health': decor_data["health"],
                        'type': decor_data["type"],
                        'path': new_path}
                else:
                    print("decoration doesn't exist, creating it. It only works with anvil, probs would work with any item")
                    decorations.decor_dict[old_name] = {
                        'action': "Smash",
                        'health': "True,,10,10",
                        'type': "item",
                        'path': items.item_dict[old_name]["path"]
                    }
    if I.info.MAP_CHANGE.get(rooms.name) != None and I.info.MAP_CHANGE[rooms.name].get("gif_ended") != None:
        for decor_name in I.info.MAP_CHANGE[rooms.name]["gif_ended"].keys():
            if gifs[decor_name].start_gif == False:
                for id in I.info.MAP_CHANGE[rooms.name]["gif_ended"][decor_name]:
                    if decorations.decor_dict[decor_name].get(id) != None:
                        del decorations.decor_dict[decor_name][id]
    if I.info.MAP_CHANGE.get(rooms.name) != None and I.info.MAP_CHANGE[rooms.name].get("add_effect") != None:
        for decor_name in I.info.MAP_CHANGE[rooms.name]["add_effect"].keys():
            if decorations.decor_dict.get(decor_name) != None:
                """decoration exists in database"""
                for id, effect in I.info.MAP_CHANGE[rooms.name]["add_effect"][decor_name].items():
                    if decorations.decor_dict[decor_name].get(id) != None:
                        """decoration exists on the map"""
                        if decorations.decor_dict[decor_name][id]["effect"] == '':
                            decorations.decor_dict[decor_name][id]["effect"] = effect
                        elif effect not in decorations.decor_dict[decor_name][id]["effect"]:
                            decorations.decor_dict[decor_name][id]["effect"] += ",," + effect
                    else:
                        # print("can not add effect to non existing decor")
                        remove_list.append((rooms.name, "add_effect", decor_name, id))

            else:
                print("decor doesn't exist in database, can not add effect")
    for room_name, case, decor_name, id in remove_list:
        del I.info.MAP_CHANGE[room_name][case][decor_name][id]


def render_bacground_decor(sub_image, decorations, data, collide, case, rooms, npc, spells):
    for option in decorations.decor_dict.keys():
        if "WALK" in decorations.decor_dict[option]["action"]:
            for id in decorations.decor_dict[option].keys():
                if isinstance(id, int):
                    decor = decorations.decor_dict[option][id]
                    decor_x = decor["rect"].x - data["Zoom_rect"].x
                    decor_y = decor["rect"].y - data["Zoom_rect"].y
                    decorations.displayed_rects_full.append(decor["rect"])

                    rect = I.pg.Rect(decor_x, decor_y, decor["rect"].w, decor["rect"].h)
                    # if "PLANT" in decor["effect"]:
                    #     plant_effect_data = decor["effect"].split(":")
                    #     if len(plant_effect_data) == 4:
                    #         I.PlantB.render_growing_plants(plant_effect_data, decorations, option, id)


                    # size = decor["image"].get_rect()
                    # decor["image"] = I.pg.transform.scale(decor["image"], (size.w, size.h))
                    sub_image.blit(decor["image"], (rect.x, rect.y))
                    if case == "outside":
                        if I.info.Player_rect.colliderect(rect):
                            collide = [option, id]
                    else:
                        foot_rect = I.pg.Rect(I.info.OFFSCREEN[0] + 600, I.info.OFFSCREEN[1] + 370, 10, 10)
                        if foot_rect.colliderect(rect):
                            if decorations.decor_dict[option]["type"] == "Stairs":
                                I.info.RESET = "Stairs"
                                if "down" in option:
                                    if "B1" in rooms.name:
                                        new_name = rooms.name.replace("B1", "B2")
                                    else:
                                        new_name = rooms.name + "B1"
                                elif "up" in option:
                                    if "B2" in rooms.name:
                                        new_name = rooms.name.replace("B2", "B1")
                                    else:
                                        new_name = rooms.name.replace("B1", "")
                                pos = I.info.OFFSCREEN[0] - 10, I.info.OFFSCREEN[1] - 20
                                rooms.select_room(new_name)
                                I.info.OFFSCREEN = pos
                                I.PB.update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"], spells.selected_spell, npc)

                                I.info.CURRENT_ROOM = {"name": new_name, "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": rooms.type}
    return collide

def render_levelup(gifs, screen):
    if gifs["Level up"].start_gif:
        frame = gifs["Level up"].next_frame(1)
        rect = frame.get_rect()
        frame = I.pg.transform.scale(frame, (rect.w * 4, rect.h * 4))
        screen.blit(frame, [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 10 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 10 * 2 + I.info.OFFSCREEN[1]])
        return frame

def handle_render_dropped_items(screen, items, data, rooms):
    items_to_add = []
    with I.info.dropped_items_lock:
        for room in I.IB.dropped_items.keys():
            if room == rooms.name:
                for x, y in I.IB.dropped_items[room].keys():
                    if rooms.size == ['1','1','1','1']:
                        if x - 145 in range(data["Zoom_rect"].x + int(I.info.OFFSCREEN[0] / 4) - 5, data["Zoom_rect"].x + int(I.info.OFFSCREEN[0] / 4) + 10) and y - 80 in range(data["Zoom_rect"].y + int(I.info.OFFSCREEN[1] / 4) - 20, data["Zoom_rect"].y + int(I.info.OFFSCREEN[1] / 4) + 10):
                            items_to_add.append((I.IB.dropped_items[room][(x, y)], x, y))
                    else:
                        me_x = int(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 25 + I.info.OFFSCREEN[0])
                        me_y = int(S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 10 + I.info.OFFSCREEN[1])
                        if x in range(me_x - 30, me_x + 50) and y in range(me_y - 40, me_y + 80):
                            items_to_add.append((I.IB.dropped_items[room][(x, y)], x, y))
                    if I.IB.dropped_items[room].get((x, y)) is not None:
                        for item in I.IB.dropped_items[room][(x, y)]:
                            if rooms.size == ['1','1','1','1']:
                                Ff.add_image_to_screen(screen, items.item_dict[item.split("|")[0]]["path"], (x - data["Zoom_rect"].x, y - data["Zoom_rect"].y, 10, 10))
                            else:
                                Ff.add_image_to_screen(screen, items.item_dict[item.split("|")[0]]["path"], (x, y, 40, 40))

    for item, x, y in items_to_add:
        for i in item:
            I.IB.dropped_items[rooms.name][(x, y)].remove(i)
            del I.IB.dropped_items[rooms.name][(x, y)]
            Ff.add_to_backpack(i, 1, items)
            Ff.display_text_player("Recieved " + str(1) + " " + str(i), 5000)

def handle_dark_rooms_render(sub_image, rooms, decorations):
    lower_beam = 0
    upper_beam = 0
    for decor_name in rooms.decor:
        if "LOCKED:True" in decorations.decor_dict[decor_name]["action"] and "ENTERABLE" not in decorations.decor_dict[decor_name]["action"]:
            """locked door found"""
            for id in decorations.decor_dict[decor_name].keys():
                if not isinstance(id, int):
                    continue
                """locked door possision found"""
                door_rect = decorations.decor_dict[decor_name][id]["rect"]
                if I.info.Closed_door_darkness.get(decor_name) == None:
                    I.info.Closed_door_darkness[decor_name] = {}
                if I.info.Closed_door_darkness[decor_name].get(id) == None:
                    for decoration in decorations.displayed_rects:
                        if decoration[1] < 150:
                            upper_beam = decoration
                        elif decoration[1] + decoration[3] > 620:
                            lower_beam = decoration

                    if door_rect.x > 500:
                        x_offset = 0
                        x_longer = 500
                    else:
                        x_offset = 200
                        if lower_beam != 0:
                            x_longer = lower_beam.x
                            x_offset = door_rect.x
                        else:
                            x_longer = door_rect.w
                    if door_rect.y > 200:
                        y_offset = -door_rect.h
                        y_longer = door_rect.h
                    else:
                        y_offset = door_rect.y
                        y_longer = door_rect.y
                    I.info.Closed_door_darkness[decor_name][id] = [door_rect.x - x_offset, door_rect.y - y_offset, x_longer, y_longer]
                else:
                    x_pos, y_pos, x_longer, y_longer = I.info.Closed_door_darkness[decor_name][id]
                    darkness = I.pg.Surface((x_longer, y_longer), I.pg.SRCALPHA)
                    darkness.fill("black")
                    sub_image[1].blit(darkness, (x_pos, y_pos))

def handle_screen_blits(sub_image, mob_screen, decor_screen, screen, data, case):
    if case == "lower":
        scaled_image = I.pg.transform.scale(sub_image[0], data["Window size"])
        screen.blit(scaled_image, (0, 0))

        scaled_mob_image = I.pg.transform.scale(mob_screen[0], data["Window size"])
        screen.blit(scaled_mob_image, (0, 0))

        I.S.Sub_image1.draw(decor_screen[0])
        scaled_decor_image = I.pg.transform.scale(decor_screen[0], data["Window size"])
        screen.blit(scaled_decor_image, (0, 0))
    elif case == "upper":
        scaled_mob_image = I.pg.transform.scale(mob_screen[1], data["Window size"])
        screen.blit(scaled_mob_image, (0, 0))

        I.S.Sub_image2.draw(decor_screen[1])
        scaled_decor_image = I.pg.transform.scale(decor_screen[1], data["Window size"])
        screen.blit(scaled_decor_image, (0, 0))

        scaled_image = I.pg.transform.scale(sub_image[1], data["Window size"])
        screen.blit(scaled_image, (0, 0))