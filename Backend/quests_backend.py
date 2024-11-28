from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S

def handle_q_click(screen, song, items):
    dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)
    dim_surface.fill((0, 0, 0, 180))
    screen.blit(dim_surface, (0, 0))

    curr_song = song["Playing"]
    song[curr_song].channel0.pause()
    for quest in I.info.QUESTS:
        if quest["TYPE"] == "Tutorial":
            if quest["ACTION"] == "QUEST_BACKPACK" and quest["COMPLETION"] == 0:
                quest["COMPLETION"] += 0.5

    quest_render(screen, items)
    song[curr_song].channel0.unpause()

def quest_render(screen, items):
    running = True
    item_w = list(I.info.BACKPACK_COORDINATES_X.values())[1] - list(I.info.BACKPACK_COORDINATES_X.values())[0]
    item_h = list(I.info.BACKPACK_COORDINATES_Y.values())[1] - list(I.info.BACKPACK_COORDINATES_Y.values())[0]
    key_auth = 0
    text = ("Quests", 13, 600)
    displaying = "Quests"
    move = 0
    start_text = S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20
    while running:
        for event in I.pg.event.get():
            if event.type == I.pg.KEYDOWN:
                if event.key in [I.pg.K_ESCAPE, I.pg.K_q]:
                    key_auth = event.key
            if event.type == I.pg.KEYUP:
                if event.key == key_auth and event.key in [I.pg.K_ESCAPE, I.pg.K_q]:
                    running = False
                elif event.key == I.pg.K_LEFT:
                    text = ("Quests", 13, 600)
                    displaying = "Quests"
                    move = 0
                elif event.key == I.pg.K_RIGHT:
                    text = ("Completed quests", 13, 540)
                    displaying = "Completed quests"
                    move = 0
                elif event.key == I.pg.K_UP:
                    move -= 1
                    if displaying == "Quests" and move > len(I.info.QUESTS):
                        move = 0
                    elif move < 0:
                        move = 0

                elif event.key == I.pg.K_DOWN:
                    move += 1
                    if move > len(I.info.COMPLETED_QUESTS) - 2:
                        move = 0
        Ff.add_image_to_screen(screen, S.PLAYING_PATH["Quest_Empty"], [S.SCREEN_WIDTH / 4, S.SCREEN_HEIGHT / 5, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT / 1.5])
        Ff.display_text(screen, text[0], text[1], (text[2],160))
        quest_number = 0

        if displaying == "Quests":
            for i in range(0 + move, 3 + move):
                if len(I.info.QUESTS) <= i or len(I.info.QUESTS) == 0:
                    continue
                quest = I.info.QUESTS[i]
                quest_type = quest["TYPE"]

                if quest_type == "GET":
                    path = "static/images/Items/"
                    path += quest["ITEM"] + ".png"
                elif quest_type == "Tutorial":
                    path = S.PLAYING_PATH["Tutorial_icon"]
                elif quest_type == "MEET":
                    path = S.PLAYING_PATH["Meet_icon"]

                quest_describtion = quest["DESC"]
                if "\\n" in quest_describtion:
                    lines = quest_describtion.split("\\n")
                    collum =  start_text * 1.1 + quest_number
                    for line in lines:
                        Ff.display_text(screen, line, 5, (S.SCREEN_WIDTH / 3 * 0.9,collum), "Black")
                        collum += 20
                else:
                    Ff.display_text(screen, quest_describtion, 5, (S.SCREEN_WIDTH / 3 * 0.9, start_text * 1.1 + quest_number), "Black")
                if quest["COMPLETION"] < 1:
                    Ff.display_text(screen, "In Progress", 4, (S.SCREEN_WIDTH / 3 * 0.9, start_text * 1.5 + quest_number), "Black")
                else:
                    quest["COMPLETION"] = 1
                    Ff.display_text(screen, "COMPLETED Recieve reward from - " + str(quest["GIVER"]), 4, (S.SCREEN_WIDTH / 3 * 0.9, start_text * 1.5 + quest_number), "Black")

                Ff.add_image_to_screen(screen, path, (885, 180 + quest_number, 30, 30))
                remainder = I.DialB.check_quest_completion(i)
                I.pg.draw.rect(screen, "black", (S.SCREEN_WIDTH / 3 * 0.9, S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 4.1 + quest_number, item_w * 18, item_h * 0.3))
                I.pg.draw.rect(screen, "green", (S.SCREEN_WIDTH / 3 * 0.9, S.SCREEN_HEIGHT / 5 + S.SCREEN_HEIGHT / 20 * 4.1 + quest_number, item_w * 18 * remainder, item_h * 0.3))
                quest_number += 140
        else:
            for i in range(0 + move, 3 + move):
                if len(I.info.COMPLETED_QUESTS) <= i or len(I.info.COMPLETED_QUESTS) == 0:
                    continue
                completed_quest = I.info.COMPLETED_QUESTS[i]
                quest_type = completed_quest["TYPE"]
                quest_describtion = completed_quest["DESC"]

                if quest_type == "GET":
                    path = "static/images/Items/"
                    path += completed_quest["ITEM"] + ".png"
                elif quest_type == "Tutorial":
                    path = S.PLAYING_PATH["Tutorial_icon"]
                elif quest_type == "MEET":
                    path = S.PLAYING_PATH["Meet_icon"]

                if "\\n" in quest_describtion:
                    lines = quest_describtion.split("\\n")
                    collum =  start_text * 1.1 + quest_number
                    for line in lines:
                        Ff.display_text(screen, line, 5, (S.SCREEN_WIDTH / 3 * 0.9, collum), "Black")
                        collum += 20
                else:
                    Ff.display_text(screen, quest_describtion, 5, (S.SCREEN_WIDTH / 3 * 0.9, start_text * 1.1 + quest_number), "Black")

                Ff.add_image_to_screen(screen, path, (885, 180 + quest_number, 30, 30))

                Ff.display_text(screen, "COMPLETED", 4,(S.SCREEN_WIDTH / 3 * 0.9, start_text * 1.5 + quest_number), "Black")
                quest_number += 140

        I.pg.display.flip()

