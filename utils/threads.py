from http.cookiejar import cut_port_re

from utils import Imports as I, Frequent_functions as Ff
from Backend import Play
from Values import Settings as S

def start_threads(data, mob, spells, decorations, rooms, npc, gifs, songs, items):
    if S.THREADS:

        five_min_thread = I.threading.Thread(target=five_min, args=(npc, ))
        five_min_thread.daemon = True
        five_min_thread.start()

        day_night_thread = I.threading.Thread(target=day_night)
        day_night_thread.deamon = True
        day_night_thread.start()

        five_hundred_msec_thread = I.threading.Thread(target=five_hundred_msec, args=(songs, ))
        five_hundred_msec_thread.daemon = True
        five_hundred_msec_thread.start()

        three_hundred_msec_thread = I.threading.Thread(target=three_hundred_msec)
        three_hundred_msec_thread.daemon = True
        three_hundred_msec_thread.start()

        light_render_calculations_thread = I.threading.Thread(target=light_render_calculations, args=(rooms, decorations))
        light_render_calculations_thread.daemon = True
        light_render_calculations_thread.start()

        item_drops_thread = I.threading.Thread(target=Handle_item_drops)
        item_drops_thread.daemon = True
        item_drops_thread.start()
        S.THREADS = False

    one_sec_thread = I.threading.Thread(target=one_sec, args=(data, decorations, rooms, gifs))
    one_sec_thread.daemon = True
    one_sec_thread.start()

    ten_min_thread = I.threading.Thread(target=ten_min, args=(mob, data, rooms, gifs))
    ten_min_thread.daemon = True
    ten_min_thread.start()

    one_hundred_msec_thread = I.threading.Thread(target=one_hundred_msec, args=(mob, spells, decorations, data, gifs))
    one_hundred_msec_thread.daemon = True
    one_hundred_msec_thread.start()

    one_min_thread = I.threading.Thread(target=one_min, args=(decorations, data))
    one_min_thread.daemon = True
    one_min_thread.start()

    I.th.start_thread(5, "planting", decorations)


def start_thread(interval, case, extra):
    interval = float(interval) / 1000
    if case == "hit":
        hit_thread = I.threading.Thread(target=hit_mob, args=(interval, extra))
        hit_thread.daemon = True
        hit_thread.start()
    if case == "cook":
        cook_thread = I.threading.Thread(target=cook, args=(interval, extra))
        cook_thread.daemon = True
        cook_thread.start()
    if case == "axe":
        axe_thread = I.threading.Thread(target=axe, args=(interval, extra))
        axe_thread.daemon = True
        axe_thread.start()
    if case == "picaxe":
        picaxe_thread = I.threading.Thread(target=picaxe, args=(interval, extra))
        picaxe_thread.daemon = True
        picaxe_thread.start()
    if case == "waves":
        wave_thread = I.threading.Thread(target=waves, args=(interval, extra))
        wave_thread.daemon = True
        wave_thread.start()
    if case == "folower":
        folower_thread = I.threading.Thread(target=folower, args=(interval, extra))
        folower_thread.daemon = True
        folower_thread.start()
    elif case == "planting":
        planting_thread = I.threading.Thread(target=planting, args=(interval, extra))
        planting_thread.daemon = True
        planting_thread.start()
    elif case == "spawn":
        spawn_thread = I.threading.Thread(target=spawn, args=(interval, extra))
        spawn_thread.daemon = True
        spawn_thread.start()





def ten_min(mob, data, rooms, gifs):
    if mob != {}:
        while S.PLAY:
            I.t.sleep(600)
            I.MB.handle_mob_respawn(mob, data, rooms, gifs)


