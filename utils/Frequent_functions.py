from http.cookiejar import cut_port_re

from utils import Imports as I
from Values import Settings as S
from Render import Settings_render as sr
import json

image_cache = {}

def get_color_by_RGB(rgb):
    try:
        # Try to get the exact color name
        color_name = I.webcolors.rgb_to_name(rgb)
        if color_name[-1].isdigit():
            color_name = color_name[:-1]
            if color_name[-1].isdigit():
                color_name = color_name[:-1]
    except ValueError:
        # If the color name is not found, find the closest color
        color_name = -1
    return color_name


def add_image_to_screen(screen, path, pos):
    # a = I.T.start_mesure()
    if path not in image_cache:
        image = I.pg.image.load(path).convert_alpha()  # Only load once
        image_cache[path] = image
    else:
        image = image_cache[path]  # Retrieve cached image

    image = I.pg.transform.scale(image, (pos[2], pos[3]))  # Only scale once
    rect = image.get_rect()
    I.pg.Surface.blit(screen, image, (pos[0], pos[1]))
    rect = rect.move(pos[0], pos[1])
    # I.T.end_mesure(a)
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

def subtract_surfaces(base_surface, subtract_surface, position):
    # Create a copy of the base surface
    result_surface = base_surface.copy()

    # Create a temporary surface with the same size as the base surface
    temp_surface = I.pg.Surface(base_surface.get_size(), I.pg.SRCALPHA)

    # Blit the smaller subtract_surface onto the temp_surface at the correct position
    temp_surface.blit(subtract_surface, position)

    # Get the pixel arrays of both surfaces
    base_pixels = I.pg.surfarray.pixels3d(result_surface)
    subtract_pixels = I.pg.surfarray.pixels3d(temp_surface)

    # Get the alpha channels as well (for transparency handling)
    base_alpha = I.pg.surfarray.pixels_alpha(result_surface)
    subtract_alpha = I.pg.surfarray.pixels_alpha(temp_surface)

    # Subtract the color values, ensuring no negative values
    base_pixels[:, :, 0] = I.np.clip(base_pixels[:, :, 0] - subtract_pixels[:, :, 0], 0, 255)
    base_pixels[:, :, 1] = I.np.clip(base_pixels[:, :, 1] - subtract_pixels[:, :, 1], 0, 255)
    base_pixels[:, :, 2] = I.np.clip(base_pixels[:, :, 2] - subtract_pixels[:, :, 2], 0, 255)

    # Subtract the alpha values (optional)
    base_alpha[:, :] = I.np.clip(base_alpha[:, :] - subtract_alpha[:, :], 0, 255)

    # Unlock the pixel arrays
    del base_pixels
    del subtract_pixels
    del base_alpha
    del subtract_alpha

    return result_surface

def list_to_string(data_list):
    return json.dumps(data_list)

def string_to_list(data_string):
    return json.loads(data_string)

def create_light_mask(radius, color):
    # Create a surface to hold the light mask
    light_surface = I.pg.Surface((radius * 2, radius * 2), I.pg.SRCALPHA)

    # Create a numpy array for the light mask
    light_array = I.np.zeros((radius * 2, radius * 2, 4), dtype=I.np.uint8)  # 4 channels for RGBA

    # Calculate the center of the mask
    center_x, center_y = radius, radius

    # Create a grid of coordinates
    y, x = I.np.ogrid[-center_y:radius * 2 - center_y, -center_x:radius * 2 - center_x]

    # Calculate the squared distance from the center
    distance_squared = x ** 2 + y ** 2
    mask_area = distance_squared < radius ** 2  # boolean mask for pixels within the radius

    # Calculate the intensity based on distance, ensuring it decays smoothly
    distance = I.np.sqrt(distance_squared)
    intensity = I.np.clip(255 - (distance / radius) * 255, 0, 255)

    # Instead of assigning each channel individually, we set all RGBA channels in one operation
    light_array[mask_area] = I.np.array([color[0], color[1], color[2], 0])  # Set RGB channels
    light_array[mask_area, 3] = intensity[mask_area]  # Set Alpha channel separately

    # Set RGB channels
    pixels = I.pg.surfarray.pixels3d(light_surface)
    alpha = I.pg.surfarray.pixels_alpha(light_surface)

    # Assign values from light_array to pixels and alpha separately
    pixels[:, :, 0] = light_array[:, :, 0]  # Red
    pixels[:, :, 1] = light_array[:, :, 1]  # Green
    pixels[:, :, 2] = light_array[:, :, 2]  # Blue
    alpha[:, :] = light_array[:, :, 3]      # Alpha

    return light_surface

