from operator import truediv

from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S

def handle_container_click(decorations, collide, screen, items, data, rooms):
    if "CONTAINER" in decorations.decor_dict[collide[0]]["action"]:
        dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))
        screen.blit(dim_surface, (0, 0))
        container_name = collide[0]
        container_size = decorations.decor_dict[collide[0]]["action"].split(":")[1]
        handle_containers(container_name, container_size, items, screen, data["Player"], decorations, collide[2], rooms)

def handle_containers(container_name, container_size, items, screen, player, decorations, id, rooms):
    pressed = 0 # key authentication
    running = True # loop var
    block = (0, 0) # backpack block
    border = 1 # rect border size
    # screen.fill((0,0,0,0))
    if I.info.CONTAINERS.get(rooms.name) == None:
        I.info.CONTAINERS[rooms.name] = {}
    use = 0 # place holder for items to be eaten/used
    selected = 0 # place holder for rect of selected block
    color = "Yellow" # color of selected rect
    pickup = (0, 0, 0) # place holder for the name, posx, posy of selected block
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    # coordinates = br.get_equipment_coordinates(block)
    container_size = int(container_size.split("x")[0]), int(container_size.split("x")[1])
    container_coordinates = get_container_coordinates(container_size)

    remove_from_container = []
    path = S.PLAYING_PATH["Backpack_Tile"]

    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key == I.pg.K_i:
                    pressed = I.pg.K_i
                elif event.key == I.pg.K_ESCAPE:
                    pressed = I.pg.K_ESCAPE
                elif event.key == I.pg.K_x:
                    pressed = I.pg.K_x
                elif event.key == I.pg.K_c:
                    pressed = I.pg.K_c
                    if selected == 0:
                        if block[0] >= 0:
                            selected = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
                            pickup = (Ff.find_item_by_slot(block[0], block[1]), block[0], block[1])
                        else:
                            selected = I.pg.Rect(container_coordinates[block][0], container_coordinates[block][1], item_w, item_h)
                            pickup = (find_item_by_slot_containers(block[0], block[1], container_name, id, rooms), block[0], block[1])
                    else:
                        # print("if selected is not 0: ", selected)
                        if pickup[0] != 0 and pickup[0] != None:
                            remove_from_container = handle_container_backpack_switching(pickup, selected, container_name, id, block, items, rooms)
                        pickup = (0, 0, 0)
                        selected = 0
                elif event.key == I.pg.K_UP:
                    block = (block[0], block[1] - 2)
                    if block[1] < 0:
                        block = (block[0], 26)
                elif event.key == I.pg.K_DOWN:
                    block = (block[0], block[1] + 2)
                    if block[1] > 26:
                        block = (block[0], 0)
                elif event.key == I.pg.K_LEFT:
                    block = (block[0] - 2, block[1])
                elif event.key == I.pg.K_RIGHT:
                    block = (block[0] + 2, block[1])
                    if block[0] > 14:
                        block = (0, block[1])
            elif event.type == I.pg.KEYUP:
                if pressed == I.pg.K_i or pressed == I.pg.K_ESCAPE:
                    running = False  # exits backpack view
                if event.key == I.pg.K_x and pressed == I.pg.K_x:
                    if block[0] < 0:
                        # IF SELECTED IN CONTAINER, REMOVE THE ITEM AND ADD IT TO BACKPACK
                        selected = I.pg.Rect(container_coordinates[block][0], container_coordinates[block][1], item_w, item_h)
                        pickup = (find_item_by_slot_containers(block[0], block[1], container_name, id, rooms), block[0], block[1])
                        if pickup[0] != None:
                            remove_from_container.append(pickup[1:3])
                            Ff.add_to_backpack(pickup[0], 1, items)
                    else:
                        # IF SELECTED IN BACKPACK, REMOVE THE ITEM AND ADD IT TO CONTAINER
                        selected = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)
                        pickup = (Ff.find_item_by_slot(block[0], block[1]), block[0], block[1])
                        new_block = (-2, 0)
                        cancel = False
                        for key, value in I.info.CONTAINERS[rooms.name].items():
                            for sub_key, sub_value in value.items():
                                if new_block == sub_key:
                                    new_block = new_block[0] - 2, new_block[1]
                                    if new_block[0] < -2 - container_size[1]:  # handles switching to lower container levels (Y axis)
                                        new_block = -2, new_block[1] + 2
                                        if new_block[1] > container_size[0] * 2 - 2: # Handles not overfilling the container. if the new block Y pos is higher than the size of container multiplied by 2 ( block format is in twos) and removed -2 (block format starts from 0) then dont add
                                            cancel = True
                        if not cancel and pickup[0] != None:
                            handle_container_storage(pickup[0], container_name, new_block, id, selected, rooms)


                    selected = 0
                    pickup = (0, 0, 0)

        I.BB.display_backpack(screen, player, items, screen.get_rect(), "half")

        # DISPLAY CONTAINER GRID
        Ff.add_image_to_screen(screen, decorations.decor_dict[container_name]["path"], [275, 175, 150, 200])
        start_row = 312
        start_collumn = 225

        for i in range(0, int(container_size[0])):
            for a in range(0, int(container_size[1])):
                Ff.add_image_to_screen(screen, path, [start_row, start_collumn, 42, 40])
                start_row += 36
            start_row = 312
            start_collumn += 36



        if block[0] < 0:
            if block[0] < -2 * container_size[1]:
                block = -2 * container_size[1], block[1]
            if block[1] > 2 * (container_size[0] - 1):
                block = block[0], 2 * (container_size[0] - 1)
            rect = I.pg.Rect(container_coordinates[block][0], container_coordinates[block][1], item_w, item_h)
        else:
            rect = I.pg.Rect(list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]], item_w, item_h)

        if remove_from_container != []:
            for i in remove_from_container:
                del I.info.CONTAINERS[rooms.name][container_name, id][i[0], i[1]]
            remove_from_container = []

        if I.info.CONTAINERS[rooms.name].get((container_name, id)) != None:
            for pos, (name, amount) in I.info.CONTAINERS[rooms.name][(container_name, id)].items():
                Ff.add_image_to_screen(screen, items.item_dict[name.split("|")[0]]["path"], [container_coordinates[pos][0], container_coordinates[pos][1], item_w, item_h])

        I.pg.draw.rect(screen, color, rect, border)
        if selected != 0:
            I.pg.draw.rect(screen, "Yellow", selected, 2)

        I.pg.display.flip()

