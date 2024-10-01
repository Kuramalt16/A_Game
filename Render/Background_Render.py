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
    txt_data = read_txt_file('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt")
    data["Player"] = update_character(txt_data, spells, npc, items)
    if I.info.CURRENT_ROOM["Mobs"]:
        monster_count = {}
        for key, current_mob in mob.items():
            monster_count[current_mob.name] = current_mob.count

    data["Window size"] = (B_W, B_H)  # Defines the size of the window (The rest is black)
    data["Zoom"] = (B_W / 4, B_H / 4)  # Defines how zoomed in to the picture the view is
    if rooms.type == "Village":
        values = rooms.name.split("_")
        data["Zoom"] = (B_W / 4, B_H / 4)  # Defines how zoomed in to the picture the view is
        data["Image"] = I.pg.image.load(S.DECOR_PATH[rooms.background + "_" + values[1] + "_" + values[2]]).convert_alpha()  # uploads the background image with transparent convert
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

# def Update(screen, data, mob, gifs, songs, spells, decorations, clock, rooms, npc, items):
#     data["Zoom_rect"].x = max(0, min(data["Zoom_rect"].x, data["Image_rect"].width - data["Zoom"][0]))
#     data["Zoom_rect"].y = max(0, min(data["Zoom_rect"].y, data["Image_rect"].height - data["Zoom"][1]))
#     I.info.Player_rect = I.pg.Rect(150 + I.info.OFFSCREEN[0]/4, 85 + I.info.OFFSCREEN[1]/4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
#     if I.info.CURRENT_ROOM["Type"] in ["Village"]:
#         sub_image = data["Image"].subsurface(data["Zoom_rect"]).copy()
#         collide = handle_decor_visualisation(decorations, sub_image, data, gifs, rooms, screen, clock, spells, npc)
#     else:
#         sub_image = screen
#         door = render_house(screen, data, rooms)
#         collide = handle_interior_visualisation(decorations, screen, data, gifs)
#         house_border_rect = interior_border_rect(S.SCREEN_WIDTH * 0.1, S.SCREEN_HEIGHT * 0.05, S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.85)
#         me = I.pg.Rect(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 25 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 10 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 22, S.SCREEN_HEIGHT / 8)
#         # I.T.Make_rect_visible(screen, me, "red")
#         handle_stepping_on_rect(me, door, data, screen, clock, spells, "Return", rooms, npc)
#         # collide = handle_stepping_on_rect(me, decorations.decor_dict, data, 0, 0, collide, "Conversation", rooms)
#         collide = handle_stepping_on_rect(me, house_border_rect, data, 0, 0, collide, "Collide_list", rooms, 0)
#
#     # handle_npc_visualisation(sub_image, data, gifs, rooms)
#
#     if I.info.CURRENT_ROOM["Mobs"]:
#         collide = handle_mob_visualisation(collide, sub_image, data, mob, gifs, songs, decorations, items)
#
#     collide = handle_death_visualisation(sub_image, data, gifs, collide)
#
#
#     cast_spell_handle(sub_image, data, spells, gifs, mob, songs, decorations, items)
#
#
#     scaled_image = I.pg.transform.scale(sub_image, data["Window size"])
#     screen.blit(scaled_image, (0, 0))
#     if data["Player"]["dead"] and collide[0] == "mob":  # dont hit mobs when u dead
#         collide = False, 0, 0, 0
#     return collide


def handle_stepping_on_rect(me, rect, data, screen, clock, extra, action, rooms, npc_or_decorations):
    if "Return" in action:
        spells = extra
        if me.colliderect(rect):
            # I.info.ENTRY_POS = [510, 370]
            rooms.select_room("Village_10_10")
            I.info.CURRENT_ROOM = {"name": "Village_10_10", "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": "Village"}
            update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"], spells.selected_spell, npc_or_decorations)
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
    #                         return extra
    #     return extra
        # if rect


def handle_mob_visualisation(collide, sub_image, data, mob_dict, gifs, song, decorations, items, rooms, spells):
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
                if decorations.decor_dict[mob.name]["type"] == "NPC_Mob":
                    if "Guard" in mob.name and "Criminal|0" in I.info.TITLES and current_mob["allignment"] == 2:
                        if current_mob["visible"]:
                            current_mob["allignment"] = 6
                            current_mob["decor"] = False
                            Ff.update_map_view(current_mob["id"], mob.name, (0, 0), "remove")

                mob_gif = 0
                mob_rect = current_mob["rect"][mob_gif]
                mob_x = decorations.decor_dict[mob.name][current_mob["id"]]["rect"].x - data["Zoom_rect"].x
                mob_y = decorations.decor_dict[mob.name][current_mob["id"]]["rect"].y - data["Zoom_rect"].y
            rect = I.pg.Rect(mob_x, mob_y, mob_rect.w, mob_rect.h)
            mob_collision = rect.collidelistall(decorations.displayed_rects_full)
            if mob_collision != []:
                # if mob_y - mob_rect.h / 2 <= decor_rect.y:
                if rect.y <= decorations.displayed_rects_full[mob_collision[0]].y + decorations.displayed_rects_full[mob_collision[0]].h / 2:
                    update_health(rect, current_mob, sub_image[0])
                    image = current_mob["image"][mob_gif]
                    sub_image[0].blit(image, (mob_x, mob_y))
                    handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items)
                    handle_damage_type_visualisation(sub_image[0], current_mob, gifs, (mob_x, mob_y), data, mob, decorations, items)
                else:
                    update_health(rect, current_mob, sub_image[1])
                    image = current_mob["image"][mob_gif]
                    sub_image[1].blit(image, (mob_x, mob_y))
                    handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items)
                    handle_damage_type_visualisation(sub_image[1], current_mob, gifs, (mob_x, mob_y), data, mob, decorations, items)
            else:
                update_health(rect, current_mob, sub_image[0])
                image = current_mob["image"][mob_gif]
                sub_image[0].blit(image, (mob_x, mob_y))
                handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items)
                handle_damage_type_visualisation(sub_image[0], current_mob, gifs, (mob_x, mob_y), data, mob, decorations, items)

            if I.info.Player_rect.colliderect(rect):
                collide = ('mob', mob_rect)
            if I.info.Player_rect.colliderect(rect) and current_mob["allignment"] in [6, 8, 9] and not data["Player"]["dead"]:
                if "Guard" in mob.name and "Criminal|0" in I.info.TITLES:
                    collide = (mob.name, current_mob, mob_rect)
                else:
                    collide = ('mob_collide', current_mob, mob_rect.x, mob_rect.y)
                    data["Player"]["Last_hit"] = I.pg.time.get_ticks()
                    data["Player"]["hp"] = data["Player"]["hp"][0] - int(current_mob["damage"][0]), data["Player"]["hp"][1]

            handle_mob_speed(data, current_mob, decorations, mob, mob_dict, items, gifs, spells)
    return collide
def handle_mob_speed(data, current_mob, decorations, mob, mob_dict, items, gifs, spells):

    speed = current_mob["speed"][0]  # MOB SPEED
    if current_mob["speed"][1] == 0:  # IF MOB SPEED SECOND VALUE IS SET TO 0 IT CAN MOVE
        current_mob["speed"] = speed, speed # RESET SPEED
        current_frame = current_mob["gif_frame"][0] # GET THE NEXT GIF FRAME
        target_pos = (I.info.Player_rect.x + data["Zoom_rect"].x, I.info.Player_rect.y + data["Zoom_rect"].y) # GET THE PLAYER POSSISION
        mob_rect = current_mob["rect"][current_frame] # GET THE CURRENT MOB POSSISION

        if not data["Player"]["dead"] and current_mob["allignment"] == 7:
            target_pos, target = closest_mob(mob_dict, mob_rect, mob.name)
            mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_towards(target_pos, current_mob, speed, decorations.displayed_rects, data["Zoom_rect"]) # GET THE NEW POSISION OF THE MOB THAT IS CHASING YOU
            if target != "" and target[2].colliderect(mob_rect):
                if spells.spawn_counter.get("Spawn " + mob.name) != None and mob_dict[target[0]].hp != 0:
                    mob_dict[target[0]].deal_damage(mob_dict[target[0]].mobs[target[1]], data["Player"], spells.spell_dict["Spawn " + mob.name], items, gifs)

            mob.update_position(mob_rect.x, mob_rect.y, current_mob)  # UPDATE THE POSSISIONS OF THE MOB

        elif not data["Player"]["dead"] and current_mob["allignment"] == 2:
            if current_mob["decor"]:
                current_mob['current_pos'] = decorations.decor_dict[mob.name][current_mob["id"]]["rect"]
            current_mob["visible"] = Ff.get_visible(target_pos, current_mob, decorations.displayed_rects, data["Zoom_rect"])
        elif not data["Player"]["dead"] and current_mob["allignment"] in [6, 8]: # IF THE PLAYER ISN'T DEAD AND THE MOB IS Neutral evil OR Chaotic neutral THEN GO TO THE PLAYER
            mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_towards(target_pos, current_mob, speed, decorations.displayed_rects, data["Zoom_rect"]) # GET THE NEW POSISION OF THE MOB THAT IS CHASING YOU
            mob.update_position(mob_rect.x, mob_rect.y, current_mob)  # UPDATE THE POSSISIONS OF THE MOB
            if current_mob["allignment"] == 8:  # IF THE ALLIGNMENT WAS Chaotic neutral AS IN ATTACKS AND THEN RUNS AWAY THEN SET THE ALLIGNMENT ACORDINGLY TO START RUNNING AWAY
                current_mob["allignment"] = 4 # MIGHT BE POORLY HANDLED I EXPECT MOBS WILL RUN AWAY THE MOMENT THEY SEE THE PLAYER INSTEAD OF ATTACKING IT FIRST

            if mob_rect.x > target_pos[0]:  #Update the orientation of mob running away from me
                current_mob["flip"] = True
            else:
                current_mob["flip"] = False


        elif not data["Player"]["dead"] and current_mob["allignment"] == 4 and current_mob["hp"][0] < current_mob["hp"][1]: # IF MOB ISN'T DEAD AND IM NOT DEAD AND THE ALLIGNMENT IS neutral good THEN RUN AWAY FROM PLAYER IF PROVOKED
            mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_away_from(target_pos, current_mob, speed, decorations.displayed_rects, data["Zoom_rect"])
            mob.update_position(mob_rect.x, mob_rect.y, current_mob)

            if mob_rect.x > target_pos[0]: #Update the orientation of mob running away from me
                current_mob["flip"] = False
            else:
                current_mob["flip"] = True

        else: # IF NOT CHASING ME AND NOT RUNNING AWAY FROM ME THEN MOB IS NOT VISIBLE
            current_mob["visible"] = False

    else:
        # IF MOB SPEED SECOND VALUE IS NOT 0 THEN REMOVE ONE
        current_mob["speed"] = current_mob["speed"][0], current_mob["speed"][1] - 1

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
    rects = {"Sword": I.info.COMBAT_RECT[0],
             "Axe": I.info.AXE[0],
             "Picaxe": I.info.PICAXE[0]
             }
    if any(r != 0 for r in rects.values()):
        damage_type = "Blunt"
        for key ,weapon in I.info.EQUIPED.items():
            if weapon[0] != 0 and rects[key] != 0:
                weapon_data = Ff.get_property(weapon[0], items, "WEAPON")
                damage_type = weapon_data[3]
                break
        if any(r != 0 and r.colliderect(rect) and not gifs[damage_type].start_gif for r in rects.values()):
        # if I.info.COMBAT_RECT[0] != 0 and I.info.COMBAT_RECT[0].colliderect(rect) and not gifs[damage_type].start_gif:
            curr_song = song["Playing"]
            effect = song[curr_song].generate_thump_sound()
            song[curr_song].play_effect(effect)
            gifs[damage_type].Start_gif(damage_type, current_mob)
            mob.deal_damage(current_mob, data["Player"], "", items, gifs)
            if current_mob["hp"][0] > 0:
                set_follower_mob_target(current_mob, mob)


