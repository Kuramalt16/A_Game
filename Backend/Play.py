from Render import Background_Render as br, Main_Menu_render as mr
from Values import Settings as S
from utils import Imports as I, Frequent_functions as Ff
from Backend import Settings_backend as SB, Setup_pygame as SP


def reset(rooms, screen):
    I.A.QUEST_SHOW_MARKS = {}
    I.BB.get_backpack_coordinates(screen, "full")
    screen.fill("black")
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
            mob[mob_name] = I.mob_data.Mob(name=mob_name, exp=cur_dict["exp"], hp=cur_dict["health"], allignment=cur_dict["allignment"], count=int(count), damage=cur_dict["damage"].split(":"), speed=cur_dict["speed"], path=path, delay=(cur_dict["delay"], cur_dict["delay"]), decor=decor, drop=cur_dict["drop"])


    collide = [False]
    pressed = 0

    npc = I.dialog.read_db()

    data = br.Start(mob, decorations, spells, rooms, npc, items, gifs)

    I.QB.set_tutorial_flag()

    I.BB.update_equiped()

    I.info.LAST_ORIENTAION = (0, 0)
    songs = {"Background": I.Songs.Song("Background", I.A.background_music),
             "Ghost": I.Songs.Song("Ghost", I.A.dead_music),
             "Playing": "Background",
             }
    songs["Pavement"] = songs[songs["Playing"]].load_premade_effect("Walk_pavement", "Pavement")
    songs["Grass-Pavement"] = songs[songs["Playing"]].load_premade_effect("Walk_pavement", "Grass-Pavement")
    songs["Sand-Pavement"] = songs[songs["Playing"]].load_premade_effect("Walk_pavement", "Sand-Pavement")

    songs["Grass-Flakes"] = songs[songs["Playing"]].load_premade_effect("Walk_grass", "Grass-Flakes")
    songs["Grass"] = songs[songs["Playing"]].load_premade_effect("Walk_grass", "Grass")

    songs["Sand"] = songs[songs["Playing"]].load_premade_effect("Walk_sand", "Sand")
    songs["Sand-Flakes"] = songs[songs["Playing"]].load_premade_effect("Walk_sand", "Sand-Flakes")
    songs["Sand-Grass"] = songs[songs["Playing"]].load_premade_effect("Walk_sand", "Sand-Grass")
    songs["Sand-Wet"] = songs[songs["Playing"]].load_premade_effect("Walk_wet_sand", "Sand-Wet")

    songs["Sand-Deck"] = songs[songs["Playing"]].load_premade_effect("Walk_deck", "Sand-Deck")
    songs["Deck"] = songs[songs["Playing"]].load_premade_effect("Walk_deck", "Deck")

    songs["Water"] = songs[songs["Playing"]].load_premade_effect("Walk_water", "Water")

    songs["SandClay-Pavement"] = songs[songs["Playing"]].load_premade_effect("Walk_clay", "SandClay-Pavement")
    songs["Clay"] = songs[songs["Playing"]].load_premade_effect("Walk_clay", "Clay")
    songs["Clay-Stairs"] = songs[songs["Playing"]].load_premade_effect("Walk_clay", "Clay-Stairs")
    songs["Clay-Flakes"] = songs[songs["Playing"]].load_premade_effect("Walk_clay", "Clay-Flakes")

    songs["Dark Grass-Pavement"] = songs[songs["Playing"]].load_premade_effect("Walk_stuffed_grass", "Dark Grass-Pavement")
    songs["Stuffed Grass"] = songs[songs["Playing"]].load_premade_effect("Walk_stuffed_grass", "Stuffed Grass")



    songs["Slashing"] = songs[songs["Playing"]].generate_slash_sound()
    songs["Blunt"] = songs[songs["Playing"]].generate_blunt_sound()
    songs["Piercing"] = songs[songs["Playing"]].generate_stabbing_sound()

    # songs["Flash"] = songs[songs["Playing"]].load_premade_effect("Spell_flash", "Flash")


    songs[songs["Playing"]].channel0.set_volume(S.VOLUME)
    songs[songs["Playing"]].channel1.set_volume(S.Effect_VOLUME)

    dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)

    I.th.start_threads(data, mob, spells, decorations, rooms, npc, gifs, songs, items)
    I.GB.set_guard_posts(decorations, mob)
    return decorations, gifs, items, spells, mob, npc, songs, dim_surface, collide, pressed, data

