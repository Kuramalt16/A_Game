from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S

AVERAGE_TIME = (0, 0)

def testing_events(event):
    if event.type == I.pg.ACTIVEEVENT:
        pass
    elif event.type == I.pg.WINDOWLEAVE:
        pass
    elif event.type == I.pg.WINDOWMOVED:
        pass
    elif event.type == I.pg.VIDEOEXPOSE:
        pass
    elif event.type == I.pg.WINDOWEXPOSED:
        pass
    elif event.type == I.pg.WINDOWENTER:
        pass
    elif event.type == I.pg.MOUSEMOTION:
        pass
    elif event.type == I.pg.AUDIODEVICEADDED:
        pass
    elif event.type == I.pg.WINDOWSHOWN:
        pass
    elif event.type == I.pg.WINDOWFOCUSGAINED:
        pass
    elif event.type == I.pg.TEXTEDITING:
        pass
    elif event.type == I.pg.WINDOWMINIMIZED:
        pass
    elif event.type == I.pg.WINDOWFOCUSLOST:
        pass
    elif event.type == I.pg.WINDOWRESTORED:
        pass
    elif event.type == I.pg.CLIPBOARDUPDATE:
        pass
    elif event.type == I.pg.WINDOWCLOSE:
        pass
    elif event.type == I.pg.MOUSEBUTTONDOWN:
        pass
    elif event.type == I.pg.MOUSEBUTTONUP:
        pass
    elif event.type == I.pg.MOUSEWHEEL:
        pass
    elif event.type == I.pg.KEYDOWN:

        if event.key == 27:
            Ff.debug_print("Esc_key")
        elif event.key == 13:
            Ff.debug_print("Enter_key")
        elif event.key == I.pg.K_F1:
            Ff.debug_print("F1")
        elif event.key == I.pg.K_F2:
            Ff.debug_print("F2")
        elif event.key == I.pg.K_F3:
            Ff.debug_print("F3")
        elif event.key == I.pg.K_F4:
            Ff.debug_print("F4")
        elif event.key == I.pg.K_F5:
            Ff.debug_print("F5")
        elif event.key == I.pg.K_F6:
            Ff.debug_print("F6")
        elif event.key == I.pg.K_F7:
            Ff.debug_print("F7")
        elif event.key == I.pg.K_F8:
            Ff.debug_print("F8")
        elif event.key == I.pg.K_F9:
            Ff.debug_print("F9")
        elif event.key == I.pg.K_F10:
            Ff.debug_print("F10")
        elif event.key == I.pg.K_F11:
            Ff.debug_print("F11")
        elif event.key == I.pg.K_F12:
            Ff.debug_print("F12")
        elif event.key == I.pg.K_DELETE:
            Ff.debug_print("DELETE")
        elif event.key == I.pg.K_BACKSPACE:
            Ff.debug_print("Backspace")
        elif event.key == I.pg.K_LSHIFT:
            Ff.debug_print("K_LSHIFT")
        elif event.key == I.pg.K_LCTRL:
            Ff.debug_print("K_LCTRL")
        elif event.key == I.pg.K_LALT:
            Ff.debug_print("K_LALT")
        elif event.key == I.pg.K_RIGHT:
            Ff.debug_print("K_RIGHT")
        elif event.key == I.pg.K_LEFT:
            Ff.debug_print("K_LEFT")
        elif event.key == I.pg.K_UP:
            Ff.debug_print("K_UP")
        elif event.key == I.pg.K_DOWN:
            Ff.debug_print("K_DOWN")
            # else:
            # Ff.debug_print(event.key)
    elif event.type == I.pg.KEYUP:
        # Ff.debug_print("KEYUP")  # pritns when a key is pressed up
        pass
    elif event.type == I.pg.TEXTINPUT:
        Ff.debug_print(event.text)  # prints what key was pressed
        # Ff.debug_print("TEXTINPUT")
        # elif event.type == pygame.WINDOWFOCUSGAINED:
        #     Ff.debug_print("WINDOWFOCUSGAINED")
        # elif event.type == pygame.WINDOWFOCUSGAINED:
        #     Ff.debug_print("WINDOWFOCUSGAINED")
        # elif event.type == pygame.WINDOWFOCUSGAINED:
        #     Ff.debug_print("WINDOWFOCUSGAINED")
        # elif event.type == pygame.WINDOWFOCUSGAINED:
        #     Ff.debug_print("WINDOWFOCUSGAINED")
    else:
        Ff.debug_print(event.type)

