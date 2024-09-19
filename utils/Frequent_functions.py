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

def add_image_to_screen_dif_rect(screen, path, pos, wh):
    image = I.pg.image.load(path).convert_alpha()
    image = I.pg.transform.scale(image, (pos[2], pos[3]))
    rect = image.get_rect()
    I.pg.Surface.blit(screen, image, (pos[0], pos[1]))
    # rect = rect.move(pos[0], pos[1])
    rect = I.pg.Rect(pos[0], pos[1], wh[0], wh[1])
    return rect

def resize_rect(rect, width, height):
    rect = I.pg.Rect(rect.left, rect.top, width, height)
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

def get_property(item, items, property):
    stack = I.info.BASE_ATTACKING_DAMAGE, 1, I.info.BASE_KNOCKBACK, "Blunt"
    property_list = items.item_dict[item.split("|")[0]]["Properties"].split(",,,")
    for prop in property_list:
        if property in prop and property == "STACK":
            stack = int(prop.split(":")[1])
        elif property in prop and property == "WEAPON":
            stack = prop.split(":")[1:]
        elif property in prop and property == "SMELT":
            property_str = prop.replace("SMELT(", "").replace(")", "")
            sub_property_list = property_str.split(",,")
            probabilities = []
            outcomes = []
            for property in sub_property_list:
                probabilities.append(float(property.split("-")[0]))
                outcomes.append(property.split("-")[1])
            return probabilities, outcomes
    return stack
def button_click_render(screen, button, data, name):
    if data == 1:
        # Pressed down
        button = add_image_to_screen(screen, 'static/images/' + name + "_Clicked.png", [button.left, button.top, button.width, button.height])
    elif data == 0:
        button = add_image_to_screen(screen, 'static/images/' + name + ".png", [button.left, button.top, button.width, button.height])
    elif name == "Slider_button":
        text = display_text(screen, "A RESTART IS REQUIRED FOR THE CHANGES TO TAKE EFFECT (CANCEL IF UNWANTED)", 10, (sr.CB_LEFT, sr.CB_TOP * 2.8), "black")
        I.pg.display.update(text)
        interval = (sr.SLIDER_MAX - sr.SLIDER_MIN) / 10
        data = data - button.width / 2
        data = round(data / interval) * interval
        if data > sr.SLIDER_MAX:
            data = sr.SLIDER_MAX
        elif data < sr.SLIDER_MIN:
            data = sr.SLIDER_MIN

        add_image_to_screen(screen, 'static/images/Frame_main_menu.png', [sr.S_LEFT, sr.S_TOP, sr.S_F_WIDTH, sr.S_F_HEIGHT])
        slider = add_image_to_screen(screen, 'static/images/Slider.png', [S.SCREEN_WIDTH / 2, sr.SLIDER_TOP, sr.SLIDER_WIDTH, sr.SLIDER_HEIGHT])
        I.pg.display.update(slider)
        button = add_image_to_screen(screen, 'static/images/' + name + "_Clicked.png", [data, button.top, button.width, button.height])
    elif name == "Slider_button_Volume":
        # text = display_text(screen, str(S.VOLUME), 10,(sr.CB_LEFT, sr.CB_TOP * 2.8), "black")
        # I.pg.display.update(text)
        interval = (sr.SLIDER_MAX - sr.SLIDER_MIN) / 10
        data = data - button.width / 2
        data = round(data / interval) * interval
        if data > sr.SLIDER_MAX:
            data = sr.SLIDER_MAX
        elif data < sr.SLIDER_MIN:
            data = sr.SLIDER_MIN
        button_name = name.split("_")
        button_name = button_name[0] + "_" + button_name[1]
        add_image_to_screen(screen, 'static/images/Frame_main_menu.png',[sr.S_LEFT, sr.S_TOP, sr.S_F_WIDTH, sr.S_F_HEIGHT])
        slider = add_image_to_screen(screen, 'static/images/Slider.png', [S.SCREEN_WIDTH / 2, sr.SLIDER_TOP * 2, sr.SLIDER_WIDTH, sr.SLIDER_HEIGHT])
        I.pg.display.update(slider)
        button = add_image_to_screen(screen, 'static/images/' + button_name + "_Clicked.png",[data, button.top, button.width, button.height])
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


