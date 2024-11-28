import random
from utils import Imports as I, Frequent_functions as Ff
class Mob:
    def __init__(self, name, hp, exp, allignment, count, damage, speed, path, delay, decor, drop):
        self.name = name
        self.hp = hp
        self.exp = exp
        self.allignment = allignment
        # Allignment: 0 - unaligned (acts randomly),
        # 1 - lawful good ( doesnt attack ever, and doesnt run away ),
        # 2 - lawful neutral ( only hits if sees you hitting others ),
        # 3 - lawful evil ( debufs you or steals from you unprovoked, attacks if you attack )
        # 4 - neutral good, (doesn't attack, runs away if provoked)
        # 5 - Neutral ( attacks if provoked ),
        # 6 - Neutral evil, (attacks player unprovoked)
        # 7 - Chaotic good, ( helps attack others )
        # 8 - Chaotic neutral, ( attacks and runs away )
        # 9 - Chaotic evil ( attacks all unprovoked )

        if name not in I.info.CURRENT_ROOM["Mobs"]:
            I.info.CURRENT_ROOM["Mobs"] += ", " + name + ":" + str(count)
            if I.info.CURRENT_ROOM["Mobs"][0] == ",":
                I.info.CURRENT_ROOM["Mobs"] = I.info.CURRENT_ROOM["Mobs"][1:]

        self.decor = decor
        self.count = (count, count)
        self.damage = damage
        self.speed = speed
        self.path = path
        self.frame_change = False
        self.delay = delay
        list_drop = drop.split(",, ")
        self.drop = []
        for drop in list_drop:
            drop_values = drop.split(",")
            self.drop.append([drop_values[0], int(drop_values[1]), int(drop_values[2])])
        if len(self.drop) == 1:
            self.drop = (self.drop[0][0], self.drop[0][1], self.drop[0][2])
        self.mobs = [self.create_mob(i) for i in range(count)]  # Create initial list of mobs



    def create_mob(self, id):
        """Create a single mob instance with unique id."""
        if self.allignment == 0:
            temp_allignment = random.randint(1, 9)
        else:
            temp_allignment = self.allignment
        if "Guard" in self.name:
            return {
                "id": id,
                "hp": (self.hp, self.hp),
                "damage": self.damage,
                "exp": self.exp,
                "drop": self.drop,
                "speed": (self.speed, 0),
                "effect": {
                    "Fire": 0,
                    "Cold": 0,
                    "Force": 0,
                },
                "decor": self.decor,
                "damage_type": "",
                "allignment": temp_allignment,
                "gif_frame": (0, Ff.count_png_files(self.path)),
                "visible": False,
                "rect": [],  # Placeholder for the Pygame rect object
                "image": [],  # Placeholder for the Pygame image list
                "previous_pos": (0, 0, 0, 0),
                "current_pos": (0, 0, 0, 0),
                "flip": "right",
                "guard_post": 0,
                "target_posision": (0, 0),
                "gifs": {}
            }
        else:
            return {
            "id": id,
            "hp": (self.hp, self.hp),
            "damage": self.damage,
            "exp": self.exp,
            "drop": self.drop,
            "speed": (self.speed, 0),
            "effect": {
                "Fire": 0,
                "Cold": 0,
                "Force": 0,
                "Necrotic": 0
            },
            "decor": self.decor,
            "damage_type": "",
            "allignment": temp_allignment,
            "gif_frame": (0, Ff.count_png_files(self.path)),
            "visible": False,
            "rect": [],  # Placeholder for the Pygame rect object
            "image": [],  # Placeholder for the Pygame image list
            "previous_pos": (0, 0, 0, 0),
            "current_pos": (0, 0, 0, 0),
            "flip": "right",
            "target_posision": (0, 0),
            "gifs": {}
            }

    def spawn_mobs(self, background_size, path, mob_gif_count, gifs, x1=0, y1=0):
        """Spawn mobs at random positions on the screen."""
        for mob in self.mobs:
            x = random.randint(0, background_size[0] - 100)
            y = random.randint(0, background_size[1] - 350)
            for a in range(mob_gif_count):
                if "Mine" in self.name:
                    self.name = self.name.replace(" Mine", "")
                if self.decor:
                    updated_name = self.name + "_Front"
                    image = I.pg.image.load(path + updated_name + "_" + str(a) + ".png").convert_alpha()
                else:
                    image = I.pg.image.load(path + self.name + "_" + str(a) + ".png").convert_alpha()
                mob["image"].append(image)
                if x1 != 0 and y1 != 0:
                    mob["rect"].append(image.get_rect(topleft=(x1, y1)))
                else:
                    mob["rect"].append(image.get_rect(topleft=(x, y)))
            mob["current_pos"] = mob["rect"][mob_gif_count-1]
            if mob["target_posision"] == (0, 0):
                mob["target_posision"] = mob["current_pos"][0:2]
            mob["previous_pos"] = mob["rect"][mob_gif_count-1]

            mob["gifs"]["Fire"] = I.gifs.Gif(*gifs["Fire"].args)  # Pass required arguments to create a new instance
            mob["gifs"]["Cold"] = I.gifs.Gif(*gifs["Cold"].args)
            mob["gifs"]["Force"] = I.gifs.Gif(*gifs["Force"].args)
            mob["gifs"]["Necrotic"] = I.gifs.Gif(*gifs["Necrotic"].args)

    def spawn_mob_acurate(self, path, mob_gif_count, id, x, y):
        for a in range(mob_gif_count):
            if "Mine" in self.name:
                self.name = self.name.replace(" Mine", "")
            image = I.pg.image.load(path + self.name + "_" + str(a) + ".png").convert_alpha()
            self.mobs[id]["image"].append(image)
            self.mobs[id]["rect"].append(image.get_rect(topleft=(x, y)))
        self.mobs[id]["current_pos"] = self.mobs[id]["rect"][mob_gif_count - 1]
        self.mobs[id]["previous_pos"] = self.mobs[id]["rect"][mob_gif_count - 1]

    # def move_mobs_randomly(self, decorations, data):
    #     """Move all mobs by random offsets, avoiding and escaping collisions."""
    #     for mob in self.mobs:
    #         if not mob["visible"]:
    #             # Randomly generate movement offsets
    #             speed = mob["speed"]
    #             if speed[1] == 0:
    #                 mob["speed"] = speed[0], speed[0]
    #                 x_offset = random.randint(-1, 1)
    #                 y_offset = random.randint(-1, 1)
    #                 if mob["rect"] != []:
    #                     new_rect = mob["rect"][0].copy()
    #                     new_rect.x += x_offset - data["Zoom_rect"].x
    #                     new_rect.y += y_offset - data["Zoom_rect"].y
    #
    #                     if not any(new_rect.colliderect(displayed_rect) for displayed_rect in decorations.displayed_rects):
    #                         self._update_mob_position(mob, x_offset, y_offset)
    #                     else:
    #                         self._escape_collision(mob, decorations, data, 1)
    #             else:
    #                 mob["speed"] = speed[0], speed[1] - 1
    #
    # def _update_mob_position(self, mob, x_offset, y_offset):
    #     """Update the mob's position by the given offsets."""
    #
    #     for rect in mob["rect"]:
    #         rect.x += x_offset
    #         rect.y += y_offset
    #
    #     if x_offset != 0:
    #         mob["flip"] = x_offset < 0
    #
    #     mob["current_pos"] = mob["rect"][0].copy()
    # def _escape_collision(self, mob, decorations, data, level):
    #     """Move the mob out of any collisions."""
    #     stuck = 0
    #     escape_directions = [(level, 0), (-level, 0), (0, level), (0, -level)]
    #
    #     for x_offset, y_offset in escape_directions:
    #         new_rect = mob["rect"][0].copy()
    #         new_rect.x += x_offset - data["Zoom_rect"].x
    #         new_rect.y += y_offset - data["Zoom_rect"].y
    #
    #         if not any(new_rect.colliderect(displayed_rect) for displayed_rect in decorations.displayed_rects):
    #             self._update_mob_position(mob, x_offset, y_offset)
    #             return
    #         else:
    #             stuck += 1
    #     if stuck == 4:
    #         self._escape_collision(mob, decorations, data, level + 1)

    # def update_visibility(self, screen, rect, id):
    #     screen_rect = screen.get_rect()
    #     if rect.colliderect(screen_rect):
    #         self.mobs[id]["visible"] = True
    #     else:
    #         self.mobs[id]["visible"] = False

    def knockback(self, victim, spaces):
        push = {"Back": (0, -spaces),
                "Front": (0, spaces),
                "Left": (-spaces, 0),
                "Right": (spaces, 0)}
        direction = I.info.LAST_ORIENT[0].split(".")[0]
        for i in range(len(victim['rect'])):
            victim['rect'][i].x += push[direction][0]
            victim['rect'][i].y += push[direction][1]
        victim["current_pos"] = victim['rect'][0]


    def remove_mob(self, mob_id):
        """Remove a mob from the list by id."""
        self.count = (self.count[0] - 1, self.count[1])
        self.mobs = [mob for mob in self.mobs if mob["id"] != mob_id]


    def deal_damage(self, victim: object, player: dict, weapon: any, items: dict, gifs: dict, rooms, data):
        if isinstance(weapon, list):
            # NOT SPELL AND NOT EFFECT DAMAGE
            damage = float(weapon[0])
            speed = float(weapon[1])
            knockback = int(weapon[2])
            type = weapon[3]
        elif weapon == "Follower":
            damage = 1 # based on pet's level
            knockback = 2
            type = "Piercing"

        elif "effect" in weapon:
            # EFFECT DAMAGE
            damage = 0.05
            knockback = 0
            type = weapon.split("_")[1]  # get's effect
        else:
            # SPELL DAMAGE
            extra = 0
            if any(weapon[0] != 0 and "Staff" in weapon[0] for weapon in I.info.EQUIPED.values()):
                if any(weapon[0] == "Wooden Staff" for weapon in I.info.EQUIPED.values()):
                    extra = 1
                else:
                    print("some other material staff")
            damage = weapon["damage"]
            if "max" in damage:
                maxId = damage.find("max")
                damage = damage[maxId:].split(",,")[1:][0]
            damage = random.randint(int(damage.split("d")[0]), int(damage.split("d")[1])) + extra
            knockback = weapon["knockback"] + extra
            type = weapon["type"]

        if victim["allignment"] == 5:
            victim["allignment"] = 6
        victim["hp"] = victim["hp"][0] - damage, victim["hp"][1]
        if victim["hp"][0] <= 0:
            gifs[type].start_gif = False
            self.remove_mob(victim["id"])
            player["Experience"] += victim["exp"]
            I.PB.level_up(player, gifs)
            if isinstance(victim["drop"], tuple): # if victim drops not more than one item
                amount = victim["drop"][1] if random.randint(0, victim["drop"][2]-1) == 0 else 0
                # print(victim["rect"][0])
                I.IB.add_dropped_items_to_var(victim["drop"][0], amount, rooms, (victim["rect"][0][0], victim["rect"][0][1]), data, "mob")

                # if amount != 0:
                #     Ff.display_text_player("Recieved " + str(amount) + " " + str(victim["drop"][0]), 5000)
            else:
                # choose = random.randint(0, len(victim["drop"]) - 1)
                if victim["drop"] != 0 and victim["drop"] != []:
                    # print(victim["drop"])
                    amount1 = victim["drop"][0][1] if random.randint(0, victim["drop"][0][2]) == 0 else 0
                    amount2 = victim["drop"][1][1] if random.randint(0, victim["drop"][1][2]) == 0 else 0
                    I.IB.add_dropped_items_to_var(victim["drop"][0][0], amount1, rooms,(victim["rect"][0][0], victim["rect"][0][1]), data, "mob")
                    I.IB.add_dropped_items_to_var(victim["drop"][1][0], amount2, rooms,(victim["rect"][0][0], victim["rect"][0][1]), data, "mob")

                    # if amount1 != 0:
                    #     Ff.display_text_player("Recieved " + str(amount1) + " " + str(victim["drop"][0][0][:-1]), 5000)
                    # if amount2 != 0:
                    #     Ff.display_text_player("Recieved " + str(amount2) + " " + str(victim["drop"][1][0][:-1]), 5000)

            # gifs[type].start_gif = False

        elif "effect" not in weapon:
            self.knockback(victim, int(knockback))
            self.effect(victim, type)

    def effect(self, victim, type):
        if type == "Cold":
            duration = random.randint(2,4)

        elif type in ["Force", "Necrotic"]:
            duration = 1

        elif type == "Fire":
            duration = random.randint(2, 3)
        if type not in ["Slashing", "Blunt", "Piercing"]:
            victim["effect"][type] = duration

    def update_position(self, new_x, new_y, mob):
        mob['previous_pos'][0] = mob['current_pos'][0]
        mob['previous_pos'][1] = mob['current_pos'][1]
        mob['current_pos'][0] = new_x
        mob['current_pos'][1] = new_y
        for rect in mob["rect"]:
            rect.topleft = (new_x, new_y)

def read_db():
    db_data = Ff.read_data_from_db("mobs", ["name", "exp", "health", "allignment", "damage", "speed", "path", "delay", "drops", "class"])
    db_dict = {}
    for data in db_data:
        db_dict[data[0]] = {"exp": int(data[1]),
                           "health": int(data[2]),
                           "allignment": int(data[3]),
                           "damage": data[4],
                           "speed": int(data[5]),
                           "path": data[6],
                           "delay": int(data[7]),
                           "drop": data[8],
                           "class": data[9]
                           }
    return db_dict