def Put_a_stone(screen):
    image = I.pg.image.load("static/images/Stone_mid.png")  # Replace with your image file path
    image = I.pg.transform.scale(image, (50, 50))
    screen.blit(image, (0, 0))
    I.pg.display.flip()  # send display data

def Make_rect_visible(screen, rect, color):
    I.pg.draw.rect(screen, color, rect)

def print_coordinates(event, coordinates):
    if event.key == I.pg.K_c:
        if I.info.CURRENT_ROOM["Type"] == "Village":
            Ff.debug_print(f"{int(coordinates.x + 145 + I.info.OFFSCREEN[0] / 4)},{int(coordinates.y + 72 + I.info.OFFSCREEN[1] / 4)},1,1,1,1,,")
        else:
            Ff.debug_print(f"{int(I.info.OFFSCREEN[0] + 528) },{int(I.info.OFFSCREEN[1] + 337)},3,3,3,3,,")

def get_time_diferance(time1, time2):
    Ff.debug_print(time1-time2)

def pause_pygame():
    I.pg.display.flip()
    running = True
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.QUIT:
                running = False
            if event.type == I.pg.KEYDOWN:
                running = False

def start_mesure():
    return I.t.perf_counter()

def end_mesure(start_time):
    end_time = I.t.perf_counter()
    execution_time = end_time - start_time - 0.0000017
    I.T.AVERAGE_TIME = (I.T.AVERAGE_TIME[0] + execution_time, I.T.AVERAGE_TIME[1] + 1)
    Ff.debug_print("overall time in ms: ", execution_time * 1000, "AVERAGE: ", (I.T.AVERAGE_TIME[0] / I.T.AVERAGE_TIME[1]) * 1000, " ms")
    return (I.T.AVERAGE_TIME[0] / I.T.AVERAGE_TIME[1]) * 1000

def end_mesure_no_print(start_time):
    end_time = I.t.perf_counter()
    execution_time = end_time - start_time - 0.0000017
    I.T.AVERAGE_TIME = (I.T.AVERAGE_TIME[0] + execution_time, I.T.AVERAGE_TIME[1] + 1)
    return (I.T.AVERAGE_TIME[0] / I.T.AVERAGE_TIME[1]) * 1000
    # if execution_time * 1000 > 30:
    #     pause_pygame()



# def get_body_coordinates(screen):
#     S_LEFT = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 5)
#     S_TOP = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / 2.2)
#     S_F_WIDTH = S.SCREEN_WIDTH - (2 * S_LEFT)
#     S_F_HEIGHT = S.SCREEN_HEIGHT / 10 * 8
#     body_sizes = [int(S_LEFT) + int(S_F_WIDTH / 4), int(S_TOP) + int(S_F_HEIGHT / 6), int(S_F_WIDTH / 2), int(S_F_HEIGHT / 2)]
#     Ff.add_image_to_screen(screen, "static/images/Race/Human/Girl/Human_Girl.png", body_sizes)
#     # Ff.debug_print(body_sizes)
#     # screen.fill("white")
#     # I.pg.display.flip()
#     color_coordinates = {}
#     # options = {0: ["Front", "Front1", "Front", "Front2", "Front", "Front1", "Front", "Front2"],
#                # 1: ["Back", "Back1", "Back", "Back2", "Back", "Back1", "Back", "Back2"],
#                # 2: ["Left"]}
#     options = {0: ["Right", "Right1","Right","Right2"]}
#     for a in range(0, len(options)):
#         for i in options[a]:
#             # Ff.debug_print(options[a])
#             draw_character(screen, "boy", "Elf", i, options[a][0])


