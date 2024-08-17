import random

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
def Start(mob, decorations, spells, rooms, npc, items):
    data = {}
    data["Player"] = read_txt_file('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt")
    data["Player"] = update_character(data["Player"], spells, npc, items)
    if I.info.CURRENT_ROOM["Mobs"]:
        monster_count = {}
        for key, current_mob in mob.items():
            monster_count[current_mob.name] = current_mob.count

    data["Window size"] = (B_W, B_H)  # Defines the size of the window (The rest is black)
    data["Zoom"] = (B_W / 4, B_H / 4)  # Defines how zoomed in to the picture the view is

    if rooms.type == "Village":
        data["Zoom"] = (B_W / 4, B_H / 4)  # Defines how zoomed in to the picture the view is
        data["Image"] = I.pg.image.load(S.DECOR_PATH[rooms.background]).convert_alpha()  # uploads the background image with transparent convert
    else:
        data["Zoom"] = (B_W / 15, B_H / 15)  # Defines how zoomed in to the picture the view is
        data["Image"] = I.pg.image.load(S.DECOR_PATH[rooms.background]).convert_alpha()  # uploads the background image with transparent convert

    data["Image_rect"] = data["Image"].get_rect()  # Gets the rect of image
    data["Zoom_rect"] = I.pg.Rect(I.info.ENTRY_POS[0], I.info.ENTRY_POS[1], *data["Zoom"])  # creates a rect based on zoomed in picture (basicly makes a window)

    decorate_from_db(rooms, decorations)
    if I.info.CURRENT_ROOM["Mobs"]:
        for key in monster_count:
            data[key] = generate_mobs(mob[key], data["Image_rect"].size)

    # image_data["Church_1"] = place_decor_by_coordinates(200, 280, S.DECOR_PATH["Church_1"], (2, 2), (2, 2))
    return data

def Update(screen, data, mob, gifs, songs, spells, decorations, clock, rooms, npc, items):
    data["Zoom_rect"].x = max(0, min(data["Zoom_rect"].x, data["Image_rect"].width - data["Zoom"][0]))
    data["Zoom_rect"].y = max(0, min(data["Zoom_rect"].y, data["Image_rect"].height - data["Zoom"][1]))
    I.info.Player_rect = I.pg.Rect(150 + I.info.OFFSCREEN[0]/4, 85 + I.info.OFFSCREEN[1]/4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
        sub_image = data["Image"].subsurface(data["Zoom_rect"]).copy()
        collide = handle_decor_visualisation(decorations, sub_image, data, gifs, rooms, screen, clock, spells, npc)
    else:
        sub_image = screen
        door = render_house(screen, data, rooms)
        collide = handle_interior_visualisation(decorations, screen, data, gifs)
        house_border_rect = interior_border_rect(S.SCREEN_WIDTH * 0.1, S.SCREEN_HEIGHT * 0.05, S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.85)
        me = I.pg.Rect(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 25 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 10 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 22, S.SCREEN_HEIGHT / 8)
        # I.T.Make_rect_visible(screen, me, "red")
        handle_stepping_on_rect(me, door, data, screen, clock, spells, "Return", rooms, npc)
        # collide = handle_stepping_on_rect(me, decorations.decor_dict, data, 0, 0, collide, "Conversation", rooms)
        collide = handle_stepping_on_rect(me, house_border_rect, data, 0, 0, collide, "Collide_list", rooms, 0)

    # handle_npc_visualisation(sub_image, data, gifs, rooms)

    if I.info.CURRENT_ROOM["Mobs"]:
        collide = handle_mob_visualisation(collide, sub_image, data, mob, gifs, songs, decorations, items)

    collide = handle_death_visualisation(sub_image, data, gifs, collide)


    cast_spell_handle(sub_image, data, spells, gifs, mob, songs, decorations, items)


    scaled_image = I.pg.transform.scale(sub_image, data["Window size"])
    screen.blit(scaled_image, (0, 0))
    if data["Player"]["dead"] and collide[0] == "mob":  # dont hit mobs when u dead
        collide = False, 0, 0, 0
    return collide


def handle_stepping_on_rect(me, rect, data, screen, clock, extra, action, rooms, npc):
    if "Return" in action:
        spells = extra
        if me.colliderect(rect):
            # I.info.ENTRY_POS = [510, 370]
            I.info.CURRENT_ROOM = {"name": "Village_1", "Spells": True, "Backpack": True, "Running": True, "Mobs": True, "Type": "Village"}
            update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"], spells.selected_spell, npc)
            rooms.select_room("Village_1")
            Play.Start(screen, clock, rooms)
    if "Collide_list" in action:
        if me.collidelistall(rect):
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
    #                         print("hi")
    #                         return extra
    #     return extra
        # if rect


def handle_mob_visualisation(collide, sub_image, data, mob_dict, gifs, song, decorations, items):
    for mob in mob_dict.values():
        for current_mob in mob.mobs:
            mob_gif = current_mob["gif_frame"][0]
            mob_rect = current_mob["rect"][mob_gif]
            mob_x = mob_rect.x - data["Zoom_rect"].x
            mob_y = mob_rect.y - data["Zoom_rect"].y
            rect = I.pg.Rect(mob_x, mob_y, mob_rect.w, mob_rect.h)
            if mob_y - mob_rect.h / 2 <= 79:
                update_health(rect, current_mob, sub_image[0])
                if current_mob["flip"]:
                    image = I.pg.transform.flip(current_mob["image"][mob_gif], True, False)
                else:
                    image = current_mob["image"][mob_gif]
                sub_image[0].blit(image, (mob_x, mob_y))

                handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items)

                handle_damage_type_visualisation(sub_image[0], current_mob, gifs, (mob_x, mob_y), data, mob, decorations, items)
            if mob_y + mob_rect.h / 2 >= 84:
                update_health(rect, current_mob, sub_image[1])
                if current_mob["flip"]:
                    image = I.pg.transform.flip(current_mob["image"][mob_gif], True, False)
                else:
                    image = current_mob["image"][mob_gif]
                sub_image[1].blit(image, (mob_x, mob_y))

                handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items)

                handle_damage_type_visualisation(sub_image[1], current_mob, gifs, (mob_x, mob_y), data, mob, decorations,items)
            if I.info.Player_rect.colliderect(rect):
                collide = ('mob', current_mob, mob_rect.x, mob_rect.y)
            if I.info.Player_rect.colliderect(rect) and current_mob["allignment"] in [6, 8, 9]:
                collide = ('mob_collide', current_mob, mob_rect.x, mob_rect.y)
                data["Player"]["Last_hit"] = I.pg.time.get_ticks()
                data["Player"]["hp"] = data["Player"]["hp"][0] - current_mob["damage"][0], data["Player"]["hp"][1]

            handle_mob_speed(data, current_mob, decorations, mob)
    return collide
def handle_mob_speed(data, current_mob, decorations, mob):

    # me = I.pg.Rect(150, 85, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
    speed = current_mob["speed"][0]
    current_frame = current_mob["gif_frame"][0]
    frame_count = current_mob["gif_frame"][1]
    if current_frame % 2 == 0:
        target_pos = (I.info.Player_rect.x + data["Zoom_rect"].x, I.info.Player_rect.y + data["Zoom_rect"].y)
        mob_rect = current_mob["rect"][current_frame]
        if not data["Player"]["dead"] and current_mob["allignment"] in [6, 8]:
            mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_towards(target_pos, current_mob, speed, decorations.displayed_rects, data["Zoom_rect"])
            mob.update_position(mob_rect.x, mob_rect.y, current_mob)
            if current_mob["allignment"] == 8:
                current_mob["allignment"] = 4

            #Update the orientation of mob running towards me
            if mob_rect.x > target_pos[0]:
                current_mob["flip"] = True
            else:
                current_mob["flip"] = False

        elif not data["Player"]["dead"] and current_mob["allignment"] == 4 and current_mob["hp"][0] < current_mob["hp"][1]:
            mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_away_from(target_pos, current_mob, speed, decorations.displayed_rects, data["Zoom_rect"])
            mob.update_position(mob_rect.x, mob_rect.y, current_mob)

            #Update the orientation of mob running away from me
            if mob_rect.x > target_pos[0]:
                current_mob["flip"] = False
            else:
                current_mob["flip"] = True

        else:
            current_mob["visible"] = False

def handle_damage_type_visualisation(sub_image, current_mob, gifs, pos, data, mob, decorations, items):
    for key in gifs.keys():
        if gifs[key].start_gif and current_mob == gifs[key].rect:
            if current_mob["effect"].get(key) != None:
                duration = current_mob["effect"][key]
                frame = gifs[key].next_frame(duration)
                if current_mob["effect"]["Fire"] != 0:
                    gifs["Cold"].start_gif = False
                    gifs["Cold"].repeat = 0
                    mob.deal_damage(current_mob, data["Player"], "effect_" + key, items, gifs)
                if current_mob["effect"]["Cold"] != 0:
                    gifs["Fire"].start_gif = False
                    gifs["Fire"].repeat = 0
                    current_mob["speed"] = (0, current_mob["speed"][1])
            else:
                frame = gifs[key].next_frame(1)  # made specifically for damage displaying on mobs displays piercing, blunt
            sub_image.blit(frame, (pos[0], pos[1]))
            # sub_image.blit(frame, (pos[0], pos[1]))

        elif not gifs[key].start_gif and current_mob["effect"].get(key) != None: # IF KEY IS NOT STARTED ITS GIF AND CURRENT MOB HAS THIS EFFECT ON IT
            if not gifs[key].start_gif and current_mob["effect"][key] != 0:
                current_mob["effect"][key] = 0
                if key == "Cold":
                    current_mob["speed"] = (current_mob["speed"][1], current_mob["speed"][1])

        elif hasattr(gifs[key], 'rect') and isinstance(gifs[key].rect, int):  # DISPLAYS EFFECTS ON DECOR
            data_to_remove = []
            for index, effect in decorations.effected_decor.items():
                # index = gifs[key].rect
                if effect == "Fire":
                    duration = -1
                else:
                    duration = 1
                    if index not in data_to_remove:
                        data_to_remove.append(index)

                frame = gifs[effect].next_frame(duration)
                sub_image.blit(frame, (decorations.displayed_rects[index].x, decorations.displayed_rects[index].y))

            if data_to_remove != [] and not gifs[effect].start_gif: # REMOVES BURNED DECOR
                for index in data_to_remove:
                    del decorations.effected_decor[index]


