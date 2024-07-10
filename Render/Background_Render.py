import random

from utils import Frequent_functions as Ff, Imports as I
from Values import Settings as S

B_Left = 0
B_Top = 0
B_W = S.SCREEN_WIDTH
B_H = S.SCREEN_HEIGHT

def read_txt_file(path):
    print(path)
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
    decor_count = {"Bush_S_1": 30, "Bush_S_2": 30, "Tree_T_1": 40}
    monster_count = {mob.name: mob.count}
    data["Window size"] = (B_W, B_H)  # Defines the size of the window (The rest is black)
    data["Zoom"] = (B_W / 4, B_H / 4)  # Defines how zoomed in to the picture the view is
    data["Image"] = I.pg.image.load(S.DECOR_PATH["Grass"]).convert_alpha()  # uploads the background image with transparent convert
    data["Image_rect"] = data["Image"].get_rect()  # Gets the rect of image
    data["Zoom_rect"] = I.pg.Rect(pos[0], pos[1], *data["Zoom"])  # creates a rect based on zoomed in picture (basicly makes a window)
    for key in decor_count:
        data[key] = generate_decor(decor_count[key], data["Image_rect"].size, S.DECOR_PATH[key])
    for key in monster_count:
        data[key] = generate_mobs(mob, data["Image_rect"].size)

    data["House_1"] = place_decor_by_coordinates(600, 380, S.DECOR_PATH["House_1"], (1.5, 1.5), (1.5, 1.4))
    # image_data["Church_1"] = place_decor_by_coordinates(200, 280, S.DECOR_PATH["Church_1"], (2, 2), (2, 2))
    return data

def Update(screen, data, mob_gif, combat_rect, mob, gif):
    data["Zoom_rect"].x = max(0, min(data["Zoom_rect"].x, data["Image_rect"].width - data["Zoom"][0]))
    data["Zoom_rect"].y = max(0, min(data["Zoom_rect"].y, data["Image_rect"].height - data["Zoom"][1]))
    sub_image = data["Image"].subsurface(data["Zoom_rect"]).copy()
    Collide = False
    me = I.pg.Rect(150, 85, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
    decor_options = ["House_1", "Bush_S_1", "Bush_S_2", "Tree_T_1"]
    displayed_rects = []  # List to keep track of displayed rectangles

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

    for current_mob in mob.mobs:
        mob_rect = current_mob["rect"][mob_gif]
        mob_x = mob_rect.x - data["Zoom_rect"].x
        mob_y = mob_rect.y - data["Zoom_rect"].y
        rect = I.pg.Rect(mob_x, mob_y, mob_rect.w, mob_rect.h)
        sub_image.blit(current_mob["image"][mob_gif], (mob_x, mob_y))
        if combat_rect != 0:
            if combat_rect.colliderect(rect):
                mob.deal_damage(current_mob)
                gif.Start_gif("Blunt", current_mob)
                # Ff.add_image_to_screen(sub_image, S.COMBAT_PATH["Blunt"][0] + str(mob_gif) + ".png", [mob_rect.x, mob_rect.y, mob_rect.w, mob_rect.h])
        if me.colliderect(rect):
            Collide = (current_mob, mob_rect.x, mob_rect.y)
            print("you collided with: ", current_mob)
        if mob_gif == S.MOB_PATH[mob.name][1] - 1:
            target_pos = (me.x + data["Zoom_rect"].x, me.y + data["Zoom_rect"].y)
            mob_rect.x, mob_rect.y, current_mob["visible"] = Ff.move_towards(target_pos, current_mob, 1, displayed_rects, data["Zoom_rect"], sub_image)
            mob.update_position(mob_rect.x, mob_rect.y, current_mob)
            # HERE RECEIVE DAMAGE
        if gif.start_gif and current_mob == gif.rect:
            frame = gif.next_frame()
            sub_image.blit(frame, (mob_x, mob_y))  # made specifically for damage displaying

    scaled_image = I.pg.transform.scale(sub_image, data["Window size"])
    screen.blit(scaled_image, (0, 0))
    return Collide
def display_char(dx, dy, screen, stance, combat_rect):
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
    if combat_rect != 0:
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
            character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20 + dx * 10,S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2 + dy * 10, S.SCREEN_WIDTH / 14,S.SCREEN_HEIGHT / 7]
    else:
        character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20,S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2, S.SCREEN_WIDTH / 14,S.SCREEN_HEIGHT / 7]

    orient = orientation[dxdy]
    if orient in orientation_images:
        images = orientation_images[orient]
        if stance == 0 or stance == 2:
            body = Ff.add_image_to_screen(screen, character_path + images[0], character_center_pos)
        elif stance == 1:
            body = Ff.add_image_to_screen(screen, character_path + images[1], character_center_pos)
        else:
            body = Ff.add_image_to_screen(screen, character_path + images[2], character_center_pos)
        I.info.LAST_ORIENT = orientation_images[orient]
    else:
        body = Ff.add_image_to_screen(screen, character_path + I.info.LAST_ORIENT[0], character_center_pos)
    return body

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

