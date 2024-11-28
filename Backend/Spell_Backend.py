from PIL.ImageChops import screen
from PIL.ImageSequence import all_frames

from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S

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
        mobs[mob_name + " Mine"] = I.mob_data.Mob(name=mob_name + " Mine", exp=cur_dict["exp"], hp=cur_dict["health"], allignment=7, count=3, damage=cur_dict["damage"].split(":"), speed=cur_dict["speed"], path=path, delay=(cur_dict["delay"], cur_dict["delay"]), decor=False, drop="Bone,1,1")

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
    if gifs[name].start_gif == False:
        data["Player"]["stats"]["Summoning"] = data["Player"]["stats"]["Summoning"] + 5

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
    if gifs[name].start_gif == False:
        data["Player"]["stats"]["Healing"] = data["Player"]["stats"]["Healing"] + 5


def bolt_spell_handle(spells, gifs, spell_name, decorations, song, data, mobs, items, sub_image, player, rooms):
    zoom_rect = data["Zoom_rect"]
    curr_song = song["Playing"]
    sound_type = {"Force": song[curr_song].generate_magic_sound(),
                  "Fire": song[curr_song].generate_fire_sound(),
                  "Cold": song[curr_song].generate_cold_sound(),
                  "Necrotic": song[curr_song].generate_cold_sound(),
                  }
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
            spells.init_cast[spell_name] = I.pg.Rect(S.SCREEN_WIDTH / 2 + S.SCREEN_WIDTH / 20 - I.info.Player_rect.w * 10 + I.info.OFFSCREEN[0],S.SCREEN_HEIGHT / 2 - I.info.Player_rect.h * 10 + I.info.OFFSCREEN[1], size[0], size[1])
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
        if rooms.size == ["1", "1", "1", "1"]:
            rect = I.pg.Rect(spells.init_cast[spell_name].x - zoom_rect.x + I.info.Player_rect.x - dir[0] * gifs[spell_name].current_frame * 6,
                             spells.init_cast[spell_name].y - zoom_rect.y + I.info.Player_rect.y - dir[1] * gifs[spell_name].current_frame * 6, size[0], size[1])
        else:
            rect = I.pg.Rect(spells.init_cast[spell_name].x - dir[0] * gifs[spell_name].current_frame * 12 * 2,
                             spells.init_cast[spell_name].y - dir[1] * gifs[spell_name].current_frame * 12 * 2, size[0], size[1])

        sub_image.blit(frame, rect)
        if rooms.size == ["1", "1", "1", "1"]:
            collide_with_decor = rect.collidelist(decorations.displayed_rects_full)
            if collide_with_decor != -1:  # if hits any decor
                type = spells.spell_dict[spell_name]["type"]
                song[curr_song].play_effect(sound_type[type])
                gifs[spell_name].start_gif = False
                index = rect.collidelist(decorations.displayed_rects_full)
                add_effect_to_decor(decorations, index, type, rooms, gifs)

                # decorations.effected_decor[index] = type
            else:
                for key in mobs.keys():
                    for current_mob in mobs[key].mobs:
                        mob_rect = I.pg.Rect(current_mob["rect"][0].x - zoom_rect.x, current_mob["rect"][0].y - zoom_rect.y, current_mob["rect"][0].w, current_mob["rect"][0].h)
                        if rect.colliderect(mob_rect):
                            mobs[key].deal_damage(current_mob, player, spells.spell_dict[spell_name], items, gifs, rooms, data)
                            gifs[spell_name].start_gif = False  # IF COMMENTED OUT, MAKES A SPELL GO THROUGH MULTIPLE ENEMIES
                            type = spells.spell_dict[spell_name]["type"]
                            gifs[type].Start_gif(type, current_mob)
                            song[curr_song].play_effect(sound_type[type])
    if gifs[spell_name].start_gif == False:
        data["Player"]["stats"]["Sorcery"] = data["Player"]["stats"]["Sorcery"] + 5

def cast_spell_handle(sub_image, data, spells, gifs, mob, song, decorations, items, rooms, screen):
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
                elif "SELF" in spells.spell_dict[spell_name]["direction"]:
                    self_spell_cast_handle(spells, spell_name, gifs, sub_image, rooms, data, mob, decorations)
                else:
                    bolt_spell_handle(spells, gifs, spell_name, decorations, song, data, mob, items, sub_image, data["Player"], rooms)
            else:
                # RESET DIRECTION OF FIRE
                spells.direction[spell_name] = 0
                spells.init_cast[spell_name] = 0

