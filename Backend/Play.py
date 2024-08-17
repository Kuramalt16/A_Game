from Render import Background_Render as br, Main_Menu_render as mr
from Values import Settings as S
from utils import Imports as I, Frequent_functions as Ff
import random
from Backend import Settings_backend as SB, Setup_pygame as SP

movement = {
    (0, 0): (0, 0),
    (1, 0): (1, 0),  # Right
    (-1, 0): (-1, 0),  # Left
    (0, 1): (0, 1),  # Down
    (0, -1): (0, -1),  # Up
    (1, -1): (1, -1),  # Right + Up
    (1, 1): (1, 1),  # Right + Down
    (-1, -1): (-1, -1),  # Left + Up
    (-1, 1): (-1, 1)  # Left + Down
}

def Start(screen, clock, rooms):

    br.get_backpack_coordinates(screen)

    decorations = I.decor.Decorations()
    gifs = I.gifs.read_db(decorations)
    items = I.items.Items()
    spells = I.Spells.Spells()

    mob = 0
    if I.info.CURRENT_ROOM["Mobs"]:
        mob = {
            "Slime_S": I.mob_data.Mob(name="Slime_S", exp=10, hp=8, allignment=5, count=10, damage=(2, "blunt"), speed=4),
            "Pig": I.mob_data.Mob(name="Pig", exp=5, hp=6, allignment=4, count=30, damage=(1, "blunt"), speed=6),
               }

    collide = [False]
    pressed = 0

    npc = I.dialog.read_db()

    data = br.Start(mob, decorations, spells, rooms, npc, items)

    br.fill_backpack(screen, data["Player"], items)
    br.update_equiped()

    I.info.LAST_ORIENTAION = (0, 0)
    songs = {"Background": I.Songs.Song("Background", I.A.background_music),
             "Ghost": I.Songs.Song("Ghost", I.A.dead_music),
             "Playing": "Background"
             }

    timers = handle_timers()
    while S.PLAY:
        for event in I.pg.event.get():
            if event.type == I.pg.QUIT:
                S.PLAY = False
            if event.type in timers.values():
                handle_timer_actions(event, timers, data, mob, spells, decorations, rooms, npc)
            if event.type == I.pg.KEYDOWN:
                pressed = handle_keydown(event, data, spells, gifs, items)
            if event.type == I.pg.KEYUP:
                pressed = handle_keyup(event, pressed, gifs, songs, screen, items, data, collide, spells, clock, rooms, npc, decorations)

        collide = br.New_Update(data, decorations, gifs, rooms, clock, screen, spells, npc, mob, songs, items)

        if S.WINDOW == "Settings":
            handle_esc_click(screen, clock)

        handle_music(songs, collide, data)

        update_display_text(screen, gifs, data, collide)

        update_char_bar(screen, data, gifs, items)

        display_spell_bar(screen, spells, gifs)

        I.pg.display.flip()
        clock.tick(I.info.TICK)



def handle_keyup(event, pressed, gifs, songs, screen, items, data, collide, spells, clock, rooms, npc, decorations):
    if event.key == pressed:
        curr_song = songs["Playing"]
        if pressed == I.pg.K_c:
            songs[curr_song].channel0.pause()
            interract(collide, data, gifs, items, screen, songs, spells, clock, rooms, npc, decorations)
            songs[curr_song].channel0.unpause()
        elif pressed == I.pg.K_x:
            I.info.COMBAT_RECT = (0, I.info.COMBAT_RECT[1])
        elif pressed == I.pg.K_ESCAPE:
            handle_esc_click(screen, clock)
        return 0

