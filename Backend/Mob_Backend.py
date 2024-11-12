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

def generate_mobs(mob, background_size):
    mob_gif_count = Ff.count_png_files(mob.path)
    mob.spawn_mobs(background_size, mob.path, mob_gif_count)
    return mob.mobs

def handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob, items, rooms):
    rects = {"Sword": I.info.COMBAT_RECT[0],
             "Axe": I.info.AXE[0],
             "Picaxe": I.info.PICAXE[0]
             }
    weapon_data = [1, 1, 1, "Blunt"]
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
            if "Shovel" in weapon[0]:
                I.info.WALKING_ON = "Mob"
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
    for key in gifs.keys():
        if gifs[key].start_gif and current_mob == gifs[key].rect:
            if current_mob["effect"].get(key) != None:
                duration = current_mob["effect"][key]
                frame = gifs[key].next_frame(duration)
                if current_mob["effect"]["Fire"] != 0:
                    gifs["Cold"].start_gif = False
                    gifs["Cold"].repeat = 0
                    mob.deal_damage(current_mob, data["Player"], "effect_" + key, items, gifs, rooms, data)
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

            if data_to_remove != [] and not gifs["effect"].start_gif: # REMOVES BURNED DECOR
                for index in data_to_remove:
                    del decorations.effected_decor[index]

def handle_mob_speed(data, current_mob, decorations, mob, mob_dict, items, gifs, spells, rooms):

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
                    mob_dict[target[0]].deal_damage(mob_dict[target[0]].mobs[target[1]], data["Player"], spells.spell_dict["Spawn " + mob.name], items, gifs, rooms, data)

            mob.update_position(mob_rect.x, mob_rect.y, current_mob)  # UPDATE THE POSSISIONS OF THE MOB

        elif not data["Player"]["dead"] and current_mob["allignment"] == 2:
            I.GB.guard_allignment_2_handle(current_mob, decorations, mob, target_pos, data)
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

def handle_mob_respawn(mob, data, rooms):
    if rooms.type in ["Village"]:
        # print("mob: ", mob)
        for monster_name in mob.keys():
            if mob[monster_name].count[0] < mob[monster_name].count[1]:
                mob[monster_name].count = (mob[monster_name].count[0] + 1, mob[monster_name].count[1])
                id = mob[monster_name].count[1] + 1
                mob[monster_name].mobs.append(mob[monster_name].create_mob(id))
                data[mob[monster_name].name] = generate_mobs(mob[monster_name], data["Image_rect"].size)

