import random

from utils import Frequent_functions as Ff, Imports as I
from Values import Settings as S
from Backend import Play

B_Left = 0
B_Top = 0
B_W = S.SCREEN_WIDTH
B_H = S.SCREEN_HEIGHT

def read_txt_file(path):
    data_dict = {}
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Convert tuples to actual tuples
                if value.startswith("(") and value.endswith(")"):
                    value = tuple(map(int, value[1:-1].split(',')))

                # Convert numeric values
                elif value.isdigit():
                    value = int(value)

                # Convert floating point values
                elif '.' in value:
                    try:
                        value = float(value)
                    except ValueError:
                        pass

                data_dict[key] = value

    return data_dict
def Start(mob, decorations):
    data = {}
    data["Player"] = read_txt_file('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt")
    data["Player"] = update_character(data["Player"])
    if I.info.CURRENT_ROOM["Mobs"]:
        monster_count = {}
        for key, current_mob in mob.items():
            monster_count[current_mob.name] = current_mob.count
    if I.info.CURRENT_ROOM["Type"] == "Village":
        decor_count = {"Bush_S_1": 30, "Bush_S_2": 30, "Tree_T_1": 40}


    data["Window size"] = (B_W, B_H)  # Defines the size of the window (The rest is black)
    data["Zoom"] = (B_W / 4, B_H / 4)  # Defines how zoomed in to the picture the view is
    if I.info.CURRENT_ROOM["Type"] == "Village":
        data["Zoom"] = (B_W / 4, B_H / 4)  # Defines how zoomed in to the picture the view is
        data["Image"] = I.pg.image.load(S.DECOR_PATH["Grass"]).convert_alpha()  # uploads the background image with transparent convert
    else:
        data["Zoom"] = (B_W / 15, B_H / 15)  # Defines how zoomed in to the picture the view is
        data["Image"] = I.pg.image.load(S.DECOR_PATH["Wooden_tiles"]).convert_alpha()  # uploads the background image with transparent convert

    data["Image_rect"] = data["Image"].get_rect()  # Gets the rect of image
    data["Zoom_rect"] = I.pg.Rect(I.info.START_POS[0], I.info.START_POS[1], *data["Zoom"])  # creates a rect based on zoomed in picture (basicly makes a window)

    if I.info.CURRENT_ROOM["Type"] == "Village":
        house_image, house_rect = decorations.place_decor_by_coordinates(600, 380, S.DECOR_PATH["House_1"], (1.5, 1.5), (1.5, 1.4))
        decorations.decor_dict["House_1"][0] = {"name": "House_1", "id": 0, "image": house_image, "rect": house_rect, "effect": ""}

    if I.info.CURRENT_ROOM["Type"] == "Village":
        display_border("Tree_M_1", decorations, data)
        for key in decor_count:
            decorations.generate_decor(key, decor_count[key], data["Image_rect"].size, S.DECOR_PATH[key])

    if I.info.CURRENT_ROOM["Mobs"]:
        for key in monster_count:
            data[key] = generate_mobs(mob[key], data["Image_rect"].size)

    # image_data["Church_1"] = place_decor_by_coordinates(200, 280, S.DECOR_PATH["Church_1"], (2, 2), (2, 2))
    return data

def Update(screen, data, mob_dict, gifs, song, spells, decorations, clock):
    data["Zoom_rect"].x = max(0, min(data["Zoom_rect"].x, data["Image_rect"].width - data["Zoom"][0]))
    data["Zoom_rect"].y = max(0, min(data["Zoom_rect"].y, data["Image_rect"].height - data["Zoom"][1]))
    collide = [False]
    I.info.Player_rect = I.pg.Rect(150 + I.info.OFFSCREEN[0]/4, 85 + I.info.OFFSCREEN[1]/4, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
        sub_image = data["Image"].subsurface(data["Zoom_rect"]).copy()
        collide = handle_decor_visualisation(decorations, sub_image, data)
        handle_npc_visualisation(sub_image, data, gifs)
    else:
        sub_image = screen
        door = render_house(screen, data)
        me = I.pg.Rect(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 10 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 10)
        I.T.Make_rect_visible(screen, me, "white")
        if me.colliderect(door):
            I.info.START_POS = [510, 370]
            I.info.CURRENT_ROOM = {"name": "Village_1", "Spells": True, "Backpack": True, "Running": True, "Mobs": True, "Type": "Village"}
            update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"])
            Play.Start(screen, clock)
    if I.info.CURRENT_ROOM["Mobs"]:
        collide = handle_mob_visualisation(collide, sub_image, data, mob_dict, gifs, song, decorations)
    # if I.info.CURRENT_ROOM["Type"] in ["Village"]:
    #     collide = handle_decor_visualisation(decorations, sub_image, data)


    collide = handle_death_visualisation(sub_image, data, gifs, collide)

    # if I.info.CURRENT_ROOM["Type"] in ["Village"]:
    #     handle_npc_visualisation(sub_image, data, gifs)


    cast_spell_handle(sub_image, data, spells, gifs, mob_dict, song, decorations)


    scaled_image = I.pg.transform.scale(sub_image, data["Window size"])
    screen.blit(scaled_image, (0, 0))
    if data["Player"]["dead"] and collide[0] == "mob":  # dont hit mobs when u dead
        collide = False, 0, 0, 0
    return collide



# def handle_decor_abuse(gifs):
def handle_mob_visualisation(collide, sub_image, data, mob_dict, gifs, song, decorations):
    for mob in mob_dict.values():
        for current_mob in mob.mobs:
            mob_gif = current_mob["gif_frame"][0]
            mob_rect = current_mob["rect"][mob_gif]
            mob_x = mob_rect.x - data["Zoom_rect"].x
            mob_y = mob_rect.y - data["Zoom_rect"].y
            rect = I.pg.Rect(mob_x, mob_y, mob_rect.w, mob_rect.h)
            update_health(rect, current_mob, sub_image)
            if current_mob["flip"]:
                image = I.pg.transform.flip(current_mob["image"][mob_gif], True, False)
            else:
                image = current_mob["image"][mob_gif]
            # print(mob_x, mob_y)
            sub_image.blit(image, (mob_x, mob_y))

            handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob)

            handle_damage_type_visualisation(sub_image, current_mob, gifs, (mob_x, mob_y), data, mob, decorations)

            if I.info.Player_rect.colliderect(rect) and current_mob["allignment"] in [6, 8, 9]:
                collide = ('mob', current_mob, mob_rect.x, mob_rect.y)
                data["Player"]["Last_hit"] = I.pg.time.get_ticks()
                data["Player"]["hp"] = data["Player"]["hp"][0] - current_mob["damage"][0], data["Player"]["hp"][1]

            handle_mob_speed(data, current_mob, decorations, mob)
    return collide
def handle_mob_speed(data, current_mob, decorations, mob):

    # me = I.pg.Rect(150, 85, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
    speed = current_mob["speed"][0]
    current_frame = current_mob["gif_frame"][0]
    frame_count = current_mob["gif_frame"][1]
    if current_frame % 2 == 0:
        target_pos = (I.info.Player_rect.x + data["Zoom_rect"].x, I.info.Player_rect.y + data["Zoom_rect"].y)
        mob_rect = current_mob["rect"][current_frame]
        if not data["Player"]["dead"] and current_mob["allignment"] in [6, 8]:
            mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_towards(target_pos, current_mob, speed, decorations.displayed_rects, data["Zoom_rect"])
            mob.update_position(mob_rect.x, mob_rect.y, current_mob)
            if current_mob["allignment"] == 8:
                current_mob["allignment"] = 4

            #Update the orientation of mob running towards me
            if mob_rect.x > target_pos[0]:
                current_mob["flip"] = True
            else:
                current_mob["flip"] = False

        elif not data["Player"]["dead"] and current_mob["allignment"] == 4 and current_mob["hp"][0] < current_mob["hp"][1]:
            mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_away_from(target_pos, current_mob, speed, decorations.displayed_rects, data["Zoom_rect"])
            mob.update_position(mob_rect.x, mob_rect.y, current_mob)

            #Update the orientation of mob running away from me
            if mob_rect.x > target_pos[0]:
                current_mob["flip"] = False
            else:
                current_mob["flip"] = True

        else:
            current_mob["visible"] = False

def handle_damage_type_visualisation(sub_image, current_mob, gifs, pos, data, mob, decorations):
    for key in gifs.keys():
        if gifs[key].start_gif and current_mob == gifs[key].rect:
            if current_mob["effect"].get(key) != None:
                duration = current_mob["effect"][key]
                frame = gifs[key].next_frame(duration)
                if current_mob["effect"]["Fire"] != 0:
                    gifs["Cold"].start_gif = False
                    gifs["Cold"].repeat = 0
                    mob.deal_damage(current_mob, data["Player"], "effect_" + key)
                if current_mob["effect"]["Cold"] != 0:
                    gifs["Fire"].start_gif = False
                    gifs["Fire"].repeat = 0
                    current_mob["speed"] = (0, current_mob["speed"][1])
            else:
                frame = gifs[key].next_frame(1)  # made specifically for damage displaying
            sub_image.blit(frame, (pos[0] - 5, pos[1]))
        elif not gifs[key].start_gif and current_mob["effect"].get(key) != None:
            if not gifs[key].start_gif and current_mob["effect"][key] != 0:
                current_mob["effect"][key] = 0
                if key == "Cold":
                    current_mob["speed"] = (current_mob["speed"][1], current_mob["speed"][1])
        elif hasattr(gifs[key], 'rect') and isinstance(gifs[key].rect, int):
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
            if data_to_remove != [] and not gifs[effect].start_gif:
                for index in data_to_remove:
                    del decorations.effected_decor[index]






def handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob):
    if I.info.COMBAT_RECT != 0:
        for key in ["Blunt", "Piercing", "Slashing"]:
            if I.info.COMBAT_RECT != 0 and I.info.COMBAT_RECT.colliderect(rect) and not gifs[key].start_gif:
                curr_song = song["Playing"]
                effect = song[curr_song].generate_thump_sound()
                song[curr_song].play_effect(effect)
                gifs["Blunt"].Start_gif(key, current_mob)
                mob.deal_damage(current_mob, data["Player"], "")
                I.info.COMBAT_RECT = 0