def handle_esc_click(screen, clock):
    running = True
    buttons = mr.Main_menu(screen)
    I.pg.display.flip()
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.MOUSEBUTTONDOWN:
                pos = I.pg.mouse.get_pos()
                for key, value in buttons.items():
                    if value.collidepoint(pos[0], pos[1]) and I.pg.mouse.get_pressed()[0]:
                        if key == "Main Menu":
                            Ff.button_click_render_down(screen, value, 1, S.PATHS["Empty_button_frame"])
                            Ff.display_text(screen, key, 30, (buttons[key + "_text"].left, buttons[key + "_text"].top * 1.005), "black")
                            clicked_button = key
                        elif key == "Resume Game":
                            Ff.button_click_render_down(screen, value, 1, S.PATHS["Empty_button_frame"])
                            Ff.display_text(screen, key, 30, (buttons[key + "_text"].left, buttons[key + "_text"].top * 1.005), "black")
                            clicked_button = key
                        elif key == "Settings":
                            Ff.button_click_render_down(screen, value, 1, S.PATHS["Empty_button_frame"])
                            Ff.display_text(screen, key, 30, (buttons[key + "_text"].left, buttons[key + "_text"].top * 1.005), "black")
                            clicked_button = key
                        I.pg.display.flip()
            if event.type == I.pg.MOUSEBUTTONUP:
                pos = I.pg.mouse.get_pos()
                for key, value in buttons.items():
                    if value.collidepoint(pos[0], pos[1]) and not I.pg.mouse.get_pressed()[0]:
                        if key == "Main Menu" and clicked_button == key:
                            Ff.button_click_render_down(screen, value, 0, S.PATHS["Empty_button_frame"])
                            running = False
                            S.WINDOW = ""
                            S.START_APP = True
                            SP.run_game(screen, clock)
                        elif key == "Resume Game" and clicked_button == key:
                            Ff.button_click_render_down(screen, value, 0, S.PATHS["Empty_button_frame"])
                            running = False
                            S.WINDOW = ""
                        elif key == "Settings" and clicked_button == key:
                            Ff.button_click_render_down(screen, value, 0, S.PATHS["Empty_button_frame"])
                            SB.Settings(screen)
                            running = False
                            S.WINDOW = "Settings"
                            # buttons = mr.Main_menu(screen)
                        I.pg.display.flip()
                    elif clicked_button == key:
                        Ff.button_click_render_down(screen, value, 0, S.PATHS["Empty_button_frame"])
                        Ff.display_text(screen, key, 30, (buttons[key + "_text"].left, buttons[key + "_text"].top), "black")
                        I.pg.display.flip()
                        clicked_button = ""
            if event.type == I.pg.KEYUP:
                if event.key == I.pg.K_ESCAPE:
                    running = False

def handle_keydown(event, data, spells, gifs, items):
    key_to_slot = {
        I.pg.K_a: 0,
        I.pg.K_s: 2,
        I.pg.K_d: 4,
        I.pg.K_f: 6,
        I.pg.K_g: 8
    }
    pressed = 0
    if event.key == I.pg.K_ESCAPE:
        pressed = I.pg.K_ESCAPE
    if event.key == I.pg.K_c:
        pressed = I.pg.K_c
    elif event.key == I.pg.K_x:
        if pressed != I.pg.K_x and not data["Player"]["dead"] and I.info.COMBAT_RECT[1] == 0:
            handle_combat(items)
            I.pg.time.set_timer(I.pg.USEREVENT + 4, int(I.info.COMBAT_RECT[1]))

        pressed = I.pg.K_x
    if event.key in [I.pg.K_a, I.pg.K_s, I.pg.K_d, I.pg.K_f, I.pg.K_g]:
        target_slot = key_to_slot[event.key]
        for slot, spell in spells.selected_spell.items():
            is_spell_ready = spells.spell_cooloff.get(spell) in [None, 0]
            is_target_slot = slot == target_slot
            has_enough_mana = data["Player"]["mana"][0] >= int(spells.spell_dict[spell]["mana"])
            is_gif_not_started = not gifs[spell].start_gif

            if is_spell_ready and is_target_slot:
                if is_gif_not_started and has_enough_mana:
                    gifs[spell].Start_gif(spell, 1)
                    data["Player"]["mana"] = (data["Player"]["mana"][0] - int(spells.spell_dict[spell]["mana"]), data["Player"]["mana"][1])
                else:
                    Ff.display_text_player("Not enough MANA", 3000)
    if event.key in [I.pg.K_UP, I.pg.K_DOWN, I.pg.K_LEFT, I.pg.K_RIGHT]:
        # fixes getting stuck on objects
        if I.info.OFFSCREEN[0] == 0:
            data["Zoom_rect"].x -= I.info.LAST_ORIENTAION[0] * I.info.FAST
        if I.info.OFFSCREEN[1] == 0:
            data["Zoom_rect"].y -= I.info.LAST_ORIENTAION[1] * I.info.FAST
        if I.info.OFFSCREEN[0] != 0:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0] - I.info.LAST_ORIENTAION[0] * 3 * I.info.FAST, I.info.OFFSCREEN[1])
        if I.info.OFFSCREEN[1] != 0:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0], I.info.OFFSCREEN[1] - I.info.LAST_ORIENTAION[1] * 3 * I.info.FAST)



    return pressed