def fill_spellbook(screen, gifs, spells, data):
    rect = screen.get_rect()
    book = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Spellbook_Empty"], [rect.center[0] * 0.5, rect.center[1] * 0.25, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT * 0.75])

    if I.info.SPELLBOOK_COORDINATES_X == {}:
        I.info.SPELLBOOK_COORDINATES_X, I.info.SPELLBOOK_COORDINATES_Y = I.BB.bag_coordinates(screen, book)

    item_w = list(I.info.SPELLBOOK_COORDINATES_X.values())[1] - list(I.info.SPELLBOOK_COORDINATES_X.values())[0]
    item_h = list(I.info.SPELLBOOK_COORDINATES_Y.values())[1] - list(I.info.SPELLBOOK_COORDINATES_Y.values())[0]
    for content in I.info.SPELLBOOK_CONTENT.keys():
        if int(data["Player"]["Level"]) >= int(spells.spell_dict[content]["level"]):
            row, collumn = I.info.SPELLBOOK_CONTENT[content]
            Ff.add_image_to_screen(screen, gifs[content].frame_paths[0][:-5] + "icon.png", [list(I.info.SPELLBOOK_COORDINATES_X.values())[row], list(I.info.SPELLBOOK_COORDINATES_Y.values())[collumn], item_w, item_h])

def spell_book(screen, data, spells, gifs):
    fill_spellbook(screen, gifs, spells, data)
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
                            if block == (row, collum) and int(spells.spell_dict[spell]["level"]) <= int(data["Player"]["Level"]):
                                selected = spell
                    else:
                        spells.selected_spell[block[0]] = selected
                        selected = 0
                pressed = 0
        fill_spellbook(screen, gifs, spells, data)
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

def display_spell_bar(screen, spells, gifs: dict):
    Ff.add_image_to_screen(screen, S.PLAYING_PATH["Spell_bar"], (S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.89,  S.SCREEN_WIDTH / 5,  S.SCREEN_HEIGHT / 10))
    spell_w = S.SCREEN_WIDTH / 28
    spell_h = S.SCREEN_HEIGHT / 12
    spell_y = S.SCREEN_HEIGHT * 0.896
    for pos, spell in spells.selected_spell.items():
        spell_x = S.SCREEN_WIDTH * 0.804 + pos * 25
        Ff.add_image_to_screen(screen, gifs[spell].frame_paths[0][:-5] + "icon.png", (spell_x, spell_y, spell_w, spell_h))
        # if spells.spell_cooloff.get(spell) != None and spells.spell_cooloff[spell] != 0 and spells.spell_cooloff[spell] != spells.spell_dict[spell]["recharge"]:
        if spells.spell_cooloff.get(spell) != None and spells.spell_cooloff[spell] != 0:
            cover = I.pg.Surface((spell_w, int(spell_h * spells.spell_cooloff[spell] / spells.spell_dict[spell]["recharge"])), I.pg.SRCALPHA)
            cover.fill((0, 0, 0, 128))
            screen.blit(cover, (spell_x, spell_y))

