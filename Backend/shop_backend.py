from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S

def fill_shop(screen, type, items, mode, player):
    rect = screen.get_rect()
    path = S.PLAYING_PATH["Shop_Empty"]
    color = ("black", "brown4", "brown4")

    if mode == 1:
        path = path[:-4] + "_Sell.png"
        color = ("brown4", "black", "brown4")
    elif mode == 2:
        path = path[:-4] + "_Exit.png"
        color = ("brown4", "brown4", "black")

    gold = player["Gold"]
    gold = round(gold, 3)

    shop = Ff.add_image_to_screen(screen, path, [rect.center[0] * 0.5, rect.center[1] * 0.25, S.SCREEN_WIDTH / 2, S.SCREEN_HEIGHT * 0.75])
    if mode == 0:
        Ff.display_text(screen, "Buy", 16, (420, 452), "black")
    elif mode == 1:
        Ff.display_text(screen, "Sell", 16, (420, 452), "black")
    elif mode == 2:
        Ff.display_text(screen, "Exit - hit [C]", 30, (500, 280), "black")

    Ff.add_image_to_screen(screen, items.item_dict["Gold"]["path"], (550, 450, 34, 30))
    Ff.display_text(screen, "Gold: " + str(gold), 16, (580, 452), "black")
    Ff.display_text(screen, "Buy", 8, (400, 119), color[0])
    Ff.display_text(screen, "Sell", 8, (540, 119), color[1])
    Ff.display_text(screen, "Exit", 8, (670, 118), color[2])
    Ff.display_text(screen, "Back", 16, (780, 452), "black")

    if I.info.SHOP_COORDINATES_X == {}:
        I.info.SHOP_COORDINATES_X, I.info.SHOP_COORDINATES_Y = I.BB.bag_coordinates(screen, shop)

    item_w = list(I.info.SHOP_COORDINATES_X.values())[1] - list(I.info.SHOP_COORDINATES_X.values())[0]
    item_h = list(I.info.SHOP_COORDINATES_Y.values())[1] - list(I.info.SHOP_COORDINATES_Y.values())[0]

    row = 0
    collumn = 0
    if I.info.SHOP_CONTENT == {} and type == "Armory":
        for item in items.item_dict.keys():
            if "WEAPON" in items.item_dict[item]["Properties"] or "HOE" in items.item_dict[item]["Properties"]:
                I.info.SHOP_CONTENT[item] = row, collumn
                row += 2
                if row == 28:
                    collumn += 2
                    row = 0

    elif I.info.SHOP_CONTENT == {} and type == "apothecary":
        for item in items.item_dict.keys():
            if "BREWABLE" in items.item_dict[item]["Properties"] or "Potion" in item: #or "TOOL:Grinder" in items.item_dict[item]["Properties"]:
                I.info.SHOP_CONTENT[item] = row, collumn
                row += 2
                if row == 28:
                    collumn += 2
                    row = 0

    if mode == 0:
        for content in I.info.SHOP_CONTENT.keys():
            row, collumn = I.info.SHOP_CONTENT[content]
            Ff.add_image_to_screen(screen, items.item_dict[content]["path"], [list(I.info.SHOP_COORDINATES_X.values())[row], list(I.info.SHOP_COORDINATES_Y.values())[collumn], item_w, item_h])
    elif mode == 1:
        row = 0
        collumn = 0
        for content in I.info.BACKPACK_CONTENT.keys():
            amount, not_used_row, not_used_collumn = I.info.BACKPACK_CONTENT[content]
            if content == "Gold":
                continue
            if row >= 0:
                Ff.add_image_to_screen(screen, items.item_dict[content.split("|")[0]]["path"], [list(I.info.SHOP_COORDINATES_X.values())[row], list(I.info.SHOP_COORDINATES_Y.values())[collumn], item_w, item_h])
                # print(row, collumn)
                Ff.display_text(screen, str(int(amount)), 1, (list(I.info.SHOP_COORDINATES_X.values())[row], list(I.info.SHOP_COORDINATES_Y.values())[collumn]), "white")
                row += 2
                if row == 30:
                    collumn += 2
                    row = 0

