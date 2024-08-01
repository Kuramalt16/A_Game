from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S

S_LEFT = S.SCREEN_WIDTH / 2 - (S.SCREEN_WIDTH / 2.2)
S_TOP = S.SCREEN_HEIGHT / 2 - (S.SCREEN_HEIGHT / 2.2)

S_F_WIDTH = S.SCREEN_WIDTH - (2 * S_LEFT)
S_F_HEIGHT = S.SCREEN_HEIGHT / 10 * 8

CB_LEFT = S_LEFT + S.SCREEN_WIDTH / 10
CB_TOP = S_TOP + S.SCREEN_HEIGHT / 20

CB_WIDTH = S.SCREEN_WIDTH / 15
CB_HEIGHT = S.SCREEN_HEIGHT / 15

B_LEFT1 = CB_LEFT * 2
B_LEFT2 = CB_LEFT * 4
B_TOP = S.SCREEN_HEIGHT - (S.SCREEN_HEIGHT / 3)

B_WIDTH = S.SCREEN_WIDTH / 5
B_HEIGHT = S.SCREEN_HEIGHT / 10

TEXT1_LEFT = CB_LEFT * 1.5
TEXT1_WIDTH = S_F_WIDTH * 0.3

SLIDER_TOP = CB_TOP * 2
SLIDER_WIDTH = S.SCREEN_WIDTH / 3
SLIDER_HEIGHT = S.SCREEN_HEIGHT / 15

SLIDER_BUTTON_HEIGHT = S.SCREEN_HEIGHT / 13.5
SLIDER_BUTTON_LEFT = S.RESOLUTION * (CB_LEFT / 2 + SLIDER_WIDTH)

SLIDER_MIN = S.SCREEN_WIDTH / 2
SLIDER_MAX = round(SLIDER_WIDTH + SLIDER_MIN - CB_WIDTH)  # SLIDER END is determened by adding the startpoint of the slider (Slider_min) then adding the width of the slider so we would get to the end and subtracting the width of the slider button it self

def Settings(screen):
    buttons = {}
    frame_main_menu = Ff.add_image_to_screen(screen, 'static/images/Frame_main_menu_Big.png', [S_LEFT, S_TOP, S_F_WIDTH, S_F_HEIGHT])
    buttons['Checkbox'] = fullscreen_checkbox(screen)
    buttons['Apply'] = Ff.add_image_to_screen(screen, 'static/images/Apply.png', [B_LEFT1, B_TOP, B_WIDTH, B_HEIGHT])
    buttons['Cancel'] = Ff.add_image_to_screen(screen, 'static/images/Cancel.png', [B_LEFT2, B_TOP, B_WIDTH, B_HEIGHT])
    Ff.display_text(screen, "RESOLUTION: ", 30, (CB_LEFT, CB_TOP * 2.1), "black")
    Ff.add_image_to_screen(screen, 'static/images/Slider.png', [S.SCREEN_WIDTH / 2, SLIDER_TOP, SLIDER_WIDTH, SLIDER_HEIGHT])
    buttons['Slider_button'] = Ff.add_image_to_screen(screen, 'static/images/Slider_button.png', [(SLIDER_MAX-SLIDER_MIN) * S.RESOLUTION + SLIDER_MIN, SLIDER_TOP, CB_WIDTH, SLIDER_BUTTON_HEIGHT])
    Ff.display_text(screen, "FRAME RATE: ", 30, (CB_LEFT, CB_TOP * 3.2), "black")
    # Ff.add_image_to_screen(screen, 'static/images/Slider.png', [S.SCREEN_WIDTH / 2, SLIDER_TOP*1.5, SLIDER_WIDTH, SLIDER_HEIGHT])
    # buttons['Slider_button_fps'] = Ff.add_image_to_screen(screen, 'static/images/Slider_button.png', [(SLIDER_MAX-SLIDER_MIN) * S.RESOLUTION + SLIDER_MIN, SLIDER_TOP * 1.5, CB_WIDTH, SLIDER_BUTTON_HEIGHT])
    Ff.add_image_to_screen(screen, 'static/images/Slider.png', [S.SCREEN_WIDTH / 2, SLIDER_TOP * 2, SLIDER_WIDTH, SLIDER_HEIGHT])
    Ff.display_text(screen, "VOLUME: ", 30, (CB_LEFT, CB_TOP * 4.3), "black")
    buttons["Slider_button_Volume"] = Ff.add_image_to_screen(screen, 'static/images/Slider_button.png', [(SLIDER_MAX-SLIDER_MIN) * S.VOLUME + SLIDER_MIN, SLIDER_TOP * 2, CB_WIDTH, SLIDER_BUTTON_HEIGHT])
    I.pg.display.flip()
    return buttons

def fullscreen_checkbox(screen):
    if S.FULLSCREEN_CH:
        text = Ff.display_text(screen, "FULL SCREEN: ", 30, (CB_LEFT, CB_TOP * 1.1), "black")
        checkbox = Ff.add_image_to_screen(screen, 'static/images/Checkbox_on.png',
                                          [S.SCREEN_WIDTH / 2, CB_TOP, CB_WIDTH, CB_HEIGHT])
    else:
        text = Ff.display_text(screen, "FULL SCREEN: ", 30, (CB_LEFT, CB_TOP * 1.1), "black")
        checkbox = Ff.add_image_to_screen(screen, 'static/images/Checkbox_off.png',
                                          [S.SCREEN_WIDTH / 2, CB_TOP, CB_WIDTH, CB_HEIGHT])
    checkbox = checkbox.union(text)
    return checkbox

