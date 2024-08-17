from Values import Settings as S
from utils import Frequent_functions as Ff, Imports as I
class Room:
    def __init__(self):
        self.name = ""
        self.decor = []
        self.data = {}
        self.type = ""
        self.background = ""
        self.room_dict = {}
        self.read_db()
    def read_db(self):
        db_data = Ff.read_data_from_db("rooms", ["name", "decor", "coordinates", "type", "background", "exit"])
        for data in db_data:
            self.room_dict[data[0]] = {"decor": data[1],
                                        "coordinates": data[2],
                                        "type": data[3],
                                        "background": data[4],
                                       "exit": data[5]
                                        }
    def select_room(self, name):
        previous_name = name  # Idiotic way
        if self.name != '':  # to solve the issue
            previous_name = self.name  # of the entry_pos being of the building that was rendered before rendering this new building.
        self.name = name
        self.decor = self.room_dict[name]["decor"].split(", ")
        self.type = self.room_dict[name]["type"]
        self.background = self.room_dict[name]["background"]
        data_list = self.room_dict[name]["coordinates"].split(",,,")
        pos = self.room_dict[previous_name]["exit"].split(", ")
        if not S.GOD_MODE:
            I.info.ENTRY_POS = [int(pos[0]), int(pos[1])]

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
