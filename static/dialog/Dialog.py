# from scipy.cluster.hierarchy import complete

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
                # print(self.response[i])
                # print(text_list[i])
                # print(self.text)
                self.text[self.response[i]] = text_list[i]

        self.conv_key = "Start"  # key to start conversations


    def get_text(self):
        self.select_id()
        id = self.iteration
        key = self.conv_key.split("|")[0]
        if key == "Funds":
            self.iteration = "0"
            id = "0"
        # print(key, id)
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
            if self.iteration != 4:
                if I.info.QUESTS != [] and any(quest["GIVER"] == "Mayor" and quest["ITEM"] == "Meat0" for quest in I.info.QUESTS):
                    """iteration 0 is getting meat quest, iteration 1 means completed quest"""
                    self.iteration = 1
                elif I.info.QUESTS != [] and any(quest["GIVER"] == "Mayor" for quest in I.info.QUESTS) and any(completed_quest["ITEM"] == "Meat0" for completed_quest in I.info.COMPLETED_QUESTS):
                    self.iteration = 2
                elif I.info.COMPLETED_QUESTS != [] and any(completed_quest["GIVER"] == "Mayor" for completed_quest in I.info.COMPLETED_QUESTS):
                    self.iteration = 3
            if I.info.COMPLETED_QUESTS != [] and any(completed_quest["GIVER"] == "Mayor" for completed_quest in I.info.COMPLETED_QUESTS):
                if any(quest["TYPE"] == "GET" and quest["ITEM"] == "Slime Ball" and quest["COMPLETION"] >= 1 for quest in I.info.QUESTS):
                    self.iteration = 5
        elif self.name == "Tutorial Man":
            if I.info.tutorial_flag == 1 and I.info.QUESTS == []:
                self.iteration = 0
            else:
                if any(quest["GIVER"] == "Purple Wizard" for quest in I.info.QUESTS) or any(completed_quest["TYPE"] == "Tutorial" and completed_quest["ACTION"] != "EAT" for completed_quest in I.info.COMPLETED_QUESTS):
                    I.info.tutorial_flag = 0
                    if any(quest["ACTION"] == "WALK" and quest["COMPLETION"] >= 1 for quest in I.info.QUESTS) and self.iteration == 0:
                        """got reward for WALK quest"""
                        self.iteration = 1
                    elif any(completed_quest["TYPE"] == "Tutorial" and completed_quest["ACTION"] == "WALK" for completed_quest in I.info.COMPLETED_QUESTS) and self.iteration == 1:
                        """Got run quest"""
                        self.iteration = 2
                    elif any(quest["ACTION"] == "RUN" and quest["COMPLETION"] >= 1 for quest in I.info.QUESTS) and self.iteration == 2:
                        """Got reward for run quest"""
                        self.iteration = 3
                    elif any(completed_quest["TYPE"] == "Tutorial" and completed_quest["ACTION"] == "RUN" for completed_quest in I.info.COMPLETED_QUESTS) and self.iteration == 3:
                        self.iteration = 4
                    elif any(quest["ACTION"] == "PUNCH" and quest["COMPLETION"] >= 1 for quest in I.info.QUESTS) and self.iteration == 4:
                        self.iteration = 5
                    elif any(completed_quest["TYPE"] == "Tutorial" and completed_quest["ACTION"] == "PUNCH" for completed_quest in I.info.COMPLETED_QUESTS) and self.iteration == 5:
                        self.iteration = 6
                    elif any(quest["ACTION"] == "QUEST_BACKPACK" and quest["COMPLETION"] >= 1 for quest in I.info.QUESTS) and self.iteration == 6:
                        self.iteration = 7
                    elif any(completed_quest["TYPE"] == "Tutorial" and completed_quest["ACTION"] == "QUEST_BACKPACK" for completed_quest in I.info.COMPLETED_QUESTS) and self.iteration == 7:
                        self.iteration = 8
                    elif any(quest["ACTION"] == "EAT" and quest["COMPLETION"] >= 1 for quest in I.info.QUESTS) and self.iteration == 8:
                        self.iteration = 9
                    elif any(completed_quest["TYPE"] == "Tutorial" and completed_quest["ACTION"] == "EAT" for completed_quest in I.info.COMPLETED_QUESTS) and self.iteration == 9:
                        self.iteration = 10
                    # elif self.iteration == 10:
                    #     self.iteration = 11
                else:
                    self.iteration = 11
        elif self.name == "Castle_Guard":
            if I.info.CRIMINAL["Charge"] != "" and I.info.CURRENT_ROOM["Type"] != "Prison":
                self.iteration = 1
            elif I.info.CURRENT_ROOM["Type"] == "Prison":
                self.iteration = 2
            else:
                self.iteration = 0
        elif self.name == "Gwen":
            if any(quest["GIVER"] == "Gwen" and quest["ITEM"] == "Stick" and quest["COMPLETION"] >= 1 for quest in I.info.QUESTS):
                if any(quest["ITEM"] == "Light Wood" and quest["COMPLETION"] >= 1 for quest in I.info.QUESTS):
                    self.iteration = 2
            elif "Wooden Axe" in list(I.info.BACKPACK_CONTENT.keys()) and not any(quest["GIVER"] == "Gwen" for quest in I.info.QUESTS) and not any(completed_quest["GIVER"] == "Gwen" and completed_quest["ITEM"] == "Stick" for completed_quest in I.info.COMPLETED_QUESTS):
                self.iteration = 1
            else:
                self.iteration = 0



    def has_conversation_ended(self):
        self.select_id()
        id = self.iteration
        key = self.conv_key.split("|")[0]
        # print("check if continue: ", key + str(id), self.text.keys())
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