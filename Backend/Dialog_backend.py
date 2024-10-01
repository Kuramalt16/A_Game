
from utils import Imports as I, Frequent_functions as Ff
from Render import Background_Render as br
from Values import Settings as S
from Backend import Play

def check_quest_completion():
    remainder = 0
    if I.info.QUESTS != 0 and I.info.QUESTS["TYPE"] == "GET":
        if I.info.BACKPACK_CONTENT.get(I.info.QUESTS["ITEM"]) == None:
            amount = 0
        else:
            amount, x, y = I.info.BACKPACK_CONTENT[I.info.QUESTS["ITEM"]]
        remainder = float(amount) / float(I.info.QUESTS["AMOUNT"])
        I.info.QUESTS["COMPLETION"] = remainder
    elif I.info.QUESTS != 0 and I.info.QUESTS["TYPE"] == "Tutorial":
        remainder = float(I.info.QUESTS["COMPLETION"])
    if remainder >= 1:
        I.info.COMPLETED_QUESTS = I.info.QUESTS
        remainder = 1
    return remainder

def init_dialog(name, player, screen, npc, items, decorations, data, gifs, rooms, clock, spells):
    dialog_obj = npc[name]["dialog"]
    I.info.tutorial_flag = 0
    dialog_obj.name = name
    check_quest_completion()
    handdle_sign_display(screen, dialog_obj, player, items, decorations, data, gifs)
    handle_dialog_outcome(dialog_obj, player, screen, items, npc, rooms, clock, data, spells)

    dialog_obj.conv_key = "Start"
def handle_functions_in_text(text, response, dialog, screen, items, decorations, data, gifs):
    """Function inside the text handler"""
    player = data["Player"]
    running = True


    if "{REWARD}" in text:
        """CHANGES {REWARD} with reward from the completed quest"""
        quest_reward = I.info.COMPLETED_QUESTS["REWARD"]
        if "{" in quest_reward:
            quest_reward = quest_reward.replace("Sp", "")
            if "Friendlyness" in quest_reward:
                quest_reward = quest_reward.replace("{Friendlyness}", "")
                sign = quest_reward[-1]
                quest_reward = quest_reward[:-1]
                if sign == "*":
                    quest_reward = str(float(quest_reward) + 5 * dialog.friendlyness) + " Sp"
        text = text.replace("{REWARD}", quest_reward)
    if "{Tutorial COMPLETED}" in text:
        gifs["Tutorial Man"] = gifs["Tutorial ManTeleport"]
        gifs["Tutorial Man"].repeat = 999
        gifs["Tutorial Man"].Start_gif("Tutorial Man", 0)
        Ff.update_map_view(0, "Tutorial Man", gifs, "remove_gif")
    if "COST" in text[text.index("{") + 1:text.index("}")]:
        """ CHANGE THE {COST|Item} to an actual value of the item"""
        word, item = text[text.index("{") + 1:text.index("}")].split("|")
        cost = items.item_dict[item]["Cost"]
        text = text.replace(text[text.index("{"):text.index("}") + 1], str(cost))
    elif "{CRIME_FINE}" in text:
        text = text.replace("{CRIME_FINE}", "10 Gp") # Needs updating with more crimes
        print(I.info.CRIMINAL)
    elif response[1] != '':
        # handles other actions
        """IF the text had a function like: {Acquired quest} it takes the second response as data and puts it into dialog.data and makes it invisible to the user"""
        dialog.data = response[1].split("|")
        response = response[0], ""
        if dialog.data[0] == "random":
            rand_addon = str(I.random.randint(0, 1))
            dialog.conv_key = dialog.conv_key.split("|")[0] + "-" + rand_addon
            dialog.data = (None, None, None, None)
            handdle_sign_display(screen, dialog, data["Player"], items, decorations, data, gifs)
            running = False
        elif dialog.data[0] == "Crime":
            if dialog.data[1] == "PayFine":
                print(I.info.CRIMINAL)
                if player["Gold"] < 10:
                    dialog.conv_key = "Funds"
                    dialog.data = (None, None, None, None)
                    text = dialog.get_text()
                    response = dialog.select_response()
                    response = response[0], ""
        elif len(dialog.data) > 2 and dialog.data[2] == "Cost":
            cost = items.item_dict[dialog.data[3]]["Cost"] / 10  # conversion from SILVER to GOLD
            dialog.data = dialog.data[0], dialog.data[1], cost, dialog.data[3]
        if len(dialog.data) > 2 and dialog.data[0:2] == ('item', 'buy') and float(dialog.data[2]) > float(player["Gold"]):
            dialog.conv_key = "Funds"
            dialog.data = (None, None, None, None)
            text = dialog.get_text()
            response = dialog.select_response()
        if "{SHOP}" in text:
            running = False
            dialog.data = ("shop", "Armory", None, None)
            return text, response, running
        if dialog.data[1] != None and "folower" in dialog.data[1]:
            x = decorations.decor_dict[dialog.data[2]][0]["rect"].x
            y = decorations.decor_dict[dialog.data[2]][0]["rect"].y
            I.info.FOLLOWER = {
                "Name": dialog.data[2],
                "current_pos": (x, y),
                "target_pos": (0, 0),
                "orientation": [],
                "aggressive": {
                    "attack": False,
                    "mob": 0,
                    "mob_pos": (0, 0),
                    "class": 0
                }
            }
            del decorations.decor_dict[dialog.data[2]][0]
            # I.pg.time.set_timer(I.pg.USEREVENT + 12, 2000)  # 5 sec
            I.th.start_thread(2000, "folower", data)

    return text, response, running