def display_spell_bar(screen, spells, gifs):
    Ff.add_image_to_screen(screen, S.PLAYING_PATH["Spell_bar"], (S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.9,  S.SCREEN_WIDTH / 5,  S.SCREEN_HEIGHT / 10))
    for pos, spell in spells.selected_spell.items():
        Ff.add_image_to_screen(screen, gifs[spell].frame_paths[0], (S.SCREEN_WIDTH * 0.803 + pos * 25, S.SCREEN_HEIGHT * 0.91,  S.SCREEN_WIDTH / 25,  S.SCREEN_HEIGHT / 10))
def handle_mob_respawn(mob, data, rooms):
    if rooms.type in ["Village"]:
        print("mob: ", mob)
        for monster_name in mob.keys():
            if mob[monster_name].count[0] < mob[monster_name].count[1]:
                mob[monster_name].count = (mob[monster_name].count[0] + 1, mob[monster_name].count[1])
                id = mob[monster_name].count[1] + 1
                mob[monster_name].mobs.append(mob[monster_name].create_mob(id))
                data[mob[monster_name].name] = br.generate_mobs(mob[monster_name], data["Image_rect"].size)

def handle_timer_actions(event, timers, data, mob, spells, decorations, rooms, npc):
    if timers["Exhaustion"] == event.type:
        data["Player"]["Exhaustion"] = (data["Player"]["Exhaustion"][0] - 1, data["Player"]["Exhaustion"][1])
        for npc_name in npc.keys():
            if npc[npc_name]["dialog"].iteration == 3: # after some time if value is 4 sets to value 5
                npc[npc_name]["dialog"].iteration = 0
    if timers["Mob_respawn"] == event.type:
        handle_mob_respawn(mob, data, rooms)
    if timers["cook"] == event.type:
        if I.info.APPLIANCE_CLICK == "Furnace":
            I.info.APPLIANCE_CLICK = ""
            if I.info.Temp_variable_holder[2] == "cook":
                # print(I.info.BACKPACK_CONTENT, I.info.Temp_variable_holder)
                if I.info.Temp_variable_holder[0] + "_Cooked" in list(I.info.BACKPACK_CONTENT.keys()):
                    I.info.BACKPACK_CONTENT[I.info.Temp_variable_holder[0] + "_Cooked"] = I.info.BACKPACK_CONTENT[I.info.Temp_variable_holder[0] + "_Cooked"][0] + 1, I.info.BACKPACK_CONTENT[I.info.Temp_variable_holder[0] + "_Cooked"][1], I.info.BACKPACK_CONTENT[I.info.Temp_variable_holder[0] + "_Cooked"][2]
                else:
                    x, y = br.find_open_space()
                    I.info.BACKPACK_CONTENT[I.info.Temp_variable_holder[0] + "_Cooked"] = (1, x, y)
                    # insert_item_to_backpack(I.info.Temp_variable_holder[0] + "_Cooked", 1)
                if any(char.isdigit() for char in I.info.Temp_variable_holder[0]):
                    I.info.Temp_variable_holder[0] = I.info.Temp_variable_holder[0][:-1]
                Ff.display_text_player("Cooked " + I.info.Temp_variable_holder[0], 3000)
            else:
                if "Ashes" in list(I.info.BACKPACK_CONTENT.keys()):
                    I.info.BACKPACK_CONTENT["Ashes"] = I.info.BACKPACK_CONTENT["Ashes"][0] + 1, I.info.BACKPACK_CONTENT["Ashes"][1], I.info.BACKPACK_CONTENT["Ashes"][2]
                else:
                    x, y = br.find_open_space()
                    I.info.BACKPACK_CONTENT["Ashes"] = (1, x, y)
                    # insert_item_to_backpack("Ashes", 1)
                Ff.display_text_player("Burned " + I.info.Temp_variable_holder[0], 3000)
            I.info.Temp_variable_holder = []
    if timers["Harvest"] == event.type:
        harvest_timeout()
    if timers["Walk"] == event.type:
        I.info.CURRENT_STANCE += 1
        if I.info.CURRENT_STANCE > 3:
            I.info.CURRENT_STANCE = 0
    if timers["mob_gif"] == event.type:
        I.info.COMBAT_RECT = (0, I.info.COMBAT_RECT[1]) # when holding down key [X] it wont stay in {Attacked} posision for too long
        if I.info.CURRENT_ROOM["Mobs"]:
            for key in mob.keys():
                for current_mob in mob[key].mobs:
                    current_mob["gif_frame"] = (current_mob["gif_frame"][0] + 1, current_mob["gif_frame"][1])
                    if current_mob["gif_frame"][0] == current_mob["gif_frame"][1]:
                        mob[key].move_mobs_randomly(decorations, data)
                        current_mob["gif_frame"] = (0, current_mob["gif_frame"][1])
        for key in spells.spell_cooloff.keys():
            if spells.spell_cooloff[key] != 0:
                spells.spell_cooloff[key] -= 1
    if timers["healing"] == event.type:
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
                                        if "True" in decorations.decor_dict[option]["flamable"]:
                                            duration = decorations.decor_dict[option]["flamable"].split(",,")[1]
                                            if decorations.decor_dict[option][index]["effect"] == "":
                                                decorations.decor_dict[option][index]["effect"] = "Fire,," + str(duration)
                                            else:
                                                duration = int(decorations.decor_dict[option][index]["effect"].split(",,")[1])
                                                duration -= 1
                                                decorations.decor_dict[option][index]["effect"] = "Fire,," + str(duration)
                                            if duration == 0:
                                                dict_to_burn.append((option, index, old_index))
                if dict_to_burn != []:
                    for option, index, old_index in dict_to_burn:
                        del decorations.decor_dict[option][index]
                        del decorations.effected_decor[old_index]
    if timers["hit"] == event.type:
        I.info.COMBAT_RECT = (I.info.COMBAT_RECT[0], 0)