def find_item_by_slot_containers(x, y, container, id, rooms):
    if I.info.CONTAINERS[rooms.name].get((container, id)) != None:
        for key, value in I.info.CONTAINERS[rooms.name][container, id].items():
            if key[0] == x and key[1] == y:
                # if the possision matches get the key
                return value[0]
    else:
        return None

def get_container_coordinates(size):
    start_row = 390
    start_collumn = 232
    size_x = 36
    size_y = 36
    coordinates = {}

    height = size[0] * 2
    width = size[1] * -2 + -2
    for i in range(0, height, 2):
        for a in range(-2, width, -2):
            coordinates[(a, i)] = (start_row + a / 2 * size_x, start_collumn + i / 2 * size_y)

    return coordinates

def get_container_block(input_tuple, size_tuple):
    # print(input_tuple, size_tuple)

    first, second = input_tuple
    collumns, rows = size_tuple

    output1 = (first / -2) - 1
    if output1 > rows - 1:
        output1 = rows - 1

    output2 = second / 2
    if output2 > collumns - 1:
        output2 = collumns - 1

    return int(output2), int(output1)

def handle_container_storage(item_name, container, possision, id, rect, rooms):
    if I.info.CONTAINERS.get(rooms.name) == None:
        I.info.CONTAINERS[rooms.name] = {}

    if I.info.CONTAINERS[rooms.name].get((container, id)) == None:
        # print("first")
        # THIS MEANS NO DATA ABOUT THIS CONTAINER EXISTS
        I.info.CONTAINERS[rooms.name][container, id] = {
            possision: (item_name, 1)
                                            }
    else:
        # THIS MEANS CONTAINER WAS ALREADY MADE AND WE CAN NOW ADD EXTRA ITEMS TO IT
        if I.info.CONTAINERS[rooms.name][container, id].get(possision) == None:
            # THIS MEANS NO ITEM EXISTS IN THIS POSSISION
            # print("no item exists here")
            I.info.CONTAINERS[rooms.name][container, id][possision] = item_name, 1
        else:
            # pass
            print("item already exists here need to skip to another location in container")

            rect = 10, 800
            # THIS MEANS AN ITEM ALREADY EXISTS HERE
            # old_item = I.info.CONTAINERS[rooms.name][container, id][possision]
            # I.info.CONTAINERS[rooms.name][container, id][possision] = item_name, 1
            # a, pos_x, pos_y = I.info.BACKPACK_CONTENT[item_name]
            # I.info.BACKPACK_CONTENT[old_item[0]] = old_item[1], pos_x, pos_y
    # I.info.CONTAINERS[rooms.name][container, id] = item_name, I.info.BACKPACK_CONTENT[item_name][0], possision
    if rect[0] >= 633 and item_name != None:
        I.info.BACKPACK_CONTENT[item_name] = I.info.BACKPACK_CONTENT[item_name][0] - 1, I.info.BACKPACK_CONTENT[item_name][1], I.info.BACKPACK_CONTENT[item_name][2]
        if I.info.BACKPACK_CONTENT[item_name][0] == 0:
            del I.info.BACKPACK_CONTENT[item_name]