# def draw_character(screen, gender, race, walk, orientation):
#     from static.data.Character_byte_data import CharacterData
#     d = CharacterData()
#     d.update_orientation(orientation)
#     d.update_walk(walk)
#     d.update_for_gender_race(gender, race)
#     options = d.get_character_options()
#     screen.fill("White")
#     for option in options:
#         for ranges, color in option.items():
#             for left in range(ranges[0], ranges[1], 10):
#                 for top in range(ranges[2], ranges[3], 10):
#                     draw_pixel(screen, left, top, color)
#     I.pg.display.flip()
#     I.pg.time.wait(100)
#     # pause_pygame()
#
#     # ŠITO DERINUKO IŠLOŠIMAI:
#     # * Galbut pagreitintas renderinimas (reikia testavimo)
#     # * Sumažinta užimtos vietos ir sutaupyta laiko kuriant atskirus veidus, jiems kodus, akių formoms.
#     # * Walking Front nebereikia nuotraukos, užtenka koju ranku ir pedu ilgius sumažinti.
#     # * Back view ir Back Walking taip pat patobuleja nes užtenka veidą panaikinti.
#     # * side walk patobulejo nes užtenka pakeisti koju ir ranku pozicijas
#
#
# def draw_pixel(screen, left, top, color):
#     for l in range(left, left + 10):
#         for t in range(top, top + 10):
#             screen.set_at((l, t), color)
#
#
#
#
# I.pg.init()  # initializes all game modules
# screen = I.pg.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))  # sets screen mode
# I.pg.display.set_caption('A Game')
# screen.fill('white')
# I.pg.display.flip()
# clock = I.pg.time.Clock()
# running = True  # if set to false game doesn't start and window doesn't open
# clicked_button = ""
# while running:
#     for event in I.pg.event.get():
#         if event.type == I.pg.QUIT:
#             running = False
#
#     get_body_coordinates(screen)

# import pygame
# import numpy as np
#
# pygame.mixer.pre_init(44100, -16, 2, 512)
# pygame.init()
#
# # Function to generate a sine wave for a given frequency
# def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=32767/10):
#     t = np.linspace(0, duration, int(sample_rate * duration), False)
#     wave = amplitude * np.sin(2 * np.pi * frequency * t)
#     wave = wave.astype(np.int16)
#     stereo_wave = np.zeros((wave.size, 2), dtype=np.int16)
#     stereo_wave[:, 0] = wave  # Left channel
#     stereo_wave[:, 1] = wave  # Right channel
#     return stereo_wave
#
# # Function to play a note
# def play_sine_wave(frequency, duration):
#     wave = generate_sine_wave(frequency, duration)
#     sound = pygame.sndarray.make_sound(wave)
#     sound.play(0)  # Play the sound once
#     pygame.time.wait(int(duration * 1000))  # Wait for the duration of the note
#
# # Example: Play a C4 note (261.63 Hz) for 0.1 second
# play_sine_wave(261.63, 0.1)
#
# # Quit Pygame
# pygame.quit()


