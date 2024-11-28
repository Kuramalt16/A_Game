from Values import Settings as S
from utils import Frequent_functions as Ff, Imports as I
class Gif:
    def __init__(self, name, count, path, delay, start):
        self.args = (name, count, path, delay, start)
        self.gif_dict = {}
        self.name = name
        self.frame_count = count
        self.delay = delay
        self.frame_paths = [path + str(i) + ".png" for i in range(count)]

        # self.read_db()
        if start == 0:
            self.start_gif = False
        else:
            self.Start_gif(self.name, 0)
        # self.start_gif = False
        self.current_frame = 0
        self.images = []
        self.frame_time = 0
        self.read_image()
        self.repeat = 1
        self.pause = 0
        self.frame_changed = False


    def read_image(self):
        for i in range(self.frame_count):
            path = self.frame_paths[i]
            call_path = I.os.getcwd()
            if "Testing" in call_path:
                call_path = call_path.replace("Testing", "") + path
                path = call_path
            self.images.append(I.pg.image.load(path).convert_alpha())

    def Start_gif(self, name, rect):
        self.name = name
        # self.name += 1
        self.start_gif = True
        self.current_frame = 0
        self.frame_changed = False
        self.frame_time = I.pg.time.get_ticks()
        self.rect = rect #  if not a mob, make 1

    def next_frame(self, repeat):
        # Check if gif time has passed:

        if self.start_gif == False:
            self.frame_changed = False
            return self.images[self.current_frame]
        if repeat == -1 and self.repeat != 999:
            self.repeat = 1
        if I.pg.time.get_ticks() - self.frame_time > self.delay:
            self.current_frame += 1
            self.frame_changed = True
            self.frame_time = I.pg.time.get_ticks()

            if self.current_frame > self.frame_count:
                if repeat == self.repeat and repeat != -1 or self.repeat == 999:
                    self.start_gif = False
                    self.repeat = 0
                    # print(decor[0].effected_decor[decor[1]])
                self.repeat += 1
                self.current_frame = 0
                return self.images[self.frame_count - 1]
            else:
                return self.images[self.current_frame - 1]
        else:
            # if frame time hasnt passed:
            self.frame_changed = False
            if self.current_frame == 0:
                return self.images[self.current_frame]
            else:
                return self.images[self.current_frame - 1]

def read_db(decorations):
    db_data = Ff.read_data_from_db("gifs", ["name", "frames", "path", "delay", "start"])
    gif_dict = {}
    for data in db_data:
        path = data[2]
        if data[2] == "Decor":
            path = decorations.decor_dict[data[0]]["path"]
        gif_dict[data[0]] = Gif(data[0], data[1], path, data[3], data[4])
    return gif_dict