from PIL.Image import blend
from PIL.ImagePalette import random

from Values import Settings as S
from utils import Imports as I, Frequent_functions as Ff

def handle_hoe(collide, data, items, decorations, screen, rooms):
    """Handles checking if there are no decorations near by and placing seed beds"""
    if collide == [False]:
        hoe_location = [weapon[0] != 0 and "Hoe" in weapon[0] for weapon in I.info.EQUIPED.values()]
        if True in hoe_location:
            pressed_button = [button[0] != 0 for button in [I.info.COMBAT_RECT, I.info.AXE, I.info.PICAXE]]
            if True in pressed_button:
                location = 10
                for i in range(3):
                    if pressed_button[i] == hoe_location[i] and pressed_button[i]:
                        location = i
                if location == 10:
                    return
                rects = {"Sword": I.info.COMBAT_RECT, "Axe": I.info.AXE, "Picaxe": I.info.PICAXE}
                speed = float(Ff.get_property(I.info.EQUIPED[list(rects.keys())[location]][0].split("|")[0], items, "WEAPON")[1])
                if list(rects.values())[location][1] in range(int(speed * I.info.BASE_ATTACKING_SPEED - 19), int(speed * I.info.BASE_ATTACKING_SPEED+1)):
                    type = I.info.EQUIPED[list(rects.keys())[location]][0].split("|")[0].split(" ")[0]
                    # if type == "Wooden":
                    #     amount = 5
                    # elif type == "Stone":
                    #     amount = 10
                    orientation = {
                        "Front.png": (0, 1),
                        "Back.png": (0, -1),
                        "Left.png": (-1, 0),
                        "Right.png": (1, 0)
                    }
                    xy = (list(rects.values())[location][0].x * 4 + orientation[I.info.LAST_ORIENT[0]][0] * 20, list(rects.values())[location][0].y * 4 + orientation[I.info.LAST_ORIENT[0]][1] * 20)
                    plantable_color = (137, 176, 46, 255)
                    if screen.get_at(xy) == plantable_color and screen.get_at((xy[0] + 55, xy[1] + 55)) == plantable_color:
                        rects[list(rects.keys())[location]][1] -= 1
                        if list(rects.values())[location][1] == speed * I.info.BASE_ATTACKING_SPEED - 20:
                            xy = data["Zoom_rect"].x + 145 + orientation[I.info.LAST_ORIENT[0]][0] * 20, data["Zoom_rect"].y + 82 + orientation[I.info.LAST_ORIENT[0]][1] * 20
                            xy = tuple(round(num / 10) * 10 for num in xy)
                            count = Ff.update_map_view(0, "Plant bed", xy, "get")
                            if count < 20:
                                image_rect = I.pg.image.load(decorations.decor_dict["Plant bed"]["path"]).get_rect()
                                if I.info.MAP_CHANGE[rooms.name]["add"].get("Plant bed") == None or I.info.MAP_CHANGE[rooms.name]["add"]["Plant bed"].get(count) == None:
                                    """if the id doesn't exist already, plant it."""
                                    Ff.update_map_view(count, "Plant bed", (xy[0], xy[1], image_rect.w, image_rect.h), "add")
                                    Ff.update_map_view(count, "Plant bed", "NoPLANT", "add_effect")
                                    data["Player"]["stats"]["Farming"] = data["Player"]["stats"]["Farming"] + 10
                                else:
                                    """if the id matches the count of the item"""
                                    for i in range(0, 30):
                                        if I.info.MAP_CHANGE[rooms.name]["add"]["Plant bed"].get(i) == None:
                                            Ff.update_map_view(i, "Plant bed", (xy[0], xy[1], image_rect.w, image_rect.h), "add")
                                            Ff.update_map_view(i, "Plant bed", "NoPLANT", "add_effect")
                                            data["Player"]["stats"]["Farming"] = data["Player"]["stats"]["Farming"] + 10
                                            break
                            else:
                                Ff.display_text_player("Maximum amount of seed beds", 3000)