# def create_light_mask(radius, color):
#     # Create a surface to hold the light mask
#     light_surface = I.pg.Surface((radius * 2, radius * 2), I.pg.SRCALPHA)
#
#     # Create a numpy array for the light mask
#     light_array = I.np.zeros((radius * 2, radius * 2, 4), dtype=I.np.uint8)  # 4 channels for RGBA
#
#     # Calculate the center of the mask
#     center_x, center_y = radius, radius
#
#     # Create a grid of coordinates
#     y, x = I.np.ogrid[-center_y:radius * 2 - center_y, -center_x:radius * 2 - center_x]
#
#     # Calculate the squared distance from the center
#     distance_squared = x ** 2 + y ** 2
#     mask_area = distance_squared < radius ** 2  # boolean mask for pixels within the radius
#
#     # Calculate the intensity based on distance, ensuring it decays smoothly
#     distance = I.np.sqrt(distance_squared)
#     intensity = I.np.clip(255 - (distance / radius) * 255, 0, 255)
#
#     # Set the color with the calculated intensity for the RGBA channels
#
#     light_array[mask_area, 0] = color[0]  # Red
#     light_array[mask_area, 1] = color[1]  # Green
#     light_array[mask_area, 2] = color[2]  # Blue
#     light_array[mask_area, 3] = intensity[mask_area]  # Alpha
#
#     # Set RGB channels
#     pixels = I.pg.surfarray.pixels3d(light_surface)
#     alpha = I.pg.surfarray.pixels_alpha(light_surface)
#
#
#     # Assign values from light_array to pixels and alpha separately
#     pixels[:, :, 0] = light_array[:, :, 0]  # Red
#     pixels[:, :, 1] = light_array[:, :, 1]  # Green
#     pixels[:, :, 2] = light_array[:, :, 2]  # Blue
#     alpha[:, :] = light_array[:, :, 3]      # Alpha
#
#
#     return light_surface



def base_settings_load():
    print("base settings")


def display_text(screen ,text ,size, pos_tuple, color="black"):
    font = I.pg.font.SysFont('minecraft', int(size + S.RESOLUTION * 10))
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = pos_tuple
    screen.blit(text_surface, text_rect)
    return text_rect

def get_property(item, items, property):
    result = [I.info.BASE_ATTACKING_DAMAGE, 1, I.info.BASE_KNOCKBACK, "Blunt"]
    property_list = items.item_dict[item.split("|")[0]]["Properties"].split(",,,")
    for prop in property_list:
        if property in prop and property == "STACK":
            result = int(prop.split(":")[1])
        elif property in prop and property == "WEAPON" and "EFFECT" not in prop:
            result = prop.split(":")[1:]
        elif property in prop and property == "SMELT":
            property_str = prop.replace("SMELT(", "").replace(")", "")
            sub_property_list = property_str.split(",,")
            probabilities = []
            outcomes = []
            for property in sub_property_list:
                probabilities.append(float(property.split("-")[0]))
                outcomes.append(property.split("-")[1])
            return probabilities, outcomes
        elif property in prop and property == "ANVIL":
            # print(property_list, prop)
            property_str = prop.replace("ANVIL(", "")
            property_str = property_str.replace(")", "")
            result = property_str.split(",,")
        elif property in prop and property == "COLOR":
            color_str = prop.replace("COLOR:(", "").replace(")", "")
            color_list = color_str.split(", ")
            result = (int(color_list[0]), int(color_list[1]), int(color_list[2]), int(color_list[3]))
    return result
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
                    line_content = value.split(":")
                    txt_dictionary[line_content[0].strip()] = line_content[1].strip()
            return txt_dictionary
    except FileNotFoundError:
        return -1
    except Exception as e:
        return -1


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

def get_visible(target, current_mob, obstacles, zoom_rect):
    # Current position
    current_x, current_y = current_mob['current_pos'].topleft

    # Calculate direction vector and distance to the target
    direction_x, direction_y = target[0] - current_x, target[1] - current_y
    distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
    if distance > 100:
        return False
    else:
        return True


