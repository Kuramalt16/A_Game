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

    br.get_backpack_coordinates(screen, "full")
    decorations = I.decor.Decorations()
    gifs = I.gifs.read_db(decorations)
    items = I.items.Items()
    spells = I.Spells.Spells()
    mob = {}
    if I.info.CURRENT_ROOM["Mobs"]:
        mob_dict = I.mob_data.read_db()
        for current_mob in I.info.CURRENT_ROOM["Mobs"].split(", "):
            mob_name = current_mob.split(":")[0]
            cur_dict = mob_dict[mob_name]
            count = current_mob.split(":")[1]
            path = cur_dict["path"]
            decor = False
            if path == "Decor":
                decor = True
                path = decorations.decor_dict[mob_name]["path"]
                path_lines = path.split("/")
                path = path_lines[0] + "/" + path_lines[1] + "/" + path_lines[2] + "/" + path_lines[3] + "/" + path_lines[4] + "/" + path_lines[5] + "/"
            mob[mob_name] = I.mob_data.Mob(name=mob_name, exp=cur_dict["exp"], hp=cur_dict["health"], allignment=cur_dict["allignment"], count=int(count), damage=cur_dict["damage"].split(":"), speed=cur_dict["speed"], path=path, delay=(cur_dict["delay"], cur_dict["delay"]), decor=decor)

    collide = [False]
    pressed = 0

    npc = I.dialog.read_db()

    data = br.Start(mob, decorations, spells, rooms, npc, items)
    if I.info.QUESTS == 0 and I.info.COMPLETED_QUESTS == 0 and data["Player"]["Gold"] == 0 and data["Player"]["Level"] == 1 and data["Player"]["Experience"] == 0:
        I.info.tutorial_flag = 1


    br.update_equiped()

    I.info.LAST_ORIENTAION = (0, 0)
    songs = {"Background": I.Songs.Song("Background", I.A.background_music),
             "Ghost": I.Songs.Song("Ghost", I.A.dead_music),
             "Playing": "Background",
             }
    songs["Slashing"] = songs[songs["Playing"]].generate_slash_sound()
    songs["Blunt"] = songs[songs["Playing"]].generate_blunt_sound()
    songs["Piercing"] = songs[songs["Playing"]].generate_stabbing_sound()


    I.th.start_threads(data, mob, spells, decorations, rooms, npc, gifs, songs, items)
    while S.PLAY:
        for event in I.pg.event.get():
            if event.type == I.pg.QUIT:
                S.PLAY = False
            if event.type == I.pg.KEYDOWN:
                pressed = handle_keydown(event, data, spells, gifs, items, songs)
            if event.type == I.pg.KEYUP:
                I.T.print_coordinates(event, data["Zoom_rect"])
                pressed = handle_keyup(event, pressed, gifs, songs, screen, items, data, collide, spells, clock, rooms, npc, decorations)

        collide = br.New_Update(data, decorations, gifs, rooms, clock, screen, spells, npc, mob, songs, items) # on average 20 ms, while dead: 9 ms
        if S.WINDOW == "Settings":
            handle_esc_click(screen, clock)

        I.TB.handle_hoe(collide, data, items, decorations, screen)

        handle_guards(collide, data, screen, npc, items, decorations, gifs, rooms, clock, spells)

        handle_music(songs, collide, data, items) # average 0.028 ms
        update_display_text(screen, gifs, data, collide) # max 0.008 ms

        update_char_bar(screen, data, gifs, items, rooms, clock, spells, npc) # max 1.11 ms
        display_spell_bar(screen, spells, gifs) # max 2.05 ms
        I.pg.display.flip()  # max 4.5 ms
        clock.tick(I.info.TICK)


def handle_keyup(event, pressed, gifs: dict, songs, screen, items, data, collide, spells, clock, rooms, npc, decorations):
    if event.key == pressed:
        curr_song = songs["Playing"]
        if pressed == I.pg.K_c:
            songs[curr_song].channel0.pause()
            interract(collide, data, gifs, items, screen, songs, spells, clock, rooms, npc, decorations)
            songs[curr_song].channel0.unpause()
        elif pressed == I.pg.K_x:
            if I.info.QUESTS != 0 and I.info.QUESTS["TYPE"] == "Tutorial" and I.info.QUESTS["ACTION"] == "PUNCH" and I.info.QUESTS["COMPLETION"] != 1:
                I.info.QUESTS["COMPLETION"] = 1
            I.info.COMBAT_RECT = [0, I.info.COMBAT_RECT[1]]
        elif pressed == I.pg.K_v:
            I.info.AXE = [0, I.info.AXE[1]]
        elif pressed == I.pg.K_b:
            I.info.PICAXE = [0, I.info.PICAXE[1]]
        elif pressed == I.pg.K_ESCAPE:
            if not I.info.PAUSE_THREAD["harvest"]:
                I.info.PAUSE_THREAD["harvest"] = True
            handle_esc_click(screen, clock)
        return 0

def handle_esc_click(screen, clock):
    running = True
    buttons = mr.Main_menu(screen)
    clicked_button = ""
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
                            I.info.SELECTED_CHARACTER = ""
                            S.PLAY = False
                            SP.run_game(screen, clock)
                        elif key == "Resume Game" and clicked_button == key:
                            Ff.button_click_render_down(screen, value, 0, S.PATHS["Empty_button_frame"])
                            running = False
                            I.info.PAUSE_THREAD["harvest"] = False
                            S.WINDOW = ""
                        elif key == "Settings" and clicked_button == key:
                            Ff.button_click_render_down(screen, value, 0, S.PATHS["Empty_button_frame"])
                            SB.Settings(screen)
                            running = False
                            S.WINDOW = "Settings"
                            # buttons = mr.Main_menu(screen)
                        I.pg.display.flip()
                    elif clicked_button != "" and clicked_button == key:
                        Ff.button_click_render_down(screen, value, 0, S.PATHS["Empty_button_frame"])
                        Ff.display_text(screen, key, 30, (buttons[key + "_text"].left, buttons[key + "_text"].top), "black")
                        I.pg.display.flip()
                        clicked_button = ""
            if event.type == I.pg.KEYUP:
                if event.key == I.pg.K_ESCAPE:
                    I.info.PAUSE_THREAD["harvest"] = False
                    running = False

