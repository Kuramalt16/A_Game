from Values import Settings as S
from utils import Frequent_functions as Ff, Imports as I

S_LEFT = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 5)
S_TOP = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / 2.2)
S_F_WIDTH = S.SCREEN_WIDTH - (2 * S_LEFT)
S_F_HEIGHT = S.SCREEN_HEIGHT / 10 * 9

CHAR_LEFT = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 6)
CHAR_TOP = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / 3)
CHAR_W = S.SCREEN_WIDTH / 10
CHAR_H = S.SCREEN_HEIGHT / 8

image_path = 'static/images/'
data_path = 'static/data/created_characters/'

def load_data(screen):
    buttons = {}
    frame = Ff.add_image_to_screen(screen, 'static/images/Frame_main_menu.png', [S_LEFT, S_TOP, S_F_WIDTH, S_F_HEIGHT])

    buttons["Back"] = Ff.add_image_to_screen(screen, image_path + 'Back.png',[frame.left + frame.w * 0.25,frame.top + frame.h * 0.8, S_F_WIDTH / 2, S_F_HEIGHT / 10])
    char_name_list = I.os.listdir(data_path)
    push_left = 0
    push_top = 0
    iteration = 0
    for name in char_name_list:
        if iteration == 3:
            iteration = 0
            push_left = 0
            push_top += CHAR_H * 2
        buttons[name] = Ff.add_image_to_screen(screen, data_path + name + "/" + name + "Front.png", [CHAR_LEFT + push_left, CHAR_TOP + push_top, CHAR_W, CHAR_H])
        Ff.display_text(screen, name, 16, (buttons[name].left, buttons[name].top - buttons[name].h/2), "Black")

        push_left += CHAR_W * 1.2
        iteration += 1
    I.pg.display.flip()
    return buttons

def char_data(screen):
    buttons = {}
    name = I.info.SELECTED_CHARACTER
    txt_data = Ff.read_text_file_return_dict(data_path + name + "/" + name + ".txt")
    I.info.DATA = txt_data
    frame = Ff.add_image_to_screen(screen, 'static/images/Frame_main_menu.png', [S_LEFT, S_TOP, S_F_WIDTH, S_F_HEIGHT])
    buttons[name] = Ff.add_image_to_screen(screen, data_path + name + "/" + name + "Front.png",[frame.left + S_F_WIDTH / 20, frame.top + S_F_HEIGHT / 20, S_F_WIDTH / 3, S_F_HEIGHT / 3])
    Ff.display_text(screen, I.info.SELECTED_CHARACTER, 30,(buttons[name].left + buttons[name].w, buttons[name].top), "Black")
    Ff.display_text(screen, "Last Save: " + str(txt_data["Last Save"]), 10,(buttons[name].left + buttons[name].w, buttons[name].top + S_F_HEIGHT / 20 * 1.5), "Black")
    Ff.display_text(screen, "Level: " + str(txt_data["Level"]), 10,(buttons[name].left + buttons[name].w, buttons[name].top + S_F_HEIGHT / 20 * 2.5), "Black")
    Ff.display_text(screen, "Class: " + str(txt_data["Class"]), 10,(buttons[name].left + buttons[name].w, buttons[name].top + S_F_HEIGHT / 20* 3.5), "Black")
    Ff.display_text(screen, "Alignment: " + str(txt_data["Alignment"]), 10,(buttons[name].left + buttons[name].w, buttons[name].top + S_F_HEIGHT / 20 * 4.5), "Black")

    Ff.display_text(screen, "Touch Yourself", 20,(frame.left + S_F_WIDTH / 20, buttons[name].top + S_F_HEIGHT / 20 * 7), "Black")
    buttons["Back"] = Ff.add_image_to_screen(screen, image_path + 'Back.png',[frame.left + frame.w * 0.25,frame.top + frame.h * 0.8, S_F_WIDTH / 2, S_F_HEIGHT / 10])
    buttons["Delete"] = Ff.add_image_to_screen(screen, image_path + 'Empty.png',[frame.left + frame.w * 0.25,frame.top + frame.h * 0.7, S_F_WIDTH / 2, S_F_HEIGHT / 10])
    Ff.display_text(screen, "Delete", 30, (buttons["Delete"].left + buttons["Delete"].left / 7, buttons["Delete"].top * 1.025), "Red")
    return buttons

def render_face(screen, data):
    face = {"Unaligned": "None",
            "Neutral Good": "static/images/Alignment/Neutral Good.png",
            "Neutral": "None",
            "Neutral Evil": "static/images/Alignment/Neutral Evil.png",
            "Chaotic Good": 'static/images/Alignment/Chaotic Good.png',
            "Chaotic Neutral": 'static/images/Alignment/Chaotic Neutral.png',
            "Chaotic Evil": 'static/images/Alignment/Chaotic Evil.png',
            "Lawful Good": 'static/images/Alignment/Lawful Good.png',
            "Lawful Neutral": 'static/images/Alignment/Lawful Neutral.png',
            "Lawful Evil": 'static/images/Alignment/Lawful Evil.png'
            }
    name = I.info.SELECTED_CHARACTER
    tuple_data = I.info.DATA["Skin"].strip('()')
    tuple_elements = tuple_data.split(',')
    if data == 1 and face[I.info.DATA["Alignment"]] != "None":
    # if data == 1:
        Ff.add_image_to_screen(screen, face[I.info.DATA["Alignment"]], [S_LEFT + S_F_WIDTH / 20, S_TOP + S_F_HEIGHT / 20, S_F_WIDTH / 3, S_F_HEIGHT / 3])
        # Ff.add_image_to_screen(screen, face["Lawful Neutral"], [S_LEFT + S_F_WIDTH / 20, S_TOP + S_F_HEIGHT / 20, S_F_WIDTH / 3, S_F_HEIGHT / 3])
        for top in range(int(S_TOP + S_F_HEIGHT / 20), int(S_TOP + S_F_HEIGHT / 20 + S_F_HEIGHT / 3)):
            for i in range(int(S_LEFT + S_F_WIDTH / 20), int(S_LEFT + S_F_WIDTH / 20 + S_F_WIDTH / 3)):
                color = screen.get_at((i, top))
                if color == (255, 205, 210, 255):
                    screen.set_at((i, top), tuple(map(int, tuple_elements)))
    elif data == 0:
        Ff.add_image_to_screen(screen, data_path + name + "/" + name + "Front.png",[S_LEFT + S_F_WIDTH / 20, S_TOP + S_F_HEIGHT / 20, S_F_WIDTH / 3, S_F_HEIGHT / 3])