def move_away_new(target, rect, mob, speed, current_mob):
    new_x, new_y = target
    direction = I.pg.math.Vector2(new_x - rect.x, new_y - rect.y)
    distance = direction.length()  # Length of the vector (distance to target)

    if distance > 100:  # If already far enough away, stop moving
        return rect.x, rect.y, False

    if direction[0] > 0:
        current_mob["flip"] = "left"
    else:
        current_mob["flip"] = "right"
    # Normalize the direction vector (gives it a length of 1)
    if distance != 0:  # Avoid division by zero
        direction = direction.normalize()

    # Invert the direction vector to move away from the target
    direction *= -1

    # Scale the direction vector by a constant speed
    velocity = direction * speed

    # Update the sprite's position using the velocity
    if mob.frame_change:  # Adjusting condition for movement
        rect.x += velocity.x
        rect.y += velocity.y

    return rect.x, rect.y, True


def move_towards_new(target, rect, mob, speed, current_mob):
    new_x, new_y = target
    direction = I.pg.math.Vector2(new_x - rect.x, new_y - rect.y)
    distance = direction.length()  # Length of the vector (distance to target)
    if distance > 100:
        return rect.x, rect.y, False

    if direction[0] < 0:
        current_mob["flip"] = "left"
    else:
        current_mob["flip"] = "right"
    # Normalize the direction vector (gives it a length of 1)
    if distance != 0:  # Avoid division by zero
        direction = direction.normalize()



    # Scale the direction vector by a constant speed
    velocity = direction * speed

    # Update the sprite's position using the velocity
    if distance > speed and mob.frame_change:  # If we're farther than one step away, keep moving
        rect.x += velocity.x
        rect.y += velocity.y
    return rect.x, rect.y, True

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
        step_size = 2
    current_x, current_y = current_mob['current_pos'].topleft
    # Calculate direction vector and distance to the target
    direction_x, direction_y = target[0] - current_x, target[1] - current_y
    distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
    if distance > 100:
        return current_x, current_y, False
    # Check if we are close enough to the target
    if distance < step_size:
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
    # d.orientation = "Left"
    # d.walking = 2 #change walk possision
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
    conn = I.sqlite3.connect(S.local_path + "/static/data/A_Game.db")
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
    # root_dir = I.os.path.dirname(I.os.path.dirname(I.os.path.abspath(__file__)))  # Adjust if necessary
    db_path = I.os.path.join(S.local_path, "static", "data", "A_Game.db")

    conn = I.sqlite3.connect(db_path)
    # conn = I.sqlite3.connect("C:/Users/user/Desktop/A_Game-main/static/data/A_Game.db")
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

def remove_from_backpack(item, amount):
    if amount != 0:
        if I.info.BACKPACK_CONTENT.get(item) != None:
            if I.info.BACKPACK_CONTENT[item][0] - amount > 0:
                I.info.BACKPACK_CONTENT[item] = I.info.BACKPACK_CONTENT[item][0] - amount, I.info.BACKPACK_CONTENT[item][1], I.info.BACKPACK_CONTENT[item][2]
            else:
                del I.info.BACKPACK_CONTENT[item]
        elif I.info.BACKPACK_CONTENT.get(item + "|STACK0") != None:
            if I.info.BACKPACK_CONTENT[item + "|STACK0"][0] - amount > 0:
                I.info.BACKPACK_CONTENT[item + "|STACK0"] = I.info.BACKPACK_CONTENT[item + "|STACK0"][0] - amount, I.info.BACKPACK_CONTENT[item + "|STACK0"][1], I.info.BACKPACK_CONTENT[item + "|STACK0"][2]
            else:
                del I.info.BACKPACK_CONTENT[item + "|STACK0"]
    else:
        print("amount not a normal number")

def add_to_backpack(item, amount, items, row=0, collumn=0):
    if amount != 0:
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
            # print("all stacks were exactly full creating new stack")
            highest_stack_item_name = 0
            for item_name in I.info.BACKPACK_CONTENT.keys():
                if item in item_name:
                    if item + "|STACK" in item_name:
                        highest_stack_item_name = item_name
                        continue
            new_name = highest_stack_item_name.split("|STACK")[0] + "|STACK" + str(int(highest_stack_item_name.split("|STACK")[1]) + 1)
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
def find_item_by_slot(x, y):
    for key, value in I.info.BACKPACK_CONTENT.items():
        if value[1] == x and value[2] == y:
            # if the possision matches get the key
            return key
    return None