def self_spell_cast_handle(spells, spell_name, gifs, sub_image, rooms, data, mob, decorations):
    # print(screen)
    if rooms.size == ['1', '1', '1', '1']:
        me = I.pg.Rect(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 25 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 10 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 22, S.SCREEN_HEIGHT / 8)
        frame = gifs[spell_name].next_frame(1)
        frame_has_changed = gifs[spell_name].frame_changed
        size = frame.get_size()
        sub_image.blit(frame, (128 + I.info.OFFSCREEN[0] / 4, 60 + I.info.OFFSCREEN[1] / 4))
        self_spell_rect = I.pg.Rect(128 + I.info.OFFSCREEN[0] / 4, 60 + I.info.OFFSCREEN[1] / 4, size[0], size[1])
        # I.T.Make_rect_visible(sub_image, self_spell_rect, "red")

        if frame_has_changed:
            if self_spell_rect.collidelist(decorations.displayed_rects) != -1:  # if hits any decor
                type = spells.spell_dict[spell_name]["type"]
                # song[curr_song].play_effect(sound_type[type])
                # gifs[spell_name].start_gif = False
                index = self_spell_rect.collidelist(decorations.displayed_rects_full)
                add_effect_to_decor(decorations, index, type, rooms, gifs)
                # decorations.effected_decor[index] = type
            """making sure that the damage is dealt when the frame changes not when the code comes here 141 vs 27"""
            for mob_name, mob_class in mob.items():
                for current_mob_dict in mob_class.mobs:
                    mob_rect = current_mob_dict["rect"][0][0] - data["Zoom_rect"].x, current_mob_dict["rect"][0][1] - data["Zoom_rect"].y, current_mob_dict["rect"][0][2], current_mob_dict["rect"][0][3]
                    # I.T.Make_rect_visible(sub_image, mob_rect, "blue")
                    """got the mob that was hit and it's class/dict"""
                    if self_spell_rect.colliderect(mob_rect):
                        """mob collides with the spell"""
                        damage = spells.spell_dict[spell_name]["damage"]
                        if "max" in damage:
                            """if max is in damage aka spell doesn't dissappear after hit"""
                            max_damage = int(damage[damage.find("max"):].split(",,")[0].replace("max", ""))
                            all_frames = gifs[spell_name].frame_count
                            current_frame = gifs[spell_name].current_frame
                            # print(max_damage, all_frames, current_frame)
                            can_deal_damage = I.random.random() < all_frames / max_damage
                            if can_deal_damage:
                                mob_class.deal_damage(current_mob_dict, data["Player"], spells.spell_dict[spell_name], 0, gifs, rooms, data)
                                # S.DUMMY_VALUE_int += 1
                        else:
                            """damage dissappears after being hit"""
                            mob_class.deal_damage(current_mob_dict, data["Player"], spells.spell_dict[spell_name], 0, gifs, rooms, data)

        # print(S.DUMMY_VALUE_int)

        # xy = data["Zoom_rect"].x + 145, data["Zoom_rect"].y + 82
        # me = I.pg.Rect(xy[0], xy[1], 100, 100)

def add_effect_to_decor(decorations, index, effect, rooms, gifs):
    # option, id = decorations.names_with_id[index]
    # decor = decorations.decor_dict[option][id]
    decor = Ff.get_decor_by_id(index, decorations, rooms)
    if decor == None:
        print("doesn't work")
        return
    if decor["effect"] == "":
        decor["effect"] = effect + ":" + str(I.pg.time.get_ticks())
        gifs[effect].Start_gif(effect, decor["rect"])
    elif "Fire" in decor["effect"] and "Cold" in effect:
        fire_str_id = decor["effect"].find("Fire")
        current_effect = decor["effect"][fire_str_id:].split(",,")[0]
        decor["effect"] = decor["effect"].replace(current_effect, "")
    elif "Cold" in decor["effect"] and "Fire" in effect:
        Cold_str_id = decor["effect"].find("Cold")
        current_effect = decor["effect"][Cold_str_id:].split(",,")[0]
        decor["effect"] = decor["effect"].replace(current_effect, "")
    elif effect not in decor["effect"]:
        decor["effect"] += ",," + effect + ":" + str(I.pg.time.get_ticks())
        gifs[effect].Start_gif(effect, decor["rect"])

def spell_effect_render_on_decor(sub_image, decor, gifs, data):
    effects_not_supported_by_decor = ["", "UNLOCKED", "LOCKED", "NoPLANT"]
    if decor["effect"] not in effects_not_supported_by_decor:
        for effect in decor["effect"].split(",,"):
            if "TIME" in effect:
                continue
            if effect not in effects_not_supported_by_decor:
                e, t = effect.split(":")
                if e in ["Force"]:
                    frame = gifs[e].next_frame(1)
                    if gifs[e].start_gif == False:
                        decor["effect"] = decor["effect"].replace(",," + effect, "")
                        decor["effect"] = decor["effect"].replace(effect, "")
                else:
                    frame = gifs[e].next_frame(-1)
                if "Guard" in decor["name"]:
                    I.info.CRIMINAL = {
                        "Charge": "Assault",
                        "Fine": 100,
                        "Prison_time": 180
                    }
                frame = I.pg.transform.scale(frame, (decor["rect"].w / 2, decor["rect"].h / 3))
                decor_x = decor["rect"].x + decor["rect"].w / 4 - data["Zoom_rect"].x
                decor_y = decor["rect"].y + decor["rect"].h / 3 - data["Zoom_rect"].y
                sub_image.blit(frame, (decor_x, decor_y))