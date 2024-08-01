from utils import Imports as I
from Values import Settings as S
class Song:
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes
        self.music = {}
        self.generate_song(notes)
        self.current_note = 0
        self.start_time = 0
        self.effect_time = 0
        self.channel0 = I.pg.mixer.Channel(0)
        self.channel1 = I.pg.mixer.Channel(1)
    def generate_song(self, notes):
        i = 0
        chord = []
        for frequency, duration in notes:
            if isinstance(frequency, tuple):
                for a in frequency:
                    chord.append(self.generate_sine_wave(a, duration/1000))
                wave = I.np.sum(I.np.array(chord), axis=0)
                wave = wave.astype(I.np.int16)
                chord = []
            else:
                wave = self.generate_sine_wave(frequency, duration/1000)
            self.music[i] = (wave, duration)
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
        sound = I.pg.sndarray.make_sound(song[self.current_note][0])
        self.channel0.play(sound)  # Play the new sound

    def next_note(self):
        self.start_time = I.pg.time.get_ticks()
        self.channel0.stop()  # Stop any sound currently playing on the channel
        self.play_song_by_note(self.music)
        self.current_note += 1
        if self.current_note >= len(self.notes):
            self.current_note = 0
        # return self.music[self.current_note][1]

    def play_once(self, frequency):
        wave = self.generate_sine_wave(frequency, 1)
        self.channel1.stop()  # Stop any sound currently playing on the channel
        sound = I.pg.sndarray.make_sound(wave)
        self.channel1.play(sound)  # Play the new sound

    def play_chords(self, frequency):
        wave = []
        self.effect_time = I.pg.time.get_ticks()
        for i in frequency:
            wave.append(self.generate_sine_wave(i, 1))
        combined_wave = I.np.sum(I.np.array(wave), axis=0)
        combined_wave = combined_wave.astype(I.np.int16)
        self.channel1.stop()  # Stop any sound currently playing on the channel
        sound = I.pg.sndarray.make_sound(combined_wave)
        self.channel1.play(sound)  # Play the new sound

    def generate_bash_sound(self, duration=0.5, sample_rate=44100, amplitude=32767 / 10):
        # Generate white noise
        noise = I.np.random.uniform(-1, 1, int(sample_rate * duration))

        # Apply an envelope to create a quick attack and decay
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)
        envelope = I.np.exp(-5 * t)  # Exponential decay for quick attack and decay
        noise *= envelope

        # Convert to stereo by duplicating the single channel
        stereo_noise = I.np.zeros((len(noise), 2), dtype=I.np.int16)
        stereo_noise[:, 0] = (amplitude * noise).astype(I.np.int16)  # Left channel
        stereo_noise[:, 1] = (amplitude * noise).astype(I.np.int16)  # Right channel

        return stereo_noise

    def generate_slicing_sound(self, duration=0.2, sample_rate=44100, amplitude=32767 / 10):
        # Generate white noise
        noise = I.np.random.uniform(-1, 1, int(sample_rate * duration))

        # Apply an envelope to create a sharp attack with quick decay
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)
        envelope = I.np.exp(-20 * t)  # Exponential decay for sharp attack and quick fade-out
        noise *= envelope

        # Convert to stereo by duplicating the single channel
        stereo_noise = I.np.zeros((len(noise), 2), dtype=I.np.int16)
        stereo_noise[:, 0] = (amplitude * noise).astype(I.np.int16)  # Left channel
        stereo_noise[:, 1] = (amplitude * noise).astype(I.np.int16)  # Right channel

        return stereo_noise

    def generate_thump_sound(self, duration=0.2, sample_rate=44100, amplitude=32767 / 10):
        """
        Generate a 'thump' sound effect representing a punch or impact.
        :param duration: Duration of the sound in seconds.
        :param sample_rate: Sample rate in Hz.
        :param amplitude: Volume of the sound.
        :return: A 2D numpy array representing stereo sound.
        """
        # Generate white noise
        noise = I.np.random.uniform(-1, 1, int(sample_rate * duration))

        # Apply an envelope to create a sharp attack with quick decay
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)
        envelope = I.np.exp(-30 * t)  # Exponential decay for sharp attack and fast fade-out
        noise *= envelope

        # Add a low-frequency component for a more punchy effect
        low_freq_tone = 0.3 * I.np.sin(2 * I.np.pi * 50 * t)  # Low-frequency tone at 50 Hz
        noise += low_freq_tone

        # Convert to stereo by duplicating the single channel
        stereo_noise = I.np.zeros((len(noise), 2), dtype=I.np.int16)
        stereo_noise[:, 0] = (amplitude * noise).astype(I.np.int16)  # Left channel
        stereo_noise[:, 1] = (amplitude * noise).astype(I.np.int16)  # Right channel

        return stereo_noise

    def generate_glass_break(self, duration=0.5, sample_rate=44100, amplitude=32767 / 10):
        """
        Generate a sound effect representing a character dying.
        :param duration: Duration of the sound in seconds.
        :param sample_rate: Sample rate in Hz.
        :param amplitude: Volume of the sound.
        :return: A 2D numpy array representing stereo sound.
        """
        # Generate white noise for ambient sound
        noise = I.np.random.uniform(-1, 1, int(sample_rate * duration))
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)

        # Create an envelope for the noise
        noise_envelope = I.np.exp(-20 * t)
        noise *= noise_envelope

        # Generate a high-pitched gasp
        gasp_freq = 1000
        gasp = 0.5 * I.np.sin(2 * I.np.pi * gasp_freq * t)
        gasp_envelope = I.np.exp(-10 * t)
        gasp *= gasp_envelope

        # Generate a low-frequency thud
        thud_freq = 50
        thud = 0.3 * I.np.sin(2 * I.np.pi * thud_freq * t)
        thud_envelope = I.np.exp(-30 * t)
        thud *= thud_envelope

        # Combine the sounds
        dying_sound = noise + gasp + thud

        # Convert to stereo by duplicating the single channel
        stereo_dying_sound = I.np.zeros((len(dying_sound), 2), dtype=I.np.int16)
        stereo_dying_sound[:, 0] = (amplitude * dying_sound).astype(I.np.int16)  # Left channel
        stereo_dying_sound[:, 1] = (amplitude * dying_sound).astype(I.np.int16)  # Right channel

        return stereo_dying_sound

    def generate_fire_sound(self, duration=1.0, sample_rate=44100, amplitude=32767 / 10):
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)
        freq = 50.0  # Low frequency for a deep, explosive sound
        fire_wave = I.np.sin(2 * I.np.pi * freq * t)

        burst_duration = 0.1  # Duration of each noise burst
        burst_intervals = int(sample_rate * burst_duration)
        num_bursts = int(duration / burst_duration)

        noise = I.np.zeros(int(sample_rate * duration))
        for i in range(num_bursts):
            start_idx = i * burst_intervals
            end_idx = start_idx + burst_intervals
            noise[start_idx:end_idx] = I.np.random.uniform(-1, 1, burst_intervals)

        fire_sound = (fire_wave * 0.7 + noise * 0.3) * I.np.exp(-3 * t)  # Combine and apply decay
        stereo_fire = I.np.zeros((len(fire_sound), 2), dtype=I.np.int16)
        stereo_fire[:, 0] = (amplitude * fire_sound).astype(I.np.int16)
        stereo_fire[:, 1] = (amplitude * fire_sound).astype(I.np.int16)
        return stereo_fire

    def generate_cold_sound(self, duration=0.5, sample_rate=44100, amplitude=32767 / 10):
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)
        freq = 1200.0  # High frequency for a clear, ringing sound
        cold_wave = I.np.sin(2 * I.np.pi * freq * t)
        noise = I.np.random.uniform(-1, 1, int(sample_rate * duration)) * 0.1
        cold_sound = (cold_wave + noise) * I.np.exp(-20 * t)  # Quick decay for a short, sharp sound
        stereo_cold = I.np.zeros((len(cold_sound), 2), dtype=I.np.int16)
        stereo_cold[:, 0] = (amplitude * cold_sound).astype(I.np.int16)
        stereo_cold[:, 1] = (amplitude * cold_sound).astype(I.np.int16)
        return stereo_cold

    def generate_magic_sound(self, duration=1.0, sample_rate=44100, amplitude=32767 / 10):
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)
        fire_wave = I.np.sin(2 * I.np.pi * 50 * t)
        freq1, freq2 = 500.0, 700.0
        wave1 = I.np.sin(2 * I.np.pi * freq1 * t)
        wave2 = I.np.sin(2 * I.np.pi * freq2 * t)
        magic_sound = (wave1 + wave2) * 0.5
        magic_sound = (fire_wave * 0.7 + magic_sound * 0.3) * I.np.exp(-3 * t)  # Combine and apply decay
        stereo_magic = I.np.zeros((len(magic_sound), 2), dtype=I.np.int16)
        stereo_magic[:, 0] = (amplitude * magic_sound).astype(I.np.int16)
        stereo_magic[:, 1] = (amplitude * magic_sound).astype(I.np.int16)
        return stereo_magic

    def generate_charging_up_sound(self, duration=2.0, sample_rate=44100, amplitude=32767 / 10):
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)
        start_freq, end_freq = 200.0, 2000.0
        freqs = I.np.linspace(start_freq, end_freq, len(t))
        charging_wave = I.np.sin(2 * I.np.pi * freqs * t)

        noise = I.np.random.uniform(-0.1, 0.1, int(sample_rate * duration))
        charging_sound = (charging_wave + noise) * I.np.exp(-0.5 * t)

        stereo_charging = I.np.zeros((len(charging_sound), 2), dtype=I.np.int16)
        stereo_charging[:, 0] = (amplitude * charging_sound).astype(I.np.int16)
        stereo_charging[:, 1] = (amplitude * charging_sound).astype(I.np.int16)
        return stereo_charging

    def play_effect(self, effect):
        self.effect_time = I.pg.time.get_ticks()
        self.channel1.stop()
        sound = I.pg.sndarray.make_sound(effect)
        self.channel1.play(sound)