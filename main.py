import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

sample_rate = 44100
duration = 5

def sine_wave(frequency, duration, sample_rate, scale_factor=1.0):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(2 * np.pi * frequency * t) * scale_factor

def bass_drum(frequency, duration_drum, sample_rate, scale_factor=1.0):
    t_drum = np.linspace(0, duration_drum, int(sample_rate * duration_drum), False)
    decay = np.exp(-t_drum * 4)
    return np.sin(2 * np.pi * frequency * t_drum) * decay * scale_factor

def clap_sound(frequency, duration_clap, sample_rate):
    t_clap = np.linspace(0, duration_clap, int(sample_rate * duration_clap), False)
    decay = np.exp(-t_clap * 8)
    return np.sin(2 * np.pi * frequency * t_clap) * decay

def snare_drum(sample_rate, duration_snare, scale_factor=1.0):
    noise_duration = int(sample_rate * duration_snare)
    noise = np.random.uniform(-1, 1, size=noise_duration)
    tone_frequency = 200
    t = np.linspace(0, duration_snare, noise_duration, False)
    tone = np.sin(2 * np.pi * tone_frequency * t)
    envelope = np.exp(-t * 10)
    return (tone + noise) * envelope * scale_factor

def floor_tom(frequency, duration_tom, sample_rate, scale_factor=1.0):
    t_tom = np.linspace(0, duration_tom, int(sample_rate * duration_tom), False)
    decay = np.exp(-t_tom * 3)
    fundamental = np.sin(2 * np.pi * frequency * t_tom)
    harmonic1 = np.sin(2 * np.pi * (frequency * 2) * t_tom) * 0.5
    harmonic2 = np.sin(2 * np.pi * (frequency * 3) * t_tom) * 0.25
    tom_sound = (fundamental + harmonic1 + harmonic2) * decay * scale_factor
    return tom_sound

def hi_hat(duration_hat, sample_rate, scale_factor=1.0):
    noise_duration = int(sample_rate * duration_hat)
    noise = np.random.uniform(-1, 1, size=noise_duration)
    envelope = np.exp(-np.linspace(0, 10, noise_duration))
    hat_sound = noise * envelope * scale_factor
    return hat_sound

# schedule sound by frequency
def schedule_sound_frequency(frequency, sound, duration, combined_waveform, sample_rate):
    intervals = np.arange(0, duration, frequency)
    for start_time in intervals:
        start_sample = int(start_time * sample_rate)
        end_sample = start_sample + len(sound)
        if end_sample > len(combined_waveform):
            end_sample = len(combined_waveform)
            sound = sound[:end_sample - start_sample]
        combined_waveform[start_sample:end_sample] += sound
    return combined_waveform

# generate sound
bass_drum_sound = bass_drum(60, 0.5, sample_rate, scale_factor=2.0)
clap_sound = clap_sound(400, 0.5, sample_rate)  
snare_sound = snare_drum(sample_rate, 0.5, 1.0) 
floor_tom_sound = floor_tom(50, 0.5, sample_rate, 1.0) 
sine_wave_sound = sine_wave(300, 0.009, sample_rate, 1.0)
hi_hat_sound = hi_hat(0.1, sample_rate, 0.5)

# initialize combined waveform and schedule drum sounds
combined_y = np.zeros(int(sample_rate * duration))

# setup frequency intervals
combined_y = schedule_sound_frequency(1.5, bass_drum_sound, duration, combined_y, sample_rate)
combined_y = schedule_sound_frequency(3, clap_sound, duration, combined_y, sample_rate)
combined_y = schedule_sound_frequency(1.5, snare_sound, duration, combined_y, sample_rate)
combined_y = schedule_sound_frequency(1, floor_tom_sound, duration, combined_y, sample_rate)
# combined_y = schedule_sound_frequency(0.5, sine_wave_sound, duration, combined_y, sample_rate)
combined_y = schedule_sound_frequency(0.25, hi_hat_sound, duration, combined_y, sample_rate)

max_val_combined = np.max(np.abs(combined_y))
if max_val_combined > 1:
    combined_y /= max_val_combined

sd.play(combined_y, sample_rate)
sd.wait()