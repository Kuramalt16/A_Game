from Values import Settings as S
from utils import Frequent_functions as Ff, Imports as I
class Items:
    def __init__(self):
        self.item_dict = {}
        self.add_items()

    def add_items(self):
        db_data = Ff.read_data_from_db("items", ["name", "cost", "properties", "aquire", "path", "describtion"])
        for data in db_data:
            self.item_dict[data[0]] = {"Cost": data[1],
                                    "Properties": data[2],
                                    "Aquire": data[3],
                                    "path": data[4],
                                    "describtion": data[5]
                                       }
            if "HARVEST" in data[3]:
                harvestable = data[3][8:].split(",,")[0]
                I.info.HARVESTABLE[harvestable] = data[0]