def handle_keydown(event, data, spells, gifs: dict, items, songs):
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
    if event.key == I.pg.K_x and I.info.AXE[1] == 0 and I.info.PICAXE[1] == 0:
        if pressed != I.pg.K_x and not data["Player"]["dead"] and I.info.COMBAT_RECT[1] == 0:
            handle_combat(items, gifs)
            I.th.start_thread(int(I.info.COMBAT_RECT[1]), "hit", gifs)
            # I.pg.time.set_timer(I.pg.USEREVENT + 4, int(I.info.COMBAT_RECT[1]))

        pressed = I.pg.K_x
    if event.key == I.pg.K_v and I.info.COMBAT_RECT[1] == 0 and I.info.PICAXE[1] == 0:
        if I.info.EQUIPED["Axe"][0] != 0 and not data["Player"]["dead"] and I.info.AXE[1] == 0:
            curr_song = songs["Playing"]
            songs[curr_song].channel0.pause()
            orientation = I.info.LAST_ORIENT[0].split(".")[0]
            attack_direction = {"Front": (0, 10),
                                "Back": (0, -10),
                                "Left": (-10, 0),
                                "Right": (10, 0)}
            axe_properties = Ff.get_property(I.info.EQUIPED["Axe"][0].split("|")[0], items, "WEAPON")
            type = axe_properties[3] + " Strike"
            gifs[type].Start_gif(type, 1)
            speed = axe_properties[1]
            I.info.AXE = [I.pg.Rect(150 + attack_direction[orientation][0] + I.info.OFFSCREEN[0] / 4, 85 + attack_direction[orientation][1] + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100), float(speed) * I.info.BASE_ATTACKING_SPEED]
            # I.pg.time.set_timer(I.pg.USEREVENT + 9, int(I.info.AXE[1]))
            I.th.start_thread(int(I.info.AXE[1]), "axe", gifs)
            songs[curr_song].channel0.unpause()
        pressed = I.pg.K_v
    if event.key == I.pg.K_b and I.info.AXE[1] == 0 and I.info.COMBAT_RECT[1] == 0:
        if I.info.EQUIPED["Picaxe"][0] != 0 and not data["Player"]["dead"] and I.info.PICAXE[1] == 0:
            curr_song = songs["Playing"]
            songs[curr_song].channel0.pause()
            orientation = I.info.LAST_ORIENT[0].split(".")[0]
            attack_direction = {"Front": (0, 10),
                                "Back": (0, -10),
                                "Left": (-10, 0),
                                "Right": (10, 0)}
            picaxe_properties = Ff.get_property(I.info.EQUIPED["Picaxe"][0].split("|")[0], items, "WEAPON")
            type = picaxe_properties[3] + " Strike"
            gifs[type].Start_gif(type, 1)
            speed = picaxe_properties[1]
            I.info.PICAXE = [I.pg.Rect(150 + attack_direction[orientation][0] + I.info.OFFSCREEN[0] / 4, 85 + attack_direction[orientation][1] + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100), float(speed) * I.info.BASE_ATTACKING_SPEED]
            # I.pg.time.set_timer(I.pg.USEREVENT + 9, int(I.info.PICAXE[1]))
            I.th.start_thread(int(I.info.PICAXE[1]), "picaxe", gifs)
            songs[curr_song].channel0.unpause()
        pressed = I.pg.K_b
    if event.key in [I.pg.K_a, I.pg.K_s, I.pg.K_d, I.pg.K_f, I.pg.K_g]:
        keys_pressed = I.pg.key.get_pressed()
        if keys_pressed[I.pg.K_LSHIFT]:
            return pressed
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

    return pressed
def display_spell_bar(screen, spells, gifs: dict):
    Ff.add_image_to_screen(screen, S.PLAYING_PATH["Spell_bar"], (S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.9,  S.SCREEN_WIDTH / 5,  S.SCREEN_HEIGHT / 10))
    spell_w = S.SCREEN_WIDTH / 28
    spell_h = S.SCREEN_HEIGHT / 12
    spell_y = S.SCREEN_HEIGHT * 0.91
    for pos, spell in spells.selected_spell.items():
        spell_x = S.SCREEN_WIDTH * 0.804 + pos * 25
        Ff.add_image_to_screen(screen, gifs[spell].frame_paths[0][:-5] + "icon.png", (spell_x, spell_y, spell_w, spell_h))
        # if spells.spell_cooloff.get(spell) != None and spells.spell_cooloff[spell] != 0 and spells.spell_cooloff[spell] != spells.spell_dict[spell]["recharge"]:
        if spells.spell_cooloff.get(spell) != None and spells.spell_cooloff[spell] != 0:
            cover = I.pg.Surface((spell_w, int(spell_h * spells.spell_cooloff[spell] / spells.spell_dict[spell]["recharge"])), I.pg.SRCALPHA)
            cover.fill((0, 0, 0, 128))
            screen.blit(cover, (spell_x, spell_y))