def handle_timers():
    timers = {}
    EXHAUSTION_TIM = I.pg.USEREVENT + 1
    I.pg.time.set_timer(EXHAUSTION_TIM, 300000) # 5 min
    timers["Exhaustion"] = EXHAUSTION_TIM

    Mob_Respawn = I.pg.USEREVENT + 2
    I.pg.time.set_timer(Mob_Respawn, 600000) # 10 min
    timers["Mob_respawn"] = Mob_Respawn

    Harvest_timer = I.pg.USEREVENT + 3
    I.pg.time.set_timer(Harvest_timer, 60000) # 1 min
    timers["Harvest"] = Harvest_timer

    timers["hit"] = I.pg.USEREVENT + 4

    Walk = I.pg.USEREVENT + 5
    I.pg.time.set_timer(Walk, 300) #0.3 sec
    timers["Walk"] = Walk

    mob_gif = I.pg.USEREVENT + 6
    I.pg.time.set_timer(mob_gif, 100) # 0.1 sec
    timers["mob_gif"] = mob_gif

    timers["cook"] = I.pg.USEREVENT + 7

    healing = I.pg.USEREVENT + 8
    I.pg.time.set_timer(healing, 1000) # 1 sec
    timers["healing"] = healing



    return timers

def update_char_bar(screen, data, gifs, items):
    rect = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Char_bar"], [0, 0, S.SCREEN_WIDTH / 8, S.SCREEN_HEIGHT / 8])

    # start gifs if player dead
    if data["Player"]["hp"][0] <= 0 and not data["Player"]["dead"]:
        data["Player"]["dead"] = data["Zoom_rect"].copy()
        data["Player"]["dead"].x += I.info.OFFSCREEN[0] / 4
        data["Player"]["dead"].y += I.info.OFFSCREEN[1] / 4
        gifs["Ghost"].Start_gif("Ghost",[S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2, S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7])
        gifs["Portal"].Start_gif("Portal", [I.info.SPAWN_POINT[0] + 30, I.info.SPAWN_POINT[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7])
        data["Zoom_rect"].x = I.info.SPAWN_POINT[0]
        data["Zoom_rect"].y = I.info.SPAWN_POINT[1]
        I.info.OFFSCREEN = (0, 0)

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
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    for option in options:
        if I.info.EQUIPED[option] != 0:
            content = I.info.EQUIPED[option]
            if "|" in content:
                Ff.add_image_to_screen(screen, items.item_dict[content.split("|")[0]]["path"], [position[option][0], position[option][1], item_w, item_h])
            else:
                Ff.add_image_to_screen(screen, items.item_dict[content]["path"], [position[option][0], position[option][1], item_w, item_h])

def walking(dx, dy, collide, data):
    if (dx, dy) in movement and not collide[0] or (dx, dy) in movement and collide[0] in ["Portal", "Barkeep"]:
        I.info.LAST_ORIENTAION = regular_walking(data, dx, dy)
    elif collide[0] not in ["mob_collide"]:
        # if collision not with mob
        if movement[(dx, dy)] == I.info.LAST_ORIENTAION or movement[(dx, dy)][0] == I.info.LAST_ORIENTAION[0] or movement[(dx, dy)][1] == I.info.LAST_ORIENTAION[1]:
            data["Zoom_rect"].x -= 0
            data["Zoom_rect"].y -= 0
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0] - (dx * 3 * I.info.FAST), I.info.OFFSCREEN[1] - (dy * 3 * I.info.FAST))
        else:
            regular_walking(data, dx, dy)
    elif collide[0] == "mob_collide":
        # if collide is mob
        hit_by_mob_walking(data, collide)

