from Render import Background_Render as br
from Values import Settings as S
from utils import Imports as I, Frequent_functions as Ff
import random

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

def Start(screen, clock):
    mob = {
        "Slime_S": I.mob_data.Mob(name="Slime_S", exp=10, hp=8, allignment=5, count=20, damage=(2, "blunt"), speed=4),
        "Pig": I.mob_data.Mob(name="Pig", exp=5, hp=6, allignment=4, count=20, damage=(1, "blunt"), speed=6),
           }
    gifs = {"ghost": I.gifs.Gif(name="Dead", frame_count=8, initial_path=S.PLAYING_PATH["Dead"], delay=50),
            "Portal": I.gifs.Gif(name="Portal", frame_count=34, initial_path=S.PLAYING_PATH["Portal"], delay=100),
            "Blunt": I.gifs.Gif(name="Blunt", frame_count=S.COMBAT_PATH["Blunt"][1], initial_path=S.COMBAT_PATH["Blunt"][0], delay=10),
            "Slashing": I.gifs.Gif(name="Slashing", frame_count=S.COMBAT_PATH["Slashing"][1], initial_path=S.COMBAT_PATH["Slashing"][0], delay=50),
            "Piercing": I.gifs.Gif(name="Piercing", frame_count=S.COMBAT_PATH["Piercing"][1], initial_path=S.COMBAT_PATH["Piercing"][0], delay=10),
            "Force": I.gifs.Gif(name="Force", frame_count=S.COMBAT_PATH["Blunt"][1], initial_path=S.COMBAT_PATH["Blunt"][0], delay=10),
            "Fire": I.gifs.Gif(name="Fire", frame_count=S.COMBAT_PATH["Fire"][1], initial_path=S.COMBAT_PATH["Fire"][0], delay=50),
            "Cold": I.gifs.Gif(name="Cold", frame_count=S.COMBAT_PATH["Cold"][1], initial_path=S.COMBAT_PATH["Cold"][0], delay=200),
            "Luna": I.gifs.Gif(name="Luna", frame_count=4, initial_path=S.PLAYING_PATH["Luna"], delay=50),
            "Bear": I.gifs.Gif(name="Bear", frame_count=4, initial_path=S.PLAYING_PATH["Bear"], delay=50),
            "Magic Bolt": I.gifs.Gif(name="Magic Bolt", frame_count=10, initial_path=S.SPELL_PATHS["Magic Bolt"], delay=50),
            "Fire Bolt": I.gifs.Gif(name="Fire Bolt", frame_count=10, initial_path=S.SPELL_PATHS["Fire Bolt"], delay=50),
            "Cold Bolt": I.gifs.Gif(name="Cold Bolt", frame_count=10, initial_path=S.SPELL_PATHS["Cold Bolt"], delay=50),
                 }
    items = I.items.Items()
    spells = I.Spells.Spells()
    collide = [False]
    pressed = 0
    data = br.Start([I.info.START_POS[0], I.info.START_POS[1]], mob)
    last_orientation = (0, 0)

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
                handle_timer_actions(event, timers, data, mob, spells)
            if event.type == I.pg.KEYDOWN:
                pressed = handle_keydown(event, data, spells, gifs)
            if event.type == I.pg.KEYUP:
                pressed = handle_keyup(event, pressed, gifs, songs, screen, items, data, collide)

        collide = br.Update(screen, data, mob, gifs, songs, spells)

        dx, dy, gif_time = keypress_handle(screen, data, songs, items, spells)

        last_orientation = walking(dx, dy, collide, data, last_orientation)

        br.display_char(dx, dy, screen, gifs)

        handle_music(songs, collide, data)

        update_display_text(screen, gifs, data, collide)

        update_char_bar(screen, data, gifs)

        display_spell_bar(screen, spells)

        I.pg.display.flip()
        clock.tick(I.info.TICK)



def handle_keyup(event, pressed, gifs, songs, screen, items, data, collide):
    if event.key == pressed:
        curr_song = songs["Playing"]
        if pressed == I.pg.K_c:
            songs[curr_song].channel0.pause()
            interract(collide, data, gifs, items, screen)
            songs[curr_song].channel0.unpause()
        elif pressed == I.pg.K_x:
            I.info.COMBAT_RECT = 0
        return 0
