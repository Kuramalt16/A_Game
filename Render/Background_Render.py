import random

from utils import Frequent_functions as Ff, Imports as I
from Values import Settings as S

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
def Start(pos, mob):
    data = {}
    data["Player"] = read_txt_file('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt")
    data["Player"] = update_character(data["Player"])
    decor_count = {"Bush_S_1": 30, "Bush_S_2": 30, "Tree_T_1": 40}
    monster_count = {}
    for key, current_mob in mob.items():
        monster_count[current_mob.name] = current_mob.count

    data["Window size"] = (B_W, B_H)  # Defines the size of the window (The rest is black)
    data["Zoom"] = (B_W / 4, B_H / 4)  # Defines how zoomed in to the picture the view is
    data["Image"] = I.pg.image.load(S.DECOR_PATH["Grass"]).convert_alpha()  # uploads the background image with transparent convert
    data["Image_rect"] = data["Image"].get_rect()  # Gets the rect of image
    data["Zoom_rect"] = I.pg.Rect(pos[0], pos[1], *data["Zoom"])  # creates a rect based on zoomed in picture (basicly makes a window)
    for key in decor_count:
        data[key] = generate_decor(decor_count[key], data["Image_rect"].size, S.DECOR_PATH[key])
    for key in monster_count:
        data[key] = generate_mobs(mob[key], data["Image_rect"].size)

    data["House_1"] = place_decor_by_coordinates(600, 380, S.DECOR_PATH["House_1"], (1.5, 1.5), (1.5, 1.4))
    # image_data["Church_1"] = place_decor_by_coordinates(200, 280, S.DECOR_PATH["Church_1"], (2, 2), (2, 2))
    return data

def Update(screen, data, mob_dict, gifs, song, spells):
    data["Zoom_rect"].x = max(0, min(data["Zoom_rect"].x, data["Image_rect"].width - data["Zoom"][0]))
    data["Zoom_rect"].y = max(0, min(data["Zoom_rect"].y, data["Image_rect"].height - data["Zoom"][1]))
    sub_image = data["Image"].subsurface(data["Zoom_rect"]).copy()
    me = I.pg.Rect(150, 85, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True

    collide, displayed_rects = handle_decor_visualisation(data, sub_image)

    for mob in mob_dict.values():
        for current_mob in mob.mobs:
            mob_gif = current_mob["gif_frame"][0]
            mob_rect = current_mob["rect"][mob_gif]
            mob_x = mob_rect.x - data["Zoom_rect"].x
            mob_y = mob_rect.y - data["Zoom_rect"].y
            rect = I.pg.Rect(mob_x, mob_y, mob_rect.w, mob_rect.h)
            update_health(rect, current_mob, sub_image)
            sub_image.blit(current_mob["image"][mob_gif], (mob_x, mob_y))



            if I.info.COMBAT_RECT != 0:
                handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob)

            handle_damage_type_visualisation(sub_image, current_mob, gifs, (mob_x, mob_y), data, mob)


            if me.colliderect(rect) and current_mob["allignment"] in [6, 8, 9]:
                collide = ('mob', current_mob, mob_rect.x, mob_rect.y)
                data["Player"]["hp"] = data["Player"]["hp"][0] - current_mob["damage"][0], data["Player"]["hp"][1]

            handle_mob_speed(data, current_mob, displayed_rects, mob)



    collide = handle_death_visualisation(sub_image, data, gifs, collide)

    handle_npc_visualisation(sub_image, data, gifs)

    if not data["Player"]["dead"]:
        cast_spell_handle(sub_image, data, spells, gifs, mob_dict, song)

    scaled_image = I.pg.transform.scale(sub_image, data["Window size"])
    screen.blit(scaled_image, (0, 0))
    if data["Player"]["dead"] and collide[0] == "mob":  # dont hit mobs when u dead
        collide = False, 0, 0, 0
    return collide


def handle_mob_speed(data, current_mob, displayed_rects, mob):

    me = I.pg.Rect(150, 85, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
    speed = current_mob["speed"][0]
    current_frame = current_mob["gif_frame"][0]
    frame_count = current_mob["gif_frame"][1]
    if current_frame % 2 == 0:
        if not data["Player"]["dead"] and current_mob["allignment"] == 6:
            target_pos = (me.x + data["Zoom_rect"].x, me.y + data["Zoom_rect"].y)
            mob_rect = current_mob["rect"][current_frame]
            mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_towards(target_pos, current_mob, speed, displayed_rects, data["Zoom_rect"])
            mob.update_position(mob_rect.x, mob_rect.y, current_mob)
        else:
            current_mob["visible"] = False
def handle_damage_type_visualisation(sub_image, current_mob, gifs, pos, data, mob):
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


def handle_physical_damaging_mobs(rect, song, mob, data, gifs, current_mob):
    for key in ["Blunt", "Piercing", "Slashing"]:
        if I.info.COMBAT_RECT.colliderect(rect) and not gifs[key].start_gif:
            curr_song = song["Playing"]
            effect = song[curr_song].generate_thump_sound()
            song[curr_song].play_effect(effect)
            gifs["Blunt"].Start_gif(key, current_mob)
            mob.deal_damage(current_mob, data["Player"], "")

def handle_death_visualisation(sub_image, data, gifs, collide):
    if data["Player"]["dead"]:
        me = I.pg.Rect(150, 85, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
        dead_disc = {"Portal": display_gif_on_subimage(sub_image, (S.SCREEN_WIDTH / 16, S.SCREEN_HEIGHT / 10), (I.info.START_POS[0] * 1.6 - data["Zoom_rect"].x , I.info.START_POS[1] + 10 * 16 - data["Zoom_rect"].y), gifs["Portal"]),
                     "Sign": display_on_subimage(sub_image, (S.SCREEN_WIDTH / 90, S.SCREEN_HEIGHT / 40), S.PLAYING_PATH["Sign"],(I.info.START_POS[0] * 1.6 - data["Zoom_rect"].x,I.info.START_POS[1] + 10 * 10 - data["Zoom_rect"].y)),
                     "Grave": display_on_subimage(sub_image, (S.SCREEN_WIDTH / 60, S.SCREEN_HEIGHT / 30), S.PLAYING_PATH["Grave"], (data["Player"]["dead"].x - data["Zoom_rect"].x + me.x, data["Player"]["dead"].y - data["Zoom_rect"].y + me.y)),
                     }
        dead_list = list(dead_disc.values())
        if me.collidelistall(dead_list):
            keys = list(dead_disc.keys())
            key = keys[me.collidelistall(dead_list)[0]]
            collide = (key, dead_disc[key].x, dead_disc[key].y)
    return collide
def handle_npc_visualisation(sub_image, data, gifs):
    npc = {"Luna": display_gif_on_subimage(sub_image, (17,18), (I.info.START_POS[0] * 1.6 - data["Zoom_rect"].x , I.info.START_POS[1] + 10 * 43 - data["Zoom_rect"].y), gifs["Luna"]),
           "Bear": display_gif_on_subimage(sub_image, (17,18), (I.info.START_POS[0] * 1.7 - data["Zoom_rect"].x , I.info.START_POS[1] + 10 * 43 - data["Zoom_rect"].y), gifs["Bear"]),
    }

def handle_decor_visualisation(data, sub_image):
    Collide = [False]
    me = I.pg.Rect(150, 85, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
    displayed_rects = []  # List to keep track of displayed rectangles
    decor_options = ["House_1", "Bush_S_1", "Bush_S_2", "Tree_T_1"]
    for option in decor_options:
        for decor in data[option].values():
            # Gets x, y position of decoration
            decor_x = decor["rect"].x - data["Zoom_rect"].x
            decor_y = decor["rect"].y - data["Zoom_rect"].y

            rect = I.pg.Rect(decor_x, decor_y, decor["rect"].w, decor["rect"].h)

            # Check if current decor collides with any already displayed decor
            if not any(rect.colliderect(displayed_rect) for displayed_rect in displayed_rects):
                if (data["Image"].get_at((decor["rect"].x, decor["rect"].y)) == (137, 176, 46, 255) and data["Image"].get_at((decor["rect"].x + decor["rect"].w, decor["rect"].y + decor["rect"].h)) == (137, 176, 46, 255)):
                    sub_image.blit(decor["image"], (decor_x, decor_y))
                    displayed_rects.append(rect)  # Add to the list of displayed rectangles
                    if option in I.info.ENTERABLE:
                        door_rect = I.pg.Rect(rect.left + rect.w * 0.6, rect.top + rect.h * 0.60, rect.w / 4, rect.h / 2)
                        # I.T.Make_rect_visible(sub_image, me)
                        if me.colliderect(door_rect):
                            Collide = ("Door", door_rect.x, door_rect.y)
                    if me.colliderect(rect):
                        Collide = (option, decor["rect"].x, decor["rect"].y)
    return Collide, displayed_rects
def display_char(dx, dy, screen, gifs):
    character_path = 'static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER
    dxdy = (dx, dy)
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
    if gifs["ghost"].start_gif:
        frame = gifs["ghost"].next_frame(-1)
        frame = I.pg.transform.scale(frame, (S.SCREEN_WIDTH / 18, S.SCREEN_HEIGHT / 7))
        screen.blit(frame, [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2])
    else:
        if I.info.COMBAT_RECT != 0:
            if dx == 0 and dy == 0:
                for key, value in orientation.items():
                    if value == I.info.LAST_ORIENT[0].split(".")[0]:
                        dx = key[0]
                        dy = key[1]
                        break
                character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + dx * 5,S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + dy * 5, S.SCREEN_WIDTH / 14,S.SCREEN_HEIGHT / 7]
                dx = 0
                dy = 0
            else:
                character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + dx * 10, S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + dy * 10, S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]
        else:
            character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2, S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]

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
    border = 1
    use = 0
    selected = 0
    color = "Yellow"
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
                        selected = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
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
                    pressed = I.pg.K_UP
                    if block[1] < 0:
                        block = (block[0], 26)
                elif event.key == I.pg.K_DOWN:
                    block = (block[0], block[1] + 2)
                    pressed = I.pg.K_DOWN
                    if block[1] > 26:
                        block = (block[0], 0)
                elif event.key == I.pg.K_LEFT:
                    block = (block[0] - 2, block[1])
                    pressed = I.pg.K_LEFT
                    if block[0] < 0:
                        block = (14, block[1])
                elif event.key == I.pg.K_RIGHT:
                    block = (block[0] + 2, block[1])
                    pressed = I.pg.K_RIGHT
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

            rect = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
            fill_backpack(screen, player)
            I.pg.draw.rect(screen, color, rect, border)
            if selected != 0:
                I.pg.draw.rect(screen, "Yellow", selected, 2)

            I.pg.display.flip()

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
        Ff.add_image_to_screen(screen, S.ITEM_PATHS[content], [list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn], item_w, item_h])
        Ff.display_text(screen, str(I.info.BACKPACK_CONTENT[content][0]), 2, [list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn]], "white")

    I.pg.draw.rect(screen, "black", (bag.w * 0.626, bag.h * 0.807, bag.w * 0.115, bag.h * 0.012))
    remainder = player["hp"][0] / player["hp"][1]
    I.pg.draw.rect(screen, "red", (bag.w * 0.626, bag.h * 0.807, bag.w * 0.115 * remainder, bag.h * 0.012))
    Ff.display_text(screen, "Hp", 1, (bag.w * 0.57, bag.h * 0.80), "black")

    I.pg.draw.rect(screen, "black", (bag.w * 0.83, bag.h * 0.807, bag.w * 0.125, bag.h * 0.012))
    remainder = player["mana"][0] / player["mana"][1]
    I.pg.draw.rect(screen, "blue", (bag.w * 0.83, bag.h * 0.807, bag.w * 0.125 * remainder, bag.h * 0.012))
    Ff.display_text(screen, "Mp", 1, (bag.w * 0.78, bag.h * 0.80), "black")

    I.pg.draw.rect(screen, "black", (bag.w * 0.626, bag.h * 0.857, bag.w * 0.115, bag.h * 0.012))
    remainder = player["Exhaustion"][0] / player["Exhaustion"][1]
    I.pg.draw.rect(screen, "Green", (bag.w * 0.626, bag.h * 0.857, bag.w * 0.115 * remainder, bag.h * 0.012))
    Ff.display_text(screen, "Exh", 1, (bag.w * 0.57, bag.h * 0.85), "black")

    return bag

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
                # screen.set_at((left, top), (0, 0, 0, 255))
                I.pg.display.flip()
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
                        for spell, (disc, row, collum) in I.info.SPELLBOOK_CONTENT.items():
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
        row = I.info.SPELLBOOK_CONTENT[content][1]
        collumn = I.info.SPELLBOOK_CONTENT[content][2]
        Ff.add_image_to_screen(screen, S.SPELL_PATHS[content] + "0.png", [list(I.info.SPELLBOOK_COORDINATES_X.values())[row], list(I.info.SPELLBOOK_COORDINATES_Y.values())[collumn], item_w, item_h])