def handle_death_visualisation(sub_image, data, gifs, collide):
    if data["Player"]["dead"]:

        me = I.pg.Rect(150, 85, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
        dead_disc = {"Portal": display_gif_on_subimage(sub_image, (S.SCREEN_WIDTH / 16, S.SCREEN_HEIGHT / 10), (I.info.START_POS[0] * 1.6 - data["Zoom_rect"].x , I.info.START_POS[1] + 10 * 16 - data["Zoom_rect"].y), gifs["Portal"]),
                     "Sign": display_on_subimage(sub_image, (S.SCREEN_WIDTH / 90, S.SCREEN_HEIGHT / 40), S.PLAYING_PATH["Sign"],(I.info.START_POS[0] * 1.6 - data["Zoom_rect"].x, I.info.START_POS[1] + 10 * 10 - data["Zoom_rect"].y)),
                     "Grave": display_on_subimage(sub_image, (S.SCREEN_WIDTH / 60, S.SCREEN_HEIGHT / 30), S.PLAYING_PATH["Grave"], (data["Player"]["dead"].x - data["Zoom_rect"].x + me.x, data["Player"]["dead"].y - data["Zoom_rect"].y + me.y)),
                     }
        dead_list = list(dead_disc.values())
        if I.info.Player_rect.collidelistall(dead_list):
            keys = list(dead_disc.keys())
            key = keys[I.info.Player_rect.collidelistall(dead_list)[0]]
            collide = (key, dead_disc[key].x, dead_disc[key].y)
    return collide
def handle_npc_visualisation(sub_image, data, gifs):
    npc = {"Luna": display_gif_on_subimage(sub_image, (17,18), (I.info.START_POS[0] * 1.6 - data["Zoom_rect"].x , I.info.START_POS[1] + 10 * 43 - data["Zoom_rect"].y), gifs["Luna"]),
           "Bear": display_gif_on_subimage(sub_image, (17,18), (I.info.START_POS[0] * 1.7 - data["Zoom_rect"].x , I.info.START_POS[1] + 10 * 43 - data["Zoom_rect"].y), gifs["Bear"]),
    }

def handle_decor_visualisation(decorations, sub_image, data):
    Collide = [False]
    decorations.displayed_rects = []  # List to keep track of displayed rectangles
    decor_options = list(decorations.decor_dict.keys())
    decorations_to_remove = []
    for option in decor_options:
        for id in decorations.decor_dict[option].keys():
            if isinstance(id, str):
                continue
            decor = decorations.decor_dict[option][id]
            # Gets x, y position of decoration
            decor_x = decor["rect"].x - data["Zoom_rect"].x
            decor_y = decor["rect"].y - data["Zoom_rect"].y

            rect = I.pg.Rect(decor_x, decor_y, decor["rect"].w, decor["rect"].h)

            # Check if current decor collides with any already displayed decor
            if not any(rect.colliderect(displayed_rect) for displayed_rect in decorations.displayed_rects):
                # I.T.Make_rect_visible(sub_image, rect, "black")
                # print(decor["rect"])
                if (data["Image"].get_at((decor["rect"].x, decor["rect"].y)) == (137, 176, 46, 255) and data["Image"].get_at((decor["rect"].x + decor["rect"].w, decor["rect"].y + decor["rect"].h)) == (137, 176, 46, 255)):
                    sub_image.blit(decor["image"], (decor_x, decor_y))
                    decorations.displayed_rects.append(rect)  # Add to the list of displayed rectangles
                    if option in I.info.ENTERABLE:
                        door_rect = I.pg.Rect(rect.left + rect.w * 0.6, rect.top + rect.h * 0.60, rect.w / 4, rect.h / 2)
                        # I.T.Make_rect_visible(sub_image, me)
                        if I.info.Player_rect.colliderect(door_rect):
                            Collide = ("Door", door_rect.x, door_rect.y)
                    if I.info.Player_rect.colliderect(rect):
                        Collide = (option, decor["rect"].x, decor["rect"].y)
                        # print("collide", Collide)

            else:
                # remove the decors that are touching:
                decorations_to_remove.append((option, id))

    if decorations_to_remove != []:
        for option, id in decorations_to_remove:
            del decorations.decor_dict[option][id]
    return Collide
def display_char(dx, dy, screen, gifs, data):
    character_path = 'static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER
    dxdy = (dx, dy)
    # I.info.OFFSCREEN = I.info.OFFSCREEN[0] + dx, I.info.OFFSCREEN[1] + dy
    orientation = {
        (0, 0): "Stand",
        (1, 0): "Right",
        (-1, 0): "Left",
        (0, 1): "Front",
        (0, -1): "Back",
        (1, -1): "Back",
        (-1, -1): "Back",
        (1, 1): "Front",
        (-1, 1): "Front"
    }
    orientation_images = {
        "Front": ["Front.png", "Front1.png", "Front2.png"],
        "Back": ["Back.png", "Back1.png", "Back2.png"],
        "Right": ["Right.png", "Right1.png", "Right2.png"],
        "Left": ["Left.png", "Left1.png", "Left2.png"]
    }
    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
        if data["Zoom_rect"].x in [0, -1, 1, 680, 681, 679]:
            I.info.OFFSCREEN = I.info.OFFSCREEN[0] + dx * 3 * I.info.FAST, I.info.OFFSCREEN[1]
        else:
            I.info.OFFSCREEN = (0, I.info.OFFSCREEN[1])
        if data["Zoom_rect"].y in [0, -1, 1, 820, 821, 819]:
            I.info.OFFSCREEN = I.info.OFFSCREEN[0], I.info.OFFSCREEN[1] + dy * 3 * I.info.FAST
        else:
            I.info.OFFSCREEN = (I.info.OFFSCREEN[0],  0)
    else:
        I.info.OFFSCREEN = I.info.OFFSCREEN[0] + dx * 3 * I.info.FAST, I.info.OFFSCREEN[1] + dy * 3 * I.info.FAST

    if gifs["ghost"].start_gif:
        frame = gifs["ghost"].next_frame(-1)
        frame = I.pg.transform.scale(frame, (S.SCREEN_WIDTH / 18, S.SCREEN_HEIGHT / 7))
        screen.blit(frame, [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + I.info.OFFSCREEN[1]])
    else:
        if I.info.COMBAT_RECT != 0:
            if dx == 0 and dy == 0:
                for key, value in orientation.items():
                    if value == I.info.LAST_ORIENT[0].split(".")[0]:
                        dx = key[0]
                        dy = key[1]
                        break
                character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + dx * 5 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + dy * 5 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]
            else:
                character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + dx * 10 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + dy * 10 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]
        else:
            character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + I.info.OFFSCREEN[1], S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]

        orient = orientation[dxdy]
        if orient in orientation_images:
            images = orientation_images[orient]
            if I.info.CURRENT_STANCE == 0 or I.info.CURRENT_STANCE == 2:
                Ff.add_image_to_screen(screen, character_path + images[0], character_center_pos)
            elif I.info.CURRENT_STANCE == 1:
                Ff.add_image_to_screen(screen, character_path + images[1], character_center_pos)
            else:
                Ff.add_image_to_screen(screen, character_path + images[2], character_center_pos)
            I.info.LAST_ORIENT = orientation_images[orient]
        else:
            Ff.add_image_to_screen(screen, character_path + I.info.LAST_ORIENT[0], character_center_pos)