def handle_mob_respawn(mob, data, rooms):
    if rooms.type in ["Village"]:
        # print("mob: ", mob)
        for monster_name in mob.keys():
            if mob[monster_name].count[0] < mob[monster_name].count[1]:
                mob[monster_name].count = (mob[monster_name].count[0] + 1, mob[monster_name].count[1])
                id = mob[monster_name].count[1] + 1
                mob[monster_name].mobs.append(mob[monster_name].create_mob(id))
                data[mob[monster_name].name] = br.generate_mobs(mob[monster_name], data["Image_rect"].size)

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
        br.update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"], spells.selected_spell, npc)
        I.info.CURRENT_ROOM = {"name": spawn_point[0], "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": "Village"}
        Start(screen, clock, rooms)
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


def walking(dx, dy, collide, data, decorations, sub_screen, rooms, screen):
    if (dx, dy) in movement and not collide[0] or (dx, dy) in movement and collide[0] in ["Portal", "Plant bed"]:
        I.info.LAST_ORIENTAION = regular_walking(data, dx, dy)
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

        # I.T.Make_rect_visible(sub_screen, me_left, "black")
        # I.T.Make_rect_visible(sub_screen, me_right, "purple")
        # I.T.Make_rect_visible(sub_screen, me_up, "white")
        # I.T.Make_rect_visible(sub_screen, me_down, "orange")

        if me_left.collidelist(decorations.displayed_rects) != -1:
            # print("colliding left", I.info.OFFSCREEN[0])
            if dx != 1:
                I.info.OFFSCREEN = (I.info.OFFSCREEN[0] - dx * 3 * I.info.FAST, I.info.OFFSCREEN[1])
        elif dx != 1:
            regular_walking(data, dx, 0)


        if me_right.collidelist(decorations.displayed_rects) != -1:
            # print("colliding right", I.info.OFFSCREEN[0])
            if dx != -1:
                I.info.OFFSCREEN = (I.info.OFFSCREEN[0] - dx * 3 * I.info.FAST, I.info.OFFSCREEN[1])
        elif dx != -1:
            regular_walking(data, dx, 0)


        if me_up.collidelist(decorations.displayed_rects) != -1:
            # print("colliding up", I.info.OFFSCREEN[1])
            if dy != 1:
                I.info.OFFSCREEN = (I.info.OFFSCREEN[0], I.info.OFFSCREEN[1] - dy * 3 * I.info.FAST)
        elif dy != 1:
            regular_walking(data, 0, dy)


        if me_down.collidelist(decorations.displayed_rects) != -1:
            # print("colliding down", I.info.OFFSCREEN[1])
            if dy != -1:
                I.info.OFFSCREEN = (I.info.OFFSCREEN[0], I.info.OFFSCREEN[1] - dy * 3 * I.info.FAST)
        elif dy != -1:
            regular_walking(data, 0, dy)


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
def keypress_handle(screen, data, song, items, spells, gifs, rooms, clock):
    keys = I.pg.key.get_pressed()
    dx = (keys[I.pg.K_RIGHT] - keys[I.pg.K_LEFT])
    dy = (keys[I.pg.K_DOWN] - keys[I.pg.K_UP])
    if I.info.QUESTS != 0 and I.info.QUESTS["TYPE"] == "Tutorial":
        if I.info.QUESTS["ACTION"] == "WALK" and I.info.QUESTS["COMPLETION"] != 1:
            if dx == -1 and I.info.QUESTS["COMPLETION"] == 0:
                I.info.QUESTS["COMPLETION"] = 0.25
            if dx == 1 and I.info.QUESTS["COMPLETION"] == 0.25:
                I.info.QUESTS["COMPLETION"] = 0.5
            if dy == -1 and I.info.QUESTS["COMPLETION"] == 0.5:
                I.info.QUESTS["COMPLETION"] = 0.75
            if dy == 1 and I.info.QUESTS["COMPLETION"] == 0.75:
                I.info.QUESTS["COMPLETION"] = 1
        elif I.info.QUESTS["ACTION"] == "RUN" and I.info.QUESTS["COMPLETION"] != 1:
            if I.info.FAST == 2:
                if dx == -1 and I.info.QUESTS["COMPLETION"] == 0:
                    I.info.QUESTS["COMPLETION"] = 0.25
                if dx == 1 and I.info.QUESTS["COMPLETION"] == 0.25:
                    I.info.QUESTS["COMPLETION"] = 0.5
                if dy == -1 and I.info.QUESTS["COMPLETION"] == 0.5:
                    I.info.QUESTS["COMPLETION"] = 0.75
                if dy == 1 and I.info.QUESTS["COMPLETION"] == 0.75:
                    I.info.QUESTS["COMPLETION"] = 1
    if keys[I.pg.K_z]:
        I.info.FAST = 2
    elif not keys[I.pg.K_z]:
        I.info.FAST = 1
    if keys[I.pg.K_u] and not data["Player"]["dead"]:
        curr_song = song["Playing"]
        song[curr_song].channel0.pause()
        br.spell_book(screen, data, spells, gifs)
        song[curr_song].channel0.unpause()
    elif keys[I.pg.K_i] and not data["Player"]["dead"]:
        curr_song = song["Playing"]
        song[curr_song].channel0.pause()
        br.BackPack(screen, items, data["Player"])
        song[curr_song].channel0.unpause()
        if I.info.QUESTS != 0 and I.info.QUESTS["TYPE"] == "Tutorial":
            if I.info.QUESTS["ACTION"] == "QUEST_BACKPACK" and I.info.QUESTS["COMPLETION"] != 1:
                I.info.QUESTS["COMPLETION"] += 0.5
    elif keys[I.pg.K_q] and not data["Player"]["dead"]:
        curr_song = song["Playing"]
        song[curr_song].channel0.pause()
        if I.info.QUESTS != 0 and I.info.QUESTS["TYPE"] == "Tutorial":
            if I.info.QUESTS["ACTION"] == "QUEST_BACKPACK" and I.info.QUESTS["COMPLETION"] != 1:
                I.info.QUESTS["COMPLETION"] += 0.5
        br.quest_render(screen, items)
        song[curr_song].channel0.unpause()


    elif keys[I.pg.K_g] and keys[I.pg.K_o] and keys[I.pg.K_d] and keys[I.pg.K_LSHIFT]:
        handle_cheats(screen, data, rooms, clock)
    return dx, dy

