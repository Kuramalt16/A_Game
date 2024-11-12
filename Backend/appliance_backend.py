from distutils.command.build import build

from select import select

from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S



def handle_appliances(items, screen, gifs, data, decorations, rooms, collide):
    appliance_name = collide[0]
    item = I.info.EQUIPED["Sword"][0]
    item_dict = items.item_dict
    if item != 0 and len(I.info.APPLIANCE_CLICK) != 4 and appliance_name in ["Furnace", "Blast Furnace", "Potion_stand", "Melter", "Anvil"]:
        if "COOK" in item_dict[item.split("|")[0]]["Properties"] and appliance_name == "Furnace": # checks if the chosen item can be cooked or smelted else burn it
            I.info.APPLIANCE_CLICK = [appliance_name, item.split("|")[0], 1, "cook"]
            # I.pg.time.set_timer(I.pg.USEREVENT + 7, 3000)  # Set timer for the appliance
            gifs["Furnace"].Start_gif("Furnace", 1)
            I.th.start_thread(3000, "cook", (items, rooms, data))
            Ff.remove_from_backpack(item, 1)  # removes the item
        elif "SMELT" in item_dict[item.split("|")[0]]["Properties"] and appliance_name == "Blast Furnace":
            I.info.APPLIANCE_CLICK = [appliance_name, item.split("|")[0], 1, "smelt"]
            if I.info.BACKPACK_CONTENT[item][0] >= 2:
                Ff.remove_from_backpack(item, 2)  # removes the item
                # I.pg.time.set_timer(I.pg.USEREVENT + 7, 2800)  # Set timer for the appliance
                gifs["Blast Furnace"].Start_gif("Blast Furnace", 1)
                I.th.start_thread(3000, "cook", (items, rooms, data))

                # I.pg.time.set_timer(I.pg.USEREVENT + 7, 10000)  # Set timer for the appliance
            else:
                Ff.display_text_player("Not enough material to smelt", 3000)
                I.info.APPLIANCE_CLICK = [""] # didnt have enough items
        elif "MELTER_FILL" in item_dict[item.split("|")[0]]["Properties"] and appliance_name == "Melter":
            handle_melter("Place", decorations, items, rooms, data, gifs)
        elif "MELT" in item_dict[item.split("|")[0]]["Properties"] and appliance_name == "Melter":
            handle_melter("Melt", decorations, items, rooms, data, gifs)
        elif appliance_name == "Furnace":
            I.info.APPLIANCE_CLICK = [appliance_name, item.split("|")[0], 1, "burn"]
            # I.pg.time.set_timer(I.pg.USEREVENT + 7, 3000)  # Set timer for the appliance
            I.th.start_thread(3200, "cook", items)

            Ff.remove_from_backpack(item, 1)  # removes the item
        elif appliance_name == "Blast Furnace":
            Ff.display_text_player(str(item.split("|"[0].replace("0", "").replace("1",""))[0]) + " can not be smelt", 3000)
        elif appliance_name == "Potion_stand":
            if "Potion_Empty" in I.info.EQUIPED["Sword"][0] and I.info.EQUIPED["Sword"][0] not in rooms.decor:
                rect = I.pg.Rect(decorations.decor_dict[appliance_name][0]["rect"].x + decorations.decor_dict[appliance_name][0]["rect"].w / 3, 90, 10, 20)
                Ff.update_map_view(0, I.info.EQUIPED["Sword"][0], rect, "add", 0)
                Ff.remove_from_backpack(I.info.EQUIPED["Sword"][0], 1)
            elif "Potion_Empty" in rooms.decor:
                handle_potion_making(screen, items, data, decorations, rooms)
            else:
                Ff.display_text_player("Place empty potion bottle", 5000)
        elif appliance_name == "Anvil":
            handle_anvil(screen, items, decorations, collide)
        # elif appliance_name == "Melter":
        #     handle_melter(decorations, items, rooms, data)
        else:
            print("incorrect item used with appliance ", appliance_name)
    elif appliance_name == "Grinder_Tool":
        I.TB.handle_grinder(screen, items, gifs, data, decorations)
    elif "Potion_Empty" in rooms.decor and appliance_name == "Potion_stand":
        handle_potion_making(screen, items, data, decorations, rooms)
    elif "Build station" == appliance_name:
        handle_build_station(screen, decorations, rooms, items, data)
    else:
        if appliance_name == "Potion_stand" and appliance_name == "Potion_stand":
            Ff.display_text_player("Place down an empty potion first", 5000)
        else:
            print("appliance not programed", appliance_name)

    I.BB.update_equiped()