def generate_decor(num_of_items, background_size, path):
    items = {}
    for i in range(num_of_items):
        x = random.randint(0, background_size[0]-100)
        y = random.randint(0, background_size[1]-100)
        image = I.pg.image.load(path).convert_alpha()
        rect = image.get_rect(topleft=(x, y))
        items[i] = {"image": image, "rect": rect}
    return items
def generate_mobs(mob, background_size):
    path = S.MOB_PATH[mob.name][0]
    mob_gif_count = S.MOB_PATH[mob.name][1]
    mob.spawn_mobs(background_size, path, mob_gif_count)
    return mob.mobs

def add_to_backpack(item, amount):
    if amount != 0:
        row = len(I.info.BACKPACK_CONTENT.keys()) * 2
        collumn = 0
        for i in range(row):
            if row > 14:
                row -= 14
                collumn += 2
        if I.info.BACKPACK_CONTENT.get(item) == None:
            I.info.BACKPACK_CONTENT[item] = (amount, row, collumn)
        else:
            value = I.info.BACKPACK_CONTENT[item]
            I.info.BACKPACK_CONTENT[item] = (value[0] + amount, value[1], value[2])

def BackPack(screen, items, player):
    pressed = 0
    fill_backpack(screen, player)
    running = True
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    block = (0, 0)
    coordinates = get_equipment_coordinates(block)
    border = 1
    use = 0
    selected = 0
    color = "Yellow"
    pickup = 0
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_b:
                    pressed = I.pg.K_b
                elif event.key == I.pg.K_x:
                    pressed = I.pg.K_x
                    color = "Green"
                    for key, value in I.info.BACKPACK_CONTENT.items():
                        if value[1] == block[0] and value[2] == block[1]:
                            # if the possision matches get the key
                            use = key
                elif event.key == I.pg.K_c:
                    pressed = I.pg.K_c
                    if selected == 0:
                        if block[0] >= 0:
                            selected = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
                        else:
                            selected = I.pg.Rect(coordinates[block][0], coordinates[block][1], item_w, item_h)
                        for key, value in I.info.BACKPACK_CONTENT.items():
                            if value[1] == block[0] and value[2] == block[1]:
                                # if the possision matches get the key
                                pickup = key
                    else:
                        if pickup != 0:
                            value = I.info.BACKPACK_CONTENT[pickup]
                            I.info.BACKPACK_CONTENT[pickup] = (value[0], block[0], block[1]) # set the new possision value
                        pickup = 0
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
                if pressed == I.pg.K_b:
                    running = False  # exits backpack view
                elif pressed == I.pg.K_x:
                    color = "Yellow"
                    if use != 0 and "CONSUMABLE" in items.item_dict[use]["Properties"]:
                        handle_consumption(items, player, use)
                        use = 0
                    pressed = 0
                    selected = 0

            fill_backpack(screen, player)
            if block[0] < 0:
                if block[0] < -10:
                    block = -10, block[1]
                if block[1] > 8:
                    block = block[0], 8
                coordinates = get_equipment_coordinates(block)
                if block[0] < -2 and block[0] >= -6 and block[1] != 8:
                    block = -10, block[1]
                if block[0] <= -6 and block[0] > -10 and block[1] != 8:
                    block = -2, block[1]
                rect = I.pg.Rect(coordinates[block][0], coordinates[block][1], item_w, item_h)
            else:
                rect = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
            I.pg.draw.rect(screen, color, rect, border)
            if selected != 0:
                I.pg.draw.rect(screen, "Yellow", selected, 2)

            I.pg.display.flip()