def interract(collide, data, gifs, items, screen, songs, spells, clock, rooms, npc, decorations):
    if collide[0] != False:
        if collide[0] in I.info.HARVESTABLE.keys() and not data["Player"]["dead"]:
            if any(collide[1] == t[0] for t in I.info.HARVESTED_OBJECTS.get(collide[0])):
                Ff.display_text_player("Nothing found", 500)
                pass
            else:
                item = I.info.HARVESTABLE[collide[0]]
                values = items.item_dict[item]["Aquire"].split(",,")
                amount = random.randint(int(values[1]), int(values[2]))
                if I.info.QUESTS != 0 and I.info.QUESTS["TYPE"] == "Tutorial" and I.info.QUESTS["ACTION"] == "EAT" and I.info.QUESTS["COMPLETION"] == 0:
                    if item == "Light Berries":
                        I.info.QUESTS["COMPLETION"] = 0.3333
                Ff.add_to_backpack(item, amount, items)  # Adds harvested plants
                duration = int(values[3])
                #  Handle registering items that were taken, used in not allowing collection of too many items from single bush
                harvested_obj_rect = decorations.decor_dict[collide[0]][collide[1]]["rect"]
                if I.info.HARVESTED_OBJECTS.get(collide[0]) == []:
                    # Ff.update_map_view(collide[1], collide[0] + "_Harvested", (harvested_obj_rect.x, harvested_obj_rect.y), "add")
                    Ff.update_map_view(collide[1], collide[0], (harvested_obj_rect.x, harvested_obj_rect.y), "remove")
                    Ff.update_map_view(collide[1], collide[0] + "_Harvested", (harvested_obj_rect.x, harvested_obj_rect.y), "add")
                    I.info.HARVESTED_OBJECTS[collide[0]] = [(collide[1], duration, I.info.CURRENT_ROOM["name"])]

                else:
                    Ff.update_map_view(collide[1], collide[0], (harvested_obj_rect.x, harvested_obj_rect.y), "remove")
                    Ff.update_map_view(collide[1], collide[0] + "_Harvested", (harvested_obj_rect.x, harvested_obj_rect.y), "add")
                    existing_values = I.info.HARVESTED_OBJECTS.get(collide[0], [])
                    existing_values.append((collide[1], duration, I.info.CURRENT_ROOM["name"]))
                    I.info.HARVESTED_OBJECTS[collide[0]] = existing_values
                Ff.display_text_player("Recieved " + str(amount) + " " + str(item), 5000)
                return
        elif "door" in collide[0]:
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
            if "CONTAINER" in decorations.decor_dict[collide[0]]["action"]:
                container_name = collide[0]
                container_size = decorations.decor_dict[collide[0]]["action"].split(":")[1]
                handle_containers(container_name, container_size, items, screen, data["Player"], decorations, collide[2])
            elif "Appliance" in decorations.decor_dict[collide[0]]["type"]:
                handle_appliances(collide[0], items.item_dict, items)
            elif "PLANT" in decorations.decor_dict[collide[0]]["action"]:
                if I.info.EQUIPED["Sword"][0] != 0 and "PLANTABLE" in items.item_dict[I.info.EQUIPED["Sword"][0]]["Properties"]:
                    plant = items.item_dict[I.info.EQUIPED["Sword"][0]]["Properties"].replace("PLANTABLE(", "").replace(")", "").split(",,,")[0].split(",,")
                    time = plant[1].replace("TIME:", "")
                    plant = plant[0].replace("PLANT:", "")
                    decorations.decor_dict[collide[0]][collide[1]]["effect"] = "PLANTED:" + plant + ":" + time + ":" + time
                    I.th.start_thread(time, "planting", decorations)
                    br.remove_from_backpack(I.info.EQUIPED["Sword"][0], 1)
                    br.update_equiped()
            elif "NPC_Mob" in decorations.decor_dict[collide[0]]["type"]:
                I.DialB.init_dialog(collide[0], data["Player"], screen, npc, items, decorations, data, gifs, rooms, clock, spells)
            else:
                print("some other decor", collide)
                print("some other decor", decorations.decor_dict[collide[0]])
        else:
            print("not harvestable", collide)

def harvest_timeout(decorations):
    for harvastable in I.info.HARVESTED_OBJECTS.keys():
        if I.info.HARVESTED_OBJECTS[harvastable] != []:
            i = 0
            while True:
                if I.info.HARVESTED_OBJECTS[harvastable][i][1] != 0:
                    I.info.HARVESTED_OBJECTS[harvastable][i] = (I.info.HARVESTED_OBJECTS[harvastable][i][0], I.info.HARVESTED_OBJECTS[harvastable][i][1] - 1, I.info.HARVESTED_OBJECTS[harvastable][i][2])
                if I.info.HARVESTED_OBJECTS[harvastable][i][1] == 0 and I.info.CURRENT_ROOM["name"] == I.info.HARVESTED_OBJECTS[harvastable][i][2]:
                    coordinates = Ff.get_decor_coordinates(harvastable + "_Harvested", I.info.HARVESTED_OBJECTS[harvastable][i][0], decorations)
                    if coordinates != None:
                        Ff.update_map_view(I.info.HARVESTED_OBJECTS[harvastable][i][0], harvastable, coordinates, "add", I.info.HARVESTED_OBJECTS[harvastable][i][2])
                        Ff.update_map_view(I.info.HARVESTED_OBJECTS[harvastable][i][0], harvastable + "_Harvested",(0, 0), "remove", I.info.HARVESTED_OBJECTS[harvastable][i][2])
                        I.info.HARVESTED_OBJECTS[harvastable].pop(i)
                else:
                    i += 1
                if I.info.HARVESTED_OBJECTS[harvastable] == [] or i >= len(I.info.HARVESTED_OBJECTS[harvastable]):
                    break


