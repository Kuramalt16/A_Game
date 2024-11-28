from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S

def handle_display_map(screen, rooms, data, decorations):
    if rooms.size == ["1", "1", "1", "1"]:
        running = True
        dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)
        dim_surface.fill((0, 0, 0, 180))
        screen.blit(dim_surface, (0, 0))
        pressed = None
        map_block_w = 100
        map_block_h = 100
        zoom_w = 100
        zoom_h = 100
        center_pos = [S.SCREEN_WIDTH / 2 , S.SCREEN_HEIGHT / 2 - map_block_h / 2]
        center_map, add_x, add_y = rooms.name.split("_")
        maps = {}

        while running:
            for event in I.pg.event.get():
                if event.type == I.pg.KEYDOWN:
                    pressed = event.key
                if event.type == I.pg.KEYUP:
                    if pressed in [I.pg.K_m, I.pg.K_ESCAPE] and event.key in [I.pg.K_m, I.pg.K_ESCAPE]:
                        running = False
                    else:
                        pressed = None
                keys = I.pg.key.get_pressed()
                if keys[I.pg.K_UP]:
                    print("up")
                #     zoom_w += 10
                #     zoom_h += 10
                #     center_pos[0] -= 5
                #     center_pos[1] -= 5
                # elif keys[I.pg.K_DOWN]:
                #     zoom_w -= 10
                #     zoom_h -= 10
                #     center_pos[0] += 5
                #     center_pos[1] += 5
                elif keys[I.pg.K_LEFT]:
                    print("left")
                elif keys[I.pg.K_RIGHT]:
                    print("right")
                Ff.add_image_to_screen(screen, S.local_path + "/static/images/Playing/Map_Empty.png", (0, 0, S.SCREEN_WIDTH, S.SCREEN_HEIGHT))


                for map_name, values in I.A.MAPS.items():
                    x, y = center_pos
                    map_x, map_y = values["possision"][0] - int(add_x), values["possision"][1] - int(add_y)
                    values["surface"] = I.pg.transform.scale(values["surface"], (zoom_w, zoom_h))
                    screen.blit(values["surface"], (x + map_x * (map_block_w + 1), y + map_y * (map_block_h + 1)))
            I.pg.display.flip()
    else:
        Ff.display_text_player("unable to open a map inside", 1000)

def add_map_to_maps(rooms, decorations):
    if I.A.MAPS.get(rooms.name) == None and rooms.size == ["1", "1", "1", "1"]:
        zoom_w = 100
        zoom_h = 100
        center_map, add_x, add_y = rooms.name.split("_")
        values = rooms.name.split("_")
        image = I.pg.image.load(S.local_path + "/static/images/Background/" + rooms.background + "_" + values[1] + "_" + values[2] + ".png").convert_alpha()  # uploads the background image with transparent convert
        sub_image = image.copy()
        for decor in decorations.decor_dict.keys():
            for id in decorations.decor_dict[decor].keys():
                if isinstance(id, int):
                    image = decorations.decor_dict[decor][id]["image"]
                    rect = decorations.decor_dict[decor][id]["rect"]
                    sub_image.blit(image, (rect.x, rect.y))

        scaled_image = I.pg.transform.scale(sub_image, (zoom_w, zoom_h))
        I.A.MAPS[rooms.name] = {"lock": False,
                                "surface": scaled_image,
                                "possision": (int(add_x), int(add_y))}

# def handle_display_map(screen, rooms):
#     running = True
#     dim_surface = I.pg.Surface((S.SCREEN_WIDTH, S.SCREEN_HEIGHT), I.pg.SRCALPHA)
#     dim_surface.fill((0, 0, 0, 180))
#     screen.blit(dim_surface, (0, 0))
#     pressed = None
#     map_block_w = 20
#     map_block_h = 10
#     center_pos = (S.SCREEN_WIDTH / 2 - map_block_w*1.5, S.SCREEN_HEIGHT / 2 - map_block_h * 2.5)
#     center_map, add_x, add_y = rooms.name.split("_")
#
#     while running:
#         for event in I.pg.event.get():
#             if event.type == I.pg.KEYDOWN:
#                 pressed = event.key
#             if event.type == I.pg.KEYUP:
#                 if pressed in [I.pg.K_m, I.pg.K_ESCAPE] and event.key in [I.pg.K_m, I.pg.K_ESCAPE]:
#                     running = False
#                 else:
#                     pressed = None
#             keys = I.pg.key.get_pressed()
#             if keys[I.pg.K_UP]:
#                 print("up")
#             elif keys[I.pg.K_DOWN]:
#                 print("down")
#             elif keys[I.pg.K_LEFT]:
#                 print("left")
#             elif keys[I.pg.K_RIGHT]:
#                 print("right")
#             Ff.add_image_to_screen(screen, S.local_path + "/static/images/Playing/Map_Empty.png", (0, 0, S.SCREEN_WIDTH, S.SCREEN_HEIGHT))
#
#             for map_name in I.A.MAPS.keys():
#                 village, value_x, value_y = map_name.split("_")
#                 addx = int(add_x) - int(value_x)
#                 addy = int(add_y) - int(value_y)
#                 # print(map_name, map_values["background"])
#                 # I.pg.draw.rect(screen, "red", (100, 75, 1080, 575))
#                 # print(addx, addy)
#                 print(len(list(I.A.MAPS[map_name].keys())))
#                 for pos, surface in I.A.MAPS[map_name].items():
#                     if pos[0] != None and pos[1] != None:
#                         map_image = I.pg.transform.scale(surface, (map_block_w, map_block_h))
#                         # print(center_pos[1] + map_block_h * pos[1] - (addy * map_block_h * 5), center_pos[0] + map_block_w * pos[0] - (addx * map_block_w * 3))
#                         # if center_pos[1] + map_block_h * pos[1] - (addy * map_block_h * 5) in range(75, 575) and center_pos[0] + map_block_w * pos[0] - (addx * map_block_w * 3) in range(100, 1080):
#                         #     # print("showing", pos)
#                         #     screen.blit(map_image, (center_pos[0] + map_block_w * pos[0] - (addx * map_block_w * 3), center_pos[1] + map_block_h * pos[1] - (addy * map_block_h * 5)))
#                         screen.blit(map_image, (center_pos[0] + map_block_w * pos[0] - (addx * map_block_w * 3), center_pos[1] + map_block_h * pos[1] - (addy * map_block_h * 5)))
#
#         I.pg.display.flip()


