import numpy as np
import wave

sample_rate = 44100
duration = 60.0  # 60 seconds
bpm = 82
beat_dur = 60.0 / bpm
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# -------------------------------------------------------------
# Track 1: Warm Fender Rhodes / Lo-Fi Electric Piano Chords
# Smooth 7th / 9th Jazz chords:
# 1. Dmaj9  (D3=146.83, F#3=185.00, A3=220.00, C#4=277.18, E4=329.63)
# 2. Bm9    (B2=123.47, D3=146.83,  F#3=185.00, A3=220.00,  C#4=277.18)
# 3. Gmaj7  (G2=98.00,  B2=123.47,  D3=146.83,  F#3=185.00)
# 4. Asus4  (A2=110.00, D3=146.83,  E3=164.81,  A3=220.00)
# -------------------------------------------------------------
rhodes_l = np.zeros_like(t)
rhodes_r = np.zeros_like(t)

chord_dur = beat_dur * 4.0  # 1 measure per chord
total_measures = int(duration / chord_dur) + 1

chord_progression = [
    [146.83, 185.00, 220.00, 277.18, 329.63], # Dmaj9
    [123.47, 146.83, 185.00, 220.00, 277.18], # Bm9
    [98.00,  123.47, 146.83, 185.00],         # Gmaj7
    [110.00, 146.83, 164.81, 220.00]          # Asus4 -> A
]

for m in range(total_measures):
    chord = chord_progression[m % len(chord_progression)]
    t_start = m * chord_dur
    idx_s = int(t_start * sample_rate)
    idx_e = min(int((t_start + chord_dur) * sample_rate), len(t))
    if idx_s >= len(t):
        break
    tm = t[idx_s:idx_e] - t_start

    # Gentle attack and warm exponential decay (Rhodes bell-like harmonic profile)
    env = (1.0 - np.exp(-tm * 25.0)) * np.exp(-tm * 0.75)

    for tone in chord:
        # Fundamental sine + subtle 2nd harmonic (warmth, no harsh buzz)
        sine1 = np.sin(2 * np.pi * tone * tm)
        sine2 = 0.22 * np.sin(2 * np.pi * (tone * 2) * tm)
        
        # Subtle stereo chorus / tremolo (classic vintage electric piano)
        tremolo_l = 1.0 + 0.12 * np.sin(2 * np.pi * 3.5 * tm)
        tremolo_r = 1.0 + 0.12 * np.sin(2 * np.pi * 3.5 * tm + np.pi / 2.0)

        note_signal = (sine1 + sine2) * env
        rhodes_l[idx_s:idx_e] += note_signal * tremolo_l * 0.14
        rhodes_r[idx_s:idx_e] += note_signal * tremolo_r * 0.14

# -------------------------------------------------------------
# Track 2: Deep Mellow Acoustic / Electric Bass (Warm & Round)
# Following chord roots: D2 (73.4Hz), B1 (61.7Hz), G1 (49.0Hz), A1 (55.0Hz)
# -------------------------------------------------------------
bass = np.zeros_like(t)
bass_notes = [73.42, 61.74, 49.00, 55.00]

for m in range(total_measures):
    fb = bass_notes[m % len(bass_notes)]
    # Play root on beat 1 and subtle octave bounce on beat 3.5
    patterns = [
        (0.0, fb, beat_dur * 2.2),
        (beat_dur * 2.5, fb * 2.0, beat_dur * 1.2)
    ]
    for p_offset, note_f, p_len in patterns:
        t_start = m * chord_dur + p_offset
        idx_s = int(t_start * sample_rate)
        idx_e = min(int((t_start + p_len) * sample_rate), len(t))
        if idx_s >= len(t):
            break
        tb = t[idx_s:idx_e] - t_start

        # Pure smooth sine wave bass with soft attack
        env_b = (1.0 - np.exp(-tb * 30.0)) * np.exp(-tb * 1.8)
        bass_wave = np.sin(2 * np.pi * note_f * tb) * env_b * 0.42
        bass[idx_s:idx_e] += bass_wave

# -------------------------------------------------------------
# Track 3: Organic Lo-Fi Drums (Soft Velvet Kick + Rimshot + Muted Hi-Hat)
# Zero aggressive clipping or harsh frequencies
# -------------------------------------------------------------
drums_l = np.zeros_like(t)
drums_r = np.zeros_like(t)
total_beats = int(duration / beat_dur)

