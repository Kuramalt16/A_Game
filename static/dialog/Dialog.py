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
                # print(self.text[self.response[i]])
        # self.text = {
        #     "Sign": [{
        #         "Start": ("Hi, looks like you died. Maybe next time try dodging the blow instead of kissing it :). \n Anyways, see that big purple portal? interact with it while standing on it and you will be revived. \n But you will loose all the items you were carrying. \n Alternatively find your grave stone and interract with it. This way you will keep all of your useless stuff. \n Don't rush to comeback. \n With love -S!", "Skip", "")
        #               }],
        #     # "Shop": [("Hello Traveler, looking for a drink?", "Yes", "No"), (("Wonderful. \n We have Ale that goes for 5 Silver per bottle", "Very well, maybe some other time"), "Goodbye/Sure", "I will kill you/What else do you have?"), ("Here You go")]
        #     "Barkeep": [
        #         {
        #             "Start": ("Hello Traveler, looking for a drink?", "Yes", "No"),
        #             "Yes": ("Wonderful. We have Ale that goes for 5 Silver per bottle", "Sounds good", "What else do you have?"),
        #             "No": ("Very well, maybe some other time", "Goodbye", "Fuck you"),
        #             "What else do you have?": ("We have fresh cooked meat that goes for 30 Silver", "Sure", "Not interested"),
        #             "Funds": ("Sorry it appears you don't have enough funds", "Apologies", "Fuck"),
        #             "Sounds good": ("{Acquired Ale}", "Close", "item,,buy,,0.5,,Ale"),
        #             "Sure": ("{Acquired Meat Cooked}", "Close", "item,,buy,,3,,Meat0_Cooked"),
        #
        #         },
        #         {
        #             "Start": ("Hello again Traveler, looking for a drink?", "Yes", "No"),
        #             "Yes": ("Wonderful. We have Ale that goes for 5 Silver per bottle", "Sounds good",
        #                     "What else do you have?"),
        #             "No": ("Very well, maybe some other time", "Goodbye", "Fuck you"),
        #             "What else do you have?": (
        #             "We have fresh cooked meat that goes for 30 Silver", "Sure", "Not interested"),
        #             "Funds": ("Sorry it appears you don't have enough funds", "Apologies", "Fuck"),
        #             "Sounds good": ("{Acquired Ale}", "Close", "item,,buy,,0.5,,Ale"),
        #             "Sure": ("{Acquired Pork}", "Close", "item,,buy,,3,,Meat0_Cooked"),
        #
        #         },
        #         {
        #             "Start": ("Hello again Traveler, looking for a drink?", "Yes", "No"),
        #             "No": ("Very well", "Goodbye", "Fuck you"),
        #             "Yes": ("Maybe you have had enough?", "Never", "Just a few more"),
        #             "Never": ("I'm sorry I don't think I can sell any more alcohol to you", "Why?", "Fuck you"),
        #             "Why?": ("Because you already have five bottles and I don't that it's healthy to buy more", "...", "Can i have some food then?"),
        #             "Can i have some food then?": ("No problem, it's 30 Silver", "Here you go", "I changed my mind"),
        #             "Just a few more": ("Okey, but only a few", "Just give me the booze", "Don't worry i know how to pace myself"),
        #             "Don't worry i know how to pace myself": ("{Acquired Ale}", "Close", "item,,buy,,0.5,,Ale"),
        #             "Just give me the booze": ("{Acquired Ale}", "Close", "item,,buy,,0.5,,Ale"),
        #             "Here you go": ("{Acquired Pork}", "Close", "item,,buy,,3,,Meat0_Cooked"),
        #             "Funds": ("Sorry it appears you don't have enough funds", "Apologies", "Fuck"),
        #         },
        #         {
        #             "Start": ("Hello again Traveler, looking for a drink?", "Yes", "No"),
        #             "No": ("Very well", "Goodbye", "Fuck you"),
        #             "Yes": ("Alcohol will not fill the hole inside you friend", "I don't care", "What?"),
        #             "I don't care": ("I'm sorry you are cut off I will not sell to you", "Asshole", "Very well"),
        #             "What?": ("You travel alone and you buy lots of ale it's not difficult to understand that something "
        #                       "is hurting inside you \n maybe it's these harsh times, maybe it's the loss of a loved"
        #                       " one \n or maybe its hatred for yourself, maybe you believe you could have changed the"
        #                       " outcome of some event \n and you blame yourself. It's not your fault dear traveler, \n"
        #                       " it's not your fault", "...", "Very well"),
        #             "...": ("If you need a place to stay you can use the living quarters free of charge, \n if you need a job speak you need only ask \n if you need a friend, you have one", "What's your name?", "Thank you"),
        #             "What's your name?": ("It's Joseph The Loner that's what they call me", "Why do they call you like that?", "Thank you"),
        #             "Why do they call you like that?": ("A story for another time friend", "Understood", "Thank you"),
        #             "Thank you": ("There is no need for gratitude friend", "*Smile*", ""),
        #             "Funds": ("Sorry it appears you don't have enough funds", "Apologies", "Fuck"),
        #
        #         },
        #              ],
        #     "Old man in a chair": [
        #         {
        #             "Start": ("Hello Traveler, want some work?", "Yes", "No"),
        #             "Yes": ("Very well. Bring me 5 pig meat, im hungry", "Ok", "How much are you paying?"),
        #             "No": ("Your loss", "Goodbye", "I don't think so"),
        #             "How much are you paying?": ("Depends on the quality of the meat, now go and stop bothering me", "...", "Fuck you im not your servant"),
        #             "Ok": ("{Acquired quest}", "Close", "quest_Old man in a chair,,Get,,5,,Meat0"),
        #             "...": ("{Acquired quest}", "Close", "quest_Old man in a chair,,Get,,5,,Meat0"),
        #         },
        #         {
        #             "Start": ("Back again? Want some work?", "Yes", "No"),
        #             "Yes": ("Ok. Bring me 5 pig meat, im hungry", "Ok", "How much are you paying?"),
        #             "No": ("Your loss", "Goodbye", "I don't think so"),
        #             "How much are you paying?": (
        #             "Depends on the quality of the meat, now go and stop bothering me", "...", "Fuck you im not your servant"),
        #             "Ok": ("{Acquired quest}", "Close", "quest_Old man in a chair,,Get,,5,,Meat0"),
        #             "...": ("{Acquired quest}", "Close", "quest_Old man in a chair,,Get,,5,,Meat0"),
        #         },
        #         {
        #             "Start": ("Do you have my meat?", "Yes", "No"),
        #             "Yes": ("Liar, stop wasting my time", "Jerk", "..."),
        #             "No": ("Well then go and get it", "Jerk", "No need to be such a bastard"),
        #             "No need to be such a bastard": ("Who are you calling a bastard smart mouth, do you know who i am?!", "Should i care?", "I dont"),
        #             "Should i care?": ("I'm the town mayor and unless you want to be kicked out of this town you should check your tone", "Big deal", "Such a big role for suck a small man?"),
        #         },
        #         {
        #             "Start": ("Do you have my meat?", "Yes", "No"),
        #             "Yes": ("Give it here if it's not of quality you won't recieve any payment", "Here", "Take it you geezer"),
        #             "No": ("Well then stop wasting my time, im a busy man", "Jerk", "I apologize"),
        #             "Here": ("Splendid meat, here is your payment 50 Sp", "Thanks", "I want more"),
        #             "I want more": ("Then get me more meat", "...", "Or i could kill you"),
        #             "Or i could kill you": ("You're welcome to try", "ha ha", "..."),
        #             "Thanks": ("{Received 50 Sp}", "Close", "questCompleted_Old man in a chair ,,Receive,,5,,Gold"),
        #             "...": ("{Received 50 Sp}", "Close", "questCompleted_Old man in a chair,,Receive,,5,,Gold"),
        #             "Take it you geezer": ("What did you say to me?!", "Nothing", "I said TAKE IT YOU GEEZER"),
        #             "Nothing": ("{Received 50 Sp}", "Close", "questCompleted_Old man in a chair,,Receive,,5,,Gold"),
        #             "I said TAKE IT YOU GEEZER": ("YOU DARE? Take your filthy payment and leave", "....", "Filthy old man"),
        #             "....": ("{Received 30 Sp}", "Close", "questCompleted_Old man in a chair,,Receive,,2,,Gold"),
        #             "Filthy old man": ("{Received 20 Sp}", "Close", "questCompleted_Old man in a chair,,Receive,,2,,Gold"),
        #         },
        #         {
        #             "Start": ("I don't need you now, get lost", "Jerk", "..."),
        #         },
        #     ],
        #              }
        self.conv_key = "Start" # key to start conversations
        # self.id = {
        #     "Sign": 0,
        #     "Barkeep": 0,
        #     "Old man in a chair": 0
        #            }

    def get_text(self):
        self.select_id()
        id = self.iteration
        key = self.conv_key.split("|")[0]
        if key == "Funds":
            self.iteration = "0"
            id = "0"
        # print("id, key: ", id, key)
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
        response = response[1], response[2]
        # print("responses:", response)
        return response

    def select_id(self):
        if self.name == "Joseph":
            if I.info.BACKPACK_CONTENT.get("Ale") != None:
                amount, x, y = I.info.BACKPACK_CONTENT["Ale"]
                if amount >= 5:
                    self.iteration = 1
                if amount >= 10:
                    self.iteration = 2

        # elif I.info.COMPLETED_QUESTS != 0:
        #     if I.info.COMPLETED_QUESTS[0] == self.name:  #If quest givver hidden in completed quests matches the person im talking to then reward
        #         self.iteration = 3
        #         self.data = (None, None, None, None)
        elif self.name == "Mayor":
            if self.iteration != 3:
                if I.info.COMPLETED_QUESTS != 0 and I.info.COMPLETED_QUESTS[1] == self.name:
                    self.iteration = 1
                    I.info.QUESTS = 0
                elif I.info.QUESTS != 0 and I.info.QUESTS != [""] and I.info.QUESTS[1] == self.name:
                    self.iteration = 2

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