def display_gif_on_subimage(sub_image, size, pos, gif):
    frame = gif.next_frame(-1)
    frame = I.pg.transform.scale(frame, (size[0], size[1]))
    sub_image.blit(frame, pos)
    return I.pg.Rect(pos[0], pos[1], size[0], size[1])

def cast_spell_handle(sub_image, data, spells, gifs, mob, song):
    for slot, spell in spells.selected_spell.items():
        if gifs[spell].start_gif:
            frame = gifs[spell].next_frame(1)
            frame = I.pg.transform.scale(frame, (20, 20))
            if spells.direction[spell] == 0:
                spells.init_cast[spell] = data["Zoom_rect"].copy()
                spells.direction[spell] = I.info.LAST_ORIENT[0].split(".")[0]
            direction_settings = {
                "Front": {"rect": (145, 80), "dir": (0, -1), "rotate": 90, "flip": (False, True)},
                "Back": {"rect": (145, 70), "dir": (0, 1), "rotate": 90, "flip": (False, False)},
                "Left": {"rect": (140, 75), "dir": (1, 0), "rotate": 0, "flip": (True, False)},
                "Right": {"rect": (150, 75), "dir": (-1, 0), "rotate": 0, "flip": (False, False)},
            }
            spell_direction = spells.direction[spell]
            settings = direction_settings.get(spell_direction)
            me = I.pg.Rect(settings["rect"][0], settings["rect"][1], S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)
            dir = settings["dir"]
            frame = I.pg.transform.rotate(frame, settings["rotate"])
            frame = I.pg.transform.flip(frame, *settings["flip"])

            if gifs[spell].current_frame != 0:
                rect = I.pg.Rect(spells.init_cast[spell].x - data["Zoom_rect"].x + me.x - dir[0] * gifs[spell].current_frame * 6, spells.init_cast[spell].y - data["Zoom_rect"].y + me.y - dir[1] * gifs[spell].current_frame * 6, 20, 20)
                sub_image.blit(frame, rect)
                for key in mob.keys():
                    for current_mob in mob[key].mobs:
                        mob_rect = I.pg.Rect(current_mob["rect"][0].x - data["Zoom_rect"].x, current_mob["rect"][0].y - data["Zoom_rect"].y, current_mob["rect"][0].w, current_mob["rect"][0].h)
                        if rect.colliderect(mob_rect):
                            mob[key].deal_damage(current_mob, data["Player"], spells.spell_dict[spell])
                            gifs[spell].start_gif = False # IF COMMENTED OUT, MAKES A SPELL GO THROUGH MULTIPLE ENEMIES
                            type = spells.spell_dict[spell].split(" ")[1]
                            gifs[type].Start_gif(type, current_mob)
                            curr_song = song["Playing"]
                            sound_type = {"Force": song[curr_song].generate_magic_sound(),
                                          "Fire": song[curr_song].generate_fire_sound(),
                                          "Cold": song[curr_song].generate_cold_sound()}
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
        if text[a-1] == "\n":
            collumn += 20
            row = 100
            text = text[a+1:]
            a = 0
        Ff.display_text(screen, text[0:a], 10, (row, S.SCREEN_HEIGHT / 2 + collumn),  "black")
        I.pg.time.wait(10)
        a += 1
        if a > len(text):
            while running:
                for event in I.pg.event.get():
                    if event.type == I.pg.KEYDOWN and event.key == I.pg.K_c:
                        running = False

        I.pg.display.flip()