# def handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items):
#     if I.info.COMBAT_RECT[0] != 0:
#         if I.info.COMBAT_RECT[0].colliderect(rect) and current_mob["damage_type"] == "":
#             curr_song = song["Playing"]
#             effect = song[curr_song].generate_thump_sound()
#             song[curr_song].play_effect(effect)
#             if I.info.EQUIPED["Sword"] != 0:
#                 current_mob["damage_type"] = "Piercing" # MAKE ADAPTABLE TO ITEM BEING HELD
#             else:
#                 current_mob["damage_type"] = "Blunt"
#             # gifs["Blunt"].Start_gif("Blunt", current_mob)
#             mob.deal_damage(current_mob, data["Player"], "", items)
#             I.info.COMBAT_RECT = 0, I.info.COMBAT_RECT[1]

def handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items):
    if I.info.COMBAT_RECT[0] != 0:
        damage_type = "Blunt"
        if I.info.EQUIPED["Sword"] != 0:
            weapon_data = Ff.get_property(I.info.EQUIPED["Sword"], items, "WEAPON")
            damage_type = weapon_data[3]
        if I.info.COMBAT_RECT[0] != 0 and I.info.COMBAT_RECT[0].colliderect(rect) and not gifs[damage_type].start_gif:
            curr_song = song["Playing"]
            effect = song[curr_song].generate_thump_sound()
            song[curr_song].play_effect(effect)
            gifs[damage_type].Start_gif(damage_type, current_mob)
            mob.deal_damage(current_mob, data["Player"], "", items, gifs)
            I.info.COMBAT_RECT = 0, 0

def handle_death_visualisation(sub_image, data, gifs, collide):
    if data["Player"]["dead"]:
        me = I.pg.Rect(150, 85, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
        dead_disc = {"Portal": display_gif_on_subimage(sub_image, (S.SCREEN_WIDTH / 16, S.SCREEN_HEIGHT / 10), (I.info.SPAWN_POINT[0] * 1.8 - data["Zoom_rect"].x , I.info.SPAWN_POINT[1] + 10 * 16 - data["Zoom_rect"].y), gifs["Portal"]),
                     "Sign": display_on_subimage(sub_image, (S.SCREEN_WIDTH / 90, S.SCREEN_HEIGHT / 40), S.PLAYING_PATH["Sign"],(I.info.SPAWN_POINT[0] * 1.6 - data["Zoom_rect"].x, I.info.SPAWN_POINT[1] + 10 * 10 - data["Zoom_rect"].y)),
                     "Grave": display_on_subimage(sub_image, (S.SCREEN_WIDTH / 60, S.SCREEN_HEIGHT / 30), S.PLAYING_PATH["Grave"], (data["Player"]["dead"].x - data["Zoom_rect"].x + me.x, data["Player"]["dead"].y - data["Zoom_rect"].y + me.y)),
                     }
        dead_list = list(dead_disc.values())
        if I.info.Player_rect.collidelistall(dead_list):
            keys = list(dead_disc.keys())
            key = keys[I.info.Player_rect.collidelistall(dead_list)[0]]
            collide = (key, dead_disc[key].x, dead_disc[key].y)
    return collide
# def handle_npc_visualisation(sub_image, data, gifs, rooms):
#     if rooms.type == "Village":
#         npc = {"Luna": display_gif_on_subimage(sub_image, (17,18), (330 * 1.6 - data["Zoom_rect"].x , 1 + 10 * 43 - data["Zoom_rect"].y), gifs["Luna"]),
#                "Bear": display_gif_on_subimage(sub_image, (17,18), (330 * 1.7 - data["Zoom_rect"].x , 1 + 10 * 43 - data["Zoom_rect"].y), gifs["Bear"])}
    # elif rooms.type == "House":
def handle_interior_visualisation(decorations, sub_image, data, gifs):
    me = I.pg.Rect(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 24 + I.info.OFFSCREEN[0],S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 16 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 24, S.SCREEN_HEIGHT / 12)
    # I.T.Make_rect_visible(sub_image, me, "blue")
    collide = [False]
    decorations.displayed_rects = []
    decor_options = list(decorations.decor_dict.keys())
    for option in decor_options:
        for id in decorations.decor_dict[option].keys():
            if isinstance(id, str):
                continue

            decor = decorations.decor_dict[option][id]

            # Gets x, y position of decoration
            rect = I.pg.Rect(decor["rect"].x, decor["rect"].y, decor["rect"].w, decor["rect"].h)
            image_rect = decor["image"].get_rect()
            # handle display
            if I.info.APPLIANCE_CLICK == "":
                if option in list(gifs.keys()) and option != "Furnace":
                    display_gif_on_subimage(sub_image, (image_rect.w, image_rect.h), (rect.x, rect.y), gifs[option])
                else:
                    sub_image.blit(decor["image"], (rect.x, rect.y))

            elif I.info.APPLIANCE_CLICK == "Furnace":
                if option in list(gifs.keys()):
                    display_gif_on_subimage(sub_image, (image_rect.w, image_rect.h), (rect.x, rect.y), gifs[option])
                else:
                    sub_image.blit(decor["image"], (rect.x, rect.y))

            # I.T.Make_rect_visible(sub_image, rect, "white")
            # handle colision
            if me.colliderect(rect):
                if option == "Furnace":
                    collide = ("Appliance-Furnace", rect.x, rect.y)
                elif decorations.decor_dict[option]["action"] == "NPC":
                    # print("created npc conversation!!")
                    collide = (option, rect.x, rect.y)
                else:
                    collide = (option, rect.x, rect.y)
    return collide
def handle_decor_visualisation(decorations, sub_image, data, gifs, rooms, screen, clock, spells, npc):
    collide = [False]
    decorations.displayed_rects = []  # List to keep track of displayed rectangles
    decor_options = list(decorations.decor_dict.keys())
    # decorations_to_remove = []
    for option in decor_options:
        for id in decorations.decor_dict[option].keys():
            if isinstance(id, str):
                continue
            # print(option, id, decorations.decor_dict[option][id])
            decor = decorations.decor_dict[option][id]
            # Gets x, y position of decoration
            decor_x = decor["rect"].x - data["Zoom_rect"].x
            decor_y = decor["rect"].y - data["Zoom_rect"].y

            rect = I.pg.Rect(decor_x, decor_y, decor["rect"].w, decor["rect"].h)


            # if (data["Image"].get_at((decor["rect"].x, decor["rect"].y)) == (137, 176, 46, 255) and data["Image"].get_at((decor["rect"].x + decor["rect"].w, decor["rect"].y + decor["rect"].h)) == (137, 176, 46, 255)):
            if option in list(gifs.keys()):
                if "door" not in option:
                    display_gif_on_subimage(sub_image, (rect.w, rect.h), (rect.x, rect.y), gifs[option])
                elif I.info.DOOR_CLICK != (90, "") and I.info.DOOR_CLICK[0] < gifs[I.info.DOOR_CLICK[1]].frame_count:
                    if I.pg.time.get_ticks() - gifs[I.info.DOOR_CLICK[1]].frame_time > gifs[I.info.DOOR_CLICK[1]].delay:
                        I.info.DOOR_CLICK = I.info.DOOR_CLICK[0] + 1, I.info.DOOR_CLICK[1]
                    display_gif_on_subimage(sub_image, (rect.w, rect.h), (rect.x, rect.y), gifs[I.info.DOOR_CLICK[1]])
                    if I.info.DOOR_CLICK[0] == gifs[I.info.DOOR_CLICK[1]].frame_count:
                        building = I.info.DOOR_CLICK[1].split("_")[0]
                        I.info.DOOR_CLICK = 90, "" # RESET I.info.DOOR_CLICK
                        # print(building)
                        I.info.CURRENT_ROOM = {"name": building, "Spells": True, "Backpack": True, "Running": True, "Mobs": False, "Type": "House"}
                        rooms.select_room(building)
                        update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"], spells.selected_spell, npc)
                        I.info.ENTRY_POS = (1, 1)
                        I.info.OFFSCREEN = (25, 250)
                        Play.Start(screen, clock, rooms)
            else:
                decor["image"] = I.pg.transform.scale(decor["image"], (rect.w, rect.h))
                sub_image.blit(decor["image"], (decor_x, decor_y))
            decorations.displayed_rects.append(rect)  # Add to the list of displayed rectangles
            # if option in I.info.ENTERABLE:
                # door_rect = (I.pg.Rect(rect.left + rect.w * 0.6, rect.top + rect.h * 0.60, rect.w / 4, rect.h / 2), option)
                # I.T.Make_rect_visible(sub_image, door_rect[0], "red")
                # if I.info.Player_rect.colliderect(rect):
                #     Collide = ("Door,," + option, rect.x, rect.y)
            rect = I.pg.Rect(rect.x, rect.y + rect.h / 2, rect.w, rect.h - rect.h / 2)
            # I.T.Make_rect_visible(sub_image, rect, "green")
            if I.info.Player_rect.colliderect(rect):
                collide = (option, decor["rect"].x, decor["rect"].y)

    # if decorations_to_remove != []:
    #     for option, id in decorations_to_remove:
    #         del decorations.decor_dict[option][id]
    return collide
def display_char(dx, dy, screen, gifs, data):
    character_path = 'static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER
    dxdy = (dx, dy)
    # I.info.OFFSCREEN = I.info.OFFSCREEN[0] + dx, I.info.OFFSCREEN[1] + dy
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
        if I.info.COMBAT_RECT[0] != 0:
            if dx == 0 and dy == 0:
                for key, value in orientation.items():
                    if value == I.info.LAST_ORIENT[0].split(".")[0]:
                        dx = key[0]
                        dy = key[1]
                        break
                character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + dx * 5 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + dy * 5 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]
            else:
                character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + dx * 10 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + dy * 10 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]
        else:
            character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]

        orient = orientation[dxdy]
        if orient in orientation_images:
            images = orientation_images[orient]
            if I.info.CURRENT_STANCE == 0 or I.info.CURRENT_STANCE == 2:
                Ff.add_image_to_screen(screen, character_path + images[0], character_center_pos)
            elif I.info.CURRENT_STANCE == 1:
                Ff.add_image_to_screen(screen, character_path + images[1], character_center_pos)
            else:
                Ff.add_image_to_screen(screen, character_path + images[2], character_center_pos)
            I.info.LAST_ORIENT = orientation_images[orient]
        else:
            Ff.add_image_to_screen(screen, character_path + I.info.LAST_ORIENT[0], character_center_pos)