def handle_keydown(event, data, spells, gifs):
    key_to_slot = {
        I.pg.K_a: 0,
        I.pg.K_s: 2,
        I.pg.K_d: 4,
        I.pg.K_f: 6,
        I.pg.K_g: 8
    }
    pressed = 0
    if event.key == I.pg.K_c:
        pressed = I.pg.K_c
    elif event.key == I.pg.K_x:
        if pressed != I.pg.K_x and not data["Player"]["dead"]:
            handle_combat()
        pressed = I.pg.K_x
    if event.key in [I.pg.K_a, I.pg.K_s, I.pg.K_d, I.pg.K_f, I.pg.K_g]:
        target_slot = key_to_slot[event.key]
        for slot, spell in spells.selected_spell.items():
            if spells.spell_cooloff.get(spell) == None:
                if slot == target_slot and not gifs[spell].start_gif and data["Player"]["mana"][0] >= int(spells.spell_dict[spell]["mana"]):
                    gifs[spell].Start_gif(spell, 1)
                    data["Player"]["mana"] = (data["Player"]["mana"][0] - int(spells.spell_dict[spell]["mana"]), data["Player"]["mana"][1])
            elif spells.spell_cooloff[spell] == 0:
                if slot == target_slot and not gifs[spell].start_gif and data["Player"]["mana"][0] >= int(spells.spell_dict[spell]["mana"]):
                    gifs[spell].Start_gif(spell, 1)
                    data["Player"]["mana"] = (data["Player"]["mana"][0] - int(spells.spell_dict[spell]["mana"]), data["Player"]["mana"][1])



    return pressed
def display_spell_bar(screen, spells):
    Ff.add_image_to_screen(screen, S.PLAYING_PATH["Spell_bar"], (S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.9,  S.SCREEN_WIDTH / 5,  S.SCREEN_HEIGHT / 10))
    for pos, spell in spells.selected_spell.items():
        Ff.add_image_to_screen(screen, S.SPELL_PATHS[spell] + "0.png", (S.SCREEN_WIDTH * 0.803 + pos * 25, S.SCREEN_HEIGHT * 0.91,  S.SCREEN_WIDTH / 25,  S.SCREEN_HEIGHT / 10))
def handle_mob_respawn(mob, data):
    if mob.count[0] < mob.count[1]:
        mob.count = (mob.count[0] + 1, mob.count[1])
        id = mob.count[1] + 1
        mob.mobs.append(mob.create_mob(id))
        data[mob.name] = br.generate_mobs(mob, data["Image_rect"].size)

def handle_timer_actions(event, timers, data, mob, spells):
    if timers["Exhaustion"] == event.type:
        data["Player"]["Exhaustion"] = (data["Player"]["Exhaustion"][0] - 1, data["Player"]["Exhaustion"][1])
    elif timers["Mob_respawn"] == event.type:
        handle_mob_respawn(mob, data)
    elif timers["Harvest"] == event.type:
        harvest_timeout()
    elif timers["Strike"] == event.type:
        I.info.COMBAT_RECT = 0
    elif timers["Walk"] == event.type:
        I.info.CURRENT_STANCE += 1
        if I.info.CURRENT_STANCE > 3:
            I.info.CURRENT_STANCE = 0
    elif timers["mob_gif"] == event.type:
        for key in mob.keys():
            for current_mob in mob[key].mobs:
                current_mob["gif_frame"] = (current_mob["gif_frame"][0] + 1, current_mob["gif_frame"][1])
                if current_mob["gif_frame"][0] == current_mob["gif_frame"][1]:
                    mob[key].move_mobs_randomly()
                    current_mob["gif_frame"] = (0, current_mob["gif_frame"][1])
    elif timers["spell_cooloff"] == event.type:
        for key in spells.spell_cooloff.keys():
            if spells.spell_cooloff[key] != 0:
                spells.spell_cooloff[key] -= 1

    elif timers["healing"] == event.type and I.pg.time.get_ticks() - data["Player"]["Last_hit"] > 20000 and data["Player"]["Exhaustion"][0] >= 90:
        if data["Player"]["hp"][0] < data["Player"]["hp"][1]:
            data["Player"]["hp"] = (data["Player"]["hp"][0] + 1, data["Player"]["hp"][1])
        if data["Player"]["mana"][0] < data["Player"]["mana"][1]:
            data["Player"]["mana"] = (data["Player"]["mana"][0] + 1, data["Player"]["mana"][1])