def five_min(npc):
    while S.PLAY:
        I.t.sleep(60)  # Wait for the interval time (in seconds)
        for npc_name in npc.keys():
            if npc[npc_name]["dialog"].iteration == 3 and npc_name == "Mayor":  # after some time if value is 3 sets to value 4
                I.info.QUESTS.append({'COMPLETION': 0, 'GIVER': 'God', 'TYPE': 'MEET', 'WHO': 'Mayor', 'REWARD': '1 Sp', 'DESC': 'Go to the Mayor'})
                npc[npc_name]["dialog"].iteration = 4

def one_min(decorations, data): # Fixed
    while S.PLAY:
        I.t.sleep(60)
        if int(data["Player"]["Exhaustion"][0]) > 0:
            data["Player"]["Exhaustion"] = (int(data["Player"]["Exhaustion"][0]) - 1, int(data["Player"]["Exhaustion"][1]))
        if not I.info.PAUSE_THREAD["harvest"]:
            I.PlantB.harvest_timeout(decorations)
        if "Prison" in I.info.CURRENT_ROOM["name"]:
            I.info.CRIMINAL["Prison_time"] -= 60
            if I.info.CRIMINAL["Prison_time"] <= 0:
                I.info.CRIMINAL["Prison_time"] = 0
                I.info.CRIMINAL["Charge"] = ""



def one_sec(data, decorations, rooms, gifs): # Fixed
    please_eat_flag = False

    while S.PLAY:
        I.t.sleep(1)
        """Healing player if not too exhausted"""
        if I.pg.time.get_ticks() - int(data["Player"]["Last_hit"]) > 20000 and int(data["Player"]["Exhaustion"][0]) >= 90:
            please_eat_flag = False
            if data["Player"]["hp"][0] < data["Player"]["hp"][1]:
                data["Player"]["hp"] = (data["Player"]["hp"][0] + 1, data["Player"]["hp"][1])
            if float(data["Player"]["mana"][0]) < float(data["Player"]["mana"][1]):
                data["Player"]["mana"] = (data["Player"]["mana"][0] + 1, data["Player"]["mana"][1])
        if int(data["Player"]["Exhaustion"][0]) <= 10:
            if not please_eat_flag:
                Ff.display_text_player("Too exhausted.. life draining..", 5000)
                please_eat_flag = True
            data["Player"]["hp"] = (data["Player"]["hp"][0] - 1, data["Player"]["hp"][1])
            data["Player"]["mana"] = (data["Player"]["mana"][0] - 1, data["Player"]["mana"][1])
        effects_not_supported_by_decor = ["UNLOCKED", "LOCKED", "NoPLANT", '']
        if rooms.size == ["1", "1", "1", "1"]:
            for option in rooms.decor:
                if decorations.decor_dict.get(option) != None:
                    for id in decorations.decor_dict[option].keys():
                        if isinstance(id, int):
                            decor = decorations.decor_dict[option][id]
                            # print(decor)
                            if decor["effect"] not in effects_not_supported_by_decor:
                                if "TIME" in decor["effect"] or "PLANTED" in decor["effect"]:
                                    continue
                                effect_list = decor["effect"].split(",,")
                                for e in effect_list:
                                    if e in effects_not_supported_by_decor:
                                        continue
                                    effect, time = e.split(":")
                                    # print(decorations.decor_dict[option]["health"])
                                    # print(effect, time)
                                    if "Fire" in effect:
                                        health = decorations.decor_dict[option]["health"]
                                        if "False" in health:
                                            decor["effect"] = decor["effect"].replace(e, "")
                                        else:
                                            hp_left, hp_max = decor["health"].split(",,")[1].split(",")
                                            hp_left = int(hp_left) - 1
                                            if hp_left < 0:
                                                hp_left = 0
                                            decor["health"] = "True,," + str(hp_left) + "," + str(hp_max)
                                            data["Player"]["stats"]["Arsonist"] = int(data["Player"]["stats"]["Arsonist"]) + 1

            # if decorations.effected_decor != {}:
            #     dict_to_burn = []
            #     for old_index, effect in decorations.effected_decor.items():
            #         if effect in ["Fire"]:
            #             rect = decorations.displayed_rects[old_index]
            #             for option in decorations.decor_dict.keys():
            #                 for index in decorations.decor_dict[option].keys():
            #                     if isinstance(index, int):
            #                         new_rect = I.pg.Rect(decorations.decor_dict[option][index]["rect"].x - data["Zoom_rect"].x, decorations.decor_dict[option][index]["rect"].y - data["Zoom_rect"].y, decorations.decor_dict[option][index]["rect"].w, decorations.decor_dict[option][index]["rect"].h)
            #                         if new_rect == rect:
            #                             # found the index for the decorations.decor_dict.
            #                             if "True" in decorations.decor_dict[option]["health"]:  # FOUND FLAMABLE
            #                                 # print("FOUND FLAMABLE")
            #                                 duration = decorations.decor_dict[option]["health"].split(",,")[1]
            #                                 if decorations.decor_dict[option][index]["effect"] == "":
            #                                     decorations.decor_dict[option][index]["effect"] = "Fire,," + str(duration)
            #                                 else:
            #                                     duration = int(decorations.decor_dict[option][index]["effect"].split(",,")[1].split(",")[0])
            #
            #                                     duration -= 1
            #                                     decorations.decor_dict[option][index]["effect"] = "Fire,," + str(duration)
            #                                 if duration == 0:
            #                                     dict_to_burn.append((option, index, old_index))
            #     if dict_to_burn != []:
            #         for option, index, old_index in dict_to_burn:
            #             del decorations.decor_dict[option][index]
            #             del decorations.effected_decor[old_index]