def generate_decor(num_of_items, background_size, path):
    items = {}
    for i in range(num_of_items):
        x = random.randint(0, background_size[0]-100)
        y = random.randint(0, background_size[1]-100)
        image = I.pg.image.load(path).convert_alpha()
        rect = image.get_rect(topleft=(x, y))
        items[i] = {"image": image, "rect": rect}
    return items
def generate_mobs(mob, background_size):
    path = S.MOB_PATH[mob.name][0]
    mob_gif_count = S.MOB_PATH[mob.name][1]
    mob.spawn_mobs(background_size, path, mob_gif_count)
    return mob.mobs

def add_to_backpack(item, amount, items):
    if amount != 0:
        # print(amount)
        in_backpack = 0
        stack = Ff.get_property(item, items, "STACK")
        for item_name in I.info.BACKPACK_CONTENT.keys():
            if item + "|STACK" in item_name:
                in_backpack = 1
                if I.info.BACKPACK_CONTENT[item_name][0] < stack:  # IF THE STACK HAS EMPTY SPACES CONTINUE
                    in_backpack = 2
                    if amount + I.info.BACKPACK_CONTENT[item_name][0] <= stack:  # IF THE AMOUNT OF NEW ITEMS PLUS THE ALREADY EXISTING ITEMS DOESNT OVERFLOW THE STACK
                        # print("stack wasnt overflowed")
                        I.info.BACKPACK_CONTENT[item_name] = I.info.BACKPACK_CONTENT[item_name][0] + amount, I.info.BACKPACK_CONTENT[item_name][1], I.info.BACKPACK_CONTENT[item_name][2]
                        break
                    else:  # IF THE AMOUNT OF NEW ITEMS PLUS THE ALREADY EXISTING ITEMS OVERFLOWS THE STACK CREATE A NEW ONE
                        while True:
                            new_addon = "|STACK" + str(int(item_name.split("|STACK")[1]) + 1)
                            new_name = item_name.split("|")[0] + new_addon
                            if I.info.BACKPACK_CONTENT.get(new_name) == None and int(amount + I.info.BACKPACK_CONTENT[item_name][0] - stack) != 0:
                                break
                            else:
                                item_name = new_name
                        row, collumn = find_open_space()
                        if int(amount + I.info.BACKPACK_CONTENT[item_name][0] - stack) != 0:
                            I.info.BACKPACK_CONTENT[new_name] = int(amount + I.info.BACKPACK_CONTENT[item_name][0] - stack), row, collumn  # FIRST CREATED NEW STACK CUZ THE OLD STACK VALUE WAS USED
                            # print("stack overflowed creating new stack: ", I.info.BACKPACK_CONTENT[new_name])
                        I.info.BACKPACK_CONTENT[item_name] = int(stack), I.info.BACKPACK_CONTENT[item_name][1], I.info.BACKPACK_CONTENT[item_name][2]  # THEN UPDATED OLD STACK
                        break
                # else:
                    # print("this stack is full")

        if in_backpack == 1:
            # print("all stacks were full creating new stack")
            for item_name in I.info.BACKPACK_CONTENT.keys():
                if item + "|STACK" in item_name:
                    continue
            new_name = item_name.split("|STACK")[0] + "|STACK" + str(int(item_name.split("|STACK")[1]) + 1)
            row, collumn = find_open_space()
            I.info.BACKPACK_CONTENT[new_name] = int(amount), row, collumn  # FIRST CREATED NEW STACK CUZ THE OLD STACK VALUE WAS USED

        if in_backpack == 0:
            # print("didn't find empty stacks \n")
            row, collumn = find_open_space()


            if I.info.BACKPACK_CONTENT.get(item) == None:                 # if the item doesnt exist in backpack
                I.info.BACKPACK_CONTENT[item] = (float(amount), row, collumn)
                # DOESNT DO STACKS
            else:                                                         # if the item already exists in backpack and there were no previous |STACK
                # DOESNT REMOVE THE ITEM WITHOUT |STACK ON IT, ADDS TOO MANY ITEMS
                stack = Ff.get_property(item, items, "STACK")
                value = I.info.BACKPACK_CONTENT[item]
                if value[0] + float(amount) > stack:
                    del I.info.BACKPACK_CONTENT[item]
                    repetitions = I.math.floor((float(value[0]) + float(amount)) / float(stack)) + 1  # adding one so loop works with one stack (if stack is 10 and amount is 14, then for loop needs to happen twice, this function returns one less)
                    addon = "|STACK"
                    for i in range(0, repetitions):
                        if i == repetitions-1:
                            stack = float(value[0]) + float(amount) - float(stack) * i
                        posx, posy = find_open_space()
                        if int(stack) != 0:
                            I.info.BACKPACK_CONTENT[item + addon + str(i)] = (int(stack), int(posx), int(posy))
                else:
                    I.info.BACKPACK_CONTENT[item] = (float(value[0] + float(amount)), value[1], value[2])

    # print("input: ", I.info.BACKPACK_CONTENT)

    # merge_stacks(items)

def remove_from_backpack(item, amount):
    if amount != 0:
        if I.info.BACKPACK_CONTENT[item][0] - amount > 0:
            I.info.BACKPACK_CONTENT[item] = I.info.BACKPACK_CONTENT[item][0] - amount, I.info.BACKPACK_CONTENT[item][1], I.info.BACKPACK_CONTENT[item][2]
        else:
            del I.info.BACKPACK_CONTENT[item]
    else:
        print("amount not a normal number")

def update_equiped():
    if I.info.BACKPACK_CONTENT == {}:
        for option in I.info.EQUIPED.keys():
            I.info.EQUIPED[option] = 0
    else:
        if I.info.Temp_variable_holder != []:
            if I.info.Temp_variable_holder[2] in ["cook", "burn"]:
                for key in I.info.EQUIPED.keys():
                    if I.info.EQUIPED[key] == I.info.Temp_variable_holder[0]:
                        if I.info.BACKPACK_CONTENT.get(I.info.Temp_variable_holder[0]) == None:
                            I.info.EQUIPED[key] = 0
        else:
            for item, (amount, posx, posy) in I.info.BACKPACK_CONTENT.items():
                if posx < 0:
                    I.info.EQUIPED[I.info.equipment[(posx, posy)]] = item


def BackPack(screen, items, player):
    pressed = 0 # key authentication
    running = True # loop var
    block = (0, 0) # backpack block
    border = 1 # rect border size
    use = 0 # place holder for items to be eaten/used
    selected = 0 # place holder for rect of selected block
    color = "Yellow" # color of selected rect
    pickup = (0, 0, 0) # place holder for the name, posx, posy of selected block
    fill_backpack(screen, player, items)
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    coordinates = get_equipment_coordinates(block)
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_b:
                    pressed = I.pg.K_b
                elif event.key == I.pg.K_ESCAPE:
                    pressed = I.pg.K_ESCAPE
                elif event.key == I.pg.K_x:
                    pressed = I.pg.K_x
                    color = "Green"
                    for key, value in I.info.BACKPACK_CONTENT.items():
                        if value[1] == block[0] and value[2] == block[1]:
                            # if the possision matches get the key
                            use = key
                elif event.key == I.pg.K_c:
                    pressed = I.pg.K_c
                    if selected == 0:
                        if block[0] >= 0:
                            selected = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
                        else:
                            selected = I.pg.Rect(coordinates[block][0], coordinates[block][1], item_w, item_h)
                            I.info.EQUIPED[I.info.equipment[block]] = 0
                        pickup = (find_item_by_slot(block[0], block[1]), block[0], block[1])

                    else:
                        if pickup[0] != 0 and pickup[0] != None:
                            update_equipment_var(block, pickup[0])
                            value = I.info.BACKPACK_CONTENT[pickup[0]]
                            taken_spaces = list(I.info.BACKPACK_CONTENT.values())
                            if not any((block[0], block[1]) == (tpl[1], tpl[2]) for tpl in taken_spaces):
                                I.info.BACKPACK_CONTENT[pickup[0]] = (value[0], block[0], block[1]) # set the new possision value
                            else:
                                # switching two item places
                                existing_item = find_item_by_slot(block[0], block[1]) # get existing item name
                                if "STACK" in existing_item and "STACK" in pickup[0]:
                                    # BOTH OF THESE ITEMS ARE STACKS
                                    stack = Ff.get_property(existing_item.split("|")[0], items, "STACK")
                                    if float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0]][0]) <= stack:
                                        # MERGING TWO STACKS INTO ONE
                                        sum = float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0]][0])
                                        I.info.BACKPACK_CONTENT[existing_item] = sum, I.info.BACKPACK_CONTENT[existing_item][1], I.info.BACKPACK_CONTENT[existing_item][2]
                                        del I.info.BACKPACK_CONTENT[pickup[0]]

                                    elif float(I.info.BACKPACK_CONTENT[existing_item][0]) < stack and float(I.info.BACKPACK_CONTENT[pickup[0]][0]) < stack:
                                        # MERGING VALUES OF STACKS WITH REMAINDER
                                        remainder = float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0]][0]) - stack
                                        I.info.BACKPACK_CONTENT[pickup[0]] = remainder, I.info.BACKPACK_CONTENT[pickup[0]][1], I.info.BACKPACK_CONTENT[pickup[0]][2]
                                        I.info.BACKPACK_CONTENT[existing_item] = stack, I.info.BACKPACK_CONTENT[existing_item][1], I.info.BACKPACK_CONTENT[existing_item][2]

                                else:
                                    I.info.BACKPACK_CONTENT[existing_item] = I.info.BACKPACK_CONTENT[existing_item][0], pickup[1], pickup[2]
                                    I.info.BACKPACK_CONTENT[pickup[0]] = I.info.BACKPACK_CONTENT[pickup[0]][0], block[0], block[1]


                                update_equipment_var((pickup[1], pickup[2]), existing_item)
                                # if block[0] < 0:
                                #     I.info.EQUIPED[I.info.equipment[(pickup[1], pickup[2])]] = existing_item
                        pickup = (0, 0, 0)
                        selected = 0
                elif event.key == I.pg.K_UP:
                    block = (block[0], block[1] - 2)
                    if block[1] < 0:
                        block = (block[0], 26)
                elif event.key == I.pg.K_DOWN:
                    block = (block[0], block[1] + 2)
                    if block[1] > 26:
                        block = (block[0], 0)
                elif event.key == I.pg.K_LEFT:
                    block = (block[0] - 2, block[1])
                elif event.key == I.pg.K_RIGHT:
                    block = (block[0] + 2, block[1])
                    if block[0] > 14:
                        block = (0, block[1])
            elif event.type == I.pg.KEYUP:
                if pressed == I.pg.K_b or pressed == I.pg.K_ESCAPE:
                    running = False  # exits backpack view
                elif pressed == I.pg.K_x:
                    color = "Yellow"
                    if "|" in str(use):
                        if use != 0 and "CONSUMABLE" in items.item_dict[use.split("|")[0]]["Properties"]:
                            handle_consumption(items, player, use)
                            use = 0
                    else:
                        if use != 0 and "CONSUMABLE" in items.item_dict[use]["Properties"]:
                            handle_consumption(items, player, use)
                            use = 0
                    pressed = 0
                    selected = 0

            fill_backpack(screen, player, items)
            if block[0] < 0:
                if block[0] < -10:
                    block = -10, block[1]
                if block[1] > 8:
                    block = block[0], 8
                coordinates = get_equipment_coordinates(block)
                if block[0] < -2 and block[0] >= -6 and block[1] != 8:
                    block = -10, block[1]
                if block[0] <= -6 and block[0] > -10 and block[1] != 8:
                    block = -2, block[1]
                rect = I.pg.Rect(coordinates[block][0], coordinates[block][1], item_w, item_h)
            else:
                rect = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
            I.pg.draw.rect(screen, color, rect, border)
            if selected != 0:
                I.pg.draw.rect(screen, "Yellow", selected, 2)

            I.pg.display.flip()