def get_equipment_coordinates(block):
    coordinates = {
        (-2, 0): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.12),
        (-2, 2): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.17),
        (-2, 4): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.21),
        (-2, 6): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.24),
        (-2, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-4, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.82,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-6, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.74,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-8, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.66,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-10, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-10, 6): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.24),
        (-10, 4): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.21),
        (-10, 2): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.17),
        (-10, 0): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.12),
    }
    return coordinates
def handle_consumption(items, player, use):
    consumable = items.item_dict[use]["Properties"][11:-1].split(",,")
    for consume in consumable:
        points, atribute = consume.split("-")
        if player[atribute][0] < player[atribute][1]:
            if "/" in points:
                points = points[1:]
                player[atribute] = (player[atribute][0] - int(points), player[atribute][1])
            else:
                player[atribute] = (player[atribute][0] + int(points), player[atribute][1])
        elif player[atribute][0] >= player[atribute][1]:
            if "/" in points:
                points = points[1:]
                player[atribute] = (player[atribute][0] - int(points), player[atribute][1])
            else:
                player[atribute] = (player[atribute][1], player[atribute][1])
    value = I.info.BACKPACK_CONTENT[use]
    if value[0] > 1:
        I.info.BACKPACK_CONTENT[use] = (value[0] - 1, value[1], value[2])
    else:
        del I.info.BACKPACK_CONTENT[use]
