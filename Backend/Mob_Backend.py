from random import random, randint
from turtledemo.forest import tree

from utils import Imports as I, Frequent_functions as Ff

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

def update_mob_health(rect, current_mob, sub_image):
    if current_mob["hp"][0] < current_mob["hp"][1]:
        health_bar = I.pg.Rect(rect.x, rect.y, rect.w, 1)
        I.pg.draw.rect(sub_image, "red", health_bar)
        health = current_mob["hp"]
        remainder = health[0] / health[1]
        reduced_health_bar = I.pg.Rect(rect.x, rect.y, rect.w * remainder, 1)
        I.pg.draw.rect(sub_image, "green", reduced_health_bar)

def generate_mobs(mob, background_size, gifs):
    mob_gif_count = Ff.count_png_files(mob.path)
    mob.spawn_mobs(background_size, mob.path, mob_gif_count, gifs)
    return mob.mobs

def handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items, rooms):
    rects = {"Sword": I.info.COMBAT_RECT[0],
             "Axe": I.info.AXE[0],
             "Picaxe": I.info.PICAXE[0]
             }
    for key, r in rects.items():
        if r != 0:
            button_pressed = key
            damage_type = "Blunt"
            weapon = I.info.EQUIPED[button_pressed]
            if weapon[0] != 0 and rects[key] != 0:
                """Equiped weapon"""
                weapon_data = Ff.get_property(weapon[0], items, "WEAPON")
                damage_type = weapon_data[3]
            else:
                """using hands"""
                weapon_data = [1, 1, 1, "Blunt"]

            if any(r != 0 and r.colliderect(rect) and not gifs[damage_type].start_gif for r in rects.values()):
            # if I.info.COMBAT_RECT[0] != 0 and I.info.COMBAT_RECT[0].colliderect(rect) and not gifs[damage_type].start_gif:
                if weapon[1] == 27:
                    curr_song = song["Playing"]
                    effect = song[curr_song].generate_thump_sound()
                    song[curr_song].play_effect(effect)
                    gifs[damage_type].Start_gif(damage_type, current_mob)
                    if weapon[0] != 0 and "Shovel" in weapon[0]:
                        I.info.WALKING_ON = "Mob"
                    """Makes sure that the attack occurs only once"""
                    if weapon[0] == 0:
                        """if you are bare handed then also attack only once"""
                        I.info.EQUIPED[key] = weapon[0], weapon[1] - 1
                    if weapon_data[3] == "Blunt":
                        data["Player"]["stats"]["Bashing"] = int(data["Player"]["stats"]["Bashing"]) + int(weapon_data[0])
                    else:
                        data["Player"]["stats"][weapon_data[3]] = int(data["Player"]["stats"][weapon_data[3]]) + int(weapon_data[0])

                    mob.deal_damage(current_mob, data["Player"], weapon_data, items, gifs, rooms, data)
                    if "Guard" in mob.name:
                        I.info.CRIMINAL = {
                                "Charge": "Assault",
                                "Fine": 100,
                                "Prison_time": 180
                            }
                    if current_mob["hp"][0] > 0:
                        I.FB.set_follower_mob_target(current_mob, mob)