def tutorial_quest_walk(dx, dy):
    for quest in I.info.QUESTS:
        if quest["TYPE"] == "Tutorial":
            if quest["ACTION"] == "WALK" and quest["COMPLETION"] != 1:
                if dx == -1 and quest["COMPLETION"] == 0:
                    quest["COMPLETION"] = 0.25
                if dx == 1 and quest["COMPLETION"] == 0.25:
                    quest["COMPLETION"] = 0.5
                if dy == -1 and quest["COMPLETION"] == 0.5:
                    quest["COMPLETION"] = 0.75
                if dy == 1 and quest["COMPLETION"] == 0.75:
                    quest["COMPLETION"] = 1
            elif quest["ACTION"] == "RUN" and quest["COMPLETION"] != 1:
                if I.info.FAST == 2:
                    if dx == -1 and quest["COMPLETION"] == 0:
                        quest["COMPLETION"] = 0.25
                    if dx == 1 and quest["COMPLETION"] == 0.25:
                        quest["COMPLETION"] = 0.5
                    if dy == -1 and quest["COMPLETION"] == 0.5:
                        quest["COMPLETION"] = 0.75
                    if dy == 1 and quest["COMPLETION"] == 0.75:
                        quest["COMPLETION"] = 1

def tutorial_berry_get(item):
    for quest in I.info.QUESTS:
        if quest["TYPE"] == "Tutorial":
            if quest["ACTION"] == "EAT" and quest["COMPLETION"] == 0:
                if item == "Light Berries":
                    quest["COMPLETION"] = 0.3333

def tutorial_hit():
    for quest in I.info.QUESTS:
        if quest["TYPE"] == "Tutorial" and quest["ACTION"] == "PUNCH" and quest["COMPLETION"] != 1:
            quest["COMPLETION"] = 1

def tutorial_backpack():
    for quest in I.info.QUESTS:
        if quest["TYPE"] == "Tutorial":
            if quest["ACTION"] == "QUEST_BACKPACK" and quest["COMPLETION"] == 0.5:
                quest["COMPLETION"] = 1

def set_tutorial_flag():
    I.info.tutorial_flag = 1
    for completed_quest in I.info.COMPLETED_QUESTS:
        if completed_quest["TYPE"] == "Tutorial":
            I.info.tutorial_flag = 0


def tutorial_eat_berry(use):
    if use == "Light Berries":
        for quest in I.info.QUESTS:
            if quest["TYPE"] == "Tutorial" and quest["ACTION"] == "EAT" and quest["COMPLETION"] == 0.6666:
                quest["COMPLETION"] = 1

def tutorial_move_berry(pickup):
    for quest in I.info.QUESTS:
        if quest["TYPE"] == "Tutorial" and quest["ACTION"] == "EAT" and quest["COMPLETION"] == 0.3333:
            if pickup[0] == "Light Berries":
                quest["COMPLETION"] += 0.3333