def handdle_sign_display(screen, dialog, player, items, decorations, data, gifs):
    # print(dialog.type, dialog.data, dialog.conv_key)
    # print("Name: id: ",dialog.name, dialog.iteration)
    text = dialog.get_text()
    response = dialog.select_response()
    print("Text:", text)
    print("response: ", response)
    running = True
    if "{" in text:
        text, response, running = handle_functions_in_text(text, response, dialog, screen, items, decorations, data, gifs)
        if not running:
            return
        print("Updated Text: ", text)
        print("Updated response: ", response)
    Ff.add_image_to_screen(screen, S.PLAYING_PATH["Text_bar"], (0, S.SCREEN_HEIGHT / 2, S.SCREEN_WIDTH, S.SCREEN_HEIGHT / 2))
    a = 0
    collumn = 100
    row = 100
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN and event.key == I.pg.K_x:
                if a > len(text):
                    running = False
                    dialog.conv_key = response[1]
                    dialog.friendlyness += int(response[1].split("|")[1])
            if event.type == I.pg.KEYDOWN and event.key == I.pg.K_c:
                if a > len(text):
                    running = False
                    dialog.conv_key = response[0]
                    if response[0] != "": # when talking to a sign there are no responses
                        dialog.friendlyness += int(response[0].split("|")[1])
            if event.type == I.pg.KEYDOWN and event.key == I.pg.K_z:
                for i in range(20):
                    if a + i >= len(text):
                        break
                    else:
                        if text[a + i] == "\n":
                            a += i
                            break
                else:
                     a += 20

        if not a > len(text) and text[a-1] == "\n":
            collumn += 20
            row = 100
            text = text[a+1:]
            a = 0
        Ff.display_text(screen, text[0:a], 10, (row, S.SCREEN_HEIGHT / 2 + collumn),  "black")

        if not a > len(text):
            I.pg.time.wait(10)
            a += 1

        # Handle resppmse
        if response[1] != "":
            Ff.display_text(screen, response[0].split("|")[0] + " [C]", 14, (80, S.SCREEN_HEIGHT / 2 + 280), "red")
            Ff.display_text(screen, response[1].split("|")[0] + " [X]", 14, (700, S.SCREEN_HEIGHT / 2 + 280), "red")
        else:
            Ff.display_text(screen, response[0].split("|")[0] + " [C]", 14,  (80, S.SCREEN_HEIGHT / 2 + 280), "red")

        I.pg.display.flip()

    if not running:
        if not dialog.has_conversation_ended():
            handdle_sign_display(screen, dialog, player, items, decorations, data, gifs)