def find_open_space():
    taken_spaces = list(I.info.BACKPACK_CONTENT.values())
    for column in range(0, 26, 2):
        for row in range(0, 16, 2):
            if any((row, column) == (tpl[1], tpl[2]) for tpl in taken_spaces):
                continue
            return row, column

# def update_map_view(id: int, item_name: str, rect: tuple, case: str, current_room=0):
#     if current_room == 0:
#         """get the name of the current room"""
#         current_room = I.info.CURRENT_ROOM["name"]
#     if current_room not in I.info.MAP_CHANGE.keys():
#         """if the name of the map isnt here, create a dict for it"""
#         I.info.MAP_CHANGE[current_room] = {"add": {},
#                                            "remove": {},
#                                            "add_bypassed": {}}
#     if case == "add":
#         """adding a new decoration"""
#         if I.info.MAP_CHANGE[current_room]["add"].get(item_name) == None:
#             """if the item name was not yet added, add it"""
#             I.info.MAP_CHANGE[current_room]["add"][item_name] = []
#         if id >= 0:
#             """if the id is more than or equal to 0 add the id to the dict with rect"""
#             I.info.MAP_CHANGE[current_room]["add"][item_name].append((id, rect))
#         else:
#             print("Id too low")
#     elif case == "remove":
#         if item_name in list(I.info.MAP_CHANGE[current_room]["add"].keys()):
#             for ida, coordinates in I.info.MAP_CHANGE[current_room]["add"][item_name]:
#                 x = coordinates[0]
#                 y = coordinates[1]
#                 if ida == id:
#                     if isinstance(I.info.MAP_CHANGE[current_room]["add"][item_name][0][1], tuple) and len(I.info.MAP_CHANGE[current_room]["add"][item_name][0][1]) == 2:
#                         I.info.MAP_CHANGE[current_room]["add"][item_name].remove((id, (x, y)))
#                     else:
#                         I.info.MAP_CHANGE[current_room]["add"][item_name].remove((id, coordinates))
#
#                     if I.info.MAP_CHANGE[current_room]["remove"].get(item_name) == None:
#                         I.info.MAP_CHANGE[current_room]["remove"][item_name] = []
#                     I.info.MAP_CHANGE[current_room]["remove"][item_name].append(id)
#         else:
#             if I.info.MAP_CHANGE[current_room]["remove"].get(item_name) == None:
#                 I.info.MAP_CHANGE[current_room]["remove"][item_name] = []
#             I.info.MAP_CHANGE[current_room]["remove"][item_name].append(id)
#     elif case == "get":
#         if I.info.MAP_CHANGE[current_room]["add"].get(item_name) == None:
#             return 0
#         else:
#             return len(I.info.MAP_CHANGE[current_room]["add"][item_name])