def set_follower_mob_target(mob, mob_class):
    I.info.FOLLOWER["aggressive"]["mob"] = mob
    I.info.FOLLOWER["aggressive"]["class"] = mob_class
    I.info.FOLLOWER["aggressive"]["mob_pos"] = mob["current_pos"]
    I.info.FOLLOWER["aggressive"]["attack"] = True

def handle_death_visualisation(sub_image, data, gifs, collide, decorations):
    if data["Player"]["dead"]:
        me = I.pg.Rect(150, 85, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
        dead_disc = {"Portal": display_gif_on_subimage(sub_image, (S.SCREEN_WIDTH / 16, S.SCREEN_HEIGHT / 10), (I.info.SPAWN_POINT[0] * 1.8 - data["Zoom_rect"].x , I.info.SPAWN_POINT[1] + 10 * 16 - data["Zoom_rect"].y), gifs["Portal"]),
                     "Sign": display_on_subimage(sub_image, (S.SCREEN_WIDTH / 90, S.SCREEN_HEIGHT / 40), S.PLAYING_PATH["Sign"],(I.info.SPAWN_POINT[0] * 1.6 - data["Zoom_rect"].x, I.info.SPAWN_POINT[1] + 10 * 10 - data["Zoom_rect"].y))
                     }
        decorations.displayed_rects.append(dead_disc["Sign"])
        dead_list = list(dead_disc.values())
        if I.info.Player_rect.collidelistall(dead_list):
            keys = list(dead_disc.keys())
            key = keys[I.info.Player_rect.collidelistall(dead_list)[0]]
            collide = (key, dead_disc[key])
        if I.info.CURRENT_ROOM["name"] == I.info.DEATH_SAVE[0]:
            grave = display_on_subimage(sub_image, (S.SCREEN_WIDTH / 60, S.SCREEN_HEIGHT / 30), S.PLAYING_PATH["Grave"], (int(I.info.DEATH_SAVE[1]) - data["Zoom_rect"].x + me.x, int(I.info.DEATH_SAVE[2]) - data["Zoom_rect"].y + me.y))
            decorations.displayed_rects.append(grave)
            collide = ("Grave", grave)
    return collide

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
            if I.info.APPLIANCE_CLICK[0] == "":
                if option in list(gifs.keys()) and option not in ["Furnace", "Blast Furnace"]:
                    display_gif_on_subimage(sub_image, (image_rect.w, image_rect.h), (rect.x, rect.y), gifs[option])
                else:
                    sub_image.blit(decor["image"], (rect.x, rect.y))

            elif I.info.APPLIANCE_CLICK[0] in ["Furnace", "Blast Furnace"]:
                if option in list(gifs.keys()):
                    display_gif_on_subimage(sub_image, (image_rect.w, image_rect.h), (rect.x, rect.y), gifs[option])
                else:
                    sub_image.blit(decor["image"], (rect.x, rect.y))
            decorations.displayed_rects.append(rect)
            # I.T.Make_rect_visible(sub_image, rect, "white")
            # handle colision
            if me.colliderect(rect):
                if decorations.decor_dict[option]["action"] == "NPC":
                    # print("created npc conversation!!")
                    collide = (option, rect, id)
                else:
                    collide = (option, rect, id)
    return collide

def display_strikes(screen, gifs, lock):
    # types = ["Slashing", "Blunt", "Piercing"]
    types = ["Slashing", "Piercing", "Blunt"]
    for type in types:
        if gifs[type + " Strike"].start_gif:
            if I.info.POS_CHANGE[0] == 0 or I.info.POS_CHANGE[0] == I.info.LAST_ORIENT[0]:
                frame = gifs[type + " Strike"].next_frame(1)
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


def display_folower(sub_image, gifs, data, decorations, mob, items):
    if I.info.FOLLOWER["Name"] != "":
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
                        I.info.FOLLOWER["aggressive"]["class"].deal_damage(I.info.FOLLOWER["aggressive"]["mob"], data["Player"], "Follower", items, gifs )
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
            rect = I.pg.Rect(I.info.FOLLOWER["current_pos"][0] - data["Zoom_rect"].x, I.info.FOLLOWER["current_pos"][1] - data["Zoom_rect"].y, 24, 24)
        else:
            rect = I.pg.Rect(I.info.FOLLOWER["current_pos"][0] - data["Zoom_rect"].x, I.info.FOLLOWER["current_pos"][1] - data["Zoom_rect"].y, 18, 18)
        # I.T.Make_rect_visible(sub_image, rect, "red")
        display_gif_on_subimage(sub_image, (rect.w, rect.h), (rect.x, rect.y), gifs[I.info.FOLLOWER["Name"] + orientation[dxdy]])

def handle_tutorial(sub_image, data, screen, npc, items, decorations, gifs, rooms, clock):
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
            I.DialB.init_dialog("Tutorial Man", data["Player"], screen, npc, items, decorations, data, gifs, rooms, clock, spells)
            I.info.tutorial_flag = 0



def display_char(dx, dy, screen, gifs, data, decorations):
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

        if S.GOD_MODE:
            decor = "Wave1"
            Ff.add_image_to_screen(screen, decorations.decor_dict[decor]["path"] + "4.png",[S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + I.info.OFFSCREEN[1], decorations.decor_dict[decor][0]["rect"].w * 4, decorations.decor_dict[decor][0]["rect"].h * 4])  # walking possision could be legs spread
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

# def generate_decor(num_of_items, background_size, path):
#     items = {}
#     for i in range(num_of_items):
#         x = random.randint(0, background_size[0]-100)
#         y = random.randint(0, background_size[1]-100)
#         image = I.pg.image.load(path).convert_alpha()
#         rect = image.get_rect(topleft=(x, y))
#         items[i] = {"image": image, "rect": rect}
#     return items
def generate_mobs(mob, background_size):
    mob_gif_count = Ff.count_png_files(mob.path)
    mob.spawn_mobs(background_size, mob.path, mob_gif_count)
    return mob.mobs





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
            I.info.EQUIPED[option] = 0, I.info.EQUIPED[option][1]
    else:
        if I.info.APPLIANCE_CLICK != [""]:
            if I.info.APPLIANCE_CLICK[3] in ["cook", "burn", "smelt"]:
                for key in I.info.EQUIPED.keys():
                    if I.info.EQUIPED[key][0] == I.info.APPLIANCE_CLICK[1]:
                        if I.info.BACKPACK_CONTENT.get(I.info.APPLIANCE_CLICK[1]) == None:
                            I.info.EQUIPED[key] = 0, I.info.EQUIPED[key][1]
        else:
            for item, (amount, posx, posy) in I.info.BACKPACK_CONTENT.items():
                if posx < 0:
                    I.info.EQUIPED[I.info.equipment[(posx, posy)]] = item, I.info.EQUIPED[I.info.equipment[(posx, posy)]][1]


    for key, item in I.info.EQUIPED.items():
        if I.info.BACKPACK_CONTENT.get(item[0]) == None:
            I.info.EQUIPED[key] = 0, I.info.EQUIPED[key][1]


def BackPack(screen, items, player):
    pressed = 0 # key authentication
    running = True # loop var
    block = (0, 0) # backpack block
    border = 1 # rect border size
    use = 0 # place holder for items to be eaten/used
    selected = 0 # place holder for rect of selected block
    color = "Yellow" # color of selected rect
    pickup = (0, 0, 0) # place holder for the name, posx, posy of selected block
    # fill_backpack(screen, player, items) IDK IF THIS IS NEEDED
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    coordinates = get_equipment_coordinates(block)
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_i:
                    pressed = I.pg.K_i
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
                            I.info.EQUIPED[I.info.equipment[block]] = 0, I.info.EQUIPED[I.info.equipment[block]][1]
                        pickup = (find_item_by_slot(block[0], block[1]), block[0], block[1])
                        if I.info.QUESTS != 0 and I.info.QUESTS["TYPE"] == "Tutorial" and I.info.QUESTS["ACTION"] == "EAT" and I.info.QUESTS["TYPE"] == "Tutorial" and I.info.QUESTS["COMPLETION"] == 0.3333:
                            if pickup[0] == "Light Berries":
                                I.info.QUESTS["COMPLETION"] += 0.3333

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
                                        I.info.BACKPACK_CONTENT[existing_item] = int(sum), I.info.BACKPACK_CONTENT[existing_item][1], I.info.BACKPACK_CONTENT[existing_item][2]
                                        del I.info.BACKPACK_CONTENT[pickup[0]]

                                    elif float(I.info.BACKPACK_CONTENT[existing_item][0]) < stack and float(I.info.BACKPACK_CONTENT[pickup[0]][0]) < stack:
                                        # MERGING VALUES OF STACKS WITH REMAINDER
                                        remainder = float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0]][0]) - stack
                                        I.info.BACKPACK_CONTENT[pickup[0]] = int(remainder), I.info.BACKPACK_CONTENT[pickup[0]][1], I.info.BACKPACK_CONTENT[pickup[0]][2]
                                        I.info.BACKPACK_CONTENT[existing_item] = int(stack), I.info.BACKPACK_CONTENT[existing_item][1], I.info.BACKPACK_CONTENT[existing_item][2]

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
                if pressed == I.pg.K_i or pressed == I.pg.K_ESCAPE:
                    running = False  # exits backpack view
                elif pressed == I.pg.K_x:
                    color = "Yellow"
                    if use != 0 and "CONSUMABLE" in items.item_dict[use.split("|")[0]]["Properties"]:
                        if use == "Light Berries":
                            if I.info.QUESTS != 0 and I.info.QUESTS["TYPE"] == "Tutorial" and I.info.QUESTS["ACTION"] == "EAT" and I.info.QUESTS["COMPLETION"] == 0.6666:
                                I.info.QUESTS["COMPLETION"] = 1
                        handle_consumption(items, player, use)
                        use = 0
                    pressed = 0
                    selected = 0

            display_backpack(screen, player, items, screen.get_rect(), "full")
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
    property_list = items.item_dict[use.split("|")[0]]["Properties"].split(",,,")
    for property in property_list:
        if "CONSUMABLE" in property:
            consumable = property[11:-1] # from CONSUMABLE(valuesss) gets only the values inside
    consumable = consumable.split(",,")
    for consume in consumable:
        points, atribute = consume.split("-")
        if atribute in list(player.keys()):
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
        else:
            if "ITEM" in atribute:
                item = atribute.replace("ITEM:", "")
                amount = I.random.randint(int(points.split(":")[0]), int(points.split(":")[1]))
                Ff.add_to_backpack(item, amount, items)
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

