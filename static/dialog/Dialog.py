from Values import Settings as S
from utils import Frequent_functions as Ff, Imports as I

class Dialog():
    def __init__(self, name):
        self.name = name
        self.data = None, None, None, None
        self.text = {}
        self.response = []
        self.iteration = 0
        self.get_dialog_data_db(name)
        self.friendlyness = 0
        self.interaction_count = 0


    def get_dialog_data_db(self, name):
        data = Ff.read_one_column_from_db("conversations", name)
        if data != []: # if npc has conversations
            for response in data[1].split(",, "):
                for res in response.split(", "):
                    self.response.append(res)  # responses (for mapping what responses lead to what text)
            # print(self.response)

            text_list = []
            for text in data[2].split(",,, "):  # text__res1__res2 list of text based on responses chosen
                for t in text.split(",, "):
                    text_list.append(t)
            for i in range(len(self.response)):
                self.text[self.response[i]] = text_list[i]

        self.conv_key = "Start"  # key to start conversations


    def get_text(self):
        self.select_id()
        id = self.iteration
        key = self.conv_key.split("|")[0]
        if key == "Funds":
            self.iteration = "0"
            id = "0"
        # print("text: ", self.text[key + str(id)])

        text = self.text[key + str(id)]

        text = text.split("__")[0]
        if "\\n" in text:
            text = text.replace("\\n", "\n")
        if key == "Start" and self.interaction_count > 0: # handles hello again traveler
            text = text.replace("Hello", "Hello again")

        return text
    def select_response(self):
        id = self.iteration
        key = self.conv_key.split("|")[0]
        response = self.text[key + str(id)].split("__")

        """ IF response only contains 3 values (text, resp1, resp2), then fit them into the slots and return,
            If response contains 2 values (text, resp) then make resp2 invisible
            if response contains 1 value then no responses can be said
        """
        if len(response) == 3:
            response = response[1], response[2]
        elif len(response) == 2:
            response = response[1], ""
        else:
            response = ("", "")
        return response

    def select_id(self):
        if self.name == "Joseph":
            if I.info.BACKPACK_CONTENT.get("Ale") != None:
                amount, x, y = I.info.BACKPACK_CONTENT["Ale"]
                if amount >= 5:
                    self.iteration = 1
                if amount >= 10:
                    self.iteration = 2
                    I.info.TITLES.append("Alcoholic")
        elif self.name == "Mayor":
            if self.iteration != 3:
                if I.info.COMPLETED_QUESTS != 0 and I.info.COMPLETED_QUESTS["GIVER"] == self.name and I.info.COMPLETED_QUESTS["ITEM"] == "Meat0":
                    """have completed quests and the quest giver was joseph"""
                    self.iteration = 1
                    I.info.QUESTS = 0
                elif I.info.QUESTS != 0 and I.info.QUESTS != [""] and I.info.QUESTS["GIVER"] == self.name and I.info.COMPLETED_QUESTS["ITEM"] == "Meat0":
                    self.iteration = 2
                if I.info.COMPLETED_QUESTS != 0 and I.info.COMPLETED_QUESTS["REWARD"] == "CLAIMED" and I.info.COMPLETED_QUESTS["GIVER"] == self.name:
                    self.iteration = 3
            if I.info.COMPLETED_QUESTS != 0 and I.info.COMPLETED_QUESTS["GIVER"] == self.name:
                if I.info.COMPLETED_QUESTS["ITEM"] == "Slime Ball" and I.info.COMPLETED_QUESTS["REWARD"] != "CLAIMED":
                    self.iteration = 5
        elif self.name == "Tutorial Man":
            if I.info.COMPLETED_QUESTS != 0:
                if I.info.COMPLETED_QUESTS["ACTION"] == "WALK" and I.info.COMPLETED_QUESTS["REWARD"] != "CLAIMED":
                    self.iteration = 1
                elif I.info.COMPLETED_QUESTS["ACTION"] == "WALK" and I.info.COMPLETED_QUESTS["REWARD"] == "CLAIMED":
                    self.iteration = 2
                elif I.info.COMPLETED_QUESTS["ACTION"] == "RUN" and I.info.COMPLETED_QUESTS["REWARD"] != "CLAIMED":
                    self.iteration = 3
                elif I.info.COMPLETED_QUESTS["ACTION"] == "RUN" and I.info.COMPLETED_QUESTS["REWARD"] == "CLAIMED":
                    self.iteration = 4
                elif I.info.COMPLETED_QUESTS["ACTION"] == "PUNCH" and I.info.COMPLETED_QUESTS["REWARD"] != "CLAIMED":
                    self.iteration = 5
                elif I.info.COMPLETED_QUESTS["ACTION"] == "PUNCH" and I.info.COMPLETED_QUESTS["REWARD"] == "CLAIMED":
                    self.iteration = 6
                elif I.info.COMPLETED_QUESTS["ACTION"] == "QUEST_BACKPACK" and I.info.COMPLETED_QUESTS["REWARD"] != "CLAIMED":
                    self.iteration = 7
                elif I.info.COMPLETED_QUESTS["ACTION"] == "QUEST_BACKPACK" and I.info.COMPLETED_QUESTS["REWARD"] == "CLAIMED":
                    self.iteration = 8
                elif I.info.COMPLETED_QUESTS["ACTION"] == "EAT" and I.info.COMPLETED_QUESTS["REWARD"] != "CLAIMED":
                    self.iteration = 9
                elif I.info.COMPLETED_QUESTS["ACTION"] == "EAT" and I.info.COMPLETED_QUESTS["REWARD"] == "CLAIMED":
                    self.iteration = 10
        elif self.name == "Castle_Guard":
            if "Criminal|0" in I.info.TITLES:
                self.iteration = 1

    def has_conversation_ended(self):
        self.select_id()
        id = self.iteration
        key = self.conv_key.split("|")[0]
        # print("dictionary: ", self.text)
        # print("list of posible responses: ", list(self.text.keys()))
        # print("has conv ended key: ",key + str(id))
        if key + str(id) not in list(self.text.keys()):
            # print("Friendlyness: ", self.friendlyness)
            self.interaction_count += 1
            # print("interraction count: ", self.interaction_count)
            return True
        else:
            return False

def read_db():
    db_data = Ff.read_data_from_db("npc", ["name", "type", "quests"])
    npc_dict = {}
    for data in db_data:
        npc_dict[data[0]] = {"type": data[1],
                             "quest": data[2],
                             "dialog": Dialog(data[0])
                             }
        # print(data[0], npc_dict[data[0]]["dialog"])
    return npc_dict