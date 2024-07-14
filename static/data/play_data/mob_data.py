import random
from utils import Imports as I
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
        "speed": self.speed,
        "effect": "",
        "allignment": temp_allignment,
        "gif_frame": (0, S.MOB_PATH[self.name][1]),
        "visible": False,
        "rect": [],  # Placeholder for the Pygame rect object
        "image": [],  # Placeholder for the Pygame image list
        "previous_pos": (0, 0, 0, 0),
        "current_pos": (0, 0, 0, 0),

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

    def move_mobs_randomly(self):
        """Move all mobs by the given offsets."""
        for mob in self.mobs:
            if not mob["visible"]:
                # speed = mob["speed"]
                x = random.randint(-1, 1)
                y = random.randint(-1, 1)
                for rect_id in range(len(mob["rect"])):
                    mob["rect"][rect_id].x += x
                    mob["rect"][rect_id].y += y

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
    def deal_damage(self, victim, player, weapon, gifs):
        if weapon == "":
            damage = 2 / 3
            knockback = 1
            type = "Blunt"
        else:
            damage, type, route, mana_cost, knockback = weapon.split(" ")
            damage = random.randint(int(damage.split("d")[0]),int(damage.split("d")[1]))

        victim["hp"] = victim["hp"][0] - damage, victim["hp"][1]
        if victim["hp"][0] <= 0:
            self.remove_mob(victim["id"])
            player["Experience"] += victim["exp"]
            if isinstance(victim["drop"], tuple):
                amount = victim["drop"][1] if random.randint(0, victim["drop"][2]-1) == 0 else 0
                br.add_to_backpack(victim["drop"][0], amount)
                if amount != 0:
                    I.info.TEXT.append("Recieved " + str(amount) + " " + str(victim["drop"][0]) + ",,5000")
            else:
                choose = random.randint(0, len(victim["drop"]) - 1)
                amount = victim["drop"][choose][1] if random.randint(0, victim["drop"][choose][2] - 1) == 0 else 0
                br.add_to_backpack(victim["drop"][choose][0], amount)
                if amount != 0:
                    I.info.TEXT.append("Recieved " + str(amount) + " " + str(victim["drop"][choose][0][:-1]) + ",,5000")
            gifs[type].start_gif = False
        else:
            self.knockback(victim, int(knockback))
            self.effect(victim, type)

    def effect(self, victim, type):
        if type == "Cold":
            print("Cold")
        elif type == "Force":
            print("Force")
        elif type == "Fire":
            print("Fire")


    def update_position(self, new_x, new_y, mob):
        mob['previous_pos'][0] = mob['current_pos'][0]
        mob['previous_pos'][1] = mob['current_pos'][1]
        mob['current_pos'][0] = new_x
        mob['current_pos'][1] = new_y
        for rect in mob["rect"]:
            rect.topleft = (new_x, new_y)