def get_backpack_coordinates(screen, word):
    rect = screen.get_rect()
    bag = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Backpack_Empty_" + word],[rect.center[0] * 0.5, rect.center[1] * 0.25, S.SCREEN_WIDTH / 2,S.SCREEN_HEIGHT * 0.75])
    if I.info.BACKPACK_COORDINATES_X == {}:
        I.info.BACKPACK_COORDINATES_X, I.info.BACKPACK_COORDINATES_Y = bag_coordinates(screen, bag)

def display_backpack(screen, player, items, rect, word):
    I.info.BACKPACK_CONTENT["Gold"] = (player["Gold"],I.info.BACKPACK_CONTENT["Gold"][1], I.info.BACKPACK_CONTENT["Gold"][2])
    bag = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Backpack_Empty_" + word], [rect.center[0] * 0.5 ,rect.center[1] * 0.25, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT * 0.75])
    get_backpack_coordinates(screen, word)
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    for content in I.info.BACKPACK_CONTENT.keys():
        row = I.info.BACKPACK_CONTENT[content][1]
        collumn = I.info.BACKPACK_CONTENT[content][2]
        if row < 0:
            if word == "half":
                continue
            else:
                coordinates = get_equipment_coordinates((row,collumn))
                Ff.add_image_to_screen(screen, items.item_dict[content.split("|")[0]]["path"], [coordinates[row, collumn][0], coordinates[row, collumn][1], item_w, item_h])
                Ff.display_text(screen, str(int(I.info.BACKPACK_CONTENT[content][0])), 2, [coordinates[row, collumn][0], coordinates[row, collumn]][1], "white")
        else:
            # HANDLE MULTIPLE STACKS
            Ff.add_image_to_screen(screen, items.item_dict[content.split("|")[0]]["path"],[list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn], item_w, item_h])
            if content == "Gold":
                amount = round(player["Gold"], 3)
                Ff.display_text(screen, str(amount), 1, [list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn]], "white")
            else:
                Ff.display_text(screen, str(int(I.info.BACKPACK_CONTENT[content][0])), 1, [list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn]], "white")
    if word == "full":
        I.pg.draw.rect(screen, "black", (bag.w * 0.604, bag.h * 0.807, bag.w * 0.115, bag.h * 0.012))
        remainder = player["hp"][0] / player["hp"][1]
        I.pg.draw.rect(screen, "red", (bag.w * 0.604, bag.h * 0.807, bag.w * 0.115 * remainder, bag.h * 0.012))
        Ff.display_text(screen, "Hp", 1, (bag.w * 0.562, bag.h * 0.80), "black")

        I.pg.draw.rect(screen, "black", (bag.w * 0.808, bag.h * 0.807, bag.w * 0.148, bag.h * 0.012))
        remainder = player["mana"][0] / player["mana"][1]
        I.pg.draw.rect(screen, "blue", (bag.w * 0.808, bag.h * 0.807, bag.w * 0.148 * remainder, bag.h * 0.012))
        Ff.display_text(screen, "Mp", 1, (bag.w * 0.752, bag.h * 0.80), "black")

        I.pg.draw.rect(screen, "black", (bag.w * 0.604, bag.h * 0.857, bag.w * 0.115, bag.h * 0.012))
        remainder = int(player["Exhaustion"][0]) / int(player["Exhaustion"][1])
        I.pg.draw.rect(screen, "Green", (bag.w * 0.604, bag.h * 0.857, bag.w * 0.115 * remainder, bag.h * 0.012))
        Ff.display_text(screen, "Exh", 1, (bag.w * 0.55, bag.h * 0.85), "black")

        Ff.add_image_to_screen(screen,'static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + "Front.png",
                               [rect.center[0] * 0.64 ,rect.center[1] * 0.4, S.SCREEN_WIDTH / 8, S.SCREEN_HEIGHT / 4])

        Ff.display_text(screen, "Level: " + str(player["Level"]) , 5, (bag.w * 0.65, bag.h * 0.25), "black")

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
                screen.set_at((left, top), (0,0,0,255))
                # I.T.pause_pygame()
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
    player_disc["hp"] = (txt_data["Health"], hp_by_race[race] * level)
    player_disc["mana"] = (txt_data["Mana"], mana_by_race[race] * level)

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
    player_disc["Exhaustion"] = (txt_data["Exhaustion"], 100)

    player_disc["Last_hit"] = I.pg.time.get_ticks()  # required to know when to start regenerating hp and mana
    player_disc["Save_point"] = txt_data["Save_point"]

    quest_tuple = txt_data["Quests"].split(",,")
    I.info.QUESTS = I.DialB.list_to_dict(quest_tuple)
    I.DialB.check_quest_completion()
    dialog_id = txt_data["Dialog"].split(",,")
    for value in dialog_id:
        if value != "":
            key, id, friendlyness = value.split("__")
            npc[key]["dialog"].iteration = int(id)
            npc[key]["dialog"].friendlyness = int(friendlyness)


    I.info.CONTAINERS = {}
    keys = txt_data["Containers"].split(":::")
    keys = keys[:-1]
    for i in range(0, len(keys), 2):
        output_key = Ff.str_to_tuple(keys[i])
        I.info.CONTAINERS[output_key] = {}
        # print("values: ", keys[i+1])
        values = keys[i+1].split("::")
        for value in values:
            key1 = value.split(":")[0]
            value2 = value.split(":")[1]
            output_key1 = Ff.str_to_tuple(key1)
            output_value = Ff.str_to_tuple(value2)
            I.info.CONTAINERS[output_key][output_key1] = output_value

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
                elif event.key == I.pg.K_u:
                    pressed = I.pg.K_u
            if event.type == I.pg.KEYUP:
                if pressed == I.pg.K_u or pressed == I.pg.K_ESCAPE:
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
            rect_selected = I.pg.Rect(list(I.info.SPELLBOOK_COORDINATES_X.values())[block[0]], list(I.info.SPELLBOOK_COORDINATES_Y.values())[11] + list(I.info.SPELLBOOK_COORDINATES_Y.values())[0], item_w, item_h)
        else:
            rect_selected = I.pg.Rect(list(I.info.SPELLBOOK_COORDINATES_X.values())[block[0]],list(I.info.SPELLBOOK_COORDINATES_Y.values())[block[1]], item_w, item_h)


        if spells.selected_spell != {}:
            for pos, spell in spells.selected_spell.items():
                rect = I.pg.Rect(list(I.info.SPELLBOOK_COORDINATES_X.values())[int(pos)],list(I.info.SPELLBOOK_COORDINATES_Y.values())[11] +list(I.info.SPELLBOOK_COORDINATES_Y.values())[0], item_w, item_h)
                Ff.add_image_to_screen(screen, gifs[spell].frame_paths[0][:-5] + "icon.png", rect)
        I.pg.draw.rect(screen, color, rect_selected, border)
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
        Ff.add_image_to_screen(screen, gifs[content].frame_paths[0][:-5] + "icon.png", [list(I.info.SPELLBOOK_COORDINATES_X.values())[row], list(I.info.SPELLBOOK_COORDINATES_Y.values())[collumn], item_w, item_h])

def display_gif_on_subimage(sub_image, size, pos, gif):
    repeat = -1
    frame = gif.next_frame(repeat)
    frame = I.pg.transform.scale(frame, (size[0], size[1]))
    sub_image.blit(frame, pos)
    return I.pg.Rect(pos[0], pos[1], size[0], size[1])

def cast_spell_handle(sub_image, data, spells, gifs, mob, song, decorations, items, rooms):
    if not data["Player"]["dead"]:
        for slot, spell_name in spells.selected_spell.items():
            if gifs[spell_name].start_gif:
                spells.spell_cooloff[spell_name] = spells.spell_dict[spell_name]["recharge"]
                # I.th.start_thread(0, "spell_cooloff", spells)
                if "Spawn" in spell_name:
                    handle_spawn_spell(data, spells, gifs, decorations, sub_image, rooms, spell_name, mob)
                elif spell_name == "Flash":
                    handle_flash_spell(data, spells, gifs, decorations, sub_image, rooms)
                elif "Heal" in spell_name:
                    handle_heal_spell(data, spells, gifs, spell_name, sub_image, rooms)
                else:
                    bolt_spell_handle(spells, gifs, spell_name, decorations, song, data["Zoom_rect"], mob, items, sub_image, data["Player"], rooms)
            else:
                # RESET DIRECTION OF FIRE
                spells.direction[spell_name] = 0
                spells.init_cast[spell_name] = 0