def five_hundred_msec(song): # Fixed ( works better than before, still play's music on inventory )
    while S.PLAY:
        I.t.sleep(0.5)
        song[song["Playing"]].next_note()



def three_hundred_msec(): # Fixed
    while S.PLAY:
        I.t.sleep(0.3)
        I.info.CURRENT_STANCE += 1
        if I.info.CURRENT_STANCE > 3:
            I.info.CURRENT_STANCE = 0

def one_hundred_msec(mob, spells, decorations, data, gifs): # works fine
    while S.PLAY:
        I.t.sleep(0.1)
        if I.info.CURRENT_ROOM["Mobs"]:
            for key in mob.keys():
                mob[key].delay = mob[key].delay[0] - 100, mob[key].delay[1] # remove 100 ms
                mob[key].frame_change = False
                if mob[key].delay[0] <= 0:
                    mob[key].frame_change = True
                    for current_mob in mob[key].mobs:
                        current_mob["gif_frame"] = (current_mob["gif_frame"][0] + 1, current_mob["gif_frame"][1])
                        if current_mob["gif_frame"][0] >= current_mob["gif_frame"][1]:
                            current_mob["gif_frame"] = (0, current_mob["gif_frame"][1])
                            current_mob["target_posision"] = current_mob["current_pos"][0] + Ff.weighted_random(), current_mob["current_pos"][1] + Ff.weighted_random()
                            # mob[key].move_mobs_randomly(decorations, data)
                    mob[key].delay = mob[key].delay[1], mob[key].delay[1]

        for key in spells.spell_cooloff.keys():
            if spells.spell_cooloff[key] != 0 and not gifs[key].start_gif:
                spells.spell_cooloff[key] -= 1

def hit_mob(interval, gifs): # Fixed
    while S.PLAY:
        while S.PLAY:
            if I.info.EQUIPED["Sword"][0] == 0:
                """if equiped is nothing basicly using hands"""
                I.t.sleep(interval)
                if I.info.EQUIPED["Sword"][1] <= 26:
                    I.info.EQUIPED["Sword"] = I.info.EQUIPED["Sword"][0], 27
                break
            else:
                """if hit was done and reseting weapon"""
                if I.info.EQUIPED["Sword"][1] <= 26:
                    I.info.EQUIPED["Sword"] = I.info.EQUIPED["Sword"][0], I.info.EQUIPED["Sword"][1] - 1
                I.t.sleep(interval/26)
                if I.info.EQUIPED["Sword"][1] == 0:
                    I.info.EQUIPED["Sword"] = I.info.EQUIPED["Sword"][0], 27
                    break
        I.info.COMBAT_RECT = [0, 0]
        I.info.WALKING_ON = None
        if I.info.POS_CHANGE[1] != 0:
            gifs[I.info.POS_CHANGE[1]].start_gif = False
            I.info.POS_CHANGE = 0, 0
        break


