from utils import Imports as I
from Values import Settings as S
from Render import Settings_render as sr


def add_image_to_screen(screen, path, pos):
    image = I.pg.image.load(path).convert_alpha()
    image = I.pg.transform.scale(image, (pos[2], pos[3]))
    rect = image.get_rect()
    I.pg.Surface.blit(screen, image, (pos[0], pos[1]))
    rect = rect.move(pos[0], pos[1])
    return rect


def toggle_bool(var):
    if var:
        var = False
    else:
        var = True
    return var


def base_settings_load():
    print("base settings")


def display_text(screen, text, size, pos_tuple, color):
    font = I.pg.font.SysFont('minecraft', int(size + S.RESOLUTION * 10))
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = pos_tuple
    screen.blit(text_surface, text_rect)
    return text_rect


def button_click_render(screen, button, data, name):
    if data == 1:
        # Pressed down
        button = add_image_to_screen(screen, 'static/images/' + name + "_Clicked.png",
                                     [button.left, button.top, button.width, button.height])
    elif data == 0:
        button = add_image_to_screen(screen, 'static/images/' + name + ".png",
                                     [button.left, button.top, button.width, button.height])
    else:
        text = display_text(screen, "A RESTART IS REQUIRED FOR THE CHANGES TO TAKE EFFECT (CANCEL IF UNWANTED)", 10,
                            (sr.CB_LEFT, sr.CB_TOP * 2.8), "black")
        I.pg.display.update(text)
        interval = (sr.SLIDER_MAX - sr.SLIDER_MIN) / 10
        data = data - button.width / 2
        data = round(data / interval) * interval
        if data > sr.SLIDER_MAX:
            data = sr.SLIDER_MAX
        elif data < sr.SLIDER_MIN:
            data = sr.SLIDER_MIN

        add_image_to_screen(screen, 'static/images/Frame_main_menu.png',
                            [sr.S_LEFT, sr.S_TOP, sr.S_F_WIDTH, sr.S_F_HEIGHT])
        slider = add_image_to_screen(screen, 'static/images/Slider.png',
                                     [S.SCREEN_WIDTH / 2, sr.SLIDER_TOP, sr.SLIDER_WIDTH, sr.SLIDER_HEIGHT])
        I.pg.display.update(slider)
        button = add_image_to_screen(screen, 'static/images/' + name + "_Clicked.png",
                                     [data, button.top, button.width, button.height])
    return button


def Coloring_tool(screen, size, change, iteration, mode):
    color_list = list(I.A.color_mappings.get(change, {}).values())
    search_at = {"Eyes": [190, 220, 600, 670],
                 "Skin":  [size.top, size.top+size.h, size.left, size.left+size.w],
                 "Skin2":  [size.top, size.top+size.h, size.left, size.left+size.w],
                 "Color_Hair": [110, 270, 550, 730],
                 "Color_Shir": [200, 320, 550, 740],
                 "Color_Pant": [300, 375, 560, 700],
                 "Color_Shoe": [360, 404, 560, 700]}
    found = False
    if iteration >= len(color_list):
        iteration = 0
    if iteration < 0:
        iteration = len(color_list) - 1
    for top in range(search_at[change][0], search_at[change][1]):
        for i in range(search_at[change][2], search_at[change][3]):
            color = screen.get_at((i, top))
            if color == I.A.DEFAULT_TEMP[change] and mode == 0:
                screen.set_at((i, top), color_list[iteration])
                found = True
            elif color == S.DEFAULT[change] and mode == 1:
                screen.set_at((i, top), color_list[iteration])
    if found:
        I.A.DEFAULT_TEMP[change] = color_list[iteration]
    return iteration


def button_click_render_down(screen, button, data, path):
    if data == 0:
        button = add_image_to_screen(screen, path,[button.left, button.top, button.width, button.height])
    else:
        button = add_image_to_screen(screen, path,[button.left, button.top + 2, button.width, button.height])
    return button


def find_iteration(list, change):
    for i in range(0, len(list)):
        if list[i] == I.A.DEFAULT_TEMP[change]:
            return i