def handle_axe_chopping(decor_rect, decor_name, decor_dict, id, items, gifs, data):
    """Handles checking if an axe is being used by the player, tree health reducing, displaying chopped tree"""
    if I.info.AXE[0] != 0 or I.info.PICAXE[0] != 0 or I.info.COMBAT_RECT[0] != 0:
        """ Button was pressed [X], [V] or [B] """
        rects = {"Sword": I.info.COMBAT_RECT, "Axe": I.info.AXE, "Picaxe": I.info.PICAXE}
        axe_location = [weapon[0] != 0 and "Axe" in weapon[0] for weapon in I.info.EQUIPED.values()]
        pressed_button = [button[0] != 0 for button in rects.values()]
        location = 10
        for i in range(len(axe_location)):
            """Axe locations is a list of three bool values, if the value is true then an item with "Axe" is there
            if pressed_button is a list of three bool values, if the value is true then the button was pressed, [X][V][B]"""
            if axe_location[i]:
                if axe_location[i] == pressed_button[i]:
                    """Found the button pressed"""
                    location = i
        if location == 10:
            return
        speed = float(Ff.get_property(I.info.EQUIPED[list(rects.keys())[location]][0].split("|")[0], items, "WEAPON")[1])

        if list(rects.values())[location][0].colliderect(decor_rect) and list(rects.values())[location][1] == speed * I.info.BASE_ATTACKING_SPEED:
            """axe collided with an object the 1000 is used for speed"""
            type = I.info.EQUIPED[list(rects.keys())[location]][0].split("|")[0].split(" ")[0]
            print("here")
            I.MB.check_if_mob_spawns(decor_name, decor_dict, id, gifs, decor_rect, data)

            if type == "Wooden":
                choppable = ["Tree_T_1"]
                damage = 1
            elif type == "Iron":
                choppable = ["Tree_T_1", "Tree_M_1", "Tree_M_2", "Tree_M_3", "Tree_M_4", "Tree_M_5", "Ent", "Tree_M_1_Harvested"]
                damage = 2

            if decor_name in choppable:
                bool_var, health = decor_dict[decor_name][id]["health"].split(",,")
                health = int(health.split(",")[0]) - damage
                rects[list(rects.keys())[location]][1] -= 1 # it is no longer 1000 so it wont be comming back here for a second time
                if health < 0:
                    health = 0
                elif health < float(decor_dict[decor_name][id]["health"].split(",,")[1].split(",")[1]) / 2: # change texture once half is chopped off.
                    path = decor_dict[decor_name]["path"]
                    path_list = path.split(decor_name)
                    path = path_list[0] + decor_name + "_Chop" + path_list[1]
                    image = I.pg.image.load(path)
                    decor_dict[decor_name][id]["image"] = image


                decor_dict[decor_name][id]["health"] = bool_var + ",," + str(health) + "," + decor_dict[decor_name][id]["health"].split(",,")[1].split(",")[1] # Removes 1 hp from wood. later change to amount of damage axe does