def str_to_tuple(input_str):
    try:
        # Use eval to convert the string representation into a tuple
        result = eval(input_str)

        # Ensure that the result is a tuple
        if isinstance(result, tuple):
            return result
        else:
            raise ValueError("The provided string does not represent a tuple.")
    except (SyntaxError, ValueError):
        raise ValueError("Invalid input string for tuple conversion.")
# def Gif_maker(image_folder, duration, name):
#     print("use the movement parts to create four gifs for moving up down left right also do this in save character to properly save the character moving")
#     # Get all the image files in the folder
#     orientation_keys = S.GIF_DICT.keys()
#     image_files = [I.os.path.join(image_folder, file) for file in I.os.listdir(image_folder) if file.endswith(('png', 'jpg', 'jpeg'))]
#     print(image_files)
#
#     # Sort the image files by name to ensure correct order
#     for key in orientation_keys:
#         new_image_files = []
#         path_endings = S.GIF_DICT[key].split(", ")
#         for path_end in path_endings:
#             new_image_files.append('static/data/created_characters/' + name + "/" + name + path_end + ".png")
#         images = [I.img.open(image) for image in new_image_files]
#         I.os.makedirs('static/data/created_characters/' + name + "/gif", exist_ok=True)
#         images[0].save('static/data/created_characters/' + name + "/gif/" + name + key + ".gif", save_all=True, append_images=images[1:], duration=duration,loop=0, disposal=2)
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


def move_towards(target, current_mob, step_size, obstacles, zoom_rect):
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
    if step_size > 1:
        step_size = 1
    else:
        step_size = 0
    current_x, current_y = current_mob['current_pos'].topleft

    # Calculate direction vector and distance to the target
    direction_x, direction_y = target[0] - current_x, target[1] - current_y
    distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
    if distance > 100:
        return current_x, current_y, False
    # Check if we are close enough to the target
    if distance < step_size:
        print('reached')
        return target[0], target[1], True

    # Normalize direction vector
    if distance > 0:
        direction_x /= distance
        direction_y /= distance

    # Calculate new position
    new_x = (current_x + direction_x * step_size)
    new_y = (current_y + direction_y * step_size)
    # Create new Rect for the potential new position
    new_rect = I.pg.Rect(new_x - zoom_rect.x, new_y - zoom_rect.y, current_mob['current_pos'].w, current_mob['current_pos'].h)

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
            return test_x, test_y, True
    return current_x, current_y, False

def move_away_from(target, current_mob, step_size, obstacles, zoom_rect):
    """
    Move the mob away from the target position while avoiding obstacles.

    Args:
        target (tuple): Target position (x, y).
        mob_rect (Rect): The Rect object for the mob.
        step_size (float): The step size for each movement.
        obstacles (list): List of Rect objects representing obstacles.
        zoom_rect (Rect): The Rect object for the zoomed area of the screen.

    Returns:
        tuple: New (x, y) position for the mob.
    """
    if step_size > 1:
        step_size = 1
    else:
        step_size = 0
    # Current position
    current_x, current_y = current_mob['current_pos'].topleft

    # Calculate direction vector and distance to the target
    direction_x, direction_y = current_x - target[0], current_y - target[1]
    distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

    if distance > 100:
        return current_x, current_y, False

    # Normalize direction vector
    if distance > 0:
        direction_x /= distance
        direction_y /= distance

    # Calculate new position
    new_x = current_x + direction_x * step_size
    new_y = current_y + direction_y * step_size

    # Create new Rect for the potential new position
    new_rect = I.pg.Rect(new_x - zoom_rect.x, new_y - zoom_rect.y, current_mob['current_pos'].w, current_mob['current_pos'].h)

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
            return test_x, test_y, True
    return current_x, current_y, False



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