def handle_timers():
    timers = {}
    EXHAUSTION_TIM = I.pg.USEREVENT + 1
    I.pg.time.set_timer(EXHAUSTION_TIM, 300000)
    timers["Exhaustion"] = EXHAUSTION_TIM

    Mob_Respawn = I.pg.USEREVENT + 2
    I.pg.time.set_timer(Mob_Respawn, 600000)
    timers["Mob_respawn"] = Mob_Respawn

    Harvest_timer = I.pg.USEREVENT + 3
    I.pg.time.set_timer(Harvest_timer, 60000)
    timers["Harvest"] = Harvest_timer

    Strike = I.pg.USEREVENT + 4
    I.pg.time.set_timer(Strike, 100)
    timers["Strike"] = Strike

    Walk = I.pg.USEREVENT + 5
    I.pg.time.set_timer(Walk, 300)
    timers["Walk"] = Walk

    mob_gif = I.pg.USEREVENT + 6
    I.pg.time.set_timer(mob_gif, 100)
    timers["mob_gif"] = mob_gif

    spell_cooloff = I.pg.USEREVENT + 7
    I.pg.time.set_timer(spell_cooloff, 100)
    timers["spell_cooloff"] = spell_cooloff

    healing = I.pg.USEREVENT + 8
    I.pg.time.set_timer(healing, 1000)
    timers["healing"] = healing

    return timers


