import random

from utils import Frequent_functions as Ff, Imports as I
class Decorations:
    def __init__(self):
        self.decor_dict = {}
        self.create_place_holders()
        self.effected_decor = {}
        self.displayed_rects = []
        self.displayed_rects_full = []
        self.names_with_id = {}
        self.health = 0

    def create_place_holders(self):
        db_data = Ff.read_data_from_db("decor", ["name", "action", "health", "type", "path"])
        for data in db_data:
            if data[3] in ["Nature", "House", "Door", "Trap Door", "Stairs"]:
                self.decor_dict[data[0]] = {"action": data[1],
                                           "health": data[2],
                                            "type": data[3],
                                            "path": data[4]
                                            }
                if "HARVESTABLE:" in data[1] and I.info.HARVESTABLE.get(data[0]) == None:
                    I.info.HARVESTED_OBJECTS[data[0]] = []
            elif data[3] in ["Furniture", "Appliance", "NPC", "NPC_Mob"]:
                self.decor_dict[data[0]] = {"action": data[1],
                                            "health": data[2],
                                            "type": data[3],
                                            "path": data[4]
                                            }

            self.health = data[2]

    def generate_decor(self, name, num_of_items, background_size, path):
        for i in range(num_of_items):
            x = random.randint(100, background_size[0] - 200)
            y = random.randint(100, background_size[1] - 200)
            image = I.pg.image.load(path).convert_alpha()
            rect = image.get_rect(topleft=(x, y))
            self.decor_dict[name][i] = {"name": name, "id": i, "image": image, "rect": rect, "effect": "", "health": self.health}

    def place_decor_by_coordinates(self,  x, y, path, scale, rect_scale):
        image = I.pg.image.load(path).convert_alpha()
        img_rect = image.get_rect(topleft=(x, y))
        image = I.pg.transform.scale(image, (img_rect.w * scale[0], img_rect.h * scale[1]))
        width = img_rect.w * rect_scale[0]
        height = img_rect.h * rect_scale[1]
        rect = I.pg.Rect(img_rect.x, img_rect.y, width, height)
        return image, rect

    def place_batches_decor_by_coordinates(self, name,  x, y, path, scale, rect_scale):
        image = I.pg.image.load(path).convert_alpha()
        rect = image.get_rect(topleft=(x, y))
        image = I.pg.transform.scale(image, (rect.w * scale[0], rect.h * scale[1]))
        rect.w = rect.w * rect_scale[0]
        rect.h = rect.h * rect_scale[1]
        self.decor_dict[name][0] = {"image": image, "rect": rect}