def styling_tool(option, screen, rect, iteration):
    folder_path = 'static/images/Clothes/' + option + '/'
    max_count = count_files_with_one(folder_path, "_")
    if iteration < 1:
        iteration = max_count
    if iteration > max_count:
        iteration = 1
    path = folder_path + option + "_" + str(iteration) + ".png"
    rect = add_image_to_screen(screen, path, (rect.left, rect.top, rect.w, rect.h))
    I.TD.Appearance[option] = iteration
    return iteration, rect

def styling_tool_path(option, screen, rect, iteration, path_addon):
    folder_path = 'static/images/Clothes/' + option + '/'
    max_count = count_files_with_one(folder_path, "_")
    if iteration < 1:
        iteration = max_count
    if iteration > max_count:
        iteration = 1
    if option != "Hair" and path_addon == "_Back":
        path_addon = ""
    if "1" in path_addon:
        split = path_addon.split("1")
        path_addon = split[0] + split[1]
        path = folder_path + option + "_" + str(iteration) + path_addon + ".png"
        rect = flip_rect(screen, path, rect)
    else:
        path = folder_path + option + "_" + str(iteration) + path_addon + ".png"
        rect = add_image_to_screen(screen, path, (rect.left, rect.top, rect.w, rect.h))
    I.TD.Appearance[option] = iteration
    return iteration, rect


def count_files_with_one(folder_path, thing):
    files = I.os.listdir(folder_path)
    count = 0
    for file in files:
        if file.count(thing) == 1:
            count += 1
    return count

def flip_rect(screen, path, size):
    image = I.pg.image.load(path)
    scaled_image = I.pg.transform.scale(image, (size[2], size[3]))
    flipped_subsurface = I.pg.transform.flip(scaled_image, True, False)
    screen.blit(flipped_subsurface, (size[0], size[1]))
    return I.pg.Rect(size[0], size[1], size[2], size[3])

def remove_white_pixels(image_path):
    with I.img.open(image_path) as img:
        img = img.convert("RGBA")
        datas = img.getdata()
        new_data = []
        for item in datas:
            if item[:3] == (255, 255, 255):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        img.save(image_path, "PNG")


def read_text_file_return_dict(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            txt_dictionary = {}
            lines = data.split("\n")
            for value in lines:
                if ":" in value:
                    line_content = value.split(": ")
                    txt_dictionary[line_content[0]] = line_content[1]
            return txt_dictionary
    except FileNotFoundError:
        return f"The file {file_path} does not exist."
    except Exception as e:
        return f"An error occurred: {e}"

def Gif_maker(image_folder, duration, name):
    print("use the movement parts to create four gifs for moving up down left right also do this in save character to properly save the character moving")
    # Get all the image files in the folder
    orientation_keys = S.GIF_DICT.keys()
    image_files = [I.os.path.join(image_folder, file) for file in I.os.listdir(image_folder) if file.endswith(('png', 'jpg', 'jpeg'))]
    print(image_files)

    # Sort the image files by name to ensure correct order
    for key in orientation_keys:
        new_image_files = []
        path_endings = S.GIF_DICT[key].split(", ")
        for path_end in path_endings:
            new_image_files.append('static/data/created_characters/' + name + "/" + name + path_end + ".png")
        images = [I.img.open(image) for image in new_image_files]
        I.os.makedirs('static/data/created_characters/' + name + "/gif", exist_ok=True)
        images[0].save('static/data/created_characters/' + name + "/gif/" + name + key + ".gif", save_all=True, append_images=images[1:], duration=duration,loop=0, disposal=2)
def clothe_walkers(value, screen):
    S_LEFT = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 5)
    S_TOP = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / 2.2)
    S_F_WIDTH = S.SCREEN_WIDTH - (2 * S_LEFT)
    S_F_HEIGHT = S.SCREEN_HEIGHT / 10 * 8

    orientation = ["_Walk.png", "_Walk1.png", "_Back_Walk.png", "_Back_Walk1.png", "_Side_Walk.png", "_Side_Walk1.png", "_Side_Walk11.png", "_Side_Walk12.png"]
    name = value["Name"]
    gender = value["Gender"]
    race = str(value["Race"].split("_")[0])

    pos = [S_LEFT + S_F_WIDTH / 4, S_TOP + S_F_HEIGHT / 6, S_F_WIDTH / 2, S_F_HEIGHT / 2]


    path = "static/images/Race/" + race + "/" + gender + "/" + race + "_" + gender
    txt_data = read_text_file_return_dict('static/data/created_characters/' + name + "/" + name + ".txt")

    for i in orientation:
        screen.fill("white")
        body = add_image_to_screen(screen, path + i, pos)
        dress_by_dict(body, txt_data, screen, i)
        sub_surface = screen.subsurface(body)
        I.pg.image.save(sub_surface, "static/data/created_characters/" + value["Name"] + "/" + value["Name"] + i)
        remove_white_pixels("static/data/created_characters/" + value["Name"] + "/" + value["Name"] + i)


    # saves pic
    # sub_surface = screen.subsurface(I.TD.Char_Rect)
    # I.pg.image.save(sub_surface, "static/data/created_characters/" + value["Name"] + "/" + value["Name"] + side + ".png")