def update_display_text(screen, gifs: dict, data, collide):
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


def handle_combat(items, gifs):
    speed = 1
    type = "Blunt"
    orientation = I.info.LAST_ORIENT[0].split(".")[0]
    attack_direction = {"Front": (0, 10),
                        "Back": (0, -10),
                        "Left": (-10, 0),
                        "Right": (10, 0)}
    if I.info.EQUIPED["Sword"][0] != 0:
        damage, speed, knockback, type = Ff.get_property(I.info.EQUIPED["Sword"][0], items, "WEAPON")
    gifs[type + " Strike"].Start_gif(type + " Strike", 1)
    I.info.COMBAT_RECT = [I.pg.Rect(150 + attack_direction[orientation][0] + I.info.OFFSCREEN[0] / 4, 80 + attack_direction[orientation][1] + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 80), float(speed) * I.info.BASE_ATTACKING_SPEED]  # Player rect (if it gets hit with other rect. colide is set to True

def handle_music(song, collide, data, items):
    # print(song["Playing"])
    if data["Player"]["dead"]:
        if song["Playing"] != "Ghost":
            song["Playing"] = "Ghost"
            I.pg.time.set_timer(I.pg.USEREVENT + 10, 1000)
    elif song["Playing"] != "Background":
        song["Playing"] = "Background"
        I.pg.time.set_timer(I.pg.USEREVENT + 10, 500)
    curr_song = song["Playing"]
    song[curr_song].channel0.set_volume(S.VOLUME)
    song[curr_song].channel1.set_volume(S.VOLUME)
    if collide[0] == "mob_collide":
        # bash = song[curr_song].generate_bash_sound()
        # slice = song[curr_song].generate_slicing_sound()
        thump = song[curr_song].generate_thump_sound()
        song[curr_song].play_effect(thump)
    elif I.info.COMBAT_RECT[0] != 0: # NO BLUNT SOUND

        if I.info.EQUIPED["Sword"][0] != 0:
            type = Ff.get_property(I.info.EQUIPED["Sword"][0], items, "WEAPON")[3]
        else:
            type = "Blunt"
            # type = "Piercing"
        song[curr_song].play_effect(song[type])

    # else:
    #     duration = song[curr_song].music[song[curr_song].current_note][1]
    #     I.pg.time.set_timer(I.pg.USEREVENT + 10, duration)
    # print(duration)

    if I.pg.time.get_ticks() - song[curr_song].effect_time > 500: # HARDCODED TO ONLY PLAY 500 ms OF EFFECT
        song[curr_song].channel1.stop()
        song[curr_song].effect_flag = False

def handle_cheats(screen, data, rooms, clock):
    running = True
    input_text = ""
    rect = I.pg.Rect(100, 500, S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.2)
    I.pg.draw.rect(screen, "white", rect)
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_ESCAPE:
                    running = False
                elif event.key == I.pg.K_RETURN:
                    running = False
                elif event.key == I.pg.K_BACKSPACE:
                    input_text = input_text[:-1]
            if event.type == I.pg.TEXTINPUT:
                input_text += event.text
        I.pg.draw.rect(screen, "white", rect)
        Ff.display_text(screen, input_text, 16, [100, 500], "red")
        I.pg.display.flip()

    command = input_text.split(":")[0]
    value = input_text.split(":")[1]
    if command in I.A.COMMANDS:
        if command == I.A.COMMANDS[0]:
            S.GOD_MODE = bool(int(value))
        if command == I.A.COMMANDS[1]:
            value = value.split(",")
            data["Zoom_rect"] = I.pg.Rect(int(value[0]), int(value[1]), data["Zoom_rect"].w, data["Zoom_rect"].h)
        if command == I.A.COMMANDS[2]:
            rooms.select_room(value)
            I.info.CURRENT_ROOM = {"name": value, "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": "Village"}
            Start(screen, clock, rooms)