# def add_map_to_maps(screen, rooms, data):
#     # print(data["Zoom_rect"])
#     cell_width = 600
#     cell_height = 300
#     grid_x, grid_y = find_grid_cell(data["Zoom_rect"].x + data["Zoom_rect"].w / 2, data["Zoom_rect"].y + data["Zoom_rect"].h / 2, screen, 50, 50)
#     # print(grid_x, grid_y)
#
#     if I.A.MAPS.get(rooms.name) == None:
#         I.A.MAPS[rooms.name] = {}
#
#     # if grid_x != None and grid_y != None:
#
#     if I.A.MAPS[rooms.name].get((grid_x, grid_y)) == None:
#         if grid_x != None and grid_y != None:
#             S.DUMMY_VALUE1.append((data["Zoom_rect"].x + data["Zoom_rect"].w / 2, data["Zoom_rect"].y + data["Zoom_rect"].h / 2))
#             capture_rect = I.pg.Rect(
#                 data["Zoom_rect"].w,
#                 data["Zoom_rect"].h,
#                 cell_width,
#                 cell_height
#             )
#             I.A.MAPS[rooms.name][(grid_x, grid_y)] = capture_screen_area(screen, capture_rect)
#             # I.T.Make_rect_visible(screen, capture_rect, "red")

# def add_map_to_maps(screen, rooms, data):
#     # print(data["Zoom_rect"])
#
#     grid_pos = find_grid_cell(data["Zoom_rect"].x, data["Zoom_rect"].y)
#     print(grid_pos)
#     if I.A.MAPS.get(rooms.name) == None:
#         I.A.MAPS[rooms.name] = {}
#
#     if I.A.MAPS[rooms.name].get(grid_pos) == None:
#         if grid_pos[0] != None and grid_pos[1] != None:
#             I.A.MAPS[rooms.name][grid_pos] = screen.copy()

# def find_grid_cell(x, y, screen, cell_w, cell_h, grid_width=1000, grid_height=1000):
#     # I.T.Make_rect_visible(screen, (x, y, 10, 10), "red")
#
#     # Calculate cell size
#     # grid_x = {
#     #     (0, 10): 0,
#     #     (320, 330): 1,
#     #     (640, 650): 2,
#     #     (960, 970): 3}
#     # grid_y = {
#     #     (0, 10): 0,
#     #     (180, 190): 1,
#     #     (360, 370): 2,
#     #     (540, 550): 3,
#     #     (720, 730): 4,
#     # }
#
#     # for (lowerlimit, upperlimit), cell_x in grid_x.items():
#     #     # print(x, "in range", 200 * i, 200 * (i + 1))
#     #     if x in range(lowerlimit, upperlimit):
#     #         # print(x, cell_x)
#     #         break
#     #     else:
#     #         cell_x = None
#
#     # for (lowerlimit, upperlimit), cell_y in grid_y.items():
#     #     # print(x, "in range", 200 * i, 200 * (i + 1))
#     #     if y in range(lowerlimit, upperlimit):
#     #         # print(y, cell_y)
#     #         break
#     #     else:
#     #         cell_y = None
#     # return cell_x, cell_y
#
#
#     cell_width = cell_w
#     cell_height = cell_h
#     # Find grid position
#     grid_x = x / cell_width
#     grid_y = y / cell_height
#     # print(x / cell_w, y / cell_h)
#     # print(grid_x, grid_y)
#     return (abs(grid_x), abs(grid_y))
#     # if abs(grid_x) % 1 == 0.0 and abs(grid_y) % 1 == 0.0:
#     #     if 0 <= grid_x and 0 <= grid_y:
#     #         return (grid_x, grid_y)
#     # else:
#     #     return None, None  # Coordinates are out of bounds

# def capture_screen_area(screen, rect):
#     """
#     Captures a smaller area of the screen defined by the given rect.
#     :param screen: The main Pygame screen surface.
#     :param rect: A pygame.Rect defining the area to capture.
#     :return: A surface containing the captured area.
#     """
#     return screen.subsurface(rect).copy()