def update_map_view(decor_id, decor_name, rect, case, current_room=0, decorations=0):
    if current_room == 0:
        current_room = I.info.CURRENT_ROOM["name"]
    if case not in ["get", "add_effect", "remove_gif", "remove_effect"]:
        rect = (rect[0], rect[1], rect[2], rect[3])
    if I.info.MAP_CHANGE.get(current_room) == None:
        I.info.MAP_CHANGE[current_room] = {"add": {},
                                           "remove": {},
                                           "remove_gif": {},
                                           "add_bypassed": {},
                                           "gif_ended": {},
                                           "add_effect": {},
                                           "remove_effect": {}
                                           }
    if case == "add":
        if I.info.MAP_CHANGE[current_room][case].get(decor_name) == None:
            I.info.MAP_CHANGE[current_room][case][decor_name] = {}
        I.info.MAP_CHANGE[current_room][case][decor_name][decor_id] = rect
        # if I.info.MAP_CHANGE[current_room]["remove"].get(decor_name) == None:
        #     """item was not previously removed by this function"""
        #     if I.info.MAP_CHANGE[current_room][case].get(decor_name) == None:
        #         I.info.MAP_CHANGE[current_room][case][decor_name] = {}
        #     I.info.MAP_CHANGE[current_room][case][decor_name][decor_id] = rect
        # else:
        #     """item may have been previously removed by this function"""
        #     if I.info.MAP_CHANGE[current_room]["remove"][decor_name].get(decor_id) == None:
        #         """item was not previously removed by this function"""
        #         if I.info.MAP_CHANGE[current_room][case].get(decor_name) == None:
        #             I.info.MAP_CHANGE[current_room][case][decor_name] = {}
        #         I.info.MAP_CHANGE[current_room][case][decor_name][decor_id] = rect
        #     else:
        #         """item was previously removed by this function"""
        #         del I.info.MAP_CHANGE[current_room]["remove"][decor_name][decor_id]
        #         """ after refreshing the map the item will appear"""
    elif case == "remove":
        if I.info.MAP_CHANGE[current_room][case].get(decor_name) == None:
            """decoration was not removed by this function before"""
            I.info.MAP_CHANGE[current_room][case][decor_name] = {}
        if I.info.MAP_CHANGE[current_room][case][decor_name].get(decor_id) == None:
            """decoration was not removed by this function"""
            I.info.MAP_CHANGE[current_room][case][decor_name][decor_id] = 0
        if rect == (0,0,0,0):
            rect = 0
        """removing from batch"""
        I.info.MAP_CHANGE[current_room][case][decor_name][decor_id] = rect

        # if I.info.MAP_CHANGE[current_room]["add"].get(decor_name) == None:
        #     """item was not previously created by this function"""
        #     if I.info.MAP_CHANGE[current_room][case].get(decor_name) == None:
        #         I.info.MAP_CHANGE[current_room][case][decor_name] = {}
        #     if rect == (0,0,0,0):
        #         rect = 0
        #     I.info.MAP_CHANGE[current_room][case][decor_name][decor_id] = rect
        #     """will remove the item from decor dict"""
        # else:
        #     """item may have been previously created by this function"""
        #     if I.info.MAP_CHANGE[current_room]["add"][decor_name].get(decor_id) == None:
        #         """the actual item was not previously created by this function"""
        #         if I.info.MAP_CHANGE[current_room][case].get(decor_name) != None:
        #             """so that errors don't occur when the plant has been actually removed from the list and tries again to remove it"""
        #             I.info.MAP_CHANGE[current_room][case][decor_name][decor_id] = rect
        #
        #     else:
        #         """the actual item was generated with this function"""
        #         print("was generated by this function before", decor_name, decor_id)
        #         if decorations != 0:
        #             print("was forecefully removed", decor_name, decor_id)
        #             del decorations.decor_dict[decor_name][decor_id]
        #         del I.info.MAP_CHANGE[current_room]["add"][decor_name][decor_id]
        #         """it's as if the item was never created in the first place"""
    if case == "remove_gif":
        gifs = rect # in the rect category gifs were placed instead
        if I.info.MAP_CHANGE[current_room].get("remove_gif") == None:
            I.info.MAP_CHANGE[current_room]["remove_gif"] = {}
        if I.info.MAP_CHANGE[current_room]["remove_gif"].get(decor_name) == None:
            I.info.MAP_CHANGE[current_room]["remove_gif"][decor_name] = {}
        # I.info.MAP_CHANGE["remove_gif"].append(gifs[decor_name].name)
        I.info.MAP_CHANGE[current_room]["remove_gif"][decor_name][decor_id] = gifs[decor_name].name
    elif case == "add_bypassed":
        if I.info.MAP_CHANGE[current_room]["add_bypassed"].get(decor_name) == None:
            I.info.MAP_CHANGE[current_room]["add_bypassed"][decor_name] = {}
            if decor_id >= 0:
                I.info.MAP_CHANGE[current_room]["add_bypassed"][decor_name][decor_id] = rect
            else:
                print("Id too low")
    elif case == "get":
        if I.info.MAP_CHANGE[current_room]["add"].get(decor_name) == None:
            return 0
        else:
            return len(I.info.MAP_CHANGE[current_room]["add"][decor_name])
    elif case == "gif_ended":
        if I.info.MAP_CHANGE[current_room][case].get(decor_name) == None:
            I.info.MAP_CHANGE[current_room][case][decor_name] = {}
        I.info.MAP_CHANGE[current_room][case][decor_name][decor_id] = rect
    elif case == "add_effect":
        effect = rect
            # I.th.start_thread(time, "planting", decorations)
        if I.info.MAP_CHANGE[current_room].get(case) == None:
            I.info.MAP_CHANGE[current_room][case] = {}
        if I.info.MAP_CHANGE[current_room][case].get(decor_name) == None:
            """decor doesnt have an effect in this list"""
            I.info.MAP_CHANGE[current_room][case][decor_name] = {}
        if I.info.MAP_CHANGE[current_room][case][decor_name].get(decor_id) == None:
            """decor trully doesnt have an effect in this list"""
            I.info.MAP_CHANGE[current_room][case][decor_name][decor_id] = 0
        I.info.MAP_CHANGE[current_room][case][decor_name][decor_id] = effect
    elif case == "remove_effect":
        effect = rect
        """Only removes effect from the add effect list"""
        # I.th.start_thread(time, "planting", decorations)
        if effect in I.info.MAP_CHANGE[current_room]["add_effect"][decor_name][decor_id]:
            if len(I.info.MAP_CHANGE[current_room]["add_effect"][decor_name][decor_id].split(",,")) == 1:
                I.info.MAP_CHANGE[current_room]["add_effect"][decor_name][decor_id] = I.info.MAP_CHANGE[current_room]["add_effect"][decor_name][decor_id].replace(effect, "")
                # print("removed", I.info.MAP_CHANGE[current_room]["add_effect"][decor_name][decor_id])
            else:
                # print("IN UPDATE MAP VIEW REMOVE EFFECT", I.info.MAP_CHANGE[current_room]["add_effect"][decor_name][decor_id])
                I.info.MAP_CHANGE[current_room]["add_effect"][decor_name][decor_id] = I.info.MAP_CHANGE[current_room]["add_effect"][decor_name][decor_id].replace(effect, "")