def handle_containers(container_name, container_size, items, screen, player, decorations, id):
    pressed = 0 # key authentication
    running = True # loop var
    block = (0, 0) # backpack block
    border = 1 # rect border size
    screen.fill((0,0,0,0))
    use = 0 # place holder for items to be eaten/used
    selected = 0 # place holder for rect of selected block
    color = "Yellow" # color of selected rect
    pickup = (0, 0, 0) # place holder for the name, posx, posy of selected block
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    # coordinates = br.get_equipment_coordinates(block)
    container_size = int(container_size.split("x")[0]), int(container_size.split("x")[1])
    container_coordinates = get_container_coordinates(container_size)

    remove_from_container = []
    path = S.PLAYING_PATH["Backpack_Tile"]

    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_i:
                    pressed = I.pg.K_i
                elif event.key == I.pg.K_ESCAPE:
                    pressed = I.pg.K_ESCAPE
                elif event.key == I.pg.K_x:
                    pressed = I.pg.K_x
                elif event.key == I.pg.K_c:
                    pressed = I.pg.K_c
                    if selected == 0:
                        if block[0] >= 0:
                            selected = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
                            pickup = (br.find_item_by_slot(block[0], block[1]), block[0], block[1])
                        else:
                            selected = I.pg.Rect(container_coordinates[block][0], container_coordinates[block][1], item_w, item_h)
                            pickup = (br.find_item_by_slot_containers(block[0], block[1], container_name, id), block[0], block[1])
                    else:
                        # print("if selected is not 0: ", selected)
                        if pickup[0] != 0 and pickup[0] != None:
                            remove_from_container = handle_container_backpack_switching(pickup, selected, container_name, id, block, items)
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
                if event.key == I.pg.K_x and pressed == I.pg.K_x:
                    if block[0] < 0:
                        # IF SELECTED IN CONTAINER, REMOVE THE ITEM AND ADD IT TO BACKPACK
                        selected = I.pg.Rect(container_coordinates[block][0], container_coordinates[block][1], item_w, item_h)
                        pickup = (br.find_item_by_slot_containers(block[0], block[1], container_name, id), block[0], block[1])
                        remove_from_container.append(pickup[1:3])
                        Ff.add_to_backpack(pickup[0], 1, items)
                    else:
                        # IF SELECTED IN BACKPACK, REMOVE THE ITEM AND ADD IT TO CONTAINER
                        selected = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
                        pickup = (br.find_item_by_slot(block[0], block[1]), block[0], block[1])
                        new_block = (-2, 0)
                        cancel = False
                        for key, value in I.info.CONTAINERS.items():
                            for sub_key, sub_value in value.items():
                                if new_block == sub_key:
                                    new_block = new_block[0] - 2, new_block[1]
                                    if new_block[0] < -2 - container_size[1]:  # handles switching to lower container levels (Y axis)
                                        new_block = -2, new_block[1] + 2
                                        if new_block[1] > container_size[0] * 2 - 2: # Handles not overfilling the container. if the new block Y pos is higher than the size of container multiplied by 2 ( block format is in twos) and removed -2 (block format starts from 0) then dont add
                                            cancel = True
                        if not cancel and pickup[0] != None:
                            handle_container_storage(pickup[0], container_name, new_block, id, selected)


                    selected = 0
                    pickup = (0, 0, 0)


        br.display_backpack(screen, player, items, screen.get_rect(), "half")


        # DISPLAY CONTAINER GRID
        Ff.add_image_to_screen(screen, decorations.decor_dict[container_name]["path"], [275, 175, 150, 200])
        start_row = 312
        start_collumn = 225

        for i in range(0, int(container_size[0])):
            for a in range(0, int(container_size[1])):
                Ff.add_image_to_screen(screen, path, [start_row, start_collumn, 42, 40])
                start_row += 36
            start_row = 312
            start_collumn += 36



        if block[0] < 0:
            if block[0] < -2 * container_size[1]:
                block = -2 * container_size[1], block[1]
            if block[1] > 2 * (container_size[0] - 1):
                block = block[0], 2 * (container_size[0] - 1)
            rect = I.pg.Rect(container_coordinates[block][0], container_coordinates[block][1], item_w, item_h)
        else:
            rect = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)

        if remove_from_container != []:
            for i in remove_from_container:
                del I.info.CONTAINERS[container_name, id][i[0], i[1]]
            remove_from_container = []

        if I.info.CONTAINERS.get((container_name, id)) != None:
            for pos, (name, amount) in I.info.CONTAINERS[(container_name, id)].items():
                Ff.add_image_to_screen(screen, items.item_dict[name.split("|")[0]]["path"], [container_coordinates[pos][0], container_coordinates[pos][1], item_w, item_h])

        I.pg.draw.rect(screen, color, rect, border)
        if selected != 0:
            I.pg.draw.rect(screen, "Yellow", selected, 2)

        I.pg.display.flip()

def get_container_coordinates(size):
    start_row = 390
    start_collumn = 232
    size_x = 36
    size_y = 36
    coordinates = {}

    height = size[0] * 2
    width = size[1] * -2 + -2
    for i in range(0, height, 2):
        for a in range(-2, width, -2):
            coordinates[(a, i)] = (start_row + a / 2 * size_x, start_collumn + i / 2 * size_y)

    return coordinates


def get_container_block(input_tuple, size_tuple):
    # print(input_tuple, size_tuple)

    first, second = input_tuple
    collumns, rows = size_tuple

    output1 = (first / -2) - 1
    if output1 > rows - 1:
        output1 = rows - 1

    output2 = second / 2
    if output2 > collumns - 1:
        output2 = collumns - 1

    return int(output2), int(output1)

def handle_container_storage(item_name, container, possision, id, rect):
    if I.info.CONTAINERS.get((container, id)) == None:
        # print("first")
        # THIS MEANS NO DATA ABOUT THIS CONTAINER EXISTS
        I.info.CONTAINERS[container, id] = {
            possision: (item_name, 1)
                                            }
    else:
        # THIS MEANS CONTAINER WAS ALREADY MADE AND WE CAN NOW ADD EXTRA ITEMS TO IT
        if I.info.CONTAINERS[container, id].get(possision) == None:
            # THIS MEANS NO ITEM EXISTS IN THIS POSSISION
            # print("no item exists here")
            I.info.CONTAINERS[container, id][possision] = item_name, 1
        else:
            # pass
            print("item already exists here need to skip to another location in container")

            rect = 10, 800
            # THIS MEANS AN ITEM ALREADY EXISTS HERE
            # old_item = I.info.CONTAINERS[container, id][possision]
            # I.info.CONTAINERS[container, id][possision] = item_name, 1
            # a, pos_x, pos_y = I.info.BACKPACK_CONTENT[item_name]
            # I.info.BACKPACK_CONTENT[old_item[0]] = old_item[1], pos_x, pos_y
    # I.info.CONTAINERS[container, id] = item_name, I.info.BACKPACK_CONTENT[item_name][0], possision
    if rect[0] >= 633 and item_name != None:
        I.info.BACKPACK_CONTENT[item_name] = I.info.BACKPACK_CONTENT[item_name][0] - 1, I.info.BACKPACK_CONTENT[item_name][1], I.info.BACKPACK_CONTENT[item_name][2]
        if I.info.BACKPACK_CONTENT[item_name][0] == 0:
            del I.info.BACKPACK_CONTENT[item_name]
    print(I.info.CONTAINERS)

