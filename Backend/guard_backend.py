from utils import Frequent_functions as Ff, Imports as I


""" on spawn guards are in allignment 2 and are decors.

    when hit by player criminal charge is set to 'Assault'
    
    when charge is not "" and player collides with guard and dialog.iteration is 0
     
    collide variable is set 'Castle_Guard', current_mob: dict, rect.
    
    with that collide configuration conversation starts.
         
    iteration is set to 1 once criminal charges are set and not in Prison 
    
    once talked with guards go to prison, pay fine or run. 
    
    RUN: get's damaged - run away. !!guard sometimes spawns away!!
    
    pay fine: guards reset, payment paid
    
    prison: go to prison !!needs to take away items and leave one pick.!!
    
    """


def handle_guards(collide, data, screen, npc, items, decorations, gifs, rooms, clock, spells):
    if collide != [False] and "Guard" in collide[0] and I.info.CRIMINAL["Charge"] != "":
        if not isinstance(collide[1], I.pg.Rect):
            """Handles talking to the guards after they catch you"""
            current_mob = collide[1]
            guard_name = collide[0]
            if npc[guard_name]["dialog"].iteration != 1:
                """if crime has been commited and still havent talked."""
                I.DialB.init_dialog(guard_name, data["Player"], screen, npc, items, decorations, data, gifs, rooms, clock, spells)
            # elif npc[guard_name]["dialog"].iteration == 1:
            #     """if iteration is 1 means conversation has been started for weather to capture or pay fine"""
            #     print("here1")

    if "Prison" in rooms.name and I.info.CRIMINAL["Prison_time"] == 0:
        """adds castle guard to prison cell, to escort the prisoner out"""
        if "Castle_Guard" not in rooms.decor:
            Ff.update_map_view(0, "Castle_Guard", (600, 200), "add")


    # if rooms.type == "Prison" and I.info.CRIMINAL["Prison_time"] == 0:
    #     """if you are in prison and you have finished serving your time"""
    #     print(decorations.decor_dict["Castle_Guard"])
    #     print(npc["Castle_Guard"]["dialog"].id)

def guard_allignment_change(mob, current_mob):
    """if the mob is a guard and player is a criminal and guard is visible,
     change allignment and make not decor."""
    if "Guard" in mob.name and I.info.CRIMINAL["Charge"] != "" and current_mob["allignment"] == 2:
        if current_mob["visible"]:
            current_mob["allignment"] = 6
            current_mob["decor"] = False
            Ff.update_map_view(current_mob["id"], mob.name, (0, 0), "remove")

def guard_allignment_2_handle(current_mob, decorations, mob, target_pos, data):
    """Castle guard changes from decor to mob"""
    if current_mob["decor"]:
        if decorations.decor_dict[mob.name].get(current_mob["id"]) == None:
            # print(decorations.decor_dict["Bush_S_2"])
            decorations.decor_dict[mob.name][current_mob["id"]] = {
                'name': mob.name,
                'id': current_mob["id"],
                'image': I.pg.image.load(decorations.decor_dict[mob.name]["path"]),
                'rect': current_mob["guard_post"],
                'effect': '',
                'health': decorations.decor_dict[mob.name]['health']
            }

        current_mob['current_pos'] = decorations.decor_dict[mob.name][current_mob["id"]]["rect"]
    """if player approaches guard turns into visible"""
    current_mob["visible"] = Ff.get_visible(target_pos, current_mob, decorations.displayed_rects, data["Zoom_rect"])

def reset_criminal_record(dialog_class):
    I.info.CRIMINAL = {
        "Charge": "",
        "Fine": 0,
        "Prison_time": 0
    }
    dialog_class.iteration = 0

def reset_guard_mob_to_decor(current_mob, mob):
    if "Guard" in mob.name and I.info.CRIMINAL["Charge"] == "":
        for current_mob in mob.mobs:
            current_mob["allignment"] = 2
            current_mob["decor"] = True
        return False
    return True

def set_guard_posts(decorations, mob):
    for option in decorations.decor_dict.keys():
        if "Guard" in option:
            for id in decorations.decor_dict[option].keys():
                if isinstance(id, int):
                    guard_rect = decorations.decor_dict[option][id]["rect"]
                    mob[option].mobs[id]["guard_post"] = guard_rect