def read_one_column_from_db(table, name):
    """
    Read data from a specific column in the specified table in the database.

    Args:
        table (str): The table name.
        column (str): The name of the column to retrieve.
        conditions (str): SQL conditions for filtering the results. Default is None (no conditions).

    Returns:
        list: A list of values from the specified column.
    """
    conn = I.sqlite3.connect("./static/data/A_Game.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM {table} WHERE Name = ?"
    cursor.execute(query, (name,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    if rows != []:
        return rows[0]
    # Flatten the list of tuples into a simple list
    return rows

def read_data_from_db(table, columns='*', conditions=None):
    """
    Read data from the specified table in the database.

    Args:
        table (str): The table name.
        columns (str or list): Columns to retrieve. Default is '*' (all columns).
        conditions (str): SQL conditions for filtering the results. Default is None (no conditions).

    Returns:
        list: A list of tuples containing the rows retrieved from the database.
    """
    conn = I.sqlite3.connect("./static/data/A_Game.db")
    cursor = conn.cursor()

    if isinstance(columns, list):
        columns = ', '.join(columns)

    query = f"SELECT {columns} FROM {table}"
    if conditions:
        query += f" WHERE {conditions}"

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

def display_text_player(text, time):
    if "Meat" in text:
        lines = text.split("Meat")
        text = lines[0] + "Meat" + lines[1][1:]
    if "_" in text:
        lines = text.split("_")
        text = lines[0] + " " + lines[1]
    if I.info.TEXT == []:
        I.info.TEXT.append(text + ",," + str(time))
    else:
        last_text = I.info.TEXT[-1]
        I.info.TEXT.append(text + ",," + str(time + int(last_text.split(",,")[1])))

    if len(I.info.TEXT) > 10:
        I.info.TEXT = I.info.TEXT[:-1]



def is_point_on_line(x1, y1, x2, y2, px, py):
    # Check if the point is collinear
    if (py - y1) * (x2 - x1) != (y2 - y1) * (px - x1):
        return False

    # Check if the point is within the bounds of the line segment
    if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2):
        return True

    return False


def rect_intersects_line(rect, x1, y1, x2, y2):
    # Define the corners of the rectangle
    rect_corners = [
        (rect.left, rect.top),  # Top-left
        (rect.right, rect.top),  # Top-right
        (rect.right, rect.bottom),  # Bottom-right
        (rect.left, rect.bottom)  # Bottom-left
    ]

    # Check each edge of the rectangle
    for i in range(4):
        p1 = rect_corners[i]
        p2 = rect_corners[(i + 1) % 4]  # Next corner (with wrapping)
        if do_intersect(p1, p2, (x1, y1), (x2, y2)):
            return True

    return False


def orientation(p, q, r):
    # Calculate the orientation of the triplet (p, q, r)
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear
    elif val > 0:
        return 1  # Clockwise
    else:
        return 2  # Counterclockwise


def do_intersect(p1, q1, p2, q2):
    # Find the four orientations needed for general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special cases
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True

    return False

def on_segment(p, q, r):
    # Check if point q lies on line segment pr
    if min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):
        return True
    return False



def move_closer(point, target, step_size, decorations, sub_image, data, recursion):

    def get_new_target(start_point, end_point, direction, distance, decorations):
        x_A, y_A = start_point
        x_C, y_C = end_point  # (Example; point C is not used directly in this case)
        d_AB = distance

        # Define the direction vector (from A to B)
        direction_vector = direction

        # Calculate the length of the direction vector
        length_v = I.math.sqrt(direction_vector[0] ** 2 + direction_vector[1] ** 2)

        # Normalize the direction vector
        normalized_direction = (direction_vector[0] / length_v, direction_vector[1] / length_v)

        # Calculate point B
        x_B = x_A + d_AB * normalized_direction[0]
        y_B = y_A + d_AB * normalized_direction[1]

        return (x_B, y_B)
    def is_valid_move(new_rect, decorations):
        """Check if the new_rect collides with any decorations."""
        for decoration in decorations:
            if new_rect.colliderect(decoration):
                return False
        return True

    diff_x = target[0] - point[0]
    diff_y = target[1] - point[1]
    distance = I.pg.math.Vector2(diff_x, diff_y).length()

    if distance <= step_size:
        return target

    direction = I.pg.math.Vector2(diff_x, diff_y).normalize()
    new_point = (point[0] + direction.x * step_size, point[1] + direction.y * step_size)

    # Ensure the movement is at least 1 pixel in any direction
    if abs(new_point[0] - point[0]) < 1 and new_point[0] != point[0]:
        new_point = (round(new_point[0]), new_point[1])
    if abs(new_point[1] - point[1]) < 1 and new_point[1] != point[1]:
        new_point = (new_point[0], round(new_point[1]))

    new_rect_left = I.pg.Rect(new_point[0] - data["Zoom_rect"].x + 3, new_point[1] - data["Zoom_rect"].y + 7 ,2, 5)
    new_rect_right = I.pg.Rect(new_point[0] - data["Zoom_rect"].x + 13, new_point[1] - data["Zoom_rect"].y + 7 ,2, 5)
    new_rect_top = I.pg.Rect(new_point[0] - data["Zoom_rect"].x + 8, new_point[1] - data["Zoom_rect"].y + 2 ,5, 2)
    new_rect_bot = I.pg.Rect(new_point[0] - data["Zoom_rect"].x + 8, new_point[1] - data["Zoom_rect"].y + 15 ,5, 2)
    # I.T.Make_rect_visible(sub_image, new_rect_left, "red")
    # I.T.Make_rect_visible(sub_image, new_rect_right, "orange")
    # I.T.Make_rect_visible(sub_image, new_rect_top, "black")
    # I.T.Make_rect_visible(sub_image, new_rect_bot, "blue")
    if not is_valid_move(new_rect_left, decorations):
        # print("left collision move right")
        new_point = new_point[0] + 1  * recursion, new_point[1]

    if not is_valid_move(new_rect_right, decorations):
        # print("right collision move left")
        new_point = new_point[0] - 1  * recursion, new_point[1]

    if not is_valid_move(new_rect_top, decorations):
        # print("top collision move bottom")
        new_point = new_point[0], new_point[1] + 1 * recursion

    if not is_valid_move(new_rect_bot, decorations):
        # print("bottom collision move top")
        new_point = new_point[0], new_point[1] - 1 * recursion
        # return slide_around_obstacle(point, direction, step_size, decorations)
    if new_point == point and recursion == 2:
        target = get_new_target(new_point, target, direction, distance, decorations)
        new_point = move_closer(new_point, target, step_size, decorations, sub_image, data, 2)
        I.info.FOLLOWER["current_pos"] = new_point
    # else:
        # pzrint("final pos:", new_point, "original_pos: ", point)

    return (int(new_point[0]), int(new_point[1]))



def get_most_often_tuple(input_tuple_list: list[tuple]):
    count = {}
    for tuple in input_tuple_list:
        if count.get(tuple) == None:
            count[tuple] = 0
        count[tuple] += 1

    max = 0
    most_often_tuple = (0, 0)
    for tuple, value in count.items():
        if value >= max:
            max = value
            most_often_tuple = tuple

    return most_often_tuple

def count_png_files(folder_path):
    png_files = [file for file in I.os.listdir(folder_path) if file.endswith('.png')]
    return len(png_files)


def add_to_backpack(item, amount, items, row=0, collumn=0):
    if amount != 0:
        # print(amount)
        in_backpack = 0
        stack = get_property(item, items, "STACK")
        for item_name in I.info.BACKPACK_CONTENT.keys():
            if item + "|STACK" in item_name:
                in_backpack = 1
                if I.info.BACKPACK_CONTENT[item_name][0] < stack:  # IF THE STACK HAS EMPTY SPACES CONTINUE
                    in_backpack = 2
                    if amount + I.info.BACKPACK_CONTENT[item_name][0] <= stack:  # IF THE AMOUNT OF NEW ITEMS PLUS THE ALREADY EXISTING ITEMS DOESNT OVERFLOW THE STACK
                        # print("stack wasnt overflowed")
                        I.info.BACKPACK_CONTENT[item_name] = I.info.BACKPACK_CONTENT[item_name][0] + amount, I.info.BACKPACK_CONTENT[item_name][1], I.info.BACKPACK_CONTENT[item_name][2]
                        break
                    else:  # IF THE AMOUNT OF NEW ITEMS PLUS THE ALREADY EXISTING ITEMS OVERFLOWS THE STACK CREATE A NEW ONE
                        while True:
                            new_addon = "|STACK" + str(int(item_name.split("|STACK")[1]) + 1)
                            new_name = item_name.split("|")[0] + new_addon
                            if I.info.BACKPACK_CONTENT.get(new_name) == None and int(amount + I.info.BACKPACK_CONTENT[item_name][0] - stack) != 0:
                                break
                            else:
                                item_name = new_name
                        if row == 0 and collumn == 0:
                            row, collumn = find_open_space()
                        if int(amount + I.info.BACKPACK_CONTENT[item_name][0] - stack) != 0:
                            I.info.BACKPACK_CONTENT[new_name] = int(amount + I.info.BACKPACK_CONTENT[item_name][0] - stack), row, collumn  # FIRST CREATED NEW STACK CUZ THE OLD STACK VALUE WAS USED
                            # print("stack overflowed creating new stack: ", I.info.BACKPACK_CONTENT[new_name])
                        I.info.BACKPACK_CONTENT[item_name] = int(stack), I.info.BACKPACK_CONTENT[item_name][1], I.info.BACKPACK_CONTENT[item_name][2]  # THEN UPDATED OLD STACK
                        break
                # else:
                    # print("this stack is full")

        if in_backpack == 1:
            # print("all stacks were full creating new stack")
            for item_name in I.info.BACKPACK_CONTENT.keys():
                if item + "|STACK" in item_name:
                    continue
            new_name = item_name.split("|STACK")[0] + "|STACK" + str(int(item_name.split("|STACK")[1]) + 1)
            if row == 0 and collumn == 0:
                row, collumn = find_open_space()
            I.info.BACKPACK_CONTENT[new_name] = int(amount), row, collumn  # FIRST CREATED NEW STACK CUZ THE OLD STACK VALUE WAS USED

        if in_backpack == 0:
            # print("didn't find empty stacks \n")
            if row == 0 and collumn == 0:
                row, collumn = find_open_space()


            if I.info.BACKPACK_CONTENT.get(item) == None:                 # if the item doesnt exist in backpack
                I.info.BACKPACK_CONTENT[item] = (float(amount), row, collumn)
                # DOESNT DO STACKS
            else:                                                         # if the item already exists in backpack and there were no previous |STACK
                # DOESNT REMOVE THE ITEM WITHOUT |STACK ON IT, ADDS TOO MANY ITEMS
                stack = get_property(item, items, "STACK")
                value = I.info.BACKPACK_CONTENT[item]
                if value[0] + float(amount) > stack:
                    del I.info.BACKPACK_CONTENT[item]
                    repetitions = I.math.floor((float(value[0]) + float(amount)) / float(stack)) + 1  # adding one so loop works with one stack (if stack is 10 and amount is 14, then for loop needs to happen twice, this function returns one less)
                    addon = "|STACK"
                    for i in range(0, repetitions):
                        if i == repetitions-1:
                            stack = float(value[0]) + float(amount) - float(stack) * i
                        if row == 0 and collumn == 0:
                            row, collumn = find_open_space()
                        if int(stack) != 0:
                            I.info.BACKPACK_CONTENT[item + addon + str(i)] = (int(stack), int(row), int(collumn))
                else:
                    I.info.BACKPACK_CONTENT[item] = (float(value[0] + float(amount)), value[1], value[2])

    # print("input: ", I.info.BACKPACK_CONTENT)

    # merge_stacks(items)

def find_open_space():
    taken_spaces = list(I.info.BACKPACK_CONTENT.values())
    for column in range(0, 26, 2):
        for row in range(0, 16, 2):
            if any((row, column) == (tpl[1], tpl[2]) for tpl in taken_spaces):
                continue
            return row, column

def update_map_view(id: int, item_name: str, coordinates: tuple, case: str):
    current_room = I.info.CURRENT_ROOM["name"]
    if current_room not in I.info.MAP_CHANGE.keys():
        I.info.MAP_CHANGE[current_room] = {"add": {},
                                           "remove": {}}
    if case == "add":
        if I.info.MAP_CHANGE[current_room]["add"].get(item_name) == None:
            I.info.MAP_CHANGE[current_room]["add"][item_name] = []
        if id >= 0:
            I.info.MAP_CHANGE[current_room]["add"][item_name].append((id, coordinates))
        else:
            print("Id too low")
    elif case == "remove":
        if item_name in list(I.info.MAP_CHANGE[current_room]["add"].keys()):
            for ida, (x, y) in I.info.MAP_CHANGE[current_room]["add"][item_name]:
                if ida == id:
                    I.info.MAP_CHANGE[current_room]["add"][item_name].remove((id, (x, y)))
                    if I.info.MAP_CHANGE[current_room]["remove"].get(item_name) == None:
                        I.info.MAP_CHANGE[current_room]["remove"][item_name] = []
                    I.info.MAP_CHANGE[current_room]["remove"][item_name].append(id)
        else:
            if I.info.MAP_CHANGE[current_room]["remove"].get(item_name) == None:
                I.info.MAP_CHANGE[current_room]["remove"][item_name] = []
            I.info.MAP_CHANGE[current_room]["remove"][item_name].append(id)
    elif case == "get":
        if I.info.MAP_CHANGE[current_room]["add"].get(item_name) == None:
            return 0
        else:
            return len(I.info.MAP_CHANGE[current_room]["add"][item_name])

def get_decor_coordinates(option, id, decorations):
    rect = decorations.decor_dict[option][id]["rect"]
    return rect.x, rect.y