def Start(screen, clock, rooms):
    decorations, gifs, items, spells, mob, npc, songs, dim_surface, collide, pressed, data = reset(rooms, screen)
    # I.S.Player_sprite = I.S.create_sprite_Player(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + I.info.OFFSCREEN[1])
    # I.S.LayeredGroup.add(I.S.Player_sprite, layer=6)

    while S.PLAY:
        # time = I.T.start_mesure()
        I.S.Sub_image1.empty()
        I.S.Sub_image2.empty()

        for event in I.pg.event.get():
            if event.type == I.pg.QUIT:
                S.PLAY = False
            elif event.type == I.pg.VIDEORESIZE:
                # Update window size based on new dimensions
                S.SCREEN_WIDTH, S.SCREEN_HEIGHT = event.w, event.h
                screen = I.pg.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.RESIZABLE)
            elif event.type == I.pg.KEYDOWN:
                pressed = handle_keydown(event, data, spells, gifs, items, songs, rooms)
            elif event.type == I.pg.KEYUP:
                # I.T.print_coordinates(event, data["Zoom_rect"])
                pressed = handle_keyup(event, pressed, gifs, songs, screen, items, data, collide, spells, clock, rooms, npc, decorations, mob)


        collide = br.New_Update(data, decorations, gifs, rooms, clock, screen, spells, npc, mob, songs, items) # on average 20 ms, while dead: 9 ms
        if not I.info.RESET:
            I.PB.Get_walking_on(rooms, data)

            queue_checks(data, decorations, gifs, mob, rooms)

            if S.WINDOW == "Settings":
                handle_esc_click(screen, clock)

            I.TB.handle_hoe(collide, data, items, decorations, screen, rooms)

            I.GB.handle_guards(collide, data, screen, npc, items, decorations, gifs, rooms, clock, spells, mob)

            handle_music(songs, collide, data, items) # average 0.028 ms

            update_display_text(screen, gifs, data, collide) # max 0.008 ms

            if not S.GOD_MODE:
                I.PB.update_char_bar(screen, data, gifs, items, rooms, clock, spells, npc) # max 1.11 ms
                I.SB.display_spell_bar(screen, spells, gifs) # max 2.05 ms
                display_playing_bar(screen, data)

            if rooms.type in ["Village"]:
                dim_surface.fill((0, 0, 0, I.info.DIM))
                screen.blit(dim_surface, (0, 0))

            I.pg.display.flip()  # max 4.5 ms
            clock.tick(S.FRAMERATE)
        else:
            if I.info.RESET == "Stairs":
                pos = I.info.OFFSCREEN
            decorations, gifs, items, spells, mob, npc, songs, dim_surface, collide, pressed, data = reset(rooms, screen)
            if I.info.RESET == "Stairs":
                I.info.OFFSCREEN = pos
            I.info.RESET = False

        # I.T.end_mesure(time)
        # if avg_time > 20:
        #     Ff.display_text_player("Lagging " + str(avg_time), 4000)


def handle_keyup(event, pressed, gifs: dict, songs, screen, items, data, collide, spells, clock, rooms, npc, decorations, mobs):
    if event.key == pressed:
        curr_song = songs["Playing"]
        if pressed == I.pg.K_c:
            songs[curr_song].channel0.pause()
            I.PB.interract(collide, data, gifs, items, screen, songs, spells, clock, rooms, npc, decorations, mobs)
            songs[curr_song].channel0.unpause()
        elif pressed == I.pg.K_x:
            I.QB.tutorial_hit()
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

def handle_keydown(event, data, spells, gifs: dict, items, songs, rooms):
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
            handle_combat(items, gifs, rooms)
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
            if rooms.size == ["1", "1", "1", "1"]:
                I.info.AXE = [I.pg.Rect(150 + attack_direction[orientation][0] + I.info.OFFSCREEN[0] / 4, 85 + attack_direction[orientation][1] + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100), float(speed) * I.info.BASE_ATTACKING_SPEED]
            else:
                I.info.AXE = [I.pg.Rect(attack_direction[orientation][0] * 4 + I.info.OFFSCREEN[0] + 600, attack_direction[orientation][1] * 5 + I.info.OFFSCREEN[1] + 300, 40, 50), float(speed) * I.info.BASE_ATTACKING_SPEED]  # Player rect (if it gets hit with other rect. colide is set to True

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
            if rooms.size == ["1", "1", "1", "1"]:
                I.info.PICAXE = [I.pg.Rect(150 + attack_direction[orientation][0] + I.info.OFFSCREEN[0] / 4, 85 + attack_direction[orientation][1] + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100), float(speed) * I.info.BASE_ATTACKING_SPEED]
            else:
                I.info.PICAXE = [I.pg.Rect(attack_direction[orientation][0] * 4 + I.info.OFFSCREEN[0] + 600, attack_direction[orientation][1] * 5 + I.info.OFFSCREEN[1] + 300, 40, 50), float(speed) * I.info.BASE_ATTACKING_SPEED]  # Player rect (if it gets hit with other rect. colide is set to True

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
                    # gifs[spell].repeat = 0
                    data["Player"]["mana"] = (data["Player"]["mana"][0] - int(spells.spell_dict[spell]["mana"]), data["Player"]["mana"][1])
                else:
                    Ff.display_text_player("Not enough MANA", 3000)

    return pressed