def update_char_bar(screen, data, gifs):
    rect = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Char_bar"], [0, 0, S.SCREEN_WIDTH / 8, S.SCREEN_HEIGHT / 8])
    I.pg.draw.rect(screen, "black", (rect.w * 0.1, rect.h * 0.56, rect.w * 0.8, rect.h * 0.08))
    remainder = data["Player"]["hp"][0] / data["Player"]["hp"][1]
    I.pg.draw.rect(screen, "red", (rect.w * 0.1, rect.h * 0.56, rect.w * 0.8 * remainder, rect.h * 0.08))
    if data["Player"]["hp"][0] <= 0 and not data["Player"]["dead"]:
        data["Player"]["dead"] = data["Zoom_rect"].copy()
        gifs["ghost"].Start_gif("Dead",[S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2, S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7])
        gifs["Portal"].Start_gif("Portal", [I.info.START_POS[0] + 30, I.info.START_POS[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7])
        data["Zoom_rect"].x = I.info.START_POS[0]
        data["Zoom_rect"].y = I.info.START_POS[1]

    I.pg.draw.rect(screen, "black", (rect.w * 0.1, rect.h * 0.82, rect.w * 0.8, rect.h * 0.08))
    remainder = data["Player"]["mana"][0] / data["Player"]["mana"][1]
    I.pg.draw.rect(screen, "blue", (rect.w * 0.1, rect.h * 0.82, rect.w * 0.8 * remainder, rect.h * 0.08))

def walking(dx, dy, collide, data, last_orientation):
    if (dx, dy) in movement and not collide[0] or (dx, dy) in movement and collide[0] in ["Portal"]:
        # if no collisions walk properly. add or substract 1 from x or y
        data["Zoom_rect"].x += movement[(dx, dy)][0] * I.info.FAST
        data["Zoom_rect"].y += movement[(dx, dy)][1] * I.info.FAST
        last_orientation = movement[(dx, dy)]
    elif collide[0] not in ["mob"]:
        # if collision not with mob
        if movement[(dx, dy)] == last_orientation or movement[(dx, dy)][0] == last_orientation[0] or movement[(dx, dy)][1] == last_orientation[1]:
            data["Zoom_rect"].x -= 0
            data["Zoom_rect"].y -= 0
        else:
            data["Zoom_rect"].x += movement[(dx, dy)][0] * I.info.FAST
            data["Zoom_rect"].y += movement[(dx, dy)][1] * I.info.FAST
    elif collide[0] == "mob":
        # if collide is mob
        differance = (collide[1]["current_pos"].x - data["Zoom_rect"].x, collide[1]["current_pos"].y - data["Zoom_rect"].y)
        dx, dy = ((differance[0] > 150) - (differance[0] < 150), (differance[1] > 80) - (differance[1] < 80))
        data["Zoom_rect"].x -= movement[(dx, dy)][0] * 7
        data["Zoom_rect"].y -= movement[(dx, dy)][1] * 7

    return last_orientation

def keypress_handle(screen, data, song, items, spells):
    keys = I.pg.key.get_pressed()
    dx = (keys[I.pg.K_RIGHT] - keys[I.pg.K_LEFT])
    dy = (keys[I.pg.K_DOWN] - keys[I.pg.K_UP])

    if keys[I.pg.K_z]:
        gif_time = 200
        I.info.FAST = 2
    elif not keys[I.pg.K_z]:
        gif_time = 300
        I.info.FAST = 1
    if keys[I.pg.K_v]:
        curr_song = song["Playing"]
        song[curr_song].channel0.pause()
        br.spell_book(screen, data, spells)
        song[curr_song].channel0.unpause()
    if keys[I.pg.K_b] and not data["Player"]["dead"]:
        curr_song = song["Playing"]
        song[curr_song].channel0.pause()
        br.BackPack(screen, items, data["Player"])
        song[curr_song].channel0.unpause()

    return dx, dy, gif_time

def interract(collide, data, gifs, items, screen):
    if collide:
        print(collide[0])
        if collide[0] in I.info.HARVESTABLE.keys() and not data["Player"]["dead"]:
            if any((collide[1], collide[2]) == (t[0], t[1]) for t in I.info.HARVESTED_OBJECTS.get(collide[0], [])):
                pass
            else:
                item = I.info.HARVESTABLE[collide[0]]
                amount = random.randrange(1, 5)
                br.add_to_backpack(item, amount)
                duration = int(items.item_dict[item]["Aquire"].split(",,")[3]) - 4
                print(duration)
                #  Handle registering items that were taken, used in not allowing collection of too many items from single bush
                if I.info.HARVESTED_OBJECTS.get(collide[0]) == []:
                    I.info.HARVESTED_OBJECTS[collide[0]] = [(collide[1], collide[2], duration)]
                else:
                    existing_values = I.info.HARVESTED_OBJECTS.get(collide[0], [])

                    existing_values.append((collide[1], collide[2], duration))
                    I.info.HARVESTED_OBJECTS[collide[0]] = existing_values

                I.info.TEXT.append("Recieved " + str(amount) + " " + str(item) + ",,5000")
                return
        elif collide[0] == "Door":
            print("Search for door")
            print(collide)
        elif collide[0] == "Portal":
            I.info.TEXT.append("Reviving.,,3000")
        elif collide[0] == "Grave":
            I.info.TEXT.append("Was Purgatory Fun?,,5000")
            data["Player"]["dead"] = False
            data["Player"]["hp"] = (data["Player"]["hp"][1], data["Player"]["hp"][1])
            gifs["ghost"].start_gif = False
        elif collide[0] == "Sign":
            br.handdle_sign_display(screen)
        else:
            print("not harvestable", collide)
    # return text
    return

def harvest_timeout():
    for harvastable in I.info.HARVESTED_OBJECTS.keys():
        if I.info.HARVESTED_OBJECTS[harvastable] != []:
            for i in range(0, len(I.info.HARVESTED_OBJECTS[harvastable])):
                # print(i, I.info.HARVESTED_OBJECTS[harvastable])
                if I.info.HARVESTED_OBJECTS[harvastable][i][2] != 0:
                    I.info.HARVESTED_OBJECTS[harvastable][i] = (I.info.HARVESTED_OBJECTS[harvastable][i][0], I.info.HARVESTED_OBJECTS[harvastable][i][1], I.info.HARVESTED_OBJECTS[harvastable][i][2] - 1)
                if I.info.HARVESTED_OBJECTS[harvastable][i][2] == 0:
                    I.info.HARVESTED_OBJECTS[harvastable].pop(i)


def update_display_text(screen, gifs, data, collide):
    if I.info.TEXT:  # Check if the dictionary is not empty
        push = S.SCREEN_HEIGHT * 0.9
        for text in I.info.TEXT:
            lines = text.split(",,")
            time = lines[1]
            # Display the text
            Ff.display_text(screen, lines[0], 16, (50, push), "black")
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
                        gifs["ghost"].start_gif = False  # stop the ghost gif
                        data["Player"]["dead"] = False  # set to alive
                        data["Player"]["hp"] = (data["Player"]["hp"][1], data["Player"]["hp"][1])  # return hp
                        I.info.BACKPACK_CONTENT = {}  # remove backpack content
                else:
                    I.info.TEXT.remove(text)
            else:
                a = I.info.TEXT.index(text)
                I.info.TEXT[a] = lines[0] + ",," + str(time)


def handle_combat():
    orientation = I.info.LAST_ORIENT[0].split(".")[0]
    attack_direction = {"Front": (0, 10),
                        "Back": (0, -10),
                        "Left": (-10, 0),
                        "Right": (10, 0)}
    I.info.COMBAT_RECT = I.pg.Rect(150 + attack_direction[orientation][0], 85 + attack_direction[orientation][1], S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True

def handle_music(song, collide, data):
    if data["Player"]["dead"]:
        song["Playing"] = "Ghost"
    else:
        song["Playing"] = "Background"
    curr_song = song["Playing"]
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