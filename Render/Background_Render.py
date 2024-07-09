import random

from utils import Frequent_functions as Ff, Imports as I
from Values import Settings as S

B_Left = 0
B_Top = 0
B_W = S.SCREEN_WIDTH
B_H = S.SCREEN_HEIGHT

def Start(pos):
    data = {}
    decor_count = {"Bush_S_1": 30, "Bush_S_2": 30, "Tree_T_1": 40}
    monster_count = {"Slime_S": 50}
    data["Window size"] = (B_W, B_H)  # Defines the size of the window (The rest is black)
    data["Zoom"] = (B_W / 4, B_H / 4)  # Defines how zoomed in to the picture the view is
    data["Image"] = I.pg.image.load(S.DECOR_PATH["Grass"]).convert_alpha()  # uploads the background image with transparent convert
    data["Image_rect"] = data["Image"].get_rect()  # Gets the rect of image
    data["Zoom_rect"] = I.pg.Rect(pos[0], pos[1], *data["Zoom"])  # creates a rect based on zoomed in picture (basicly makes a window)
    for key in decor_count:
        data[key] = generate_decor(decor_count[key], data["Image_rect"].size, S.DECOR_PATH[key])
    for key in monster_count:
        data[key] = generate_mobs(monster_count[key], data["Image_rect"].size, key)

    data["House_1"] = place_decor_by_coordinates(600, 380, S.DECOR_PATH["House_1"], (1.5, 1.5), (1.5, 1.4))
    # image_data["Church_1"] = place_decor_by_coordinates(200, 280, S.DECOR_PATH["Church_1"], (2, 2), (2, 2))
    return data

def Update(screen, data, mob_gif, combat_rect):
    data["Zoom_rect"].x = max(0, min(data["Zoom_rect"].x, data["Image_rect"].width - data["Zoom"][0]))
    data["Zoom_rect"].y = max(0, min(data["Zoom_rect"].y, data["Image_rect"].height - data["Zoom"][1]))
    sub_image = data["Image"].subsurface(data["Zoom_rect"]).copy()
    Collide = False
    me = I.pg.Rect(150, 85, S.SCREEN_WIDTH / 100, S.SCREEN_HEIGHT / 100)  # Player rect (if it gets hit with other rect. colide is set to True
    decor_options = ["House_1", "Bush_S_1", "Bush_S_2", "Tree_T_1"]
    mob_options = ["Slime_S"]
    displayed_rects = []  # List to keep track of displayed rectangles
    displayed_mobs = []

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
    killed_mobs = []
    for option in mob_options:
        for mob, value in data[option].items():
            decor_x = value["rect"][mob_gif].x - data["Zoom_rect"].x
            decor_y = value["rect"][mob_gif].y - data["Zoom_rect"].y
            rect = I.pg.Rect(decor_x, decor_y, value["rect"][mob_gif].w, value["rect"][mob_gif].h)

            sub_image.blit(value["image"][mob_gif], (decor_x, decor_y))
            displayed_mobs.append(rect)
            if combat_rect != 0:
                I.T.Make_rect_visible(sub_image, combat_rect)
                if combat_rect.colliderect(rect):
                    value["hp"] -= 1
                    if value["hp"] <= 0:
                        killed_mobs.append(mob)
            if me.colliderect(rect):
                Collide = (option, value["rect"][mob_gif].x, value["rect"][mob_gif].y)
                print("you collided with: ", option)
                # HERE RECIEVE DAMAGE
            if mob_gif == S.MOB_PATH[option][1]-1:
                touching_rect = Ff.check_if_mob_collides(displayed_rects, rect)  # returns 0 if no collision or returns obj number to what collides
                (value["rect"][mob_gif].x, value["rect"][mob_gif].y), value["visible"] = Ff.move_towards(touching_rect, data, value, (me.x + data["Zoom_rect"].x, me.y + data["Zoom_rect"].y),(value["rect"][mob_gif].x, value["rect"][mob_gif].y), 1, displayed_rects)
                # makes all coordinates the same so the gif works properly and not just one frame moved towards me
                for i in range(0, mob_gif):
                    value["rect"][i].x = value["rect"][mob_gif].x
                    value["rect"][i].y = value["rect"][mob_gif].y
    if killed_mobs != []:
        for key in killed_mobs:
            del data["Slime_S"][key]
    scaled_image = I.pg.transform.scale(sub_image, data["Window size"])
    screen.blit(scaled_image, (0, 0))
    return Collide
def display_char(dx, dy, screen, stance):
    character_path = 'static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER
    character_center_pos = [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2, S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7]
    dxdy = str(dx) + ", " + str(dy)
    orientation = {
        "0, 0": "Stand",
        "1, 0": "Side",
        "-1, 0": "Side1",
        "0, 1": "Front",
        "0, -1": "Back",
        "1, -1": "Back",
        "-1, -1": "Back",
        "1, 1": "Front",
        "-1, 1": "Front"
    }
    orientation_images = {
        "Front": ["Front.png", "Front1.png", "Front2.png"],
        "Back": ["Back.png", "Back1.png", "Back2.png"],
        "Side": ["Right.png", "Right1.png", "Right2.png"],
        "Side1": ["Left.png", "Left1.png", "Left2.png"]
    }

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
def generate_mobs(num_of_mobs, background_size, name):
    path = S.MOB_PATH[name][0]
    items = {}
    for i in range(num_of_mobs):
        x = random.randint(0, background_size[0]-100)
        y = random.randint(0, background_size[1]-350)
        image_list = []
        rect_list = []
        for a in range(0, S.MOB_PATH[name][1]):
            image = I.pg.image.load(path + name + "_" + str(a) + ".png").convert_alpha()
            rect = image.get_rect(topleft=(x, y))
            image_list.append(image)
            rect_list.append(rect)
        items[i] = {"image": image_list, "rect": rect_list, "visible": 0, "hp": I.mob_data.HP["Slime_S"]}
    return items
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


