from Render import Background_Render as br
from Values import Settings as S
from utils import Imports as I, Frequent_functions as Ff
import random
from static.data.play_data import mob_data

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
    mob = mob_data.Mob(name="Slime_S", exp=10, hp=8, allignment=0, count=20)
    gif = I.gifs.Gif(name="Blunt", frame_count=S.COMBAT_PATH["Blunt"][1], initial_path=S.COMBAT_PATH["Blunt"][0], delay=50)
    stance = 0
    mob_gif = 0
    collide = False
    pressed = 0
    disp_text = []
    gif_time = 300
    mob_gif_time = 75
    start_time = I.pg.time.get_ticks()
    start_time1 = I.pg.time.get_ticks()
    data = br.Start([I.info.START_POS[0], I.info.START_POS[1]], mob)
    last_orientation = (0, 0)
    combat_rect = 0
    music = [
        (I.A.NOTES["C3"], 500),
        (I.A.NOTES["G3"], 500),
        (I.A.NOTES["E3"], 500),
        (I.A.NOTES["C4"], 500),

        (I.A.NOTES["C3"], 500),
        (I.A.NOTES["G3"], 500),
        (I.A.NOTES["E3"], 500),
        (I.A.NOTES["C4"], 500),

        (I.A.NOTES["C3"], 500),
        (I.A.NOTES["G3"], 500),
        (I.A.NOTES["E3"], 500),
        (I.A.NOTES["C4"], 500),

        (I.A.NOTES["C3"], 500),
        (I.A.NOTES["G3"], 500),
        (I.A.NOTES["E3"], 500),
        (I.A.NOTES["C4"], 500),

    ]
    # song = Ff.generate_sine_wave_multiple(music)

    # print(song)
    # Ff.play_sine_wave_waveform(song)
    song = I.Songs.Song("Background", music)



    c_t = 0
    harvestable_objects = I.info.HARVESTED_OBJECTS.keys()
    while S.PLAY:
        for event in I.pg.event.get():
            if event.type == I.pg.QUIT:
                S.PLAY = False
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_c:
                    pressed = I.pg.K_c
                if event.key == I.pg.K_x:
                    if pressed != I.pg.K_x:
                        combat_rect = handle_combat()
                        c_t = I.pg.time.get_ticks()
                    pressed = I.pg.K_x
            elif event.type == I.pg.KEYUP:
                if event.key == pressed and event.key == I.pg.K_c:
                    disp_text = interract(collide, disp_text)
                    pressed = 0
                elif event.key == pressed and event.key == I.pg.K_x:
                    combat_rect = 0
                    pressed = 0

        if I.pg.time.get_ticks() - gif_time >= start_time:
            stance += 1
            start_time = I.pg.time.get_ticks()
            if stance > 3:
                stance = 0
        if I.pg.time.get_ticks() - mob_gif_time >= start_time1:
            mob_gif += 1
            start_time1 = I.pg.time.get_ticks()
            if mob_gif >= S.MOB_PATH["Slime_S"][1]:
                mob_gif = 0
                make_mobs_jump_around(mob)


        harvest_timeout(harvestable_objects)

        dx, dy, gif_time = keypress_handle(screen)

        collide = br.Update(screen, data, mob_gif, combat_rect, mob, gif)

        last_orientation = walking(dx, dy, collide, data, last_orientation)

        br.display_char(dx, dy, screen, stance, combat_rect)

        handle_music(song, collide)


        update_display_text(screen, disp_text)


        I.pg.display.flip()
        clock.tick(I.info.TICK)

        if I.pg.time.get_ticks() - c_t > 100:
            combat_rect = 0

def walking(dx, dy, collide, data, last_orientation):
    if (dx, dy) in movement and not collide:
        # if no collisions walk properly. add or substract 1 from x or y
        data["Zoom_rect"].x += movement[(dx, dy)][0] * I.info.FAST
        data["Zoom_rect"].y += movement[(dx, dy)][1] * I.info.FAST
        last_orientation = movement[(dx, dy)]
    elif collide[0] != "mob":
        # if collision occurs only able to move away from target.
        if movement[(dx, dy)] == last_orientation or movement[(dx, dy)][0] == last_orientation[0] or movement[(dx, dy)][1] == last_orientation[1]:
            data["Zoom_rect"].x -= 0
            data["Zoom_rect"].y -= 0
        else:
            data["Zoom_rect"].x += movement[(dx, dy)][0] * I.info.FAST
            data["Zoom_rect"].y += movement[(dx, dy)][1] * I.info.FAST
    else:
        differance = (collide[1]["current_pos"].x - data["Zoom_rect"].x, collide[1]["current_pos"].y - data["Zoom_rect"].y)
        dx, dy = ((differance[0] > 150) - (differance[0] < 150), (differance[1] > 80) - (differance[1] < 80))
        data["Zoom_rect"].x -= movement[(dx, dy)][0] * 7
        data["Zoom_rect"].y -= movement[(dx, dy)][1] * 7
    return last_orientation

