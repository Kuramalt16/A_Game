import random
from utils import Imports as I

class Mob:
    def __init__(self, name, hp, exp, allignment, count):
        self.name = name
        self.hp = hp
        self.exp = exp
        self.allignment = allignment
        self.count = count
        self.mobs = [self.create_mob(i) for i in range(count)]  # Create initial list of mobs

    def create_mob(self, id):
        """Create a single mob instance with unique id."""
        return {
        "id": id,
        "hp": self.hp,
        "visible": False,
        "rect": [],  # Placeholder for the Pygame rect object
        "image": [],  # Placeholder for the Pygame image list
        "previous_pos": (0, 0, 0, 0),
        "current_pos": (0, 0, 0, 0)
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

    def move_mobs_randomly(self, x_offset, y_offset):
        """Move all mobs by the given offsets."""
        for mob in self.mobs:
            if not mob["visible"]:
                for rect_id in range(len(mob["rect"])):
                      mob["rect"][rect_id].x += x_offset
                      mob["rect"][rect_id].y += y_offset

    def update_visibility(self, screen, rect, id):
        screen_rect = screen.get_rect()
        if rect.colliderect(screen_rect):
            self.mobs[id]["visible"] = True
        else:
            self.mobs[id]["visible"] = False

    def kill_mobs(self, combat_rect, damage):
        """Update the state of the mobs, e.g., handling collisions."""
        killed_mobs = []
        for mob in self.mobs:
            if mob["visible"] and combat_rect.colliderect(mob["rect"][9]):
                mob["hp"] -= damage
                if mob["hp"] <= 0:
                    killed_mobs.append(mob["id"])
        for mob_id in killed_mobs:
            self.remove_mob(mob_id)
        return killed_mobs
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
        self.count -= 1
        self.mobs = [mob for mob in self.mobs if mob["id"] != mob_id]
    def deal_damage(self, victim):
        if I.info.EQUIPED["Hand1"] == 0 and I.info.EQUIPED["Hand2"] == 0:
            damage = 2 / 3
            victim["hp"] -= damage
            if victim["hp"] <= 0:
                self.remove_mob(victim["id"])
            else:
                self.knockback(victim, 2)



    def update_position(self, new_x, new_y, mob):
        mob['previous_pos'][0] = mob['current_pos'][0]
        mob['previous_pos'][1] = mob['current_pos'][1]
        mob['current_pos'][0] = new_x
        mob['current_pos'][1] = new_y
        for rect in mob["rect"]:
            rect.topleft = (new_x, new_y)
