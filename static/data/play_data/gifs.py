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

    def read_image(self):
        for i in range(self.frame_count):
            path = self.frame_paths[i]
            self.images.append(I.pg.image.load(path).convert_alpha())

    # def update_frame(self):
    def Start_gif(self, name, object):
        self.name = name
        self.start_gif = True
        self.frame_time = I.pg.time.get_ticks()
        self.rect = object

    def next_frame(self):
        # Check if gif time has passed:
        if I.pg.time.get_ticks() - self.frame_time > self.delay:
            self.current_frame += 1
            self.frame_time = I.pg.time.get_ticks()
            if self.current_frame > self.frame_count:
                self.current_frame = 0
                self.start_gif = False
                return self.images[self.frame_count - 1]
            else:
                return self.images[self.current_frame - 1]
        else:
            # if frame time hasnt passed:
            return self.images[self.current_frame - 1]