def keypress_handle(screen):
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
        print("something")
    if keys[I.pg.K_b]:
        br.BackPack(screen)

    return dx, dy, gif_time

def interract(collide, disp_text):
    if collide:
        if collide[0] in I.info.HARVESTABLE.keys():
            if any((collide[1], collide[2]) == (t[0], t[1]) for t in I.info.HARVESTED_OBJECTS.get(collide[0], [])):
                pass
            else:
                item = I.info.HARVESTABLE[collide[0]]
                amount = random.randrange(1, 5)
                if I.info.BACKPACK_CONTENT.get(item) == []:
                    I.info.BACKPACK_CONTENT[item] = amount
                else:
                    I.info.BACKPACK_CONTENT[item] = I.info.BACKPACK_CONTENT.get(item, 0) + amount

                #  Handle registering items that were taken, used in not allowing collection of too many items from single bush
                if I.info.HARVESTED_OBJECTS.get(collide[0]) == []:
                    I.info.HARVESTED_OBJECTS[collide[0]] = [(collide[1], collide[2], 10000)]
                else:
                    existing_values = I.info.HARVESTED_OBJECTS.get(collide[0], [])
                    existing_values.append((collide[1], collide[2], 10000))
                    I.info.HARVESTED_OBJECTS[collide[0]] = existing_values

                disp_text.append("Recieved " + str(amount) + " " + str(item) + ",,5000")
                return disp_text
        elif collide[0] == "Door":
            print("Search for door")
            print(collide)
        else:
            print("not harvestable", collide)
    # return text
    return disp_text

def harvest_timeout(harvestable_objects):
    for harvastable in harvestable_objects:
        if I.info.HARVESTED_OBJECTS[harvastable] != []:
            for i in range(0, len(I.info.HARVESTED_OBJECTS[harvastable])):
                if I.info.HARVESTED_OBJECTS[harvastable][i][2] == 0:
                    I.info.HARVESTED_OBJECTS[harvastable].pop(i)
                    break
                else:
                    I.info.HARVESTED_OBJECTS[harvastable][i] = (
                    I.info.HARVESTED_OBJECTS[harvastable][i][0], I.info.HARVESTED_OBJECTS[harvastable][i][1],
                    I.info.HARVESTED_OBJECTS[harvastable][i][2] - 1)


def update_display_text(screen, disp_text):
    if disp_text:  # Check if the dictionary is not empty
        push = S.SCREEN_HEIGHT * 0.9
        for text in disp_text:
            lines = text.split(",,")
            time = lines[1]
            # Display the text
            Ff.display_text(screen, lines[0], 16, (50, push), "black")
            push -= 30
            # Decrease the timer
            time = int(time) - 50
            # Check if the timer has expired
            if time < 0:
                disp_text.remove(text)
            else:
                a = disp_text.index(text)
                disp_text[a] = lines[0] + ",," + str(time)

def make_mobs_jump_around(mob):
    # CURRENTLY ONLY WORKS FOR SLIMES
    x = random.randint(-3, 3)
    y = random.randint(-3, 3)
    mob.move_mobs_randomly(x, y)

def handle_combat():
    orientation = I.info.LAST_ORIENT[0].split(".")[0]
    attack_direction = {"Front": (0, 10),
                        "Back": (0, -10),
                        "Left": (-10, 0),
                        "Right": (10, 0)}
    combat_rect = I.pg.Rect(150 + attack_direction[orientation][0], 85 + attack_direction[orientation][1], S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
    return combat_rect

def handle_music(song, hit):
    duration = song.song[song.current_note][1]
    start_time = song.start_time
    # if not hit:
    if I.pg.time.get_ticks() - start_time > duration:
        song.next_note()
    # else:
    #     song.play_once(I.A.NOTES["C2"])
    #     song.play_once(I.A.NOTES["E2"])