def dress_by_dict(rect, dict, screen, orientation):
    search_at = {"Eyes": [170, 200, 600, 670],
                 "Skin":  [rect.top, rect.top+rect.h, rect.left, rect.left+rect.w],
                 "Skin2":  [rect.top, rect.top+rect.h, rect.left, rect.left+rect.w],
                 "Color_Hair": [110, 270, 550, 730],
                 "Color_Shir": [200, 320, 550, 740],
                 "Color_Pant": [300, 375, 560, 710],
                 "Color_Shoe": [350, 414, 500, 750]}
    first = ["Eyes", "Skin", "Skin2"]
    second = ["Pant", "Shoe", "Shir", "Hair"]
    third = ["Color_Shoe", "Color_Shir", "Color_Pant", "Color_Hair"]

    # skin color
    for change in first:
        tuple_data = dict[change].strip('()')
        tuple_elements = tuple_data.split(',')
        for top in range(search_at[change][0], search_at[change][1]):
            for i in range(search_at[change][2], search_at[change][3]):
                color = screen.get_at((i, top))
                if color == S.DEFAULT[change]:
                    screen.set_at((i, top), tuple(map(int, tuple_elements)))

    # Clothing
    for clothing in second:
        path = 'static/images/Clothes/' + clothing + "/" + dict[clothing] + orientation
        if clothing == "Hair":
            new_orientation = {
                "_Walk.png": ".png",
                "_Walk1.png": ".png",
                "_Back_Walk.png": "_Back.png",
                "_Back_Walk1.png": "_Back.png",
                "_Side_Walk.png": "_Side.png",
                "_Side_Walk1.png": "_Side.png",
                "_Side_Walk11.png": "_Side1.png",
                "_Side_Walk12.png": "_Side1.png",}
            path = 'static/images/Clothes/' + clothing + "/" + dict[clothing] + new_orientation[orientation]
        elif clothing == "Shir" or clothing == "Pant":
            new_orientation = {
                "_Walk.png": "_Walk.png",
                "_Walk1.png": "_Walk1.png",
                "_Back_Walk.png": "_Walk.png",
                "_Back_Walk1.png": "_Walk1.png",
                "_Side_Walk.png": "_Side_Walk.png",
                "_Side_Walk1.png": "_Side_Walk1.png",
                "_Side_Walk11.png": "_Side_Walk.png",
                "_Side_Walk12.png": "_Side_Walk1.png", }
            path = 'static/images/Clothes/' + clothing + "/" + dict[clothing] + new_orientation[orientation]
        elif clothing == "Shoe":
            new_orientation = {
                "_Walk.png": "_Walk.png",
                "_Walk1.png": "_Walk1.png",
                "_Back_Walk.png": "_Walk.png",
                "_Back_Walk1.png": "_Walk1.png",
                "_Side_Walk.png": "_Side_Walk.png",
                "_Side_Walk1.png": "_Side_Walk.png",
                "_Side_Walk11.png": "_Side_Walk1.png",
                "_Side_Walk12.png": "_Side_Walk1.png", }
            path = 'static/images/Clothes/' + clothing + "/" + dict[clothing] + new_orientation[orientation]
        rect = add_image_to_screen(screen, path, (rect.left, rect.top, rect.w, rect.h))
    # Coloring Clothing

    for change in third:
        tuple_data = dict[change].strip('()')
        tuple_elements = tuple_data.split(',')
        for top in range(search_at[change][0], search_at[change][1]):
            for i in range(search_at[change][2], search_at[change][3]):
                color = screen.get_at((i, top))
                if color == S.DEFAULT[change]:
                    screen.set_at((i, top), tuple(map(int, tuple_elements)))
    I.pg.display.flip()


