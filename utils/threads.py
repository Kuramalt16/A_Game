from utils import Imports as I, Frequent_functions as Ff
from Backend import Play
from Values import Settings as S

def start_threads(data, mob, spells, decorations, rooms, npc, gifs, songs, items):
    ten_min_thread = I.threading.Thread(target=ten_min, args=(mob, data, rooms))
    ten_min_thread.daemon = True
    ten_min_thread.start()

    five_min_thread = I.threading.Thread(target=five_min, args=(data, npc))
    five_min_thread.daemon = True
    five_min_thread.start()

    one_min_thread = I.threading.Thread(target=one_min, args=(decorations, ))
    one_min_thread.daemon = True
    one_min_thread.start()

    one_sec_thread = I.threading.Thread(target=one_sec, args=(data, decorations))
    one_sec_thread.daemon = True
    one_sec_thread.start()

    five_hundred_msec_thread = I.threading.Thread(target=five_hundred_msec, args=(songs, ))
    five_hundred_msec_thread.daemon = True
    five_hundred_msec_thread.start()

    three_hundred_msec_thread = I.threading.Thread(target=three_hundred_msec)
    three_hundred_msec_thread.daemon = True
    three_hundred_msec_thread.start()

    one_hundred_msec_thread = I.threading.Thread(target=one_hundred_msec, args=(mob, spells, decorations, data, gifs))
    one_hundred_msec_thread.daemon = True
    one_hundred_msec_thread.start()

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
    # elif case == "spell_cooloff":
    #     spell_cooloff_thread = I.threading.Thread(target=spell_cooloff_th, args=(interval, extra))
    #     spell_cooloff_thread.daemon = True
    #     spell_cooloff_thread.start()





def ten_min(mob, data, rooms):
    while S.PLAY:
        I.t.sleep(600)
        Play.handle_mob_respawn(mob, data, rooms)


def five_min(data, npc):
    while S.PLAY:
        I.t.sleep(10)  # Wait for the interval time (in seconds)

        data["Player"]["Exhaustion"] = (data["Player"]["Exhaustion"][0] - 1, data["Player"]["Exhaustion"][1])

        for npc_name in npc.keys():
            if npc[npc_name]["dialog"].iteration == 3 and npc_name == "Mayor":  # after some time if value is 4 sets to value 5
                print("change")
                npc[npc_name]["dialog"].iteration = 4

def one_min(decorations): # Fixed
    while S.PLAY:
        I.t.sleep(60)
        if not I.info.PAUSE_THREAD["harvest"]:
            Play.harvest_timeout(decorations)


def one_sec(data, decorations): # Fixed
    while S.PLAY:
        I.t.sleep(1)
        """Healing player if not too exhausted"""
        if I.pg.time.get_ticks() - data["Player"]["Last_hit"] > 20000 and data["Player"]["Exhaustion"][0] >= 90:
            if data["Player"]["hp"][0] < data["Player"]["hp"][1]:
                data["Player"]["hp"] = (data["Player"]["hp"][0] + 1, data["Player"]["hp"][1])
            if float(data["Player"]["mana"][0]) < float(data["Player"]["mana"][1]):
                data["Player"]["mana"] = (data["Player"]["mana"][0] + 1, data["Player"]["mana"][1])

        if I.info.CURRENT_ROOM["Type"] in ["Village"]:
            if decorations.effected_decor != {}:
                dict_to_burn = []
                for old_index, effect in decorations.effected_decor.items():
                    if effect in ["Fire"]:
                        rect = decorations.displayed_rects[old_index]
                        for option in decorations.decor_dict.keys():
                            for index in decorations.decor_dict[option].keys():
                                if isinstance(index, int):
                                    new_rect = I.pg.Rect(decorations.decor_dict[option][index]["rect"].x - data["Zoom_rect"].x, decorations.decor_dict[option][index]["rect"].y - data["Zoom_rect"].y, decorations.decor_dict[option][index]["rect"].w, decorations.decor_dict[option][index]["rect"].h)
                                    if new_rect == rect:
                                        # found the index for the decorations.decor_dict.
                                        if "True" in decorations.decor_dict[option]["health"]:  # FOUND FLAMABLE
                                            # print("FOUND FLAMABLE")
                                            duration = decorations.decor_dict[option]["health"].split(",,")[1]
                                            if decorations.decor_dict[option][index]["effect"] == "":
                                                decorations.decor_dict[option][index]["effect"] = "Fire,," + str(duration)
                                            else:
                                                duration = int(decorations.decor_dict[option][index]["effect"].split(",,")[1].split(",")[0])

                                                duration -= 1
                                                decorations.decor_dict[option][index]["effect"] = "Fire,," + str(duration)
                                            if duration == 0:
                                                dict_to_burn.append((option, index, old_index))
                if dict_to_burn != []:
                    for option, index, old_index in dict_to_burn:
                        del decorations.decor_dict[option][index]
                        del decorations.effected_decor[old_index]