def get_equipment_coordinates(block):
    coordinates = {
        (-2, 0): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.12),
        (-2, 2): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.17),
        (-2, 4): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.21),
        (-2, 6): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.24),
        (-2, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-4, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.82,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-6, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.74,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-8, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.66,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-10, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-10, 6): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.24),
        (-10, 4): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.21),
        (-10, 2): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.17),
        (-10, 0): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.12),
    }
    return coordinates
def handle_consumption(items, player, use):
    if "|" in use:
        property_list = items.item_dict[use.split("|")[0]]["Properties"].split(",,,")
    else:
        property_list = items.item_dict[use]["Properties"].split(",,,")

    for property in property_list:
        if "CONSUMABLE" in property:
            consumable = property[11:-1] # from CONSUMABLE(valuesss) gets only the values inside
    # print(consumable)
    consumable = consumable.split(",,")
    for consume in consumable:
        points, atribute = consume.split("-")
        if player[atribute][0] < player[atribute][1]:
            if "/" in points:
                points = points[1:]
                player[atribute] = (player[atribute][0] - int(points), player[atribute][1])
            else:
                player[atribute] = (player[atribute][0] + int(points), player[atribute][1])
        elif player[atribute][0] >= player[atribute][1]:
            if "/" in points:
                points = points[1:]
                player[atribute] = (player[atribute][0] - int(points), player[atribute][1])
            else:
                player[atribute] = (player[atribute][1], player[atribute][1])
    value = I.info.BACKPACK_CONTENT[use]
    if value[0] > 1:
        I.info.BACKPACK_CONTENT[use] = (value[0] - 1, value[1], value[2])
    else:
        del I.info.BACKPACK_CONTENT[use]
def display_on_subimage(sub_image, size, path, pos):
    image = I.pg.image.load(path).convert_alpha()
    image = I.pg.transform.scale(image, (size[0], size[1]))
    sub_image.blit(image, pos)
    return I.pg.Rect(pos[0], pos[1], size[0], size[1])

def get_backpack_coordinates(screen):
    rect = screen.get_rect()
    bag = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Backpack_Empty"],[rect.center[0] * 0.5, rect.center[1] * 0.25, S.SCREEN_WIDTH / 2,S.SCREEN_HEIGHT * 0.75])
    if I.info.BACKPACK_COORDINATES_X == {}:
        I.info.BACKPACK_COORDINATES_X, I.info.BACKPACK_COORDINATES_Y = bag_coordinates(screen, bag)

def fill_backpack(screen, player, items):
    I.info.BACKPACK_CONTENT["Gold"] = (player["Gold"],I.info.BACKPACK_CONTENT["Gold"][1], I.info.BACKPACK_CONTENT["Gold"][2])
    rect = screen.get_rect()
    bag = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Backpack_Empty"], [rect.center[0] * 0.5 ,rect.center[1] * 0.25, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT * 0.75])
    get_backpack_coordinates(screen)
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    for content in I.info.BACKPACK_CONTENT.keys():
        row = I.info.BACKPACK_CONTENT[content][1]
        collumn = I.info.BACKPACK_CONTENT[content][2]
        if row < 0:
            coordinates = get_equipment_coordinates((row,collumn))
            # HANDLE MULTIPLE STACKS
            if "|" in content:
                Ff.add_image_to_screen(screen, items.item_dict[content.split("|")[0]]["path"], [coordinates[row, collumn][0], coordinates[row, collumn][1], item_w, item_h])
            else:
                # handle one stack
                Ff.add_image_to_screen(screen, items.item_dict[content]["path"], [coordinates[row, collumn][0], coordinates[row, collumn][1], item_w, item_h])
            Ff.display_text(screen, str(I.info.BACKPACK_CONTENT[content][0]), 2, [coordinates[row, collumn][0], coordinates[row, collumn]][1], "white")
        else:
            # HANDLE MULTIPLE STACKS
            if "|" in content:
                Ff.add_image_to_screen(screen, items.item_dict[content.split("|")[0]]["path"],[list(I.info.BACKPACK_COORDINATES_X.values())[row],list(I.info.BACKPACK_COORDINATES_Y.values())[collumn], item_w, item_h])
            else:
                # handle one stack
                Ff.add_image_to_screen(screen, items.item_dict[content]["path"], [list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn], item_w, item_h])

            if content == "Gold":
                Ff.display_text(screen, str(I.info.BACKPACK_CONTENT[content][0]), 2, [list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn]], "white")
            else:
                Ff.display_text(screen, str(int(I.info.BACKPACK_CONTENT[content][0])), 2, [list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn]], "white")

    I.pg.draw.rect(screen, "black", (bag.w * 0.604, bag.h * 0.807, bag.w * 0.115, bag.h * 0.012))
    remainder = player["hp"][0] / player["hp"][1]
    I.pg.draw.rect(screen, "red", (bag.w * 0.604, bag.h * 0.807, bag.w * 0.115 * remainder, bag.h * 0.012))
    Ff.display_text(screen, "Hp", 1, (bag.w * 0.562, bag.h * 0.80), "black")

    I.pg.draw.rect(screen, "black", (bag.w * 0.808, bag.h * 0.807, bag.w * 0.148, bag.h * 0.012))
    remainder = player["mana"][0] / player["mana"][1]
    I.pg.draw.rect(screen, "blue", (bag.w * 0.808, bag.h * 0.807, bag.w * 0.148 * remainder, bag.h * 0.012))
    Ff.display_text(screen, "Mp", 1, (bag.w * 0.752, bag.h * 0.80), "black")

    I.pg.draw.rect(screen, "black", (bag.w * 0.604, bag.h * 0.857, bag.w * 0.115, bag.h * 0.012))
    remainder = player["Exhaustion"][0] / player["Exhaustion"][1]
    I.pg.draw.rect(screen, "Green", (bag.w * 0.604, bag.h * 0.857, bag.w * 0.115 * remainder, bag.h * 0.012))
    Ff.display_text(screen, "Exh", 1, (bag.w * 0.55, bag.h * 0.85), "black")

    Ff.add_image_to_screen(screen,
                           'static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + "Front.png",
                           [rect.center[0] * 0.64 ,rect.center[1] * 0.4, S.SCREEN_WIDTH / 8, S.SCREEN_HEIGHT / 4])


    I.pg.draw.rect(screen, "black", (bag.w * 0.626, bag.h * 0.71, bag.w * 0.3, bag.h * 0.025))
    remainder = player["Experience"] / exp_till_lvup(player)
    I.pg.draw.rect(screen, "light green", (bag.w * 0.626, bag.h * 0.707, bag.w * 0.3 * remainder, bag.h * 0.025))
    Ff.display_text(screen, "Exp", 1, (bag.w * 0.58, bag.h * 0.71), "black")


    return bag
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

