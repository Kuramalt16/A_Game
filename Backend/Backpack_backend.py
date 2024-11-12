from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S

def BackPack(screen, items, player):
    pressed = 0 # key authentication
    running = True # loop var
    block = (0, 0) # backpack block
    border = 1 # rect border size
    use = 0 # place holder for items to be eaten/used
    selected = 0 # place holder for rect of selected block
    color = "Yellow" # color of selected rect
    pickup = (0, 0, 0) # place holder for the name, posx, posy of selected block
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    coordinates = get_equipment_coordinates(block)
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_i:
                    pressed = I.pg.K_i
                elif event.key == I.pg.K_ESCAPE:
                    pressed = I.pg.K_ESCAPE
                elif event.key == I.pg.K_x:
                    pressed = I.pg.K_x
                    color = "Green"
                    for key, value in I.info.BACKPACK_CONTENT.items():
                        if value[1] == block[0] and value[2] == block[1]:
                            # if the possision matches get the key
                            use = key
                elif event.key == I.pg.K_c:
                    pressed = I.pg.K_c
                    if selected == 0:
                        if block[0] >= 0:
                            selected = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
                        else:
                            selected = I.pg.Rect(coordinates[block][0], coordinates[block][1], item_w, item_h)
                            I.info.EQUIPED[I.info.equipment[block]] = 0, I.info.EQUIPED[I.info.equipment[block]][1]
                        pickup = (Ff.find_item_by_slot(block[0], block[1]), block[0], block[1])
                        I.QB.tutorial_move_berry(pickup)

                    else:
                        if pickup[0] != 0 and pickup[0] != None and (pickup[1:]) != block:
                            I.PB.update_equipment_var(block, pickup[0])
                            value = I.info.BACKPACK_CONTENT[pickup[0]]
                            taken_spaces = list(I.info.BACKPACK_CONTENT.values())
                            if not any((block[0], block[1]) == (tpl[1], tpl[2]) for tpl in taken_spaces):
                                I.info.BACKPACK_CONTENT[pickup[0]] = (value[0], block[0], block[1]) # set the new possision value
                            else:
                                # switching two item places
                                existing_item = Ff.find_item_by_slot(block[0], block[1]) # get existing item name
                                if "STACK" in existing_item and "STACK" in pickup[0] and pickup[0].split("|")[0] == existing_item.split("|")[0]:
                                    # BOTH OF THESE ITEMS ARE STACKS and are the same item name
                                    stack = Ff.get_property(existing_item.split("|")[0], items, "STACK")
                                    if float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0]][0]) <= stack:
                                        # MERGING TWO STACKS INTO ONE
                                        sum = float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0]][0])
                                        I.info.BACKPACK_CONTENT[existing_item] = int(sum), I.info.BACKPACK_CONTENT[existing_item][1], I.info.BACKPACK_CONTENT[existing_item][2]
                                        del I.info.BACKPACK_CONTENT[pickup[0]]

                                    elif float(I.info.BACKPACK_CONTENT[existing_item][0]) < stack and float(I.info.BACKPACK_CONTENT[pickup[0]][0]) < stack:
                                        # MERGING VALUES OF STACKS WITH REMAINDER
                                        remainder = float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0]][0]) - stack
                                        I.info.BACKPACK_CONTENT[pickup[0]] = int(remainder), I.info.BACKPACK_CONTENT[pickup[0]][1], I.info.BACKPACK_CONTENT[pickup[0]][2]
                                        I.info.BACKPACK_CONTENT[existing_item] = int(stack), I.info.BACKPACK_CONTENT[existing_item][1], I.info.BACKPACK_CONTENT[existing_item][2]
                                else:
                                    """Changing places of two diferent items"""
                                    I.info.BACKPACK_CONTENT[existing_item] = I.info.BACKPACK_CONTENT[existing_item][0], pickup[1], pickup[2]
                                    I.info.BACKPACK_CONTENT[pickup[0]] = I.info.BACKPACK_CONTENT[pickup[0]][0], block[0], block[1]

                                I.PB.update_equipment_var((pickup[1], pickup[2]), existing_item)
                                # if block[0] < 0:
                                #     I.info.EQUIPED[I.info.equipment[(pickup[1], pickup[2])]] = existing_item
                        pickup = (0, 0, 0)
                        selected = 0
                block = key_press_get_block(event, block, 14, 26, "backpack")
            elif event.type == I.pg.KEYUP:
                if pressed == I.pg.K_i or pressed == I.pg.K_ESCAPE:
                    running = False  # exits backpack view
                elif pressed == I.pg.K_x:
                    color = "Yellow"
                    if use != 0 and "CONSUMABLE" in items.item_dict[use.split("|")[0]]["Properties"]:
                        I.QB.tutorial_eat_berry(use)
                        handle_consumption(items, player, use)
                        use = 0
                    pressed = 0
                    selected = 0

            display_backpack(screen, player, items, screen.get_rect(), "full")
            if block[0] < 0:
                if block[0] < -10:
                    block = -10, block[1]
                if block[1] > 8:
                    block = block[0], 8
                coordinates = get_equipment_coordinates(block)
                if block[0] < -2 and block[0] >= -6 and block[1] != 8:
                    block = -10, block[1]
                if block[0] <= -6 and block[0] > -10 and block[1] != 8:
                    block = -2, block[1]
                rect = I.pg.Rect(coordinates[block][0], coordinates[block][1], item_w, item_h)
            else:
                rect = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
            I.pg.draw.rect(screen, color, rect, border)
            if selected != 0:
                I.pg.draw.rect(screen, "Yellow", selected, 2)

            I.pg.display.flip()