def move_towards(target, current_mob, step_size, obstacles, zoom_rect, sub_screen):
    """
    Move the mob towards the target position while avoiding obstacles.

    Args:
        target (tuple): Target position (x, y).
        mob_rect (Rect): The Rect object for the mob.
        step_size (float): The step size for each movement.
        obstacles (list): List of Rect objects representing obstacles.
        zoom_rect (Rect): The Rect object for the zoomed area of the screen.

    Returns:
        tuple: New (x, y) position for the mob.
    """
    # Current position
    current_x, current_y = current_mob['current_pos'].topleft

    # Calculate direction vector and distance to the target
    direction_x, direction_y = target[0] - current_x, target[1] - current_y
    distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

    if distance > 100:
        return current_x, current_y, False
    # Check if we are close enough to the target
    if distance < step_size:
        print("Reached target")
        return target[0], target[1], True

    # Normalize direction vector
    if distance > 0:
        direction_x /= distance
        direction_y /= distance

    # Calculate new position
    new_x = current_x + direction_x * step_size
    new_y = current_y + direction_y * step_size

    # Create new Rect for the potential new position
    new_rect = I.pg.Rect(new_x - zoom_rect.x, new_y - zoom_rect.y, current_mob['current_pos'].w, current_mob['current_pos'].h)
    # I.T.Make_rect_visible(sub_screen, new_rect)
    # Check for collisions
    if not any(obstacle.colliderect(new_rect) for obstacle in obstacles):
        return new_x, new_y, True

    if abs(direction_x) > abs(direction_y):  # Moving mostly horizontally
        # Move Up, Down, and diagonals
        alternate_moves = [
            (0, step_size), (0, -step_size),  # Up, Down
            (step_size, step_size), (step_size, -step_size),  # Down-Right, Up-Right
            (-step_size, step_size), (-step_size, -step_size)  # Down-Left, Up-Left
        ]
    else:  # Moving mostly vertically
        # Move Left, Right, and diagonals
        alternate_moves = [
            (step_size, 0), (-step_size, 0),  # Right, Left
            (step_size, step_size), (step_size, -step_size),  # Down-Right, Up-Right
            (-step_size, step_size), (-step_size, -step_size)  # Down-Left, Up-Left
        ]

    # Attempt to move around obstacles
    for dx, dy in alternate_moves:
        test_x = new_x + dx
        test_y = new_y + dy
        test_rect = I.pg.Rect(test_x - zoom_rect.x, test_y - zoom_rect.y, current_mob['current_pos'].w, current_mob['current_pos'].h)
        if not any(obstacle.colliderect(test_rect) for obstacle in obstacles):
            # if abs(current_mob["previous_pos"].x - int(test_x)) > 1 and abs(current_mob["previous_pos"].y - int(test_y)) > 1:
            # print(f"No collisions in alternate direction ({dx}, {dy}), moving around")
            # print("x: ", current_mob["previous_pos"].x, int(test_x))
            # print("y: ", current_mob["previous_pos"].y, int(test_y))
            return test_x, test_y, True
            # else:
            #     target = (current_mob["previous_pos"].x ,target[1])
            #     return move_towards(target, current_mob, step_size, obstacles, zoom_rect, sub_screen)


    # If stuck, remain in place
    # print("stuck")
    return current_x, current_y, False