def handle_dialog_outcome(dialog, player, screen, items, npc, rooms, clock, data, spells):
    if dialog.data != (None, None, None, None):
        if "quest" in dialog.data[0]:
            giver = dialog.data[1].replace("GIVER:", "")
            iteration = dialog.data[2].replace("ITERATION:", "")
            if npc[giver]["quest"] == False:
                print("ERROR DATASHEET FOR NPC DOESN'T HAVE A QUEST FOR THIS NPC")
                return

            if "questfail" in dialog.data[0]:
                I.info.QUESTS = 0
                dialog.iteration = 0
                dialog.data = (None, None, None, None)
            elif "questcomplete" in dialog.data[0]:
                reward = I.info.COMPLETED_QUESTS["REWARD"]
                if "Gp" in reward:
                    reward = reward.replace("Gp", "")
                    currency = " Gp"
                    player["Gold"] += float(reward)
                if "Sp" in reward:
                    reward = reward.replace("Sp", "")
                    currency = " Sp"
                    if "Friendlyness" in reward:
                        reward = reward.replace("{Friendlyness}", "")
                        sign = reward[-1]
                        reward = reward[:-1]
                        if sign == "*":
                            reward = float(reward) + 5 * dialog.friendlyness
                    player["Gold"] += round(float(reward) / 10, 2)
                    player["Gold"] = round(player["Gold"], 2)
                Ff.display_text_player("Recieved " + str(reward) + currency + " for completing a quest", 4000)
                I.info.COMPLETED_QUESTS["REWARD"] = "CLAIMED"
                # if dialog.data[2] == "Silver":
                #     player["Gold"] += float(dialog.data[1])/10
                # br.remove_from_backpack(dialog.data[4], int(dialog.data[3]))
                # dialog.iteration = 3
                dialog.data = (None, None, None, None)
            else:
                I.info.QUESTS = get_quest_dict(npc[giver]["quest"].split(",,,")[int(iteration)], giver) # QUESTS GET ASSIGNED HERE
                check_quest_completion()
                dialog.data = (None, None, None, None)
        elif "shop" in dialog.data[0]:
            br.handle_shop(dialog.data[1], player, screen, items)
        elif dialog.data[0] == "item":
            if "buy" in dialog.data[1]:
                # print("Buying ", dialog.data[3], "for ", dialog.data[2])
                player["Gold"] = float(player["Gold"]) - float(dialog.data[2])
                Ff.add_to_backpack(dialog.data[3], 1, items)  # Adds bought items through conversation
                Ff.display_text_player("Received 1 " + dialog.data[3], 5000)
                Ff.display_text_player("Removed " + str(dialog.data[2]) + " Gold", 5000)
                dialog.data = (None, None, None, None)
            elif dialog.data[1] == "get":
                dialog.data = (None, None, None, None)
            elif "False" in dialog.data[1]:
                """Get an item for free"""
                name = dialog.data[2].replace("NAME:", "")
                amount = dialog.data[3].replace("AMOUNT:", "")
                if name == "Gold":
                    player[name] += float(amount)
                else:
                    Ff.add_to_backpack(name, amount, items)
                dialog.data = (None, None, None, None)
        elif "Crime" in dialog.data[0]:
            if "Assault" in dialog.data[1]:
                I.info.CRIMINAL["Fine"] = 50
                I.info.CRIMINAL["Prison_time"] = 360
                I.info.CRIMINAL["Charge"] = dialog.data[1]
                if "Criminal|0" not in I.info.TITLES:
                    I.info.TITLES.append("Criminal|0")
            elif "Abuse" in dialog.data[1]:
                I.info.CRIMINAL["Fine"] = 5
                I.info.CRIMINAL["Prison_time"] = 60
                I.info.CRIMINAL["Charge"] = dialog.data[1]
                if "Criminal|0" not in I.info.TITLES:
                    I.info.TITLES.append("Criminal|0")
            elif "PayFine" in dialog.data[1]:
                player["Gold"] -= 10
                I.info.TITLES.remove("Criminal|0")
                print("Transport character near prison")
            elif "Prison" in dialog.data[1]:
                rooms.select_room("Prison1")
                I.info.CURRENT_ROOM = {"name": "Prison1", "Spells": True, "Backpack": True, "Running": True, "Mobs": rooms.mobs, "Type": "House"}
                I.info.ENTRY_POS = (1, 1)
                I.info.OFFSCREEN = (25, 250)
                br.update_character_stats('static/data/created_characters/' + I.info.SELECTED_CHARACTER + "/" + I.info.SELECTED_CHARACTER + ".txt", data["Player"], spells.selected_spell, npc)
                Play.Start(screen, clock, rooms)
                print("transport player to prison")


def get_quest_dict(quest_data, giver):
    if giver == 'Tutorial Man':
        giver = "Purple Wizard"
    dict = {"COMPLETION": 0, "GIVER": giver}
    quest_list = quest_data.split(",,")
    for data in quest_list:
        property = data.split(":")[0]
        dict[property] = data.split(":")[1]
    return dict

def list_to_dict(list):
    dict = {}
    if list == ['', ''] or list == ['']:
        return 0
    for lis in list:
        key, value = lis.split(":")
        dict[key] = value
    return dict