def handle_shop(case, player, screen, items):
    if case == "Armory" or case == "apothecary":
        I.info.SHOP_CONTENT = {}
        block = (0, 0)
        color = "yellow"
        border = 1
        pressed = 0
        mode = 0
        running = True
        selected = 0
        display_text = []
        fill_shop(screen, case, items, mode, player)
        item_w = list(I.info.SHOP_COORDINATES_X.values())[1] - list(I.info.SHOP_COORDINATES_X.values())[0]
        item_h = list(I.info.SHOP_COORDINATES_Y.values())[1] - list(I.info.SHOP_COORDINATES_Y.values())[0]
        while running:
            for event in I.pg.event.get():
                if event.type == I.pg.KEYDOWN:
                    if event.key == I.pg.K_c:
                        if mode == 2:
                            running = False
                        pressed = I.pg.K_c
                    elif event.key == I.pg.K_UP:
                        if selected == 0:
                            block = (block[0], block[1] - 2)
                            if block[1] < 0:
                                block = (block[0], 16)
                    elif event.key == I.pg.K_ESCAPE:
                        pressed = I.pg.K_ESCAPE
                    elif event.key == I.pg.K_DOWN:
                        if selected == 0:
                            block = (block[0], block[1] + 2)
                            if block[1] > 16:
                                block = (block[0], 0)
                    elif event.key == I.pg.K_LEFT:
                        if selected == 0:
                            block = (block[0] - 2, block[1])
                            if block[0] < 0 and selected == 0:
                                block = (28, block[1])
                        else:
                            block = (block[0] - 15, block[1])
                            if block[0] < 0 and selected != 0:
                                block = (20, block[1])
                    elif event.key == I.pg.K_RIGHT:
                        if selected == 0:
                            block = (block[0] + 2, block[1])
                            if block[0] > 28:
                                block = (0, block[1])
                        else:
                            block = (block[0] + 10, block[1])
                            if block[0] > 28:
                                block = (0, block[1])
                    elif event.key == I.pg.K_q and selected == 0:
                        # so that only be able to switch rows when no item is selected
                        mode -= 1
                        if mode < 0:
                            mode = 0
                    elif event.key == I.pg.K_e and selected == 0:
                        # so that only be able to switch rows when no item is selected
                        mode += 1
                        if mode > 2:
                            mode = 2
                if event.type == I.pg.KEYUP:
                    if pressed == I.pg.K_ESCAPE:
                        running = False
                    if event.key == I.pg.K_c and pressed == I.pg.K_c:
                        if selected == 0:
                            if mode == 0:
                                for item, (row, collum) in I.info.SHOP_CONTENT.items():
                                    if block == (row, collum):
                                        selected = item
                                        border = 2
                            elif mode == 1:
                                item_list = []
                                for item, (amount, row, collum) in I.info.BACKPACK_CONTENT.items():
                                    if item == "Gold":
                                        continue
                                    item_list.append(item)
                                if len(item_list) - 1 >= int(block[0] / 2 + 15 * (block[1] / 2)):
                                    selected = item_list[int(block[0] / 2 + 15 * (block[1] / 2))]
                                    border = 2
                                    block = 0, block[1]
                                else:
                                    selected = 0
                        else:
                            if mode == 0:
                                if block[0] == 0:
                                    # If selected item in buying and pressed "buy"
                                    if items.item_dict[selected]["Cost"] > player["Gold"] * 10:
                                        display_text = ["Not enough Gold", 40, [420, 520]]
                                    else:
                                        display_text = ["Bought", 40, [420, 520]]
                                        Ff.add_to_backpack(selected, 1, items)  # Adds bought item through shop
                                        player["Gold"] -= items.item_dict[selected]["Cost"] / 10
                                        block = I.info.SHOP_CONTENT[selected]
                                        selected = 0
                                else:
                                    # If selected item in buying and pressed "Back"
                                    block = I.info.SHOP_CONTENT[selected]
                                    selected = 0
                            elif mode == 1:
                                # if selected item in selling
                                if block[0] == 0:
                                    # selling this item
                                    player["Gold"] += items.item_dict[selected.split("|")[0]]["Cost"] / 10 * 0.8
                                    location = list(I.info.BACKPACK_CONTENT.keys()).index(selected)
                                    block = (location % 15) * 2 - 2, (location // 15) * 2
                                    Ff.remove_from_backpack(selected, 1)
                                    selected = 0
                                else:
                                    # going back
                                    location = list(I.info.BACKPACK_CONTENT.keys()).index(selected)
                                    block = (location % 15) * 2 - 2, (location // 15) * 2
                                    selected = 0
                            if block[0] == 20:
                                selected = 0

                    if event.key == I.pg.K_x:
                        selected = 0
                        display_text = []
                        border = 1
                    pressed = 0
            if selected != 0:
                if block[0] < 10:
                    block = 0, block[1]
                    rect = I.pg.Rect(list(I.info.SHOP_COORDINATES_X.values())[block[0]],list(I.info.SHOP_COORDINATES_Y.values())[16] + item_h * 1.8, item_w * 6, item_h)
                elif block[0] < 28:
                    block = 20, block[1]
                    rect = I.pg.Rect(list(I.info.SHOP_COORDINATES_X.values())[block[0]] + 12,list(I.info.SHOP_COORDINATES_Y.values())[16] + item_h * 1.8, item_w * 6 - 4, item_h)
            else:
                rect = I.pg.Rect(list(I.info.SHOP_COORDINATES_X.values())[block[0]],list(I.info.SHOP_COORDINATES_Y.values())[block[1]], item_w, item_h)

            fill_shop(screen, case, items, mode, player)

            if mode == 0:
                for item, (row, collum) in I.info.SHOP_CONTENT.items():
                    if block == (row, collum) and selected == 0:
                        display_text = [items.item_dict[item]["describtion"], 10, [390, 500]]
                        break
            elif mode == 1:
                item_list = []
                for item, (amount, row, collum) in I.info.BACKPACK_CONTENT.items():
                    if item == "Gold":
                        continue
                    item_list.append(item)
                    if len(item_list) - 1 >= block[0] / 2 + 15 * (block[1] / 2) and selected == 0:
                        display_text = [items.item_dict[item_list[int((block[0] / 2) + 15 * (block[1] / 2))].split("|")[0]]["describtion"], 10, [390, 500]]
                        break
            elif mode == 2:
                display_text = []

            if display_text != []:
                if "\\n" in display_text[0]:
                    lines = display_text[0].split("\\n")
                    for i in range(len(lines)):
                        Ff.display_text(screen, lines[i], display_text[1], (display_text[2][0], display_text[2][1] + i * 20), "black")
                else:
                    Ff.display_text(screen, display_text[0], display_text[1], display_text[2], "black")

            if mode != 2:
                I.pg.draw.rect(screen, color, rect, border)
            I.pg.display.flip()