def handle_potion_making(screen, items, data, decorations, rooms):
    potion_strength = {}
    running = True
    color = "Yellow"  # color of selected rect
    border = 1  # rect border size
    path = items.item_dict["Potion_Empty"]["path"]


    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    block = [0, 0]

    ingredient_list = []

    while running:
        screen.fill((0, 0, 0, 0))
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_ESCAPE:
                    running = False
                elif event.key == I.pg.K_DOWN:
                    block[1] += 2
                    if block[1] > 26:
                        block[1] = 0
                elif event.key == I.pg.K_UP:
                    block[1] -= 2
                    if block[1] < 0:
                        block[1] = 26
                elif event.key == I.pg.K_LEFT:
                    block[0] -= 2
                    if block[0] < 0:
                        block[0] = 14
                elif event.key == I.pg.K_RIGHT:
                    block[0] += 2
                    if block[0] > 14:
                        block[0] = 0
            elif event.type == I.pg.KEYUP:
                if event.key == I.pg.K_z and ingredient_list != []:
                    path_str_id = path.find("Potion_")
                    potion_name = path[path_str_id:].replace(".png", "")
                    path = items.item_dict["Potion_Empty"]["path"]
                    strength = potion_strength[potion_name]

                    Ff.add_to_backpack(potion_name, strength, items)

                    x = decorations.decor_dict["Potion_Empty"][0]["rect"].x
                    y = decorations.decor_dict["Potion_Empty"][0]["rect"].y
                    Ff.update_map_view(0, "Potion_Empty", (x, y), "remove")
                    rooms.decor.remove("Potion_Empty")
                    running = False
                elif event.key == I.pg.K_x:
                    for ingredient in ingredient_list:
                        Ff.add_to_backpack(ingredient, 1, items)
                    ingredient_list = []
                    path = items.item_dict["Potion_Empty"]["path"]
                elif event.key == I.pg.K_c:
                    pickup = Ff.find_item_by_slot(block[0], block[1])
                    if pickup != None and "BREWABLE" in items.item_dict[pickup.split("|")[0]]["Properties"]:
                        ingredient_list.append(pickup)
                        Ff.remove_from_backpack(pickup, 1)

                        property_list = []
                        for ingredient in ingredient_list:
                            ingredient_str_id = items.item_dict[ingredient.split("|")[0]]["Properties"].find("BREWABLE")
                            dust_properties = items.item_dict[ingredient.split("|")[0]]["Properties"][ingredient_str_id:].split(",,,")[0].split(":")
                            dust_properties.remove("BREWABLE")
                            for property in dust_properties:
                                property_list.append(I.A.POTIONS[property[:-1]])
                        if len(property_list) != 1:
                            potion_dict = {}
                            potion_str = 0
                            for property in property_list:
                                if potion_dict.get(property) == None:
                                    potion_dict[property] = 1
                                else:
                                    potion_dict[property] += 1
                            if len(potion_dict.keys()) <= 1:
                                potion_name = list(potion_dict.keys())[0]
                                potion_strength = {"Potion_" + str(potion_name): potion_dict[potion_name]}
                            else:
                                colors = []
                                for ingredient in ingredient_list:
                                    colors_name = ingredient.replace(" Dust", "")
                                    colors.append(I.A.DUST_COLORS[colors_name.split("|")[0].lower()])
                                blended_color = tuple(sum(color[i] for color in colors) // len(colors) for i in range(4))
                                blended_color = blended_color[0], blended_color[1], blended_color[2]
                                color_name = Ff.get_color_by_RGB(blended_color)
                                if color_name != -1:
                                    potion_name = "Potion_" + color_name
                                    path_str_id = path.find("Potion_")
                                    path = path[:path_str_id] + potion_name + ".png"
                                    potion_strength = {str(potion_name): 1}

                        else:
                            potion_name = "Potion_" + property_list[0]
                            potion_strength = {potion_name:1}
                            path = path.replace("Potion_Empty", potion_name)

        I.BB.display_backpack(screen, data["Player"], items, screen.get_rect(), "half")
        Ff.add_image_to_screen(screen, path, (200, 100, 200, 300))

        Ff.display_text(screen, "[Z] to mix", 20, (100, 650), "green")
        Ff.display_text(screen, "[X] to empty potion", 20, (300, 650), "red")

        rect = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]],
                         list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
        I.pg.draw.rect(screen, color, rect, border)

        I.pg.display.flip()

