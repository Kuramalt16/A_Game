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
        self.effect_flag = False
        self.channel0 = I.pg.mixer.Channel(0)
        self.channel1 = I.pg.mixer.Channel(5)
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

    def generate_teleport_sound(self, duration=0.2, sample_rate=44100, amplitude=32767 / 3):
        # Time array
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)

        # Frequency parameters
        start_freq = 10.0  # Low starting frequency
        end_freq = 200.0  # High climax frequency
        sweep_duration = 0.1  # Duration of pitch sweep to climax

        # Frequency sweep
        num_sweep_samples = int(sample_rate * sweep_duration)
        frequency = I.np.linspace(start_freq, end_freq, num_sweep_samples)

        # Generate the smooth sine wave
        wave = I.np.zeros(len(t))
        for i in range(len(t)):
            f = I.np.interp(i, [0, len(t) - 1], [start_freq, end_freq])
            wave[i] = I.np.sin(2 * I.np.pi * f * t[i])

        # Apply envelope: smooth attack, peak, and decay
        attack_samples = int(sample_rate * sweep_duration)
        sustain_samples = int(sample_rate * (duration - sweep_duration - 0.05))
        decay_samples = int(sample_rate * 0.05)

        envelope = I.np.concatenate([
            I.np.linspace(0, 1, attack_samples),  # Attack
            I.np.ones(sustain_samples),  # Sustain
            I.np.linspace(1, 0, decay_samples)  # Decay
        ])
        envelope = envelope[:len(wave)]  # Ensure the envelope matches the length of the wave
        wave *= envelope

        # Add reverb effect (simple room simulation)
        reverb_strength = 0.3
        reverb_wave = I.np.copy(wave)
        reverb_wave[int(sample_rate * 0.02):] += wave[:len(wave) - int(sample_rate * 0.02)] * reverb_strength

        # Normalize and convert to stereo
        stereo_wave = I.np.zeros((len(reverb_wave), 2), dtype=I.np.int16)
        stereo_wave[:, 0] = (amplitude * reverb_wave).astype(I.np.int16)
        stereo_wave[:, 1] = (amplitude * reverb_wave).astype(I.np.int16)

        return stereo_wave

    def generate_stabbing_sound(self, duration=0.1, sample_rate=44100, amplitude=32767 / 10):
        # Time array
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)

        # Frequency parameters
        base_freq = 200.0  # High frequency for piercing sound
        noise_strength = 0.5  # Strength of the white noise

        # Generate the high-frequency component
        wave = I.np.sin(2 * I.np.pi * base_freq * t)

        # Generate white noise
        noise = I.np.random.normal(0, noise_strength, len(t))

        # Combine wave and noise
        combined_wave = wave + noise

        # Apply envelope: fast attack and sharp decay
        attack_duration = 0.02  # Short attack phase
        decay_duration = 0.08  # Short decay phase

        attack_samples = int(sample_rate * attack_duration)
        decay_samples = int(sample_rate * decay_duration)

        envelope = I.np.concatenate([
            I.np.linspace(0, 1, attack_samples),  # Attack
            I.np.ones(len(t) - attack_samples - decay_samples),  # Sustain
            I.np.linspace(1, 0, decay_samples)  # Decay
        ])
        envelope = envelope[:len(combined_wave)]  # Ensure the envelope matches the length of the wave
        combined_wave *= envelope

        # Apply a basic reverb effect
        reverb_strength = 0.2
        reverb_wave = I.np.copy(combined_wave)
        delay = int(sample_rate * 0.01)  # Short delay for reverb effect
        if len(reverb_wave) > delay:
            reverb_wave[delay:] += combined_wave[:len(combined_wave) - delay] * reverb_strength

        # Normalize and convert to stereo
        stereo_wave = I.np.zeros((len(reverb_wave), 2), dtype=I.np.int16)
        stereo_wave[:, 0] = (amplitude * reverb_wave).astype(I.np.int16)
        stereo_wave[:, 1] = (amplitude * reverb_wave).astype(I.np.int16)

        return stereo_wave
    def generate_slash_sound(self, duration=0.2, sample_rate=44100, amplitude=32767 / 10):
        # Time array
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)

        # Frequency parameters
        start_freq = 300.0  # Starting frequency
        end_freq = 310.0  # Ending frequency
        sweep_duration = 0.1  # Duration of pitch sweep

        # Generate the frequency sweep
        frequency_sweep = I.np.linspace(start_freq, end_freq, int(sample_rate * sweep_duration))
        wave = I.np.zeros(len(t))
        for i in range(len(t)):
            f = I.np.interp(i, [0, len(t) - 1], [start_freq, end_freq])
            wave[i] = I.np.sin(2 * I.np.pi * f * t[i])

        # Generate white noise
        noise = I.np.random.normal(0, 0.2, len(t))

        # Combine wave and noise
        combined_wave = wave * 0.1 + noise * 0.9

        # Apply envelope: attack, peak, and decay
        attack_samples = int(sample_rate * sweep_duration)
        sustain_samples = int(sample_rate * (duration - sweep_duration - 0.05))
        decay_samples = int(sample_rate * 0.05)

        envelope = I.np.concatenate([
            I.np.linspace(0, 1, attack_samples),  # Attack
            I.np.ones(sustain_samples),  # Sustain
            I.np.linspace(1, 0, decay_samples)  # Decay
        ])
        envelope = envelope[:len(combined_wave)]  # Ensure the envelope matches the length of the wave
        combined_wave *= envelope

        # Apply a basic form of reverb by mixing the sound with a delayed version
        reverb_strength = 0.3
        reverb_wave = I.np.copy(combined_wave)
        delay = int(sample_rate * 0.02)  # Short delay for reverb effect
        if len(reverb_wave) > delay:
            reverb_wave[delay:] += combined_wave[:len(combined_wave) - delay] * reverb_strength

        # Normalize and convert to stereo
        stereo_wave = I.np.zeros((len(reverb_wave), 2), dtype=I.np.int16)
        stereo_wave[:, 0] = (amplitude * reverb_wave).astype(I.np.int16)
        stereo_wave[:, 1] = (amplitude * reverb_wave).astype(I.np.int16)

        return stereo_wave
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

    def generate_deep_bubble_sound(self, duration=0.25, sample_rate=44100, amplitude=32767 / 10):
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)
        base_freq = 150.0
        wave = I.np.sin(2 * I.np.pi * base_freq * t)
        wave *= I.np.exp(-4 * t)  # Longer decay for a deeper sound
        # noise = I.np.random.normal(0, 0.3, wave.shape)
        # wave += noise * 0.2
        stereo_wave = I.np.zeros((len(wave), 2), dtype=I.np.int16)
        stereo_wave[:, 0] = (amplitude * wave).astype(I.np.int16)
        stereo_wave[:, 1] = (amplitude * wave).astype(I.np.int16)
        return stereo_wave

    def generate_slime_sound(self, duration=0.15, sample_rate=44100, amplitude=32767 / 5):
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)

        # Base frequency for the "cutting" sound
        base_freq = 120.0

        # Generate a sharp, high-pitched sine wave
        sine_wave = I.np.sin(2 * I.np.pi * base_freq * t)

        # Apply frequency modulation to give a dynamic effect
        modulating_wave = I.np.sin(2 * I.np.pi * 60 * t)
        modulated_wave = I.np.sin(2 * I.np.pi * (base_freq + 400 * modulating_wave) * t)

        # Combine the original and modulated waves
        slash_wave = sine_wave * 0.7 + modulated_wave * 0.3

        # Apply an aggressive exponential decay for quick fade-out
        slash_wave *= I.np.exp(-12 * t)

        # Add a burst of white noise for texture
        noise = I.np.random.normal(0, 0.2, slash_wave.shape)
        slash_wave += noise * 0.1

        # Normalize and convert to stereo
        stereo_wave = I.np.zeros((len(slash_wave), 2), dtype=I.np.int16)
        stereo_wave[:, 0] = (amplitude * slash_wave).astype(I.np.int16)
        stereo_wave[:, 1] = (amplitude * slash_wave).astype(I.np.int16)

        return stereo_wave

    def generate_blunt_sound(self, duration=0.1, sample_rate=44100, amplitude=32767 / 10):
        # Generate white noise
        noise = I.np.random.uniform(0, 1, int(sample_rate * duration))

        # Apply an envelope to create a quick attack and decay
        t = I.np.linspace(0, duration, int(sample_rate * duration), False)
        # envelope = I.np.exp(-5 * t)  # Exponential decay for quick attack and decay
        # noise *= envelope

        # Convert to stereo by duplicating the single channel
        stereo_noise = I.np.zeros((len(noise), 2), dtype=I.np.int16)
        stereo_noise[:, 0] = (amplitude * noise).astype(I.np.int16)  # Left channel
        stereo_noise[:, 1] = (amplitude * noise).astype(I.np.int16)  # Right channel

        return stereo_noise
    def play_effect(self, effect):
        if not self.effect_flag:
            self.effect_flag = True
            self.effect_time = I.pg.time.get_ticks()
            self.channel1.stop()
            sound = I.pg.sndarray.make_sound(effect)
            self.channel1.play(sound)