def handle_picaxe_chopping(decor_rect, decor_name, decor_dict, id, items):
    """Handles checking if an picaxe is being used by the player, stone health reducing, displaying chopped stone"""
    if I.info.AXE[0] != 0 or I.info.PICAXE[0] != 0 or I.info.COMBAT_RECT[0] != 0:
        location, rects = get_tool_location_in_equiped("Picaxe")
        if location == None:
            return

        speed = float(Ff.get_property(I.info.EQUIPED[list(rects.keys())[location]][0].split("|")[0], items, "WEAPON")[1])
        if list(rects.values())[location][0].colliderect(decor_rect) and list(rects.values())[location][1] == speed * I.info.BASE_ATTACKING_SPEED:
                """Picaxe collided with an object the 1000 is used for something"""
                type = I.info.EQUIPED[list(rects.keys())[location]][0].split("|")[0].split(" ")[0]
                if type == "Wooden":
                    breakable = ["Stone_T_1"]
                    damage = 1
                elif type == "Iron":
                    breakable = ["Stone_T_1", "Stone_S_1"]
                    damage = 2
                if decor_name in breakable:
                    bool_var, health = decor_dict[decor_name][id]["health"].split(",,")
                    health = int(health.split(",")[0]) - damage
                    rects[list(rects.keys())[location]][1] -= 1 # it is no longer 1000 so it wont be comming back here for a second time
                    if health < 0:
                        health = 0
                    elif health < float(decor_dict[decor_name][id]["health"].split(",,")[1].split(",")[1]) / 2: # change texture once half is chopped off.
                        path = decor_dict[decor_name]["path"]
                        path_list = path.split(decor_name)
                        path = path_list[0] + decor_name + "_Chop" + path_list[1]
                        image = I.pg.image.load(path)
                        decor_dict[decor_name][id]["image"] = image


                    decor_dict[decor_name][id]["health"] = bool_var + ",," + str(health) + "," + decor_dict[decor_name][id]["health"].split(",,")[1].split(",")[1] # Removes 1 hp from wood. later change to amount of damage axe does

def handle_axe_rewards(decorations, tree_name, items, rooms, data, id):

    if "Fire" not in decorations.decor_dict[tree_name][id]["effect"]:
        if "PICAXE" in decorations.decor_dict[tree_name]["action"]:
            action_list = decorations.decor_dict[tree_name]["action"].split(",,")
            for action in action_list:
                if "PICAXE" in action:
                    action = action[7:]
                    possible_rewards = action.split(",")
                    loot_list = []
                    amount_list = []
                    exp = decorations.decor_dict[tree_name]["health"].split(",,")[1][0]
                    data["Player"]["stats"]["Mining"] = int(data["Player"]["stats"]["Mining"]) + int(exp)
                    for reward in possible_rewards:
                        loot, chance_min, chance_max = reward.split(":")
                        amount = int(I.random.uniform(float(chance_min), float(chance_max)))
                        if amount != 0:
                            loot_list.append(loot)
                            amount_list.append(amount)

        elif "AXE" in decorations.decor_dict[tree_name]["action"]:
            action_list = decorations.decor_dict[tree_name]["action"].split(",,")
            for action in action_list:
                if "AXE" in action:
                    action = action[4:]
                    possible_rewards = action.split(",")
                    loot_list = []
                    amount_list = []
                    exp = decorations.decor_dict[tree_name]["health"].split(",,")[1][0]
                    data["Player"]["stats"]["Felling"] = int(data["Player"]["stats"]["Felling"]) + int(exp)
                    for reward in possible_rewards:
                        if len(reward.split(":")) == 3:
                            loot, chance_min, chance_max = reward.split(":")
                            amount = int(I.random.uniform(float(chance_min), float(chance_max)))
                            if amount != 0:
                                loot_list.append(loot)
                                amount_list.append(amount)

        for i in range(0, len(loot_list)):
            I.IB.add_dropped_items_to_var(loot_list[i], amount_list[i], rooms, (decorations.decor_dict[tree_name][id]["rect"][0], decorations.decor_dict[tree_name][id]["rect"][1]), data, "tree")
            # Ff.display_text_player("Acquired " + str(amount_list[i]) + " " + loot_list[i], 5000)
    else:
        amount = I.random.randint(0, 5)
        I.IB.add_dropped_items_to_var("Ashes", amount, rooms, decorations.decor_dict[tree_name][id]["rect"], data,"tree")