def get_quest_dict(quest_data, giver):
    if giver == 'Tutorial Man':
        giver = "Purple Wizard"
    dict = {"COMPLETION": 0, "GIVER": giver}
    dict2 = {"COMPLETION": 0, "GIVER": giver}
    single_quest = True
    quest_list = quest_data.split(",,")
    for data in quest_list:
        property = data.split(":")[0]
        if "|" in data.split(":")[1]:
            dict[property] = data.split(":")[1].split("|")[0]
            dict2[property] = data.split(":")[1].split("|")[1]
            single_quest = False
        else:
            dict[property] = data.split(":")[1]
    if single_quest and not any(quest["DESC"] == dict["DESC"] for quest in I.info.QUESTS):
        I.info.QUESTS.append(dict)
    elif not any(quest["DESC"] == dict["DESC"] for quest in I.info.QUESTS):
        I.info.QUESTS.append(dict)
        I.info.QUESTS.append(dict2)

def handle_completed_quest_dialog(player, dialog):
    reward = 0
    items_to_be_removed = []
    sum = 0
    for quest in I.info.QUESTS:
        if quest["GIVER"] == dialog.name and quest["COMPLETION"] >= 1 or quest["GIVER"] == "Purple Wizard" and quest["COMPLETION"] >= 1:
            if "Sp" in quest["REWARD"]:
                currency = "Sp"
                reward_money_id = quest["REWARD"].find(" ")
                sum += int(quest["REWARD"][:reward_money_id])
                reward = str(sum) + quest["REWARD"][reward_money_id:]
            elif "Gp" in quest["REWARD"]:
                currency = "Gp"
                reward += int(quest["REWARD"].replace(" Gp", "")) * 10
            I.info.COMPLETED_QUESTS.append(quest)
    for completed_quest in I.info.COMPLETED_QUESTS:
        if completed_quest in I.info.QUESTS:
            if completed_quest["TYPE"] == "GET":
                items_to_be_removed.append((completed_quest["ITEM"], completed_quest["AMOUNT"]))
            I.info.QUESTS.remove(completed_quest)

    for item, amount in items_to_be_removed:
        Ff.remove_from_backpack(item, int(amount))

    reward = str(reward) + " Sp"
    if "Gp" in reward:
        reward = reward.replace("Gp", "")
        currency = " Gp"
        player["Gold"] += float(reward)
    if "Sp" in reward:
        reward = reward.replace("Sp", "")
        currency = " Sp"
        if "Friendlyness" in reward:
            reward = reward.replace("{Friendlyness}", "")
            reward = reward[:-1]
            sign = reward[-1]
            reward = reward[:-1]
            if sign == "*":
                reward = float(reward) + 5 * dialog.friendlyness
        player["Gold"] += round(float(reward) / 10, 2)
        player["Gold"] = round(player["Gold"], 2)
    Ff.display_text_player("Recieved " + str(reward) + currency + " for completing a quest", 4000)
    # I.info.COMPLETED_QUESTS["REWARD"] = "CLAIMED"
    # if dialog.data[2] == "Silver":
    #     player["Gold"] += float(dialog.data[1])/10
    # br.remove_from_backpack(dialog.data[4], int(dialog.data[3]))
    # dialog.iteration = 3
    dialog.data = (None, None, None, None)

def handle_meet_quests(name, player):
    for quest in I.info.QUESTS:
        if quest["TYPE"] == "MEET":
            if name == quest["WHO"]:
                quest["COMPLETION"] = 1
                I.info.COMPLETED_QUESTS.append(quest)
                remove_completed_quests()
                player["Gold"] += 0.1
                Ff.display_text_player("Recieved 1 Sp for completing a quest", 4000)

def remove_completed_quests():
    for completed_quest in I.info.COMPLETED_QUESTS:
        if completed_quest in I.info.QUESTS:
            I.info.QUESTS.remove(completed_quest)