def rename_images_in_folder(folder_path):
    import os
    import glob
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        Ff.debug_print(f"The folder '{folder_path}' does not exist.")
        return

    # Get the folder name
    folder_name = folder_path.split("/")[-1]

    # Get all image files in the folder (assuming common image extensions)
    image_files = glob.glob(os.path.join(folder_path, '*.*'))

    # # Filter image files to include only common image formats (you can add more if needed)
    image_files = [f for f in image_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # # Check if there are any image files in the folder
    if not image_files:
        Ff.debug_print(f"No image files found in the folder '{folder_path}'.")
        return
    Ff.debug_print(image_files)
    # # Rename each image file
    for image_path in image_files:
        folders = image_path.split("/")
        # Ff.debug_print(folders)
        new_path = ""
        for i in range(0, len(folders)-1):
            new_path += folders[i] + "/"
        new_path += folder_name + "/"
        file = folders[-1].split("\\")[1]
        try:
            number = file.split("pixil-frame-")[1]
            new_path += folder_name + "_" + number
            os.rename(image_path, new_path)
        except IndexError:
            Ff.debug_print("Completed")
        # Ff.debug_print(new_path)


# Example usage




# import pygame
# import numpy as np
#
# # Initialize Pygame mixer
# pygame.mixer.pre_init(44100, -16, 2, 512)
# pygame.init()
#
# # Function to generate a sine wave for a given frequency
#
# # Function to generate white noise
#
# # Generate components of the dying sound
# thud = generate_dying_sound()
#
#
# # Concatenate the sounds
#
# # Create a Pygame sound object
# sound = pygame.sndarray.make_sound(thud)
#
# # Play the sound
# sound.play()
# pygame.time.wait(1000)  # Wait for the sound to finish playing
#
# # Quit Pygame
# pygame.quit()

def create_table_if_not_exists(cursor, table_name, columns):
    """
    Create a table if it does not exist.

    Args:
        cursor (sqlite3.Cursor): SQLite cursor object.
        table_name (str): Name of the table to create.
        columns (list of tuples): Column definitions in the format (name, type).
    """
    columns_sql = ', '.join([f"{name} {type}" for name, type in columns])
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
    cursor.execute(create_table_sql)

def upload_data_to_db(table, data):
    import sqlite3
    """
    Upload data to the specified table in the database. If an entry with the same name exists, update it.
    Otherwise, insert a new entry.

    Args:
        table (str): The table name.
        data (list): The data to insert/update in the table.
    """
    conn = sqlite3.connect("C:/Users/gytis/PycharmProjects/A_Game/static/data/A_Game.db")
    cursor = conn.cursor()

    tables = {
        "items": [("name", "TEXT"), ("cost", "INTEGER"), ("properties", "TEXT"), ("aquire", "TEXT")],
        "spells": [("name", "TEXT"), ("damage", "TEXT"), ("type", "TEXT"), ("direction", "TEXT"),
                   ("mana", "INTEGER"), ("knockback", "INTEGER"), ("level", "INTEGER"), ("recharge", "INTEGER"),
                   ("description", "TEXT")],
        "decor": [("name", "TEXT"), ("harvestable", "TEXT"), ("flamable", "TEXT")]
    }

    if table not in tables:
        raise ValueError(f"Unknown table: {table}")

    # Create table if it doesn't exist
    create_table_if_not_exists(cursor, table, tables[table])

    # Check if an entry with the same name exists
    cursor.execute(f"SELECT * FROM {table} WHERE name = ?", (data[0],))
    existing_entry = cursor.fetchone()

    if existing_entry:
        # If entry exists, update it
        set_clause = ', '.join([f"{column[0]} = ?" for column in tables[table]])
        update_sql = f"UPDATE {table} SET {set_clause} WHERE name = ?"
        cursor.execute(update_sql, (*data, data[0]))
    else:
        # If entry does not exist, insert a new entry
        placeholders = ', '.join(['?' for _ in data])
        insert_sql = f"INSERT INTO {table} VALUES ({placeholders})"
        cursor.execute(insert_sql, data)

    conn.commit()
    cursor.close()
    conn.close()


# Upload_data_to_db(
#     "items",
#     [("name", "TEXT"), ("cost", "INTEGER"), ("properties", "TEXT"), ("aquire", "TEXT")],
#     ["Light Berries", 1, "CONSUMABLE(1-hp,,1-Exhaustion)", "HARVEST Bush_S_2,,1,,4,,5"])


# NAME # DAMAGE # TYPE # DIRECTION # MANA # KNOCKBACK # LEVEL # RECHARGE ( 1 = 100ms ) # DESCRIPTION
# Upload_data_to_db(
#     "spells",
#     ["Magic Bolt", "'1d4'", "Force", "LINE", 3, 3, 1, 3, "A blast of raw magical force"])
#
# Upload_data_to_db(
#     "spells",
#     ["Fire Bolt", "'1d4'", "Fire", "LINE", 5, 1, 2, 5, "A blast of fire that burns everything to cinders"])
#
# upload_data_to_db(
#     "spells",
#     ["Cold Bolt", '"1d4"', "Cold", "LINE", 6, 0, 3, 10, "A blast of ice that freezes the target"])

# upload_data_to_db(
#     "decor",
#     ["Bush_S_1", '', "True,,10"])
#
# upload_data_to_db(
#     "decor",
#     ["Bush_S_2", 'HARVESTABLE:Light Berries', "True,,10"])
#
# upload_data_to_db(
#     "decor",
#     ["Tree_T_1", '', "True,,5"])
#
# upload_data_to_db(
#     "decor",
#     ["Tree_M_1", 'AXE:Dark Wood', "True,,11"])
#
# upload_data_to_db(
#     "decor",
#     ["Tree_M_2", 'AXE:Light Wood,,HARVESTABLE:Apple', "True,,10"])

# import os
# I.pg.init()
#
# # Screen setup
# screen = I.pg.display.set_mode((800, 600))
# I.pg.display.set_caption("Sprite Example")
#
# clock = I.pg.time.Clock()
# FPS = 60
#
# def get_collision_side(rect1, rect2):
#     """
#     Determine which side of rect1 is colliding with rect2.
#     Returns a string: 'left', 'right', 'top', 'bottom'.
#     """
#     # Calculate overlap on each side
#     dx_left = abs(rect1.right - rect2.left)  # Distance from rect1's right to rect2's left
#     dx_right = abs(rect1.left - rect2.right)  # Distance from rect1's left to rect2's right
#     dy_top = abs(rect1.bottom - rect2.top)  # Distance from rect1's bottom to rect2's top
#     dy_bottom = abs(rect1.top - rect2.bottom)  # Distance from rect1's top to rect2's bottom
#
#     # Find the smallest overlap
#     min_dx = min(dx_left, dx_right)
#     min_dy = min(dy_top, dy_bottom)
#
#     if min_dx < min_dy:  # Horizontal collision
#         if dx_left < dx_right:
#             return [-1, 0]
#         else:
#             return [1, 0]
#     else:  # Vertical collision
#         if dy_top < dy_bottom:
#             return [0, 1]
#         else:
#             return [0, -1]
#
# class Decoration(I.pg.sprite.Sprite):
#     def __init__(self, rect, path, hp):
#         super().__init__()
#         image = I.pg.image.load(path)
#
#         self.image = I.pg.transform.scale(image, (rect[2], rect[3]))
#
#         self.rect = rect
#
# class Mob(I.pg.sprite.Sprite):
#     def __init__(self, init_x, init_y, path, frame_count, delay):
#         # I.pg.sprite.Sprite.__init__(self)
#         super().__init__()
#         self.images = []
#         self.frame_count = frame_count
#         self.current_frame = 0
#         self.frame_time = I.pg.time.get_ticks()
#         self.frame_change = False
#         self.delay = delay
#         for i in range(0, self.frame_count):
#             self.images.append(I.pg.image.load(path.replace("0", str(i))))
#
#         self.rect = I.pg.Rect(init_x, init_y, 100, 100)
#         self.target_position = I.pg.math.Vector2(init_x, init_y)
#
#         self.blocking_movement = [0, 0]
#     def update(self):
#         if self.frame_time + self.delay < I.pg.time.get_ticks():
#             self.current_frame += 1
#             self.frame_time = I.pg.time.get_ticks()
#             self.frame_change = True
#             if self.current_frame >= self.frame_count:
#                 self.current_frame = 0
#         else:
#             self.frame_change = False
#         self.image = self.images[self.current_frame]
#         self.image = I.pg.transform.scale(self.image, (100, 100))
#         self.go(self.target_position.x, self.target_position.y)
#
#     def set_target(self, x, y):
#         # Set a new target position
#         self.target_position = I.pg.math.Vector2(x, y)
#
#     def go(self, new_x, new_y):
#         # Calculate the direction vector
#         direction = I.pg.math.Vector2(new_x - self.rect.x, new_y - self.rect.y)
#         distance = direction.length()  # Length of the vector (distance to target)
#
#         # Normalize the direction vector (gives it a length of 1)
#         if distance != 0:  # Avoid division by zero
#             direction = direction.normalize()
#         # Scale the direction vector by a constant speed
#         speed = 5  # Pixels per frame (adjust for desired pace)
#         velocity = direction * speed
#
#         # Update the sprite's position using the velocity
#         if distance > speed and self.frame_change:  # If we're farther than one step away, keep moving
#             if self.blocking_movement[0] == -1 and velocity.x < 0:
#                 self.rect.x += 0
#                 Ff.debug_print("blocking_left")
#             elif self.blocking_movement[0] == 1 and velocity.x > 0:
#                 self.rect.x += 0
#                 Ff.debug_print("blocking right")
#             else:
#                 self.rect.x += velocity.x
#             Ff.debug_print(velocity, self.blocking_movement)
#             if self.blocking_movement[1] == 1 and velocity.y < 0:
#                 self.rect.y += 0
#                 Ff.debug_print("blocking up")
#             elif self.blocking_movement[1] == -1 and velocity.y > 0:
#                 self.rect.y += 0
#                 Ff.debug_print("blocking down")
#             else:
#                 self.rect.y += velocity.y
#         self.blocking_movement = [0, 0]
#
#
# path = os.getcwd().replace("Testing", "/static/images/Mobs/Ooze/Slime_S/Slime_S_0.png")
# mob = Mob(400, 200, path, 10, 50)
# path = os.getcwd().replace("Testing", "/static/images/Background/Trees/Tree_M_1.png")
#
# decor = Decoration(I.pg.Rect(350, 350, 100, 100), path, 10)
# decor1 = Decoration(I.pg.Rect(300, 330, 100, 100), path.replace("M_1", "M_2"), 10)
# mobs = I.pg.sprite.Group()
# decorations = I.pg.sprite.Group()
# decorations.add(decor)
# decorations.add(decor1)
# mobs.add(mob)
#
# running = True
# while running:
#     screen.fill("black")
#     for event in I.pg.event.get():
#         if event.type == I.pg.MOUSEMOTION:
#             pos = I.pg.mouse.get_pos()
#             mob.set_target(pos[0], pos[1])
#         elif event.type == I.pg.QUIT:
#             running = False
#     decorations.draw(screen)
#     mobs.update()
#     mobs.draw(screen)
#     collisions = I.pg.sprite.groupcollide(mobs, decorations, False, False)
#     if collisions:
#         for mob, colliding_decorations in collisions.items():
#             # Ff.debug_print(f"{mob} is colliding with {colliding_decorations}")
#             for decor in colliding_decorations:
#                 mob.blocking_movement = get_collision_side(decor.rect, mob.rect)
#                 # Ff.debug_print(side)
#
#
#     I.pg.display.flip()
# I.pg.quit()
#
# Ff.debug_print(mobs)



 # pyinstaller --onefile --icon=.\static\images\Icon.ico .\A_Game.py
# rename_images_in_folder("C:/Users/gytis.monstvilas/Documents/GitHub/A_Game/static/images/Mobs/Plant/Ent_Hidden")  #at the end of the path last folder doesn't need /