def handle_unlocking_door(difficulty, door, screen, clock, decorations, data):
    """Checking if the player has any lockpicks or this key"""
    door_name = door[0]
    door_id = door[2]
    if I.info.BACKPACK_CONTENT.get(door_name + "_key") != None:
        # print(I.info.BACKPACK_CONTENT[door_name + "_key"])
        pass
    elif I.info.BACKPACK_CONTENT.get("Lockpick") != None:
        dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))
        screen.blit(dim_surface, (0, 0))
        unlocked = handle_lockpick_game(difficulty, screen, clock)
        if unlocked == True:
            decorations.decor_dict[door_name][door_id]["effect"] = "UNLOCKED"
            data["Player"]["stats"]["Lockpicking"] = int(data["Player"]["stats"]["Lockpicking"]) + difficulty * 10
    else:
        Ff.display_text_player("Door is locked", 3000)

def handle_lockpick_game(difficulty, screen, clock):
    break_pick_dict = {10: [2, 2],
                       8: [3, 2],
                       6: [4, 4],
                       4: [4, 4],
                       2: [5, 4]
                       }

    running = True
    unlocked = False
    pick_break = break_pick_dict[difficulty][0]
    tolerance = break_pick_dict[difficulty][1]
    rotation = 0
    rotation_up_down = 0
    lock_width = 600
    lock_height = 600
    unlock_step = 0
    disp_text = [0, "*CLICK*"]
    unlock_flag = False
    rotation_max = False

    lock_path = "static/images/Playing/Lock/"
    lock_img = I.pg.image.load(lock_path + "Lock_0.png")
    hook_img = I.pg.image.load(lock_path + "Hook.png")
    hook_img_left = I.pg.transform.flip(hook_img, 1, 0)
    hook_img_right = I.pg.image.load(lock_path + "Hook.png")

    pick_img = I.pg.image.load(lock_path + "Pick.png")
    pick_broke_img = I.pg.image.load(lock_path + "Pick Broken.png")

    pick_unlock_values = []
    for i in range(difficulty):
        pick_unlock_value = I.random.randrange(4, 90, 2)
        pick_unlock_values.append(pick_unlock_value)


    while running:
        I.pg.event.get()
        keys = I.pg.key.get_pressed()
        if keys[I.pg.K_ESCAPE] or keys[I.pg.K_x]:
            running = False
        if disp_text[1] != "*Lockpick Broke*":
            if keys[I.pg.K_LEFT] or keys[I.pg.K_RIGHT]:
                display_hook = True
                if keys[I.pg.K_LEFT]:
                    hook_img = hook_img_left
                    rotation += 3
                    if rotation > 10:
                        rotation = 10
                if keys[I.pg.K_RIGHT]:
                    hook_img = hook_img_right
                    rotation -= 3
                    if rotation < int((unlock_step + 1) * -90 / difficulty):
                        rotation = int((unlock_step + 1) * -90 / difficulty)
                        rotation_max = True
                    else:
                        rotation_max = False
            else:
                display_hook = False
                if rotation in range(-3, 3):
                    rotation = 0
                if rotation > 0:
                    rotation -= 2
                elif rotation < 0:
                    rotation += 2

            if keys[I.pg.K_DOWN] or keys[I.pg.K_UP]:
                if keys[I.pg.K_DOWN]:
                    if rotation_up_down in range(pick_unlock_values[unlock_step] - tolerance, pick_unlock_values[unlock_step] + tolerance) and rotation_max:
                        unlock_flag = True
                    else:
                        unlock_flag = False
                    if unlock_flag:
                        rotation_up_down += 1
                    else:
                        rotation_up_down += 2
                    if rotation_up_down > 90:
                        rotation_up_down = 90
                if keys[I.pg.K_UP]:
                    if unlock_flag:
                        unlock_step += 1
                        disp_text = [5, "*CLICK*"]
                        unlock_flag = False
                        if unlock_step == difficulty:
                            running = False
                            unlocked = True
                            Ff.display_text_player("*Lock clicks*", 5000)
                    elif rotation_max:
                        pick_break -= 1
                        if pick_break == 0:
                            pick_img = pick_broke_img
                            disp_text = [5, "*Lockpick Broke*"]
                            Ff.remove_from_backpack("Lockpick", 1)
                            pick_break = break_pick_dict[difficulty][0]
                            rotation = 0
                            rotation_up_down = 0
            else:
                if rotation_up_down in range(-3, 3):
                    rotation_up_down = 0
                if rotation_up_down > 0:
                    rotation_up_down -= 4
                elif rotation_up_down < 0:
                    rotation_up_down += 4

        screen.fill("black")
        lock_img_resized = I.pg.transform.scale(lock_img, (lock_width, lock_height))
        lock_img_rotated = I.pg.transform.rotate(lock_img_resized, rotation)
        rotated_rect = lock_img_rotated.get_rect(center=(300 + lock_width // 2, 50 + lock_height // 2))
        screen.blit(lock_img_rotated, rotated_rect.topleft)

        Ff.add_image_to_screen(screen, lock_path + "Lock_1_wood.png", (300, 50, 600, 600))

        if display_hook:
            hook_img_resized = I.pg.transform.scale(hook_img, (lock_width, lock_height))
            hook_img_rotated = I.pg.transform.rotate(hook_img_resized, rotation)
            rotated_rect = hook_img_rotated.get_rect(center=(300 + lock_width // 2, 50 + lock_height // 2))
            screen.blit(hook_img_rotated, rotated_rect.topleft)

        pick_img_resized = I.pg.transform.scale(pick_img, (lock_width, lock_height))
        pick_img_rotated = I.pg.transform.rotate(pick_img_resized, rotation_up_down)
        rotated_rect = pick_img_rotated.get_rect(center=(300 + lock_width // 2, 50 + lock_height // 2))
        screen.blit(pick_img_rotated, rotated_rect.topleft)

        if disp_text[0] != 0:
            if disp_text[0] == 5:
                x = I.random.randrange(100, 800)
                y = I.random.randrange(50, 600)
            Ff.display_text(screen, disp_text[1], 21, (x, y), "white")
            disp_text[0] -= 1
        elif disp_text == [0, "*Lockpick Broke*"]:
            if I.info.BACKPACK_CONTENT.get("Lockpick") == None:
                running = False
                Ff.display_text_player("No more lockpicks", 5000)
            else:
                pick_img = I.pg.image.load(lock_path + "Pick.png")
                disp_text = [0, ""]
        I.pg.display.flip()
        clock.tick(10)

    return unlocked

def handle_grinder(screen, items, gifs, data, decorations):
    def move_closer_to_center(row, column, target_row=300, target_column=410, step_size=10):
        # Move row closer to the target row
        if row < target_row:
            row = min(row + step_size, target_row)
        elif row > target_row:
            row = max(row - step_size, target_row)

        # Move column closer to the target column
        if column < target_column:
            column = min(column + step_size, target_column)
        elif column > target_column:
            column = max(column - step_size, target_column)

        return row, column
    running = True
    grind_start = False
    screen.fill((0, 0, 0, 0))
    border = 1 # rect border size
    path = decorations.decor_dict["Grinder_Tool"]["path"]
    path = path.replace("Grinder_tool", "Grinder_backpack")
    gif_iteration = 0
    grind_count = 0
    string_for_X = "[X] to exit"

    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    block = [0, 0]
    add_to_grinder = []
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
                if event.key == I.pg.K_c and len(add_to_grinder) < 5:
                    pickup = (Ff.find_item_by_slot(block[0], block[1]), block[0], block[1])
                    if pickup[0] != None:
                        row = I.random.randrange(200, 350, 10)
                        collumn = I.random.randrange(320, 430, 10)
                        add_to_grinder.append((pickup[0], row, collumn))
                        Ff.remove_from_backpack(pickup[0], 1)
                        string_for_X = "[X] to empty"
                elif event.key == I.pg.K_x:
                    if add_to_grinder == []:
                        running = False
                    for item, row, collumn in add_to_grinder:
                        Ff.add_to_backpack(item, 1, items)
                    add_to_grinder = []
                    string_for_X = "[X] to exit"
                elif event.key == I.pg.K_z and add_to_grinder != []:
                    grind_start = True
                    gif_time = I.pg.time.get_ticks()

        I.BB.display_backpack(screen, data["Player"], items, screen.get_rect(), "half")
        if grind_start:
            old_iteration = path[-5]
            path = path.replace("_" + str(old_iteration), "_" + str(gif_iteration))
        else:
            path = decorations.decor_dict["Grinder_Tool"]["path"]
            path = path.replace("Grinder_tool", "Grinder_backpack_0")
        Ff.add_image_to_screen(screen, path, (100, 200, 400, 400))



        for item, row, collumn in add_to_grinder:
            Ff.add_image_to_screen(screen, items.item_dict[item.split("|")[0]]["path"], (row, collumn, item_w*2, item_h*2))

        Ff.display_text(screen, string_for_X, 20, (400, 650), "red")
        Ff.display_text(screen, "[Z] to grind", 20, (100, 650), "green")

        rect = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
        I.pg.draw.rect(screen, "yellow", rect, border)

        I.pg.display.flip()

        if grind_start and gif_time + 100 <= I.pg.time.get_ticks():
            gif_iteration += 1
            gif_time = I.pg.time.get_ticks()
            if gif_iteration == 6:
                gif_iteration = 1
                for i in range(0, len(add_to_grinder)):
                    new_row_collumn_values = move_closer_to_center(add_to_grinder[i][1], add_to_grinder[i][2])
                    add_to_grinder[i] = add_to_grinder[i][0], new_row_collumn_values[0], new_row_collumn_values[1]
                grind_count += 1
            if grind_count == 3:
                grind_count = 0
                grind_start = False
                colors = []
                for item, row, collumn in add_to_grinder:
                    found_start = items.item_dict[item.split("|")[0]]["Properties"].find("GRINDABLE")
                    if found_start != -1:
                        color = items.item_dict[item.split("|")[0]]["Properties"][found_start:].split(",,,")[0].split(":")[1]
                        colors.append(I.A.DUST_COLORS[color.lower()])
                if colors != []:
                    blended_color = tuple(sum(color[i] for color in colors) // len(colors) for i in range(4))
                    blended_color = blended_color[0], blended_color[1], blended_color[2]
                    # print(I.webcolors.rgb_to_name(blended_color))
                    color_name = Ff.get_color_by_RGB(blended_color)
                    # print("Color: ", color_name)
                    if color_name != -1:
                        for item in items.item_dict.keys():
                            if "BREWABLE" in items.item_dict[item]["Properties"]:
                                dust_name = color_name + " Dust"
                                if dust_name == item:
                                    Ff.add_to_backpack(item, 1, items)
                    else:
                        print("failed", blended_color)
                    add_to_grinder = []

def handle_hammer_hits(items, decorations, rooms, data):
    """Handles checking if a hammer is being used by the player, melted rock health reducing"""
    if I.info.AXE[0] != 0 or I.info.PICAXE[0] != 0 or I.info.COMBAT_RECT[0] != 0:
        location, rects = get_tool_location_in_equiped("Hammer")
        if location == None:
            return
        speed = float(Ff.get_property(I.info.EQUIPED[list(rects.keys())[location]][0].split("|")[0], items, "WEAPON")[1])

        attack_rect = list(rects.values())[location][0]
        hit_id = attack_rect.collidelistall(decorations.displayed_rects_full)
        # print("hit id: ", hit_id)
        if hit_id != [] and float(speed) * I.info.BASE_ATTACKING_SPEED == rects[list(rects.keys())[location]][1]:
            remove_list = []
            for hit in hit_id:
                # count = -1
                # print("easyer: ", decorations.names_with_id[hit])
                decor_name, id = decorations.names_with_id[hit]
                if decorations.decor_dict[decor_name]["action"] == 'Smash' and decorations.decor_dict[decor_name][id]["rect"] == decorations.displayed_rects_full[hit]:
                    type = I.info.EQUIPED[list(rects.keys())[location]][0].split("|")[0].split(" ")[0]
                    if type == "Wooden":
                        damage = 2
                    elif type == "Iron":
                        damage = 4
                    if S.GOD_MODE:
                        damage = 100

                    bool_var, health = decorations.decor_dict[decor_name][id]["health"].split(",,")
                    health = int(health.split(",")[0]) - damage
                    rects[list(rects.keys())[location]][1] -= 1  # debouncing variable. so that it would enter here once per hit
                    data["Player"]["stats"]["Smithing"] = data["Player"]["stats"]["Smithing"] + damage

                    if health <= 0:
                        health = 0
                        remove_list.append((decor_name, id))
                    else:
                        decorations.decor_dict[decor_name][id]["health"] = bool_var + ",," + str(health) + "," + decorations.decor_dict[decor_name][id]["health"].split(",,")[1].split(",")[1]
            for decor_name, id in remove_list:
                rect_location = decorations.decor_dict[decor_name][id]["rect"]
                del decorations.decor_dict[decor_name]
                rooms.decor.remove(decor_name)
                del I.info.MAP_CHANGE[rooms.name]["add_bypassed"][decor_name]
                decorations.decor_dict["Anvil"][0]["effect"] = ""

                item_find_id = items.item_dict[decor_name]["Properties"].find("ANVIL")
                item_properties = items.item_dict[decor_name]["Properties"][item_find_id:].split(",,,")[0].replace("ANVIL(", ""). replace(")", "")
                possible_items = item_properties.split(",,")
                rewards = []
                total_odds = 0
                for possible_item in possible_items:
                    odds = float(possible_item.split("-")[0])
                    total_odds += odds
                    item_name = possible_item.split("-")[1].split(":")[0]
                    amount_min = int(possible_item.split("-")[1].split(":")[1])
                    amount_max = int(possible_item.split("-")[1].split(":")[2])
                    rewards.append((odds, item_name, amount_min, amount_max))
                choice = I.random.uniform(0, total_odds)
                cumulative = 0
                for odds, item_name, min_amount, max_amount in rewards:
                    cumulative += odds
                    if choice <= cumulative:
                        # Choose a random amount within the specified range
                        amount = I.random.randint(min_amount, max_amount)
                        break
                I.IB.add_dropped_items_to_var(item_name, amount, rooms, (rect_location.x, rect_location.y), data, "decor")

def handle_shovel_digging(decorations, items, rooms, data, collide, background_screen):
    # print(I.info.WALKING_ON)
    if I.info.WALKING_ON in ["Grass", "Sand"] and collide == [False]:
        if I.info.AXE[0] != 0 or I.info.PICAXE[0] != 0 or I.info.COMBAT_RECT[0] != 0:
            location, rects = get_tool_location_in_equiped("Shovel")
            if location == None:
                return
            speed = float(Ff.get_property(I.info.EQUIPED[list(rects.keys())[location]][0].split("|")[0], items, "WEAPON")[1])
            attack_rect = list(rects.values())[location][0]
            hit_id = attack_rect.collidelistall(decorations.displayed_rects)
            if hit_id == [] and float(speed) * I.info.BASE_ATTACKING_SPEED == rects[list(rects.keys())[location]][1]:
                """if dig spot is nothing aka free ground and ariving here only once"""
                rects[list(rects.keys())[location]][1] -= 1  # debouncing variable. so that it would enter here once per hit
                orientation = {
                    "Front.png": (-0.5, 1),
                    "Back.png": (-0.5, -0.6),
                    "Left.png": (-1, 0),
                    "Right.png": (0, 0)
                }
                hole_type = {"Grass": "Grass Hole",
                             "Sand": "Sand Hole"
                             }


                image = I.pg.image.load(decorations.decor_dict[hole_type[I.info.WALKING_ON]]["path"])
                rect = image.get_rect()
                rect.x = rects[list(rects.keys())[location]][0].x + data["Zoom_rect"].x + 20 * orientation[I.info.LAST_ORIENT[0]][0]
                rect.y = rects[list(rects.keys())[location]][0].y + data["Zoom_rect"].y + 10 * orientation[I.info.LAST_ORIENT[0]][1]

                collisions = rect.collidelist(decorations.displayed_rects_full)
                error = 0
                error_code = {0: "Can not dig hole there",
                              1: "It seems you are walking on unknown ground",
                              2: "Seems like you want to dig something that is dificult to dig",
                              }
                if collisions == -1:
                    error = 1
                    """fixes not digging holes on holes"""
                    coordinate_get = rect.copy()
                    coordinate_get.x = coordinate_get.x - data["Zoom_rect"].x
                    coordinate_get.y = coordinate_get.y - data["Zoom_rect"].y
                    rightbottom = tuple(background_screen.get_at((coordinate_get.x + coordinate_get.w, coordinate_get.y + coordinate_get.h)))
                    lefttop = tuple(background_screen.get_at((coordinate_get.x, coordinate_get.y)))
                    # I.T.Make_rect_visible(background_screen, coordinate_get, "black")
                    # background_screen.set_at((coordinate_get.x, coordinate_get.y), "black")
                    # background_screen.set_at((coordinate_get.x + coordinate_get.w, coordinate_get.y + coordinate_get.h), "black")
                    if I.A.WALKING_COLORS.get(lefttop) != None and I.A.WALKING_COLORS.get(rightbottom) != None:
                        error = 2
                        if I.A.WALKING_COLORS[lefttop] in ["Grass", "Sand"] and I.A.WALKING_COLORS[rightbottom] in ["Grass", "Sand"] and I.A.WALKING_COLORS[lefttop] == I.A.WALKING_COLORS[rightbottom]:
                            error = 3
                            print(I.A.WALKING_COLORS[lefttop], I.A.WALKING_COLORS.get(rightbottom), lefttop, rightbottom)

                            if decorations.decor_dict[hole_type[I.A.WALKING_COLORS[lefttop]]].get(0) == None:
                                Ff.update_map_view(0, hole_type[I.A.WALKING_COLORS[lefttop]], rect, "add", rooms.name)
                            else:
                                numeric_list = [int(x) for x in list(decorations.decor_dict[hole_type[I.A.WALKING_COLORS[lefttop]]].keys()) if str(x).isdigit()]
                                Ff.update_map_view(max(numeric_list) + 1, hole_type[I.A.WALKING_COLORS[lefttop]], rect, "add", rooms.name)
                            action_str_id = decorations.decor_dict[hole_type[I.A.WALKING_COLORS[lefttop]]]["action"].find("Shovel")
                            item, amount = decorations.decor_dict[hole_type[I.A.WALKING_COLORS[lefttop]]]["action"][action_str_id:].split(",,")[0].replace("Shovel:", "").split(":")
                            I.IB.add_dropped_items_to_var(item, int(amount), rooms, (rect.x, rect.y), data, "")
                            data["Player"]["stats"]["Digging"] = data["Player"]["stats"]["Digging"] + 1
                if error != 3:
                    Ff.display_text_player(error_code[error], 5000)
def get_tool_location_in_equiped(tool_name):
    rects = {"Sword": I.info.COMBAT_RECT, "Axe": I.info.AXE, "Picaxe": I.info.PICAXE}
    shovel_location = [weapon[0] != 0 and tool_name in weapon[0] for weapon in I.info.EQUIPED.values()]
    pressed_button = [button[0] != 0 for button in rects.values()]
    location = 10
    for i in range(len(shovel_location)):
        """Axe locations is a list of three bool values, if the value is true then an item with "Axe" is there
        if pressed_button is a list of three bool values, if the value is true then the button was pressed, [X][V][B]"""
        if shovel_location[i]:
            if shovel_location[i] == pressed_button[i]:
                """Found the button pressed"""
                return i, rects
    if location == 10:
        return None, rects
