from Values import Settings as S
from utils import Frequent_functions as Ff, Imports as I
class Room:
    def __init__(self):
        self.name = ""
        self.decor = []
        self.data = {}
        self.type = ""
        self.mobs = []
        self.background = ""
        self.room_dict = {}
        self.read_db()
        self.start_game = 1
    def read_db(self):
        db_data = Ff.read_data_from_db("rooms", ["name", "decor", "coordinates", "type", "background", "exit", "mobs"])
        for data in db_data:
            self.room_dict[data[0]] = {"decor": data[1],
                                        "coordinates": data[2],
                                        "type": data[3],
                                        "background": data[4],
                                       "exit": data[5],
                                       "mobs": data[6]
                                        }
    def select_room(self, name):
        previous_name = name  # Idiotic way
        if self.name != '':  # to solve the issue
            previous_name = self.name  # of the entry_pos being of the building that was rendered before rendering this new building.
        self.name = name
        self.decor = self.room_dict[name]["decor"].split(", ")
        self.type = self.room_dict[name]["type"]
        self.background = self.room_dict[name]["background"]
        self.mobs = self.room_dict[name]["mobs"]
        data_list = self.room_dict[name]["coordinates"].split(",,,")
        pos = self.room_dict[previous_name]["exit"].split(", ")
        if not S.GOD_MODE:
            values = previous_name.split("_")
            new_values = name.split("_")
            direction = (0, 0)
            if len(new_values) != 1 and len(values) != 1:
                direction = int(new_values[1]) - int(values[1]), int(new_values[2]) - int(values[2])
            # direction = int(new_values[1]) - int(values[1]), int(new_values[2]) - int(values[2])
            if self.start_game == 1:
                self.start_game = 0
            else:
                if direction != (0, 0):
                    starting_pos = {
                        (-1, 0): (800, 390),
                        (1, 0): (1, 390),
                        (0, -1): (330, 820),
                        (0, 1): (330, 1)
                                    }
                    offscreen = {
                        (-1, 0): (600, 0),
                        (1, 0): (-600, 0),
                        (0, -1): (0, 300),
                        (0, 1): (0, -330)
                    }
                    I.info.OFFSCREEN = offscreen[direction]
                    I.info.ENTRY_POS = starting_pos[direction]
                else:
                    I.info.OFFSCREEN = (0, 0)
                    # I.info.ENTRY_POS
                    I.info.ENTRY_POS = (int(pos[0]), int(pos[1]))
        for i in range(0, len(data_list)):
            if ",," in data_list[i]:
                self.data[self.decor[i]] = []
                mini_data_list = data_list[i].split(",,")
                for info in mini_data_list:
                    data = info.split(",")
                    x = int(data[0])
                    y = int(data[1])
                    img_x = float(data[2])
                    img_y = float(data[3])
                    rect_x = float(data[4])
                    rect_y = float(data[5])
                    self.data[self.decor[i]].append({"x": x, "y": y, "img_x": img_x, "img_y": img_y, "rect_x": rect_x, "rect_y": rect_y})
            else:
                data = data_list[i].split(",")
                x = int(data[0])
                y = int(data[1])
                img_x = float(data[2])
                img_y = float(data[3])
                rect_x = float(data[4])
                rect_y = float(data[5])
                self.data[self.decor[i]] = []
                self.data[self.decor[i]].append({"x": x, "y": y, "img_x": img_x, "img_y": img_y, "rect_x": rect_x, "rect_y": rect_y})