def cook(interval, extra):
    items, rooms, data = extra
    while S.PLAY:
        I.t.sleep(interval)
        I.AB.handle_cooking_food(items, rooms, data)
        break

def axe(interval, gifs): # Fixed
    while S.PLAY:
        while S.PLAY:
            if I.info.EQUIPED["Axe"][1] <= 26:
                I.info.EQUIPED["Axe"] = I.info.EQUIPED["Axe"][0], I.info.EQUIPED["Axe"][1] - 1
            I.t.sleep(interval / 26)
            if I.info.EQUIPED["Axe"][1] == 0:
                I.info.EQUIPED["Axe"] = I.info.EQUIPED["Axe"][0], 27
                break
        I.info.AXE = [0, 0]
        I.info.WALKING_ON = None
        if I.info.POS_CHANGE[1] != 0:
            gifs[I.info.POS_CHANGE[1]].start_gif = False
            gifs[I.info.POS_CHANGE[1].replace(" Strike", "")].start_gif = False
            I.info.POS_CHANGE = 0, 0
        break

def picaxe(interval, gifs): # Fixed
    while S.PLAY:
        while S.PLAY:
            if I.info.EQUIPED["Picaxe"][1] <= 26:
                I.info.EQUIPED["Picaxe"] = I.info.EQUIPED["Picaxe"][0], I.info.EQUIPED["Picaxe"][1] - 1
            I.t.sleep(interval / 26)
            if I.info.EQUIPED["Picaxe"][1] == 0:
                I.info.EQUIPED["Picaxe"] = I.info.EQUIPED["Picaxe"][0], 27
                break
        I.info.PICAXE = [0, 0]
        I.info.WALKING_ON = None
        if I.info.POS_CHANGE[1] != 0:
            gifs[I.info.POS_CHANGE[1]].start_gif = False
            gifs[I.info.POS_CHANGE[1].replace(" Strike", "")].start_gif = False
            I.info.POS_CHANGE = 0, 0
        break

def waves(interval, gifs): # Fixed
    while S.PLAY:
        I.t.sleep(interval)
        for key in gifs.keys():
            if "Wave1" in key or "Wave4" in key:
                gifs[key].pause = 0
        break
        # I.pg.time.set_timer(I.pg.USEREVENT + 11, 0)

def folower(interval, data): # Fixed
    while S.PLAY:
        I.t.sleep(interval)
        x_init = 148 + data["Zoom_rect"].x + int(I.info.OFFSCREEN[0] / 4)
        y_init = 72 + data["Zoom_rect"].y + int(I.info.OFFSCREEN[1] / 4)
        range = 50
        x = I.random.randrange(x_init - range, x_init + range)
        y = I.random.randrange(y_init - range, y_init + range)
        I.info.FOLLOWER["target_pos"] = x, y
        I.info.FOLLOWER["orientation"] = []

def spawn(interval, extra):
    spells, mobs = extra
    while S.PLAY:
        I.t.sleep(interval)
        mob_name = list(spells.spawn_counter.keys())[0].replace("Spawn ", "")
        # mob_count = list(spells.spawn_counter.values())[0]
        del mobs[mob_name + " Mine"]
        spells.spawn_counter = {}
        break