def handle_quest_mark_render(sub_image, npc, decorations, gifs, rooms, data):
    if I.A.QUEST_SHOW_MARKS == {}:
        not_in_Completed_quests = {}
        not_in_started_quests = {}
        for npc_name in npc.keys():
            """Checking if from all the quests if they exist in the list of completed quests"""
            if npc[npc_name]["quest"] != 'False' and npc_name in rooms.decor:
                quest = npc[npc_name]["quest"]
                # print(quest)
                quests = quest.split(",,,")
                for q in quests:
                    quest_describtion_str_id = q.find("DESC:")
                    q = q[quest_describtion_str_id:].replace("DESC:", "")
                    if "|" in q:
                        q1 = q.split("|")[0]
                        q2 = q.split("|")[1]
                        if not any(q1 == completed_quest["DESC"] for completed_quest in I.info.COMPLETED_QUESTS):
                            if not_in_Completed_quests.get(npc_name) == None:
                                not_in_Completed_quests[npc_name] = q1 + "|" + q2
                            else:
                                not_in_Completed_quests[npc_name] += ",," + q1 + "|" + q2
                    else:
                        if not any(q == completed_quest["DESC"] for completed_quest in I.info.COMPLETED_QUESTS):
                            if not_in_Completed_quests.get(npc_name) == None:
                                not_in_Completed_quests[npc_name] = q
                            else:
                                not_in_Completed_quests[npc_name] += ",," + q

        for giver in not_in_Completed_quests.keys():
            """checking if the quests that dont exist in the completed quests exist in the current quests"""
            quest_str = not_in_Completed_quests[giver]
            quests = quest_str.split(",,")
            for quest_desc in quests:
                if "|" in quest_desc:
                    q1, q2 = quest_desc.split("|")
                    if not any(q1 == quest["DESC"] for quest in I.info.QUESTS):
                        if not_in_started_quests.get(giver) == None:
                            not_in_started_quests[giver] = q1 + "|" + q2
                        else:
                            not_in_started_quests[giver] += ",," + q1 + "|" + q2
                else:
                    if not any(quest_desc.replace("\n", " ") == quest["DESC"].replace("\\n", " ") for quest in I.info.QUESTS):
                        if not_in_started_quests.get(giver) == None:
                            not_in_started_quests[giver] = quest_desc
                        else:
                            not_in_started_quests[giver] += ",," + quest_desc

        """check if the quest is available if you talk to the quest giver"""
        for giver in not_in_started_quests.keys():
            current_iteration = npc[giver]["dialog"].iteration
            for response, text in npc[giver]["dialog"].text.items():
                if response[-1] == str(current_iteration):
                    text_data = text.split("__")
                    if len(text_data) == 3:
                        t, r1, r2 = text_data
                        response_data = r2.split("|")
                        if response_data[0] == "quest":

                            if I.A.QUEST_SHOW_MARKS.get(rooms.name) == None:
                                I.A.QUEST_SHOW_MARKS[rooms.name] = {}
                            rect = decorations.decor_dict[giver][0]["rect"]
                            mark_img = I.pg.image.load(S.local_path + "/static/images/Playing/Quest Available.png")
                            if rooms.size == ["1", "1", "1", "1"]:
                                rect = (rect.x + rect.w / 6, rect.y - rect.h / 4, 20, 20)
                            else:
                                rect = (rect.x + 10, rect.y - rect.h / 2, 40, 40)
                            mark_img = I.pg.transform.scale(mark_img, (rect[2], rect[3]))
                            I.A.QUEST_SHOW_MARKS[rooms.name][giver] = ["!", mark_img, rect]
                            break
                    else:
                        """only two responses definately not got a quest"""

        if I.A.QUEST_SHOW_MARKS == {}:
            I.A.QUEST_SHOW_MARKS = None
    elif I.A.QUEST_SHOW_MARKS not in [{}, None]:
        for room_name in I.A.QUEST_SHOW_MARKS:
            for giver in I.A.QUEST_SHOW_MARKS[room_name]:
                mark, image, rect = I.A.QUEST_SHOW_MARKS[room_name][giver]
                sub_image.blit(image, (rect[0] - data["Zoom_rect"].x, rect[1]  - data["Zoom_rect"].y))
                # I.T.Make_rect_visible(sub_image, (rect[0]  - data["Zoom_rect"].x, rect[1] - data["Zoom_rect"].y, rect[2], rect[3]), "red")

def set_quest_mark_complete(rooms):
    if I.info.QUESTS != []:
        for quest in I.info.QUESTS:
            if quest["COMPLETION"] >= 1:
                giver = quest["GIVER"]
                if giver == "Purple Wizard":
                    giver = "Tutorial Man"
                if I.A.QUEST_SHOW_MARKS[rooms.name][giver][0] == "!":
                    image = I.pg.image.load(S.local_path + "/static/images/Playing/Quest Completed.png")
                    mark, old_image, rect = I.A.QUEST_SHOW_MARKS[rooms.name][giver]
                    image = I.pg.transform.scale(image, (rect[2], rect[3]))
                    I.A.QUEST_SHOW_MARKS[rooms.name][giver] = ["?", image, rect]