def keypress_handle(screen, data, song, items, spells, gifs, rooms, clock, decorations):
    keys = I.pg.key.get_pressed()
    dx = (keys[I.pg.K_RIGHT] - keys[I.pg.K_LEFT])
    dy = (keys[I.pg.K_DOWN] - keys[I.pg.K_UP])
    if dx != 0 or dy != 0:
        song[song["Playing"]].play_effect(I.info.WALKING_ON)
    I.QB.tutorial_quest_walk(dx, dy)
    if keys[I.pg.K_z] and data["Player"]["Exhaustion"][0] > 30:
        I.info.FAST = 2
    elif data["Player"]["Exhaustion"][0] < 30 and keys[I.pg.K_z]:
        Ff.display_text_player("Too Exhausted to run", 1000)
    elif not keys[I.pg.K_z]:
        I.info.FAST = 1
    if keys[I.pg.K_u] and not data["Player"]["dead"] and True not in [keys[I.pg.K_i], keys[I.pg.K_q], keys[I.pg.K_o], keys[I.pg.K_m], keys[I.pg.K_p], keys[I.pg.K_g]]:
        dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))
        screen.blit(dim_surface, (0, 0))
        curr_song = song["Playing"]
        song[curr_song].channel0.pause()
        I.SB.spell_book(screen, data, spells, gifs)
        song[curr_song].channel0.unpause()
    elif keys[I.pg.K_i] and not data["Player"]["dead"] and True not in [keys[I.pg.K_u], keys[I.pg.K_q], keys[I.pg.K_o], keys[I.pg.K_m], keys[I.pg.K_p], keys[I.pg.K_g]]:
        dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))
        screen.blit(dim_surface, (0, 0))
        curr_song = song["Playing"]
        song[curr_song].channel0.pause()
        I.BB.BackPack(screen, items, data["Player"])
        song[curr_song].channel0.unpause()
        I.QB.tutorial_backpack()

    elif keys[I.pg.K_q] and not data["Player"]["dead"] and True not in [keys[I.pg.K_u], keys[I.pg.K_i], keys[I.pg.K_o], keys[I.pg.K_m], keys[I.pg.K_p], keys[I.pg.K_g]]:
        I.QB.handle_q_click(screen, song, items)
    elif keys[I.pg.K_o] and True not in [keys[I.pg.K_u], keys[I.pg.K_i], keys[I.pg.K_q], keys[I.pg.K_m], keys[I.pg.K_p], keys[I.pg.K_g]]:
        I.PB.handle_display_stats(screen, data, gifs)
    elif keys[I.pg.K_m] and True not in [keys[I.pg.K_u], keys[I.pg.K_i], keys[I.pg.K_q], keys[I.pg.K_o], keys[I.pg.K_p], keys[I.pg.K_g]]:
        I.MapB.handle_display_map(screen, rooms, data, decorations)
    elif keys[I.pg.K_p] and True not in [keys[I.pg.K_u], keys[I.pg.K_i], keys[I.pg.K_q], keys[I.pg.K_o], keys[I.pg.K_m], keys[I.pg.K_g]]:
        Ff.display_text_player("Pets not programed yet", 1000)
    if keys[I.pg.K_g] and keys[I.pg.K_o] and keys[I.pg.K_d] and keys[I.pg.K_LSHIFT]:
        dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))
        screen.blit(dim_surface, (0, 0))
        handle_cheats(screen, data, rooms, clock, items)
    return dx, dy


def update_display_text(screen, gifs: dict, data, collide):
    if I.info.TEXT:  # Check if the dictionary is not empty
        if I.info.CURRENT_ROOM["Type"] in ["Village"]:
            color = "black"
        else:
            color = "white"
        push = S.SCREEN_HEIGHT * 0.85
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