def handle_container_backpack_switching(pickup, selected, container_name, id, block, items, rooms):
    remove_from_container = []

    # HANDLE OLD POSSISION, (Delete if it's from the container, get value if its from the backpack)
    if I.info.BACKPACK_CONTENT.get(pickup[0]) != None:
        # IF THE ITEM IN PICKUP[0] EXISTS IN BACKPACK THEN CONTINUE
        if selected[0] < 633:
            # FROM CONTAINER
            value = I.info.CONTAINERS[rooms.name][container_name, id][pickup[1:3]]
            value = value[1], pickup[1], pickup[2]
            # print("then the value is: ", value)
            if find_item_by_slot_containers(block[0], block[1], container_name, id, rooms) == None:
                # print("if the item exists in container: add it to the deleting list")
                remove_from_container.append(pickup[1:3])
        else:
            # FROM BACKPACK
            value = I.info.BACKPACK_CONTENT[pickup[0]]
            # print("if the selected item is from backpack, then the value is: ", value)
    else:
        # print("if the picked up item doesn't exist in the backpack")
        # IF THE ITEM DOESNT EXIST IN THE BACKPACK, CHECK THE CONTAINER
        value = I.info.CONTAINERS[rooms.name][container_name, id][pickup[1:3]]
        value = value[1], pickup[1], pickup[2]
        # print("then we add it to backpack and remove it from the container")
        remove_from_container.append(pickup[1:3])

    # HANDLE NEW POSSISION
    taken_spaces = list(I.info.BACKPACK_CONTENT.values())
    if not any((block[0], block[1]) == (tpl[1], tpl[2]) for tpl in taken_spaces):
        # print("if the new possision is not in a taken space")
        #  IF THE SPOT WE WANT TO ASSIGN IS NOT TAKEN CONTINUE
        if block[0] < 0 and pickup[0] != None:
            # print("if the new possision is in the container:")
            handle_container_storage(pickup[0], container_name, block, id, selected, rooms)
        else:
            # print("if the new possision is in the backpack")
            # FIRST LET's CHECK IF THE VALUE DIDN'T ALREADY EXIST:
            if I.info.BACKPACK_CONTENT.get(pickup[0]) != None and selected[0] < 633:
                # print("if the picked up item already existed in the backpack and it was selected from the container")
                # PICKUP[0] item did exist. lets merge them.
                I.info.BACKPACK_CONTENT[pickup[0]] = (
                I.info.BACKPACK_CONTENT[pickup[0]][0] + value[0], block[0], block[1])
            else:
                # print("if the picked up item didnt exist in the backpack or was picked up from the backpack")
                I.info.BACKPACK_CONTENT[pickup[0]] = (value[0], block[0], block[1])  # set the new possision value
    else:
        # print("if the new possision is on another item")
        # ITEM PLACE WAS TAKEN, SWITCHING PLACES
        existing_item = Ff.find_item_by_slot(block[0], block[1])  # get existing item name
        if "STACK" in existing_item and "STACK" in pickup[0] and selected[0] >= 633:
            # print("if the possisions` item has stack in it and the item was in backpack")
            # BOTH OF THESE ITEMS ARE STACKS
            stack = Ff.get_property(existing_item.split("|")[0], items, "STACK")
            if float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0]][0]) <= stack:
                # print("if the existing item added up with the new picked up item is still less tahn the amount allowed by the stack")
                # MERGING TWO STACKS INTO ONE
                sum = float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0]][0])
                I.info.BACKPACK_CONTENT[existing_item] = sum, I.info.BACKPACK_CONTENT[existing_item][1], I.info.BACKPACK_CONTENT[existing_item][2]
                del I.info.BACKPACK_CONTENT[pickup[0]]
                # print("then we add up the items and remove the picked up item from the backpack")

            elif float(I.info.BACKPACK_CONTENT[existing_item][0]) < stack and float(I.info.BACKPACK_CONTENT[pickup[0]][0]) < stack and selected[0] >= 633:
                # print("if the existing item and the picked up item both are less than the stack allows and the item was in backpack")
                # MERGING VALUES OF STACKS WITH REMAINDER
                remainder = float(I.info.BACKPACK_CONTENT[existing_item][0]) + float(I.info.BACKPACK_CONTENT[pickup[0]][0]) - stack
                I.info.BACKPACK_CONTENT[pickup[0]] = remainder, I.info.BACKPACK_CONTENT[pickup[0]][1], I.info.BACKPACK_CONTENT[pickup[0]][2]
                I.info.BACKPACK_CONTENT[existing_item] = stack, I.info.BACKPACK_CONTENT[existing_item][1], I.info.BACKPACK_CONTENT[existing_item][2]
                # print("then we add up the items but leave a remainder")
        else:
            # print("if the existing item didn't have a stack")
            # CHECKING IF IT'S POSSIBLE TO JUST ADD THE TWO DIFERENT ITEMS INTO ONE ONLY IN BACKPACK
            stack = Ff.get_property(existing_item.split("|")[0], items, "STACK")
            if existing_item.split("|")[0] == pickup[0].split("|")[0] and I.info.BACKPACK_CONTENT[existing_item][0] + 1 < stack and selected[0:2] != [list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]]]:
                # print("if the existing items name is the same as the name of pickup and if the existing item is less than stack and if the selected new spot is not the same as the old spot IN BACKPACK")
                I.info.BACKPACK_CONTENT[existing_item] = I.info.BACKPACK_CONTENT[existing_item][0] + 1, block[0], block[1]
                # print("then we add one to the existing item")
            elif existing_item.split("|")[0] == pickup[0].split("|")[0] and selected[0:2] != [list(I.info.BACKPACK_COORDINATES_X.values())[block[0]], list(I.info.BACKPACK_COORDINATES_Y.values())[block[1]]]:
                # print("if the existing item names are the same and the stack got overflowed. then we only add one item to a new stack")
                Ff.add_to_backpack(pickup[0], 1, items)
            else:
                # print("if the names aren't the same")
                if selected[0] >= 633:
                    # print("if the item was selected from the backpack")
                    I.info.BACKPACK_CONTENT[existing_item] = I.info.BACKPACK_CONTENT[existing_item][0], pickup[1], pickup[2]
                    I.info.BACKPACK_CONTENT[pickup[0]] = I.info.BACKPACK_CONTENT[pickup[0]][0], block[0], block[1]
                    # print("then we switch the places of those items")
                else:
                    # print("if the selected item was from the container, erase the deleting list")
                    remove_from_container = []
    return remove_from_container
