import random
from utils import Imports as I, Frequent_functions as Ff
from Render import Background_Render as br
from Values import Settings as S
class Mob:
    def __init__(self, name, hp, exp, allignment, count, damage, speed):
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
        self.count = (count, count)
        self.damage = damage
        self.speed = speed
        self.mobs = [self.create_mob(i) for i in range(count)]  # Create initial list of mobs


    def create_mob(self, id):
        """Create a single mob instance with unique id."""
        if self.allignment == 0:
            temp_allignment = random.randint(1, 9)
        else:
            temp_allignment = self.allignment

        return {
        "id": id,
        "hp": (self.hp, self.hp),
        "damage": self.damage,
        "exp": self.exp,
        "drop": I.A.DROPS[self.name],
        "speed": (self.speed, self.speed),
        "effect": {
            "Fire": 0,
            "Cold": 0,
            "Force": 0,
        },
        "damage_type": "",
        "allignment": temp_allignment,
        "gif_frame": (0, S.MOB_PATH[self.name][1]),
        "visible": False,
        "rect": [],  # Placeholder for the Pygame rect object
        "image": [],  # Placeholder for the Pygame image list
        "previous_pos": (0, 0, 0, 0),
        "current_pos": (0, 0, 0, 0),
        "flip": False

        }

    def spawn_mobs(self, background_size, path, mob_gif_count):
        """Spawn mobs at random positions on the screen."""
        for mob in self.mobs:
            x = random.randint(0, background_size[0] - 100)
            y = random.randint(0, background_size[1] - 350)
            for a in range(mob_gif_count):
                image = I.pg.image.load(path + self.name + "_" + str(a) + ".png").convert_alpha()
                mob["image"].append(image)
                mob["rect"].append(image.get_rect(topleft=(x, y)))
            mob["current_pos"] = mob["rect"][mob_gif_count-1]
            mob["previous_pos"] = mob["rect"][mob_gif_count-1]

    def move_mobs_randomly(self, decorations, data):
        """Move all mobs by random offsets, avoiding and escaping collisions."""
        for mob in self.mobs:
            if not mob["visible"]:
                # Randomly generate movement offsets
                x_offset = random.randint(-1, 1)
                y_offset = random.randint(-1, 1)

                new_rect = mob["rect"][0].copy()
                new_rect.x += x_offset - data["Zoom_rect"].x
                new_rect.y += y_offset - data["Zoom_rect"].y

                if not any(new_rect.colliderect(displayed_rect) for displayed_rect in decorations.displayed_rects):
                    self._update_mob_position(mob, x_offset, y_offset)
                else:
                    self._escape_collision(mob, decorations, data)

    def _update_mob_position(self, mob, x_offset, y_offset):
        """Update the mob's position by the given offsets."""
        for rect in mob["rect"]:
            rect.x += x_offset
            rect.y += y_offset

        if x_offset != 0:
            mob["flip"] = x_offset < 0

        mob["current_pos"] = mob["rect"][0].copy()

    def _escape_collision(self, mob, decorations, data):
        """Move the mob out of any collisions."""
        escape_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for x_offset, y_offset in escape_directions:
            new_rect = mob["rect"][0].copy()
            new_rect.x += x_offset - data["Zoom_rect"].x
            new_rect.y += y_offset - data["Zoom_rect"].y

            if not any(new_rect.colliderect(displayed_rect) for displayed_rect in decorations.displayed_rects):
                self._update_mob_position(mob, x_offset, y_offset)
                return
    def update_visibility(self, screen, rect, id):
        screen_rect = screen.get_rect()
        if rect.colliderect(screen_rect):
            self.mobs[id]["visible"] = True
        else:
            self.mobs[id]["visible"] = False

    def knockback(self, victim, spaces):
        rects = victim['rect']
        push = {"Back": (0, -spaces),
                "Front": (0, spaces),
                "Left": (-spaces, 0),
                "Right": (spaces, 0)}
        direction = I.info.LAST_ORIENT[0].split(".")[0]
        for rect in rects:
            rect.x += push[direction][0]
            rect.y += push[direction][1]

    def remove_mob(self, mob_id):
        """Remove a mob from the list by id."""
        self.count = (self.count[0] - 1, self.count[1])
        self.mobs = [mob for mob in self.mobs if mob["id"] != mob_id]
    def deal_damage(self, victim, player, weapon, items, gifs):
        if weapon == "":
            # NOT SPELL AND NOT EFFECT DAMAGE
            if I.info.EQUIPED["Sword"] != 0:
                damage, speed, knockback, type = Ff.get_property(I.info.EQUIPED["Sword"], items, "WEAPON")
                damage = int(damage)
                speed = float(speed)
                knockback = int(knockback)
            else:
                damage = I.info.BASE_ATTACKING_DAMAGE
                knockback = I.info.BASE_KNOCKBACK
                type = "Blunt"
        elif "effect" in weapon:
            # EFFECT DAMAGE
            damage = 0.05
            knockback = 0
            type = weapon.split("_")[1]  # get's effect
        else:
            # SPELL DAMAGE
            damage = weapon["damage"]
            damage = random.randint(int(damage.split("d")[0]), int(damage.split("d")[1]))
            knockback = weapon["knockback"]
            type = weapon["type"]

        if victim["allignment"] == 5:
            victim["allignment"] = 6
        victim["hp"] = victim["hp"][0] - damage, victim["hp"][1]
        if victim["hp"][0] <= 0:
            gifs[type].start_gif = False
            self.remove_mob(victim["id"])
            player["Experience"] += victim["exp"]
            if isinstance(victim["drop"], tuple): # if victim drops not more than one item
                amount = victim["drop"][1] if random.randint(0, victim["drop"][2]-1) == 0 else 0
                br.add_to_backpack(victim["drop"][0], amount, items)  # Adds mob drops 1
                if amount != 0:
                    Ff.display_text_player("Recieved " + str(amount) + " " + str(victim["drop"][0]), 5000)
            else:
                # choose = random.randint(0, len(victim["drop"]) - 1)
                amount1 = victim["drop"][0][1] if random.randint(0, victim["drop"][0][2]) == 0 else 0
                br.add_to_backpack(victim["drop"][0][0], amount1, items)  # adds mob drops 2
                amount2 = victim["drop"][1][1] if random.randint(0, victim["drop"][1][2]) == 0 else 0
                br.add_to_backpack(victim["drop"][1][0], amount2, items)  # adds mob drops 3

                if amount1 != 0:
                    Ff.display_text_player("Recieved " + str(amount1) + " " + str(victim["drop"][0][0][:-1]), 5000)
                if amount2 != 0:
                    Ff.display_text_player("Recieved " + str(amount2) + " " + str(victim["drop"][1][0][:-1]), 5000)

            # gifs[type].start_gif = False

        elif "effect" not in weapon:
            self.knockback(victim, int(knockback))
            self.effect(victim, type)

    def effect(self, victim, type):
        if type == "Cold":
            duration = random.randint(1,3)
            if victim["effect"].get(type) == None:
                victim["effect"][type] = duration
            else:
                victim["effect"][type] += duration

        elif type == "Force":
            victim["effect"][type] = 1

        elif type == "Fire":
            duration = random.randint(1, 2)
            if victim["effect"].get(type) == None:
                victim["effect"][type] = duration
            else:
                victim["effect"][type] += duration


    def update_position(self, new_x, new_y, mob):
        mob['previous_pos'][0] = mob['current_pos'][0]
        mob['previous_pos'][1] = mob['current_pos'][1]
        mob['current_pos'][0] = new_x
        mob['current_pos'][1] = new_y
        for rect in mob["rect"]:
            rect.topleft = (new_x, new_y)