# def move_towards(touching_rect, data, mob_rect, target, step_size, obstacles):
#
#     current = (mob_rect.x, mob_rect.y)
#     # Calculate the direction vector from current to target
#     direction = (target[0] - current[0], target[1] - current[1])
#     # Calculate the distance to the target
#     distance = I.math.sqrt(direction[0] ** 2 + direction[1] ** 2)
#
#     if distance > 100:
#         return current
#
#     # If the distance is less than the step size, just move to the target
#     if distance < step_size:
#         return target
#
#     # Normalize the direction vector (make it a unit vector)
#     unit_vector = (direction[0] / distance, direction[1] / distance)
#     # Calculate the step vector
#     step_vector = (unit_vector[0] * step_size, unit_vector[1] * step_size)
#
#     # Update the current position
#     if touching_rect != 0:
#         # Touching something, needs to not go on the object
#         potential_positions = {
#             # (current[0] + step_vector[0], current[1] + step_vector[1]),  # Direct move
#             "Left":(current[0] - step_vector[0], current[1]),  # Move left
#             "Right": (current[0] + step_vector[0], current[1]),  # Move right
#             "Up": (current[0], current[1] - step_vector[1]),  # Move up
#             "Down": (current[0], current[1] + step_vector[1])  # Move down
#         }
#
#         # Check each potential position to see if it's valid (not colliding with any obstacle)
#         for pos in ["Left", "Right", "Up", "Down"]:
#             rect = I.pg.Rect(potential_positions[pos][0] - data["Zoom_rect"].x, potential_positions[pos][1] - data["Zoom_rect"].y, mob_rect.w, mob_rect.h)
#             if check_if_mob_collides(obstacles, rect) == 0:  # doesnt collide
#                 new_position = potential_positions[pos]
#                 break
#         else:
#             # If no valid position is found, stay in place
#             new_position = (current[0] + step_vector[0], current[1] + step_vector[1])
#     else:
#         # Not touching anything, proceed towards the target
#         new_position = (current[0] + step_vector[0], current[1] + step_vector[1])
#         rect = I.pg.Rect(new_position[0] - data["Zoom_rect"].x, new_position[1] - data["Zoom_rect"].y, mob_rect.w, mob_rect.h)
#         if check_if_mob_collides(obstacles, rect) != 0:  # collides
#             colliding_obstacles = [rect for rect in obstacles if rect.collidepoint((new_position[0] - data["Zoom_rect"].x, new_position[1] - data["Zoom_rect"].y))]
#             if colliding_obstacles:
#                 touching_rect = colliding_obstacles[0]
#                 return move_towards(touching_rect, data, mob_rect, target, step_size, obstacles)
#             else:
#                 new_position = current
#     return new_position


def draw_pixel(screen, left, top, color):
    for l in range(left, left + 10):
        for t in range(top, top + 10):
            screen.set_at((l, t), color)



def draw_character(screen, d, gender, race, options):
    # in options give a list of options to recreate
    d.update_for_gender_race(gender, race)
    options = d.get_character_options(options)
    # print(options)
    for option in options:
        for ranges, color in option.items():
            if color == (0, 0, 0, 0): # skips a color if it is 0, 0, 0, 0
                continue
            if d.orientation == "Right" and ranges[0] > 610 and color == d.hair_color or d.orientation == "Right" and ranges[0] > 610 and color == (0, 0, 0, 254):
                continue
            if d.orientation == "Left" and ranges[1] < 610 and color == d.hair_color or d.orientation == "Left" and ranges[1] < 620 and color == (0, 0, 0, 254):
                continue
            # print(color)
            for left in range(ranges[0], ranges[1], 10):
                for top in range(ranges[2], ranges[3], 10):
                    draw_pixel(screen, left, top, color)
    # I.T.pause_pygame()

def check_if_mob_collides(obstacles, mob):
    a = mob.collidelist(obstacles)
    if a == -1:
        return 0
    else:
        return a