def display_on_subimage(sub_image, size, path, pos):
    image = I.pg.image.load(path).convert_alpha()
    image = I.pg.transform.scale(image, (size[0], size[1]))
    sub_image.blit(image, pos)
    return I.pg.Rect(pos[0], pos[1], size[0], size[1])

def fill_backpack(screen, player):
    rect = screen.get_rect()
    bag = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Backpack_Empty"], [rect.center[0] * 0.5 ,rect.center[1] * 0.25, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT * 0.75])
    if I.info.BACKPACK_COORDINATES_X == {}:
        I.info.BACKPACK_COORDINATES_X, I.info.BACKPACK_COORDINATES_Y = bag_coordinates(screen, bag)
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    for content in I.info.BACKPACK_CONTENT.keys():
        row = I.info.BACKPACK_CONTENT[content][1]
        collumn = I.info.BACKPACK_CONTENT[content][2]
        if row < 0:
            coordinates = get_equipment_coordinates((row,collumn))
            Ff.add_image_to_screen(screen, S.ITEM_PATHS[content], [coordinates[row, collumn][0], coordinates[row, collumn][1], item_w, item_h])
            Ff.display_text(screen, str(I.info.BACKPACK_CONTENT[content][0]), 2, [coordinates[row, collumn][0], coordinates[row, collumn]][1], "white")
        else:
            Ff.add_image_to_screen(screen, S.ITEM_PATHS[content], [list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn], item_w, item_h])
            Ff.display_text(screen, str(I.info.BACKPACK_CONTENT[content][0]), 2, [list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn]], "white")

    I.pg.draw.rect(screen, "black", (bag.w * 0.604, bag.h * 0.807, bag.w * 0.115, bag.h * 0.012))
    remainder = player["hp"][0] / player["hp"][1]
    I.pg.draw.rect(screen, "red", (bag.w * 0.604, bag.h * 0.807, bag.w * 0.115 * remainder, bag.h * 0.012))
    Ff.display_text(screen, "Hp", 1, (bag.w * 0.562, bag.h * 0.80), "black")

    I.pg.draw.rect(screen, "black", (bag.w * 0.808, bag.h * 0.807, bag.w * 0.148, bag.h * 0.012))
    remainder = player["mana"][0] / player["mana"][1]
    I.pg.draw.rect(screen, "blue", (bag.w * 0.808, bag.h * 0.807, bag.w * 0.148 * remainder, bag.h * 0.012))
    Ff.display_text(screen, "Mp", 1, (bag.w * 0.752, bag.h * 0.80), "black")

    I.pg.draw.rect(screen, "black", (bag.w * 0.604, bag.h * 0.857, bag.w * 0.115, bag.h * 0.012))
    remainder = player["Exhaustion"][0] / player["Exhaustion"][1]
    I.pg.draw.rect(screen, "Green", (bag.w * 0.604, bag.h * 0.857, bag.w * 0.115 * remainder, bag.h * 0.012))
    Ff.display_text(screen, "Exh", 1, (bag.w * 0.55, bag.h * 0.85), "black")

    Ff.add_image_to_screen(screen,
                           'static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + "Front.png",
                           [rect.center[0] * 0.64 ,rect.center[1] * 0.4, S.SCREEN_WIDTH / 8, S.SCREEN_HEIGHT / 4])


    I.pg.draw.rect(screen, "black", (bag.w * 0.626, bag.h * 0.71, bag.w * 0.3, bag.h * 0.025))
    remainder = player["Experience"] / exp_till_lvup(player)
    I.pg.draw.rect(screen, "light green", (bag.w * 0.626, bag.h * 0.707, bag.w * 0.3 * remainder, bag.h * 0.025))
    Ff.display_text(screen, "Exp", 1, (bag.w * 0.58, bag.h * 0.71), "black")


    return bag
def exp_till_lvup(player):
    level = int(player["Level"])

    if level > 5:
        exp_needed = level * 100 * 0.9
    elif level > 10:
        exp_needed = level * 100 * 0.8
    elif level > 15:
        exp_needed = level * 100 * 0.7
    elif level > 20:
        exp_needed = level * 100 * 0.6
    else:
        exp_needed = level * 100
    return  exp_needed