def handle_damage_type_visualisation(sub_image, current_mob, gifs, pos, data, mob, decorations, items, rooms):
    for key in ["Force", "Fire", "Cold", "Necrotic", "Slashing", "Blunt", "Piercing"]:
        if gifs[key].start_gif and current_mob == gifs[key].rect:
            """when assigning rect cuz of mob hit we use the rect to store the current mob dict"""
            if current_mob["effect"].get(key) != None:
                """Magic effect"""
                duration = current_mob["effect"][key]
                frame = None
                if current_mob["effect"][key] != 0:
                    frame = gifs[key].next_frame(duration)
                if current_mob["effect"]["Fire"] != 0:
                    current_mob["effect"]["Cold"] = 0
                    mob.deal_damage(current_mob, data["Player"], "effect_" + key, items, gifs, rooms, data)
                if current_mob["effect"]["Cold"] != 0:
                    current_mob["effect"]["Fire"] = 0
                    """freeze mob"""
                    current_mob["speed"] = (current_mob["speed"][0], 999)
                if gifs[key].frame_changed and gifs[key].current_frame == gifs[key].frame_count and gifs[key].repeat == duration:
                    current_mob["effect"][key] = 0
                    gifs[key].repeat = 0
            else:
                """Physical effect"""
                frame = gifs[key].next_frame(1) # made specifically for damage displaying on mobs displays piercing, blunt

            if frame != None:
                sub_image.blit(frame, (pos[0], pos[1]))
            if current_mob["effect"]["Cold"] == 0 and current_mob["speed"][1] == 998:
                current_mob["speed"] = (current_mob["speed"][0], current_mob["speed"][0])
        # elif not gifs[key].start_gif and current_mob["effect"].get(key) != None: # IF KEY IS NOT STARTED ITS GIF AND CURRENT MOB HAS THIS EFFECT ON IT
        #     if not gifs[key].start_gif and current_mob["effect"][key] != 0:
        #         current_mob["effect"][key] = 0
        #         if key == "Cold":
        #             """Reset speed with physical hit"""
        #             current_mob["speed"] = (current_mob["speed"][1], current_mob["speed"][1])

def handle_mob_speed(data, current_mob, decorations, mob, mob_dict, items, gifs, spells, rooms):

    speed = current_mob["speed"][0]  # MOB SPEED
    if current_mob["speed"][1] == 0:  # IF MOB SPEED SECOND VALUE IS SET TO 0 IT CAN MOVE
        current_mob["speed"] = speed, speed # RESET SPEED
        current_frame = current_mob["gif_frame"][0] # GET THE NEXT GIF FRAME
        target_pos = (I.info.Player_rect.x + data["Zoom_rect"].x, I.info.Player_rect.y + data["Zoom_rect"].y) # GET THE PLAYER POSSISION
        mob_rect = current_mob["rect"][current_frame] # GET THE CURRENT MOB POSSISION

        if not data["Player"]["dead"] and current_mob["allignment"] == 7:
            target_pos, target = closest_mob(mob_dict, mob_rect, mob.name)
            # mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_towards(target_pos, current_mob, speed, decorations.displayed_rects, data["Zoom_rect"]) # GET THE NEW POSISION OF THE MOB THAT IS CHASING YOU
            mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_towards_new(target_pos, mob_rect, mob, speed, current_mob) # GET THE NEW POSISION OF THE MOB THAT IS CHASING YOU
            if target != "" and target[2].colliderect(mob_rect):
                if spells.spawn_counter.get("Spawn " + mob.name) != None and mob_dict[target[0]].hp != 0:
                    mob_dict[target[0]].deal_damage(mob_dict[target[0]].mobs[target[1]], data["Player"], spells.spell_dict["Spawn " + mob.name], items, gifs, rooms, data)

            mob.update_position(mob_rect.x, mob_rect.y, current_mob)  # UPDATE THE POSSISIONS OF THE MOB

        elif not data["Player"]["dead"] and current_mob["allignment"] == 2:
            I.GB.guard_allignment_2_handle(current_mob, decorations, mob, target_pos, data)
        elif not data["Player"]["dead"] and current_mob["allignment"] in [6, 8, 9]: # IF THE PLAYER ISN'T DEAD AND THE MOB IS Neutral evil OR Chaotic neutral THEN GO TO THE PLAYER
            # mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_towards(target_pos, current_mob, speed, decorations.displayed_rects, data["Zoom_rect"]) # GET THE NEW POSISION OF THE MOB THAT IS CHASING YOU
            """Speed set at 8 is HARD to run away from without flash"""
            mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_towards_new(target_pos, mob_rect, mob, speed, current_mob) # GET THE NEW POSISION OF THE MOB THAT IS CHASING YOU
            mob.update_position(mob_rect.x, mob_rect.y, current_mob)  # UPDATE THE POSSISIONS OF THE MOB
            if current_mob["allignment"] == 8:  # IF THE ALLIGNMENT WAS Chaotic neutral AS IN ATTACKS AND THEN RUNS AWAY THEN SET THE ALLIGNMENT ACORDINGLY TO START RUNNING AWAY
                current_mob["allignment"] = 4 # MIGHT BE POORLY HANDLED I EXPECT MOBS WILL RUN AWAY THE MOMENT THEY SEE THE PLAYER INSTEAD OF ATTACKING IT FIRST


        elif not data["Player"]["dead"] and current_mob["allignment"] == 4 and current_mob["hp"][0] < current_mob["hp"][1]: # IF MOB ISN'T DEAD AND IM NOT DEAD AND THE ALLIGNMENT IS neutral good THEN RUN AWAY FROM PLAYER IF PROVOKED
            mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_away_new(target_pos, mob_rect, mob, speed, current_mob)
            # mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_away_from(target_pos, current_mob, speed, decorations.displayed_rects, data["Zoom_rect"])
            mob.update_position(mob_rect.x, mob_rect.y, current_mob)

        else: # IF NOT CHASING ME AND NOT RUNNING AWAY FROM ME THEN MOB IS NOT VISIBLE
            fake_speed = I.random.randrange(1, speed)
            mob_rect.x, mob_rect.y, i_dont_need_visibility_changes = Ff.move_towards_new(current_mob["target_posision"], mob_rect, mob, fake_speed, current_mob) # GET THE NEW POSISION OF THE MOB THAT IS CHASING YOU
            mob.update_position(mob_rect.x, mob_rect.y, current_mob)  # UPDATE THE POSSISIONS OF THE MOB
            current_mob["visible"] = False

    else:
        current_mob["speed"] = current_mob["speed"][0], current_mob["speed"][1] - 1