def bag_coordinates(screen, bag):
    stop = False
    start = 0
    coordinates_x = {}
    coordinates_y = {}

    # Gets start coordinates
    for top in range(bag.top, bag.top + bag.h):
        if stop:
            break
        for left in range(bag.left, bag.left + bag.w):
            color = screen.get_at((left, top))
            if color == S.DEFAULT["Backpack_Empty"]:
                start = (left, top)
                stop = True
                break
    left = start[0]
    top = start[1]
    cube = 1

    #  Gets coordinates of X
    color = screen.get_at((start[0], start[1]))
    if color == S.DEFAULT["Backpack_Empty"]:
        kill = False
        while not kill:
            color1 = color
            coordinates_x[cube] = left
            cube += 1
            while color1 == S.DEFAULT["Backpack_Empty"]:
                coordinates_x[cube] = left
                left += 1
                color1 = screen.get_at((left, top))
                # screen.set_at((left, top), (0,0,0,255))
            if color1 == (204, 130, 98, 255):
                cube += 1
                while color1 == (204, 130, 98, 255):
                    left += 1
                    color1 = screen.get_at((left, top))
                if color1 == (156, 90, 60, 255):
                    kill = True

    #  Gets coordinates of Y
    left = start[0]
    top = start[1]
    cube = 1
    color = screen.get_at((start[0], start[1]))
    if color == S.DEFAULT["Backpack_Empty"]:
        kill = False
        while not kill:
            color1 = color
            coordinates_y[cube] = top
            cube += 1
            while color1 == S.DEFAULT["Backpack_Empty"]:
                coordinates_y[cube] = top
                top += 1
                color1 = screen.get_at((left, top))
            if color1 == (204, 130, 98, 255):
                cube += 1
                while color1 == (204, 130, 98, 255):
                    top += 1
                    color1 = screen.get_at((left, top))
                if color1 == (156, 90, 60, 255):
                    kill = True

    return (coordinates_x, coordinates_y)


def place_decor_by_coordinates(x, y, path, scale, rect_scale):
    items = {}
    image = I.pg.image.load(path).convert_alpha()
    rect = image.get_rect(topleft=(x, y))
    image = I.pg.transform.scale(image, (rect.w * scale[0], rect.h * scale[1]))
    rect.w = rect.w * rect_scale[0]
    rect.h = rect.h * rect_scale[1]
    items[0] = {"image": image, "rect": rect}
    return items

def update_health(rect, current_mob, sub_image):
    if current_mob["hp"][0] < current_mob["hp"][1]:
        health_bar = I.pg.Rect(rect.x, rect.y, rect.w, 1)
        I.pg.draw.rect(sub_image, "red", health_bar)
        health = current_mob["hp"]
        remainder = health[0] / health[1]
        reduced_health_bar = I.pg.Rect(rect.x, rect.y, rect.w * remainder, 1)
        I.pg.draw.rect(sub_image, "green", reduced_health_bar)

def update_character(player_disc, spells, npc, items):
    spell_str = player_disc["Spells"]
    spell_list = spell_str.split(",,")
    for slot_spell in spell_list:
        if slot_spell != '' and slot_spell != "Empty":
            slot, spell = slot_spell.split("__")
            spells.selected_spell[int(slot)] = spell
    I.info.BACKPACK_CONTENT = {}
    backpack_str = player_disc["Backpack"]
    backpack_str_list = backpack_str.split(",,")
    for backpack_data in backpack_str_list:
        if backpack_data != {} and backpack_data != "Empty" and backpack_data != '':
            item, amount, posx, posy = backpack_data.split("__")
            add_to_backpack(item, amount, items)  # adds items from txt

    hp_by_race = {"Elf": 11,
                  "Human": 10}

    mana_by_race = {"Elf": 14,
                    "Human": 10}

    race = player_disc["Race"]
    level = player_disc["Level"]
    player_disc["hp"] = (player_disc["Health"], hp_by_race[race] * level)
    player_disc["mana"] = (player_disc["Mana"], mana_by_race[race] * level)

    player_disc["dead"] = False

    player_disc["Exhaustion"] = (player_disc["Exhaustion"], 100)

    player_disc["Last_hit"] = I.pg.time.get_ticks()  # required to know when to start regenerating hp and mana

    quest_tuple = player_disc["Quests"].split(",,")
    if quest_tuple != ['', '']:
        quest_tuple = quest_tuple[0].split("__")
        I.info.QUESTS = quest_tuple
        check_quest_completion()
    dialog_id = player_disc["Dialog"].split(",,")
    for value in dialog_id:
        if value != "":
            key, id = value.split("__")
            npc[key]["dialog"].iteration = int(id)


    return player_disc

def spell_book(screen, data, spells, gifs):
    fill_spellbook(screen, gifs)
    item_w = list(I.info.SPELLBOOK_COORDINATES_X.values())[1] - list(I.info.SPELLBOOK_COORDINATES_X.values())[0]
    item_h = list(I.info.SPELLBOOK_COORDINATES_Y.values())[1] - list(I.info.SPELLBOOK_COORDINATES_Y.values())[0]
    block = (0,0)
    color = "yellow"
    border = 1
    pressed = 0
    running = True
    selected = 0
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_UP:
                    block = (block[0], block[1] - 2)
                    if block[1] < 0:
                        block = (block[0], 16)
                elif event.key == I.pg.K_ESCAPE:
                    pressed = I.pg.K_ESCAPE
                elif event.key == I.pg.K_DOWN:
                    block = (block[0], block[1] + 2)
                    if block[1] > 16:
                        block = (block[0], 0)
                elif event.key == I.pg.K_LEFT:
                    block = (block[0] - 2, block[1])
                    if block[0] < 0 and selected == 0:
                        block = (28, block[1])
                elif event.key == I.pg.K_RIGHT:
                    block = (block[0] + 2, block[1])
                    if block[0] > 28:
                        block = (0, block[1])
                elif event.key == I.pg.K_v:
                    pressed = I.pg.K_v
            if event.type == I.pg.KEYUP:
                if pressed == I.pg.K_v or pressed == I.pg.K_ESCAPE:
                    running = False
                if event.key == I.pg.K_c:
                    if selected == 0:
                        for spell, (row, collum) in I.info.SPELLBOOK_CONTENT.items():
                            if block == (row, collum):
                                selected = spell
                    else:
                        spells.selected_spell[block[0]] = selected
                        selected = 0
                pressed = 0
        fill_spellbook(screen, gifs)
        if selected != 0:
            if block[0] > 8:
                block = (8, block[1])
            if block[0] < 0:
                block = (0, block[1])
            rect = I.pg.Rect(list(I.info.SPELLBOOK_COORDINATES_X.values())[block[0]], list(I.info.SPELLBOOK_COORDINATES_Y.values())[11] + list(I.info.SPELLBOOK_COORDINATES_Y.values())[0], item_w, item_h)
        else:
            rect = I.pg.Rect(list(I.info.SPELLBOOK_COORDINATES_X.values())[block[0]],list(I.info.SPELLBOOK_COORDINATES_Y.values())[block[1]], item_w, item_h)
        I.pg.draw.rect(screen, color, rect, border)

        if spells.selected_spell != {}:
            for pos, spell in spells.selected_spell.items():
                rect = I.pg.Rect(list(I.info.SPELLBOOK_COORDINATES_X.values())[int(pos)],list(I.info.SPELLBOOK_COORDINATES_Y.values())[11] +list(I.info.SPELLBOOK_COORDINATES_Y.values())[0], item_w, item_h)
                Ff.add_image_to_screen(screen, gifs[spell].frame_paths[0], rect)


        I.pg.display.flip()

def fill_spellbook(screen, gifs):
    rect = screen.get_rect()
    book = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Spellbook_Empty"], [rect.center[0] * 0.5, rect.center[1] * 0.25, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT * 0.75])

    if I.info.SPELLBOOK_COORDINATES_X == {}:
        I.info.SPELLBOOK_COORDINATES_X, I.info.SPELLBOOK_COORDINATES_Y = bag_coordinates(screen, book)

    item_w = list(I.info.SPELLBOOK_COORDINATES_X.values())[1] - list(I.info.SPELLBOOK_COORDINATES_X.values())[0]
    item_h = list(I.info.SPELLBOOK_COORDINATES_Y.values())[1] - list(I.info.SPELLBOOK_COORDINATES_Y.values())[0]
    for content in I.info.SPELLBOOK_CONTENT.keys():
        row, collumn = I.info.SPELLBOOK_CONTENT[content]
        Ff.add_image_to_screen(screen, gifs[content].frame_paths[0], [list(I.info.SPELLBOOK_COORDINATES_X.values())[row], list(I.info.SPELLBOOK_COORDINATES_Y.values())[collumn], item_w, item_h])
def display_gif_on_subimage(sub_image, size, pos, gif):
    frame = gif.next_frame(-1)
    frame = I.pg.transform.scale(frame, (size[0], size[1]))
    sub_image.blit(frame, pos)
    return I.pg.Rect(pos[0], pos[1], size[0], size[1])

