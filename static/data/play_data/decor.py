import random
from utils import Frequent_functions as Ff, Imports as I
class Decorations:
    def __init__(self):
        self.decor_dict = {}
        self.create_place_holders()
        self.effected_decor = {}
        self.displayed_rects = []

    def create_place_holders(self):
        db_data = Ff.read_data_from_db("decor", ["name", "harvestable", "flamable"])
        for data in db_data:
            self.decor_dict[data[0]] = {"harvestable": data[1],
                                       "flamable": data[2],
                                        }
            if "HARVESTABLE:" in data[1]:
                I.info.HARVESTED_OBJECTS[data[0]] = []
            elif "ENTERABLE:" in data[1]:
                if ",," in data[1]:
                    enter_through = data[1].split(",,")[0]
                I.info.ENTERABLE.append(data[0])
    def generate_decor(self, name, num_of_items, background_size, path):
        for i in range(num_of_items):
            x = random.randint(0, background_size[0] - 100)
            y = random.randint(0, background_size[1] - 100)
            image = I.pg.image.load(path).convert_alpha()
            rect = image.get_rect(topleft=(x, y))
            self.decor_dict[name][i] = {"name": name, "id": i, "image": image, "rect": rect, "effect": ""}

    def place_decor_by_coordinates(self, name,  x, y, path, scale, rect_scale):
        image = I.pg.image.load(path).convert_alpha()
        rect = image.get_rect(topleft=(x, y))
        image = I.pg.transform.scale(image, (rect.w * scale[0], rect.h * scale[1]))
        rect.w = rect.w * rect_scale[0]
        rect.h = rect.h * rect_scale[1]
        self.decor_dict[name][0] = {"image": image, "rect": rect}