def BackPack(screen):
    pressed = 0
    fill_backpack(screen)
    running = True
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_b:
                    pressed = I.pg.K_b
            elif event.type == I.pg.KEYUP:
                if event.key == pressed:
                    running = False  # exits backpackview
            I.pg.display.flip()

def fill_backpack(screen):
    rect = screen.get_rect()
    bag = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Backpack_Empty"], [rect.center[0] * 0.5 ,rect.center[1] * 0.25, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT * 0.75])
    if I.info.BACKPACK_COORDINATES_X == {}:
        bag_coordinates(screen, bag)

    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    i = 0
    for content in I.info.BACKPACK_CONTENT.keys():
        Ff.add_image_to_screen(screen, S.PLAYING_PATH[content], [list(I.info.BACKPACK_COORDINATES_X.values())[i], list(I.info.BACKPACK_COORDINATES_Y.values())[i], item_w, item_h])
        Ff.display_text(screen, str(I.info.BACKPACK_CONTENT[content]), 2, [list(I.info.BACKPACK_COORDINATES_X.values())[i], list(I.info.BACKPACK_COORDINATES_Y.values())[i]], "white")
        i += 2

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

    I.info.BACKPACK_COORDINATES_X = coordinates_x
    I.info.BACKPACK_COORDINATES_Y = coordinates_y


def place_decor_by_coordinates(x, y, path, scale, rect_scale):
    items = {}
    image = I.pg.image.load(path).convert_alpha()
    rect = image.get_rect(topleft=(x, y))
    image = I.pg.transform.scale(image, (rect.w * scale[0], rect.h * scale[1]))
    rect.w = rect.w * rect_scale[0]
    rect.h = rect.h * rect_scale[1]
    items[0] = {"image": image, "rect": rect}
    return items


def render_attack(screen, path, pos, combat_rect):
    if combat_rect != 0:

        character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2, S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]
        # orientation = I.info.LAST_ORIENT[0].split(".")[0]
        # attack_direction = {"Front": (character_center_pos[2] * 0.1, character_center_pos[3] * 0.35),
        #                     "Back": (0, 0),
        #                     "Left": (-character_center_pos[2] * 0.2, 0),
        #                     "Right": (character_center_pos[2] * 0.2, 0)}

        if I.info.EQUIPED["Hand1"] == 0 and I.info.EQUIPED["Hand2"] == 0:
            # shirt_rect = I.pg.Rect(character_center_pos[0] + attack_direction[orientation][0], character_center_pos[1] + attack_direction[orientation][1], character_center_pos[2] * 0.15, character_center_pos[3] * 0.2)
            # combat_rect.y = 80

            # combat_rect.w = S.SCREEN_WIDTH / 200
            # combat_rect.h = S.SCREEN_HEIGHT / 200
            # print(data["Player"])
            # I.T.Make_rect_visible(screen, shirt_rect, data["Player"]["Color_Shir"])
            I.T.Make_rect_visible(screen, shirt_rect, data["Player"]["Skin"])