def display_backpack(screen, player, items, rect, word):
    I.info.BACKPACK_CONTENT["Gold"] = (player["Gold"],I.info.BACKPACK_CONTENT["Gold"][1], I.info.BACKPACK_CONTENT["Gold"][2])
    bag = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Backpack_Empty_" + word], [rect.center[0] * 0.5 ,rect.center[1] * 0.25, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT * 0.75])
    get_backpack_coordinates(screen, word)
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    for content in I.info.BACKPACK_CONTENT.keys():
        row = I.info.BACKPACK_CONTENT[content][1]
        collumn = I.info.BACKPACK_CONTENT[content][2]
        if row < 0:
            if word == "half":
                continue
            else:
                coordinates = get_equipment_coordinates((row,collumn))
                Ff.add_image_to_screen(screen, items.item_dict[content.split("|")[0]]["path"], [coordinates[row, collumn][0], coordinates[row, collumn][1], item_w, item_h])
                Ff.display_text(screen, str(int(I.info.BACKPACK_CONTENT[content][0])), 2, [coordinates[row, collumn][0], coordinates[row, collumn]][1], "white")
        else:
            # HANDLE MULTIPLE STACKS
            Ff.add_image_to_screen(screen, items.item_dict[content.split("|")[0]]["path"],[list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn], item_w, item_h])
            if content == "Gold":
                amount = round(player["Gold"], 3)
                Ff.display_text(screen, str(amount), 1, [list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn]], "white")
            else:
                Ff.display_text(screen, str(int(I.info.BACKPACK_CONTENT[content][0])), 1, [list(I.info.BACKPACK_COORDINATES_X.values())[row], list(I.info.BACKPACK_COORDINATES_Y.values())[collumn]], "white")
    if word == "full":
        I.pg.draw.rect(screen, "black", (bag.w * 0.604, bag.h * 0.807, bag.w * 0.115, bag.h * 0.012))
        remainder = player["hp"][0] / player["hp"][1]
        I.pg.draw.rect(screen, "red", (bag.w * 0.604, bag.h * 0.807, bag.w * 0.115 * remainder, bag.h * 0.012))
        Ff.display_text(screen, "Hp", 1, (bag.w * 0.562, bag.h * 0.80), "black")

        I.pg.draw.rect(screen, "black", (bag.w * 0.808, bag.h * 0.807, bag.w * 0.148, bag.h * 0.012))
        remainder = player["mana"][0] / player["mana"][1]
        I.pg.draw.rect(screen, "blue", (bag.w * 0.808, bag.h * 0.807, bag.w * 0.148 * remainder, bag.h * 0.012))
        Ff.display_text(screen, "Mp", 1, (bag.w * 0.752, bag.h * 0.80), "black")

        I.pg.draw.rect(screen, "black", (bag.w * 0.604, bag.h * 0.857, bag.w * 0.115, bag.h * 0.012))
        remainder = int(player["Exhaustion"][0]) / int(player["Exhaustion"][1])
        I.pg.draw.rect(screen, "Green", (bag.w * 0.604, bag.h * 0.857, bag.w * 0.115 * remainder, bag.h * 0.012))
        Ff.display_text(screen, "Exh", 1, (bag.w * 0.55, bag.h * 0.85), "black")

        Ff.add_image_to_screen(screen,'static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + "Front.png",
                               [rect.center[0] * 0.64 ,rect.center[1] * 0.4, S.SCREEN_WIDTH / 8, S.SCREEN_HEIGHT / 4])

        Ff.display_text(screen, "Level: " + str(player["Level"]) , 5, (bag.w * 0.65, bag.h * 0.25), "black")

        I.pg.draw.rect(screen, "black", (bag.w * 0.626, bag.h * 0.71, bag.w * 0.3, bag.h * 0.025))
        remainder = player["Experience"] / I.PB.exp_till_lvup(player)
        I.pg.draw.rect(screen, "light green", (bag.w * 0.626, bag.h * 0.707, bag.w * 0.3 * remainder, bag.h * 0.025))
        Ff.display_text(screen, "Exp", 1, (bag.w * 0.58, bag.h * 0.71), "black")


    return bag