def cast_spell_handle(sub_image, data, spells, gifs, mob, song, decorations, items):
    if not data["Player"]["dead"]:
        curr_song = song["Playing"]
        sound_type = {"Force": song[curr_song].generate_magic_sound(),
                      "Fire": song[curr_song].generate_fire_sound(),
                      "Cold": song[curr_song].generate_cold_sound()}
        for slot, spell in spells.selected_spell.items():
            if gifs[spell].start_gif:
                spells.spell_cooloff[spell] = spells.spell_dict[spell]["recharge"]
                frame = gifs[spell].next_frame(1)
                if I.info.CURRENT_ROOM["Type"] in ["Village"]:
                    size = (20, 20)
                else:
                    size = (80, 80)
                frame = I.pg.transform.scale(frame, size)

                if spells.direction[spell] == 0:
                    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
                        spells.init_cast[spell] = data["Zoom_rect"].copy()
                        spells.direction[spell] = I.info.LAST_ORIENT[0].split(".")[0]
                    else:
                        spells.init_cast[spell] = I.pg.Rect(S.SCREEN_WIDTH / 2 + S.SCREEN_WIDTH / 20 - I.info.Player_rect.w * 10 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - I.info.Player_rect.h * 10 + I.info.OFFSCREEN[1], size[0], size[1])
                        spells.direction[spell] = I.info.LAST_ORIENT[0].split(".")[0]
                direction_settings = {
                    "Front": {"rect": (145, 80), "dir": (0, -1), "rotate": 90, "flip": (False, True)},
                    "Back": {"rect": (145, 70), "dir": (0, 1), "rotate": 90, "flip": (False, False)},
                    "Left": {"rect": (140, 75), "dir": (1, 0), "rotate": 0, "flip": (True, False)},
                    "Right": {"rect": (150, 75), "dir": (-1, 0), "rotate": 0, "flip": (False, False)},
                }
                spell_direction = spells.direction[spell]
                settings = direction_settings.get(spell_direction)
                # me = I.pg.Rect(settings["rect"][0], settings["rect"][1], S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)
                dir = settings["dir"]
                frame = I.pg.transform.rotate(frame, settings["rotate"])
                frame = I.pg.transform.flip(frame, *settings["flip"])

                if gifs[spell].current_frame != 0:
                    if I.info.CURRENT_ROOM["Type"] == "Village":
                        rect = I.pg.Rect(spells.init_cast[spell].x - data["Zoom_rect"].x + I.info.Player_rect.x - dir[0] * gifs[spell].current_frame * 6, spells.init_cast[spell].y - data["Zoom_rect"].y + I.info.Player_rect.y - dir[1] * gifs[spell].current_frame * 6, size[0], size[1])
                    else:
                        rect = I.pg.Rect(spells.init_cast[spell].x - dir[0] * gifs[spell].current_frame * 12*2, spells.init_cast[spell].y - dir[1] * gifs[spell].current_frame * 12*2, size[0], size[1])
                    sub_image.blit(frame, rect)
                    if I.info.CURRENT_ROOM["Type"] == "Village":
                        if rect.collidelist(decorations.displayed_rects) != -1: # if hits any decor
                            type = spells.spell_dict[spell]["type"]
                            song[curr_song].play_effect(sound_type[type])
                            gifs[spell].start_gif = False
                            index = rect.collidelist(decorations.displayed_rects)
                            decorations.effected_decor[index] = type
                        else:
                            for key in mob.keys():
                                for current_mob in mob[key].mobs:
                                    mob_rect = I.pg.Rect(current_mob["rect"][0].x - data["Zoom_rect"].x,
                                                         current_mob["rect"][0].y - data["Zoom_rect"].y,
                                                         current_mob["rect"][0].w, current_mob["rect"][0].h)
                                    if rect.colliderect(mob_rect):
                                        mob[key].deal_damage(current_mob, data["Player"], spells.spell_dict[spell], items, gifs)
                                        gifs[spell].start_gif = False  # IF COMMENTED OUT, MAKES A SPELL GO THROUGH MULTIPLE ENEMIES
                                        type = spells.spell_dict[spell]["type"]
                                        gifs[type].Start_gif(type, current_mob)
                                        song[curr_song].play_effect(sound_type[type])
            else:
                # RESET DIRECTION OF FIRE
                spells.direction[spell] = 0
                spells.init_cast[spell] = 0
def init_dialog(name, player, screen, npc, items):
    dialog_obj = npc[name]["dialog"]
    dialog_obj.name = name
    check_quest_completion()
    handdle_sign_display(screen, dialog_obj, player, items)
    # dialog.id[dialog.type] = 1
    handle_dialog_outcome(dialog_obj, player, screen, items)

    dialog_obj.conv_key = "Start"

def handle_dialog_outcome(dialog, player, screen, items):
    if dialog.data != (None, None, None, None):
        if "quest" in dialog.data[0]:
            if "questfail" in dialog.data[0]:
                I.info.QUESTS = 0
                dialog.iteration = 0
                dialog.data = (None, None, None, None)
            elif "questcomplete" in dialog.data[0]:
                # print("completed quest, gained reward: ", dialog.data[1], dialog.data[2], " for getting", dialog.data[3], dialog.data[4])
                if dialog.data[2] == "Silver":
                    player["Gold"] += float(dialog.data[1])/10
                remove_from_backpack(dialog.data[4], int(dialog.data[3]))
                dialog.iteration = 3
                dialog.data = (None, None, None, None)
            else:
                # print(dialog.data)
                # print("you have to ", dialog.data[2], " ", dialog.data[3], " ", dialog.data[4] + " For " + dialog.data[1])
                I.info.QUESTS = dialog.data
                check_quest_completion()
                dialog.data = (None, None, None, None)
        elif "shop" in dialog.data[0]:
            handle_shop(dialog.data[1], player, screen, items)
        # elif "questCompleted_" in dialog.data[0]:
        #     remove_from_backpack(I.info.COMPLETED_QUESTS[3], int(I.info.COMPLETED_QUESTS[2]))
        #     I.info.QUESTS = 0
        #     dialog.id[dialog.type] = 4
        #     print("you have", dialog.data[1] + "d", dialog.data[2], dialog.data[3])
        #     if dialog.data[3] == "Gold":
        #         player["Gold"] += float(dialog.data[2]) # Adds gold to backpack that was recieved from the quest
        #     else:
        #         add_to_backpack(dialog.data[3], int(dialog.data[2])) # Adds item to backpack that was recieved from the quest
        #
        #     Ff.display_text_player("Received " + dialog.data[2] + " " + dialog.data[3], 5000)
        #     Ff.display_text_player("Removed " + I.info.COMPLETED_QUESTS[2] + " " + I.info.COMPLETED_QUESTS[3], 10000)
        #     I.info.COMPLETED_QUESTS = 0
        #     dialog.data = (None, None, None, None)

        elif dialog.data[0] == "item":
            if dialog.data[1] == "buy":
                # print("Buying ", dialog.data[3], "for ", dialog.data[2])
                player["Gold"] = float(player["Gold"]) - float(dialog.data[2])
                add_to_backpack(dialog.data[3], 1, items)  # Adds bought items through conversation
                Ff.display_text_player("Received 1 " + dialog.data[3], 5000)
                Ff.display_text_player("Removed " + str(dialog.data[2]) + " Gold", 5000)
                dialog.data = (None, None, None, None)
            if dialog.data[1] == "get":
                # print("got ", dialog.data[3], "for free")
                dialog.data = (None, None, None, None)
            # dialog.id[dialog.type] += 1 # Switches to next conversation
def handdle_sign_display(screen, dialog, player, items):
    # print(dialog.type, dialog.data, dialog.conv_key)

    text = dialog.get_text()
    response = dialog.select_response()
    running = True
    if "{" in text:
        # print("action text: ", text, "responses: ", response)
        if "COST" in text[text.index("{")+1:text.index("}")]:
            word, item = text[text.index("{") + 1:text.index("}")].split("|")
            cost = items.item_dict[item]["Cost"]
            text = text.replace(text[text.index("{"):text.index("}")+1], str(cost))
        elif response[1] != '':
            # handles other actions

            dialog.data = response[1].split("|")
            response = response[0], ""
            if dialog.data[0] == "random":
                rand_addon = str(random.randint(0, 1))
                # dialog.conv_key += "-" + rand_addon
                dialog.conv_key = dialog.conv_key.split("|")[0] + "-" + rand_addon
                dialog.data = (None, None, None, None)
                handdle_sign_display(screen, dialog, player, items)
                running = False
                # text = dialog.get_text()
                # response = dialog.select_response()
            elif len(dialog.data) > 2 and dialog.data[2] == "Cost":
                cost = items.item_dict[dialog.data[3]]["Cost"] / 10 # conversion from SILVER to GOLD
                dialog.data = dialog.data[0], dialog.data[1], cost, dialog.data[3]
            if len(dialog.data) > 2 and dialog.data[0:2] == ('item', 'buy') and float(dialog.data[2]) > float(player["Gold"]):
                dialog.conv_key = "Funds"
                dialog.data = (None, None, None, None)
                text = dialog.get_text()
                response = dialog.select_response()





    Ff.add_image_to_screen(screen, S.PLAYING_PATH["Text_bar"], (0, S.SCREEN_HEIGHT / 2, S.SCREEN_WIDTH, S.SCREEN_HEIGHT / 2))
    a = 0
    collumn = 100
    row = 100
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN and event.key == I.pg.K_x:
                if a > len(text):
                    running = False
                    dialog.conv_key = response[1]
                    dialog.friendlyness += int(response[1].split("|")[1])
            if event.type == I.pg.KEYDOWN and event.key == I.pg.K_c:
                if a > len(text):
                    running = False
                    dialog.conv_key = response[0]
                    dialog.friendlyness += int(response[0].split("|")[1])
            if event.type == I.pg.KEYDOWN and event.key == I.pg.K_z:
                for i in range(20):
                    if a + i >= len(text):
                        break
                    else:
                        if text[a + i] == "\n":
                            a += i
                            break
                else:
                     a += 20

        if not a > len(text) and text[a-1] == "\n":
            collumn += 20
            row = 100
            text = text[a+1:]
            a = 0
        Ff.display_text(screen, text[0:a], 10, (row, S.SCREEN_HEIGHT / 2 + collumn),  "black")

        if not a > len(text):
            I.pg.time.wait(10)
            a += 1

        # Handle resppmse
        if response[1] != "":
            Ff.display_text(screen, response[0].split("|")[0] + " [C]", 14, (80, S.SCREEN_HEIGHT / 2 + 280), "red")
            Ff.display_text(screen, response[1].split("|")[0] + " [X]", 14, (700, S.SCREEN_HEIGHT / 2 + 280), "red")
        else:
            Ff.display_text(screen, response[0].split("|")[0] + " [C]", 14,  (80, S.SCREEN_HEIGHT / 2 + 280), "red")

        I.pg.display.flip()

    if not running:
        if not dialog.has_conversation_ended():
            handdle_sign_display(screen, dialog, player, items)