def handle_appliances(appliance_name, item_dict, items):
    item = I.info.EQUIPED["Sword"][0]
    if item != 0 and I.info.APPLIANCE_CLICK == [""]:
        if "COOK" in item_dict[item]["Properties"] and appliance_name == "Furnace": # checks if the chosen item can be cooked or smelted else burn it
            I.info.APPLIANCE_CLICK = [appliance_name, item.split("|")[0], 1, "cook"]
            # I.pg.time.set_timer(I.pg.USEREVENT + 7, 3000)  # Set timer for the appliance
            I.th.start_thread(3000, "cook", items)
            br.remove_from_backpack(item, 1)  # removes the item
        elif "SMELT" in item_dict[item]["Properties"] and appliance_name == "Blast Furnace":
            I.info.APPLIANCE_CLICK = [appliance_name, item.split("|")[0], 1, "smelt"]
            if I.info.BACKPACK_CONTENT[item][0] >= 2:
                br.remove_from_backpack(item, 2)  # removes the item
                # I.pg.time.set_timer(I.pg.USEREVENT + 7, 2800)  # Set timer for the appliance
                I.th.start_thread(3000, "cook", items)

                # I.pg.time.set_timer(I.pg.USEREVENT + 7, 10000)  # Set timer for the appliance
            else:
                Ff.display_text_player("Not enough material to smelt", 3000)
                I.info.APPLIANCE_CLICK = [""] # didnt have enough items

        elif appliance_name == "Furnace":
            I.info.APPLIANCE_CLICK = [appliance_name, item.split("|")[0], 1, "burn"]
            # I.pg.time.set_timer(I.pg.USEREVENT + 7, 3000)  # Set timer for the appliance
            I.th.start_thread(3200, "cook", items)

            br.remove_from_backpack(item, 1)  # removes the item
        elif appliance_name == "Blast Furnace":
            Ff.display_text_player(str(item.split("|"[0].replace("0", "").replace("1",""))[0]) + " can not be smelt", 3000)

    br.update_equiped()

def handle_cooking_food(items):
    if I.info.APPLIANCE_CLICK[0] == "Furnace":
        I.info.APPLIANCE_CLICK[0] = ""
        if I.info.APPLIANCE_CLICK[3] == "cook":
            Ff.add_to_backpack(I.info.APPLIANCE_CLICK[1] + "_Cooked", 1, items)
            if any(char.isdigit() for char in I.info.APPLIANCE_CLICK[1]):  # if name has a number. like Meat1 or Meat0
                I.info.APPLIANCE_CLICK[1] = I.info.APPLIANCE_CLICK[1][:-1]
            Ff.display_text_player("Cooked " + I.info.APPLIANCE_CLICK[1], 5000)
        else:
            Ff.add_to_backpack("Ashes", 1, items)
            Ff.display_text_player("Burned " + I.info.APPLIANCE_CLICK[1], 3000)
    elif I.info.APPLIANCE_CLICK[0] == "Blast Furnace":
        I.info.APPLIANCE_CLICK[0] = ""
        if I.info.APPLIANCE_CLICK[3] == "smelt":
            item = get_smelted_item(I.info.APPLIANCE_CLICK[1], items)
            Ff.add_to_backpack(item, 1, items)
            Ff.display_text_player("Smelted " + I.info.APPLIANCE_CLICK[1], 5000)
        # else:
        #     Ff.display_text_player("This item can not be smelted", 5000)
    I.info.APPLIANCE_CLICK = [""]

def get_smelted_item(item_name, items):
    probabilities, outcomes = Ff.get_property(item_name, items, "SMELT")
    item = random.choices(outcomes, probabilities)[0]
    return item