def handle_combat(items, gifs, rooms):
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
    if rooms.size == ["1", "1", "1", "1"]:
        I.info.COMBAT_RECT = [I.pg.Rect(150 + attack_direction[orientation][0] + I.info.OFFSCREEN[0] / 4, 80 + attack_direction[orientation][1] + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 80), float(speed) * I.info.BASE_ATTACKING_SPEED]  # Player rect (if it gets hit with other rect. colide is set to True
    else:
        I.info.COMBAT_RECT = [I.pg.Rect(attack_direction[orientation][0] * 4 + I.info.OFFSCREEN[0] + 600 ,attack_direction[orientation][1] * 5 + I.info.OFFSCREEN[1] + 300, 40, 50), float(speed) * I.info.BASE_ATTACKING_SPEED]  # Player rect (if it gets hit with other rect. colide is set to True

def handle_music(song, collide, data, items):
    # print(song["Playing"])
    if data["Player"]["dead"]:
        if song["Playing"] != "Ghost":
            song["Playing"] = "Ghost"
    elif song["Playing"] != "Background":
        song["Playing"] = "Background"
    curr_song = song["Playing"]
    song[curr_song].channel0.set_volume(S.VOLUME)
    song[curr_song].channel1.set_volume(S.Effect_VOLUME)
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

    if song[curr_song].effect_flag and I.pg.time.get_ticks() - song[curr_song].effect_time > 500: # HARDCODED TO ONLY PLAY 500 ms OF EFFECT
        print("stoping: ", I.pg.time.get_ticks())
        song[curr_song].channel1.stop()
        song[curr_song].effect_flag = False

def handle_cheats(screen, data, rooms, clock, items):
    running = True
    input_text = ""
    rect = I.pg.Rect(100, 500, S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.2)
    I.pg.draw.rect(screen, "white", rect)
    iteration = 0
    pressed = 0
    while running:
        for event in I.pg.event.get():
            keys = I.pg.key.get_pressed()
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_ESCAPE:
                    running = False
                    pressed = event.key
                elif event.key == I.pg.K_RETURN:
                    error = 1
                    command = input_text.split(":")[0]
                    value = input_text.split(":")[1]
                    if command == "GET":
                        value = value.split(",")
                        if items.item_dict.get(value[0].split("|")[0]) == None:
                            input_text = "Item Doesn't Exist"
                        else:
                            error = 0
                    else:
                        error = 0
                    if error == 0:
                        running = False
                        pressed = event.key
                        Ff.display_text_player("CHEATER!!!!!!!!!!!!", 20000)
                elif event.key == I.pg.K_BACKSPACE:
                    if keys[I.pg.K_LCTRL]:
                        length = len(input_text)
                        for i in range(1, length):
                            if input_text[length - i] == ":":
                                break
                            else:
                                input_text = input_text[:-1]
                    else:
                        input_text = input_text[:-1]


                elif event.key == I.pg.K_DOWN:
                    input_text = I.A.COMMANDS[iteration]
                    if iteration == 1:
                        input_text += ":x,y"
                    if iteration == 2:
                        input_text += ":RoomName"
                    if iteration == 3:
                        input_text += ":dim_value"
                    if iteration == 4:
                        input_text += ":item_name,amount"
                    iteration += 1
                    if iteration >= len(I.A.COMMANDS):
                        iteration = 0
            if event.type == I.pg.TEXTINPUT:
                input_text += event.text
        I.pg.draw.rect(screen, "white", rect)
        Ff.display_text(screen, input_text, 16, [100, 500], "red")
        I.pg.display.flip()

    if pressed == I.pg.K_RETURN:
        command = input_text.split(":")[0]
        value = input_text.split(":")[1]
        if command in I.A.COMMANDS:
            if command == I.A.COMMANDS[0]:
                S.GOD_MODE = bool(int(value))
            elif command in [I.A.COMMANDS[1], I.A.COMMANDS[4]]:
                value = value.split(",")
                if I.A.COMMANDS[1] == command:
                    data["Zoom_rect"] = I.pg.Rect(int(value[0]), int(value[1]), data["Zoom_rect"].w, data["Zoom_rect"].h)
                elif I.A.COMMANDS[4] == command:
                    Ff.add_to_backpack(value[0], value[1], items)
            elif command == I.A.COMMANDS[2]:
                rooms.select_room(value)
                I.info.CURRENT_ROOM = {"name": value, "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": "Village"}
                # Start(screen, clock, rooms)
                I.info.RESET = True
            elif command == I.A.COMMANDS[3]:
                I.info.DIM = int(value)

