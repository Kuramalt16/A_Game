from Values import Settings as S
class Items:
    def __init__(self):
        self.item_dict = {}
        self.add_items()

    def add_items(self):
        for name, path in S.ITEM_PATHS.items():
            if ".txt" in path:
                with open(path, 'r') as file:
                    lines = file.readlines()
                    self.item_dict[name[:-5]] = {"Cost": lines[1].split("=")[1][:-2],
                                            "Properties": lines[2].split("=")[1][:-2],
                                            "Aquire": lines[3].split("=")[1][:-2]}

