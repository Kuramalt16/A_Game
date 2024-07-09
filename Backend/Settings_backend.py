from utils import Imports as I, Frequent_functions as Ff
from Render import Settings_render as sr
from Values import Settings as S


def Settings(screen):
    apply = False
    cancel = False
    clicked_button = ""
    screen.fill("white")
    I.pg.display.flip()
    buttons = sr.Settings(screen)
    while not apply and not cancel:
        for event in I.pg.event.get():
            if event.type == I.pg.QUIT:
                cancel = True
                Ff.base_settings_load()
            pos = I.pg.mouse.get_pos()
            if event.type == I.pg.MOUSEBUTTONDOWN:
                for key, value in buttons.items():
                    if value.collidepoint(pos[0], pos[1]) and I.pg.mouse.get_pressed()[0]:
                        if key == "Checkbox":
                            S.FULLSCREEN_CH = Ff.toggle_bool(S.FULLSCREEN_CH)
                            buttons[key] = sr.fullscreen_checkbox(screen)
                            I.pg.display.update(buttons[key])
                            clicked_button = key
                        elif key in ["Apply", "Cancel"]:
                            Ff.button_click_render(screen, value, 1, key)
                            I.pg.display.flip()
                            clicked_button = key
                        elif key == "Slider_button":
                            while True:
                                pos = I.pg.mouse.get_pos()
                                buttons[key] = Ff.button_click_render(screen, value, pos[0], key)
                                I.pg.display.update(buttons[key])
                                I.pg.event.get()
                                if not I.pg.mouse.get_pressed()[0]:
                                    clicked_button = key
                                    buttons[key] = Ff.button_click_render(screen, buttons[key], 0, key)
                                    I.pg.display.update(buttons[key])
                                    break
            if event.type == I.pg.MOUSEBUTTONUP:
                for key, value in buttons.items():
                    if value.collidepoint(pos[0], pos[1]) and not I.pg.mouse.get_pressed()[0]:
                        if key == "Apply" and clicked_button == key:
                            apply = True
                            Ff.button_click_render(screen, value, 0, key)
                            I.pg.display.flip()
                        elif key == "Cancel" and clicked_button == key:
                            cancel = True
                            Ff.base_settings_load()
                            Ff.button_click_render(screen, value, 0, key)
                            I.pg.display.flip()
                        elif key == "Slider_button" and clicked_button == key:
                            Ff.button_click_render(screen, value, 0, key)
                            I.pg.display.flip()
                    else:
                        if clicked_button == key and clicked_button != "Checkbox":
                            Ff.button_click_render(screen, value, 0, clicked_button)
                            I.pg.display.flip()
                            clicked_button = ""

    if apply:
        Apply_settings(buttons)

    S.START_APP = True
    S.MAIN_MENU = True

def Apply_settings(buttons):
    if S.FULLSCREEN_CH and not S.FULLSCREEN:  # if full screen checkbox is True set Fullscreen variable to True and toggle fullscreen to ON
        I.pg.display.toggle_fullscreen()
        S.FULLSCREEN = True
    elif not S.FULLSCREEN_CH and S.FULLSCREEN:
        I.pg.display.toggle_fullscreen()
        S.FULLSCREEN = False
    data = buttons["Slider_button"].left
    if data > sr.SLIDER_MAX:
        data = sr.SLIDER_MAX
    elif data < sr.SLIDER_MIN:
        data = sr.SLIDER_MIN
    demo_resolution = (data - sr.SLIDER_MIN) / (sr.SLIDER_MAX - sr.SLIDER_MIN)
    if demo_resolution > 1:
        demo_resolution = 1
    if demo_resolution != S.RESOLUTION:
        S.SCREEN_WIDTH = round((demo_resolution * 600 + 680) / 10) * 10
        S.RESTART = True
    save_settings()

def save_settings():
    with open("Values/Settings.py", 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith('SCREEN_WIDTH'):
            # Update the line with the new value
            lines[i] = f'SCREEN_WIDTH = {S.SCREEN_WIDTH}\n'
            break
    with open("Values/Settings.py", 'w') as file:
        file.writelines(lines)