def day_night():
    """ Toggle day/night cycle """
    value = 1
    while S.PLAY:
        I.t.sleep(2)
        I.info.DIM += value
        if I.info.DIM >= 240:  # set to 240 so it wouldn't get black
            value = -1
            I.t.sleep(10)
        if I.info.DIM <= 1:
            value = 1
            I.t.sleep(10)

def light_render_calculations(rooms, decorations):
    light_source_exists = False
    while S.PLAY:
        for decoration in rooms.decor:
            if decorations.decor_dict.get(decoration) != None and "LIGHT SOURCE" in decorations.decor_dict[decoration]["action"]:
                radius = decorations.decor_dict[decoration]["action"].find("LIGHT SOURCE")
                radius = int(decorations.decor_dict[decoration]["action"][radius:].split(",,")[0].split(":")[1])
                radius_2 = int(radius * 0.5)
                light_source_exists = True

                if rooms.type not in ["House", "Prison"]:
                    radius = int(radius / 4)
                    radius_2 = int(radius / 4)

                I.info.LIGHT[0] = Ff.create_light_mask(radius_2, (10, 10, 10))
                I.info.LIGHT[1] = Ff.create_light_mask(radius, (20, 20, 20))
        I.t.sleep(0.1)
    if not light_source_exists:
        I.t.sleep(1)

# Threaded function to handle item drops
def Handle_item_drops():
    def adjust_y_sequence(y, step):
        # "up, up, down, down" sequence
        if step % 6 == 0 or step % 6 == 1 or step % 6 == 2:  # First two steps: move up by 1
            return y - 1
        elif step % 6 == 3 or step % 6 == 4 or step % 6 == 5:  # Next two steps: move down by 1
            return y + 1

    # Dictionary to track both step and current y position for each item
    item_steps = {}

    while S.PLAY:
        I.t.sleep(0.2)
        # Update y-coordinates in-place in I.IB.dropped_items
        with I.info.dropped_items_lock:
            for room, items in I.IB.dropped_items.items():
                for position, item in list(items.items()):
                    x, y = position

                    # Initialize step counter and current y position for this item if not present
                    if position not in item_steps:
                        item_steps[position] = {"step": 0, "y": y}

                    # Get the current step and y position for this item
                    step = item_steps[position]["step"]
                    current_y = item_steps[position]["y"]

                    # Calculate the new y position based on the current step
                    new_y = adjust_y_sequence(current_y, step)

                    # Define the new position and update in I.IB.dropped_items
                    new_position = (x, new_y)
                    items.pop(position)  # Remove the old position
                    items[new_position] = item  # Add the item with the new position

                    # Update `item_steps`: remove the old key and add the new one
                    item_steps.pop(position)  # Remove old entry
                    item_steps[new_position] = {"step": step + 1, "y": new_y}  # Update step count and y position


