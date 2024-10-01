from utils import Imports as I, Frequent_functions as Ff

def handle_hoe(collide, data, items, decorations, screen):
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
                    if type == "Wooden":
                        amount = 5
                    elif type == "Stone":
                        amount = 10
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
                            count = Ff.update_map_view(0, "Plant bed", xy, "get")
                            if count < amount:
                                Ff.update_map_view(count, "Plant bed", xy, "add")
                            else:
                                Ff.display_text_player("Maximum amount of seed beds", 3000)


def handle_axe_chopping(decor_rect, decor_name, decor_dict, id, items):
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
            """axe collided with an object the 1000 is used for something"""
            type = I.info.EQUIPED[list(rects.keys())[location]][0].split("|")[0].split(" ")[0]
            if type == "Wooden":
                choppable = ["Tree_T_1"]
                damage = 1
            elif type == "Stone":
                choppable = ["Tree_T_1", "Tree_M_1"]
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
        """ Button was pressed [X], [V] or [B] """
        rects = {"Sword": I.info.COMBAT_RECT, "Axe": I.info.AXE, "Picaxe": I.info.PICAXE}
        picaxe_location = [weapon[0] != 0 and "Picaxe" in weapon for weapon in I.info.EQUIPED.values()]
        pressed_button = [button[0] != 0 for button in rects.values()]
        location = 10

        for i in range(len(picaxe_location)):
            """Picaxe locations is a list of three bool values, if the value is true then an item with "Picaxe" is there
            if pressed_button is a list of three bool values, if the value is true then the button was pressed, [X][V][B]"""
            if picaxe_location[i]:
                if picaxe_location[i] == pressed_button[i]:
                    """Found the button pressed"""
                    location = i

        if location == 10:
            return
        speed = float(Ff.get_property(I.info.EQUIPED[list(rects.keys())[location]][0].split("|")[0], items, "WEAPON")[1])

        if list(rects.values())[location][0].colliderect(decor_rect) and list(rects.values())[location][1] == speed * I.info.BASE_ATTACKING_SPEED:
            """Picaxe collided with an object the 1000 is used for something"""
            type = I.info.EQUIPED[list(rects.keys())[location]][0].split("|")[0].split(" ")[0]
            if type == "Wooden":
                breakable = ["Stone_T_1"]
                damage = 1
            elif type == "Stone":
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

def handle_axe_rewards(decorations, tree_name, items):
    if "PICAXE" in decorations.decor_dict[tree_name]["action"]:
        action_list = decorations.decor_dict[tree_name]["action"].split(",,")
        for action in action_list:
            if "PICAXE" in action:
                action = action[7:]
                possible_rewards = action.split(",")
                loot_list = []
                amount_list = []
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
                for reward in possible_rewards:
                    loot, chance_min, chance_max = reward.split(":")

                    amount = int(I.random.uniform(float(chance_min), float(chance_max)))
                    if amount != 0:
                        loot_list.append(loot)
                        amount_list.append(amount)

    for i in range(0, len(loot_list)):
        Ff.add_to_backpack(loot_list[i], amount_list[i], items)
        Ff.display_text_player("Acquired " + str(amount_list[i]) + " " + loot_list[i], 5000)