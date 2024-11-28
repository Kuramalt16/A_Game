from Values import Settings as S
from utils import Imports as I

def rotate_point(x, y, angle, origin=(0, 0)):
    """Rotate (x, y) around origin by the specified angle in degrees."""
    ox, oy = origin
    cos_theta = I.math.cos(I.math.radians(angle))
    sin_theta = I.math.sin(I.math.radians(angle))

    x -= ox
    y -= oy

    x_new = x * cos_theta - y * sin_theta
    y_new = x * sin_theta + y * cos_theta

    x_new += ox
    y_new += oy

    return x_new, y_new


def round_to_nearest_10(value):
    return round(value / 10) * 10


def rotate_and_round_point(x, y, angle, origin=(0, 0)):
    x_new, y_new = rotate_point(x, y, angle, origin)
    return round_to_nearest_10(x_new), round_to_nearest_10(y_new)


def rotate_ranges_degrees(ranges_dict, angle, origin=(0, 0)):
    rotated_dict = {}
    points_to_color = {}

    for (x1, x2, y1, y2), color in ranges_dict.items():
        for x in range(x1, x2, 10):
            for y in range(y1, y2, 10):
                x_new, y_new = rotate_and_round_point(x, y, angle, origin)
                if (x_new, y_new) not in points_to_color:
                    points_to_color[(x_new, y_new)] = color
                else:
                    # If the point is already in the dictionary, ensure it keeps the same color
                    points_to_color[(x_new, y_new)] = color

    # Reconstruct ranges from rotated points
    for (x, y), color in points_to_color.items():
        x_range = (x, x + 10)
        y_range = (y, y + 10)
        rotated_dict[(x_range[0], x_range[1], y_range[0], y_range[1])] = color

    return rotated_dict
