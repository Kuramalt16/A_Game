import os

from utils import Imports as I, Frequent_functions as Ff
from Values import Settings as S



# class create_sprite_decoration_gif(I.pg.sprite.Sprite):
#     def __init__(self, x, y, name, id, frame_path, frame_count, delay, start):
#         super().__init__()  # Initialize the parent Sprite class
#
#         # Create a simple surface to represent the sprite
#         self.frame_paths = [frame_path + str(i) + ".png" for i in range(frame_count)]
#         self.frame_count = frame_count
#         self.name = name
#         self.id = id
#         self.delay = delay
#         self.repeat = 0
#         self.current_frame = 0
#         self.images = []
#         self.frame_time = 0
#         self.pause = 0
#         self.frame_changed = False
#
#         if start == 0:
#             self.start_gif = False
#         else:
#             self.Start_gif(self.name, 0)
#
#         for i in range(self.frame_count):
#             path = self.frame_paths[i]
#             self.images.append(I.pg.image.load(path).convert_alpha())
#
#     def Start_gif(self, name, rect, repeat = 1):
#         self.start_gif = True
#         self.frame_changed = False
#         self.frame_time = I.pg.time.get_ticks()
#         self.repeat = repeat
#
#     def next_frame(self):
#         if self.start_gif and self.repeat != 0:
#             if self.repeat == -1:
#                 self.repeat = 1
#             if I.pg.time.get_ticks() >= self.frame_time + self.delay:
#                 self.current_frame += 1
#                 self.frame_time = I.pg.time.get_ticks()
#                 if self.current_frame > self.frame_count:
#                     self.current_frame = 0
#                     self.repeat -= 1
#                     if self.repeat < 0:
#                         self.repeat = 0
#             frame = self.images[self.current_frame]
#             return frame
#
#
# class create_sprite_npc(I.pg.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()  # Initialize the parent Sprite class
#
#         # Create a simple surface to represent the sprite
#         self.image = I.pg.Surface((50, 50))  # Create a 50x50 surface
#         self.image.fill((255, 0, 0))  # Fill the surface with red color
#
#         # Define the rectangular area of the sprite
#         self.rect = self.image.get_rect()  # Get the rectangle of the surface
#         self.rect.topleft = (x, y)  # Set the initial position
#
# class create_sprite_mob(I.pg.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()  # Initialize the parent Sprite class
#
#         # Create a simple surface to represent the sprite
#         self.image = I.pg.Surface((50, 50))  # Create a 50x50 surface
#         self.image.fill((255, 0, 0))  # Fill the surface with red color
#
#         # Define the rectangular area of the sprite
#         self.rect = self.image.get_rect()  # Get the rectangle of the surface
#         self.rect.topleft = (x, y)  # Set the initial position


class create_sprite_decoration(I.pg.sprite.Sprite):
    def __init__(self, name, id, image, rect, effect, hp, action, image_path):
        super().__init__()  # Initialize the parent Sprite class

        # Create a simple surface to represent the sprite
        image = I.pg.image.load(image_path)  # Create a 50x50 surface
        image_rect = image.get_size()
        self.name = name
        self.id = id
        flamable = hp.split(",,")[0]
        if flamable.lower() == "false":
            self.flamable = False
        else:
            self.flamable = True
        hp = int(hp.split(",,")[1].split(",")[0])
        self.hp = [hp, hp]
        self.image = image
        self.type = type
        self.action = action
        self.rect = rect
        self.effect = ''

class create_sprite_Player(I.pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Initialize the parent Sprite class
        self.player_group = I.pg.sprite.Group()
        self.images = []
        # Create a simple surface to represent the sprite
        for orientation in ["Back", "Front", "Left", "Right"]:
            for walking in ["", "1", "2"]:
                path = os.getcwd()
                path = path + "\static\data\created_characters\\" + str(I.info.SELECTED_CHARACTER) + "\\" + str(I.info.SELECTED_CHARACTER) + orientation + walking + ".png"
                image = I.pg.image.load(path)
                image = I.pg.transform.scale(image, (S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7))
                self.images.append(image)

        # Define the rectangular area of the sprite
        self.get_image = {
            ("Back", 0): 0,
            ("Back", 1): 1,
            ("Back", 2): 0,
            ("Back", 3): 2,
            ("Front", 0): 3,
            ("Front", 1): 4,
            ("Front", 2): 3,
            ("Front", 3): 5,
            ("Left", 0): 6,
            ("Left", 1): 7,
            ("Left", 2): 6,
            ("Left", 3): 8,
            ("Right", 0): 9,
            ("Right", 1): 10,
            ("Right", 2): 9,
            ("Right", 3): 11
        }
        self.image = self.images[self.get_image[I.info.LAST_ORIENT[0].replace(".png", ""), I.info.CURRENT_STANCE]]

        self.rect = I.pg.Rect(x, y, S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7)
        self.name = "Player"

    def update_player(self, x, y):
        self.image = self.images[self.get_image[I.info.LAST_ORIENT[0].replace(".png", ""), I.info.CURRENT_STANCE]]
        # self.rect.x += x
        # self.rect.y += y


class LayeredGroup(I.pg.sprite.LayeredUpdates):
    def __init__(self):
        super().__init__()

    def draw_sub_image(self, surface, data):
        sorted_sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.y)
        for sprite in sorted_sprites:
            temp_rect = sprite.rect.copy()
            temp_rect.topleft = sprite.rect.x - data["Zoom_rect"].x, sprite.rect.y - data["Zoom_rect"].y
            surface.blit(sprite.image, temp_rect)

    def draw_player(self, surface):
        player_sprite = next((sprite for sprite in self.sprites() if sprite.name == "Player"), None)
        surface.blit(player_sprite.image, player_sprite.rect)


Player_sprite = 0


class Sprite(I.pg.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        self.image = image
        self.rect = rect


Sub_image1 = I.pg.sprite.Group()
Sub_image2 = I.pg.sprite.Group()

# class DecorationGroup(I.pg.sprite.Group):
#     def draw(self, surface)