def bag_coordinates(screen, bag):
    stop = False
    start = 0
    coordinates_x = {}
    coordinates_y = {}

    # Gets start coordinates
    for top in range(bag.top, bag.top + bag.h):
        if stop:
            break
        for left in range(bag.left, bag.left + bag.w):
            color = screen.get_at((left, top))
            if color == S.DEFAULT["Backpack_Empty"]:
                start = (left, top)
                stop = True
                break
    left = start[0]
    top = start[1]
    cube = 1

    #  Gets coordinates of X
    color = screen.get_at((start[0], start[1]))
    if color == S.DEFAULT["Backpack_Empty"]:
        kill = False
        while not kill:
            color1 = color
            coordinates_x[cube] = left
            cube += 1
            while color1 == S.DEFAULT["Backpack_Empty"]:
                coordinates_x[cube] = left
                left += 1
                color1 = screen.get_at((left, top))
                # screen.set_at((left, top), (0,0,0,255))
            if color1 == (204, 130, 98, 255):
                cube += 1
                while color1 == (204, 130, 98, 255):
                    left += 1
                    color1 = screen.get_at((left, top))
                if color1 == (156, 90, 60, 255):
                    kill = True

    #  Gets coordinates of Y
    left = start[0]
    top = start[1]
    cube = 1
    color = screen.get_at((start[0], start[1]))
    if color == S.DEFAULT["Backpack_Empty"]:
        kill = False
        while not kill:
            color1 = color
            coordinates_y[cube] = top
            cube += 1
            while color1 == S.DEFAULT["Backpack_Empty"]:
                coordinates_y[cube] = top
                top += 1
                color1 = screen.get_at((left, top))
            if color1 == (204, 130, 98, 255):
                cube += 1
                while color1 == (204, 130, 98, 255):
                    top += 1
                    color1 = screen.get_at((left, top))
                if color1 == (156, 90, 60, 255):
                    kill = True

    return (coordinates_x, coordinates_y)


def place_decor_by_coordinates(x, y, path, scale, rect_scale):
    items = {}
    image = I.pg.image.load(path).convert_alpha()
    rect = image.get_rect(topleft=(x, y))
    image = I.pg.transform.scale(image, (rect.w * scale[0], rect.h * scale[1]))
    rect.w = rect.w * rect_scale[0]
    rect.h = rect.h * rect_scale[1]
    items[0] = {"image": image, "rect": rect}
    return items

def update_health(rect, current_mob, sub_image):
    health_bar = I.pg.Rect(rect.x, rect.y, rect.w, 1)
    I.pg.draw.rect(sub_image, "red", health_bar)
    health = current_mob["hp"]
    remainder = health[0] / health[1]
    reduced_health_bar = I.pg.Rect(rect.x, rect.y, rect.w * remainder, 1)
    I.pg.draw.rect(sub_image, "green", reduced_health_bar)

def update_character(player_disc):
    hp_by_race = {"Elf": 11,
                  "Human": 10}

    mana_by_race = {"Elf": 14,
                    "Human": 10}

    race = player_disc["Race"]
    level = player_disc["Level"]
    player_disc["hp"] = (hp_by_race[race] * level, hp_by_race[race] * level)
    player_disc["mana"] = (mana_by_race[race] * level, mana_by_race[race] * level)

    player_disc["dead"] = False

    player_disc["Exhaustion"] = (100, 100)

    player_disc["Last_hit"] = I.pg.time.get_ticks()  # required to know when to start regenerating hp and mana

    return player_disc

def spell_book(screen, data, spells):
    fill_spellbook(screen)
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
                elif event.key == I.pg.K_v:
                    pressed = I.pg.K_v
            if event.type == I.pg.KEYUP:
                if pressed == I.pg.K_v:
                    running = False
                if event.key == I.pg.K_c:
                    if selected == 0:
                        for spell, (row, collum) in I.info.SPELLBOOK_CONTENT.items():
                            if block == (row, collum):
                                selected = spell
                    else:
                        spells.selected_spell[block[0]] = selected
                        selected = 0
                pressed = 0
        fill_spellbook(screen)
        if selected != 0:
            if block[0] > 8:
                block = (8, block[1])
            if block[0] < 0:
                block = (0, block[1])
            rect = I.pg.Rect(list(I.info.SPELLBOOK_COORDINATES_X.values())[block[0]], list(I.info.SPELLBOOK_COORDINATES_Y.values())[11] + list(I.info.SPELLBOOK_COORDINATES_Y.values())[0], item_w, item_h)
        else:
            rect = I.pg.Rect(list(I.info.SPELLBOOK_COORDINATES_X.values())[block[0]],list(I.info.SPELLBOOK_COORDINATES_Y.values())[block[1]], item_w, item_h)
        I.pg.draw.rect(screen, color, rect, border)

        if spells.selected_spell != {}:
            for pos, spell in spells.selected_spell.items():
                rect = I.pg.Rect(list(I.info.SPELLBOOK_COORDINATES_X.values())[int(pos)],list(I.info.SPELLBOOK_COORDINATES_Y.values())[11] +list(I.info.SPELLBOOK_COORDINATES_Y.values())[0], item_w, item_h)
                Ff.add_image_to_screen(screen, S.SPELL_PATHS[spell] + "0.png", rect)


        I.pg.display.flip()

def fill_spellbook(screen):
    rect = screen.get_rect()
    book = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Spellbook_Empty"], [rect.center[0] * 0.5, rect.center[1] * 0.25, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT * 0.75])

    if I.info.SPELLBOOK_COORDINATES_X == {}:
        I.info.SPELLBOOK_COORDINATES_X, I.info.SPELLBOOK_COORDINATES_Y = bag_coordinates(screen, book)

    item_w = list(I.info.SPELLBOOK_COORDINATES_X.values())[1] - list(I.info.SPELLBOOK_COORDINATES_X.values())[0]
    item_h = list(I.info.SPELLBOOK_COORDINATES_Y.values())[1] - list(I.info.SPELLBOOK_COORDINATES_Y.values())[0]
    for content in I.info.SPELLBOOK_CONTENT.keys():
        row, collumn = I.info.SPELLBOOK_CONTENT[content]
        Ff.add_image_to_screen(screen, S.SPELL_PATHS[content] + "0.png", [list(I.info.SPELLBOOK_COORDINATES_X.values())[row], list(I.info.SPELLBOOK_COORDINATES_Y.values())[collumn], item_w, item_h])
