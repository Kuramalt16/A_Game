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
            if quest["ACTION"] == "QUEST_BACKPACK" and quest["COMPLETION"] != 1:
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
            if quest["ACTION"] == "QUEST_BACKPACK" and quest["COMPLETION"] != 1:
                quest["COMPLETION"] += 0.5

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