def get_decor_coordinates(option, id, decorations):
    if decorations.decor_dict.get(option) != None and decorations.decor_dict[option].get(id) != None:
        rect = decorations.decor_dict[option][id]["rect"]
        return rect
    else:
        I.t.sleep(0.5)
        # print("error decor coordinates")

def dict_to_string(data):
    import json
    """Convert dictionary with complex keys and values into a string."""
    def convert_keys(d):
        """Recursively convert all tuple keys into JSON-friendly format (strings)."""
        if isinstance(d, dict):
            new_dict = {}
            for key, value in d.items():
                # Serialize the tuple key as a string
                new_key = json.dumps(key) if isinstance(key, tuple) else key
                new_dict[new_key] = convert_keys(value)
            return new_dict
        elif isinstance(d, list):
            return [convert_keys(item) for item in d]
        else:
            return d

    # Convert the dictionary with complex keys into a JSON-friendly format
    data_json_friendly = convert_keys(data)

    # Convert to JSON string
    return json.dumps(data_json_friendly)


def string_to_dict(data_str):
    import json
    """Convert string back into the original dictionary."""
    def restore_keys(d):
        """Recursively convert all string keys that represent tuples back to tuples."""
        if isinstance(d, dict):
            new_dict = {}
            for key, value in d.items():
                # Deserialize the string key back to a tuple if possible
                try:
                    new_key = tuple(json.loads(key)) if isinstance(key, str) else key
                except (json.JSONDecodeError, TypeError):
                    new_key = key  # In case it's not a tuple
                new_dict[new_key] = restore_keys(value)
            return new_dict
        elif isinstance(d, list):
            return [restore_keys(item) for item in d]
        else:
            return d

    # Convert JSON string back to dictionary
    data_dict = json.loads(data_str)

    # Restore tuple keys from strings
    return restore_keys(data_dict)


def rect_polygon_collision(rect, polygon):
    rect_points = [
        I.pg.Vector2(rect.left, rect.top),
        I.pg.Vector2(rect.right, rect.top),
        I.pg.Vector2(rect.right, rect.bottom),
        I.pg.Vector2(rect.left, rect.bottom)
    ]

    # Check if any of the rectangle's corners are inside the polygon
    for point in rect_points:
        if point_in_polygon(point, polygon):
            return True

    return False

def point_in_polygon(point, polygon):
    x, y = point.x, point.y
    n = len(polygon)
    inside = False
    px, py = polygon[0]
    for i in range(n + 1):
        sx, sy = polygon[i % n]
        if y > min(py, sy):
            if y <= max(py, sy):
                if x <= max(px, sx):
                    if py != sy:
                        xinters = (y - py) * (sx - px) / (sy - py) + px
                    if px == sx or x <= xinters:
                        inside = not inside
        px, py = sx, sy
    return inside

def get_decor_by_id(index, decorations, rooms):
    decor_list = []
    for option in rooms.decor:
        for id in decorations.decor_dict[option].keys():
            if isinstance(id, int):
                decor_list.append(decorations.decor_dict[option][id])
    if index < len(decor_list):
        return decor_list[index]

def weighted_random():
    if I.random.random() < 0.6:  # 30% probability
        return I.random.randint(-40, 40)
    else:  # 70% probability
        return 0