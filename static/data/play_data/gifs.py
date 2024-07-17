from utils import Imports as I
class Gif:
    def __init__(self, name, frame_count, initial_path, delay):
        self.name = name
        self.frame_count = frame_count
        self.frame_paths = [initial_path + str(i) + ".png" for i in range(frame_count)]
        self.delay = delay
        self.start_gif = False
        self.current_frame = 0
        self.images = []
        self.frame_time = 0
        self.read_image()
        self.repeat = 1

    def read_image(self):
        for i in range(self.frame_count):
            path = self.frame_paths[i]
            self.images.append(I.pg.image.load(path).convert_alpha())

    # def update_frame(self):
    def Start_gif(self, name, rect):
        self.name = name
        self.start_gif = True
        self.current_frame = 0
        self.frame_time = I.pg.time.get_ticks()
        self.rect = rect #  if not a mob, make 1

    def next_frame(self, repeat):
        # Check if gif time has passed:
        if I.pg.time.get_ticks() - self.frame_time > self.delay:
            self.current_frame += 1
            self.frame_time = I.pg.time.get_ticks()
            if self.current_frame > self.frame_count:
                if repeat == self.repeat and repeat != -1:
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
            if self.current_frame == 0:
                return self.images[self.current_frame]
            else:
                return self.images[self.current_frame - 1]