def hit_by_mob_walking(data, collide):
    differance = (collide[1]["current_pos"].x - data["Zoom_rect"].x, collide[1]["current_pos"].y - data["Zoom_rect"].y)
    dx, dy = ((differance[0] > 150) - (differance[0] < 150), (differance[1] > 80) - (differance[1] < 80))
    if I.info.OFFSCREEN[0] == 0:
        data["Zoom_rect"].x -= dx * 7
        data["Zoom_rect"].y -= 0
    else:
        data["Zoom_rect"].x -= 0
        data["Zoom_rect"].y -= 0
    if I.info.OFFSCREEN[1] == 0:
        data["Zoom_rect"].x -= 0
        data["Zoom_rect"].y -= dy * 7
    else:
        data["Zoom_rect"].x -= 0
        data["Zoom_rect"].y -= 0

def handle_mob_respawn(mob, data, rooms, gifs):
    if rooms.type in ["Village"]:
        # print("mob: ", mob)
        for monster_name in mob.keys():
            if mob[monster_name].count[0] < mob[monster_name].count[1]:
                mob[monster_name].count = (mob[monster_name].count[0] + 1, mob[monster_name].count[1])
                id = mob[monster_name].count[1] + 1
                mob[monster_name].mobs.append(mob[monster_name].create_mob(id))
                data[mob[monster_name].name] = generate_mobs(mob[monster_name], data["Image_rect"].size, gifs)

def check_if_mob_spawns(tree_name, decor_dict, id, gifs, tree_rect, data):
    if "MOB SPAWN" in decor_dict[tree_name]["action"]:
        word, hp = decor_dict[tree_name][id]["health"].split(",,")
        hp_left, hp_full = hp.split(",")
        if int(hp_left) == int(hp_full):
            str_id = decor_dict[tree_name]["action"].find("MOB SPAWN")
            ods = float(decor_dict[tree_name]["action"][str_id:].split(",,")[0].replace("MOB SPAWN:", ""))
            if random() < 1:
                gifs[tree_name].Start_gif(tree_name, tree_rect)
                gifs[tree_name].repeat = 0
                Ff.update_map_view(id, tree_name, tree_rect, "gif_ended")
                if (id, tree_name, tree_rect, "decor-mob:Ent") not in list(data["Queue_to_be_removed"].queue):
                    temp_rect = tree_rect.x + data["Zoom_rect"].x, tree_rect.y + data["Zoom_rect"].y, tree_rect.w, tree_rect.h
                    data["Queue_to_be_removed"].put((id, tree_name, temp_rect, "decor-mob:Ent"))