def handle_build_station(screen, decorations, rooms, items, data):
    running = True
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    block = (0, 0)
    craft_posisions = {}
    to_remove = []
    build_possisions = {}
    build_coordinates_x = {
        -2: 358,
        -4: 326,
        -6: 294,
        -8: 262,
        -10: 230,
        -12: 198,
    }
    build_coordinates_y = {
        4: 286,
        6: 312,
        8: 337,
        10: 363,
        12: 388,
        14: 413,
    }
    selected_item_flag = False
    ready_to_craft = False
    selected_item_rect = None
    screen_rect = screen.get_rect()
    build_station_path = decorations.decor_dict["Build station"]["path"].replace("Build station.png", "Build station_backpack.png")
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYUP:
                if event.key == I.pg.K_ESCAPE or event.key == I.pg.K_i:
                    running = False
                    for block, (item, amount) in craft_posisions.items():
                        Ff.add_to_backpack(item, amount, items)
                elif event.key == I.pg.K_c:
                    if not selected_item_flag:
                        """no item has been picked up, picking up now"""
                        selected_item_flag = True
                        if block[0] >= 0:
                            """picking up item from backpack"""
                            selected_item_rect =  I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
                            selected_item = (Ff.find_item_by_slot(block[0], block[1]), block[0], block[1])
                            if selected_item[0] == None:
                                selected_item_flag = False
                                selected_item_rect = None
                        else:
                            """picking up item from build station"""
                            selected_item_rect =  I.pg.Rect(build_coordinates_x[block[0]], build_coordinates_y[block[1]], 26, 24)
                            if craft_posisions.get(block) != None:
                                selected_item = craft_posisions[block][0], block[0], block[1]
                            else:
                                selected_item_flag = False
                                selected_item_rect = None
                    else:
                        """item has been selected moving to new spot"""
                        selected_item_flag = False
                        selected_item_rect = None
                        if block[0] < 0:
                            """if placing item down in build station"""
                            if selected_item[1] < 0:
                                """if placing from build station to build station"""
                                if craft_posisions.get(block) == None:
                                    """selected spot is free. transfer"""
                                    craft_posisions[block] = selected_item[0], 1
                                    remove_item_from_build_station(selected_item, craft_posisions)
                                else:
                                    """selected spot is ocupied."""
                                    if craft_posisions[block][0] == craft_posisions[selected_item[1:]][0]:
                                        """selected spot is occupied with the same item, adding them"""
                                        craft_posisions[block] = craft_posisions[block][0], craft_posisions[block][1] + craft_posisions[selected_item[1:]][1]
                                        remove_item_from_build_station(selected_item, craft_posisions)
                            else:
                                """if placing from backpack to build station"""
                                if craft_posisions.get(block) == None:
                                    """if item didnt exist in the build station"""
                                    craft_posisions[block] = selected_item[0], 1
                                    Ff.remove_from_backpack(selected_item[0], 1)
                                elif selected_item[0] == craft_posisions[block][0]:
                                    """if item already exists in the build station and share a name"""
                                    craft_posisions[block] = selected_item[0], craft_posisions[block][1] + 1
                                    Ff.remove_from_backpack(selected_item[0], 1)
                        else:
                            """if placing item down in backpack"""
                            if selected_item[1] >= 0:
                                """if picked up item was in backpack"""
                                if Ff.find_item_by_slot(block[0], block[1]) == None:
                                    place_item_in_unused_spot_inbackpack(block, selected_item[0])
                                else:
                                    switch_item_spots_inbackpack(block, selected_item[0], items)
                            else:
                                """if picked up item was in build station"""
                                is_spot_free = Ff.find_item_by_slot(block[0], block[1])
                                if is_spot_free == None:
                                    Ff.add_to_backpack(selected_item[0], 1, items, block[0], block[1])
                                    # amount, old_x, old_y = I.info.BACKPACK_CONTENT[selected_item[0]]
                                    # I.info.BACKPACK_CONTENT[selected_item[0]] = 1 + amount, block[0], block[1]
                                    remove_item_from_build_station(selected_item, craft_posisions)
                                elif is_spot_free == selected_item[0]:
                                    amount, old_x, old_y = I.info.BACKPACK_CONTENT[selected_item[0]]
                                    I.info.BACKPACK_CONTENT[selected_item[0]] = amount + 1, block[0], block[1]
                                    remove_item_from_build_station(selected_item, craft_posisions)
                elif event.key == I.pg.K_x:
                    if ready_to_craft != None:
                        selected_item_flag = None
                        selected_item_rect = None
                        Ff.add_to_backpack(ready_to_craft[0], ready_to_craft[1], items)
                        for block, (item, amount) in craft_posisions.items():
                            to_remove.append((block, item))
                        for block, item in to_remove:
                            remove_item_from_build_station((item, block[0], block[1]), craft_posisions)
                        to_remove = []
                        ready_to_craft = None
                elif event.key == I.pg.K_z:
                    if selected_item_flag and block[0] < 0 and I.info.BACKPACK_CONTENT.get(selected_item[0]) != None:
                        """if item is selected and dropping into build station and the selected item is not 0"""
                        if craft_posisions.get(block) == None:
                            """if spot in build station is free"""
                            craft_posisions[block] = selected_item[0], 1
                            Ff.remove_from_backpack(selected_item[0], 1)
                        elif selected_item[0] == craft_posisions[block][0]:
                            """if spot in build station is not free and shares the name"""
                            craft_posisions[block] = selected_item[0], 1 + craft_posisions[block][1]
                            Ff.remove_from_backpack(selected_item[0], 1)
                    if selected_item_flag and I.info.BACKPACK_CONTENT.get(selected_item[0]) == None:
                        selected_item_flag = None
                        selected_item_rect = None
                        selected_item = None
                    elif not selected_item_flag and block[0] < 0 and craft_posisions.get(block) != None:
                        item_name, amount = craft_posisions[block]
                        Ff.add_to_backpack(item_name, 1, items)
                        remove_item_from_build_station((item_name, block[0], block[1]), craft_posisions)

                block = I.BB.key_press_get_block(event, block, 14, 26, "build station")
                if block[0] < -12:
                    block = 14, block[1]
                if block[0] > 14:
                    block = -12, block[1]
        Ff.add_image_to_screen(screen, build_station_path, screen_rect)
        I.BB.display_backpack(screen, data["Player"], items, screen_rect, "half")
        if block[0] >= 0:
            """in backpack"""
            selection_rect = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
        else:
            """in build station"""
            """making sure entering from backpack to build station doesn't crash"""
            if block[1] < 4:
                block = block[0], 4
            if block[1] > 14:
                block = block[0], 14

            """making sure in build station that going up over limit returns to bottom"""

            selection_rect = I.pg.Rect(build_coordinates_x[block[0]], build_coordinates_y[block[1]], item_w-1, item_h-1)
        handle_building(screen, craft_posisions, items, build_coordinates_x, build_coordinates_y, build_possisions)
        build_possisions = push_everything_incrafting(build_possisions)

        ready_to_craft = check_if_buildable_incrafting(build_possisions, screen, items)
        build_possisions = {}

        Ff.display_text(screen, "[X] to build", 24, (100, 630), "green")
        I.pg.draw.rect(screen, "yellow", selection_rect, 1)

        if selected_item_rect != None:
            I.pg.draw.rect(screen, "yellow", selected_item_rect, 2)

        I.pg.display.flip()