def planting(interval, decorations):
    """currently interval holds time value in ms, so if time was set for 240 seconds, it became ms"""
    interval = 20
    """set the interval to 20 seconds so that all diferent seed times could be done, currently only working with 240 s"""
    while S.PLAY:
        remove_list = []
        for plant_name, plant_values in decorations.decor_dict.items():
            if "PLANT" in plant_values["action"]:
                for id in decorations.decor_dict[plant_name].keys():
                    if isinstance(id, int):
                        plant_decor = decorations.decor_dict[plant_name][id]
                        if plant_decor["effect"] != "":
                            """This decor that can hold seeds and has an effect"""
                            if "NoPLANT" in plant_decor["effect"] and "PLANTED" in plant_decor["effect"]:
                                plant_decor["effect"].replace("NoPlant", "")
                            elif "NoPLANT" in plant_decor["effect"]:
                                remove_list = I.PlantB.remove_not_seeded_beds(plant_decor, remove_list, plant_name, id)
                            elif "NoPlant" not in plant_decor["effect"] and "PLANTED" in plant_decor["effect"]:
                                """ONLY SEEDED BEDS HERE"""
                                state, plant, time, full_time = plant_decor["effect"].split(":")
                                if state == "PLANTED_0":
                                    """initial seedling drop and state change"""
                                    Ff.update_map_view(id, plant_name, plant_decor["effect"], "remove_effect")
                                    plant_decor["effect"] = ""
                                    state = state.replace("_0", "_1")
                                    new_effect = state + ":" + plant + ":" + str(I.pg.time.get_ticks()) + ":" + full_time
                                    Ff.update_map_view(id, plant_name, new_effect, "add_effect")
                                    path = decorations.decor_dict[plant_name]["path"].replace("_0", "_1")
                                    img = I.pg.image.load(path)
                                    plant_decor["image"] = img
                                elif state == "PLANTED_1" and int(int(time) + (int(full_time) / 4) * 1000 <= I.pg.time.get_ticks()):
                                    """if state has changed and time has passed, change the state again and set new timer"""
                                    Ff.update_map_view(id, plant_name, plant_decor["effect"], "remove_effect")
                                    plant_decor["effect"] = ""
                                    state = state.replace("_1", "_2")
                                    new_effect = state + ":" + plant + ":" + str(I.pg.time.get_ticks()) + ":" + full_time
                                    Ff.update_map_view(id, plant_name, new_effect, "add_effect")
                                    path = decorations.decor_dict[plant_name]["path"].replace("_0", "_2")
                                    img = I.pg.image.load(path)
                                    plant_decor["image"] = img
                                elif state == "PLANTED_2" and int(int(time) + (int(full_time) / 4) * 1000 <= I.pg.time.get_ticks()):
                                    """if state has changed and time has passed, change the state again and set new timer"""
                                    Ff.update_map_view(id, plant_name, plant_decor["effect"], "remove_effect")
                                    plant_decor["effect"] = ""
                                    state = state.replace("_2", "_3")
                                    new_effect = state + ":" + plant + ":" + str(I.pg.time.get_ticks()) + ":" + full_time
                                    Ff.update_map_view(id, plant_name, new_effect, "add_effect")
                                    path = decorations.decor_dict[plant_name]["path"].replace("_0", "_3")
                                    img = I.pg.image.load(path)
                                    plant_decor["image"] = img
                                elif state == "PLANTED_3" and int(int(time) + (int(full_time) / 4) * 1000 <= I.pg.time.get_ticks()):
                                    """final state change occured"""
                                    Ff.update_map_view(id, plant_name, plant_decor["effect"], "remove_effect")
                                    plant_decor["effect"] = ""
                                    state = state.replace("_2", "_3")
                                    count = Ff.update_map_view(0, plant, 0, "get")
                                    if decorations.decor_dict[plant].get(count) == None:
                                        Ff.update_map_view(count, plant, plant_decor["rect"], "add")
                                    else:
                                        for i in range(count, count + 1000):
                                            if decorations.decor_dict[plant].get(i) == None:
                                                Ff.update_map_view(i, plant, plant_decor["rect"], "add")
                                                break
                                    remove_list.append((plant_name, id))
                                if state == "PLANTED_1":
                                    path = decorations.decor_dict[plant_name]["path"].replace("_0", "_1")
                                    img = I.pg.image.load(path)
                                    plant_decor["image"] = img
                                elif state == "PLANTED_2":
                                    path = decorations.decor_dict[plant_name]["path"].replace("_0", "_2")
                                    img = I.pg.image.load(path)
                                    plant_decor["image"] = img
                                elif state == "PLANTED_3":
                                    path = decorations.decor_dict[plant_name]["path"].replace("_0", "_3")
                                    img = I.pg.image.load(path)
                                    plant_decor["image"] = img
                        else:
                            """this decor that can hold seeds and has no effect"""
        for (option, id) in remove_list:
            Ff.update_map_view(id, option, (0, 0, 0, 0), "remove")
            del decorations.decor_dict[option][id]
        I.t.sleep(interval)