def get_backpack_coordinates(screen, word):
    rect = screen.get_rect()
    bag = Ff.add_image_to_screen(screen, S.PLAYING_PATH["Backpack_Empty_" + word],[rect.center[0] * 0.5, rect.center[1] * 0.25, S.SCREEN_WIDTH / 2,S.SCREEN_HEIGHT * 0.75])
    if I.info.BACKPACK_COORDINATES_X == {}:
        I.info.BACKPACK_COORDINATES_X, I.info.BACKPACK_COORDINATES_Y = bag_coordinates(screen, bag)

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
                screen.set_at((left, top), (0,0,0,255))
                # I.T.pause_pygame()
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
            if color1 == (204, 130, 98, 255):
                cube += 1
                while color1 == (204, 130, 98, 255):
                    top += 1
                    color1 = screen.get_at((left, top))
                if color1 == (156, 90, 60, 255):
                    kill = True

    return (coordinates_x, coordinates_y)

def handle_consumption(items, player, use):
    property_list = items.item_dict[use.split("|")[0]]["Properties"].split(",,,")
    for property in property_list:
        if "CONSUMABLE" in property:
            consumable = property[11:-1] # from CONSUMABLE(valuesss) gets only the values inside
    consumable = consumable.split(",,")
    for consume in consumable:
        points, atribute = consume.split("-")
        if atribute in list(player.keys()):
            if int(player[atribute][0]) < int(player[atribute][1]):
                if "/" in points:
                    points = points[1:]
                    player[atribute] = (player[atribute][0] - int(points), player[atribute][1])
                else:
                    player[atribute] = (player[atribute][0] + int(points), player[atribute][1])
                    # print(player[atribute])
                    if int(player[atribute][0]) > int(player[atribute][1]):
                        player[atribute] = player[atribute][1], player[atribute][1]
            elif player[atribute][0] >= player[atribute][1]:
                if "/" in points:
                    points = points[1:]
                    player[atribute] = (player[atribute][0] - int(points), player[atribute][1])
                else:
                    player[atribute] = (player[atribute][1], player[atribute][1])
        else:
            if "ITEM" in atribute:
                item = atribute.replace("ITEM:", "")
                amount = I.random.randint(int(points.split(":")[0]), int(points.split(":")[1]))
                Ff.add_to_backpack(item, amount, items)
    value = I.info.BACKPACK_CONTENT[use]
    if value[0] > 1:
        I.info.BACKPACK_CONTENT[use] = (value[0] - 1, value[1], value[2])
    else:
        del I.info.BACKPACK_CONTENT[use]

def get_equipment_coordinates(block):
    coordinates = {
        (-2, 0): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.12),
        (-2, 2): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.17),
        (-2, 4): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.21),
        (-2, 6): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.24),
        (-2, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.90,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-4, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.82,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-6, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.74,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-8, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.66,
                  list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-10, 8): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.27),
        (-10, 6): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.24),
        (-10, 4): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.21),
        (-10, 2): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.17),
        (-10, 0): (list(I.info.BACKPACK_COORDINATES_X.values())[0] * 0.576,
                   list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]] * 1.12),
    }
    return coordinates

def update_equiped():
    if I.info.BACKPACK_CONTENT == {}:
        for option in I.info.EQUIPED.keys():
            I.info.EQUIPED[option] = 0, I.info.EQUIPED[option][1]
    else:
        if I.info.APPLIANCE_CLICK != [""] and len(I.info.APPLIANCE_CLICK) == 4:
            """if appliance is selected and its not melter item placed (cuz it only has one member)"""
            if I.info.APPLIANCE_CLICK[3] in ["cook", "burn", "smelt"]:
                for key in I.info.EQUIPED.keys():
                    if I.info.EQUIPED[key][0] == I.info.APPLIANCE_CLICK[1]:
                        if I.info.BACKPACK_CONTENT.get(I.info.APPLIANCE_CLICK[1]) == None:
                            I.info.EQUIPED[key] = 0, I.info.EQUIPED[key][1]
        else:
            for item, (amount, posx, posy) in I.info.BACKPACK_CONTENT.items():
                if posx < 0:
                    I.info.EQUIPED[I.info.equipment[(posx, posy)]] = item, I.info.EQUIPED[I.info.equipment[(posx, posy)]][1]


    for key, item in I.info.EQUIPED.items():
        if I.info.BACKPACK_CONTENT.get(item[0]) == None:
            I.info.EQUIPED[key] = 0, I.info.EQUIPED[key][1]

def key_press_get_block(event, block, right_limit, bottom_limit, case):
    if event.key == I.pg.K_UP:
        block = (block[0], block[1] - 2)
        if block[1] < 0:
            block = (block[0], bottom_limit)

    elif event.key == I.pg.K_DOWN:
        block = (block[0], block[1] + 2)
        if block[1] > bottom_limit:
            block = (block[0], 0)
    elif event.key == I.pg.K_LEFT:
        block = (block[0] - 2, block[1])
        if case == "not backpack" and block[0] < 0:
            block = (right_limit, block[1])
    elif event.key == I.pg.K_RIGHT:
        block = (block[0] + 2, block[1])
        if block[0] > right_limit and case not in ["build station"]:
            block = (0, block[1])
    return block