def handle_anvil(screen, items, decorations, collide):
    rect = collide[1]
    id = collide[2]
    crushable_items = Ff.get_property(I.info.EQUIPED["Sword"][0], items, "ANVIL")
    if "Blunt" not in crushable_items and decorations.decor_dict["Anvil"][id]["effect"] == "":
        Ff.update_map_view(id, I.info.EQUIPED["Sword"][0], (rect.x + 10, rect.y - 20, 30, 30), "add_bypassed")
        decorations.decor_dict["Anvil"][id]["effect"] = "PLACED:" + str(I.info.EQUIPED["Sword"][0])
        Ff.remove_from_backpack(I.info.EQUIPED["Sword"][0], 1)
    elif decorations.decor_dict["Anvil"][id]["effect"] == "":
        Ff.display_text_player("item can not be used on the anvil", 5000)
    else:
        Ff.display_text_player("item already placed on the anvil", 5000)

def get_smelted_item(item_name, items):
    probabilities, outcomes = Ff.get_property(item_name, items, "SMELT")
    item = I.random.choices(outcomes, probabilities)[0]
    return item

def handle_cooking_food(items, rooms, data):
    """comes here after the gif ends"""
    if I.info.APPLIANCE_CLICK[0] == "Furnace":
        I.info.APPLIANCE_CLICK[0] = ""
        if I.info.APPLIANCE_CLICK[3] == "cook":
            I.IB.add_dropped_items_to_var(I.info.APPLIANCE_CLICK[1] + "_Cooked", 1, rooms, (980,100), data, "decor")
            if any(char.isdigit() for char in I.info.APPLIANCE_CLICK[1]):  # if name has a number. like Meat1 or Meat0
                I.info.APPLIANCE_CLICK[1] = I.info.APPLIANCE_CLICK[1][:-1]
            Ff.display_text_player("Cooked " + I.info.APPLIANCE_CLICK[1], 5000)
        else:
            I.IB.add_dropped_items_to_var("Ashes", 1, rooms, (980,100), data, "decor")
            Ff.display_text_player("Burned " + I.info.APPLIANCE_CLICK[1], 3000)
    elif I.info.APPLIANCE_CLICK[0] == "Blast Furnace":
        I.info.APPLIANCE_CLICK[0] = ""
        if I.info.APPLIANCE_CLICK[3] == "smelt":
            item = get_smelted_item(I.info.APPLIANCE_CLICK[1], items)
            I.IB.add_dropped_items_to_var(item, 1, rooms, (980,200), data, "decor")

            Ff.display_text_player("Smelted " + I.info.APPLIANCE_CLICK[1], 5000)
        # else:
        #     Ff.display_text_player("This item can not be smelted", 5000)
    elif I.info.APPLIANCE_CLICK[0] == "Melter":
        decorations = items[1]
        items = items[0]
        I.info.APPLIANCE_CLICK[0] = ""
        if I.info.APPLIANCE_CLICK[3] == "melt":
            coordinates = decorations.decor_dict[I.info.APPLIANCE_CLICK[1].split(":")[0].split(" ")[-1]][0]["rect"]
            Ff.update_map_view(0, I.info.APPLIANCE_CLICK[1].split(":")[0].split(" ")[-1], (coordinates.x, coordinates.y), "remove")
            item = get_melted_item(I.info.APPLIANCE_CLICK[1], items)
            I.IB.add_dropped_items_to_var(I.info.APPLIANCE_CLICK[1].split(":")[0], 1, rooms, (coordinates.x,coordinates.y + 20), data, "decor")
            I.IB.add_dropped_items_to_var(item, 1, rooms, (coordinates.x,coordinates.y + 20), data, "decor")

            Ff.display_text_player("Melted " + I.info.APPLIANCE_CLICK[1].split(":")[1], 5000)
    I.info.APPLIANCE_CLICK = [""]