def display_playing_bar(screen, data):
    if S.PLAYING_BAR_SCREEN == 0:
        S.PLAYING_BAR_SCREEN = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)

        Ff.add_image_to_screen(S.PLAYING_BAR_SCREEN, S.PLAYING_PATH["Spell_bar"], (0, S.SCREEN_HEIGHT * 0.91,  S.SCREEN_WIDTH / 6,  S.SCREEN_HEIGHT / 12))
        icon_w = S.SCREEN_WIDTH / 40
        icon_h = S.SCREEN_HEIGHT / 20
        icon_y = S.SCREEN_HEIGHT * 0.925
        gap_x = 10
        map_icon_path = S.local_path + "/static/images/Playing/Map_icon.png"
        backpack_icon_path = S.local_path + "/static/images/Playing/Backpack_icon.png"
        stats_icon_path = S.local_path + "/static/images/Playing/Stats_icon.png"
        pets_icon_path = S.local_path + "/static/images/Playing/Pets_icon.png"
        settings_icon_path = S.local_path + "/static/images/Playing/Settings_icon.png"
        Ff.add_image_to_screen(S.PLAYING_BAR_SCREEN, backpack_icon_path, (8, icon_y, icon_w, icon_h))
        Ff.display_text(S.PLAYING_BAR_SCREEN, "[I]", 1, (8, icon_y+icon_h - 2), "black")
        Ff.add_image_to_screen(S.PLAYING_BAR_SCREEN, stats_icon_path, (icon_w + gap_x + 8, icon_y, icon_w, icon_h))
        Ff.display_text(S.PLAYING_BAR_SCREEN, "[O]", 1, (icon_w + gap_x + 8, icon_y+icon_h - 2), "black")
        Ff.add_image_to_screen(S.PLAYING_BAR_SCREEN, pets_icon_path, ((icon_w + gap_x)*2 + 8, icon_y, icon_w, icon_h))
        Ff.display_text(S.PLAYING_BAR_SCREEN, "[P]", 1, ((icon_w + gap_x)*2 + 8, icon_y+icon_h - 2), "black")
        Ff.add_image_to_screen(S.PLAYING_BAR_SCREEN, map_icon_path, ((icon_w + gap_x)*3 + 7, icon_y, icon_w, icon_h))
        Ff.display_text(S.PLAYING_BAR_SCREEN, "[M]", 1, ((icon_w + gap_x)*3 + 7, icon_y+icon_h - 2), "black")
        Ff.add_image_to_screen(S.PLAYING_BAR_SCREEN, settings_icon_path, ((icon_w + gap_x)*4 + 6, icon_y, icon_w, icon_h))
        Ff.display_text(S.PLAYING_BAR_SCREEN, "[Esc]", 1, ((icon_w + gap_x)*4 + 6, icon_y+icon_h - 2), "black")

    screen.blit(S.PLAYING_BAR_SCREEN, (0, 0))

def queue_checks(data, decorations, gifs, mob, rooms):
    get = 0
    for i in data["Queue_to_be_removed"].queue:
        id, option, rect, case = i
        if case == "decor-decor":
            if decorations.decor_dict[option].get(id) == None:
                Ff.update_map_view(id, option, rect, "add", rooms.name)
                get = 1
        elif "decor-mob" in case:
            word, mob_word = case.split("-")
            mob_name = mob_word.split(":")[1]
            if decorations.decor_dict[option].get(id) == None:
                mob_dict = I.mob_data.read_db()
                cur_dict = mob_dict[mob_name]
                frame_count = Ff.count_png_files(cur_dict["path"])
                path = cur_dict["path"]
                if mob.get(mob_name) == None:
                    mob[mob_name] = I.mob_data.Mob(name=mob_name, exp=cur_dict["exp"], hp=cur_dict["health"], allignment=cur_dict["allignment"], count=1, damage=cur_dict["damage"].split(":"), speed=cur_dict["speed"], path=path, delay=(cur_dict["delay"], cur_dict["delay"]), decor=False, drop=cur_dict["drop"])
                else:
                    mob[mob_name].count = mob[mob_name].count[0] + 1, mob[mob_name].count[1] + 1
                    mob[mob_name].mobs.append(mob[mob_name].create_mob(mob[mob_name].count[0]))
                    # self.mobs = [self.create_mob(i) for i in range(count)]  # Create initial list of mobs
                print(mob[mob_name].count)
                mob[mob_name].spawn_mob_acurate(cur_dict["path"], frame_count, mob[mob_name].count[0] - 1, rect[0], rect[1])
                get = 1
    if get == 1:
        data["Queue_to_be_removed"].get()
        print("mobs:", I.info.CURRENT_ROOM["Mobs"])