def five_hundred_msec(song): # Fixed ( works better than before, still play's music on inventory )
    while S.PLAY:
        I.t.sleep(0.5)
        song[song["Playing"]].next_note()

def three_hundred_msec(): # Fixed
    while S.PLAY:
        I.t.sleep(0.4)
        I.info.CURRENT_STANCE += 1
        if I.info.CURRENT_STANCE > 3:
            I.info.CURRENT_STANCE = 0

def one_hundred_msec(mob, spells, decorations, data, gifs): # works fine
    while S.PLAY:
        I.t.sleep(0.1)
        if I.info.CURRENT_ROOM["Mobs"]:
            for key in mob.keys():
                mob[key].delay = mob[key].delay[0] - 100, mob[key].delay[1] # remove 100 ms
                if mob[key].delay[0] <= 0:
                    for current_mob in mob[key].mobs:
                        current_mob["gif_frame"] = (current_mob["gif_frame"][0] + 1, current_mob["gif_frame"][1])
                        # current_mob["gif_frame"] = ((current_mob["gif_frame"][0] + current_mob["gif_frame"][1]) % current_mob["gif_frame"][1], current_mob["gif_frame"][1])
                        # print(current_mob["gif_frame"])
                        if current_mob["gif_frame"][0] >= current_mob["gif_frame"][1]:
                            current_mob["gif_frame"] = (0, current_mob["gif_frame"][1])
                            mob[key].move_mobs_randomly(decorations, data)
                    mob[key].delay = mob[key].delay[1], mob[key].delay[1]

        for key in spells.spell_cooloff.keys():
            if spells.spell_cooloff[key] != 0 and not gifs[key].start_gif:
                spells.spell_cooloff[key] -= 1

def hit_mob(interval, gifs): # Fixed
    while True:
        while True:
            if I.info.EQUIPED["Sword"][0] == 0:
                I.t.sleep(interval)
                break
            else:
                if I.info.EQUIPED["Sword"][1] <= 26:
                    I.info.EQUIPED["Sword"] = I.info.EQUIPED["Sword"][0], I.info.EQUIPED["Sword"][1] - 1
                I.t.sleep(interval/26)
                if I.info.EQUIPED["Sword"][1] == 0:
                    I.info.EQUIPED["Sword"] = I.info.EQUIPED["Sword"][0], 27
                    break
        I.info.COMBAT_RECT = [0, 0]
        if I.info.POS_CHANGE[1] != 0:
            gifs[I.info.POS_CHANGE[1]].start_gif = False
            I.info.POS_CHANGE = 0, 0
        break


def cook(interval, items):
    while True:
        I.t.sleep(interval)
        Play.handle_cooking_food(items)
        break

def axe(interval, gifs): # Fixed
    while True:
        while True:
            if I.info.EQUIPED["Axe"][1] <= 26:
                I.info.EQUIPED["Axe"] = I.info.EQUIPED["Axe"][0], I.info.EQUIPED["Axe"][1] - 1
            I.t.sleep(interval / 26)
            if I.info.EQUIPED["Axe"][1] == 0:
                I.info.EQUIPED["Axe"] = I.info.EQUIPED["Axe"][0], 27
                break
        I.info.AXE = [0, 0]
        if I.info.POS_CHANGE[1] != 0:
            gifs[I.info.POS_CHANGE[1]].start_gif = False
            gifs[I.info.POS_CHANGE[1].replace(" Strike", "")].start_gif = False
            I.info.POS_CHANGE = 0, 0
        break

def picaxe(interval, gifs): # Fixed
    while True:
        while True:
            if I.info.EQUIPED["Picaxe"][1] <= 26:
                I.info.EQUIPED["Picaxe"] = I.info.EQUIPED["Picaxe"][0], I.info.EQUIPED["Picaxe"][1] - 1
            I.t.sleep(interval / 26)
            if I.info.EQUIPED["Picaxe"][1] == 0:
                I.info.EQUIPED["Picaxe"] = I.info.EQUIPED["Picaxe"][0], 27
                break
        I.info.PICAXE = [0, 0]
        if I.info.POS_CHANGE[1] != 0:
            gifs[I.info.POS_CHANGE[1]].start_gif = False
            gifs[I.info.POS_CHANGE[1].replace(" Strike", "")].start_gif = False
            I.info.POS_CHANGE = 0, 0
        break

