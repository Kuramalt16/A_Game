from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S

def handle_harvesting_decor(decorations, collide, rooms, data, items):
    harvest_name = collide[0]
    harvest_decor_id = collide[2]
    harvest_decor_rect = collide[1]
    harvest_decor_dict = decorations.decor_dict[harvest_name][harvest_decor_id]
    if "Harvested" not in harvest_name:
        """picking up fruit/berries"""
        Ff.update_map_view(harvest_decor_id, harvest_name, harvest_decor_rect, "remove", rooms.name, decorations)
        if rooms.size == ['1', '1', '1', '1']:
            harvest_decor_rect = harvest_decor_rect[0] + data["Zoom_rect"].x, harvest_decor_rect[1] + data["Zoom_rect"].y, harvest_decor_rect[2], harvest_decor_rect[3]
            Ff.update_map_view(harvest_decor_id, harvest_name + "_Harvested", harvest_decor_rect, "add", rooms.name)
        else:
            Ff.update_map_view(harvest_decor_id, harvest_name + "_Harvested", harvest_decor_rect, "add", rooms.name)
        item_name, item_min, item_max = decorations.decor_dict[harvest_name]["action"][decorations.decor_dict[harvest_name]["action"].find("HARVESTABLE"):].split(",,")[0].replace("HARVESTABLE:", "").split(",")
        amount = I.random.randint(int(item_min), int(item_max))
        I.QB.tutorial_berry_get(item_name)
        I.IB.add_dropped_items_to_var(item_name, amount, rooms, collide[1], data, "decor")
        data["Player"]["stats"]["Botany"] = data["Player"]["stats"]["Botany"] + amount
    else:
        Ff.display_text_player("Wait for the plant to produce fruit", 5000)

    # if collide[0] in I.info.HARVESTABLE.keys() and not data["Player"]["dead"]:
    #     if any(collide[1] == t[0] for t in I.info.HARVESTED_OBJECTS.get(collide[0])):
    #         Ff.display_text_player("Nothing found", 500)
    #         pass
    #     else:
    #         item = I.info.HARVESTABLE[collide[0]]
    #         values = items.item_dict[item]["Aquire"].split(",,")
    #         amount = I.random.randint(int(values[1]), int(values[2]))
    #         I.QB.tutorial_berry_get(item)
    #         I.IB.add_dropped_items_to_var(item, amount, rooms, collide[1], data, "decor")
    #         duration = int(values[3])
    #         data["Player"]["stats"]["Botany"] = data["Player"]["stats"]["Botany"] + amount
    #
    #         #  Handle registering items that were taken, used in not allowing collection of too many items from single bush
    #         harvested_obj_rect = decorations.decor_dict[collide[0]][collide[2]]["rect"]
    #         if I.info.HARVESTED_OBJECTS.get(collide[0]) == []:
    #             # Ff.update_map_view(collide[2], collide[0] + "_Harvested", (harvested_obj_rect.x, harvested_obj_rect.y), "add")
    #
    #             Ff.update_map_view(collide[2], collide[0], (0,0,0,0), "remove")
    #             Ff.update_map_view(collide[2], collide[0] + "_Harvested", harvested_obj_rect, "add")
    #             I.info.HARVESTED_OBJECTS[collide[0]] = [(collide[2], duration, I.info.CURRENT_ROOM["name"])]
    #
    #         else:
    #             Ff.update_map_view(collide[2], collide[0], (0,0,0,0), "remove")
    #             Ff.update_map_view(collide[2], collide[0] + "_Harvested", harvested_obj_rect, "add")
    #             existing_values = I.info.HARVESTED_OBJECTS.get(collide[0], [])
    #             existing_values.append((collide[2], duration, I.info.CURRENT_ROOM["name"]))
    #             I.info.HARVESTED_OBJECTS[collide[0]] = existing_values
    #         return