def display_border(border_image_name, decorations, data):
    path = decorations.decor_dict[border_image_name]["path"]
    image = I.pg.image.load(path).convert_alpha()
    rect = image.get_rect()
    tree_amount = 0
    row = 0
    while True:
        # building on the x axis (virsus ir apacia)
        # virsui pirma juosta
        # apacioj pirma
        # virsui antra
        # apacioj antra
        tree_image1, tree_rect1 = decorations.place_decor_by_coordinates(row, 0, path, (0.8, 0.8), (1, 0.3))
        tree_image2, tree_rect2 = decorations.place_decor_by_coordinates(row, data["Image_rect"].h - (rect.h * 0.8), path, (0.8, 0.8), (1, 0.5))

        tree_image3, tree_rect3 = decorations.place_decor_by_coordinates(row + rect.w/4, rect.h * 0.3, path, (0.8, 0.8), (0.8, 0.8))
        tree_image4, tree_rect4 = decorations.place_decor_by_coordinates(row + rect.w/4, data["Image_rect"].h - (rect.h * 1.3), path, (0.8, 0.8), (0.8, 0.5))
        if data["Image_rect"].w <= tree_rect3.x + tree_rect3.w:
            break
        decorations.decor_dict[border_image_name][tree_amount] = {"name": border_image_name, "id": tree_amount, "image": tree_image1, "rect": tree_rect1, "effect": ""}
        tree_amount += 1
        decorations.decor_dict[border_image_name][tree_amount] = {"name": border_image_name, "id": tree_amount, "image": tree_image2, "rect": tree_rect2, "effect": ""}
        tree_amount += 1

        decorations.decor_dict[border_image_name][tree_amount] = {"name": border_image_name, "id": tree_amount, "image": tree_image3, "rect": tree_rect3, "effect": ""}
        tree_amount += 1
        decorations.decor_dict[border_image_name][tree_amount] = {"name": border_image_name, "id": tree_amount, "image": tree_image4, "rect": tree_rect4, "effect": ""}
        tree_amount += 1

        row += rect.w * 0.5

    column = rect.h * 0.5
    while True:
        # building on the y axis (kaire ir desine)
        # kairei pirma juosta
        # desinei pirma
        # kairei antra
        # desinei antra

        tree_image1, tree_rect1 = decorations.place_decor_by_coordinates(0, column, path, (0.8, 0.8), (0.4, 0.5))
        tree_image2, tree_rect2 = decorations.place_decor_by_coordinates(data["Image_rect"].w - rect.w, column, path, (0.8, 0.8), (0.8, 0.7))

        tree_image3, tree_rect3 = decorations.place_decor_by_coordinates(rect.w * 0.4, column + rect.h/4, path, (0.8, 0.8), (0.8, 0.7))
        tree_image4, tree_rect4 = decorations.place_decor_by_coordinates(data["Image_rect"].w - (rect.w * 1.3), column + rect.h/4, path, (0.8, 0.8), (0.3, 0.7))
        if data["Image_rect"].h <= (tree_rect3.y + tree_rect3.h):
            break

        decorations.decor_dict[border_image_name][tree_amount] = {"image": tree_image1, "rect": tree_rect1}
        tree_amount += 1
        decorations.decor_dict[border_image_name][tree_amount] = {"image": tree_image2, "rect": tree_rect2}
        tree_amount += 1

        decorations.decor_dict[border_image_name][tree_amount] = {"image": tree_image3, "rect": tree_rect3}
        tree_amount += 1
        decorations.decor_dict[border_image_name][tree_amount] = {"image": tree_image4, "rect": tree_rect4}
        tree_amount += 1

        column += rect.w * 0.5

def render_house(screen, data, rooms):
    screen.fill("black")
    tile_pos = (S.SCREEN_WIDTH * 0.1, S.SCREEN_HEIGHT * 0.1, S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.8)
    Ff.add_image_to_screen(screen, S.DECOR_PATH[rooms.background], tile_pos)
    door_rect = I.pg.Rect(S.SCREEN_WIDTH * 0.45, S.SCREEN_HEIGHT * 0.875, S.SCREEN_WIDTH * 0.11, S.SCREEN_HEIGHT * 0.025)
    I.T.Make_rect_visible(screen, door_rect, (45, 19, 4, 255))
    return door_rect

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
                dialog_str += npc_name + "__" + str(npc[npc_name]["dialog"].iteration) + ",,"
            lines[i] = f'Dialog: {dialog_str}\n'
        elif line.startswith('Quests:'):
            if I.info.QUESTS != 0 and I.info.QUESTS != [""]:
                quest_str = I.info.QUESTS[0] + "__" + I.info.QUESTS[1] + "__" + I.info.QUESTS[2] + "__" + I.info.QUESTS[3] + "__" + I.info.QUESTS[4] + ",,"
            else:
                quest_str = ',,'
            lines[i] = f'Quests: {quest_str}\n'

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

def find_open_space():
    taken_spaces = list(I.info.BACKPACK_CONTENT.values())
    for column in range(0, 26, 2):
        for row in range(0, 16, 2):
            if any((row, column) == (tpl[1], tpl[2]) for tpl in taken_spaces):
                continue
            return row, column

def find_item_by_slot(x, y):
    for key, value in I.info.BACKPACK_CONTENT.items():
        if value[1] == x and value[2] == y:
            # if the possision matches get the key
            return key

def update_equipment_var(key, value):
    if key[0] < 0:
        I.info.EQUIPED[I.info.equipment[key]] = value

def interior_border_rect(left, top, width, height):
    right = left + width
    bottom = top + height
    top_rect = I.pg.Rect(left, top, right - left, 5) # top
    right_rect = I.pg.Rect(right,top, 5, bottom - top) # right
    left_rect = I.pg.Rect(left, top, 5, bottom - top) # left
    bottom_rect = I.pg.Rect(left, bottom, right - left, 5) # bottom
    return [top_rect, right_rect, left_rect, bottom_rect]

def decorate_from_db(rooms, decorations):
    for decor_name in rooms.decor:
        path = decorations.decor_dict[decor_name]["path"]
        if decor_name == "Furnace":
            path += "out.png"
        elif path[-1] == "_":
            path += "0.png"
        for i in range(0, len(rooms.data[decor_name])):
            image, rect = decorations.place_decor_by_coordinates(rooms.data[decor_name][i]["x"], rooms.data[decor_name][i]["y"], path, (rooms.data[decor_name][i]["img_x"], rooms.data[decor_name][i]["img_y"]), (rooms.data[decor_name][i]["rect_x"], rooms.data[decor_name][i]["rect_y"]))
            decorations.decor_dict[decor_name][i] = {"name": decor_name, "id": i, "image": image, "rect": rect, "effect": ""}

def quest_render(screen, items):
    running = True
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    key_auth = 0
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key in [I.pg.K_ESCAPE, I.pg.K_n]:
                    key_auth = event.key
            if event.type == I.pg.KEYUP:
                if event.key == key_auth and event.key in [I.pg.K_ESCAPE, I.pg.K_n]:
                    running = False
        Ff.add_image_to_screen(screen, S.PLAYING_PATH["Quest_Empty"], [S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 5, S.SCREEN_WIDTH / 3, S.SCREEN_HEIGHT / 1.5])
        if I.info.QUESTS != 0 and I.info.QUESTS != [""]:
            Ff.display_text(screen, I.info.QUESTS[2] + " " + I.info.QUESTS[3], 20, (S.SCREEN_WIDTH / 3 + S.SCREEN_WIDTH / 20 * 0.5, S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 1.1), "Black")
            Ff.add_image_to_screen(screen, items.item_dict[I.info.QUESTS[4]]["path"], [S.SCREEN_WIDTH / 3 + S.SCREEN_WIDTH / 20 * 2, S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 1.1, item_w, item_h])
            remainder = check_quest_completion()
            I.pg.draw.rect(screen, "black", (S.SCREEN_WIDTH / 3 + S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 2.2, item_w * 5, item_h * 0.3))
            I.pg.draw.rect(screen, "green", (S.SCREEN_WIDTH / 3 + S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 2.2, item_w * 5 * remainder, item_h * 0.3))
        I.pg.display.flip()

def check_quest_completion():
    remainder = 0
    print(I.info.QUESTS)
    if I.info.QUESTS != 0 and I.info.QUESTS != [""] and  I.info.QUESTS[2] == "Get":
        if I.info.BACKPACK_CONTENT.get(I.info.QUESTS[4]) == None:
            amount = 0
        else:
            amount, x, y = I.info.BACKPACK_CONTENT[I.info.QUESTS[4]]
        remainder = float(amount) / float(I.info.QUESTS[3])
    if remainder >= 1:
        I.info.COMPLETED_QUESTS = I.info.QUESTS
        remainder = 1
    return remainder

def handle_shop(case, player, screen, items):
    if case == "Armory":
        fill_shop(screen, case, items)
        item_w = list(I.info.SHOP_COORDINATES_X.values())[1] - list(I.info.SHOP_COORDINATES_X.values())[0]
        item_h = list(I.info.SHOP_COORDINATES_Y.values())[1] - list(I.info.SHOP_COORDINATES_Y.values())[0]
        block = (0, 0)
        color = "yellow"
        border = 1
        pressed = 0
        display_text = []
        running = True
        selected = 0
        while running:
            for event in I.pg.event.get():
                if event.type == I.pg.KEYDOWN:
                    if event.key == I.pg.K_c:
                        pressed = I.pg.K_c
                    elif event.key == I.pg.K_UP:
                        if selected == 0:
                            block = (block[0], block[1] - 2)
                            if block[1] < 0:
                                block = (block[0], 16)
                    elif event.key == I.pg.K_ESCAPE:
                        pressed = I.pg.K_ESCAPE
                    elif event.key == I.pg.K_DOWN:
                        if selected == 0:
                            block = (block[0], block[1] + 2)
                            if block[1] > 16:
                                block = (block[0], 0)
                    elif event.key == I.pg.K_LEFT:
                        if selected == 0:
                            block = (block[0] - 2, block[1])
                            if block[0] < 0 and selected == 0:
                                block = (28, block[1])
                        else:
                            block = (block[0] - 10, block[1])
                            if block[0] < 0 and selected != 0:
                                block = (20, block[1])
                    elif event.key == I.pg.K_RIGHT:
                        if selected == 0:
                            block = (block[0] + 2, block[1])
                            if block[0] > 28:
                                block = (0, block[1])
                        else:
                            block = (block[0] + 10, block[1])
                            if block[0] > 28:
                                block = (0, block[1])
                if event.type == I.pg.KEYUP:
                    if pressed == I.pg.K_ESCAPE:
                        running = False
                    if event.key == I.pg.K_c and pressed == I.pg.K_c:
                        if selected == 0:
                            for item, (row, collum) in I.info.SHOP_CONTENT.items():
                                if block == (row, collum):
                                    selected = item
                                    border = 2
                                    display_text = [items.item_dict[selected]["describtion"], 10, [390, 500]]

                        else:
                            if block[0] == 0:
                                if items.item_dict[selected]["Cost"] > player["Gold"]:
                                    display_text = ["Not enough Gold", 40, [420, 520]]
                                    # Ff.display_text(screen, "Not enough Gold", 40, [300, 500], "black")
                                else:
                                    display_text = ["Bought", 40, [420, 520]]
                                    add_to_backpack(selected, 1, items)  # Adds bought item through shop
                                    player["Gold"] -= items.item_dict[selected]["Cost"]
                                    selected = 0
                            elif block[0] == 10:
                                display_text = ["Not implemented", 40, [420, 520]]
                            elif block[0] == 20:
                                display_text = ["Exit", 40, [420, 520]]
                                running = False
                    if event.key == I.pg.K_x:
                        selected = 0
                        display_text = []
                        border = 1
                    pressed = 0
            if selected != 0:
                if block[0] < 10:
                    block = 0, block[1]
                elif block[0] < 20:
                    block = 10, block[1]
                elif block[0] < 28:
                    block = 20, block[1]
                rect = I.pg.Rect(list(I.info.SHOP_COORDINATES_X.values())[block[0]],list(I.info.SHOP_COORDINATES_Y.values())[16] + item_h * 1.8, item_w * 6, item_h)
            else:
                rect = I.pg.Rect(list(I.info.SHOP_COORDINATES_X.values())[block[0]],list(I.info.SHOP_COORDINATES_Y.values())[block[1]], item_w, item_h)

            fill_shop(screen, case, items)

            if display_text != []:
                if "\\n" in display_text[0]:
                    lines = display_text[0].split("\\n")
                    for i in range(len(lines)):
                        Ff.display_text(screen, lines[i], display_text[1], (display_text[2][0], display_text[2][1] + i * 20), "black")
                else:
                    Ff.display_text(screen, display_text[0], display_text[1], display_text[2], "black")
            I.pg.draw.rect(screen, color, rect, border)


            I.pg.display.flip()