def waves(interval, gifs): # Fixed
    while True:
        I.t.sleep(interval)
        for key in gifs.keys():
            if "Wave1" in key or "Wave4" in key:
                gifs[key].pause = 0
        break
        # I.pg.time.set_timer(I.pg.USEREVENT + 11, 0)

def folower(interval, data): # Fixed
    while True:
        I.t.sleep(interval)
        x_init = 148 + data["Zoom_rect"].x + int(I.info.OFFSCREEN[0] / 4)
        y_init = 72 + data["Zoom_rect"].y + int(I.info.OFFSCREEN[1] / 4)
        range = 50
        x = I.random.randrange(x_init - range, x_init + range)
        y = I.random.randrange(y_init - range, y_init + range)
        I.info.FOLLOWER["target_pos"] = x, y
        I.info.FOLLOWER["orientation"] = []

def planting(interval, decorations):
    interval = interval / 4 * 10000
    cancel = False
    update_time = []
    while not cancel:
        for option in decorations.decor_dict:
            if "PLANT" in decorations.decor_dict[option]["action"]:
                for id in decorations.decor_dict[option].keys():
                    if isinstance(id, int):
                        if decorations.decor_dict[option][id]["effect"] != "":
                            stage, plant, time, full_time = decorations.decor_dict[option][id]["effect"].split(":")
                            if "_" not in stage:
                                """ initial seed placement"""
                                decorations.decor_dict[option][id]["effect"] = str(stage) + "_1:" + str(plant) + ":" + str(time) + ":" + str(full_time)
                                # print(decorations.decor_dict[option][id])
                                path = decorations.decor_dict[option]["path"][:-5] + "1.png"
                                img = I.pg.image.load(path)
                                # print(img)
                                update_time.append((option, id))
                                decorations.decor_dict[option][id]["image"] = img
                                # print(decorations.decor_dict[option][id])
                            elif int(stage[-1]) == 1 and int(full_time) - interval / 10 == int(time):
                                """Updates seeds to grow bigger"""
                                num = int(stage[-1]) + 1
                                decorations.decor_dict[option][id]["effect"] = str(stage[:-1]) + str(num) + ":" + str(plant) + ":" + str(time) + ":" + str(full_time)
                                path = decorations.decor_dict[option]["path"][:-5] + str(num) + ".png"
                                img = I.pg.image.load(path)
                                update_time.append((option, id))
                                decorations.decor_dict[option][id]["image"] = img
                            elif int(stage[-1]) == 2 and int(full_time) - interval / 5 == int(time):
                                """Updates seeds to grow bigger"""
                                num = int(stage[-1]) + 1
                                decorations.decor_dict[option][id]["effect"] = str(stage[:-1]) + str(num) + ":" + str(plant) + ":" + str(time) + ":" + str(full_time)
                                path = decorations.decor_dict[option]["path"][:-5] + str(num) + ".png"
                                img = I.pg.image.load(path)
                                update_time.append((option, id))
                                decorations.decor_dict[option][id]["image"] = img
                            elif int(full_time) - interval / 10 * 3 == int(time):
                                """final change from seed bed to normal tree, bush, flower, vegetable"""
                                if "Tree" in plant or "Bush" in plant:
                                    """this means that the planted plant was a tree or a bush"""

                                    Ff.update_map_view(id, "Plant bed", 0, "remove")
                                    coordinates = decorations.decor_dict[option][id]["rect"]
                                    integers = [item for item in list(decorations.decor_dict[plant].keys()) if isinstance(item, int)]
                                    new_id = max(integers) + 1
                                    if "Tree" in plant:
                                        Ff.update_map_view(new_id, plant, (coordinates.x, coordinates.y - 20), "add")
                                    else:
                                        Ff.update_map_view(new_id, plant, (coordinates.x, coordinates.y), "add")
                                cancel = True
                                break
        I.t.sleep(interval)
        if update_time != []:
            for option, id in update_time:
                effect = decorations.decor_dict[option][id]["effect"].split(":")
                decorations.decor_dict[option][id]["effect"] = effect[0] + ":" + effect[1] + ":" + str(int(effect[2]) - int(interval / 10)) + ":" + str(full_time)
            update_time = []


def spawn(interval, extra):
    spells, mobs = extra
    while True:
        I.t.sleep(interval)
        mob_name = list(spells.spawn_counter.keys())[0].replace("Spawn ", "")
        mob_count = list(spells.spawn_counter.values())[0]
        del mobs[mob_name + " Mine"]
        spells.spawn_counter = {}
        break