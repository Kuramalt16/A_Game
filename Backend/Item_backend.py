from utils import Imports as I

dropped_items = {}

def add_dropped_items_to_var(item_name:str, amount:int, rooms:classmethod, location:tuple, data, case):
    # print(item_name, amount, rooms.name, location)

    if dropped_items.get(rooms.name) == None:
        dropped_items[rooms.name] = {}
    if case == "decor":
        x = location[0] + data["Zoom_rect"].x
        y = location[1] + data["Zoom_rect"].y
    else:
        x = location[0]
        y = location[1]
    for i in range(amount):
        if rooms.size == ["1", "1", "1", "1"]:
            new_x = x + I.random.randint(0, 20)
            new_y = y + I.random.randint(0, 20)
        else:
            new_x = x + I.random.randint(50, 100)
            new_y = y + I.random.randint(50, 100)
        if dropped_items[rooms.name].get((new_x, new_y)) == None:
            dropped_items[rooms.name][(new_x, new_y)] = [item_name]
        else:
            dropped_items[rooms.name][(new_x, new_y)].append(item_name)

def remove_dropped_items_from_var(item_name:str, location:tuple, rooms:classmethod):
    dropped_items[rooms.name][location].remove(item_name)