def bolt_spell_handle(spells, gifs, spell_name, decorations, song, zoom_rect, mobs, items, sub_image, player, rooms):
    curr_song = song["Playing"]
    sound_type = {"Force": song[curr_song].generate_magic_sound(),
                  "Fire": song[curr_song].generate_fire_sound(),
                  "Cold": song[curr_song].generate_cold_sound()}
    frame = gifs[spell_name].next_frame(1)

    if rooms.type in ["Village"]:
        size = (20, 20)
    else:
        size = (80, 80)
    frame = I.pg.transform.scale(frame, size)
    if spells.direction[spell_name] == 0:
        if I.info.CURRENT_ROOM["Type"] in ["Village"]:
            spells.init_cast[spell_name] = zoom_rect.copy()
            spells.direction[spell_name] = I.info.LAST_ORIENT[0].split(".")[0]
        else:
            spells.init_cast[spell_name] = I.pg.Rect(S.SCREEN_WIDTH / 2 + S.SCREEN_WIDTH / 20 - I.info.Player_rect.w * 10 + I.info.OFFSCREEN[0],
                S.SCREEN_HEIGHT / 2 - I.info.Player_rect.h * 10 + I.info.OFFSCREEN[1], size[0], size[1])
            spells.direction[spell_name] = I.info.LAST_ORIENT[0].split(".")[0]

    direction_settings = {
        "Front": {"rect": (145, 80), "dir": (0, -1), "rotate": 90, "flip": (False, True)},
        "Back": {"rect": (145, 70), "dir": (0, 1), "rotate": 90, "flip": (False, False)},
        "Left": {"rect": (140, 75), "dir": (1, 0), "rotate": 0, "flip": (True, False)},
        "Right": {"rect": (150, 75), "dir": (-1, 0), "rotate": 0, "flip": (False, False)},
    }
    spell_direction = spells.direction[spell_name]
    settings = direction_settings.get(spell_direction)
    # me = I.pg.Rect(settings["rect"][0], settings["rect"][1], S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)
    dir = settings["dir"]
    frame = I.pg.transform.rotate(frame, settings["rotate"])
    frame = I.pg.transform.flip(frame, *settings["flip"])

    if gifs[spell_name].current_frame != 0:
        if I.info.CURRENT_ROOM["Type"] == "Village":
            rect = I.pg.Rect(spells.init_cast[spell_name].x - zoom_rect.x + I.info.Player_rect.x - dir[0] * gifs[spell_name].current_frame * 6,
                             spells.init_cast[spell_name].y - zoom_rect.y + I.info.Player_rect.y - dir[1] * gifs[spell_name].current_frame * 6, size[0], size[1])
        else:
            rect = I.pg.Rect(spells.init_cast[spell_name].x - dir[0] * gifs[spell_name].current_frame * 12 * 2,
                             spells.init_cast[spell_name].y - dir[1] * gifs[spell_name].current_frame * 12 * 2, size[0], size[1])

        sub_image.blit(frame, rect)
        if I.info.CURRENT_ROOM["Type"] == "Village":
            if rect.collidelist(decorations.displayed_rects) != -1:  # if hits any decor
                type = spells.spell_dict[spell_name]["type"]
                song[curr_song].play_effect(sound_type[type])
                gifs[spell_name].start_gif = False
                index = rect.collidelist(decorations.displayed_rects)
                decorations.effected_decor[index] = type
            else:
                for key in mobs.keys():
                    for current_mob in mobs[key].mobs:
                        mob_rect = I.pg.Rect(current_mob["rect"][0].x - zoom_rect.x, current_mob["rect"][0].y - zoom_rect.y, current_mob["rect"][0].w, current_mob["rect"][0].h)
                        if rect.colliderect(mob_rect):
                            mobs[key].deal_damage(current_mob, player, spells.spell_dict[spell_name], items, gifs)
                            gifs[spell_name].start_gif = False  # IF COMMENTED OUT, MAKES A SPELL GO THROUGH MULTIPLE ENEMIES
                            type = spells.spell_dict[spell_name]["type"]
                            gifs[type].Start_gif(type, current_mob)
                            song[curr_song].play_effect(sound_type[type])

def handle_heal_spell(data, spells, gifs, name, sub_image, rooms):
    healing_power = 0

    frame = gifs[name].next_frame(1)
    if "Minor" in name and healing_power == 0:
        healing_power = 0.06
    if rooms.type in ["Village"]:
        rect = I.pg.Rect(I.info.Player_rect.x - 20,I.info.Player_rect.y - 25, I.info.Player_rect.w, I.info.Player_rect.h )
    else:
        rect = I.pg.Rect(I.info.OFFSCREEN[0] + 530, I.info.OFFSCREEN[1] + 250, I.info.Player_rect.w, I.info.Player_rect.h)
        frame = I.pg.transform.scale(frame, (I.info.Player_rect.w * 14, I.info.Player_rect.h * 12))
    data["Player"]["hp"] = data["Player"]["hp"][0] + healing_power, data["Player"]["hp"][1]
    if data["Player"]["hp"][0] > data["Player"]["hp"][1]:
        data["Player"]["hp"] = data["Player"]["hp"][1], data["Player"]["hp"][1]
    sub_image.blit(frame, rect)

def handle_spawn_spell(data, spells, gifs, decorations, sub_image, rooms, name, mobs):
    frame = gifs[name].next_frame(1)
    mob_name = name.split(" ")[1]
    if rooms.type in ["Village"]:
        frame = I.pg.transform.scale(frame, (I.info.Player_rect.w * 5, I.info.Player_rect.h * 5))
        rect = I.pg.Rect(I.info.Player_rect.x - 20, I.info.Player_rect.y - 25, I.info.Player_rect.w, I.info.Player_rect.h)
    else:
        rect = I.pg.Rect(I.info.OFFSCREEN[0] + 530, I.info.OFFSCREEN[1] + 250, I.info.Player_rect.w, I.info.Player_rect.h)
        frame = I.pg.transform.scale(frame, (I.info.Player_rect.w * 14, I.info.Player_rect.h * 12))
    if spells.spawn_counter.get(name) == None:
        """ no skeletons spawned """
        mob_dict = I.mob_data.read_db()
        cur_dict = mob_dict[mob_name]
        frame_count = Ff.count_png_files(cur_dict["path"])
        path = cur_dict["path"]
        if path == "Decor":
            path = decorations.decor_dict[mob_dict]["path"]
        mobs[mob_name + " Mine"] = I.mob_data.Mob(name=mob_name + " Mine", exp=cur_dict["exp"], hp=cur_dict["health"], allignment=7, count=3, damage=cur_dict["damage"].split(":"), speed=cur_dict["speed"], path=path, delay=(cur_dict["delay"], cur_dict["delay"]), decor=False)

        mobs[mob_name + " Mine"].spawn_mob_acurate(cur_dict["path"], frame_count, 0, data["Zoom_rect"].x + 180, data["Zoom_rect"].y + 60)
        mobs[mob_name + " Mine"].spawn_mob_acurate(cur_dict["path"], frame_count, 1, data["Zoom_rect"].x + 140, data["Zoom_rect"].y + 80)
        mobs[mob_name + " Mine"].spawn_mob_acurate(cur_dict["path"], frame_count, 2, data["Zoom_rect"].x + 160, data["Zoom_rect"].y + 100)
        I.th.start_thread(30000, "spawn", (spells, mobs))
        spells.init_cast[name] = 3
        spells.spawn_counter[name] = 3
    elif spells.spawn_counter[name] >= 3 and spells.init_cast[name] != 3:
        mob_dict = I.mob_data.read_db()
        cur_dict = mob_dict[mob_name]
        frame_count = Ff.count_png_files(cur_dict["path"])

        # mobs[mob_name + " Mine"] = I.mob_data.Mob(name=mob_name + " Mine", exp=cur_dict["exp"], hp=cur_dict["health"], allignment=6, count=6, damage=cur_dict["damage"].split(":"), speed=cur_dict["speed"], path=cur_dict["path"], delay=(cur_dict["delay"], cur_dict["delay"]))
        mobs[mob_name + " Mine"].allignment = 6
        mobs[mob_name + " Mine"].count = (3 + mobs[mob_name + " Mine"].count[0], 3 + mobs[mob_name + " Mine"].count[1])
        mobs[mob_name + " Mine"].mobs.append(mobs[mob_name + " Mine"].create_mob(3))
        mobs[mob_name + " Mine"].mobs.append(mobs[mob_name + " Mine"].create_mob(4))
        mobs[mob_name + " Mine"].mobs.append(mobs[mob_name + " Mine"].create_mob(5))
        mobs[mob_name + " Mine"].spawn_mob_acurate(cur_dict["path"], frame_count, 3, data["Zoom_rect"].x + 180, data["Zoom_rect"].y + 60)
        mobs[mob_name + " Mine"].spawn_mob_acurate(cur_dict["path"], frame_count, 4, data["Zoom_rect"].x + 140, data["Zoom_rect"].y + 80)
        mobs[mob_name + " Mine"].spawn_mob_acurate(cur_dict["path"], frame_count, 5, data["Zoom_rect"].x + 160, data["Zoom_rect"].y + 100)
        spells.init_cast[name] = 3 + spells.init_cast[name]
        spells.spawn_counter[name] = 3 + spells.spawn_counter[name]

    sub_image.blit(frame, rect)