def display_gif_on_subimage(sub_image, size, pos, gif):
    frame = gif.next_frame(-1)
    frame = I.pg.transform.scale(frame, (size[0], size[1]))
    sub_image.blit(frame, pos)
    return I.pg.Rect(pos[0], pos[1], size[0], size[1])

def cast_spell_handle(sub_image, data, spells, gifs, mob, song, decorations):
    if not data["Player"]["dead"]:
        curr_song = song["Playing"]
        sound_type = {"Force": song[curr_song].generate_magic_sound(),
                      "Fire": song[curr_song].generate_fire_sound(),
                      "Cold": song[curr_song].generate_cold_sound()}
        for slot, spell in spells.selected_spell.items():
            if gifs[spell].start_gif:
                spells.spell_cooloff[spell] = spells.spell_dict[spell]["recharge"]
                frame = gifs[spell].next_frame(1)
                if I.info.CURRENT_ROOM["Type"] in ["Village"]:
                    size = (20, 20)
                else:
                    size = (100, 100)
                frame = I.pg.transform.scale(frame, size)

                if spells.direction[spell] == 0:
                    if I.info.CURRENT_ROOM["Type"] in ["Village"]:
                        spells.init_cast[spell] = data["Zoom_rect"].copy()
                        spells.direction[spell] = I.info.LAST_ORIENT[0].split(".")[0]
                    else:
                        spells.init_cast[spell] = I.pg.Rect(S.SCREEN_WIDTH / 2 + S.SCREEN_WIDTH / 20 - I.info.Player_rect.w * 10 + I.info.OFFSCREEN[0], S.SCREEN_HEIGHT / 2 - I.info.Player_rect.h * 10 + I.info.OFFSCREEN[1], size[0], size[1])
                        spells.direction[spell] = I.info.LAST_ORIENT[0].split(".")[0]
                direction_settings = {
                    "Front": {"rect": (145, 80), "dir": (0, -1), "rotate": 90, "flip": (False, True)},
                    "Back": {"rect": (145, 70), "dir": (0, 1), "rotate": 90, "flip": (False, False)},
                    "Left": {"rect": (140, 75), "dir": (1, 0), "rotate": 0, "flip": (True, False)},
                    "Right": {"rect": (150, 75), "dir": (-1, 0), "rotate": 0, "flip": (False, False)},
                }
                spell_direction = spells.direction[spell]
                settings = direction_settings.get(spell_direction)
                # me = I.pg.Rect(settings["rect"][0], settings["rect"][1], S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)
                dir = settings["dir"]
                frame = I.pg.transform.rotate(frame, settings["rotate"])
                frame = I.pg.transform.flip(frame, *settings["flip"])

                if gifs[spell].current_frame != 0:
                    if I.info.CURRENT_ROOM["Type"] == "Village":
                        rect = I.pg.Rect(spells.init_cast[spell].x - data["Zoom_rect"].x + I.info.Player_rect.x - dir[0] * gifs[spell].current_frame * 6, spells.init_cast[spell].y - data["Zoom_rect"].y + I.info.Player_rect.y - dir[1] * gifs[spell].current_frame * 6, size[0], size[1])
                    else:
                        rect = I.pg.Rect(spells.init_cast[spell].x - dir[0] * gifs[spell].current_frame * 12, spells.init_cast[spell].y - dir[1] * gifs[spell].current_frame * 12, size[0], size[1])
                    sub_image.blit(frame, rect)
                    if I.info.CURRENT_ROOM["Type"] == "Village":
                        if rect.collidelist(decorations.displayed_rects) != -1: # if hits any decor
                            type = spells.spell_dict[spell]["type"]
                            song[curr_song].play_effect(sound_type[type])
                            gifs[spell].start_gif = False
                            index = rect.collidelist(decorations.displayed_rects)
                            decorations.effected_decor[index] = type
                        else:
                            for key in mob.keys():
                                for current_mob in mob[key].mobs:
                                    mob_rect = I.pg.Rect(current_mob["rect"][0].x - data["Zoom_rect"].x,
                                                         current_mob["rect"][0].y - data["Zoom_rect"].y,
                                                         current_mob["rect"][0].w, current_mob["rect"][0].h)
                                    if rect.colliderect(mob_rect):
                                        mob[key].deal_damage(current_mob, data["Player"], spells.spell_dict[spell])
                                        gifs[spell].start_gif = False  # IF COMMENTED OUT, MAKES A SPELL GO THROUGH MULTIPLE ENEMIES
                                        type = spells.spell_dict[spell]["type"]
                                        gifs[type].Start_gif(type, current_mob)
                                        song[curr_song].play_effect(sound_type[type])
            else:
                # RESET DIRECTION OF FIRE
                spells.direction[spell] = 0
                spells.init_cast[spell] = 0

def handdle_sign_display(screen):
    running = True
    Ff.add_image_to_screen(screen, S.PLAYING_PATH["Text_bar"], (0, S.SCREEN_HEIGHT / 2, S.SCREEN_WIDTH, S.SCREEN_HEIGHT / 2))
    text = "Hi, looks like you died. Maybe next time try dodging the blow instead of kissing it : ). \n Anyways, see that big purple portal? interact with it while standing on it and you will be revived. \n But you will loose all the items you were carrying. \n Alternatively find your grave stone and interract with it. This way you will keep all of your useless stuff. \n Don't rush to comeback. \n With love -S!"
    a = 0
    collumn = 100
    row = 100
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN and event.key == I.pg.K_c:
                if a > len(text):
                    running = False
                else:
                    for i in range(20):
                        if text[a + i] == "\n":
                            a += i
                            break
                    else:
                         a += 20

        if not a > len(text) and text[a-1] == "\n":
            collumn += 20
            row = 100
            text = text[a+1:]
            a = 0

        Ff.display_text(screen, text[0:a], 10, (row, S.SCREEN_HEIGHT / 2 + collumn),  "black")

        if not a > len(text):
            I.pg.time.wait(10)
            a += 1

        I.pg.display.flip()