def regular_walking(data, dx, dy):
    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
        if I.info.OFFSCREEN[0] in [0, 3, -3]:
            # if no collisions walk properly. move screen in x axis
            data["Zoom_rect"].x += movement[(dx, dy)][0] * I.info.FAST
            data["Zoom_rect"].y += 0
            last_orientation = movement[(dx, dy)]
        else:
            data["Zoom_rect"].x += 0
            data["Zoom_rect"].y += 0
            last_orientation = movement[(dx, dy)]
        if I.info.OFFSCREEN[1] in [0, 3, -3]:
            # if no collisions walk properly. move screen in y axis
            data["Zoom_rect"].x += 0
            data["Zoom_rect"].y += movement[(dx, dy)][1] * I.info.FAST
            last_orientation = movement[(dx, dy)]
        else:
            data["Zoom_rect"].x += 0
            data["Zoom_rect"].y += 0
            last_orientation = movement[(dx, dy)]
        return last_orientation
    else:
        data["Zoom_rect"].x += 0
        data["Zoom_rect"].y += 0
        return movement[(dx, dy)]

def hit_by_mob_walking(data, collide):
    differance = (collide[1]["current_pos"].x - data["Zoom_rect"].x, collide[1]["current_pos"].y - data["Zoom_rect"].y)
    dx, dy = ((differance[0] > 150) - (differance[0] < 150), (differance[1] > 80) - (differance[1] < 80))
    if I.info.OFFSCREEN[0] == 0:
        data["Zoom_rect"].x -= movement[(dx, dy)][0] * 7
        data["Zoom_rect"].y -= 0
    else:
        data["Zoom_rect"].x -= 0
        data["Zoom_rect"].y -= 0
    if I.info.OFFSCREEN[1] == 0:
        data["Zoom_rect"].x -= 0
        data["Zoom_rect"].y -= movement[(dx, dy)][1] * 7
    else:
        data["Zoom_rect"].x -= 0
        data["Zoom_rect"].y -= 0