def handle_flash_spell(data, spells, gifs, decorations, sub_image, rooms):

    distance = 50
    gifs["Flash"].next_frame(1)
    gifs["Flash"].start_gif = False
    i = 1
    while distance != i:

        pos = {
            "Right.png": (1, 0),
            "Left.png": (-1, 0),
            "Front.png": (0, 1),
            "Back.png": (0, -1)
        }
        if rooms.type == "Village":
            me = I.pg.Rect(150 + pos[I.info.LAST_ORIENT[0]][0] * i + I.info.OFFSCREEN[0] / 4, 85 + pos[I.info.LAST_ORIENT[0]][1] * i + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)
            I.T.Make_rect_visible(sub_image, I.pg.Rect(150 - pos[I.info.LAST_ORIENT[0]][0] * i + I.info.OFFSCREEN[0] / 4, 80 - pos[I.info.LAST_ORIENT[0]][1] * i + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 50), "yellow")
        else:
            me = I.pg.Rect(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 24 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 16 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 24, S.SCREEN_HEIGHT / 12)
            I.T.Make_rect_visible(sub_image, me, "yellow")
        if me.collidelist(decorations.displayed_rects) != -1:
            print("collide")
            break
        if I.info.OFFSCREEN[0] == 0 and I.info.LAST_ORIENT[0] in ["Right.png", "Left.png"] and int(data["Zoom_rect"].x + pos[I.info.LAST_ORIENT[0]][0]) > 0 and int(data["Zoom_rect"].x + pos[I.info.LAST_ORIENT[0]][0]) < 680:
            data["Zoom_rect"] = I.pg.Rect(data["Zoom_rect"].x + pos[I.info.LAST_ORIENT[0]][0], data["Zoom_rect"].y, data["Zoom_rect"].w, data["Zoom_rect"].h)
        elif I.info.LAST_ORIENT[0] in ["Right.png", "Left.png"]:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0] + pos[I.info.LAST_ORIENT[0]][0] * 3, I.info.OFFSCREEN[1])
        if I.info.OFFSCREEN[1] == 0 and I.info.LAST_ORIENT[0] in ["Back.png", "Front.png"] and int(data["Zoom_rect"].y + pos[I.info.LAST_ORIENT[0]][1]) > 0 and int(data["Zoom_rect"].y + pos[I.info.LAST_ORIENT[0]][1]) < 820:
            data["Zoom_rect"] = I.pg.Rect(data["Zoom_rect"].x, data["Zoom_rect"].y + pos[I.info.LAST_ORIENT[0]][1], data["Zoom_rect"].w, data["Zoom_rect"].h)
        elif I.info.LAST_ORIENT[0] in ["Back.png", "Front.png"]:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0], I.info.OFFSCREEN[1] + pos[I.info.LAST_ORIENT[0]][1] * 3)
        i += 1



# def display_border(border_image_name, decorations, data):
#     path = decorations.decor_dict[border_image_name]["path"]
#     image = I.pg.image.load(path).convert_alpha()
#     rect = image.get_rect()
#     tree_amount = 0
#     row = 0
#     while True:
#         # building on the x axis (virsus ir apacia)
#         # virsui pirma juosta
#         # apacioj pirma
#         # virsui antra
#         # apacioj antra
#         tree_image1, tree_rect1 = decorations.place_decor_by_coordinates(row, 0, path, (0.8, 0.8), (1, 0.3))
#         tree_image2, tree_rect2 = decorations.place_decor_by_coordinates(row, data["Image_rect"].h - (rect.h * 0.8), path, (0.8, 0.8), (1, 0.5))
#
#         tree_image3, tree_rect3 = decorations.place_decor_by_coordinates(row + rect.w/4, rect.h * 0.3, path, (0.8, 0.8), (0.8, 0.8))
#         tree_image4, tree_rect4 = decorations.place_decor_by_coordinates(row + rect.w/4, data["Image_rect"].h - (rect.h * 1.3), path, (0.8, 0.8), (0.8, 0.5))
#         if data["Image_rect"].w <= tree_rect3.x + tree_rect3.w:
#             break
#         decorations.decor_dict[border_image_name][tree_amount] = {"name": border_image_name, "id": tree_amount, "image": tree_image1, "rect": tree_rect1, "effect": ""}
#         tree_amount += 1
#         decorations.decor_dict[border_image_name][tree_amount] = {"name": border_image_name, "id": tree_amount, "image": tree_image2, "rect": tree_rect2, "effect": ""}
#         tree_amount += 1
#
#         decorations.decor_dict[border_image_name][tree_amount] = {"name": border_image_name, "id": tree_amount, "image": tree_image3, "rect": tree_rect3, "effect": ""}
#         tree_amount += 1
#         decorations.decor_dict[border_image_name][tree_amount] = {"name": border_image_name, "id": tree_amount, "image": tree_image4, "rect": tree_rect4, "effect": ""}
#         tree_amount += 1
#
#         row += rect.w * 0.5
#
#     column = rect.h * 0.5
#     while True:
#         # building on the y axis (kaire ir desine)
#         # kairei pirma juosta
#         # desinei pirma
#         # kairei antra
#         # desinei antra
#
#         tree_image1, tree_rect1 = decorations.place_decor_by_coordinates(0, column, path, (0.8, 0.8), (0.4, 0.5))
#         tree_image2, tree_rect2 = decorations.place_decor_by_coordinates(data["Image_rect"].w - rect.w, column, path, (0.8, 0.8), (0.8, 0.7))
#
#         tree_image3, tree_rect3 = decorations.place_decor_by_coordinates(rect.w * 0.4, column + rect.h/4, path, (0.8, 0.8), (0.8, 0.7))
#         tree_image4, tree_rect4 = decorations.place_decor_by_coordinates(data["Image_rect"].w - (rect.w * 1.3), column + rect.h/4, path, (0.8, 0.8), (0.3, 0.7))
#         if data["Image_rect"].h <= (tree_rect3.y + tree_rect3.h):
#             break
#
#         decorations.decor_dict[border_image_name][tree_amount] = {"image": tree_image1, "rect": tree_rect1}
#         tree_amount += 1
#         decorations.decor_dict[border_image_name][tree_amount] = {"image": tree_image2, "rect": tree_rect2}
#         tree_amount += 1
#
#         decorations.decor_dict[border_image_name][tree_amount] = {"image": tree_image3, "rect": tree_rect3}
#         tree_amount += 1
#         decorations.decor_dict[border_image_name][tree_amount] = {"image": tree_image4, "rect": tree_rect4}
#         tree_amount += 1
#
#         column += rect.w * 0.5

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
                dialog_str += npc_name + "__" + str(npc[npc_name]["dialog"].iteration) + "__" + str(npc[npc_name]["dialog"].friendlyness) + ",,"
            lines[i] = f'Dialog: {dialog_str}\n'
        elif line.startswith('Quests:'):
            if I.info.QUESTS != 0:
                quest_str = ""
                for key in I.info.QUESTS.keys():
                    quest_str += str(key) + ":" + str(I.info.QUESTS[key]) + ",,"
                quest_str = quest_str[:-2]
            else:
                quest_str = ',,'
            lines[i] = f'Quests: {quest_str}\n'
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
            container_str = ""
            # print(I.info.CONTAINERS)
            for key, value in I.info.CONTAINERS.items():
                # print("containers: ", key, value)
                container_str += str(key) + ":::"
                for sub_key, sub_value in value.items():
                    # print(sub_key, sub_value)
                    container_str += str(sub_key) + ":" + str(sub_value) + "::"
                container_str += ":"
                # print(container_str)
            container_str = container_str[:-3]
            lines[i] = f'Containers: {container_str}\n'


    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)



def find_item_by_slot(x, y):
    for key, value in I.info.BACKPACK_CONTENT.items():
        if value[1] == x and value[2] == y:
            # if the possision matches get the key
            return key
    return None

def find_item_by_slot_containers(x, y, container, id):
    if I.info.CONTAINERS.get((container, id)) != None:
        for key, value in I.info.CONTAINERS[container, id].items():
            if key[0] == x and key[1] == y:
                # if the possision matches get the key
                return value[0]
    else:
        return None

def update_equipment_var(key, value):
    if key[0] < 0:
        I.info.EQUIPED[I.info.equipment[key]] = value, I.info.EQUIPED[I.info.equipment[key]][1]

def interior_border_rect(left, top, width, height, decorations):
    right = left + width
    bottom = top + height
    top_rect = I.pg.Rect(left, top, right - left, 5) # top
    right_rect = I.pg.Rect(right,top, 5, bottom - top) # right
    left_rect = I.pg.Rect(left, top, 5, bottom - top) # left
    bottom_rect = I.pg.Rect(left, bottom, right - left, 5) # bottom
    decorations.displayed_rects.append(top_rect)
    decorations.displayed_rects.append(right_rect)
    decorations.displayed_rects.append(left_rect)
    decorations.displayed_rects.append(bottom_rect)
    return [top_rect, right_rect, left_rect, bottom_rect]

def decorate_from_db(rooms, decorations):
    for decor_name in rooms.decor:
        path = decorations.decor_dict[decor_name]["path"]
        health = decorations.decor_dict[decor_name]["health"]
        if decor_name in ["Furnace", "Blast Furnace"]:
            path += "out.png"
        elif path[-1] == "_":
            path += "0.png"
        for i in range(0, len(rooms.data[decor_name])):
            image, rect = decorations.place_decor_by_coordinates(rooms.data[decor_name][i]["x"], rooms.data[decor_name][i]["y"], path, (rooms.data[decor_name][i]["img_x"], rooms.data[decor_name][i]["img_y"]), (rooms.data[decor_name][i]["rect_x"], rooms.data[decor_name][i]["rect_y"]))
            decorations.decor_dict[decor_name][i] = {"name": decor_name, "id": i, "image": image, "rect": rect, "effect": "", "health": health}