for b in range(total_beats):
    t_beat = b * beat_dur
    ib_start = int(t_beat * sample_rate)

    # 1. Soft Warm Kick on beats 1 and sometimes syncopated on 2.5
    is_kick = (b % 4 == 0) or (b % 4 == 2 and (b // 4) % 2 == 1)
    if is_kick:
        k_len = int(0.28 * sample_rate)
        k_end = min(ib_start + k_len, len(t))
        tk = t[ib_start:k_end] - t_beat
        # Gentle pitch drop from 75Hz to 42Hz (warm acoustic lo-fi thud, no click)
        k_freq = 42.0 + 33.0 * np.exp(-tk * 20.0)
        k_phase = 2 * np.pi * np.cumsum(k_freq) / sample_rate
        k_env = np.exp(-tk * 12.0)
        kick_val = np.sin(k_phase) * k_env * 0.55
        drums_l[ib_start:k_end] += kick_val
        drums_r[ib_start:k_end] += kick_val

    # 2. Gentle Wooden Rimshot on beats 2 and 4 (Warm wooden click instead of harsh snare)
    if b % 2 == 1:
        s_len = int(0.12 * sample_rate)
        s_end = min(ib_start + s_len, len(t))
        ts = t[ib_start:s_end] - t_beat
        # Wooden click: 420Hz damped tone + soft filtered noise
        wood_tone = np.sin(2 * np.pi * 420.0 * ts) * np.exp(-ts * 55.0)
        soft_noise = np.random.normal(0, 0.15, len(ts)) * np.exp(-ts * 40.0)
        rim = (wood_tone * 0.4 + soft_noise * 0.6) * 0.35
        drums_l[ib_start:s_end] += rim
        drums_r[ib_start:s_end] += rim

    # 3. Soft Closed Shaker / Muted Hat every 8th note
    for sub in [0.0, beat_dur / 2.0]:
        t_hat = t_beat + sub
        ih_start = int(t_hat * sample_rate)
        ih_len = int(0.045 * sample_rate)
        ih_end = min(ih_start + ih_len, len(t))
        if ih_start >= len(t):
            break
        th = t[ih_start:ih_end] - t_hat
        # Soft noise with fast decay and bandpass feel
        hat = np.random.uniform(-0.1, 0.1, len(th)) * np.exp(-th * 90.0)
        drums_l[ih_start:ih_end] += hat * 0.18
        drums_r[ih_start:ih_end] += hat * 0.14

# -------------------------------------------------------------
# Track 4: Ambient Silk Atmosphere & Gentle Vinyl Crackle
# Creates a calm, cozy coffee-shop lo-fi feel
# -------------------------------------------------------------
ambient_l = np.zeros_like(t)
ambient_r = np.zeros_like(t)

# Soft vinyl surface warmth
vinyl = np.random.normal(0, 0.008, len(t))
# Occasional gentle vinyl clicks (warm tiny impulses)
click_indices = np.random.choice(len(t), size=120, replace=False)
vinyl[click_indices] += np.random.uniform(-0.06, 0.06, 120)

# Soft high-pad harmony in background (warm sine-based)
pad_freq = [440.0, 554.37, 659.25]  # A4, C#5, E5 gentle shimmer
for pf in pad_freq:
    slow_lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.12 * t)
    ambient_l += 0.015 * np.sin(2 * np.pi * pf * t) * slow_lfo
    ambient_r += 0.015 * np.sin(2 * np.pi * (pf * 1.002) * t) * slow_lfo

ambient_l += vinyl * 0.5
ambient_r += vinyl * 0.5

# -------------------------------------------------------------
# Master Mix & Gentle Acoustic Limiter (Professional Mastering)
# -------------------------------------------------------------
final_left = rhodes_l * 0.65 + bass * 0.5 + drums_l * 0.55 + ambient_l * 0.6
final_right = rhodes_r * 0.65 + bass * 0.5 + drums_r * 0.55 + ambient_r * 0.6

# Smooth fade in (2s) and fade out (3s) to be completely seamless and calm
fade_in_len = int(2.0 * sample_rate)
fade_out_len = int(3.0 * sample_rate)
fade_in = np.linspace(0.0, 1.0, fade_in_len)
fade_out = np.linspace(1.0, 0.0, fade_out_len)

final_left[:fade_in_len] *= fade_in
final_right[:fade_in_len] *= fade_in
final_left[-fade_out_len:] *= fade_out
final_right[-fade_out_len:] *= fade_out

# Normalize to comfortable -3dB ceiling (never harsh, never saturating)
peak = max(np.max(np.abs(final_left)), np.max(np.abs(final_right)))
if peak > 0:
    target_peak = 0.72  # Soft, comfortable listening volume
    final_left = (final_left / peak) * target_peak
    final_right = (final_right / peak) * target_peak

output_wav = "video/soundtrack_lofi_chill_ambient_60s.wav"
with wave.open(output_wav, 'w') as wav_file:
    wav_file.setnchannels(2)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    
    interleaved = np.empty((len(t) * 2,), dtype=np.int16)
    interleaved[0::2] = (final_left * 32767).astype(np.int16)
    interleaved[1::2] = (final_right * 32767).astype(np.int16)
    wav_file.writeframes(interleaved.tobytes())

print(f"Generated Calming Lo-Fi Soundtrack: {output_wav} (60s, 44.1kHz stereo)")