def keypress_handle(screen, data, song, items, spells, gifs):
    keys = I.pg.key.get_pressed()
    dx = (keys[I.pg.K_RIGHT] - keys[I.pg.K_LEFT])
    dy = (keys[I.pg.K_DOWN] - keys[I.pg.K_UP])

    if keys[I.pg.K_z]:
        I.info.FAST = 2
    elif not keys[I.pg.K_z]:
        I.info.FAST = 1
    if keys[I.pg.K_v] and not data["Player"]["dead"]:
        curr_song = song["Playing"]
        song[curr_song].channel0.pause()
        br.spell_book(screen, data, spells, gifs)
        song[curr_song].channel0.unpause()
    if keys[I.pg.K_b] and not data["Player"]["dead"]:
        curr_song = song["Playing"]
        song[curr_song].channel0.pause()
        br.BackPack(screen, items, data["Player"])
        song[curr_song].channel0.unpause()
    if keys[I.pg.K_n] and not data["Player"]["dead"]:
        curr_song = song["Playing"]
        song[curr_song].channel0.pause()
        br.quest_render(screen, items)
        song[curr_song].channel0.unpause()
    return dx, dy

def interract(collide, data, gifs, items, screen, songs, spells, clock, rooms, npc, decorations):
    if collide[0] != False:
        if collide[0] in I.info.HARVESTABLE.keys() and not data["Player"]["dead"]:
            if any((collide[1], collide[2]) == (t[0], t[1]) for t in I.info.HARVESTED_OBJECTS.get(collide[0], [])):
                pass
            else:
                item = I.info.HARVESTABLE[collide[0]]
                amount = random.randrange(1, 5)
                br.add_to_backpack(item, amount, items)  # Adds harvested plants
                duration = int(items.item_dict[item]["Aquire"].split(",,")[3])
                #  Handle registering items that were taken, used in not allowing collection of too many items from single bush
                if I.info.HARVESTED_OBJECTS.get(collide[0]) == []:
                    I.info.HARVESTED_OBJECTS[collide[0]] = [(collide[1], collide[2], duration)]
                else:
                    existing_values = I.info.HARVESTED_OBJECTS.get(collide[0], [])

                    existing_values.append((collide[1], collide[2], duration))
                    I.info.HARVESTED_OBJECTS[collide[0]] = existing_values

                Ff.display_text_player("Recieved " + str(amount) + " " + str(item), 5000)
                return
        elif "door" in collide[0]:
            I.info.DOOR_CLICK = 0, collide[0]

            # building = collide[0].split("_")[0]
            # I.info.CURRENT_ROOM = {"name": building, "Spells": True, "Backpack": True, "Running": True, "Mobs": False, "Type": "House"}
            # rooms.select_room(building)
            # br.update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"], spells.selected_spell, npc)
            # I.info.ENTRY_POS = (1, 1)
            # I.info.OFFSCREEN = (25, 250)
            # Start(screen, clock, rooms)
        elif collide[0] == "Portal":
            Ff.display_text_player("Reviving", 3000)
        elif collide[0] == "Grave":
            Ff.display_text_player("Was Purgatory Fun?", 5000)
            data["Player"]["dead"] = False
            data["Player"]["hp"] = (data["Player"]["hp"][1], data["Player"]["hp"][1])
            gifs["Ghost"].start_gif = False
        elif collide[0] == "Sign":
            br.init_dialog("Sign", data["Player"], screen, npc, items)
        elif "Appliance" in collide[0]:
            appliance_name = collide[0].split("-")[1]
            for item in I.info.EQUIPED.values():
                if item != 0 and I.info.Temp_variable_holder == []:
                    I.info.APPLIANCE_CLICK = appliance_name
                    I.pg.time.set_timer(I.pg.USEREVENT + 7, 3000)
                    if I.info.BACKPACK_CONTENT[item][0] == 1:
                        del I.info.BACKPACK_CONTENT[item]
                    else:
                        I.info.BACKPACK_CONTENT[item] = (int(I.info.BACKPACK_CONTENT[item][0]) - 1, I.info.BACKPACK_CONTENT[item][1], I.info.BACKPACK_CONTENT[item][2])
                    backup_item = item
                    if "|" in backup_item:
                        backup_item = item.split("|")[0]
                    if "COOK" in items.item_dict[backup_item]["Properties"]:
                        I.info.Temp_variable_holder = [backup_item, 1, "cook"]
                    else:
                        I.info.Temp_variable_holder = [backup_item, 1, "burn"]
            br.update_equiped()
        elif collide[0] in npc.keys():
            # print("npc: ", collide[0])
            # print("I.info.Conversation: ", I.info.CONVERSATION)
            br.init_dialog(collide[0], data["Player"], screen, npc, items)
            # I.info.CONVERSATION = 0
            # if shop:
            #     br.init_shop(screen)
        else:
            print("not harvestable", collide)
            print(collide)

