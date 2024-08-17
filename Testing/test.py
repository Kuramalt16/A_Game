from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S

def testing_events(event):
    if event.type == I.pg.ACTIVEEVENT:
        # print("ACTIVEEVENT")
        pass
    elif event.type == I.pg.WINDOWLEAVE:
        # print("WINDOWLEAVE")
        pass
    elif event.type == I.pg.WINDOWMOVED:
        # print("WINDOWMOVED")  # prints when screen was moved
        pass
    elif event.type == I.pg.VIDEOEXPOSE:
        # print("VIDEOEXPOSE")  # prints once when the game is on screen after being moved
        pass
    elif event.type == I.pg.WINDOWEXPOSED:
        # print("WINDOWEXPOSED")  # prints once when the game is on screen after being moved
        pass
    elif event.type == I.pg.WINDOWENTER:
        # print("WINDOWENTER")  # prints once the game is in focus (mouse on window)
        pass
    elif event.type == I.pg.MOUSEMOTION:
        # print("MOUSEMOTION")  # prints when mouse moves
        pass
    elif event.type == I.pg.AUDIODEVICEADDED:
        # print("AUDIODEVICEADDED")  # prints once the game is launched
        pass
    elif event.type == I.pg.WINDOWSHOWN:
        # print("WINDOWSHOWN")  # prints when the game first is opened
        pass
    elif event.type == I.pg.WINDOWFOCUSGAINED:
        # print("WINDOWFOCUSGAINED")
        pass
    elif event.type == I.pg.TEXTEDITING:
        # print("TEXTEDITING")  # prints once when minimized
        pass
    elif event.type == I.pg.WINDOWMINIMIZED:
        # print("WINDOWMINIMIZED")
        pass
    elif event.type == I.pg.WINDOWFOCUSLOST:
        # print("WINDOWFOCUSLOST")
        pass
    elif event.type == I.pg.WINDOWRESTORED:
        # print("WINDOWRESTORED")
        pass
    elif event.type == I.pg.CLIPBOARDUPDATE:
        # print("CLIPBOARDUPDATE")
        pass
    elif event.type == I.pg.WINDOWCLOSE:
        # print("WINDOWCLOSE")
        pass
    elif event.type == I.pg.MOUSEBUTTONDOWN:
        # print("MOUSEBUTTONDOWN")  # when mouse button was clicked
        pass
    elif event.type == I.pg.MOUSEBUTTONUP:
        # print("MOUSEBUTTONUP")  # when mouse button was released
        pass
    elif event.type == I.pg.MOUSEWHEEL:
        # print("MOUSEWHEEL")  # prints when mousewheel is scrolling
        pass
    elif event.type == I.pg.KEYDOWN:
        # print("KEYDOWN")  # pritns when a key is pressed down

        if event.key == 27:
            print("Esc_key")
        elif event.key == 13:
            print("Enter_key")
        elif event.key == I.pg.K_F1:
            print("F1")
        elif event.key == I.pg.K_F2:
            print("F2")
        elif event.key == I.pg.K_F3:
            print("F3")
        elif event.key == I.pg.K_F4:
            print("F4")
        elif event.key == I.pg.K_F5:
            print("F5")
        elif event.key == I.pg.K_F6:
            print("F6")
        elif event.key == I.pg.K_F7:
            print("F7")
        elif event.key == I.pg.K_F8:
            print("F8")
        elif event.key == I.pg.K_F9:
            print("F9")
        elif event.key == I.pg.K_F10:
            print("F10")
        elif event.key == I.pg.K_F11:
            print("F11")
        elif event.key == I.pg.K_F12:
            print("F12")
        elif event.key == I.pg.K_DELETE:
            print("DELETE")
        elif event.key == I.pg.K_BACKSPACE:
            print("Backspace")
        elif event.key == I.pg.K_LSHIFT:
            print("K_LSHIFT")
        elif event.key == I.pg.K_LCTRL:
            print("K_LCTRL")
        elif event.key == I.pg.K_LALT:
            print("K_LALT")
        elif event.key == I.pg.K_RIGHT:
            print("K_RIGHT")
        elif event.key == I.pg.K_LEFT:
            print("K_LEFT")
        elif event.key == I.pg.K_UP:
            print("K_UP")
        elif event.key == I.pg.K_DOWN:
            print("K_DOWN")
            # else:
            # print(event.key)
    elif event.type == I.pg.KEYUP:
        # print("KEYUP")  # pritns when a key is pressed up
        pass
    elif event.type == I.pg.TEXTINPUT:
        print(event.text)  # prints what key was pressed
        # print("TEXTINPUT")
        # elif event.type == pygame.WINDOWFOCUSGAINED:
        #     print("WINDOWFOCUSGAINED")
        # elif event.type == pygame.WINDOWFOCUSGAINED:
        #     print("WINDOWFOCUSGAINED")
        # elif event.type == pygame.WINDOWFOCUSGAINED:
        #     print("WINDOWFOCUSGAINED")
        # elif event.type == pygame.WINDOWFOCUSGAINED:
        #     print("WINDOWFOCUSGAINED")
    else:
        print(event.type)