def quest_render(screen, items):
    running = True
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    key_auth = 0
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key in [I.pg.K_ESCAPE, I.pg.K_q]:
                    key_auth = event.key
            if event.type == I.pg.KEYUP:
                if event.key == key_auth and event.key in [I.pg.K_ESCAPE, I.pg.K_q]:
                    running = False
        Ff.add_image_to_screen(screen, S.PLAYING_PATH["Quest_Empty"], [S.SCREEN_WIDTH / 4, S.SCREEN_HEIGHT / 5, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT / 1.5])
        Ff.display_text(screen, "Quests", 13, (600,160))
        if I.info.QUESTS != 0:
            quest_type = I.info.QUESTS["TYPE"]
            quest_describtion = I.info.QUESTS["DESC"]
            if "\\n" in quest_describtion:
                lines = quest_describtion.split("\\n")
                collum =  S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 1.5
                for line in lines:
                    Ff.display_text(screen, line, 5, (S.SCREEN_WIDTH / 3 * 0.9,collum), "Black")
                    collum += 20
            else:
                Ff.display_text(screen, quest_describtion, 5, (S.SCREEN_WIDTH / 3 * 0.9, S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 1.5), "Black")
            if I.info.QUESTS["COMPLETION"] != 1:
                Ff.display_text(screen, "In Progress", 4, (S.SCREEN_WIDTH / 3 * 0.9, S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 3.5), "Black")
            else:
                Ff.display_text(screen, "COMPLETED Recieve reward from - " + str(I.info.QUESTS["GIVER"]), 4, (S.SCREEN_WIDTH / 3 * 0.9, S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 3.5), "Black")

            # if quest_type == "GET":
            #     Ff.add_image_to_screen(screen, items.item_dict[I.info.QUESTS["ITEM"]]["path"], [S.SCREEN_WIDTH / 3 * 1.5, S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 1.1, item_w, item_h])

            remainder = I.DialB.check_quest_completion()
            I.pg.draw.rect(screen, "black", (S.SCREEN_WIDTH / 3 * 0.9, S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 4.1, item_w * 18, item_h * 0.3))
            I.pg.draw.rect(screen, "green", (S.SCREEN_WIDTH / 3 * 0.9, S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 4.1, item_w * 18 * remainder, item_h * 0.3))
        I.pg.display.flip()