def harvest_timeout(decorations):
    decor_to_remove = []
    for option, decor in decorations.decor_dict.items():
        if "_Harvested" in option:
            for id in decor.keys():
                if isinstance(id, int):
                    time = int(decorations.decor_dict[option]["action"][decorations.decor_dict[option]["action"].find("HARVEST_TIME"):].split(",,")[0].replace("HARVEST_TIME:", ""))
                    if "TIME" not in decor[id]["effect"]:
                        decor[id]["effect"] = "TIME:" + str(int(time - 60))
                    else:
                        time_str = decor[id]["effect"].find("TIME:")
                        time_property = decor[id]["effect"][time_str:].split(",,")[0]
                        time = int(time_property.split(":")[1])
                        decor[id]["effect"] = "TIME:" + str(int(time - 60))
                    if int(decor[id]["effect"][decor[id]["effect"].find("TIME:"):].split(":")[1]) == 0:
                        Ff.update_map_view(id, option, (0, 0, 0, 0), "remove")
                        Ff.update_map_view(id, option.replace("_Harvested", ""), decor[id]["rect"], "add")
                        decor_to_remove.append((option, id))

    # for harvastable in I.info.HARVESTED_OBJECTS.keys():
    #     if I.info.HARVESTED_OBJECTS[harvastable] != []:
    #         i = 0
    #         while True:
    #             if I.info.HARVESTED_OBJECTS[harvastable][i][1] != 0:
    #                 I.info.HARVESTED_OBJECTS[harvastable][i] = (I.info.HARVESTED_OBJECTS[harvastable][i][0], I.info.HARVESTED_OBJECTS[harvastable][i][1] - 1, I.info.HARVESTED_OBJECTS[harvastable][i][2])
    #             if I.info.HARVESTED_OBJECTS[harvastable][i][1] == 0 and I.info.CURRENT_ROOM["name"] == I.info.HARVESTED_OBJECTS[harvastable][i][2]:
    #                 rect = Ff.get_decor_coordinates(harvastable + "_Harvested", I.info.HARVESTED_OBJECTS[harvastable][i][0], decorations)
    #                 if rect != None:
    #                     Ff.update_map_view(I.info.HARVESTED_OBJECTS[harvastable][i][0], harvastable, rect, "add", I.info.HARVESTED_OBJECTS[harvastable][i][2])
    #                     Ff.update_map_view(I.info.HARVESTED_OBJECTS[harvastable][i][0], harvastable + "_Harvested",(0, 0, 0, 0), "remove", I.info.HARVESTED_OBJECTS[harvastable][i][2])
    #                     I.info.HARVESTED_OBJECTS[harvastable].pop(i)
    #             else:
    #                 i += 1
    #             if I.info.HARVESTED_OBJECTS[harvastable] == [] or i >= len(I.info.HARVESTED_OBJECTS[harvastable]):
    #                 break

def handle_plant_growing(decorations, option, id, decor_to_remove):
    # print(decorations.decor_dict[option][id]["effect"])
    stage, plant, time, full_time = decorations.decor_dict[option][id]["effect"].split(":")
    effect = decorations.decor_dict[option][id]["effect"]
    # print(stage, plant, time, full_time, option)
    rect = decorations.decor_dict[option][id]["rect"]
    if "PLANT0" in decorations.decor_dict[option]["action"]:
        """change from bare plant bed to plant bed with first growings"""
        Ff.update_map_view(id, option, (0, 0, 0, 0), "remove")
        decor_to_remove.append((option, id))
        Ff.update_map_view(id, option + "_1", rect, "add")
        Ff.update_map_view(id, option + "_1", effect, "add_effect")
    elif "PLANT1" in decorations.decor_dict[option]["action"]:
        """change from first growing plant bed to second growings"""
        Ff.update_map_view(id, option, (0, 0, 0, 0), "remove")
        decor_to_remove.append((option, id))
        option = option.replace("1", "2")
        Ff.update_map_view(id, option, rect, "add")
        Ff.update_map_view(id, option, effect, "add_effect")
    elif "PLANT2" in decorations.decor_dict[option]["action"]:
        """change from first growing plant bed to second growings"""
        Ff.update_map_view(id, option, (0, 0, 0, 0), "remove")
        decor_to_remove.append((option, id))
        Ff.update_map_view(id, option.replace("2", "3"), rect, "add")
        Ff.update_map_view(id, option.replace("2", "3"), effect, "add_effect")
    elif "PLANT3" in decorations.decor_dict[option]["action"]:
        """change from first growing plant bed to second growings"""
        Ff.update_map_view(id, option, (0, 0, 0, 0), "remove")
        decor_to_remove.append((option, id))
        count = len(decorations.decor_dict[plant]) - 4
        if decorations.decor_dict[plant].get(count) == None and decorations.decor_dict[plant + "_Harvested"].get(count) == None:
            Ff.update_map_view(count, plant, rect, "add")
        else:
            for i in range(count, count + 100):
                if decorations.decor_dict[plant].get(i) == None and decorations.decor_dict[plant + "_Harvested"].get(i) == None:
                    Ff.update_map_view(i, plant, rect, "add")
                    break
    return decor_to_remove

def render_growing_plants(plant_effect_data, decorations, option, id):
    stage, plant, time, full_time = plant_effect_data
    if "_1"  in stage:
        """initial seedlings"""
        # print("put initial seedlings")
        path = decorations.decor_dict[option]["path"][:-5] + "1.png"
        img = I.pg.image.load(path)
        decorations.decor_dict[option][id]["image"] = img
    elif "_2" in stage:
        path = decorations.decor_dict[option]["path"][:-5] + "2.png"
        img = I.pg.image.load(path)
        decorations.decor_dict[option][id]["image"] = img
    elif "_3" in stage:
        path = decorations.decor_dict[option]["path"][:-5] + "3.png"
        img = I.pg.image.load(path)
        decorations.decor_dict[option][id]["image"] = img

def remove_not_seeded_beds(plant_decor, remove_list, plant_name, id):
    """ONLY Not seeded plant beds here"""
    if ":" not in plant_decor["effect"]:
        """if plant bed is not seeded set timer"""
        plant_decor["effect"] = "NoPLANT:" + str(I.pg.time.get_ticks())
    else:
        """: is in the effect, means we can calculate if the time has passed"""
        time_start = int(plant_decor["effect"].split(":")[1])
        if time_start + 20000 <= I.pg.time.get_ticks():
            """if after 20k ticks aka 20 seconds not planted make it go away"""
            remove_list.append((plant_name, id))
    return remove_list