def Put_a_stone(screen):
    image = I.pg.image.load("static/images/Stone_mid.png")  # Replace with your image file path
    image = I.pg.transform.scale(image, (50, 50))
    screen.blit(image, (0, 0))
    I.pg.display.flip()  # send display data

def Make_rect_visible(screen, rect, color):
    I.pg.draw.rect(screen, color, rect)


def get_time_diferance(time1, time2):
    print(time1-time2)

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
    execution_time = end_time - start_time
    print("overall time: should be 233 ms ", execution_time)



# def get_body_coordinates(screen):
#     S_LEFT = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 5)
#     S_TOP = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / 2.2)
#     S_F_WIDTH = S.SCREEN_WIDTH - (2 * S_LEFT)
#     S_F_HEIGHT = S.SCREEN_HEIGHT / 10 * 8
#     body_sizes = [int(S_LEFT) + int(S_F_WIDTH / 4), int(S_TOP) + int(S_F_HEIGHT / 6), int(S_F_WIDTH / 2), int(S_F_HEIGHT / 2)]
#     Ff.add_image_to_screen(screen, "static/images/Race/Human/Girl/Human_Girl.png", body_sizes)
#     # print(body_sizes)
#     # screen.fill("white")
#     # I.pg.display.flip()
#     color_coordinates = {}
#     # options = {0: ["Front", "Front1", "Front", "Front2", "Front", "Front1", "Front", "Front2"],
#                # 1: ["Back", "Back1", "Back", "Back2", "Back", "Back1", "Back", "Back2"],
#                # 2: ["Left"]}
#     options = {0: ["Right", "Right1","Right","Right2"]}
#     for a in range(0, len(options)):
#         for i in options[a]:
#             # print(options[a])
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
        print(f"The folder '{folder_path}' does not exist.")
        return

    # Get the folder name
    folder_name = folder_path.split("/")[-1]

    # Get all image files in the folder (assuming common image extensions)
    image_files = glob.glob(os.path.join(folder_path, '*.*'))

    # # Filter image files to include only common image formats (you can add more if needed)
    image_files = [f for f in image_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # # Check if there are any image files in the folder
    if not image_files:
        print(f"No image files found in the folder '{folder_path}'.")
        return
    print(image_files)
    # # Rename each image file
    for image_path in image_files:
        folders = image_path.split("/")
        # print(folders)
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
            print("Completed")
        # print(new_path)


# Example usage

# rename_images_in_folder("C:/Users/gytis/PycharmProjects/A_Game/static/images/Combat/Piercing")



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


#  pyinstaller --onefile --icon=.\static\images\Icon.ico .\A_Game.py