def handle_shop(case, player, screen, items):
    if case == "Armory":
        block = (0, 0)
        color = "yellow"
        border = 1
        pressed = 0
        mode = 0
        running = True
        selected = 0
        display_text = []
        fill_shop(screen, case, items, mode, player)
        item_w = list(I.info.SHOP_COORDINATES_X.values())[1] - list(I.info.SHOP_COORDINATES_X.values())[0]
        item_h = list(I.info.SHOP_COORDINATES_Y.values())[1] - list(I.info.SHOP_COORDINATES_Y.values())[0]
        while running:
            for event in I.pg.event.get():
                if event.type == I.pg.KEYDOWN:
                    if event.key == I.pg.K_c:
                        if mode == 2:
                            running = False
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
                            block = (block[0] - 15, block[1])
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
                    elif event.key == I.pg.K_q and selected == 0:
                        # so that only be able to switch rows when no item is selected
                        mode -= 1
                        if mode < 0:
                            mode = 0
                    elif event.key == I.pg.K_e and selected == 0:
                        # so that only be able to switch rows when no item is selected
                        mode += 1
                        if mode > 2:
                            mode = 2
                if event.type == I.pg.KEYUP:
                    if pressed == I.pg.K_ESCAPE:
                        running = False
                    if event.key == I.pg.K_c and pressed == I.pg.K_c:
                        if selected == 0:
                            if mode == 0:
                                for item, (row, collum) in I.info.SHOP_CONTENT.items():
                                    if block == (row, collum):
                                        selected = item
                                        border = 2
                            elif mode == 1:
                                item_list = []
                                for item, (amount, row, collum) in I.info.BACKPACK_CONTENT.items():
                                    if item == "Gold":
                                        continue
                                    item_list.append(item)
                                if len(item_list) - 1 >= int(block[0] / 2 + 15 * (block[1] / 2)):
                                    selected = item_list[int(block[0] / 2 + 15 * (block[1] / 2))]
                                    print(selected, int(block[0] / 2 + 15 * (block[1] / 2)), block, item_list)
                                    border = 2
                                    block = 0, block[1]
                                else:
                                    selected = 0
                        else:
                            if mode == 0:
                                if block[0] == 0:
                                    # If selected item in buying and pressed "buy"
                                    if items.item_dict[selected]["Cost"] > player["Gold"] * 10:
                                        display_text = ["Not enough Gold", 40, [420, 520]]
                                    else:
                                        display_text = ["Bought", 40, [420, 520]]
                                        Ff.add_to_backpack(selected, 1, items)  # Adds bought item through shop
                                        player["Gold"] -= items.item_dict[selected]["Cost"] / 10
                                        block = I.info.SHOP_CONTENT[selected]
                                        selected = 0
                                else:
                                    # If selected item in buying and pressed "Back"
                                    block = I.info.SHOP_CONTENT[selected]
                                    selected = 0
                            elif mode == 1:
                                # if selected item in selling
                                if block[0] == 0:
                                    # selling this item
                                    player["Gold"] += items.item_dict[selected.split("|")[0]]["Cost"] / 10 * 0.8
                                    location = list(I.info.BACKPACK_CONTENT.keys()).index(selected)
                                    block = (location % 15) * 2 - 2, (location // 15) * 2
                                    remove_from_backpack(selected, 1)
                                    selected = 0
                                else:
                                    # going back
                                    location = list(I.info.BACKPACK_CONTENT.keys()).index(selected)
                                    block = (location % 15) * 2 - 2, (location // 15) * 2
                                    selected = 0
                            if block[0] == 20:
                                selected = 0

                    if event.key == I.pg.K_x:
                        selected = 0
                        display_text = []
                        border = 1
                    pressed = 0
            if selected != 0:
                if block[0] < 10:
                    block = 0, block[1]
                    rect = I.pg.Rect(list(I.info.SHOP_COORDINATES_X.values())[block[0]],list(I.info.SHOP_COORDINATES_Y.values())[16] + item_h * 1.8, item_w * 6, item_h)
                elif block[0] < 28:
                    block = 20, block[1]
                    rect = I.pg.Rect(list(I.info.SHOP_COORDINATES_X.values())[block[0]] + 12,list(I.info.SHOP_COORDINATES_Y.values())[16] + item_h * 1.8, item_w * 6 - 4, item_h)
            else:
                rect = I.pg.Rect(list(I.info.SHOP_COORDINATES_X.values())[block[0]],list(I.info.SHOP_COORDINATES_Y.values())[block[1]], item_w, item_h)

            fill_shop(screen, case, items, mode, player)

            if mode == 0:
                for item, (row, collum) in I.info.SHOP_CONTENT.items():
                    if block == (row, collum) and selected == 0:
                        display_text = [items.item_dict[item]["describtion"], 10, [390, 500]]
                        break
            elif mode == 1:
                item_list = []
                for item, (amount, row, collum) in I.info.BACKPACK_CONTENT.items():
                    if item == "Gold":
                        continue
                    item_list.append(item)
                    if len(item_list) - 1 >= block[0] / 2 + 15 * (block[1] / 2) and selected == 0:
                        display_text = [items.item_dict[item_list[int((block[0] / 2) + 15 * (block[1] / 2))].split("|")[0]]["describtion"], 10, [390, 500]]
                        break
            elif mode == 2:
                display_text = []

            if display_text != []:
                if "\\n" in display_text[0]:
                    lines = display_text[0].split("\\n")
                    for i in range(len(lines)):
                        Ff.display_text(screen, lines[i], display_text[1], (display_text[2][0], display_text[2][1] + i * 20), "black")
                else:
                    Ff.display_text(screen, display_text[0], display_text[1], display_text[2], "black")

            if mode != 2:
                I.pg.draw.rect(screen, color, rect, border)
            I.pg.display.flip()

def fill_shop(screen, type, items, mode, player):
    rect = screen.get_rect()
    path = S.PLAYING_PATH["Shop_Empty"]
    color = ("black", "brown4", "brown4")

    if mode == 1:
        path = path[:-4] + "_Sell.png"
        color = ("brown4", "black", "brown4")
    elif mode == 2:
        path = path[:-4] + "_Exit.png"
        color = ("brown4", "brown4", "black")

    gold = player["Gold"]
    gold = round(gold, 3)

    shop = Ff.add_image_to_screen(screen, path, [rect.center[0] * 0.5, rect.center[1] * 0.25, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT * 0.75])
    if mode == 0:
        Ff.display_text(screen, "Buy", 16, (420, 452), "black")
    elif mode == 1:
        Ff.display_text(screen, "Sell", 16, (420, 452), "black")
    elif mode == 2:
        Ff.display_text(screen, "Exit - hit [C]", 30, (500, 280), "black")

    Ff.add_image_to_screen(screen, items.item_dict["Gold"]["path"], (550, 450, 34, 30))
    Ff.display_text(screen, "Gold: " + str(gold), 16, (580, 452), "black")
    Ff.display_text(screen, "Buy", 8, (400, 119), color[0])
    Ff.display_text(screen, "Sell", 8, (540, 119), color[1])
    Ff.display_text(screen, "Exit", 8, (670, 118), color[2])
    Ff.display_text(screen, "Back", 16, (780, 452), "black")

    if I.info.SHOP_COORDINATES_X == {}:
        I.info.SHOP_COORDINATES_X, I.info.SHOP_COORDINATES_Y = bag_coordinates(screen, shop)

    item_w = list(I.info.SHOP_COORDINATES_X.values())[1] - list(I.info.SHOP_COORDINATES_X.values())[0]
    item_h = list(I.info.SHOP_COORDINATES_Y.values())[1] - list(I.info.SHOP_COORDINATES_Y.values())[0]

    new_backpackcontent = []
    row = 0
    collumn = 0
    if I.info.SHOP_CONTENT == {}:
        for item in items.item_dict.keys():
            if "WEAPON" in items.item_dict[item]["Properties"] or "HOE" in items.item_dict[item]["Properties"]:
                I.info.SHOP_CONTENT[item] = row, collumn
                row += 2
                if row == 28:
                    collumn += 2
                    row = 0
    if mode == 0:
        for content in I.info.SHOP_CONTENT.keys():
            row, collumn = I.info.SHOP_CONTENT[content]
            Ff.add_image_to_screen(screen, items.item_dict[content]["path"], [list(I.info.SHOP_COORDINATES_X.values())[row], list(I.info.SHOP_COORDINATES_Y.values())[collumn], item_w, item_h])
    elif mode == 1:
        row = 0
        collumn = 0
        for content in I.info.BACKPACK_CONTENT.keys():
            amount, not_used_row, not_used_collumn = I.info.BACKPACK_CONTENT[content]
            if content == "Gold":
                continue
            if row >= 0:
                Ff.add_image_to_screen(screen, items.item_dict[content.split("|")[0]]["path"], [list(I.info.SHOP_COORDINATES_X.values())[row], list(I.info.SHOP_COORDINATES_Y.values())[collumn], item_w, item_h])
                # print(row, collumn)
                Ff.display_text(screen, str(int(amount)), 1, (list(I.info.SHOP_COORDINATES_X.values())[row], list(I.info.SHOP_COORDINATES_Y.values())[collumn]), "white")
                row += 2
                if row == 30:
                    collumn += 2
                    row = 0

def display_lower_upper_decor(option, gifs, new_subimage, rect, rooms, clock, screen, decor, decorations, data, spells, npc):
    if option in list(gifs.keys()):
        if "door" not in option and "Wave" not in option:
            # Display all gifs appart from door and wave.
            display_gif_on_subimage(new_subimage, (rect.w, rect.h), (rect.x, rect.y), gifs[option])
        elif "Wave" in option:
            if gifs[option].pause == 0:
                display_gif_on_subimage(new_subimage, (rect.w, rect.h), (rect.x, rect.y), gifs[option])
            if gifs[option].current_frame == 0 and gifs[option].pause == 0 and option in ["Wave1", "Wave4"]:
                gifs[option].pause = 1
                # I.pg.time.set_timer(I.pg.USEREVENT + 11, 2000)
                I.th.start_thread(5000, "waves", gifs)
        elif I.info.DOOR_CLICK != (90, "") and I.info.DOOR_CLICK[0] < gifs[I.info.DOOR_CLICK[1]].frame_count:
            if I.pg.time.get_ticks() - gifs[I.info.DOOR_CLICK[1]].frame_time > gifs[I.info.DOOR_CLICK[1]].delay:
                I.info.DOOR_CLICK = I.info.DOOR_CLICK[0] + 1, I.info.DOOR_CLICK[1]
            display_gif_on_subimage(new_subimage, (rect.w, rect.h), (rect.x, rect.y), gifs[I.info.DOOR_CLICK[1]])
            if I.info.DOOR_CLICK[0] == gifs[I.info.DOOR_CLICK[1]].frame_count:
                building = I.info.DOOR_CLICK[1].split("_")[0]
                I.info.DOOR_CLICK = 90, ""  # RESET I.info.DOOR_CLICK
                # print(building)
                rooms.select_room(building)
                I.info.CURRENT_ROOM = {"name": building, "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": "House"}
                I.info.ENTRY_POS = (1, 1)
                I.info.OFFSCREEN = (25, 250)
                update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"], spells.selected_spell, npc)
                Play.Start(screen, clock, rooms)
    else:
        size = decor["image"].get_rect()
        decor["image"] = I.pg.transform.scale(decor["image"], (size.w, size.h))
        new_subimage.blit(decor["image"], (rect.x, rect.y))

def New_Update(data, decorations, gifs: dict, rooms, clock, screen, spells, npc, mob, songs, items):
    data["Zoom_rect"].x = max(0, min(data["Zoom_rect"].x, data["Image_rect"].width - data["Zoom"][0]))
    data["Zoom_rect"].y = max(0, min(data["Zoom_rect"].y, data["Image_rect"].height - data["Zoom"][1]))
    I.info.Player_rect = I.pg.Rect(148 + I.info.OFFSCREEN[0] / 4, 80 + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 60)  # Player rect (if it gets hit with other rect. colide is set to True
    removable_list = []
    collide = [False]
    sub_image = data["Image"].subsurface(data["Zoom_rect"]).copy()
    new_subimage = I.pg.Surface([data["Zoom_rect"][2], data["Zoom_rect"][3]], I.pg.SRCALPHA, 32).convert_alpha()
    sub_image = (sub_image, new_subimage)
    if mob != {}:
        collide = handle_mob_visualisation(collide, sub_image, data, mob, gifs, songs, decorations, items, rooms, spells)

    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
        collide = handle_outside_display(data, decorations, removable_list, items, spells, npc, screen, clock, gifs, rooms, collide, sub_image, mob, songs)
    else:
        sub_image = (screen, screen)
        door = render_house(sub_image[0], data, rooms)
        collide = handle_interior_visualisation(decorations, sub_image[0], data, gifs)
        house_border_rect = interior_border_rect(S.SCREEN_WIDTH * 0.1, S.SCREEN_HEIGHT * 0.05, S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.85, decorations)
        # I.T.Make_rect_visible(screen, house_border_rect[0], "green")
        # I.T.Make_rect_visible(screen, house_border_rect[1], "green")
        # I.T.Make_rect_visible(screen, house_border_rect[2], "green")
        # I.T.Make_rect_visible(screen, house_border_rect[3], "green")
        me = I.pg.Rect(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 25 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 10 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 22, S.SCREEN_HEIGHT / 8)
        handle_stepping_on_rect(me, door, data, sub_image[0], clock, spells, "Return", rooms, npc)
        collide = handle_stepping_on_rect(me, house_border_rect, data, 0, 0, collide, "Collide_list", rooms, decorations)

    collide = handle_death_visualisation(sub_image[0], data, gifs, collide, decorations)

    collide = display_bacground_decor(sub_image[0], decorations, data, collide)

    cast_spell_handle(sub_image[0], data, spells, gifs, mob, songs, decorations, items, rooms)

    display_folower(sub_image[0], gifs, data, decorations, mob, items)

    handle_tutorial(sub_image, data, screen, npc, items, decorations, gifs, rooms, clock)

    scaled_image = I.pg.transform.scale(sub_image[0], data["Window size"])
    screen.blit(scaled_image, (0, 0))

    dx, dy = Play.keypress_handle(screen, data, songs, items, spells, gifs, rooms, clock)

    if S.GOD_MODE:
        collide = (0, 0)
    Play.walking(dx, dy, collide, data, decorations, sub_image[1], rooms, screen)
    display_strikes(screen, gifs, 0)

    display_char(dx, dy, screen, gifs, data, decorations)

    if gifs["Level up"].start_gif:
        frame = gifs["Level up"].next_frame(1)
        rect = frame.get_rect()
        # I.T.Make_rect_visible(screen, I.pg.Rect(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + I.info.OFFSCREEN[1], rect.w * 2, rect.h * 2), "red")
        frame = I.pg.transform.scale(frame, (rect.w * 4, rect.h * 4))
        screen.blit(frame, [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 10 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 10 * 2 + I.info.OFFSCREEN[1]])

    display_strikes(screen, gifs, 1)

    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
        scaled_image = I.pg.transform.scale(sub_image[1], data["Window size"])
        screen.blit(scaled_image, (0, 0))

    if data["Player"]["dead"] and collide[0] == "mob":  # dont hit mobs when u dead
        collide = False, 0, 0, 0

    if removable_list != []:
        for option, id in removable_list:
            del decorations.decor_dict[option][id]

    handle_map_walk(data, rooms, screen, clock, spells, npc)

    return collide

def handle_giant_tree(name, decorations, rect, sub_image, collide):
    adjusted_rect = I.pg.Rect(rect.x, rect.y + rect.h * 0.75, rect.w, rect.h * 0.15)
    second_rect = I.pg.Rect(rect.x + rect.w * 0.35, rect.y + rect.h * 0.5, rect.w * 0.3, rect.h * 0.3)
    # I.T.Make_rect_visible(sub_image[0], second_rect, "red")
    # I.T.Make_rect_visible(sub_image[0], adjusted_rect, "blue")
    decorations.displayed_rects.append(second_rect)
    if I.info.Player_rect.colliderect(second_rect):
        collide = (name, adjusted_rect)
    return collide, adjusted_rect
def handle_map_walk(data, rooms, screen, clock, spells, npc):
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

            rooms.select_room(name)
            I.info.CURRENT_ROOM = {"name": name, "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": "Village"}
            if I.info.DEATH_SAVE != 0:
                I.info.DEATH_SAVE = I.info.DEATH_SAVE[0], I.info.DEATH_SAVE[1], I.info.DEATH_SAVE[2], I.info.DEATH_SAVE[3], I.info.DEATH_SAVE[4],  1
            update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt",data["Player"], spells.selected_spell, npc)

            Play.Start(screen, clock, rooms)







def display_decor_hp(decor, rect, sub_image):
    if decor["health"].split(",,")[1].split(",")[0] < decor["health"].split(",,")[1].split(",")[1]:
        hp_rect = (rect.x, rect.y - rect.h * 0.2, rect.w, 1)
        I.pg.draw.rect(sub_image, "red", hp_rect)
        remainder_hp = float(decor["health"].split(",,")[1].split(",")[0]) / float(decor["health"].split(",,")[1].split(",")[1])
        hp_rect = (rect.x, rect.y - rect.h * 0.2, rect.w * remainder_hp, 1)
        I.pg.draw.rect(sub_image, "green", hp_rect)


def process_decor(option, gifs, sub_image, rect, rooms, clock, screen, decor, decorations, data, spells, npc, collide, id):
    display_lower_upper_decor(option, gifs, sub_image, rect, rooms, clock, screen, decor, decorations, data, spells, npc)

    adjusted_rect = I.pg.Rect(rect.x, rect.y + rect.h / 2, rect.w, rect.h - rect.h / 2)

    if option == "Tree_SB_1":
        collide, adjusted_rect = handle_giant_tree(option, decorations, rect, sub_image, collide)


    if decorations.decor_dict[option]["type"] == "House":
        adjusted_rect = I.pg.Rect(rect.x, rect.y + rect.h / 2, rect.w, rect.h - rect.h / 2 - 1)

    if decor["image"].get_rect().h == adjusted_rect.h:
        adjusted_rect = I.pg.Rect(adjusted_rect.x, adjusted_rect.y - adjusted_rect.h, adjusted_rect.w,
                                  adjusted_rect.h * 2)
    display_decor_hp(decor, rect, sub_image)

    if "Wave" not in option:
        decorations.displayed_rects.append(adjusted_rect)  # Add to the list of displayed rectangles

    if I.info.Player_rect.colliderect(adjusted_rect):
        if option in I.info.HARVESTABLE:
            collide = (option, id)
        else:
            collide = (option, adjusted_rect)

    return collide


def handle_outside_display(data, decorations, removable_list, items, spells, npc, screen, clock, gifs, rooms, collide, sub_image, mob, songs):


    # I.T.Make_rect_visible(sub_image[0], I.info.Player_rect, "red")

    decorations.displayed_rects = []  # List to keep track of displayed rectangles
    decorations.displayed_rects_full = []  # List to keep track of displayed rectangles

    decor_options = decorations.decor_dict.keys()
    #{'action': 'AXE:Light Wood', 'health': 'True,,15,15', 'type': 'Nature', 'path': 'static/images/Background/Trees/Tree_M_3.png', 0: {'name': 'Tree_M_3', 'id': 0, 'image': <Surface(28x44x32 SW)>, 'rect': <rect(45, 517, 28, 44)>, 'effect': '', 'health': 'True,,15,15'}, 1: {'name': 'Tree_M_3', 'id': 1, 'image': <Surface(28x44x32 SW)>, 'rect': <rect(30, 558, 28, 44)>, 'effect': '', 'health': 'True,,15,15'}, 2: {'name': 'Tree_M_3', 'id': 2, 'image': <Surface(28x44x32 SW)>, 'rect': <rect(28, 700, 28, 44)>, 'effect': '', 'health': 'True,,15,15'}, 3: {'name': 'Tree_M_3', 'id': 3, 'image': <Surface(28x44x32 SW)>, 'rect': <rect(71, 759, 28, 44)>, 'effect': '', 'health': 'True,,15,15'}, 4: {'name': 'Tree_M_3', 'id': 4, 'image': <Surface(28x44x32 SW)>, 'rect': <rect(103, 802, 28, 44)>, 'effect': '', 'health': 'True,,15,15'}, 5: {'name': 'Tree_M_3', 'id': 5, 'image': <Surface(28x44x32 SW)>, 'rect': <rect(173, 848, 28, 44)>, 'effect': '', 'health': 'True,,15,15'}, 6: {'name': 'Tree_M_3', 'id': 6, 'image': <Surface(28x44x32 SW)>, 'rect': <rect(74, 854, 28, 44)>, 'effect': '', 'health': 'True,,15,15'}, 7: {'name': 'Tree_M_3', 'id': 7, 'image': <Surface(28x44x32 SW)>, 'rect': <rect(221, 869, 28, 44)>, 'effect': '', 'health': 'True,,15,15'}, 8: {'name': 'Tree_M_3', 'id': 8, 'image': <Surface(28x44x32 SW)>, 'rect': <rect(80, 876, 28, 44)>, 'effect': '', 'health': 'True,,15,15'}, 9: {'name': 'Tree_M_3', 'id': 9, 'image': <Surface(28x44x32 SW)>, 'rect': <rect(211, 894, 28, 44)>, 'effect': '', 'health': 'True,,15,15'}, 10: {'name': 'Tree_M_3', 'id': 10, 'image': <Surface(28x44x32 SW)>, 'rect': <rect(372, 923, 28, 44)>, 'effect': '', 'health': 'True,,15,15'}, 11: {'name': 'Tree_M_3', 'id': 11, 'image': <Surface(28x44x32 SW)>, 'rect': <rect(150, 965, 28, 44)>, 'effect': '', 'health': 'True,,15,15'}}

    update_decor_dict(decorations, gifs)

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
            # print(decorations.decor_dict[option])

            if int(decor["health"].split(",,")[1].split(",")[0]) == 0:  # if decor is without health dont display it.
                removable_list.append((option, id))
                I.TB.handle_axe_rewards(decorations, option, items)
                continue

            I.TB.handle_axe_chopping(rect, option, decorations.decor_dict, id, items)

            I.TB.handle_picaxe_chopping(rect, option, decorations.decor_dict, id, items)

            # Check and process decorations in the upper part of the screen
            if decor_y - rect.h / 2 <= 79 + I.info.OFFSCREEN[1] / 4:
                collide = process_decor(option, gifs, sub_image[0], rect, rooms, clock, screen, decor, decorations, data, spells, npc, collide, id)

            if decor_y + rect.h / 2 >= 84 + I.info.OFFSCREEN[1] / 4:
                collide = process_decor(option, gifs, sub_image[1], rect, rooms, clock, screen, decor, decorations, data, spells, npc, collide, id)
                # if mob != {}:
                #     collide = handle_mob_visualisation(collide, sub_image, data, mob, gifs, songs, decorations, items, 1)

            collide = handle_dam_border(rooms, data, sub_image, decorations, collide)
            # I.T.Make_rect_visible(sub_image[0], rect, "green")


            if collide[0] != False and "Wave" in collide[0]:
                collide = [False]

    return collide

def handle_dam_border(rooms, data, sub_image, decorations, collide):
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

        # x1 = 0 - data["Zoom_rect"].x
        # y1 = 308 - data["Zoom_rect"].y
        # x2 = 470 - data["Zoom_rect"].x
        # y2 = 415 - data["Zoom_rect"].y
        # # border8 = I.pg.draw.line(sub_image[0], "red", (x1, y1), (x2, y2))
        # z1 = 510 - data["Zoom_rect"].x
        # c1 = 428 - data["Zoom_rect"].y
        # z2 = 1000 - data["Zoom_rect"].x
        # c2 = 578 - data["Zoom_rect"].y
        # border9 = I.pg.draw.line(sub_image[0], "red", (z1, c1), (z2, c2))
        # decorations.displayed_rects.append(border8)
        # decorations.displayed_rects.append(border9)
        # I.T.Make_rect_visible(sub_image[0], border8, "red")
        # I.T.Make_rect_visible(sub_image[0], border9, "red")
        # if Ff.rect_intersects_line(I.info.Player_rect, x1, y1, x2, y2):
        #     # print("collide")
        #     collide = "border", "line"

        rect_list = [border1, border2, border3, border4, border5, border6, border7, border8, border9, border10, border11, border12, border13]
        collide_id = I.info.Player_rect.collidelistall(rect_list)
        if collide_id != []:
            # print(collide_id)
            collide = ("border", rect_list[collide_id[0]])

    return collide

def level_up(player, gifs):
    exp = exp_till_lvup(player)
    if player["Experience"] >= exp:
        player["Experience"] = 0
        player["Level"] = 1 + int(player["Level"])
        player["hp"] = player["hp"][1], player["hp"][1]
        player["mana"] = player["mana"][1], player["mana"][1]
        gifs["Level up"].Start_gif("Level up", [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2, S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7])

def update_decor_dict(decorations, gifs):
    if I.info.MAP_CHANGE.get(I.info.CURRENT_ROOM["name"]) != None and I.info.MAP_CHANGE[I.info.CURRENT_ROOM["name"]].get("add") != None:
        for option in I.info.MAP_CHANGE[I.info.CURRENT_ROOM["name"]]["add"].keys():
            if decorations.decor_dict.get(option) != None:
                for decor in I.info.MAP_CHANGE[I.info.CURRENT_ROOM["name"]]["add"][option]:
                    if decorations.decor_dict[option].get(decor[0]) == None:
                        path = decorations.decor_dict[option]["path"]
                        health = decorations.decor_dict[option]["health"]
                        image = I.pg.image.load(path).convert_alpha()
                        img_rect = image.get_rect(topleft=(decor[1][0], decor[1][1]))
                        decorations.decor_dict[option][decor[0]] = {"name": option, "id": decor[0], "image": image, "rect": img_rect, "effect": "", "health": health}
            else:
                """decoration doesn't exist in decor_dict, creating key"""
                old_name_split = option.split("_")
                old_name = old_name_split[0] + "_" + old_name_split[1] + "_" + old_name_split[2]
                if decorations.decor_dict.get(old_name) != None:
                    """old name exists, using it's data"""
                    decor_data = decorations.decor_dict[old_name]
                    new_path = decor_data["path"].replace(".png", "")
                    new_path += "_" + old_name_split[3] + ".png"
                    decorations.decor_dict[option] = {
                        'action': decor_data["action"],
                        'health': decor_data["health"],
                        'type': decor_data["type"],
                        'path': new_path}
    if I.info.MAP_CHANGE.get(I.info.CURRENT_ROOM["name"]) != None and I.info.MAP_CHANGE[I.info.CURRENT_ROOM["name"]].get("remove") != None:
        for option in I.info.MAP_CHANGE[I.info.CURRENT_ROOM["name"]]["remove"].keys():
            for id in I.info.MAP_CHANGE[I.info.CURRENT_ROOM["name"]]["remove"][option]:
                if decorations.decor_dict[option].get(id) != None:
                    del decorations.decor_dict[option][id]
        I.info.MAP_CHANGE[I.info.CURRENT_ROOM["name"]]["remove"] = {}
    if I.info.MAP_CHANGE.get("remove_gif") != None:
        for gif_name in I.info.MAP_CHANGE["remove_gif"]:
            if gifs[gif_name].repeat == 1:
                gifs[gif_name].start_gif = False
                del decorations.decor_dict[gif_name][0]
                I.info.MAP_CHANGE["remove_gif"].pop(0)



def display_bacground_decor(sub_image, decorations, data, collide):
    for option in decorations.decor_dict.keys():
        if "WALK" in decorations.decor_dict[option]["action"]:
            for id in decorations.decor_dict[option].keys():
                if isinstance(id, int):
                    decor = decorations.decor_dict[option][id]
                    decor_x = decor["rect"].x - data["Zoom_rect"].x
                    decor_y = decor["rect"].y - data["Zoom_rect"].y

                    rect = I.pg.Rect(decor_x, decor_y, decor["rect"].w, decor["rect"].h)
                    # print(decor)

                    size = decor["image"].get_rect()
                    decor["image"] = I.pg.transform.scale(decor["image"], (size.w, size.h))
                    sub_image.blit(decor["image"], (rect.x, rect.y))

                    if I.info.Player_rect.colliderect(rect):
                        collide = [option, id]
    return collide


def closest_mob(mob_class, current_pos, name):
    final_distance = 99999
    target_pos = 0,0
    target = ""
    i = 0
    for key in mob_class.keys():
        for id in mob_class[key].mobs:
            mob_rect = id["current_pos"]
            distance = ((current_pos.x - mob_rect.x) ** 2 + (current_pos.y - mob_rect.y) ** 2) ** 0.5
            if name != key.replace(" Mine", ""):
                if final_distance > distance:
                    final_distance = int(distance)
                    target_pos = mob_rect.x, mob_rect.y
                    target = key, i, mob_rect
            i += 1
        i = 0
    return target_pos, target