def display_border(border_image_name, decorations, data):
    image = I.pg.image.load(S.DECOR_PATH[border_image_name]).convert_alpha()
    rect = image.get_rect()
    tree_amount = 0
    row = 0
    while True:
        # building on the x axis (virsus ir apacia)
        # virsui pirma juosta
        # apacioj pirma
        # virsui antra
        # apacioj antra
        tree_image1, tree_rect1 = decorations.place_decor_by_coordinates(row, 0, S.DECOR_PATH[border_image_name], (0.8, 0.8), (1, 0.3))
        tree_image2, tree_rect2 = decorations.place_decor_by_coordinates(row, data["Image_rect"].h - (rect.h * 0.8), S.DECOR_PATH[border_image_name], (0.8, 0.8), (1, 0.5))

        tree_image3, tree_rect3 = decorations.place_decor_by_coordinates(row + rect.w/4, rect.h * 0.3, S.DECOR_PATH[border_image_name], (0.8, 0.8), (0.8, 0.8))
        tree_image4, tree_rect4 = decorations.place_decor_by_coordinates(row + rect.w/4, data["Image_rect"].h - (rect.h * 1.3), S.DECOR_PATH[border_image_name], (0.8, 0.8), (0.8, 0.5))
        if data["Image_rect"].w <= tree_rect3.x + tree_rect3.w:
            break
        decorations.decor_dict["Tree_M_1"][tree_amount] = {"name": border_image_name, "id": tree_amount, "image": tree_image1, "rect": tree_rect1, "effect": ""}
        tree_amount += 1
        decorations.decor_dict["Tree_M_1"][tree_amount] = {"name": border_image_name, "id": tree_amount, "image": tree_image2, "rect": tree_rect2, "effect": ""}
        tree_amount += 1

        decorations.decor_dict["Tree_M_1"][tree_amount] = {"name": border_image_name, "id": tree_amount, "image": tree_image3, "rect": tree_rect3, "effect": ""}
        tree_amount += 1
        decorations.decor_dict["Tree_M_1"][tree_amount] = {"name": border_image_name, "id": tree_amount, "image": tree_image4, "rect": tree_rect4, "effect": ""}
        tree_amount += 1

        row += rect.w * 0.5

    column = rect.h * 0.5
    while True:
        # building on the y axis (kaire ir desine)
        # kairei pirma juosta
        # desinei pirma
        # kairei antra
        # desinei antra

        tree_image1, tree_rect1 = decorations.place_decor_by_coordinates(0, column, S.DECOR_PATH["Tree_M_1"], (0.8, 0.8), (0.4, 0.5))
        tree_image2, tree_rect2 = decorations.place_decor_by_coordinates(data["Image_rect"].w - rect.w, column, S.DECOR_PATH["Tree_M_1"], (0.8, 0.8), (0.8, 0.7))

        tree_image3, tree_rect3 = decorations.place_decor_by_coordinates(rect.w * 0.4, column + rect.h/4, S.DECOR_PATH["Tree_M_1"], (0.8, 0.8), (0.8, 0.7))
        tree_image4, tree_rect4 = decorations.place_decor_by_coordinates(data["Image_rect"].w - (rect.w * 1.3), column + rect.h/4, S.DECOR_PATH["Tree_M_1"], (0.8, 0.8), (0.3, 0.7))
        if data["Image_rect"].h <= (tree_rect3.y + tree_rect3.h):
            break

        decorations.decor_dict["Tree_M_1"][tree_amount] = {"image": tree_image1, "rect": tree_rect1}
        tree_amount += 1
        decorations.decor_dict["Tree_M_1"][tree_amount] = {"image": tree_image2, "rect": tree_rect2}
        tree_amount += 1

        decorations.decor_dict["Tree_M_1"][tree_amount] = {"image": tree_image3, "rect": tree_rect3}
        tree_amount += 1
        decorations.decor_dict["Tree_M_1"][tree_amount] = {"image": tree_image4, "rect": tree_rect4}
        tree_amount += 1

        column += rect.w * 0.5

def render_door_open(screen):
    print("open Door")


def render_house(screen, data):
    screen.fill("black")
    tile_pos = (S.SCREEN_WIDTH * 0.1, S.SCREEN_HEIGHT * 0.1, S.SCREEN_WIDTH * 0.8, S.SCREEN_HEIGHT * 0.8)
    Ff.add_image_to_screen(screen, S.DECOR_PATH["Wooden_tiles"], tile_pos)
    door_rect = I.pg.Rect(S.SCREEN_WIDTH * 0.45, S.SCREEN_HEIGHT * 0.9, S.SCREEN_WIDTH * 0.11, S.SCREEN_HEIGHT * 0.05)
    I.T.Make_rect_visible(screen, door_rect, "white")
    return door_rect

def update_character_stats(file_path, player_data):
    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Update the Level and Experience lines
    for i, line in enumerate(lines):
        if line.startswith('Level:'):
            lines[i] = f'Level: {player_data["Level"]}\n'
        elif line.startswith('Experience:'):
            lines[i] = f'Experience: {player_data["Experience"]}\n'

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)