class CharacterData:
    def __init__(self):
        self.arm_push = 0
        self.leg_push = 0
        self.foot_push = 0

        self.arm_raise = (0,0)
        self.leg_raise = (0,0)
        self.foot_raise = (0,0)

        self.orientation = "Front"

        self.gender = None
        self.race = None

        self.skin_color = S.DEFAULT["Skin"]
        self.skin_color2 = S.DEFAULT["Skin2"]
        self.eye_color = S.DEFAULT["Eyes"]


        self.front_skin_color = self.skin_color
        self.back_skin_color = self.skin_color2

        self.walking = None

        self.push_up = -30

        self.head_variable = []
        self.leg_variable = []
        self.leg_right_variable = []

        self.shirt_variable = []
        self.pants_variable = []
        self.shoes_variable = []
        self.sleeve_variable = []
        self.hair_variable = [(0, 0, 0, 0),
                              (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                              (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                              (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                              (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                              (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                              (0, 0, 0, 0)
                              ]
        self.make_longer_left = 0
        self.make_longer_right = 0

        self.shirt_color = (254, 0, 0, 255)
        self.pants_color = (254, 0, 0, 255)
        self.shoes_color = (254, 0, 0, 255)
        self.hair_color = "red"

        self._init_default_data()

    def classic_coloring_tool(self, part, color, iteration):
        color_list = list(I.A.color_mappings.get(part, {}).values())
        if iteration >= len(color_list):
            iteration = 0
        if iteration < 0:
            iteration = len(color_list) - 1
        if color == "":
            color = color_list[iteration]
        elif part == "Skin":
            self.skin_color = color
        elif part == "Skin2":
            self.skin_color2 = color
        elif part == "Eyes":
            self.eye_color = color
        elif part == "Color_Shir":
            self.shirt_color = color
        elif part == "Color_Pant":
            self.pants_color = color
        elif part == "Color_Shoe":
            self.shoes_color = color
        elif part == "Color_Hair":
            self.hair_color = color

        self._init_default_data()
        return iteration

    def _init_default_data(self):

        self.EYES = {
            (590, 600, 200 + self.push_up, 210 + self.push_up): (254, 255, 255, 255),  # Eye white
            (600, 610, 200 + self.push_up, 210 + self.push_up): self.eye_color,
            (640, 650, 200 + self.push_up, 210 + self.push_up): self.eye_color,
            (650, 660, 200 + self.push_up, 210 + self.push_up): (254, 255, 255, 255),  # Eye white

            (590, 600, 210 + self.push_up, 220 + self.push_up): (254, 255, 255, 255),  # Eye white
            (600, 610, 210 + self.push_up, 220 + self.push_up): (0, 0, 0, 255),
            (640, 650, 210 + self.push_up, 220 + self.push_up): (0, 0, 0, 255),
            (650, 660, 210 + self.push_up, 220 + self.push_up): (254, 255, 255, 255),  # Eye white
        }
        self.SMILE_HAPPY = {
            (600, 610, 230 + self.push_up, 240 + self.push_up): (0, 0, 0, 255),
            (640, 650, 230 + self.push_up, 240 + self.push_up): (0, 0, 0, 255),

            (610, 640, 240 + self.push_up, 250 + self.push_up): (0, 0, 0, 255),
        }

        self.LEFT_SMILE = {
            (600, 610, 230 + self.push_up, 240 + self.push_up): (0, 0, 0, 255),
            (580, 600, 240 + self.push_up, 250 + self.push_up): (0, 0, 0, 255),
        }
        self.LEFT_EYE = {
            (590, 600, 200 + self.push_up, 210 + self.push_up): self.eye_color,
            (600, 610, 200 + self.push_up, 210 + self.push_up): (254, 255, 255, 255),  # Eye white
            # (640, 650, 200, 210 + self.push_up): self.eye_color,
            # (650, 660, 200, 210 + self.push_up): (254, 255, 255, 255),  # Eye white

            (590, 600, 210 + self.push_up, 220 + self.push_up): (0, 0, 0, 255),  # Eye white
            (600, 610, 210 + self.push_up, 220 + self.push_up): (254, 255, 255, 255),
            # (640, 650, 210, 220 + self.push_up): (0, 0, 0, 255),
            # (650, 660, 210, 220 + self.push_up): (254, 255, 255, 255),  # Eye white
        }

        self.RIGHT_SMILE = {
            (640, 650, 230 + self.push_up, 240 + self.push_up): (0, 0, 0, 255),
            (650, 670, 240 + self.push_up, 250 + self.push_up): (0, 0, 0, 255),
        }
        self.RIGHT_EYE = {
            # (590, 600, 200, 210 + self.push_up): eye_color,
            # (600, 610, 200, 210 + self.push_up): (254, 255, 255, 255),  # Eye white
            (640, 650, 200 + self.push_up, 210 + self.push_up): (254, 255, 255, 255),
            (650, 660, 200 + self.push_up, 210 + self.push_up): self.eye_color,  # Eye white

            # (590, 600, 210, 220 + self.push_up): (0, 0, 0, 255),  # Eye white
            # (600, 610, 210, 220 + self.push_up): (254, 255, 255, 255),
            (640, 650, 210 + self.push_up, 220 + self.push_up): (254, 255, 255, 255),
            (650, 660, 210 + self.push_up, 220 + self.push_up): (0, 0, 0, 255),  # Eye white
        }

    def clothing_select(self, part, value):
        if part == "Shir":
            if value == 0:
                self.shirt_variable = [self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color,
                                       self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color,
                                       self.chest_variable[1], self.skin_color, self.chest_variable[2], self.skin_color, self.chest_variable[1],
                                       self.chest_variable[3], self.chest_variable[1], self.skin_color, self.skin_color, self.chest_variable[1],
                                       self.chest_variable[4], self.chest_variable[5], self.skin_color, self.skin_color, self.skin_color,
                                       self.chest_variable[4], self.chest_variable[6], self.chest_variable[5], self.skin_color, self.skin_color,
                                       self.chest_variable[5], self.chest_variable[6], self.skin_color, self.skin_color, self.skin_color,
                                       self.skin_color, self.chest_variable[7]]
            elif value == 1:
                self.shirt_variable = [self.shirt_color, self.shirt_color, self.shirt_color, (0, 0, 0, 254), self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.shirt_color, (0, 0, 0, 254), (0, 0, 0, 254), (0, 0, 0, 254),
                                       (0, 0, 0, 254), (0, 0, 0, 254)]
            elif value == 2:
                self.shirt_variable = [(0, 0, 0, 254), self.shirt_color, (0, 0, 0, 254), self.skin_color, (0, 0, 0, 254),
                                       (0, 0, 0, 254), self.shirt_color, self.shirt_color, (0, 0, 0, 254), self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.shirt_color, (0, 0, 0, 254), (0, 0, 0, 254), (0, 0, 0, 254),
                                       (0, 0, 0, 254), (0, 0, 0, 254)]
            elif value == 3:
                self.shirt_variable = [self.shirt_color, self.shirt_color, self.shirt_color, (0, 0, 0, 254), self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, (0, 0, 0, 254), self.shirt_color, (0, 0, 0, 254), (0, 0, 0, 254),
                                       (0, 0, 0, 254), self.chest_variable[5], (0, 0, 0, 254), self.skin_color, (0, 0, 0, 254),
                                       (0, 0, 0, 254), self.chest_variable[6], self.chest_variable[5], self.skin_color, self.skin_color,
                                       self.chest_variable[5], self.chest_variable[6], self.chest_variable[7], self.skin_color, self.skin_color,
                                       self.skin_color, self.chest_variable[7]]
            elif value == 4:
                self.shirt_variable = [self.shirt_color, (0, 0, 0, 254), self.shirt_color, (0, 0, 0, 254), self.shirt_color,
                                       (0, 0, 0, 254), self.shirt_color, self.shirt_color, self.shirt_color, (0, 0, 0, 254),
                                       self.chest_variable[1], self.shirt_color, self.chest_variable[2], (0, 0, 0, 254), self.chest_variable[1],
                                       self.chest_variable[3], self.chest_variable[1], self.skin_color, (0, 0, 0, 254), self.chest_variable[1],
                                       self.chest_variable[4], self.chest_variable[5], self.skin_color, self.skin_color, (0, 0, 0, 254),
                                       self.chest_variable[4], self.chest_variable[6], self.chest_variable[5], self.skin_color, self.skin_color,
                                       self.chest_variable[5], self.chest_variable[6], self.chest_variable[7], self.skin_color, self.skin_color,
                                       self.skin_color, self.chest_variable[7]]
            elif value == 5:
                self.shirt_variable = [(0, 0, 0, 254), (0, 0, 0, 254), self.skin_color, self.skin_color, self.skin_color,
                                       self.shirt_color, self.shirt_color, (0, 0, 0, 254), self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, (0, 0, 0, 254), self.shirt_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, (0, 0, 0, 254), self.shirt_color,
                                       (0, 0, 0, 254), self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       (0, 0, 0, 254), self.chest_variable[6], (0, 0, 0, 254), (0, 0, 0, 254), self.shirt_color,
                                       (0, 0, 0, 254), self.chest_variable[6], self.chest_variable[7], self.skin_color, (0, 0, 0, 254),
                                       self.skin_color, self.chest_variable[7]]
            elif value == 6:
                self.shirt_variable = [self.shirt_color, self.shirt_color, self.shirt_color, (0, 0, 0, 254), self.skin_color,
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.skin_color, self.shirt_color, self.skin_color, self.chest_variable[1],
                                       self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.chest_variable[1],
                                       (0, 0, 0, 254), self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color,
                                       self.shirt_color, self.chest_variable[6], (0, 0, 0, 254), self.shirt_color, self.skin_color,
                                       self.shirt_color, self.shirt_color, self.chest_variable[7], self.skin_color, (0, 0, 0, 254),
                                       (0, 0, 0, 254), (0, 0, 0, 254)]
        elif part == "Slee":
            sleeve_dict = {
                0: [self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color, (0, 0, 0, 0), (0, 0, 0, 0), self.skin_color, (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color2],
                1: [self.shirt_color, self.shirt_color, (0, 0, 0, 254), self.skin_color, self.skin_color, self.skin_color, (0, 0, 0, 0), (0, 0, 0, 0), self.skin_color, (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color2],
                2: [self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, (0, 0, 0, 255), self.shirt_color, (0, 0, 0, 0), (0, 0, 0, 0), self.skin_color, (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color2],
                3: [self.shirt_color, self.skin_color, self.shirt_color, self.shirt_color, (0, 0, 0, 255), self.skin_color, (0, 0, 0, 0), (0, 0, 0, 0), self.skin_color, (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color2],
                4: [self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, self.shirt_color, (0, 0, 0, 255), self.shirt_color,  self.shirt_color, self.shirt_color, (0, 0, 0, 255), self.shirt_color]
                           }
            self.sleeve_variable = sleeve_dict[value]

        elif part == "Pant":
            if value == 0:
                self.pants_variable = [self.front_skin_color, self.front_skin_color, self.front_skin_color, self.front_skin_color, (0, 0, 0, 0),
                                       (0, 0, 0, 255), self.front_skin_color, self.front_skin_color, self.leg_variable[1], self.leg_variable[0],
                                       self.front_skin_color, self.leg_variable[1], self.leg_variable[0], self.front_skin_color, self.front_skin_color,
                                       (0, 0, 0, 255), self.front_skin_color, (0, 0, 0, 255), (0, 0, 0, 255), self.front_skin_color]
            elif value == 1:
                self.pants_variable = [self.pants_color, (0, 0, 0, 255), (0, 0, 0, 255), self.pants_color, (0, 0, 0, 0),
                                       (0, 0, 0, 255), (0, 0, 0, 255), self.pants_color, (0, 0, 0, 255), self.pants_color,
                                       self.pants_color, (0, 0, 0, 255), self.pants_color, self.pants_color, self.pants_color,
                                       (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255),]
            elif value == 2:
                self.pants_variable = [self.pants_color, self.pants_color, self.pants_color, self.pants_color, (0, 0, 0, 0),
                                       (0, 0, 0, 255), self.pants_color, self.pants_color, (0, 0, 0, 255), (0, 0, 0, 255),
                                       (0, 0, 0, 255), self.leg_variable[1], self.leg_variable[0], self.skin_color, self.skin_color,
                                       (0, 0, 0, 255), self.skin_color, (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color]
            elif value == 3:
                self.pants_variable = [self.pants_color, self.pants_color, (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 0),
                                       (0, 0, 0, 255), self.skin_color,  self.skin_color, self.leg_variable[1], self.leg_variable[0],
                                       self.skin_color, self.leg_variable[1], self.leg_variable[0], self.skin_color, self.skin_color,
                                       (0, 0, 0, 255), self.skin_color, self.pants_color, (0, 0, 0, 254), self.skin_color]
            elif value == 4:
                self.pants_variable = [self.pants_color, (0, 0, 0, 255), (0, 0, 0, 255), self.pants_color, (0, 0, 0, 0),
                                       (0, 0, 0, 255), self.pants_color, self.pants_color, (0, 0, 0, 255), self.pants_color,
                                       self.pants_color, (0, 0, 0, 255), self.pants_color, (0, 0, 0, 255), self.pants_color,
                                       (0, 0, 0, 255), self.skin_color, self.pants_color, self.pants_color, (0, 0, 0, 255)]
            elif value == 5:
                self.pants_variable = [self.pants_color, (0, 0, 0, 255), (0, 0, 0, 255), self.pants_color, (0, 0, 0, 255),
                                       self.pants_color, self.pants_color, self.pants_color, self.pants_color, self.pants_color,
                                       self.pants_color, (0, 0, 0, 255), self.pants_color, self.pants_color, self.pants_color,
                                       (0, 0, 0, 255), (0, 0, 0, 255), self.pants_color, self.pants_color, (0, 0, 0, 255)]
        elif part == "Shoe":
            if value == 0:
                self.shoes_variable = [self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color]
            elif value == 1:
                self.shoes_variable = [self.shoes_color, (255, 255, 255, 255), self.shoes_color, (255, 255, 255, 255), self.shoes_color]
            elif value == 2:
                self.shoes_variable = [self.shoes_color, self.shoes_color, self.shoes_color, self.shoes_color, self.shoes_color]
            elif value == 3:
                self.shoes_variable = [self.skin_color, self.skin_color, self.shoes_color, self.shoes_color, self.skin_color]
            elif value == 4:
                self.shoes_variable = [self.shoes_color, self.shoes_color, self.shoes_color, self.shoes_color, self.skin_color]

        elif part == "Hair":
            if value == 0:
                self.hair_variable = [(0, 0, 0, 0),
                                      (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                                      (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                                      (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                                      (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                                      (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                                      (0, 0, 0, 0)
                                      ]
            elif value == 1:
                self.hair_variable = [(0, 0, 0, 0),  # 0
                                      (0, 0, 0, 0), self.hair_color, (0, 0, 0, 0), self.hair_color, self.hair_color,  # 1, 2, 3, 4, 5
                                      self.hair_color, self.hair_color, (0, 0, 0, 0), self.hair_color, (0, 0, 0, 0),
                                      (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), self.hair_color, (0, 0, 0, 0),
                                      self.hair_color, self.hair_color, self.hair_color, self.hair_color, self.hair_color,
                                      (0, 0, 0, 0), (0, 0, 0, 0), self.hair_color, (0, 0, 0, 0), self.hair_color,
                                      (0, 0, 0, 0)
                                      ]
            elif value == 2:
                self.hair_variable = [(0, 0, 0, 0),  # 0
                                      (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),  # 1, 2, 3
                                      (0, 0, 0, 0), self.hair_color, (0, 0, 0, 0), (0, 0, 0, 0), self.hair_color,
                                      self.hair_color, self.hair_color, self.hair_color, (0, 0, 0, 0), (0, 0, 0, 0),
                                      self.hair_color, (0, 0, 0, 0), (0, 0, 0, 0), self.hair_color, self.hair_color,
                                      self.hair_color, (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                                      (0, 0, 0, 0)
                                      ]
            elif value == 3:
                self.hair_variable = [(0, 0, 0, 0),  # 0
                                      (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),  # 1, 2, 3
                                      self.hair_color, self.hair_color, (0, 0, 0, 0), (0, 0, 0, 0), self.hair_color,
                                      (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                                      self.hair_color, self.hair_color, self.hair_color, self.hair_color, self.hair_color,
                                      (0, 0, 0, 0), self.hair_color, self.hair_color, self.hair_color, (0, 0, 0, 0),
                                      (0, 0, 0, 0)
                                      ]
            elif value == 4:
                self.hair_variable = [(0, 0, 0, 0), # 0
                                      self.hair_color, (0, 0, 0, 0), self.hair_color, self.hair_color, self.hair_color,  # 1, 2, 3, 4, 5
                                      self.hair_color, self.hair_color, (0, 0, 0, 0), (0, 0, 0, 254), self.hair_color,
                                      (0, 0, 0, 254), (0, 0, 0, 0), (0, 0, 0, 254), (0, 0, 0, 254), (0, 0, 0, 0),
                                      (0, 0, 0, 254), self.hair_color, self.hair_color, self.hair_color, self.hair_color,
                                      (0, 0, 0, 0), self.hair_color, self.hair_color, self.hair_color, (0, 0, 0, 0),
                                      (0, 0, 0, 0)
                                      ]
            elif value == 5:
                self.hair_variable = [self.hair_color,
                                      self.hair_color, self.hair_color, self.hair_color, self.hair_color, self.hair_color,  # 1, 2, 3, 4, 5
                                      self.hair_color, self.hair_color, self.hair_color, self.hair_color, self.hair_color,
                                      (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), self.hair_color, (0, 0, 0, 0),
                                      self.hair_color, self.hair_color, (0, 0, 0, 0), (0, 0, 0, 0),  (0, 0, 0, 0),
                                      (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0),
                                      (0, 0, 0, 0)
                                      ]
            elif value == 6:
                self.hair_variable = [(0, 0, 0, 0),
                                      self.hair_color, self.hair_color, (0, 0, 0, 0), self.hair_color, (0, 0, 0, 0),  # 1, 2, 3, 4, 5
                                      self.hair_color, self.hair_color, self.hair_color, self.hair_color, self.hair_color,
                                      self.hair_color, (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), self.hair_color,
                                      self.hair_color, (0, 0, 0, 0), self.hair_color, self.hair_color, (0, 0, 0, 0),
                                      self.hair_color, (0, 0, 0, 0), (0, 0, 0, 0), self.hair_color, (0, 0, 0, 0),
                                      (0, 0, 0, 0)
                                      ]

    def update_orientation(self, orientation, lock):
        # print("orientation: ", orientation)
        if lock == 0:
            if orientation == 0:
                self.orientation = "Front"
                self.walking = 0
                self.arm_raise = (0, 0)
                self.leg_raise = (0, 0)
                self.foot_raise = (0, 0)
                self.front_skin_color = self.skin_color
            elif orientation == 1:
                self.walking = 0
                self.arm_raise = (0, 0)
                self.leg_raise = (0, 0)
                self.foot_raise = (0, 0)
                self.orientation = "Left"
                self.front_skin_color = self.skin_color
            elif orientation == 2:
                self.walking = 0
                self.arm_raise = (0, 0)
                self.leg_raise = (0, 0)
                self.foot_raise = (0, 0)
                self.orientation = "Back"
                self.front_skin_color = self.skin_color
            elif orientation == 3:
                self.walking = 0
                self.arm_raise = (0, 0)
                self.leg_raise = (0, 0)
                self.foot_raise = (0, 0)
                self.orientation = "Right"
                self.front_skin_color = self.skin_color
        else:
            if orientation == 0:
                self.orientation = "Front"
                self.walking = 0
                self.arm_raise = (0, 0)
                self.leg_raise = (0, 0)
                self.foot_raise = (0, 0)
                self.front_skin_color = self.skin_color
            elif orientation == 1:
                self.walking = 1
                self.arm_raise = (-20,20)
                self.leg_raise = (20, -20)
                self.foot_raise = (10, -40)
                self.orientation = "Front"
                self.front_skin_color = self.skin_color
            elif orientation == 2:
                self.walking = 2
                self.arm_raise = (20, -20)
                self.leg_raise = (-20, 20)
                self.foot_raise = (-10, 40)
                self.orientation = "Front"
                self.front_skin_color = self.skin_color
            elif orientation == 3:
                self.walking = 0
                self.arm_raise = (0, 0)
                self.leg_raise = (0, 0)
                self.foot_raise = (0, 0)
                self.orientation = "Left"
                self.front_skin_color = self.skin_color
            elif orientation == 4:
                self.walking = 1
                self.back_skin_color = self.skin_color2
                self.front_skin_color = self.skin_color
                # self.SIDE_HAND_WALKF = rotate_ranges_degrees(self.SIDE_HAND, 45, (620, 300))
                # self.SIDE_HAND_WALKB = rotate_ranges_degrees(self.SIDE_HAND, -45, (620, 300))
                # self.LEFT_LEGF = rotate_ranges_degrees(self.SIDE_LEGS, 45, (620, 380))
                # self.LEFT_LEGB = rotate_ranges_degrees(self.SIDE_HAND, -45, (620, 380))
                # self.SIDE_HAND_WALKB = {}
                # self.LEFT_LEGF = {}
                # self.LEFT_LEGB = {}
                self.orientation = "Left"
            elif orientation == 5:
                self.walking = 2
                self.back_skin_color = self.skin_color
                self.front_skin_color = self.skin_color2
                # self.SIDE_HAND_WALKF = rotate_ranges_degrees(self.SIDE_HAND, -45, (640, 300))
                # self.SIDE_HAND_WALKB = rotate_ranges_degrees(self.SIDE_HAND, 45, (620, 300))

                # self.LEFT_LEGF = rotate_ranges_degrees(self.SIDE_LEGS, -15, (620, 360))
                # temp_disc = rotate_ranges_degrees(self.LEFT_SHOE, -15, (620, 360))
                # self.LEFT_LEGF.update(temp_disc)
                #
                # self.LEFT_LEGB = rotate_ranges_degrees(self.SIDE_LEGS, 15, (620, 360))
                # temp_disc = rotate_ranges_degrees(self.LEFT_SHOE, 15, (620, 360))
                # self.LEFT_LEGB.update(temp_disc)
                #
                # self.SIDE_HAND_WALKF = {}
                # self.SIDE_HAND_WALKB = {}
                # self.LEFT_LEGF = {}
                # self.LEFT_LEGB = {}
                self.orientation = "Left"
            elif orientation == 6:
                self.walking = 0
                self.arm_raise = (0, 0)
                self.leg_raise = (0, 0)
                self.foot_raise = (0, 0)
                self.orientation = "Back"
                self.front_skin_color = self.skin_color
            elif orientation == 7:
                self.walking = 1
                self.arm_raise = (20, -20)
                self.leg_raise = (-20, 20)
                self.foot_raise = (-10, 40)
                self.orientation = "Back"
                self.front_skin_color = self.skin_color
            elif orientation == 8:
                self.walking = 2
                self.arm_raise = (-20,20)
                self.leg_raise = (20, -20)
                self.foot_raise = (10, -40)
                self.orientation = "Back"
                self.front_skin_color = self.skin_color
            elif orientation == 9:
                self.walking = 0
                self.arm_raise = (0, 0)
                self.leg_raise = (0, 0)
                self.foot_raise = (0, 0)
                self.orientation = "Right"
                self.front_skin_color = self.skin_color
            elif orientation == 10:
                self.walking = 1
                self.back_skin_color = self.skin_color2
                self.front_skin_color = self.skin_color
                # self.SIDE_HAND_WALKF = rotate_ranges_degrees(self.SIDE_HAND, 45, (620, 300))
                # self.SIDE_HAND_WALKB = {}
                # self.LEFT_LEGF = {}
                # self.LEFT_LEGB = {}
                self.orientation = "Right"
            elif orientation == 11:
                self.walking = 2
                self.back_skin_color = self.skin_color
                self.front_skin_color = self.skin_color2 # NOTHING bug
                # self.SIDE_HAND_WALKF = rotate_ranges_degrees(self.SIDE_HAND, -45, (640, 300))
                # self.SIDE_HAND_WALKB = {}
                # self.LEFT_LEGF = {}
                # self.LEFT_LEGB = {}
                self.orientation = "Right"

    def update_for_gender_race(self, gender, race):
        self.gender = gender
        self.race = race
        if self.orientation in ["Front", "Back"]:
            if race == "Human":
                self.leg_push = 0
                self.foot_push = 0
                if gender == "Boy":
                    self.arm_push = 0
                    self.arm_push = 0
                    self.head_variable = [(0, 0, 0, 255), self.skin_color, (0, 0, 0, 255), (0, 0, 0, 0), (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color, self.skin_color, self.skin_color, self.skin_color]
                    self.chest_variable = [(0, 0, 0, 255), self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color]
                    self.leg_variable = [self.skin_color, (0, 0, 0, 255)]
                elif gender == "Girl":
                    self.arm_push = 10
                    self.arm_push = 10
                    self.head_variable = [(0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color, self.skin_color, self.skin_color, self.skin_color]
                    self.chest_variable = [(0, 0, 0, 255), self.skin_color, self.skin_color, (0, 0, 0, 255), (0, 0, 0, 0), (0, 0, 0, 255), (0, 0, 0, 0), (0, 0, 0, 255)]
                    self.leg_variable = [(0, 0, 0, 255), (0, 0, 0, 0)]
            elif race == "Elf":
                self.ELF_EAR_TIPS = {

                    # Left ear
                    (550, 560, 180 + self.push_up, 190 + self.push_up): (0, 0, 0, 255),

                    (550, 570, 190 + self.push_up, 200 + self.push_up): (0, 0, 0, 255),

                    (550, 560, 200 + self.push_up, 220 + self.push_up): (0, 0, 0, 255),
                    (560, 570, 200 + self.push_up, 210 + self.push_up): self.skin_color2,
                    (570, 580, 200 + self.push_up, 210 + self.push_up): (0, 0, 0, 255),

                    # Right ear
                    (690, 700, 180 + self.push_up, 190 + self.push_up): (0, 0, 0, 255),

                    (680, 700, 190 + self.push_up, 200 + self.push_up): (0, 0, 0, 255),

                    (670, 680, 200 + self.push_up, 210 + self.push_up): (0, 0, 0, 255),
                    (680, 690, 200 + self.push_up, 210 + self.push_up): self.skin_color2,
                    (690, 700, 200 + self.push_up, 220 + self.push_up): (0, 0, 0, 255),
                }
                self.head_variable = [(0, 0, 0, 0), self.skin_color2, (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color, (0, 0, 0, 255), self.skin_color, self.skin_color, self.skin_color, self.skin_color]
                if gender == "Boy":
                    self.arm_push = 0
                    self.arm_push = 0
                    self.leg_push = 10
                    self.foot_push = 10
                    self.chest_variable = [self.skin_color2, self.skin_color, self.skin_color, (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color, (0, 0, 0, 255), (0, 0, 0, 255)]
                    self.leg_variable = [self.skin_color, (0, 0, 0, 255)]
                if gender == "Girl":
                    self.arm_push = 10
                    self.arm_push = 10
                    self.leg_push = 0
                    self.foot_push = 0
                    self.chest_variable = [self.skin_color2, (0, 0, 0, 255), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 255), self.skin_color, self.skin_color, self.skin_color]
                    self.leg_variable = [(0, 0, 0, 255), (0, 0, 0, 0)]
        else:
            if self.orientation in ["Left", "Right"] and self.race == "Human":
                if self.gender == "Boy":
                    self.head_variable = [(0, 0, 0, 255), self.skin_color, (0, 0, 0, 255), (0, 0, 0, 0), (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color, self.skin_color, self.skin_color, self.skin_color]
                elif self.gender == "Girl":
                    self.head_variable = [(0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color, self.skin_color, self.skin_color, self.skin_color]
            elif self.orientation == "Right" and self.race == "Elf":
                self.head_variable =[(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), self.skin_color, (0, 0, 0, 0), (0, 0, 0, 255), self.skin_color2, self.skin_color, self.skin_color]
            elif self.orientation == "Left" and self.race == "Elf":
                self.head_variable =[(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), self.skin_color, (0, 0, 0, 0), self.skin_color, self.skin_color, (0, 0, 0, 255), self.skin_color2]
            self.LEFT_ELF_EAR_TIPS = {

                (650, 660, 180 + self.push_up, 190 + self.push_up): (0, 0, 0, 255),
                #
                (640, 660, 190 + self.push_up, 200 + self.push_up): (0, 0, 0, 255),

                (650, 660, 200 + self.push_up, 210 + self.push_up): (0, 0, 0, 255),
                (640, 650, 200 + self.push_up, 210 + self.push_up): self.skin_color2,
                (630, 640, 200 + self.push_up, 210 + self.push_up): (0, 0, 0, 255),
            }
            self.RIGHT_ELF_EAR_TIPS = {
                (590, 600, 180 + self.push_up, 190 + self.push_up): (0, 0, 0, 255),

                (590, 610, 190 + self.push_up, 200 + self.push_up): (0, 0, 0, 255),

                (590, 600, 200 + self.push_up, 210 + self.push_up): (0, 0, 0, 255),
                (600, 610, 200 + self.push_up, 210 + self.push_up): self.skin_color2,
                (610, 620, 200 + self.push_up, 210 + self.push_up): (0, 0, 0, 255),
            }

        if I.TD.Appearance == {}:
            self.shirt_variable = [self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color,
                                   self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color,
                                   self.chest_variable[1], self.skin_color, self.chest_variable[2], self.skin_color, self.chest_variable[1],
                                   self.chest_variable[3], self.chest_variable[1], self.skin_color, self.skin_color, self.chest_variable[1],
                                   self.chest_variable[4], self.chest_variable[5], self.skin_color, self.skin_color, self.skin_color,
                                   self.chest_variable[4], self.chest_variable[6], self.chest_variable[5], self.skin_color, self.skin_color,
                                   self.chest_variable[5], self.chest_variable[6], self.chest_variable[7], self.skin_color, self.skin_color,
                                   self.skin_color, self.chest_variable[7]]

            self.sleeve_variable = [self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color, (0, 0, 0, 0), (0, 0, 0, 0), self.skin_color, (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color2, self.skin_color2]

            self.pants_variable = [self.skin_color, self.skin_color, self.skin_color, self.skin_color, (0, 0, 0, 0),
                                   (0, 0, 0, 255), self.skin_color, self.skin_color, self.leg_variable[1], self.leg_variable[0],
                                   self.skin_color, self.leg_variable[1], self.leg_variable[0], self.skin_color, self.skin_color,
                                   (0, 0, 0, 255), self.skin_color, (0, 0, 0, 255), (0, 0, 0, 255), self.skin_color ]

            self.shoes_variable = [self.skin_color, self.skin_color, self.skin_color, self.skin_color, self.skin_color]
        self.HEAD = {
            # (510, 600, 170, 180): (255, 255, 255, 255),  # 1 line
            (600, 650, 170 + self.push_up, 180 + self.push_up): (0, 0, 0, 255),
            # (650, 740, 170, 180): (255, 255, 255, 255),

            # (510, 580, 180, 190): (255, 255, 255, 255),  # 2 line
            (580, 600, 180 + self.push_up, 190 + self.push_up): (0, 0, 0, 255),
            (600, 650, 180 + self.push_up, 190 + self.push_up): self.skin_color,
            (650, 670, 180 + self.push_up, 190 + self.push_up): (0, 0, 0, 255),
            # (670, 740, 180, 190): (255, 255, 255, 255),

            # (510, 570, 190, 210): (255, 255, 255, 255),  # 3, 4 line
            (570, 580, 190 + self.push_up, 210 + self.push_up): self.head_variable[0],
            (580, 670, 190 + self.push_up, 210 + self.push_up): self.skin_color,
            (670, 680, 190 + self.push_up, 210 + self.push_up): self.head_variable[0],
            # (680, 740, 190, 210): (255, 255, 255, 255),

            # (510, 560, 210, 230): (255, 255, 255, 255),  # 5, 6 line
            (560, 570, 210 + self.push_up, 230 + self.push_up): self.head_variable[2],
            (570, 580, 210 + self.push_up, 230 + self.push_up): self.head_variable[1],
            (580, 600, 210 + self.push_up, 230 + self.push_up): self.skin_color,
            (600, 610, 210 + self.push_up, 230 + self.push_up): self.head_variable[6],  # LEFT EAR
            (610, 620, 210 + self.push_up, 230 + self.push_up): self.head_variable[7],  # LEFT EAR
            (620, 630, 210 + self.push_up, 230 + self.push_up): self.skin_color,
            (630, 640, 210 + self.push_up, 230 + self.push_up): self.head_variable[9],  # RIGHT EAR
            (640, 650, 210 + self.push_up, 230 + self.push_up): self.head_variable[8],  # RIGHT EAR
            (650, 670, 210 + self.push_up, 230 + self.push_up): self.skin_color,
            (670, 680, 210 + self.push_up, 230 + self.push_up): self.head_variable[1],
            (680, 690, 210 + self.push_up, 230 + self.push_up): self.head_variable[2],
            # (690, 740, 210, 230): (255, 255, 255, 255),

            # (510, 570, 230, 250): (255, 255, 255, 255),  # 7, 8 line
            (550, 560, 230 + self.push_up, 240 + self.push_up): self.head_variable[3],
            (570, 580, 230 + self.push_up, 240 + self.push_up): self.head_variable[5],
            (570, 580, 240 + self.push_up, 250 + self.push_up): self.head_variable[0],
            (580, 590, 230 + self.push_up, 240 + self.push_up): self.skin_color,
            (590, 600, 230 + self.push_up, 240 + self.push_up): self.head_variable[6],  # LEFT EAR
            (600, 610, 230 + self.push_up, 240 + self.push_up): self.skin_color,
            (610, 620, 230 + self.push_up, 240 + self.push_up): self.head_variable[6],  # LEFT EAR
            (620, 630, 230 + self.push_up, 240 + self.push_up): self.skin_color,
            (630, 640, 230 + self.push_up, 240 + self.push_up): self.head_variable[8],  # RIGHT EAR
            (640, 650, 230 + self.push_up, 240 + self.push_up): self.skin_color,
            (650, 660, 230 + self.push_up, 240 + self.push_up): self.head_variable[8],  # RIGHT EAR
            (660, 670, 230 + self.push_up, 240 + self.push_up): self.skin_color,

            (580, 670, 240 + self.push_up, 250 + self.push_up): self.skin_color,
            (670, 680, 230 + self.push_up, 240 + self.push_up): self.head_variable[5],
            (690, 700, 230 + self.push_up, 240 + self.push_up): self.head_variable[3],
            (670, 680, 240 + self.push_up, 250 + self.push_up): self.head_variable[0],
            # (680, 740, 230, 250): (255, 255, 255, 255),

            # (510, 580, 250, 260): (255, 255, 255, 255),  # 9 line
            (580, 590, 250 + self.push_up, 260 + self.push_up): (0, 0, 0, 255),
            (590, 660, 250 + self.push_up, 260 + self.push_up): self.skin_color,
            (660, 670, 250 + self.push_up, 260 + self.push_up): (0, 0, 0, 255),
            # (670, 740, 250, 260): (255, 255, 255, 255),

            # (510, 590, 260, 270): (255, 255, 255, 255),  # 10 line
            (590, 600, 260 + self.push_up, 270 + self.push_up): (0, 0, 0, 255),
            (600, 610, 260 + self.push_up, 270 + self.push_up): self.head_variable[4],
            (610, 640, 260 + self.push_up, 270 + self.push_up): self.skin_color,
            (640, 650, 260 + self.push_up, 270 + self.push_up): self.head_variable[4],
            (650, 660, 260 + self.push_up, 270 + self.push_up): (0, 0, 0, 255),
            # (660, 740, 260, 270): (255, 255, 255, 255),
        }

        self.CHEST = {
            (570, 610, 270 + self.push_up, 280 + self.push_up): (0, 0, 0, 255),
            (610, 620, 270 + self.push_up, 280 + self.push_up): self.chest_variable[0],
            (620, 630, 270 + self.push_up, 280 + self.push_up): self.skin_color2,
            (630, 640, 270 + self.push_up, 280 + self.push_up): self.chest_variable[0],
            (640, 680, 270 + self.push_up, 280 + self.push_up): (0, 0, 0, 255),

            (580, 590, 280 + self.push_up, 290 + self.push_up): self.shirt_variable[0],  # 1st 2nd 3rd (black) 4th 5th 6th (black) 7th
            (590, 600, 280 + self.push_up, 290 + self.push_up): self.shirt_variable[1],  # 1st 2nd 3rd 4th 5th (black) 6th (black) 7th
            (600, 610, 280 + self.push_up, 290 + self.push_up): self.shirt_variable[2],  # 1st 2nd 3rd (black) 4th 5th 7th
            (610, 620, 280 + self.push_up, 290 + self.push_up): self.shirt_variable[3],  # 1st (black) 2nd (black) 4th (black) 5th (black) 7th (black)
            (620, 630, 280 + self.push_up, 290 + self.push_up): self.skin_color2,
            (630, 640, 280 + self.push_up, 290 + self.push_up): self.shirt_variable[3],
            (640, 650, 280 + self.push_up, 290 + self.push_up): self.shirt_variable[4], # 1st 2nd 3rd (black) 4th 5th
            (650, 660, 280 + self.push_up, 290 + self.push_up): self.shirt_variable[1],
            (660, 670, 280 + self.push_up, 290 + self.push_up): self.shirt_variable[0],

            (580, 590, 290 + self.push_up, 300 + self.push_up): self.shirt_variable[5],  # 1st 2nd 3rd (black) 4th 5th (black) 6th 7th
            (590, 600, 290 + self.push_up, 300 + self.push_up): self.shirt_variable[6],  # all
            (600, 610, 290 + self.push_up, 300 + self.push_up): self.shirt_variable[7],  # 1st 2nd 3rd 4th 5th 6th (black) 7th
            (610, 620, 290 + self.push_up, 300 + self.push_up): self.shirt_variable[2],
            (620, 630, 290 + self.push_up, 300 + self.push_up): self.shirt_variable[3],
            (630, 640, 290 + self.push_up, 300 + self.push_up): self.shirt_variable[2],
            (640, 650, 290 + self.push_up, 300 + self.push_up): self.shirt_variable[7],
            (650, 660, 290 + self.push_up, 300 + self.push_up): self.shirt_variable[6],
            (660, 670, 290 + self.push_up, 300 + self.push_up): self.shirt_variable[5],

            (580, 590, 300 + self.push_up, 310 + self.push_up): self.shirt_variable[8],  # 1st 2nd 3rd (black) 4th 5th 6th 7th
            (590, 610, 300 + self.push_up, 310 + self.push_up): self.shirt_variable[6],  # all
            (610, 620, 300 + self.push_up, 310 + self.push_up): self.shirt_variable[7],
            (620, 630, 300 + self.push_up, 310 + self.push_up): self.shirt_variable[0],
            (630, 640, 300 + self.push_up, 310 + self.push_up): self.shirt_variable[7],
            (640, 660, 300 + self.push_up, 310 + self.push_up): self.shirt_variable[6],  # all
            (660, 670, 300 + self.push_up, 310 + self.push_up): self.shirt_variable[8],

            (580, 670, 310 + self.push_up, 320 + self.push_up): self.shirt_variable[6],  # all

            (580, 590, 320 + self.push_up, 330 + self.push_up): self.shirt_variable[9],  # 1st 2nd 3rd 4th 5th (black) 6th 7th
            (590, 610, 320 + self.push_up, 330 + self.push_up): self.shirt_variable[6],
            (610, 620, 320 + self.push_up, 330 + self.push_up): self.shirt_variable[7],
            (620, 630, 320 + self.push_up, 330 + self.push_up): self.shirt_variable[6],
            (630, 640, 320 + self.push_up, 330 + self.push_up): self.shirt_variable[7],
            (640, 660, 320 + self.push_up, 330 + self.push_up): self.shirt_variable[6],
            (660, 670, 320 + self.push_up, 330 + self.push_up): self.shirt_variable[9],  # 1st 2nd 3rd 4th 5th (black) 6th 7th

            (580, 590, 330 + self.push_up, 340 + self.push_up): self.shirt_variable[10],  # 1st 2nd 3rd 4th 5th (set1) 6th 7th
            (590, 600, 330 + self.push_up, 340 + self.push_up): self.shirt_variable[9],
            (600, 640, 330 + self.push_up, 340 + self.push_up): self.shirt_variable[6],
            (640, 650, 330 + self.push_up, 340 + self.push_up): self.shirt_variable[11],  #1st 2nd 3rd 4th 5th 6th
            (650, 660, 330 + self.push_up, 340 + self.push_up): self.shirt_variable[9],
            (660, 670, 330 + self.push_up, 340 + self.push_up): self.shirt_variable[10],


            (580, 590, 340 + self.push_up, 350 + self.push_up): self.shirt_variable[12],  # 1st 2nd 3rd 4th 5th (set2) 6th 7th
            (590, 600, 340 + self.push_up, 350 + self.push_up): self.shirt_variable[10],
            (600, 610, 340 + self.push_up, 350 + self.push_up): self.shirt_variable[1],
            (610, 640, 340 + self.push_up, 350 + self.push_up): self.shirt_variable[6],
            (640, 650, 340 + self.push_up, 350 + self.push_up): self.shirt_variable[13],  # 1st 2nd 3rd 4th 5th (black) 6th (black)
            (650, 660, 340 + self.push_up, 350 + self.push_up): self.shirt_variable[14],
            (660, 670, 340 + self.push_up, 350 + self.push_up): self.shirt_variable[12],

            (580, 590, 350 + self.push_up, 360 + self.push_up): self.shirt_variable[15],  # 1st 2nd 3rd 4th 5th (set3) 6th 7th
            (590, 600, 350 + self.push_up, 360 + self.push_up): self.shirt_variable[16],  # 1st 2nd 3rd 4th 5th (set3) 6th 7th
            (600, 610, 350 + self.push_up, 360 + self.push_up): self.shirt_variable[17],  # 1st 2nd 3rd 4th 6th 7th
            (610, 620, 350 + self.push_up, 360 + self.push_up): self.shirt_variable[18],  # 1st 2nd 3rd 4th (black) 5th (black) 6th (black) 7th
            (620, 630, 350 + self.push_up, 360 + self.push_up): self.shirt_variable[7],
            (630, 640, 350 + self.push_up, 360 + self.push_up): self.shirt_variable[18],
            (640, 650, 350 + self.push_up, 360 + self.push_up): self.shirt_variable[17],
            (650, 660, 350 + self.push_up, 360 + self.push_up): self.shirt_variable[19], # 1st 2nd 3rd 4th (black) 5th (set1) 6th 7th (set1)
            (660, 670, 350 + self.push_up, 360 + self.push_up): self.shirt_variable[15],

            (580, 590, 360 + self.push_up, 370 + self.push_up): self.shirt_variable[20],  # 1st 2nd 3rd 4th (black) 5th (set4) 6th (black) 7th (black)
            (590, 600, 360 + self.push_up, 370 + self.push_up): self.shirt_variable[21],  # 1st 2nd 3rd 4th (set5) 5th (set5) 6th 7th
            (600, 610, 360 + self.push_up, 370 + self.push_up): self.shirt_variable[22],  # 1st 2nd 3rd 4th (black) 6th 7th
            (610, 620, 360 + self.push_up, 370 + self.push_up): self.shirt_variable[23],  # 1st 2nd 3rd 6th 7th
            (620, 630, 360 + self.push_up, 370 + self.push_up): self.shirt_variable[24],  # 1st 2nd 3rd 4th (black) 5th (black) 6th 7th
            (630, 640, 360 + self.push_up, 370 + self.push_up): self.shirt_variable[23],
            (640, 650, 360 + self.push_up, 370 + self.push_up): self.shirt_variable[22],
            (650, 660, 360 + self.push_up, 370 + self.push_up): self.shirt_variable[21],
            (660, 670, 360 + self.push_up, 370 + self.push_up): self.shirt_variable[25],  # 1st 2nd 3rd 4th (black) 5th (set4) 6th (black) 7th

            (580, 590, 370 + self.push_up, 380 + self.push_up): self.shirt_variable[26],  # 1st 2nd 3rd 4th (set6) 5th (set6) 6th (set6) 7th (set6)
            (590, 600, 370 + self.push_up, 380 + self.push_up): self.shirt_variable[27],  # 1st 2nd 3rd 4th (set5) 5th (set5) 6th (black) 7th (black)
            (600, 610, 370 + self.push_up, 380 + self.push_up): self.shirt_variable[28],  # 1st 2nd 3rd 6th (black) 7th
            (610, 620, 370 + self.push_up, 380 + self.push_up): self.shirt_variable[29],  # 1st 2nd 3rd 6th
            (620, 640, 370 + self.push_up, 380 + self.push_up): self.shirt_variable[23],
            (640, 650, 370 + self.push_up, 380 + self.push_up): self.shirt_variable[28],
            (650, 660, 370 + self.push_up, 380 + self.push_up): self.shirt_variable[30],  # 1st 2nd 3rd 4th (set5) 5th (set5) 6th (black) 7th
            (660, 670, 370 + self.push_up, 380 + self.push_up): self.shirt_variable[31],  # 1st 2nd 3rd 4th (set6) 5th (set6) 6th (set6) 7th

            (580, 590, 380 + self.push_up, 390 + self.push_up): self.shirt_variable[32],  # 1st (black) 2nd (black) 3rd (black) 4th (set7) 5th (set7) 6th (set7) 7th (set7)
            (590, 600, 380 + self.push_up, 390 + self.push_up): self.shirt_variable[33],  # 1st (black) 2nd (black) 3rd (black)
            (600, 650, 380 + self.push_up, 390 + self.push_up): self.shirt_variable[34],  # 1st (black) 2nd (black) 3rd (black) 6th (black) 7th (black)
            (650, 660, 380 + self.push_up, 390 + self.push_up): self.shirt_variable[35],  # 1st (black) 2nd (black) 3rd (black) 7th (black)
            (660, 670, 380 + self.push_up, 390 + self.push_up): self.shirt_variable[36],  # 1st (black) 2nd (black) 3rd (black) 4th (set7) 5th (set7) 6th (set7) 7th (black)



            (670, 680, 310 + self.push_up, 390 + self.push_up): (0, 0, 0, 255),

        }
        self.SIDE_CHEST = {
            (600, 620, 270 + self.push_up, 280 + self.push_up): (0, 0, 0, 255),
            (620, 630, 270 + self.push_up, 280 + self.push_up): self.skin_color2,
            (630, 650, 270 + self.push_up, 280 + self.push_up): (0, 0, 0, 255),

            (590, 600, 280 + self.push_up, 290 + self.push_up): (0, 0, 0, 255),
            (600, 620, 280 + self.push_up, 290 + self.push_up): self.shirt_variable[6],
            (620, 630, 280 + self.push_up, 290 + self.push_up): self.skin_color2,
            (630, 650, 280 + self.push_up, 290 + self.push_up): self.shirt_variable[6],
            (650, 660, 280 + self.push_up, 290 + self.push_up): (0, 0, 0, 255),

            (580, 590, 290 + self.push_up, 360 + self.push_up): (0, 0, 0, 255),
            (590, 660, 290 + self.push_up, 330 + self.push_up): self.shirt_variable[6],
            (590, 660, 330 + self.push_up, 360 + self.push_up): self.shirt_variable[6],
            (660, 670, 290 + self.push_up, 360 + self.push_up): (0, 0, 0, 255),

            (590, 600, 360 + self.push_up, 390 + self.push_up): (0, 0, 0, 255),
            (600, 650, 360 + self.push_up, 390 + self.push_up): self.shirt_variable[6],
            (650, 660, 360 + self.push_up, 390 + self.push_up): (0, 0, 0, 255),

        }

        self.FOOT_LEFT = {
            (580 + self.foot_push, 590 + self.foot_push, 450 + self.push_up - self.leg_raise[0], 460 + self.push_up - self.leg_raise[0]): (0, 0, 0, 255),  # 31
            (590 + self.foot_push, 620, 450 + self.push_up - self.leg_raise[0], 460 + self.push_up - self.leg_raise[0]): self.shoes_variable[0],
            (620, 630, 450 + self.push_up - self.leg_raise[0], 460 + self.push_up - self.leg_raise[0]): (0, 0, 0, 255),

            (610 + self.foot_push, 630, 460 + self.push_up - self.leg_raise[0], 490 + self.push_up - self.leg_raise[0]): (0, 0, 0, 255),
            (570 + self.foot_push, 580 + self.foot_push, 460 + self.push_up - self.leg_raise[0], 490 + self.push_up - self.leg_raise[0]): (0, 0, 0, 255),  # 32, 33, 34

            (580 + self.foot_push, 590 + self.foot_push, 460 + self.push_up - self.leg_raise[0], 470 + self.push_up - self.leg_raise[0]): self.shoes_variable[3],
            (590 + self.foot_push, 600, 460 + self.push_up - self.leg_raise[0], 470 + self.push_up - self.leg_raise[0]): self.shoes_variable[0],
            (600, 620, 460 + self.push_up - self.leg_raise[0], 470 + self.push_up - self.leg_raise[0]): self.shoes_variable[4],

            (580 + self.foot_push, 590, 470 + self.push_up - self.leg_raise[0], 480 + self.push_up - self.leg_raise[0]): self.shoes_variable[0],
            (590, 600, 470 + self.push_up - self.leg_raise[0], 480 + self.push_up - self.leg_raise[0]): self.shoes_variable[2],
            (600, 620, 470 + self.push_up - self.leg_raise[0], 480 + self.push_up - self.leg_raise[0]): self.shoes_variable[4],

            (580 + self.foot_push, 600, 480 + self.push_up - self.leg_raise[0], 490 + self.push_up - self.leg_raise[0]): self.shoes_variable[0],
            (600, 610, 480 + self.push_up - self.leg_raise[0], 490 + self.push_up - self.leg_raise[0]): self.shoes_variable[2],
            (610, 620, 480 + self.push_up - self.leg_raise[0], 490 + self.push_up - self.leg_raise[0]): self.shoes_variable[0],

            (580 + self.foot_push, 620, 490 + self.push_up - self.leg_raise[0], 500 + self.push_up - self.leg_raise[0]): (0, 0, 0, 255),  # 35

        }
        self.FOOT_RIGHT = {
            (620, 630, 450 + self.push_up - self.leg_raise[1], 460 + self.push_up - self.leg_raise[1]): (0, 0, 0, 255),
            # 31
            (630, 660, 450 + self.push_up - self.leg_raise[1], 460 + self.push_up - self.leg_raise[1]): self.shoes_variable[0],  # first
            (660 - self.foot_push, 670 - self.foot_push, 450 + self.push_up - self.leg_raise[1], 460 + self.push_up - self.leg_raise[1]): (0, 0, 0, 255),

            (620, 630, 460 + self.push_up - self.leg_raise[1], 490 + self.push_up - self.leg_raise[1]): (0, 0, 0, 255),
            # 32, 33, 34
            (630, 650, 460 + self.push_up - self.leg_raise[1], 470 + self.push_up - self.leg_raise[1]): self.shoes_variable[4],
            (650, 660, 460 + self.push_up - self.leg_raise[1], 470 + self.push_up - self.leg_raise[1]): self.shoes_variable[0],
            (660 - self.foot_push, 670, 460 + self.push_up - self.leg_raise[1], 470 + self.push_up - self.leg_raise[1]): self.shoes_variable[3], # second

            (630, 650, 470 + self.push_up - self.leg_raise[1], 480 + self.push_up - self.leg_raise[1]): self.shoes_variable[4],
            (650, 660, 470 + self.push_up - self.leg_raise[1], 480 + self.push_up - self.leg_raise[1]): self.shoes_variable[2], # third
            (660, 670 - self.foot_push, 470 + self.push_up - self.leg_raise[1], 480 + self.push_up - self.leg_raise[1]): self.shoes_variable[0],

            (630, 640, 480 + self.push_up - self.leg_raise[1], 490 + self.push_up - self.leg_raise[1]): self.shoes_variable[0],
            (640, 650, 480 + self.push_up - self.leg_raise[1], 490 + self.push_up - self.leg_raise[1]): self.shoes_variable[2], # fourth
            (650, 670 - self.foot_push, 480 + self.push_up - self.leg_raise[1], 490 + self.push_up - self.leg_raise[1]): self.shoes_variable[0],

            (670 - self.foot_push, 680 - self.foot_push, 460 + self.push_up - self.leg_raise[1], 490 + self.push_up - self.leg_raise[1]): (0, 0, 0, 255),
            #
            (630, 670 - self.foot_push, 490 + self.push_up - self.leg_raise[1], 500 + self.push_up - self.leg_raise[1]): (0, 0, 0, 255),  # 35
        }
        self.LEFT_SHOE = {
            (600, 620, 450 + self.push_up, 460 + self.push_up): (0, 0, 0, 255),
            (620, 650, 450 + self.push_up, 460 + self.push_up): self.shoes_variable[4],
            (650, 660, 450 + self.push_up, 460 + self.push_up): (0, 0, 0, 255),

            (590, 600, 460 + self.push_up, 490 + self.push_up): (0, 0, 0, 255),

            (600, 610, 460 + self.push_up, 470 + self.push_up): self.shoes_variable[1], # 1st (white) 2nd
            (610, 620, 460 + self.push_up, 470 + self.push_up): self.shoes_variable[2], # all red
            (620, 650, 460 + self.push_up, 470 + self.push_up): self.shoes_variable[4], # 1st 2nd red others skin

            (600, 610, 470 + self.push_up, 480 + self.push_up): self.shoes_variable[0],
            (610, 620, 470 + self.push_up, 480 + self.push_up): self.shoes_variable[2],
            (620, 650, 470 + self.push_up, 480 + self.push_up): self.shoes_variable[4],

            (600, 610, 480 + self.push_up, 490 + self.push_up): self.shoes_variable[0],
            (610, 620, 480 + self.push_up, 490 + self.push_up): self.shoes_variable[2],
            (620, 650, 480 + self.push_up, 490 + self.push_up): self.shoes_variable[0],

            (650, 660, 460 + self.push_up, 490 + self.push_up): (0, 0, 0, 255),

            (600, 650, 490 + self.push_up, 500 + self.push_up): (0, 0, 0, 255),
        }
        self.RIGHT_SHOE = {

            (590, 600, 450 + self.push_up, 460 + self.push_up): (0, 0, 0, 255),
            (600, 630, 450 + self.push_up, 460 + self.push_up): self.shoes_variable[4],
            (630, 650, 450 + self.push_up, 460 + self.push_up): (0, 0, 0, 255),

            (590, 600, 460 + self.push_up, 490 + self.push_up): (0, 0, 0, 255),
            (600, 630, 460 + self.push_up, 470 + self.push_up): self.shoes_variable[4],
            (630, 640, 460 + self.push_up, 470 + self.push_up): self.shoes_variable[2],
            (640, 650, 460 + self.push_up, 470 + self.push_up): self.shoes_variable[1],

            (600, 630, 470 + self.push_up, 480 + self.push_up): self.shoes_variable[4],
            (630, 640, 470 + self.push_up, 480 + self.push_up): self.shoes_variable[2],
            (640, 650, 470 + self.push_up, 480 + self.push_up): self.shoes_variable[0],

            (600, 630, 480 + self.push_up, 490 + self.push_up): self.shoes_variable[0],
            (630, 640, 480 + self.push_up, 490 + self.push_up): self.shoes_variable[2],
            (640, 650, 480 + self.push_up, 490 + self.push_up): self.shoes_variable[0],

            (650, 660, 460 + self.push_up, 490 + self.push_up): (0, 0, 0, 255),

            (600, 650, 490 + self.push_up, 500 + self.push_up): (0, 0, 0, 255),
        }

        self.LEG_LEFT = {
            # (510, 570, 390, 410 + self.push_up): (255, 255, 255, 255),
            (570 + self.leg_push, 580 + self.leg_push, 390 + self.push_up - self.leg_raise[0], 410 + self.push_up): (0, 0, 0, 255),  # 23, 24

            (570 + self.leg_push, 580 + self.leg_push, 390 + self.push_up, 430 + self.push_up - self.leg_raise[0]): (0, 0, 0, 255),

            (580 + self.leg_push, 590 + self.leg_push, 390 + self.push_up,400 + self.push_up): self.pants_variable[0], #all
            (590, 600, 390 + self.push_up,400 + self.push_up): self.pants_variable[1],# 1st (black) 2nd 3rd 4th (black) 5th (black)
            (600, 620, 390 + self.push_up,400 + self.push_up): self.pants_variable[0],


            (580 + self.leg_push, 590 + self.leg_push, 400 + self.push_up,410 + self.push_up): self.pants_variable[2], # 1st (black) 2nd 3rd (black) 4th (black) 5th (black)
            (590, 610, 400 + self.push_up,410 + self.push_up): self.pants_variable[3],  # 1st 2nd 3rd (black) 4th 5th
            (610, 620, 400 + self.push_up,410 + self.push_up): self.pants_variable[0],  # all

            (560 + self.leg_push, 570 + self.leg_push, 410 + self.push_up,420 + self.push_up): self.pants_variable[4],  # 5th (black)
            (570 + self.leg_push, 580 + self.leg_push, 410 + self.push_up,420 + self.push_up): self.pants_variable[5],  # all black 5th red
            (580 + self.leg_push, 590 + self.leg_push, 410 + self.push_up,420 + self.push_up): self.pants_variable[6],  # 1st (black) 2nd 4th 5th
            (590, 610, 410 + self.push_up,420 + self.push_up): self.pants_variable[7],  # 1st 2nd 4th 5th
            (610, 620, 410 + self.push_up,420 + self.push_up): self.pants_variable[3],

            (560 + self.leg_push, 570 + self.leg_push, 420 + self.push_up,430 + self.push_up): self.pants_variable[4],
            (570 + self.leg_push, 580 + self.leg_push, 420 + self.push_up,430 + self.push_up): self.pants_variable[5],
            (580 + self.leg_push, 620, 420 + self.push_up,430 + self.push_up): self.pants_variable[7],

            (560 + self.leg_push, 570 + self.leg_push, 430 + self.push_up, 440 + self.push_up - self.leg_raise[0]): self.pants_variable[4],
            (570 + self.leg_push, 580 + self.leg_push, 430 + self.push_up, 440 + self.push_up - self.leg_raise[0]): self.pants_variable[8],
            (580 + self.leg_push, 590, 430 + self.push_up, 440 + self.push_up - self.leg_raise[0]): self.pants_variable[9],
            (590, 620, 430 + self.push_up, 440 + self.push_up - self.leg_raise[0]): self.pants_variable[10],

            (550 + self.leg_push, 570 + self.leg_push, 440 + self.push_up, 450 + self.push_up - self.leg_raise[0]): self.pants_variable[4],
            (570 + self.leg_push, 580 + self.leg_push, 440 + self.push_up, 450 + self.push_up - self.leg_raise[0]): self.pants_variable[11],
            (580 + self.leg_push, 590, 440 + self.push_up, 450 + self.push_up - self.leg_raise[0]): self.pants_variable[12],
            (590, 600, 440 + self.push_up, 450 + self.push_up - self.leg_raise[0]): self.pants_variable[13],
            (600, 610, 440 + self.push_up, 450 + self.push_up - self.leg_raise[0]): self.pants_variable[14],
            (610, 620, 440 + self.push_up, 450 + self.push_up - self.leg_raise[0]): self.pants_variable[13],

            (580 + self.leg_push, 590 + self.leg_push, 450 + self.push_up, 460 + self.push_up - self.leg_raise[0]): self.pants_variable[15],
            (590 + self.leg_push, 600, 450 + self.push_up, 460 + self.push_up - self.leg_raise[0]): self.pants_variable[16],
            (600, 610, 450 + self.push_up, 460 + self.push_up - self.leg_raise[0]): self.pants_variable[19],
            (610, 620, 450 + self.push_up, 460 + self.push_up - self.leg_raise[0]): self.pants_variable[16],
        }
        self.LEG_RIGHT = {

            (670 - self.leg_push, 680 - self.leg_push, 410 + self.push_up, 430 + self.push_up - self.leg_raise[1]): (0, 0, 0, 255),

            (620, 650, 390 + self.push_up, 400 + self.push_up): self.pants_variable[0],  # 23, 24
            (650, 660, 390 + self.push_up, 400 + self.push_up): self.pants_variable[1],  # 23, 24
            (660, 670, 390 + self.push_up, 400 + self.push_up): self.pants_variable[0],  # 23, 24

            (620, 640, 400 + self.push_up, 410 + self.push_up): self.pants_variable[0],  # 23, 24
            (640, 660, 400 + self.push_up, 410 + self.push_up): self.pants_variable[3],  # 23, 24
            (660, 670, 400 + self.push_up, 410 + self.push_up): self.pants_variable[2],  # 23, 24

            (670 - self.leg_push, 680 - self.leg_push, 390 + self.push_up, 410 + self.push_up): (0, 0, 0, 255),

            (620, 630, 410 + self.push_up, 420 + self.push_up): self.pants_variable[17],  # 25
            (620, 630, 420 + self.push_up, 450 + self.push_up): self.pants_variable[18],  # 26, 27, 28, 29, 30

            (630, 640, 410 + self.push_up, 420 + self.push_up): self.pants_variable[3],
            (640, 660, 410 + self.push_up, 420 + self.push_up): self.pants_variable[7],
            (660, 670, 410 + self.push_up, 420 + self.push_up): self.pants_variable[6],
            (670 - self.leg_push, 680 - self.leg_push, 410 + self.push_up, 420 + self.push_up): self.pants_variable[5],
            (680 - self.leg_push, 690 - self.leg_push, 410 + self.push_up, 420 + self.push_up): self.pants_variable[4],

            (630, 670, 420 + self.push_up, 430 + self.push_up): self.pants_variable[7],
            (670 - self.leg_push, 680 - self.leg_push, 420 + self.push_up, 430 + self.push_up): self.pants_variable[5],
            (680 - self.leg_push, 690 - self.leg_push, 420 + self.push_up, 430 + self.push_up): self.pants_variable[4],

            (630, 660, 430 + self.push_up, 440 + self.push_up - self.leg_raise[1]): self.pants_variable[10],
            (660, 670, 430 + self.push_up, 440 + self.push_up - self.leg_raise[1]): self.pants_variable[9],
            (670 - self.leg_push, 680 - self.leg_push, 430 + self.push_up, 440 + self.push_up - self.leg_raise[1]): self.pants_variable[8],
            (680 - self.leg_push, 690 - self.leg_push, 430 + self.push_up, 440 + self.push_up - self.leg_raise[1]): self.pants_variable[4],

            (630, 640, 440 + self.push_up, 450 + self.push_up - self.leg_raise[1]): self.pants_variable[13],
            (640, 650, 440 + self.push_up, 450 + self.push_up - self.leg_raise[1]): self.pants_variable[14],
            (650, 660, 440 + self.push_up, 450 + self.push_up - self.leg_raise[1]): self.pants_variable[13],
            (660, 670, 440 + self.push_up, 450 + self.push_up - self.leg_raise[1]): self.pants_variable[12],
            (670 - self.leg_push, 680 - self.leg_push, 440 + self.push_up, 450 + self.push_up - self.leg_raise[1]): self.pants_variable[11],
            (680 - self.leg_push, 700 - self.leg_push, 440 + self.push_up, 450 + self.push_up - self.leg_raise[1]): self.pants_variable[4],

            (630, 640, 450 + self.push_up, 460 + self.push_up - self.leg_raise[1]): self.pants_variable[16],
            (640, 650, 450 + self.push_up, 460 + self.push_up - self.leg_raise[1]): self.pants_variable[19],
            (650, 660, 450 + self.push_up, 460 + self.push_up - self.leg_raise[1]): self.pants_variable[16],
            (660 - self.leg_push, 670 - self.leg_push, 450 + self.push_up, 460 + self.push_up - self.leg_raise[1]): self.pants_variable[15],


            # (660, 670, 430 + self.push_up, 450 + self.push_up - self.leg_raise[1]): self.leg_variable[0],
            # (670 - self.leg_push, 680 - self.leg_push, 430 + self.push_up, 450 + self.push_up - self.leg_raise[1]): self.leg_variable[1],
        }
        self.SIDE_LEGS = {
            (590, 600, 390 + self.push_up, 450 + self.push_up): (0, 0, 0, 255),
            (650, 660, 390 + self.push_up, 450 + self.push_up): (0, 0, 0, 255),

            (600, 610, 390 + self.push_up, 400 + self.push_up): self.pants_variable[1],
            (610, 640, 390 + self.push_up, 400 + self.push_up): self.pants_variable[0],
            (640, 650, 390 + self.push_up, 400 + self.push_up): self.pants_variable[1],

            (600, 610, 400 + self.push_up, 410 + self.push_up): self.pants_variable[3],
            (610, 620, 400 + self.push_up, 410 + self.push_up): self.pants_variable[2],
            (620, 630, 400 + self.push_up, 410 + self.push_up): self.pants_variable[3],
            (630, 640, 400 + self.push_up, 410 + self.push_up): self.pants_variable[2],
            (640, 650, 400 + self.push_up, 410 + self.push_up): self.pants_variable[3],

            (600, 610, 410 + self.push_up, 420 + self.push_up): self.pants_variable[6],
            (610, 620, 410 + self.push_up, 420 + self.push_up): self.pants_variable[7],
            (620, 630, 410 + self.push_up, 420 + self.push_up): self.pants_variable[7],
            (630, 640, 410 + self.push_up, 420 + self.push_up): self.pants_variable[7],
            (640, 650, 410 + self.push_up, 420 + self.push_up): self.pants_variable[6],

            (580, 590, 420 + self.push_up, 430 + self.push_up): self.pants_variable[4],
            (590, 600, 420 + self.push_up, 430 + self.push_up): self.pants_variable[5],
            (600, 650, 420 + self.push_up, 430 + self.push_up): self.pants_variable[7],
            (650, 660, 420 + self.push_up, 430 + self.push_up): self.pants_variable[5],
            (660, 670, 420 + self.push_up, 430 + self.push_up): self.pants_variable[4],

            (580, 590, 430 + self.push_up, 440 + self.push_up): self.pants_variable[4],
            (590, 600, 430 + self.push_up, 440 + self.push_up): self.pants_variable[5],
            (600, 650, 430 + self.push_up, 440 + self.push_up): self.pants_variable[10],
            (650, 660, 430 + self.push_up, 440 + self.push_up): self.pants_variable[5],
            (660, 670, 430 + self.push_up, 440 + self.push_up): self.pants_variable[4],

            (570, 590, 440 + self.push_up, 450 + self.push_up): self.pants_variable[4],
            (590, 600, 440 + self.push_up, 450 + self.push_up): self.pants_variable[5],
            (600, 610, 440 + self.push_up, 450 + self.push_up): self.pants_variable[13],
            (610, 620, 440 + self.push_up, 450 + self.push_up): self.pants_variable[14],
            (620, 630, 440 + self.push_up, 450 + self.push_up): self.pants_variable[13],
            (630, 640, 440 + self.push_up, 450 + self.push_up): self.pants_variable[14],
            (640, 650, 440 + self.push_up, 450 + self.push_up): self.pants_variable[13],
            (650, 660, 440 + self.push_up, 450 + self.push_up): self.pants_variable[5],
            (660, 680, 440 + self.push_up, 450 + self.push_up): self.pants_variable[4],


            (600, 610, 450 + self.push_up, 460 + self.push_up): self.pants_variable[16],
            (610, 620, 450 + self.push_up, 460 + self.push_up): self.pants_variable[19],
            (620, 630, 450 + self.push_up, 460 + self.push_up): self.pants_variable[16],
            (630, 640, 450 + self.push_up, 460 + self.push_up): self.pants_variable[19],
            (640, 650, 450 + self.push_up, 460 + self.push_up): self.pants_variable[16],


        }
        self.LEFT_LEGF = {
        (590, 600, 370 + self.push_up, 380 + self.push_up): (0, 0, 0, 255),
        (600, 610, 370 + self.push_up, 380 + self.push_up): self.pants_variable[1],

        (580, 590, 380 + self.push_up, 390 + self.push_up): (0, 0, 0, 255),
        (590, 600, 380 + self.push_up, 390 + self.push_up): self.pants_variable[3],
        (600, 610, 380 + self.push_up, 390 + self.push_up): self.pants_variable[2],
        (610, 620, 380 + self.push_up, 390 + self.push_up): self.pants_variable[3],

        (570, 580, 390 + self.push_up, 400 + self.push_up): (0, 0, 0, 255),
        (580, 590, 390 + self.push_up, 400 + self.push_up): self.pants_variable[6],
        (590, 620, 390 + self.push_up, 400 + self.push_up): self.pants_variable[7],
        (620, 640, 390 + self.push_up, 400 + self.push_up): self.pants_variable[3],
        (640, 650, 390 + self.push_up, 400 + self.push_up): self.pants_variable[6],
        (650, 660, 390 + self.push_up, 400 + self.push_up): (0, 0, 0, 255),

        (560, 570, 400 + self.push_up, 410 + self.push_up): (0, 0, 0, 255),
        (570, 580, 400 + self.push_up, 410 + self.push_up): self.pants_variable[7],
        (580, 590, 400 + self.push_up, 410 + self.push_up): self.pants_variable[7],
        (590, 640, 400 + self.push_up, 410 + self.push_up): self.pants_variable[7],
        (640, 650, 400 + self.push_up, 410 + self.push_up): self.pants_variable[5],
        (650, 660, 400 + self.push_up, 410 + self.push_up): self.pants_variable[4],
        (640, 650, 400 + self.push_up, 410 + self.push_up): (0, 0, 0, 255),

        (550, 560, 410 + self.push_up, 420 + self.push_up): (0, 0, 0, 255),
        (560, 570, 410 + self.push_up, 420 + self.push_up): self.pants_variable[10],
        (570, 580, 410 + self.push_up, 420 + self.push_up): self.pants_variable[10],
        (580, 640, 410 + self.push_up, 420 + self.push_up): self.pants_variable[10],
        (640, 650, 410 + self.push_up, 420 + self.push_up): self.pants_variable[5],
        (650, 660, 410 + self.push_up, 420 + self.push_up): self.pants_variable[4],
        (630, 640, 410 + self.push_up, 420 + self.push_up): (0, 0, 0, 255),

        (540, 550, 420 + self.push_up, 430 + self.push_up): (0, 0, 0, 255),
        (550, 560, 420 + self.push_up, 430 + self.push_up): self.pants_variable[13],
        (560, 570, 420 + self.push_up, 430 + self.push_up): self.pants_variable[14],
        (570, 580, 420 + self.push_up, 430 + self.push_up): self.pants_variable[13],
        (580, 590, 420 + self.push_up, 430 + self.push_up): self.pants_variable[14],
        (590, 600, 420 + self.push_up, 430 + self.push_up): self.pants_variable[13],
        (600, 610, 420 + self.push_up, 430 + self.push_up): self.pants_variable[14],
        (610, 620, 420 + self.push_up, 430 + self.push_up): self.pants_variable[13],
        (620, 630, 420 + self.push_up, 430 + self.push_up): self.pants_variable[5],
        (630, 650, 420 + self.push_up, 430 + self.push_up): self.pants_variable[4],
        (620, 630, 420 + self.push_up, 430 + self.push_up): (0, 0, 0, 255),

        (530, 540, 430 + self.push_up, 440 + self.push_up): (0, 0, 0, 255),
        (540, 550, 430 + self.push_up, 440 + self.push_up): self.pants_variable[16],
        (550, 560, 430 + self.push_up, 440 + self.push_up): self.pants_variable[19],
        (560, 570, 430 + self.push_up, 440 + self.push_up): self.pants_variable[16],
        (570, 580, 430 + self.push_up, 440 + self.push_up): self.pants_variable[19],
        (580, 610, 430 + self.push_up, 440 + self.push_up): self.pants_variable[16],
        (610, 620, 430 + self.push_up, 440 + self.push_up): (0, 0, 0, 255),

        (530, 540, 440 + self.push_up, 450 + self.push_up): (0, 0, 0, 255),
        # (540, 600, 440 + self.push_up, 450 + self.push_up): self.back_skin_color,
        (540, 550, 440 + self.push_up, 450 + self.push_up): self.shoes_variable[0],
        (550, 560, 440 + self.push_up, 450 + self.push_up): self.shoes_variable[2],
        (560, 600, 440 + self.push_up, 450 + self.push_up): self.shoes_variable[0],
        (600, 610, 440 + self.push_up, 450 + self.push_up): (0, 0, 0, 255),

        (540, 550, 450 + self.push_up, 460 + self.push_up): (0, 0, 0, 255),
        (550, 560, 450 + self.push_up, 460 + self.push_up): self.shoes_variable[0],
        (560, 570, 450 + self.push_up, 460 + self.push_up): self.shoes_variable[2],
        (570, 590, 450 + self.push_up, 460 + self.push_up): self.shoes_variable[0],
        (590, 600, 450 + self.push_up, 460 + self.push_up): (0, 0, 0, 255),

        (550, 560, 460 + self.push_up, 470 + self.push_up): (0, 0, 0, 255),
        (560, 570, 460 + self.push_up, 470 + self.push_up): self.shoes_variable[2],
        (570, 580, 460 + self.push_up, 470 + self.push_up): self.shoes_variable[0],
        (580, 590, 460 + self.push_up, 470 + self.push_up): (0, 0, 0, 255),

        (560, 580, 470 + self.push_up, 480 + self.push_up): (0, 0, 0, 255)

        }
        self.LEFT_LEGB = {

        (640, 650, 370 + self.push_up, 380 + self.push_up): self.pants_variable[1],
        (650, 660, 370 + self.push_up, 380 + self.push_up): (0, 0, 0, 255),

        (630, 640, 380 + self.push_up, 390 + self.push_up): self.pants_variable[3],
        (640, 650, 380 + self.push_up, 390 + self.push_up): self.pants_variable[2],
        (650, 660, 380 + self.push_up, 390 + self.push_up): self.pants_variable[3],
        (660, 670, 380 + self.push_up, 390 + self.push_up): (0, 0, 0, 255),

        (590, 600, 390 + self.push_up, 400 + self.push_up): (0, 0, 0, 255),
        (600, 610, 390 + self.push_up, 400 + self.push_up): self.pants_variable[6],
        (610, 630, 390 + self.push_up, 400 + self.push_up): self.pants_variable[3],
        (630, 660, 390 + self.push_up, 400 + self.push_up): self.pants_variable[7],
        (660, 670, 390 + self.push_up, 400 + self.push_up): self.pants_variable[6],
        (670, 680, 390 + self.push_up, 400 + self.push_up): (0, 0, 0, 255),

        (600, 610, 400 + self.push_up, 410 + self.push_up): (0, 0, 0, 255),
        (590, 600, 400 + self.push_up, 410 + self.push_up): self.pants_variable[4],
        (600, 610, 400 + self.push_up, 410 + self.push_up): self.pants_variable[5],
        (610, 680, 400 + self.push_up, 410 + self.push_up): self.pants_variable[7],
        (680, 690, 400 + self.push_up, 410 + self.push_up): (0, 0, 0, 255),

        (610, 620, 410 + self.push_up, 420 + self.push_up): (0, 0, 0, 255),
        (590, 600, 410 + self.push_up, 420 + self.push_up): self.pants_variable[4],
        (600, 610, 410 + self.push_up, 420 + self.push_up): self.pants_variable[5],
        (610, 690, 410 + self.push_up, 420 + self.push_up): self.pants_variable[10],
        (690, 700, 410 + self.push_up, 420 + self.push_up): (0, 0, 0, 255),

        (620, 630, 420 + self.push_up, 430 + self.push_up): (0, 0, 0, 255),
        (590, 610, 420 + self.push_up, 430 + self.push_up): self.pants_variable[4],
        (610, 620, 420 + self.push_up, 430 + self.push_up): self.pants_variable[5],
        (620, 660, 420 + self.push_up, 430 + self.push_up): self.pants_variable[13],
        (660, 670, 420 + self.push_up, 430 + self.push_up): self.pants_variable[14],
        (670, 680, 420 + self.push_up, 430 + self.push_up): self.pants_variable[13],
        (680, 690, 420 + self.push_up, 430 + self.push_up): self.pants_variable[14],
        (690, 700, 420 + self.push_up, 430 + self.push_up): self.pants_variable[13],
        (700, 710, 420 + self.push_up, 430 + self.push_up): (0, 0, 0, 255),

        (630, 640, 430 + self.push_up, 440 + self.push_up): (0, 0, 0, 255),
        (640, 650, 430 + self.push_up, 440 + self.push_up): self.pants_variable[16],
        (650, 660, 430 + self.push_up, 440 + self.push_up): self.pants_variable[19],
        (660, 670, 430 + self.push_up, 440 + self.push_up): self.pants_variable[16],
        (670, 680, 430 + self.push_up, 440 + self.push_up): self.pants_variable[19],
        (680, 710, 430 + self.push_up, 440 + self.push_up): self.pants_variable[16],
        (710, 720, 430 + self.push_up, 440 + self.push_up): (0, 0, 0, 255),

        (640, 650, 440 + self.push_up, 450 + self.push_up): (0, 0, 0, 255),
        (650, 660, 440 + self.push_up, 450 + self.push_up): self.shoes_variable[0],
        (660, 670, 440 + self.push_up, 450 + self.push_up): self.shoes_variable[2],
        (670, 710, 440 + self.push_up, 450 + self.push_up): self.shoes_variable[0],
        (710, 720, 440 + self.push_up, 450 + self.push_up): (0, 0, 0, 255),

        (650, 660, 450 + self.push_up, 460 + self.push_up): (0, 0, 0, 255),
        (660, 670, 450 + self.push_up, 460 + self.push_up): self.shoes_variable[0],
        (670, 680, 450 + self.push_up, 460 + self.push_up): self.shoes_variable[2],
        (680, 700, 450 + self.push_up, 460 + self.push_up): self.shoes_variable[0],
        (700, 710, 450 + self.push_up, 460 + self.push_up): (0, 0, 0, 255),

        (660, 670, 460 + self.push_up, 470 + self.push_up): (0, 0, 0, 255),
        (670, 680, 460 + self.push_up, 470 + self.push_up): self.shoes_variable[2],
        (680, 690, 460 + self.push_up, 470 + self.push_up): self.shoes_variable[0],
        (690, 700, 460 + self.push_up, 470 + self.push_up): (0, 0, 0, 255),

        (670, 690, 470 + self.push_up, 480 + self.push_up): (0, 0, 0, 255),
        }
        """from x1 to x2 left to right and then from y1 to y2 up to down im talking about arm left, arm_push is for gender changes ig, pushup is for walking straiht"""
        self.ARM_LEFT = {
            (550 + self.arm_push, 580, 270 + self.push_up, 280 + self.push_up): (0, 0, 0, 255),  # 11 line

            (540 + self.arm_push, 550 + self.arm_push, 280 + self.push_up, 290 + self.push_up): (0, 0, 0, 255),
            # 12 line
            (550 + self.arm_push, 580, 280 + self.push_up, 290 + self.push_up): self.sleeve_variable[0],

            (530 + self.arm_push, 540 + self.arm_push, 290 + self.push_up, 310 + self.push_up): (0, 0, 0, 255),
            # 13, 14 lines
            (540 + self.arm_push, 550, 290 + self.push_up, 300 + self.push_up): self.sleeve_variable[0],
            (550, 560, 290 + self.push_up, 300 + self.push_up): self.sleeve_variable[1],
            (560, 580, 290 + self.push_up, 300 + self.push_up): self.sleeve_variable[0],

            (540 + self.arm_push, 550, 300 + self.push_up, 310 + self.push_up): self.sleeve_variable[1],
            (550, 580, 300 + self.push_up, 310 + self.push_up): self.sleeve_variable[0],
            #
            (540, 550, 310 + self.push_up, 320 + self.push_up): self.sleeve_variable[2],
            (550, 570, 310 + self.push_up, 320 + self.push_up): self.sleeve_variable[0],

            (540, 550, 320 + self.push_up, 330 + self.push_up): self.sleeve_variable[3],
            (550, 570, 320 + self.push_up, 330 + self.push_up): self.sleeve_variable[2],

            (540, 570, 330 + self.push_up, 350 + self.push_up + self.arm_raise[0]): self.sleeve_variable[3],

            (540, 570, 350 + self.push_up + self.arm_raise[0], 360 + self.push_up + self.arm_raise[0]): self.sleeve_variable[4],

            (540, 570, 360 + self.push_up + self.arm_raise[0], 390 + self.push_up + self.arm_raise[0]): self.skin_color,# 15, 16, 17, 18, 19, 20, 21, 22 lines
            (530 + self.arm_push, 540 + self.arm_push, 310 + self.push_up, 390 + self.push_up + self.arm_raise[0]): (0, 0, 0, 255),
            (570, 580, 310 + self.push_up, 390 + self.push_up + self.arm_raise[0]): (0, 0, 0, 255),
            (540 + self.arm_push, 570, 390 + self.push_up + self.arm_raise[0], 400 + self.push_up + self.arm_raise[0]): (0, 0, 0, 255),  # 23 line

            (530 + self.arm_push, 540 + self.arm_push, 340 + self.push_up, 410 + self.push_up): self.sleeve_variable[6],
            (570 + self.arm_push, 580, 340 + self.push_up, 410 + self.push_up): self.sleeve_variable[6],
            (540 + self.arm_push, 570, 340 + self.push_up, 410 + self.push_up): self.sleeve_variable[7],

            (540 + self.arm_push, 570, 410 + self.push_up, 420 + self.push_up): self.sleeve_variable[6]


        }
        self.ARM_RIGHT = {
            (670 - self.arm_push, 700 - self.arm_push, 270 + self.push_up, 280 + self.push_up): (0, 0, 0, 255),
            # 11 line shoulder black line

            (670, 700, 280 + self.push_up, 290 + self.push_up): self.sleeve_variable[0],  # 12 line shoulder dot and skin
            (700 - self.arm_push, 710 - self.arm_push, 280 + self.push_up, 290 + self.push_up): (0, 0, 0, 255),

            (670, 710, 290 + self.push_up, 310 + self.push_up): self.sleeve_variable[0],  # 13, 14 lines shoulder dot and skin
            (710 - self.arm_push, 720 - self.arm_push, 290 + self.push_up, 310 + self.push_up): (0, 0, 0, 255),

            (670, 680, 310 + self.push_up, 390 + self.push_up + self.arm_raise[1]): (0, 0, 0, 255),
            # 15, 16, 17, 18, 19, 20, 21, 22 lines inside of arm black line
            (680, 700, 310 + self.push_up, 320 + self.push_up): self.sleeve_variable[0],
            (700, 710, 310 + self.push_up, 320 + self.push_up): self.sleeve_variable[2],

            (680, 700, 320 + self.push_up, 330 + self.push_up): self.sleeve_variable[2],  # skin color
            (700, 710, 320 + self.push_up, 330 + self.push_up): self.sleeve_variable[3],

            (680, 690, 330 + self.push_up, 340 + self.push_up): self.sleeve_variable[5],  # skin color
            (690, 710, 330 + self.push_up, 340 + self.push_up): self.sleeve_variable[3],  # skin color

            (680, 700, 340 + self.push_up, 350 + self.push_up + self.arm_raise[1]): self.sleeve_variable[3],  # skin color
            (700, 710, 340 + self.push_up, 350 + self.push_up + self.arm_raise[1]): self.sleeve_variable[5],  # skin color

            (680, 710, 350 + self.push_up + self.arm_raise[1], 360 + self.push_up + self.arm_raise[1]): self.sleeve_variable[4],  # skin color
            (680, 710, 360 + self.push_up + self.arm_raise[1], 390 + self.push_up + self.arm_raise[1]): self.skin_color,  # skin color
            (710 - self.arm_push, 720 - self.arm_push, 310 + self.push_up, 390 + self.push_up + self.arm_raise[1]): (0, 0, 0, 255),
            # outside black line of arm

            (680, 710 - self.arm_push, 390 + self.push_up + self.arm_raise[1], 400 + self.push_up + self.arm_raise[1]): (0, 0, 0, 255),

            (710 - self.arm_push, 720 - self.arm_push, 360 + self.push_up, 410 + self.push_up + self.arm_raise[1]): self.sleeve_variable[6],
            (670 + self.arm_push, 710 - self.arm_push, 360 + self.push_up, 410 + self.push_up + self.arm_raise[1]): self.sleeve_variable[7],
            (670 + self.arm_push, 680 - self.arm_push, 360 + self.push_up, 410 + self.push_up + self.arm_raise[1]): self.sleeve_variable[6],


            (680, 710 - self.arm_push, 410 + self.push_up, 420 + self.push_up + self.arm_raise[1]): self.sleeve_variable[6]


            # end of arm black
        }


        self.SIDE_HAND = {

            (600, 650, 290 + self.push_up, 300 + self.push_up): (0, 0, 0, 255),

            (600, 610, 300 + self.push_up, 400 + self.push_up): (0, 0, 0, 255),

            (610, 640, 300 + self.push_up, 320 + self.push_up): self.sleeve_variable[0],

            (610, 620, 320 + self.push_up, 330 + self.push_up): self.sleeve_variable[1], # holes
            (620, 640, 320 + self.push_up, 330 + self.push_up): self.sleeve_variable[0],

            (610, 640, 330 + self.push_up, 340 + self.push_up): self.sleeve_variable[2],

            (610, 640, 340 + self.push_up, 350 + self.push_up): self.sleeve_variable[3],

            (610, 620, 350 + self.push_up, 360 + self.push_up): self.sleeve_variable[3],
            (620, 630, 350 + self.push_up, 360 + self.push_up): self.sleeve_variable[5], # holes
            (630, 640, 350 + self.push_up, 360 + self.push_up): self.sleeve_variable[3],

            (610, 640, 360 + self.push_up, 370 + self.push_up): self.sleeve_variable[4],

            (610, 640, 370 + self.push_up, 400 + self.push_up): self.skin_color,

            (640, 650, 300 + self.push_up, 400 + self.push_up): (0, 0, 0, 255),

            (600, 650, 400 + self.push_up, 410 + self.push_up): (0, 0, 0, 255),

            (610, 640, 360 + self.push_up, 410 + self.push_up): self.sleeve_variable[7],
            (600, 650, 410 + self.push_up, 420 + self.push_up): self.sleeve_variable[6],

        }

        self.SIDE_HAND_WALKF = {

            (620, 630, 280 + self.push_up, 290 + self.push_up): (0, 0, 0, 255),

            (610, 620, 290 + self.push_up, 300 + self.push_up): (0, 0, 0, 255),
            (620, 630, 290 + self.push_up, 300 + self.push_up): self.sleeve_variable[0],
            (630, 640, 290 + self.push_up, 300 + self.push_up): (0, 0, 0, 255),

            (600, 610, 300 + self.push_up, 310 + self.push_up): (0, 0, 0, 255),
            (610, 620, 300 + self.push_up, 310 + self.push_up): self.sleeve_variable[1],
            (620, 640, 300 + self.push_up, 310 + self.push_up): self.sleeve_variable[0],
            (640, 650, 300 + self.push_up, 310 + self.push_up): (0, 0, 0, 255),

            (590, 600, 310 + self.push_up, 320 + self.push_up): (0, 0, 0, 255),
            (600, 650, 310 + self.push_up, 320 + self.push_up): self.sleeve_variable[2],
            (650, 660, 310 + self.push_up, 320 + self.push_up): (0, 0, 0, 255),

            (580, 590, 320 + self.push_up, 330 + self.push_up): (0, 0, 0, 255),
            (590, 640, 320 + self.push_up, 330 + self.push_up): self.sleeve_variable[3],
            (640, 650, 320 + self.push_up, 330 + self.push_up): (0, 0, 0, 255),

            (570, 580, 330 + self.push_up, 340 + self.push_up): (0, 0, 0, 255),
            (580, 590, 330 + self.push_up, 340 + self.push_up): self.sleeve_variable[3],
            (590, 610, 330 + self.push_up, 340 + self.push_up): self.sleeve_variable[5],
            (610, 630, 330 + self.push_up, 340 + self.push_up): self.sleeve_variable[3],
            (630, 640, 330 + self.push_up, 340 + self.push_up): (0, 0, 0, 255),

            (560, 570, 340 + self.push_up, 350 + self.push_up): (0, 0, 0, 255),
            (570, 620, 340 + self.push_up, 350 + self.push_up): self.sleeve_variable[4],
            (620, 630, 340 + self.push_up, 350 + self.push_up): (0, 0, 0, 255),

            (550, 560, 350 + self.push_up, 360 + self.push_up): (0, 0, 0, 255),
            (560, 610, 350 + self.push_up, 360 + self.push_up): self.front_skin_color,
            (610, 620, 350 + self.push_up, 360 + self.push_up): (0, 0, 0, 255),

            (540, 550, 360 + self.push_up, 370 + self.push_up): (0, 0, 0, 255),
            (550, 600, 360 + self.push_up, 370 + self.push_up): self.front_skin_color,
            (600, 610, 360 + self.push_up, 370 + self.push_up): (0, 0, 0, 255),

            (550, 560, 370 + self.push_up, 380 + self.push_up): (0, 0, 0, 255),
            (560, 590, 370 + self.push_up, 380 + self.push_up): self.front_skin_color,
            (590, 600, 370 + self.push_up, 380 + self.push_up): (0, 0, 0, 255),

            (560, 570, 380 + self.push_up, 390 + self.push_up): (0, 0, 0, 255),
            (570, 580, 380 + self.push_up, 390 + self.push_up): self.front_skin_color,
            (580, 590, 380 + self.push_up, 390 + self.push_up): (0, 0, 0, 255),

            (570, 580, 390 + self.push_up, 400 + self.push_up): (0, 0, 0, 255), # idk hand

            (560, 610, 350 + self.push_up, 360 + self.push_up): self.sleeve_variable[8], # front hand

            (550, 600, 360 + self.push_up, 370 + self.push_up): self.sleeve_variable[8], # front hand

            (540, 550, 370 + self.push_up, 380 + self.push_up): self.sleeve_variable[6], # front hand
            (550, 560, 370 + self.push_up, 380 + self.push_up): self.sleeve_variable[9], # front hand
            (560, 590, 370 + self.push_up, 380 + self.push_up): self.sleeve_variable[8], # front hand

            (540, 550, 380 + self.push_up, 390 + self.push_up): self.sleeve_variable[6], # front hand
            (550, 560, 380 + self.push_up, 390 + self.push_up): self.sleeve_variable[7], # front hand
            (560, 570, 380 + self.push_up, 390 + self.push_up): self.sleeve_variable[9], # front hand
            (570, 580, 380 + self.push_up, 390 + self.push_up): self.sleeve_variable[8], # front hand

            (550, 570, 390 + self.push_up, 400 + self.push_up): self.sleeve_variable[6], # front hand
            (570, 580, 390 + self.push_up, 400 + self.push_up): self.sleeve_variable[10], # front hand


            (670, 690, 350 + self.push_up, 360 + self.push_up): self.sleeve_variable[11],# back hand 4: shirt color others: skin2 color

            (660, 700, 360 + self.push_up, 370 + self.push_up): self.sleeve_variable[11],# back hand 4: shirt color others: skin2 color

            (660, 690, 370 + self.push_up, 380 + self.push_up): self.sleeve_variable[11], # back hand 4: shirt color others: skin2 color
            (690, 700, 370 + self.push_up, 380 + self.push_up): self.sleeve_variable[9], # back hand 4: shirt color others: black
            (700, 710, 370 + self.push_up, 380 + self.push_up): self.sleeve_variable[6], # back hand 4: black others: seethrough

            (670, 680, 380 + self.push_up, 390 + self.push_up): self.sleeve_variable[11], # back hand 4: shirt color others: skin2 color
            (680, 690, 380 + self.push_up, 390 + self.push_up): self.sleeve_variable[9], # back hand 4: shirt color others: black
            (690, 700, 380 + self.push_up, 390 + self.push_up): self.sleeve_variable[7], # back hand 4: shirt color others: seethrough
            (700, 710, 380 + self.push_up, 390 + self.push_up): self.sleeve_variable[6], # back hand 4: black others: seethrough

            (680, 710, 390 + self.push_up, 400 + self.push_up): self.sleeve_variable[6], # back hand




        }
        self.SIDE_HAND_WALKB = {
        # -45 degree
        (620, 630, 280 + self.push_up, 290 + self.push_up): (0, 0, 0, 255),

        (610, 620, 290 + self.push_up, 300 + self.push_up): (0, 0, 0, 255),
        (620, 630, 290 + self.push_up, 300 + self.push_up): self.sleeve_variable[0],
        (630, 640, 290 + self.push_up, 300 + self.push_up): (0, 0, 0, 255),

        (600, 610, 300 + self.push_up, 310 + self.push_up): (0, 0, 0, 255),
        (610, 620, 300 + self.push_up, 310 + self.push_up): self.sleeve_variable[1],
        (620, 640, 300 + self.push_up, 310 + self.push_up): self.sleeve_variable[0],
        (640, 650, 300 + self.push_up, 310 + self.push_up): (0, 0, 0, 255),

        (590, 600, 310 + self.push_up, 320 + self.push_up): (0, 0, 0, 255),
        (600, 650, 310 + self.push_up, 320 + self.push_up): self.sleeve_variable[2],
        (650, 660, 310 + self.push_up, 320 + self.push_up): (0, 0, 0, 255),

        (600, 610, 320 + self.push_up, 330 + self.push_up): (0, 0, 0, 255),
        (610, 660, 320 + self.push_up, 330 + self.push_up): self.sleeve_variable[3],
        (660, 670, 320 + self.push_up, 330 + self.push_up): (0, 0, 0, 255),

        (610, 620, 330 + self.push_up, 340 + self.push_up): (0, 0, 0, 255),
        (620, 630, 330 + self.push_up, 340 + self.push_up): self.sleeve_variable[3],
        (630, 650, 330 + self.push_up, 340 + self.push_up): self.sleeve_variable[5],
        (650, 670, 330 + self.push_up, 340 + self.push_up): self.sleeve_variable[3],
        (670, 680, 330 + self.push_up, 340 + self.push_up): (0, 0, 0, 255),

        (620, 630, 340 + self.push_up, 350 + self.push_up): (0, 0, 0, 255),
        (630, 680, 340 + self.push_up, 350 + self.push_up): self.sleeve_variable[4],
        (680, 690, 340 + self.push_up, 350 + self.push_up): (0, 0, 0, 255),

        (630, 640, 350 + self.push_up, 360 + self.push_up): (0, 0, 0, 255),
        (640, 690, 350 + self.push_up, 360 + self.push_up): self.back_skin_color,
        (690, 700, 350 + self.push_up, 360 + self.push_up): (0, 0, 0, 255),

        (640, 650, 360 + self.push_up, 370 + self.push_up): (0, 0, 0, 255),
        (650, 700, 360 + self.push_up, 370 + self.push_up): self.back_skin_color,
        (700, 710, 360 + self.push_up, 370 + self.push_up): (0, 0, 0, 255),

        (650, 660, 370 + self.push_up, 380 + self.push_up): (0, 0, 0, 255),
        (660, 690, 370 + self.push_up, 380 + self.push_up): self.back_skin_color,
        (690, 700, 370 + self.push_up, 380 + self.push_up): (0, 0, 0, 255),

        (660, 670, 380 + self.push_up, 390 + self.push_up): (0, 0, 0, 255),
        (670, 680, 380 + self.push_up, 390 + self.push_up): self.back_skin_color,
        (680, 690, 380 + self.push_up, 390 + self.push_up): (0, 0, 0, 255),

        (670, 680, 390 + self.push_up, 400 + self.push_up): (0, 0, 0, 255),

        (640, 690, 350 + self.push_up, 360 + self.push_up): self.sleeve_variable[11],

        (650, 700, 360 + self.push_up, 370 + self.push_up): self.sleeve_variable[11],

        (660, 690, 370 + self.push_up, 380 + self.push_up): self.sleeve_variable[11],
        (690, 700, 370 + self.push_up, 380 + self.push_up): self.sleeve_variable[9],

        (670, 680, 380 + self.push_up, 390 + self.push_up): self.sleeve_variable[11],
        (680, 690, 380 + self.push_up, 390 + self.push_up): self.sleeve_variable[9],


        }

        if I.TD.Appearance != {}:
            if self.orientation == "Front":
                self.hair_variable[26] = (0, 0, 0, 0)
                self.make_longer_left = 0
                self.make_longer_right = 0
            elif self.orientation == "Back" and "Hair" in I.TD.Appearance.keys():
                if I.TD.Appearance["Hair"] != 0:
                    self.make_longer_left = 0
                    self.make_longer_right = 0
                    self.hair_variable[26] = self.hair_color
            elif self.orientation == "Right":
                self.make_longer_right = 30
                self.make_longer_left = 0
            elif self.orientation == "Left":
                self.make_longer_right = 0
                self.make_longer_left = 30
        self.push_up -= 10
        self.HAIR = {

            (580, 670, 190 + self.push_up, 270 + self.push_up): self.hair_variable[26],
            (610, 640, 270 + self.push_up, 280 + self.push_up): self.hair_variable[26],

            (560, 570 + self.make_longer_right, 140 + self.push_up, 150 + self.push_up): self.hair_variable[0], # only 5th
            (660, 670, 140 + self.push_up, 150 + self.push_up): self.hair_variable[0],

            (570, 590 + self.make_longer_right, 150 + self.push_up, 160 + self.push_up): self.hair_variable[0],
            (610, 630, 150 + self.push_up, 160 + self.push_up): self.hair_variable[0],
            (650, 660, 150 + self.push_up, 160 + self.push_up): self.hair_variable[0],
            (680 - self.make_longer_left, 690, 150 + self.push_up, 160 + self.push_up): self.hair_variable[0],

            (560, 570 + self.make_longer_right, 160 + self.push_up, 170 + self.push_up): self.hair_variable[0],
            (570, 580 + self.make_longer_right, 160 + self.push_up, 170 + self.push_up): self.hair_variable[1], # 4th 5th 6th
            (580, 600 + self.make_longer_right, 160 + self.push_up, 170 + self.push_up): self.hair_variable[4], # 1st 4th 5th 6th
            (600, 650, 160 + self.push_up, 170 + self.push_up): self.hair_variable[2], # 1st 5th 6th
            (650, 660, 160 + self.push_up, 170 + self.push_up): self.hair_variable[4], # 1st 4th 5th 6th
            (660, 670, 160 + self.push_up, 170 + self.push_up): self.hair_variable[5], # 1st 4th 5th
            (670 - self.make_longer_left, 680, 160 + self.push_up, 170 + self.push_up): self.hair_variable[3], # 4th 5th

            (550, 560 + self.make_longer_right, 170 + self.push_up, 180 + self.push_up): self.hair_variable[0],
            (560, 570 + self.make_longer_right, 170 + self.push_up, 180 + self.push_up): self.hair_variable[1],
            (570, 590 + self.make_longer_right, 170 + self.push_up, 180 + self.push_up): self.hair_variable[4],
            (590, 600 + self.make_longer_right, 170 + self.push_up, 180 + self.push_up): self.hair_variable[6], # 1st 3rd 4th 5th 6th
            (600, 630 + self.make_longer_right, 170 + self.push_up, 180 + self.push_up): self.hair_variable[7],  # all
            (620 - self.make_longer_left, 660, 170 + self.push_up, 180 + self.push_up): self.hair_variable[7],  # all
            (660, 680, 170 + self.push_up, 180 + self.push_up): self.hair_variable[4],
            (680 - self.make_longer_left, 690, 170 + self.push_up, 180 + self.push_up): self.hair_variable[3],
            (690 - self.make_longer_left, 700, 170 + self.push_up, 180 + self.push_up): self.hair_variable[0],

            (540, 550 + self.make_longer_right, 180 + self.push_up, 190 + self.push_up): self.hair_variable[0],
            (550, 560 + self.make_longer_right, 180 + self.push_up, 190 + self.push_up): self.hair_variable[8],  # 5th 6th
            (560, 580 + self.make_longer_right, 180 + self.push_up, 190 + self.push_up): self.hair_variable[4],
            (580, 640 + self.make_longer_right , 180 + self.push_up, 190 + self.push_up): self.hair_variable[7],
            (620 - self.make_longer_left, 670, 180 + self.push_up, 190 + self.push_up): self.hair_variable[7],
            (670 - self.make_longer_left, 680, 180 + self.push_up, 190 + self.push_up): self.hair_variable[4],
            (680 - self.make_longer_left, 690, 180 + self.push_up, 190 + self.push_up): self.hair_variable[5],
            (690 - self.make_longer_left, 710, 180 + self.push_up, 190 + self.push_up): self.hair_variable[0],

            (550, 560 + self.make_longer_right, 190 + self.push_up, 200 + self.push_up): self.hair_variable[8],
            (550, 560 + self.make_longer_right, 190 + self.push_up, 200 + self.push_up): self.hair_variable[8],
            (560, 570 + self.make_longer_right, 190 + self.push_up, 200 + self.push_up): self.hair_variable[9],  # 4th changes to black
            (570, 590 + self.make_longer_right, 190 + self.push_up, 200 + self.push_up): self.hair_variable[7],
            (590, 600 + self.make_longer_right, 190 + self.push_up, 200 + self.push_up): self.hair_variable[10],  # 2nd 3rd 4th 5th 6th
            (600, 610, 190 + self.push_up, 200 + self.push_up): self.hair_variable[11], # 2nd 4th (black) 6th
            (610, 640, 190 + self.push_up, 200 + self.push_up): self.hair_variable[12],  # 2nd
            (640, 650, 190 + self.push_up, 200 + self.push_up): self.hair_variable[13],# 2nd 4th (black)
            (650, 660, 190 + self.push_up, 200 + self.push_up): self.hair_variable[10],
            (660 - self.make_longer_left, 680, 190 + self.push_up, 200 + self.push_up): self.hair_variable[7],
            (680 - self.make_longer_left, 690, 190 + self.push_up, 200 + self.push_up): self.hair_variable[14],# 1st 4th (black) 5th
            (690 - self.make_longer_left, 700, 190 + self.push_up, 200 + self.push_up): self.hair_variable[0],

            (550, 560 + self.make_longer_right, 200 + self.push_up, 210 + self.push_up): self.hair_variable[15],  # 6th
            (560, 570 + self.make_longer_right, 200 + self.push_up, 210 + self.push_up): self.hair_variable[4],  # 1st 4th 5th 6th
            (570, 580 + self.make_longer_right, 200 + self.push_up, 210 + self.push_up): self.hair_variable[16],  # all but 4th (black)
            (580, 590 + self.make_longer_right, 200 + self.push_up, 210 + self.push_up): self.hair_variable[11],  # 2nd 4th (black) 6th
            (590, 600 + self.make_longer_right, 200 + self.push_up, 210 + self.push_up): self.hair_variable[13],  # 2nd 4th (black)
            (610, 650, 200 + self.push_up, 210 + self.push_up): self.hair_variable[12],  # 2nd
            (650, 670, 200 + self.push_up, 210 + self.push_up): self.hair_variable[13],  # 2nd 4th (black)
            (670 - self.make_longer_left, 680, 200 + self.push_up, 210 + self.push_up): self.hair_variable[16],  # all but 4th (black)
            (680 - self.make_longer_left, 690, 200 + self.push_up, 210 + self.push_up): self.hair_variable[5],  # 1st 4th 5th

            (550, 560 + self.make_longer_right, 210 + self.push_up, 220 + self.push_up): self.hair_variable[15],
            (560, 570 + self.make_longer_right, 210 + self.push_up, 220 + self.push_up): self.hair_variable[6],
            (570, 580 + self.make_longer_right, 210 + self.push_up, 220 + self.push_up): self.hair_variable[7],
            (580, 590 + self.make_longer_right, 210 + self.push_up, 220 + self.push_up): self.hair_variable[15],
            (670 - self.make_longer_left, 680, 210 + self.push_up, 220 + self.push_up): self.hair_variable[7],
            (680 - self.make_longer_left, 690, 210 + self.push_up, 220 + self.push_up): self.hair_variable[5],
            #
            (550, 560 + self.make_longer_right, 220 + self.push_up, 230 + self.push_up): self.hair_variable[15],  # 6th
            (560, 570 + self.make_longer_right, 220 + self.push_up, 230 + self.push_up): self.hair_variable[6],
            (570, 580 + self.make_longer_right, 220 + self.push_up, 230 + self.push_up): self.hair_variable[7],  # all
            (670 - self.make_longer_left, 680, 220 + self.push_up, 230 + self.push_up): self.hair_variable[7],
            (680 - self.make_longer_left, 690, 220 + self.push_up, 230 + self.push_up): self.hair_variable[17],  # 1st 3rd 4th 5th
            #
            (550, 560 + self.make_longer_right, 230 + self.push_up, 240 + self.push_up): self.hair_variable[15],
            (560, 570 + self.make_longer_right, 230 + self.push_up, 240 + self.push_up): self.hair_variable[18],  # 1st 3rd 4th 6th
            (570, 580 + self.make_longer_right, 230 + self.push_up, 240 + self.push_up): self.hair_variable[7],
            (670 - self.make_longer_left, 680, 230 + self.push_up, 240 + self.push_up): self.hair_variable[7],
            (680 - self.make_longer_left, 690, 230 + self.push_up, 240 + self.push_up): self.hair_variable[23],  # 1st 3rd 4th

            (550, 560 + self.make_longer_right, 240 + self.push_up, 250 + self.push_up): self.hair_variable[15],
            (560, 570 + self.make_longer_right, 240 + self.push_up, 250 + self.push_up): self.hair_variable[19],  # 1st 2nd 3rd 4th 6th
            (570, 580 + self.make_longer_right, 240 + self.push_up, 250 + self.push_up): self.hair_variable[7],
            (670 - self.make_longer_left, 680, 240 + self.push_up, 250 + self.push_up): self.hair_variable[7],
            (680 - self.make_longer_left, 690, 240 + self.push_up, 250 + self.push_up): self.hair_variable[20],  # 1st 2nd 3rd 4th

            (550, 560 + self.make_longer_right, 250 + self.push_up, 260 + self.push_up): self.hair_variable[21],  # 2nd 6th
            (560, 570 + self.make_longer_right, 250 + self.push_up, 260 + self.push_up): self.hair_variable[19],
            (570, 580 + self.make_longer_right, 250 + self.push_up, 260 + self.push_up): self.hair_variable[7],
            (580, 590 + self.make_longer_right, 250 + self.push_up, 260 + self.push_up): self.hair_variable[22],  # 3rd 4th
            (660 - self.make_longer_left, 670, 250 + self.push_up, 260 + self.push_up): self.hair_variable[22],
            (670 - self.make_longer_left, 680, 250 + self.push_up, 260 + self.push_up): self.hair_variable[7],
            (680 - self.make_longer_left, 690, 250 + self.push_up, 260 + self.push_up): self.hair_variable[20],
            (690 - self.make_longer_left, 700, 250 + self.push_up, 260 + self.push_up): self.hair_variable[12],

            (550, 560 + self.make_longer_right, 260 + self.push_up, 270 + self.push_up): self.hair_variable[15],
            (560, 570 + self.make_longer_right, 260 + self.push_up, 270 + self.push_up): self.hair_variable[19],
            (570, 580 + self.make_longer_right, 260 + self.push_up, 270 + self.push_up): self.hair_variable[18],
            (580, 590 + self.make_longer_right, 260 + self.push_up, 270 + self.push_up): self.hair_variable[6],
            (660 - self.make_longer_left, 670, 260 + self.push_up, 270 + self.push_up): self.hair_variable[6],
            (670 - self.make_longer_left, 680, 260 + self.push_up, 270 + self.push_up): self.hair_variable[23],  # 1st 3rd 4th
            (680 - self.make_longer_left, 690, 260 + self.push_up, 270 + self.push_up): self.hair_variable[20],

            (550, 560 + self.make_longer_right, 270 + self.push_up, 280 + self.push_up): self.hair_variable[15],
            (560, 570 + self.make_longer_right, 270 + self.push_up, 280 + self.push_up): self.hair_variable[24],  # 3rd 4th 6th
            (570, 590 + self.make_longer_right, 270 + self.push_up, 280 + self.push_up): self.hair_variable[18],  # 1st 3rd 4th 6th
            (590, 600 + self.make_longer_right, 270 + self.push_up, 280 + self.push_up): self.hair_variable[25],  # 1st
            (650 - self.make_longer_left, 660, 270 + self.push_up, 280 + self.push_up): self.hair_variable[25],
            (660 - self.make_longer_left, 680, 270 + self.push_up, 280 + self.push_up): self.hair_variable[23],
            (680 - self.make_longer_left, 690, 270 + self.push_up, 280 + self.push_up): self.hair_variable[22],

            (560, 580 + self.make_longer_right, 280 + self.push_up, 290 + self.push_up): self.hair_variable[24],
            (580, 590 + self.make_longer_right, 280 + self.push_up, 290 + self.push_up): self.hair_variable[22],
            (660 - self.make_longer_left, 690, 280 + self.push_up, 290 + self.push_up): self.hair_variable[22],

            (560, 580 + self.make_longer_right, 290 + self.push_up, 300 + self.push_up): self.hair_variable[24],
            (580, 590 + self.make_longer_right, 290 + self.push_up, 300 + self.push_up): self.hair_variable[22],
            (660 - self.make_longer_left, 690, 290 + self.push_up, 300 + self.push_up): self.hair_variable[22],

            (560, 570 + self.make_longer_right, 300 + self.push_up, 310 + self.push_up): self.hair_variable[24],
            (570, 590 + self.make_longer_right, 300 + self.push_up, 310 + self.push_up): self.hair_variable[22],
            (660 - self.make_longer_left, 690, 300 + self.push_up, 310 + self.push_up): self.hair_variable[22],
        }
        self.push_up += 10

    def get_character_options(self, option):
        if option != []:
            if option == "Eyes":
                return [self.EYES]
            elif option == "Skin" or option == "Skin2":
                if self.race == "Human" and self.gender == "Boy":
                    return [self.HEAD, self.EYES, self.SMILE_HAPPY, self.ARM_RIGHT, self.ARM_LEFT, self.FOOT_RIGHT,
                            self.FOOT_LEFT, self.LEG_LEFT, self.LEG_RIGHT, self.CHEST]
                elif self.race == "Human" and self.gender == "Girl":
                    return [self.HEAD, self.EYES, self.SMILE_HAPPY, self.CHEST,self.ARM_LEFT, self.ARM_RIGHT,
                            self.LEG_LEFT, self.LEG_RIGHT,self.FOOT_LEFT, self.FOOT_RIGHT]
                elif self.race == "Elf" and self.gender == "Boy":
                    return [self.HEAD, self.ELF_EAR_TIPS,  self.CHEST, self.EYES, self.SMILE_HAPPY, self.ARM_LEFT,
                            self.ARM_RIGHT, self.LEG_LEFT, self.LEG_RIGHT, self.FOOT_LEFT,self.FOOT_RIGHT]
                elif self.race == "Elf" and self.gender == "Girl":
                    return [self.HEAD, self.ELF_EAR_TIPS, self.CHEST,self.EYES, self.SMILE_HAPPY,self.ARM_LEFT,
                            self.ARM_RIGHT, self.LEG_LEFT, self.LEG_RIGHT,self.FOOT_LEFT, self.FOOT_RIGHT]
        else:
            # clothing_dict = {
            #     "Human": {
            #         "Boy": {
            #             "Front": [
            #                 self.HEAD, self.CHEST, self.EYES, self.SMILE_HAPPY, self.ARM_LEFT,
            #                 self.ARM_RIGHT, self.FOOT_LEFT,self.FOOT_RIGHT, self.LEG_LEFT, self.LEG_RIGHT, self.HAIR
            #             ],
            #             "Back": [
            #                 self.HEAD, self.CHEST, self.ARM_LEFT,self.ARM_RIGHT, self.FOOT_LEFT,self.FOOT_RIGHT,
            #                 self.LEG_LEFT, self.LEG_RIGHT,self.HAIR
            #             ],
            #             "Left": {
            #                 1: [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.SIDE_CHEST, self.LEFT_LEGB, self.SIDE_HAND_WALKF, self.HAIR],
            #                 2: [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.SIDE_CHEST, self.LEFT_LEGF, self.SIDE_HAND_WALKB, self.HAIR],
            #                 0: [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_CHEST, self.SIDE_LEGS, self.LEFT_SHOE, self.SIDE_HAND, self.HAIR]
            #             },
            #             "Right": {
            #                 1: [self.HEAD, self.RIGHT_EYE, self.RIGHT_SMILE, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.SIDE_CHEST, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR],
            #                 2: [self.HEAD, self.RIGHT_EYE, self.RIGHT_SMILE, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.SIDE_CHEST, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR],
            #                 0: [self.HEAD, self.RIGHT_EYE, self.RIGHT_SMILE, self.SIDE_CHEST, self.SIDE_LEGS, self.RIGHT_SHOE, self.SIDE_HAND, self.HAIR]
            #             }
            #         },
            #         "Girl": {
            #             "Front": [
            #                 self.HEAD, self.CHEST,self.EYES, self.SMILE_HAPPY, self.ARM_LEFT, self.ARM_RIGHT,
            #                 self.FOOT_LEFT, self.FOOT_RIGHT, self.LEG_LEFT, self.LEG_RIGHT, self.HAIR
            #             ],
            #             "Back": [
            #                 self.HEAD, self.CHEST,self.ARM_LEFT,self.ARM_RIGHT, self.FOOT_LEFT, self.FOOT_RIGHT,
            #                 self.LEG_LEFT, self.LEG_RIGHT, self.HAIR
            #             ],
            #             "Left": {
            #                 1: [self.HEAD, self.LEFT_EYE, self.LEFT_SMILE, self.SIDE_HAND_WALKB, self.LEFT_LEGF,
            #                         self.SIDE_CHEST, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR],
            #                 2: [self.HEAD, self.LEFT_EYE, self.LEFT_SMILE, self.SIDE_HAND_WALKF, self.LEFT_LEGB,
            #                         self.SIDE_CHEST, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR],
            #                 0: [ self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_CHEST, self.SIDE_LEGS, self.LEFT_SHOE, self.SIDE_HAND, self.HAIR]
            #             },
            #             "Right": {
            #                 1: [self.HEAD, self.RIGHT_EYE, self.RIGHT_SMILE, self.SIDE_HAND_WALKB, self.LEFT_LEGF,
            #                         self.SIDE_CHEST, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR],
            #                 2: [self.HEAD, self.RIGHT_EYE, self.RIGHT_SMILE, self.SIDE_HAND_WALKF, self.LEFT_LEGB,
            #                         self.SIDE_CHEST, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR],
            #                 0: [self.HEAD, self.RIGHT_EYE, self.RIGHT_SMILE, self.SIDE_CHEST, self.SIDE_LEGS, self.RIGHT_SHOE, self.SIDE_HAND, self.HAIR]
            #             }
            #         }
            #     },
            #     "Elf": {
            #         "Boy": {
            #             "Front": [
            #                 self.HEAD,  self.CHEST, self.EYES, self.SMILE_HAPPY, self.ARM_LEFT,
            #                 self.ARM_RIGHT, self.FOOT_LEFT,self.FOOT_RIGHT, self.LEG_LEFT, self.LEG_RIGHT, self.HAIR, self.ELF_EAR_TIPS
            #             ],
            #             "Back": [
            #                 self.HEAD,  self.CHEST, self.ARM_LEFT,
            #                 self.ARM_RIGHT, self.FOOT_LEFT,self.FOOT_RIGHT, self.LEG_LEFT, self.LEG_RIGHT, self.HAIR, self.ELF_EAR_TIPS
            #             ],
            #             "Left": {
            #                 1: [self.HEAD, self.LEFT_SMILE,self.LEFT_EYE, self.SIDE_HAND_WALKB, self.LEFT_LEGF,
            #                         self.SIDE_CHEST, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR, self.LEFT_ELF_EAR_TIPS],
            #                 2: [self.HEAD, self.LEFT_SMILE,self.LEFT_EYE, self.SIDE_HAND_WALKF, self.LEFT_LEGB,
            #                         self.SIDE_CHEST, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR, self.LEFT_ELF_EAR_TIPS],
            #                 0: [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_CHEST, self.SIDE_LEGS,
            #                         self.LEFT_SHOE, self.SIDE_HAND, self.HAIR, self.LEFT_ELF_EAR_TIPS]
            #             },
            #             "Right": {
            #                 1: [self.HEAD, self.RIGHT_EYE,
            #                         self.RIGHT_SMILE, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.SIDE_CHEST,
            #                         self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR, self.RIGHT_ELF_EAR_TIPS],
            #                 2: [self.HEAD, self.RIGHT_EYE,
            #                         self.RIGHT_SMILE, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.SIDE_CHEST,
            #                         self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR, self.RIGHT_ELF_EAR_TIPS],
            #                 0: [self.HEAD, self.RIGHT_EYE,
            #                         self.RIGHT_SMILE, self.SIDE_CHEST, self.SIDE_LEGS, self.RIGHT_SHOE, self.SIDE_HAND, self.HAIR, self.RIGHT_ELF_EAR_TIPS]
            #             }
            #         },
            #         "Girl": {
            #             "Front": [
            #                 self.HEAD, self.CHEST,self.EYES, self.SMILE_HAPPY,self.ARM_LEFT,
            #                 self.ARM_RIGHT, self.FOOT_LEFT, self.FOOT_RIGHT, self.LEG_LEFT, self.LEG_RIGHT, self.HAIR, self.ELF_EAR_TIPS
            #             ],
            #             "Back": [
            #                 self.HEAD, self.CHEST,self.ARM_LEFT, self.ARM_RIGHT,
            #                 self.FOOT_LEFT, self.FOOT_RIGHT, self.LEG_LEFT,self.LEG_RIGHT, self.HAIR, self.ELF_EAR_TIPS
            #             ],
            #             "Left": {
            #                 1: [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_HAND_WALKB, self.LEFT_LEGF,
            #                         self.SIDE_CHEST, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR, self.LEFT_ELF_EAR_TIPS],
            #                 2: [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_HAND_WALKF, self.LEFT_LEGB,
            #                         self.SIDE_CHEST, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR, self.LEFT_ELF_EAR_TIPS],
            #                 0: [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_CHEST, self.SIDE_LEGS,
            #                         self.LEFT_SHOE, self.SIDE_HAND, self.HAIR, self.LEFT_ELF_EAR_TIPS]
            #             },
            #             "Right": {
            #                 1: [self.HEAD, self.RIGHT_SMILE, self.RIGHT_EYE, self.SIDE_HAND_WALKB, self.LEFT_LEGF,
            #                         self.SIDE_CHEST, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR, self.RIGHT_ELF_EAR_TIPS],
            #                 2: [self.HEAD, self.RIGHT_SMILE, self.RIGHT_EYE, self.SIDE_HAND_WALKF, self.LEFT_LEGB,
            #                         self.SIDE_CHEST, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR, self.RIGHT_ELF_EAR_TIPS],
            #                 0: [self.HEAD, self.RIGHT_SMILE, self.RIGHT_EYE, self.SIDE_CHEST, self.SIDE_LEGS,
            #                         self.RIGHT_SHOE, self.SIDE_HAND, self.HAIR, self.RIGHT_ELF_EAR_TIPS]
            #             }
            #         }
            #     }
            # }
            # if self.orientation in ["Left", "Right"]:
            #     print(clothing_dict[self.race][self.gender][self.orientation][self.walking])
            # else:
            #     print(clothing_dict[self.race][self.gender][self.orientation])
        # print("eye color: ", self.eye_color)
            if self.race == "Human":
                if self.gender == "Boy":
                    if self.orientation == "Front":
                        return [
                            self.HEAD, self.CHEST, self.EYES, self.SMILE_HAPPY, self.ARM_LEFT,
                            self.ARM_RIGHT, self.FOOT_LEFT,self.FOOT_RIGHT, self.LEG_LEFT, self.LEG_RIGHT, self.HAIR
                        ]
                    elif self.orientation == "Back":
                        return [
                            self.HEAD, self.CHEST, self.ARM_LEFT,self.ARM_RIGHT, self.FOOT_LEFT,self.FOOT_RIGHT,
                            self.LEG_LEFT, self.LEG_RIGHT,self.HAIR
                        ]
                    elif self.orientation == "Left":
                        if self.walking == 1:
                            return [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.SIDE_CHEST, self.LEFT_LEGB, self.SIDE_HAND_WALKF, self.HAIR]
                        elif self.walking == 2:
                            return [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.SIDE_CHEST, self.LEFT_LEGF, self.SIDE_HAND_WALKB, self.HAIR]
                        else:
                            return [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_CHEST, self.SIDE_LEGS, self.LEFT_SHOE, self.SIDE_HAND, self.HAIR]
                    elif self.orientation == "Right":
                        if self.walking == 1:
                            return [self.HEAD, self.RIGHT_EYE, self.RIGHT_SMILE, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.SIDE_CHEST, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR]
                        elif self.walking == 2:
                            return [self.HEAD, self.RIGHT_EYE, self.RIGHT_SMILE, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.SIDE_CHEST, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR]
                        else:
                            return [self.HEAD, self.RIGHT_EYE, self.RIGHT_SMILE, self.SIDE_CHEST, self.SIDE_LEGS, self.RIGHT_SHOE, self.SIDE_HAND, self.HAIR]
                elif self.gender == "Girl":
                    if self.orientation == "Front":
                        return [
                            self.HEAD, self.CHEST,self.EYES, self.SMILE_HAPPY, self.ARM_LEFT, self.ARM_RIGHT,
                            self.FOOT_LEFT, self.FOOT_RIGHT, self.LEG_LEFT, self.LEG_RIGHT, self.HAIR
                        ]
                    elif self.orientation == "Back":
                        return [
                            self.HEAD, self.CHEST,self.ARM_LEFT,self.ARM_RIGHT, self.FOOT_LEFT, self.FOOT_RIGHT,
                            self.LEG_LEFT, self.LEG_RIGHT, self.HAIR
                        ]
                    elif self.orientation == "Left":
                        if self.walking == 1:
                            return [self.HEAD, self.LEFT_EYE, self.LEFT_SMILE, self.SIDE_HAND_WALKB, self.LEFT_LEGF,
                                    self.SIDE_CHEST, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR]
                        elif self.walking == 2:
                            return [self.HEAD, self.LEFT_EYE, self.LEFT_SMILE, self.SIDE_HAND_WALKF, self.LEFT_LEGB,
                                    self.SIDE_CHEST, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR]
                        else:
                            return [ self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_CHEST, self.SIDE_LEGS, self.LEFT_SHOE, self.SIDE_HAND, self.HAIR]
                    elif self.orientation == "Right":
                        if self.walking == 1:
                            return [self.HEAD, self.RIGHT_EYE, self.RIGHT_SMILE, self.SIDE_HAND_WALKB, self.LEFT_LEGF,
                                    self.SIDE_CHEST, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR]
                        elif self.walking == 2:
                            return [self.HEAD, self.RIGHT_EYE, self.RIGHT_SMILE, self.SIDE_HAND_WALKF, self.LEFT_LEGB,
                                    self.SIDE_CHEST, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR]
                        else:
                            return [self.HEAD, self.RIGHT_EYE, self.RIGHT_SMILE, self.SIDE_CHEST, self.SIDE_LEGS, self.RIGHT_SHOE, self.SIDE_HAND, self.HAIR]
            elif self.race == "Elf":
                if self.gender == "Boy":
                    if self.orientation == "Front":
                        return [
                            self.HEAD,  self.CHEST, self.EYES, self.SMILE_HAPPY, self.ARM_LEFT,
                            self.ARM_RIGHT, self.FOOT_LEFT,self.FOOT_RIGHT, self.LEG_LEFT, self.LEG_RIGHT, self.HAIR, self.ELF_EAR_TIPS
                        ]
                    elif self.orientation == "Back":
                        return [
                            self.HEAD,  self.CHEST, self.ARM_LEFT,
                            self.ARM_RIGHT, self.FOOT_LEFT,self.FOOT_RIGHT, self.LEG_LEFT, self.LEG_RIGHT, self.HAIR, self.ELF_EAR_TIPS
                        ]
                    elif self.orientation == "Left":
                        if self.walking == 1:
                            # return [self.LEFT_LEGF]
                            return [self.HEAD, self.LEFT_SMILE,self.LEFT_EYE, self.SIDE_HAND_WALKB, self.LEFT_LEGF,
                                    self.SIDE_CHEST, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR, self.LEFT_ELF_EAR_TIPS]
                        elif self.walking == 2:
                            # return [self.LEFT_LEGF]
                            return [self.HEAD, self.LEFT_SMILE,self.LEFT_EYE, self.SIDE_HAND_WALKF, self.LEFT_LEGB,
                                    self.SIDE_CHEST, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR, self.LEFT_ELF_EAR_TIPS]
                        else:
                            # return [self.LEFT_LEGF]
                            return [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_CHEST, self.SIDE_LEGS,
                                    self.LEFT_SHOE, self.SIDE_HAND, self.HAIR, self.LEFT_ELF_EAR_TIPS]
                    elif self.orientation == "Right":
                        if self.walking == 1:
                            return [self.HEAD, self.RIGHT_EYE,
                                    self.RIGHT_SMILE, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.SIDE_CHEST,
                                    self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR, self.RIGHT_ELF_EAR_TIPS]
                        elif self.walking == 2:
                            return [self.HEAD, self.RIGHT_EYE,
                                    self.RIGHT_SMILE, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.SIDE_CHEST,
                                    self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR, self.RIGHT_ELF_EAR_TIPS]
                        else:
                            return [self.HEAD, self.RIGHT_EYE,
                                    self.RIGHT_SMILE, self.SIDE_CHEST, self.SIDE_LEGS, self.RIGHT_SHOE, self.SIDE_HAND, self.HAIR, self.RIGHT_ELF_EAR_TIPS]
                elif self.gender == "Girl":
                    if self.orientation == "Front":
                        return [
                            self.HEAD, self.CHEST,self.EYES, self.SMILE_HAPPY,self.ARM_LEFT,
                            self.ARM_RIGHT, self.FOOT_LEFT, self.FOOT_RIGHT, self.LEG_LEFT, self.LEG_RIGHT, self.HAIR, self.ELF_EAR_TIPS
                        ]
                    elif self.orientation == "Back":
                        return [
                            self.HEAD, self.CHEST,self.ARM_LEFT, self.ARM_RIGHT,
                            self.FOOT_LEFT, self.FOOT_RIGHT, self.LEG_LEFT,self.LEG_RIGHT, self.HAIR, self.ELF_EAR_TIPS
                        ]
                    elif self.orientation == "Left":
                        if self.walking == 1:
                            return [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_HAND_WALKB, self.LEFT_LEGF,
                                    self.SIDE_CHEST, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR, self.LEFT_ELF_EAR_TIPS]
                        elif self.walking == 2:
                            return [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_HAND_WALKF, self.LEFT_LEGB,
                                    self.SIDE_CHEST, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR, self.LEFT_ELF_EAR_TIPS]
                        else:
                            return [self.HEAD, self.LEFT_SMILE, self.LEFT_EYE, self.SIDE_CHEST, self.SIDE_LEGS,
                                    self.LEFT_SHOE, self.SIDE_HAND, self.HAIR, self.LEFT_ELF_EAR_TIPS]
                    elif self.orientation == "Right":
                        if self.walking == 1:
                            return [self.HEAD, self.RIGHT_SMILE, self.RIGHT_EYE, self.SIDE_HAND_WALKB, self.LEFT_LEGF,
                                    self.SIDE_CHEST, self.SIDE_HAND_WALKF, self.LEFT_LEGB, self.HAIR, self.RIGHT_ELF_EAR_TIPS]
                        elif self.walking == 2:
                            return [self.HEAD, self.RIGHT_SMILE, self.RIGHT_EYE, self.SIDE_HAND_WALKF, self.LEFT_LEGB,
                                    self.SIDE_CHEST, self.SIDE_HAND_WALKB, self.LEFT_LEGF, self.HAIR, self.RIGHT_ELF_EAR_TIPS]
                        else:
                            return [self.HEAD, self.RIGHT_SMILE, self.RIGHT_EYE, self.SIDE_CHEST, self.SIDE_LEGS,
                                    self.RIGHT_SHOE, self.SIDE_HAND, self.HAIR, self.RIGHT_ELF_EAR_TIPS]
            # return []
