from utils import Imports as I
class Song:
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes
        self.song = {}
        self.generate_song(notes)
        self.current_note = 0
        self.start_time = 0
    def generate_song(self, notes):
        i = 0
        for frequency, duration in notes:
            wave = self.generate_sine_wave(frequency, 1)
            self.song[i] = (wave, duration)
            i += 1

    def generate_sine_wave(self, frequency, duration, sample_rate=44100, amplitude=32767 / 10):
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)
        wave = amplitude * I.np.sin(2 * I.np.pi * frequency * t)
        wave = wave.astype(I.np.int16)
        stereo_wave = I.np.zeros((wave.size, 2), dtype=I.np.int16)
        stereo_wave[:, 0] = wave  # Left channel
        stereo_wave[:, 1] = wave  # Right channel
        return stereo_wave

    def play_song_by_note(self, song):
        if self.current_note >= len(self.notes):
            self.current_note = 0
        sound = I.pg.sndarray.make_sound(song[self.current_note][0])
        sound.play()  # Play the sound once
    def next_note(self):
        self.start_time = I.pg.time.get_ticks()
        sound = I.pg.sndarray.make_sound(self.song[self.current_note][0])
        sound.stop()
        self.current_note += 1
        self.play_song_by_note(self.song)
        return self.song[self.current_note][1]

    def play_once(self, frequency):
        wave = self.generate_sine_wave(frequency, 1)
        sound = I.pg.sndarray.make_sound(wave)
        sound.play(0)