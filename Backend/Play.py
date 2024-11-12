from Render import Background_Render as br, Main_Menu_render as mr
from Values import Settings as S
from utils import Imports as I, Frequent_functions as Ff
from Backend import Settings_backend as SB, Setup_pygame as SP

def reset(rooms, screen):
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

    data = br.Start(mob, decorations, spells, rooms, npc, items)

    I.QB.set_tutorial_flag()

    I.BB.update_equiped()

    I.info.LAST_ORIENTAION = (0, 0)
    songs = {"Background": I.Songs.Song("Background", I.A.background_music),
             "Ghost": I.Songs.Song("Ghost", I.A.dead_music),
             "Playing": "Background",
             }
    songs["Slashing"] = songs[songs["Playing"]].generate_slash_sound()
    songs["Blunt"] = songs[songs["Playing"]].generate_blunt_sound()
    songs["Piercing"] = songs[songs["Playing"]].generate_stabbing_sound()

    dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)

    I.th.start_threads(data, mob, spells, decorations, rooms, npc, gifs, songs, items)
    I.GB.set_guard_posts(decorations, mob)
    return decorations, gifs, items, spells, mob, npc, songs, dim_surface, collide, pressed, data

def Start(screen, clock, rooms):

    decorations, gifs, items, spells, mob, npc, songs, dim_surface, collide, pressed, data = reset(rooms, screen)

    while S.PLAY:
        for event in I.pg.event.get():
            if event.type == I.pg.QUIT:
                S.PLAY = False
            if event.type == I.pg.KEYDOWN:
                pressed = handle_keydown(event, data, spells, gifs, items, songs, rooms)
            if event.type == I.pg.KEYUP:
                I.T.print_coordinates(event, data["Zoom_rect"])
                pressed = handle_keyup(event, pressed, gifs, songs, screen, items, data, collide, spells, clock, rooms, npc, decorations)


        collide = br.New_Update(data, decorations, gifs, rooms, clock, screen, spells, npc, mob, songs, items) # on average 20 ms, while dead: 9 ms

        if not I.info.RESET:
            I.PB.Get_walking_on(rooms, data)

            if S.WINDOW == "Settings":
                handle_esc_click(screen, clock)

            I.TB.handle_hoe(collide, data, items, decorations, screen)

            I.GB.handle_guards(collide, data, screen, npc, items, decorations, gifs, rooms, clock, spells)

            handle_music(songs, collide, data, items) # average 0.028 ms
            update_display_text(screen, gifs, data, collide) # max 0.008 ms

            I.PB.update_char_bar(screen, data, gifs, items, rooms, clock, spells, npc) # max 1.11 ms
            I.SB.display_spell_bar(screen, spells, gifs) # max 2.05 ms

            if rooms.type in ["Village"]:
                dim_surface.fill((0, 0, 0, I.info.DIM))
                screen.blit(dim_surface, (0, 0))

            I.pg.display.flip()  # max 4.5 ms
            clock.tick(I.info.TICK)

        else:
            if I.info.RESET == "Stairs":
                pos = I.info.OFFSCREEN
            decorations, gifs, items, spells, mob, npc, songs, dim_surface, collide, pressed, data = reset(rooms, screen)
            if I.info.RESET == "Stairs":
                I.info.OFFSCREEN = pos
            I.info.RESET = False


def handle_keyup(event, pressed, gifs: dict, songs, screen, items, data, collide, spells, clock, rooms, npc, decorations):
    if event.key == pressed:
        curr_song = songs["Playing"]
        if pressed == I.pg.K_c:
            songs[curr_song].channel0.pause()
            I.PB.interract(collide, data, gifs, items, screen, songs, spells, clock, rooms, npc, decorations)
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
                    data["Player"]["mana"] = (data["Player"]["mana"][0] - int(spells.spell_dict[spell]["mana"]), data["Player"]["mana"][1])
                else:
                    Ff.display_text_player("Not enough MANA", 3000)

    return pressed

def keypress_handle(screen, data, song, items, spells, gifs, rooms, clock):
    keys = I.pg.key.get_pressed()
    dx = (keys[I.pg.K_RIGHT] - keys[I.pg.K_LEFT])
    dy = (keys[I.pg.K_DOWN] - keys[I.pg.K_UP])
    I.QB.tutorial_quest_walk(dx, dy)
    if keys[I.pg.K_z] and data["Player"]["Exhaustion"][0] > 30:
        I.info.FAST = 2
    elif not keys[I.pg.K_z]:
        I.info.FAST = 1
    if keys[I.pg.K_u] and not data["Player"]["dead"]:
        dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))
        screen.blit(dim_surface, (0, 0))
        curr_song = song["Playing"]
        song[curr_song].channel0.pause()
        I.SB.spell_book(screen, data, spells, gifs)
        song[curr_song].channel0.unpause()
    elif keys[I.pg.K_i] and not data["Player"]["dead"]:
        dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))
        screen.blit(dim_surface, (0, 0))
        curr_song = song["Playing"]
        song[curr_song].channel0.pause()
        I.BB.BackPack(screen, items, data["Player"])
        song[curr_song].channel0.unpause()
        I.QB.tutorial_backpack()

    elif keys[I.pg.K_q] and not data["Player"]["dead"]:
        I.QB.handle_q_click(screen, song, items)
    elif keys[I.pg.K_g] and keys[I.pg.K_o] and keys[I.pg.K_d] and keys[I.pg.K_LSHIFT]:
        dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))
        screen.blit(dim_surface, (0, 0))
        handle_cheats(screen, data, rooms, clock, items)
    return dx, dy

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

def handle_cheats(screen, data, rooms, clock, items):
    running = True
    input_text = ""
    rect = I.pg.Rect(100, 500, S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.2)
    I.pg.draw.rect(screen, "white", rect)
    iteration = 0
    while running:
        for event in I.pg.event.get():
            keys = I.pg.key.get_pressed()
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_ESCAPE:
                    running = False
                elif event.key == I.pg.K_RETURN:
                    running = False
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