def harvest_timeout():
    for harvastable in I.info.HARVESTED_OBJECTS.keys():
        if I.info.HARVESTED_OBJECTS[harvastable] != []:
            i = 0
            while True:
                if I.info.HARVESTED_OBJECTS[harvastable][i][2] != 0:
                    I.info.HARVESTED_OBJECTS[harvastable][i] = (I.info.HARVESTED_OBJECTS[harvastable][i][0], I.info.HARVESTED_OBJECTS[harvastable][i][1], I.info.HARVESTED_OBJECTS[harvastable][i][2] - 1)
                if I.info.HARVESTED_OBJECTS[harvastable][i][2] == 0:
                    I.info.HARVESTED_OBJECTS[harvastable].pop(i)
                else:
                    i += 1
                if I.info.HARVESTED_OBJECTS[harvastable] == [] or i >= len(I.info.HARVESTED_OBJECTS[harvastable]):
                    break


def update_display_text(screen, gifs, data, collide):
    if I.info.TEXT:  # Check if the dictionary is not empty
        if I.info.CURRENT_ROOM["Type"] in ["Village"]:
            color = "black"
        else:
            color = "white"
        push = S.SCREEN_HEIGHT * 0.9
        for text in I.info.TEXT:
            lines = text.split(",,")
            time = lines[1]
            # Display the text
            Ff.display_text(screen, lines[0], 16, (50, push), color)
            push -= 30
            # Decrease the timer
            time = int(time) - 50
            # Check if the timer has expired
            if time < 0:
                if "Reviving" in text and collide[0] == "Portal":
                    a = I.info.TEXT.index(text)
                    I.info.TEXT[a] = lines[0] + "." + ",,3000"
                    if "..." in I.info.TEXT[a]:
                        I.info.TEXT.remove(lines[0] + "." + ",,3000")
                        gifs["Ghost"].start_gif = False  # stop the ghost gif
                        data["Player"]["dead"] = False  # set to alive
                        data["Player"]["hp"] = (data["Player"]["hp"][1], data["Player"]["hp"][1])  # return hp
                        I.info.BACKPACK_CONTENT = {"Gold": (0, 0, 0)}  # remove backpack content
                else:
                    I.info.TEXT.remove(text)
            else:
                a = I.info.TEXT.index(text)
                I.info.TEXT[a] = lines[0] + ",," + str(time)


def handle_combat(items):
    speed = 1
    orientation = I.info.LAST_ORIENT[0].split(".")[0]
    attack_direction = {"Front": (0, 10),
                        "Back": (0, -10),
                        "Left": (-10, 0),
                        "Right": (10, 0)}
    if I.info.EQUIPED["Sword"] != 0:
        damage, speed, knockback, type = Ff.get_property(I.info.EQUIPED["Sword"], items, "WEAPON")

    I.info.COMBAT_RECT = (I.pg.Rect(150 + attack_direction[orientation][0] + I.info.OFFSCREEN[0] / 4, 85 + attack_direction[orientation][1] + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100), float(speed) * I.info.BASE_ATTACKING_SPEED)  # Player rect (if it gets hit with other rect. colide is set to True

def handle_music(song, collide, data):
    if data["Player"]["dead"]:
        song["Playing"] = "Ghost"
    else:
        song["Playing"] = "Background"
    curr_song = song["Playing"]
    song[curr_song].channel0.set_volume(S.VOLUME)
    song[curr_song].channel1.set_volume(S.VOLUME)
    start_time = song[curr_song].start_time
    if collide[0] == "mob":
        bash = song[curr_song].generate_bash_sound()
        slice = song[curr_song].generate_slicing_sound()
        thump = song[curr_song].generate_thump_sound()
        song[curr_song].play_effect(thump)
    else:
        duration = song[curr_song].music[song[curr_song].current_note][1]
        if I.pg.time.get_ticks() - start_time > duration:
            song[curr_song].next_note()

    if I.pg.time.get_ticks() - song[curr_song].effect_time > 500:
        song[curr_song].channel1.stop()