def place_item_in_unused_spot_inbackpack(new_spot, item_name):
    amount, current_x, current_y = I.info.BACKPACK_CONTENT[item_name]
    I.info.BACKPACK_CONTENT[item_name] = amount, new_spot[0], new_spot[1]

def switch_item_spots_inbackpack(selected_spot, selected_item, items):
    amount1, old_x, old_y = I.info.BACKPACK_CONTENT[selected_item]
    taken_spot_item_name = Ff.find_item_by_slot(selected_spot[0], selected_spot[1])
    if "STACK" in taken_spot_item_name and "STACK" in selected_item and taken_spot_item_name.split("|")[0] == selected_item.split("|")[0] and taken_spot_item_name != selected_item:
        """both items are stacks and of the same name"""
        merge_two_stacks(taken_spot_item_name, selected_item, selected_spot, items)
    else:
        amount2, x, y = I.info.BACKPACK_CONTENT[taken_spot_item_name]
        I.info.BACKPACK_CONTENT[taken_spot_item_name] = amount2, old_x, old_y
        I.info.BACKPACK_CONTENT[selected_item] = amount1, selected_spot[0], selected_spot[1]

def merge_two_stacks(taken_spot_item_name, selected_item, new_spot, items):
    stack = Ff.get_property(taken_spot_item_name.split("|")[0], items, "STACK")
    amount1 = I.info.BACKPACK_CONTENT[taken_spot_item_name][0]
    amount2 = I.info.BACKPACK_CONTENT[selected_item][0]
    if amount1 + amount2 <= stack:
        """merging two items into one"""
        I.info.BACKPACK_CONTENT[taken_spot_item_name] = amount1 + amount2, new_spot[0], new_spot[1]
        del I.info.BACKPACK_CONTENT[selected_item]
    else:
        """can not merge two items into one, calculating with remainder"""
        if amount1 < stack and amount2 < stack:
            """it's possible to combine and leave a remainder"""
            remainder = stack - amount1 + amount2
            I.info.BACKPACK_CONTENT[taken_spot_item_name] = stack, I.info.BACKPACK_CONTENT[taken_spot_item_name][1], I.info.BACKPACK_CONTENT[taken_spot_item_name][2]
            I.info.BACKPACK_CONTENT[selected_item] = remainder, I.info.BACKPACK_CONTENT[selected_item][1], I.info.BACKPACK_CONTENT[selected_item][2]
        else:
            """one of the stacks is full changing the stack possisions"""
            amount2, x, y = I.info.BACKPACK_CONTENT[taken_spot_item_name]
            amount1, old_x, old_y = I.info.BACKPACK_CONTENT[selected_item]

            I.info.BACKPACK_CONTENT[taken_spot_item_name] = amount2, old_x, old_y
            I.info.BACKPACK_CONTENT[selected_item] = amount1, new_spot[0], new_spot[1]