def handle_container_backpack_switching(pickup, selected, container_name, id, block, items):
    remove_from_container = []

    # HANDLE OLD POSSISION, (Delete if it's from the container, get value if its from the backpack)
    if I.info.BACKPACK_CONTENT.get(pickup[0]) != None:
        # IF THE ITEM IN PICKUP[0] EXISTS IN BACKPACK THEN CONTINUE
        if selected[0] < 633:
            # FROM CONTAINER
            value = I.info.CONTAINERS[container_name, id][pickup[1:3]]
            value = value[1], pickup[1], pickup[2]
            # print("then the value is: ", value)
            if br.find_item_by_slot_containers(block[0], block[1], container_name, id) == None:
                # print("if the item exists in container: add it to the deleting list")
                remove_from_container.append(pickup[1:3])
        else:
            # FROM BACKPACK
            value = I.info.BACKPACK_CONTENT[pickup[0]]
            # print("if the selected item is from backpack, then the value is: ", value)
    else:
        # print("if the picked up item doesn't exist in the backpack")
        # IF THE ITEM DOESNT EXIST IN THE BACKPACK, CHECK THE CONTAINER
        value = I.info.CONTAINERS[container_name, id][pickup[1:3]]
        value = value[1], pickup[1], pickup[2]
        # print("then we add it to backpack and remove it from the container")
        remove_from_container.append(pickup[1:3])

    # HANDLE NEW POSSISION
    taken_spaces = list(I.info.BACKPACK_CONTENT.values())
    if not any((block[0], block[1]) == (tpl[1], tpl[2]) for tpl in taken_spaces):
        # print("if the new possision is not in a taken space")
        #  IF THE SPOT WE WANT TO ASSIGN IS NOT TAKEN CONTINUE
        if block[0] < 0 and pickup[0] != None:
            # print("if the new possision is in the container:")
            handle_container_storage(pickup[0], container_name, block, id, selected)
        else:
            # print("if the new possision is in the backpack")
            # FIRST LET's CHECK IF THE VALUE DIDN'T ALREADY EXIST:
            if I.info.BACKPACK_CONTENT.get(pickup[0]) != None and selected[0] < 633:
                # print("if the picked up item already existed in the backpack and it was selected from the container")
                # PICKUP[0] item did exist. lets merge them.
                I.info.BACKPACK_CONTENT[pickup[0]] = (
                I.info.BACKPACK_CONTENT[pickup[0]][0] + value[0], block[0], block[1])
            else:
                # print("if the picked up item didnt exist in the backpack or was picked up from the backpack")
                I.info.BACKPACK_CONTENT[pickup[0]] = (value[0], block[0], block[1])  # set the new possision value
    else:
        # print("if the new possision is on another item")
        # ITEM PLACE WAS TAKEN, SWITCHING PLACES
        existing_item = br.find_item_by_slot(block[0], block[1])  # get existing item name
        if "STACK" in existing_item and "STACK" in pickup[0] and selected[0] >= 633:
            # print("if the possisions` item has stack in it and the item was in backpack")
            # BOTH OF THESE ITEMS ARE STACKS
            stack = Ff.get_property(existing_item.split("|")[0], items, "STACK")
            if float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0].split("|")[0]][0]) <= stack:
                # print("if the existing item added up with the new picked up item is still less tahn the amount allowed by the stack")
                # MERGING TWO STACKS INTO ONE
                sum = float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0]][0])
                I.info.BACKPACK_CONTENT[existing_item] = sum, I.info.BACKPACK_CONTENT[existing_item][1], I.info.BACKPACK_CONTENT[existing_item][2]
                del I.info.BACKPACK_CONTENT[pickup[0]]
                # print("then we add up the items and remove the picked up item from the backpack")

            elif float(I.info.BACKPACK_CONTENT[existing_item][0]) < stack and float(I.info.BACKPACK_CONTENT[pickup[0]][0]) < stack and selected[0] >= 633:
                # print("if the existing item and the picked up item both are less than the stack allows and the item was in backpack")
                # MERGING VALUES OF STACKS WITH REMAINDER
                remainder = float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0]][0]) - stack
                I.info.BACKPACK_CONTENT[pickup[0]] = remainder, I.info.BACKPACK_CONTENT[pickup[0]][1], I.info.BACKPACK_CONTENT[pickup[0]][2]
                I.info.BACKPACK_CONTENT[existing_item] = stack, I.info.BACKPACK_CONTENT[existing_item][1], I.info.BACKPACK_CONTENT[existing_item][2]
                # print("then we add up the items but leave a remainder")
        else:
            # print("if the existing item didn't have a stack")
            # CHECKING IF IT'S POSSIBLE TO JUST ADD THE TWO DIFERENT ITEMS INTO ONE ONLY IN BACKPACK
            stack = Ff.get_property(existing_item.split("|")[0], items, "STACK")
            if existing_item.split("|")[0] == pickup[0].split("|")[0] and I.info.BACKPACK_CONTENT[existing_item][0] + 1 < stack and selected[0:2] != [list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]]]:
                # print("if the existing items name is the same as the name of pickup and if the existing item is less than stack and if the selected new spot is not the same as the old spot IN BACKPACK")
                I.info.BACKPACK_CONTENT[existing_item] = I.info.BACKPACK_CONTENT[existing_item][0] + 1, block[0], block[1]
                # print("then we add one to the existing item")
            elif existing_item.split("|")[0] == pickup[0].split("|")[0] and selected[0:2] != [list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]]]:
                # print("if the existing item names are the same and the stack got overflowed. then we only add one item to a new stack")
                Ff.add_to_backpack(pickup[0], 1, items)
            else:
                # print("if the names aren't the same")
                if selected[0] >= 633:
                    # print("if the item was selected from the backpack")
                    I.info.BACKPACK_CONTENT[existing_item] = I.info.BACKPACK_CONTENT[existing_item][0], pickup[1], pickup[2]
                    I.info.BACKPACK_CONTENT[pickup[0]] = I.info.BACKPACK_CONTENT[pickup[0]][0], block[0], block[1]
                    # print("then we switch the places of those items")
                else:
                    # print("if the selected item was from the container, erase the deleting list")
                    remove_from_container = []
    return remove_from_container

def handle_guards(collide, data, screen, npc, items, decorations, gifs, rooms, clock, spells):

    if collide != [False] and "Guard" in collide[0] and "Criminal" in ",".join(I.info.TITLES):
        current_mob = collide[1]
        guard_name = collide[0]
        if current_mob["hp"][0] == current_mob["hp"][1] and npc[guard_name]["dialog"].iteration != 1:
            I.DialB.init_dialog(guard_name, data["Player"], screen, npc, items, decorations, data, gifs, rooms, clock, spells)
            # current_mob["hp"] = current_mob["hp"][0], current_mob["hp"][1] + 1
        elif "Criminal|0" in I.info.TITLES and npc[guard_name]["dialog"].iteration == 1:
            I.info.TITLES.remove("Criminal|0")
            I.info.TITLES.append("Criminal|1")