def fill_shop(screen, type, items):
    rect = screen.get_rect()
    shop = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Shop_Empty"], [rect.center[0] * 0.5, rect.center[1] * 0.25, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT * 0.75])
    Ff.display_text(screen, "Buy", 16, (420, 442), "black")
    Ff.display_text(screen, "Sell", 16, (610, 442), "black")
    Ff.display_text(screen, "Exit", 16, (780, 442), "black")

    if I.info.SHOP_COORDINATES_X == {}:
        I.info.SHOP_COORDINATES_X, I.info.SHOP_COORDINATES_Y = bag_coordinates(screen, shop)

    item_w = list(I.info.SHOP_COORDINATES_X.values())[1] - list(I.info.SHOP_COORDINATES_X.values())[0]
    item_h = list(I.info.SHOP_COORDINATES_Y.values())[1] - list(I.info.SHOP_COORDINATES_Y.values())[0]

    row = 0
    collumn = 0
    if I.info.SHOP_CONTENT == {}:
        for item in items.item_dict.keys():
            if "WEAPON" in items.item_dict[item]["Properties"]:
                I.info.SHOP_CONTENT[item] = row, collumn
                row += 2
                if row == 28:
                    collumn += 2
                    row = 0

    for content in I.info.SHOP_CONTENT.keys():
        row, collumn = I.info.SHOP_CONTENT[content]
        Ff.add_image_to_screen(screen, items.item_dict[content]["path"], [list(I.info.SHOP_COORDINATES_X.values())[row], list(I.info.SHOP_COORDINATES_Y.values())[collumn], item_w, item_h])


def display_lower_upper_decor(option, gifs, new_subimage, rect, rooms, clock, screen, decor, decorations, decor_x, decor_y, data, spells, npc):
    if option in list(gifs.keys()):
        if "door" not in option:
            display_gif_on_subimage(new_subimage, (rect.w, rect.h), (rect.x, rect.y), gifs[option])
        elif I.info.DOOR_CLICK != (90, "") and I.info.DOOR_CLICK[0] < gifs[I.info.DOOR_CLICK[1]].frame_count:
            if I.pg.time.get_ticks() - gifs[I.info.DOOR_CLICK[1]].frame_time > gifs[I.info.DOOR_CLICK[1]].delay:
                I.info.DOOR_CLICK = I.info.DOOR_CLICK[0] + 1, I.info.DOOR_CLICK[1]
            display_gif_on_subimage(new_subimage, (rect.w, rect.h), (rect.x, rect.y), gifs[I.info.DOOR_CLICK[1]])
            if I.info.DOOR_CLICK[0] == gifs[I.info.DOOR_CLICK[1]].frame_count:
                building = I.info.DOOR_CLICK[1].split("_")[0]
                I.info.DOOR_CLICK = 90, ""  # RESET I.info.DOOR_CLICK
                # print(building)
                I.info.CURRENT_ROOM = {"name": building, "Spells": True, "Backpack": True, "Running": True, "Mobs": False, "Type": "House"}
                rooms.select_room(building)
                update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"], spells.selected_spell, npc)
                I.info.ENTRY_POS = (1, 1)
                I.info.OFFSCREEN = (25, 250)
                Play.Start(screen, clock, rooms)
    else:
        decor["image"] = I.pg.transform.scale(decor["image"], (rect.w, rect.h))
        new_subimage.blit(decor["image"], (decor_x, decor_y))
    decorations.displayed_rects.append(rect)  # Add to the list of displayed rectangles

def New_Update(data, decorations, gifs, rooms, clock, screen, spells, npc, mob, songs, items):
    data["Zoom_rect"].x = max(0, min(data["Zoom_rect"].x, data["Image_rect"].width - data["Zoom"][0]))
    data["Zoom_rect"].y = max(0, min(data["Zoom_rect"].y, data["Image_rect"].height - data["Zoom"][1]))
    I.info.Player_rect = I.pg.Rect(150 + I.info.OFFSCREEN[0] / 4, 85 + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
        sub_image = data["Image"].subsurface(data["Zoom_rect"]).copy()
        new_subimage = I.pg.Surface([data["Zoom_rect"][2], data["Zoom_rect"][3]], I.pg.SRCALPHA, 32).convert_alpha()
        sub_image = (sub_image, new_subimage)
        collide = [False]
        decorations.displayed_rects = []  # List to keep track of displayed rectangles

        decor_options = decorations.decor_dict.keys()

        for option in decor_options:
            for id in decorations.decor_dict[option].keys():
                if isinstance(id, str):
                    continue

                decor = decorations.decor_dict[option][id]
                # Gets x, y position of decoration
                decor_x = decor["rect"].x - data["Zoom_rect"].x
                decor_y = decor["rect"].y - data["Zoom_rect"].y

                rect = I.pg.Rect(decor_x, decor_y, decor["rect"].w, decor["rect"].h)

                # Check and process decorations in the upper part of the screen
                if decor_y - rect.h / 2 <= 79:
                    display_lower_upper_decor(option, gifs, sub_image[0], rect, rooms, clock, screen, decor, decorations, decor_x, decor_y, data, spells, npc)
                    adjusted_rect = I.pg.Rect(rect.x, rect.y + rect.h / 2, rect.w, rect.h - rect.h / 2)
                    if decorations.decor_dict[option]["type"] == "House":
                        adjusted_rect = I.pg.Rect(rect.x, rect.y + rect.h / 2, rect.w, rect.h - rect.h / 2 - 1)
                    I.T.Make_rect_visible(sub_image[0], adjusted_rect, "green")
                    if I.info.Player_rect.colliderect(adjusted_rect):
                        collide = (option, decor["rect"].x, decor["rect"].y)

                # Check and process decorations in the lower part of the screen
                if decor_y + rect.h / 2 >= 84:
                    display_lower_upper_decor(option, gifs, sub_image[1], rect, rooms, clock, screen, decor, decorations, decor_x, decor_y, data, spells, npc)
                    adjusted_rect = I.pg.Rect(rect.x, rect.y + rect.h / 2, rect.w, rect.h - rect.h / 2)
                    I.T.Make_rect_visible(sub_image[1], adjusted_rect, "blue")
                    if I.info.Player_rect.colliderect(adjusted_rect):
                        collide = (option, decor["rect"].x, decor["rect"].y)

    else:
        sub_image = (screen, 0)
        door = render_house(sub_image[0], data, rooms)
        collide = handle_interior_visualisation(decorations, sub_image[0], data, gifs)
        house_border_rect = interior_border_rect(S.SCREEN_WIDTH * 0.1, S.SCREEN_HEIGHT * 0.05, S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.85)
        me = I.pg.Rect(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 25 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 10 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 22, S.SCREEN_HEIGHT / 8)
        # I.T.Make_rect_visible(screen, me, "red")
        handle_stepping_on_rect(me, door, data, sub_image[0], clock, spells, "Return", rooms, npc)
        # collide = handle_stepping_on_rect(me, decorations.decor_dict, data, 0, 0, collide, "Conversation", rooms)
        collide = handle_stepping_on_rect(me, house_border_rect, data, 0, 0, collide, "Collide_list", rooms, 0)

    if I.info.CURRENT_ROOM["Mobs"]:
        collide = handle_mob_visualisation(collide, sub_image, data, mob, gifs, songs, decorations, items)

    collide = handle_death_visualisation(sub_image[0], data, gifs, collide)

    cast_spell_handle(sub_image[0], data, spells, gifs, mob, songs, decorations, items)

    scaled_image = I.pg.transform.scale(sub_image[0], data["Window size"])
    screen.blit(scaled_image, (0, 0))

    dx, dy = Play.keypress_handle(screen, data, songs, items, spells, gifs)

    Play.walking(dx, dy, collide, data)

    display_char(dx, dy, screen, gifs, data)

    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
        scaled_image = I.pg.transform.scale(sub_image[1], data["Window size"])
        screen.blit(scaled_image, (0, 0))

    if data["Player"]["dead"] and collide[0] == "mob":  # dont hit mobs when u dead
        collide = False, 0, 0, 0

    return collide