def handle_building(screen, craft_posisions, items, coordinates_x, coordinates_y, build_possisions):
    for (block_x, block_y), (item, amount) in craft_posisions.items():
        build_possisions[(block_x, block_y)] = item
        path = items.item_dict[item.split("|")[0]]["path"]
        Ff.add_image_to_screen(screen, path, (coordinates_x[block_x], coordinates_y[block_y], 26, 24))
        Ff.display_text(screen, str(amount), 1, (coordinates_x[block_x], coordinates_y[block_y]), "white")

def remove_item_from_build_station(selected_item, craft_posisions):
    if craft_posisions[selected_item[1:]][1] == 1:
        del craft_posisions[selected_item[1:]]
    else:
        item_name, amount = craft_posisions[selected_item[1:]]
        craft_posisions[selected_item[1:]] = item_name, amount - 1
    return craft_posisions

def push_everything_incrafting(build_possisions):
    if build_possisions != {}:
        new_build_possisions = {}
        leftest_x = max(list(build_possisions.keys()), key=lambda x: x[0])[0]
        uppest_y = min(list(build_possisions.keys()), key=lambda x: x[1])[1]
        remainder_x = -2 - leftest_x
        remainder_y = uppest_y - 4
        for (block_x, block_y), item in build_possisions.items():
            new_x = block_x + remainder_x
            new_y = block_y - remainder_y
            new_build_possisions[(new_x, new_y)] = item.split("|")[0]
        build_possisions = new_build_possisions
    return build_possisions
    # for (block_x, block_y), item in build_possisions:

def check_if_buildable_incrafting(built_pattern, screen, items):
    for item_name, pattern in I.A.CRAFTING_DICT.items():
        if built_pattern == pattern:
            amount = 1
            if "**" in item_name:
                amount, item_name = item_name.split("**")
                amount = int(amount)
            Ff.add_image_to_screen(screen, items.item_dict[item_name]["path"], (545, 330, 40, 40))
            return item_name, amount

def handle_melter(case, decorations, items, rooms, data, gifs):
    if case == "Place":
        """Places item down"""
        item = I.info.EQUIPED["Sword"][0].split("|")[0].split(" ")[-1]
        I.info.APPLIANCE_CLICK = ["", I.info.EQUIPED["Sword"][0].split("|")[0]]
        Ff.update_map_view(0, item, (652, 178, 40, 40), "add")
        Ff.remove_from_backpack(I.info.EQUIPED["Sword"][0].split("|")[0], 1)  # removes the item
    elif case == "Melt":
        if len(I.info.APPLIANCE_CLICK) == 2 and I.info.APPLIANCE_CLICK[1] != "":
            if I.info.BACKPACK_CONTENT[I.info.EQUIPED["Sword"][0]][0] >= 3:
                I.info.APPLIANCE_CLICK = ["Melter", I.info.APPLIANCE_CLICK[1] + ":" + I.info.EQUIPED["Sword"][0].split("|")[0], 1, "melt"]
                gifs["Melter"].Start_gif("Melter", 1)
                Ff.remove_from_backpack(I.info.EQUIPED["Sword"][0], 3)
                I.th.start_thread(2000, "cook", ((items, decorations), rooms, data))
            else:
                Ff.display_text_player("Not enough material", 5000)
        else:
            Ff.display_text_player("Place an item to collect the molten material", 3000)

def get_melted_item(item_name, items):
    casing = item_name.split(":")[0]
    item_name = item_name.split(":")[1]
    # print(casing, item_name)
    find_id = items.item_dict[casing]["Properties"].find("CAST:")
    melted_item = items.item_dict[casing]["Properties"][find_id:].split(",,,")[0].replace("CAST:", "")
    if item_name == "Sand":
        item_name = "Glass"
    print(item_name + " " + melted_item)
    return item_name + " " + melted_item
