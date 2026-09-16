import numpy as np
import wave

SAMPLE_RATE = 44100
DURATION = 60.0
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION)
BPM = 125.0
BEAT_DUR = 60.0 / BPM          # 0.48 s
SIXTEENTH = BEAT_DUR / 4.0      # 0.12 s
EIGHTH = BEAT_DUR / 2.0         # 0.24 s
BAR_DUR = BEAT_DUR * 4.0        # 1.92 s

left = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
right = np.zeros(TOTAL_SAMPLES, dtype=np.float32)

def midi_to_freq(m):
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))

# MIDI Note Numbers (Key: C minor)
# C2=36, Eb2=39, F2=41, G2=43, Ab2=44, Bb2=46
# C3=48, D3=50, Eb3=51, F3=53, G3=55, Ab3=56, B3=59
# C4=60, D4=62, Eb4=63, F4=65, G4=67, Ab4=68, Bb4=70, C5=72
NOTE_C2 = 36
NOTE_EB2 = 39
NOTE_F2 = 41
NOTE_G2 = 43
NOTE_AB2 = 44
NOTE_B2 = 47

NOTE_C3 = 48
NOTE_D3 = 50
NOTE_EB3 = 51
NOTE_F3 = 53
NOTE_G3 = 55
NOTE_AB3 = 56
NOTE_B3 = 59

NOTE_C4 = 60
NOTE_D4 = 62
NOTE_EB4 = 63
NOTE_F4 = 65
NOTE_G4 = 67
NOTE_AB4 = 68
NOTE_BB4 = 70
NOTE_C5 = 72
NOTE_D5 = 74
NOTE_EB5 = 75

# ==============================================================================
# 1. INDUSTRIAL GATED DRUMS (Movement Systems Drum Computer style @ 125 BPM)
# ==============================================================================
def make_sweet_kick():
    k_dur = 0.22
    k_samples = int(k_dur * SAMPLE_RATE)
    kt = np.linspace(0, k_dur, k_samples, endpoint=False)
    # Heavy, punchy bottom thump (from 140Hz down to 44Hz)
    k_pitch = 140.0 * np.exp(-kt * 30.0) + 44.0
    k_phase = 2 * np.pi * np.cumsum(k_pitch) / SAMPLE_RATE
    body = np.sin(k_phase) * np.exp(-kt * 14.0)
    # Beater click
    click = np.sin(2 * np.pi * 1400 * kt) * np.exp(-kt * 200.0)
    snd = (body * 0.90 + click * 0.35) * 0.88
    return np.clip(snd, -0.92, 0.92)

def make_sweet_snare():
    s_dur = 0.26
    s_samples = int(s_dur * SAMPLE_RATE)
    st = np.linspace(0, s_dur, s_samples, endpoint=False)
    # Gated plate reverb noise
    noise = (np.random.rand(s_samples) * 2.0 - 1.0) * np.exp(-st * 12.0)
    body = np.sin(2 * np.pi * 185 * st) * np.exp(-st * 20.0)
    clap = np.sin(2 * np.pi * 950 * st) * np.exp(-st * 40.0)
    snd = (noise * 0.70 + body * 0.35 + clap * 0.25) * 0.85
    return np.clip(snd, -0.90, 0.90)

def make_sweet_hat():
    h_dur = 0.055
    h_samples = int(h_dur * SAMPLE_RATE)
    ht = np.linspace(0, h_dur, h_samples, endpoint=False)
    env = np.exp(-ht * 55.0)
    noise = (np.random.rand(h_samples) * 2.0 - 1.0) * env * 0.22
    return noise

kick_raw = make_sweet_kick()
snare_raw = make_sweet_snare()
hat_raw = make_sweet_hat()

def add_audio(snd, start_t, pan=0.5, vol=1.0):
    idx = int(start_t * SAMPLE_RATE)
    s_len = len(snd)
    if idx + s_len >= TOTAL_SAMPLES:
        s_len = TOTAL_SAMPLES - idx
    if idx < 0 or s_len <= 0:
        return
    left[idx:idx+s_len] += snd[:s_len] * (1.0 - pan) * vol
    right[idx:idx+s_len] += snd[:s_len] * pan * vol

num_bars = int(DURATION / BAR_DUR) + 1
for bar in range(num_bars):
    b_start = bar * BAR_DUR
    
    # Kicks: Heavy on Beat 1, Beat 3, and offbeat pickup on 3.5 (& of 3)
    add_audio(kick_raw, b_start + 0.0 * BEAT_DUR, pan=0.5, vol=0.95)
    add_audio(kick_raw, b_start + 2.0 * BEAT_DUR, pan=0.5, vol=0.90)
    add_audio(kick_raw, b_start + 2.5 * BEAT_DUR, pan=0.5, vol=0.85)
    
    # Snares: Industrial gated crack on Beats 2 and 4
    add_audio(snare_raw, b_start + 1.0 * BEAT_DUR, pan=0.48, vol=0.92)
    add_audio(snare_raw, b_start + 3.0 * BEAT_DUR, pan=0.52, vol=0.95)
    
    # 16th-note metallic hi-hats
    for s in range(16):
        s_t = b_start + s * SIXTEENTH
        pan = 0.38 + 0.15 * (s % 2)
        v = 0.75 if (s % 2 == 0) else 0.45
        add_audio(hat_raw, s_t, pan=pan, vol=v)

# ==============================================================================
# 2. THE LEGENDARY HYPNOTIC ANALOG BASS/SYNTH ARPEGGIO (Roland SH-101)
# ==============================================================================
# The exact 2-bar ostinato riff in 16th notes:
# Bar 1 (Cm): C3, C3, Eb3, C3, G3, C3, Ab3, G3, C3, C3, Eb3, C3, G3, C3, Ab3, G3
# Bar 2 (Ab -> G): Ab2, Ab2, C3, Ab2, Eb3, Ab2, F3, Eb3, G2, G2, B2, G2, D3, G2, Eb3, D3
sweet_dreams_riff = [
    # Bar 1 (Cm) - 16 sixteenths
    (NOTE_C3, 0),  (NOTE_C3, 1),  (NOTE_EB3, 2), (NOTE_C3, 3),
    (NOTE_G3, 4),  (NOTE_C3, 5),  (NOTE_AB3, 6), (NOTE_G3, 7),
    (NOTE_C3, 8),  (NOTE_C3, 9),  (NOTE_EB3, 10), (NOTE_C3, 11),
    (NOTE_G3, 12), (NOTE_C3, 13), (NOTE_AB3, 14), (NOTE_G3, 15),
    
    # Bar 2 (Ab: sixteenths 16-23 | G: sixteenths 24-31)
    (NOTE_AB2, 16), (NOTE_AB2, 17), (NOTE_C3, 18),  (NOTE_AB2, 19),
    (NOTE_EB3, 20), (NOTE_AB2, 21), (NOTE_F3, 22),  (NOTE_EB3, 23),
    (NOTE_G2, 24),  (NOTE_G2, 25),  (NOTE_B2, 26),  (NOTE_G2, 27),
    (NOTE_D3, 28),  (NOTE_G2, 29),  (NOTE_EB3, 30), (NOTE_D3, 31)
]

def play_sh101_note(midi_pitch, start_t, dur, vol=0.42):
    idx = int(start_t * SAMPLE_RATE)
    s_len = int(dur * SAMPLE_RATE)
    if idx + s_len >= TOTAL_SAMPLES:
        s_len = TOTAL_SAMPLES - idx
    if s_len <= 0:
        return
    f = midi_to_freq(midi_pitch)
    st = np.linspace(0, dur, s_len, endpoint=False)
    
    # Analog Roland SH-101 synthesis:
    # Pulse wave with modulated pulse width (approx 30% duty) + Sawtooth + Sub-oscillator (-1 octave)
    phase = (f * st) % 1.0
    pulse = np.where(phase < 0.32, 1.0, -1.0)
    saw = 2.0 * phase - 1.0
    sub = np.sin(2 * np.pi * (f * 0.5) * st)
    
    # Resonant filter sweep envelope (punchy cutoff decay)
    filt_env = np.exp(-st * 22.0)
    osc_mix = pulse * 0.50 + saw * 0.35 + sub * 0.30
    # Saturation
    osc_mix = np.tanh(osc_mix * 1.3)
    
    # Amplitude envelope
    amp_env = np.exp(-st * 11.0) * (1.0 - np.exp(-st * 400.0))
    snd = osc_mix * amp_env * vol
    
    # Slight stereo width
    left[idx:idx+s_len] += snd * 0.92
    right[idx:idx+s_len] += snd * 0.88
    
    # 16th-note delay slap
    del_s = int(SIXTEENTH * 0.5 * SAMPLE_RATE)
    if idx + del_s + s_len < TOTAL_SAMPLES:
        left[idx+del_s:idx+del_s+s_len] += snd * 0.16
        right[idx+del_s:idx+del_s+s_len] += snd * 0.22

# Play the 2-bar riff continuously across the 60s
two_bar_dur_sixteenths = 32
num_riff_cycles = int((DURATION / SIXTEENTH) / two_bar_dur_sixteenths) + 1

for c in range(num_riff_cycles):
    base_s = c * two_bar_dur_sixteenths
    for pitch, offset_s in sweet_dreams_riff:
        note_time = (base_s + offset_s) * SIXTEENTH
        if note_time < DURATION - 0.15:
            # Play crisp 16th note staccato
            play_sh101_note(pitch, note_time, SIXTEENTH * 0.92, vol=0.44)

# ==============================================================================
# 3. ANALOG STRING PADS (Solina / Elka Rhapsody style)
# ==============================================================================
def play_string_chord(notes, start_t, dur, vol=0.18):
    idx = int(start_t * SAMPLE_RATE)
    s_len = int(dur * SAMPLE_RATE)
    if idx + s_len >= TOTAL_SAMPLES:
        s_len = TOTAL_SAMPLES - idx
    if s_len <= 0:
        return
    ct = np.linspace(0, dur, s_len, endpoint=False)
    # Slow attack and smooth release
    env = np.minimum(ct / 0.18, 1.0) * np.minimum((dur - ct) / 0.20, 1.0)
    chord_l = np.zeros(s_len, dtype=np.float32)
    chord_r = np.zeros(s_len, dtype=np.float32)
    for n in notes:
        f = midi_to_freq(n)
        # 3 detuned saws for lush ensemble chorus
        saw1 = 2.0 * ((f * 0.997) * ct % 1.0) - 1.0
        saw2 = 2.0 * ((f * 1.003) * ct % 1.0) - 1.0
        saw3 = 2.0 * (f * ct % 1.0) - 1.0
        chord_l += (saw1 * 0.4 + saw3 * 0.6)
        chord_r += (saw2 * 0.4 + saw3 * 0.6)
    left[idx:idx+s_len] += chord_l * env * vol
    right[idx:idx+s_len] += chord_r * env * vol

# 2-bar chord progression: Bar 1 = Cm, Bar 2 = Ab (2 beats) -> G (2 beats)
chord_cycle_bars = num_bars // 2 + 1
for cb in range(chord_cycle_bars):
    t_c = cb * BAR_DUR * 2
    # Bar 1: Cm [C4, Eb4, G4]
    play_string_chord([NOTE_C4, NOTE_EB4, NOTE_G4], t_c, BAR_DUR * 0.95, vol=0.16)
    # Bar 2: Ab [C4, Eb4, Ab4] (first 2 beats)
    play_string_chord([NOTE_C4, NOTE_EB4, NOTE_AB4], t_c + BAR_DUR, BEAT_DUR * 1.95, vol=0.17)
    # Bar 2: G [B3, D4, G4] (last 2 beats)
    play_string_chord([NOTE_B3, NOTE_D4, NOTE_G4], t_c + BAR_DUR + BEAT_DUR * 2.0, BEAT_DUR * 1.95, vol=0.18)

# ==============================================================================
# 4. ICONIC LEAD HOOK & VOCAL SYNTH ("Sweet dreams are made of this...")
# ==============================================================================
# The unmistakable vocal melody:
# "Sweet dreams are made of this"
# C4, C4, D4, Eb4, D4, C4, Bb3, C4
# "Who am I to disagree?"
# C4, C4, D4, Eb4, D4, C4, Bb3, C4
# "I travel the world and the seven seas"
# C4, C4, D4, Eb4, D4, C4, Bb3, C4, Eb4, F4, G4
# "Everybody's looking for something"
# G4, F4, Eb4, F4, Eb4, D4, C4
#
# Bridge: "Hold your head up, keep your head up..."
# High brass stabs: Eb5, D5, C5

melody_phrases = [
    # Phrase 1: "Sweet dreams are made of this"
    (NOTE_C4, 0.0, 0.6), (NOTE_C4, 0.75, 0.6), (NOTE_D4, 1.5, 0.6), (NOTE_EB4, 2.0, 0.8),
    (NOTE_D4, 2.75, 0.6), (NOTE_C4, 3.5, 0.6), (NOTE_BB3 if 'NOTE_BB3' in locals() else 58, 4.0, 0.6), (NOTE_C4, 4.75, 1.8),
    
    # Phrase 2: "Who am I to disagree?"
    (NOTE_C4, 8.0, 0.6), (NOTE_C4, 8.75, 0.6), (NOTE_D4, 9.5, 0.6), (NOTE_EB4, 10.0, 0.8),
    (NOTE_D4, 10.75, 0.6), (NOTE_C4, 11.5, 0.6), (58, 12.0, 0.6), (NOTE_C4, 12.75, 1.8),

    # Phrase 3: "I travel the world and the seven seas"
    (NOTE_C4, 16.0, 0.6), (NOTE_C4, 16.75, 0.6), (NOTE_D4, 17.5, 0.6), (NOTE_EB4, 18.0, 0.8),
    (NOTE_D4, 18.75, 0.6), (NOTE_C4, 19.5, 0.6), (58, 20.0, 0.6), (NOTE_C4, 20.75, 0.8),
    (NOTE_EB4, 21.5, 0.8), (NOTE_F4, 22.25, 0.8), (NOTE_G4, 23.0, 2.0),

    # Phrase 4: "Everybody's looking for something"
    (NOTE_G4, 25.0, 0.7), (NOTE_F4, 26.0, 0.7), (NOTE_EB4, 27.0, 0.7), (NOTE_F4, 28.0, 0.7),
    (NOTE_EB4, 29.0, 0.7), (NOTE_D4, 30.0, 0.7), (NOTE_C4, 31.0, 2.5)
]

def play_sweet_lead(midi_pitch, start_t, dur, vol=0.32):
    idx = int(start_t * SAMPLE_RATE)
    s_len = int(dur * SAMPLE_RATE)
    if idx + s_len >= TOTAL_SAMPLES:
        s_len = TOTAL_SAMPLES - idx
    if s_len <= 0:
        return
    f = midi_to_freq(midi_pitch)
    lt = np.linspace(0, dur, s_len, endpoint=False)
    
    # Warm analog lead with subtle vibrato
    vibrato = 1.0 + 0.006 * np.sin(2 * np.pi * 5.2 * lt) * np.minimum(lt / 0.25, 1.0)
    phase = 2 * np.pi * np.cumsum(f * vibrato) / SAMPLE_RATE
    saw = 2.0 * (phase / (2 * np.pi) % 1.0) - 1.0
    pulse = np.where((phase / (2 * np.pi) % 1.0) < 0.45, 1.0, -1.0)
    
    env = np.exp(-lt * 2.5) * (1.0 - np.exp(-lt * 200.0))
    snd = (saw * 0.6 + pulse * 0.4) * env * vol
    
    # Stereo delay echo
    left[idx:idx+s_len] += snd * 0.85
    right[idx:idx+s_len] += snd * 0.85
    
    del_s = int(EIGHTH * SAMPLE_RATE)
    if idx + del_s + s_len < TOTAL_SAMPLES:
        left[idx+del_s:idx+del_s+s_len] += snd * 0.25
        right[idx+del_s:idx+del_s+s_len] += snd * 0.35

# Play melody starting from bar 4 (~7.68s) up to 55s!
melody_start_beat = 16 # bar 4
for pitch, b_offset, dur_b in melody_phrases:
    note_time = (melody_start_beat + b_offset) * BEAT_DUR
    if note_time + dur_b * BEAT_DUR < DURATION - 1.0:
        play_sweet_lead(pitch, note_time, dur_b * BEAT_DUR, vol=0.32)

# High brass stabs in the bridge (from 38s onwards)
bridge_stabs = [
    (NOTE_EB5, 80.0), (NOTE_D5, 82.0), (NOTE_C5, 84.0),
    (NOTE_EB5, 88.0), (NOTE_D5, 90.0), (NOTE_C5, 92.0),
    (NOTE_G4, 96.0), (NOTE_AB4, 98.0), (NOTE_BB4, 100.0), (NOTE_C5, 102.0)
]
for pitch, b_pos in bridge_stabs:
    t_pos = b_pos * BEAT_DUR
    if t_pos + BEAT_DUR * 1.5 < DURATION - 0.5:
        play_sweet_lead(pitch, t_pos, BEAT_DUR * 1.2, vol=0.35)

# ==============================================================================
# 5. MASTERING & WARMTH
# ==============================================================================
max_val = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-6)
left = (left / max_val) * 0.90
right = (right / max_val) * 0.90

# Soft analog saturation
left = np.tanh(left * 1.15) * 0.88
right = np.tanh(right * 1.15) * 0.88

# Fades
f_in = int(0.2 * SAMPLE_RATE)
left[:f_in] *= np.linspace(0.0, 1.0, f_in)
right[:f_in] *= np.linspace(0.0, 1.0, f_in)

f_out = int(1.4 * SAMPLE_RATE)
left[-f_out:] *= np.linspace(1.0, 0.0, f_out)
right[-f_out:] *= np.linspace(1.0, 0.0, f_out)

out_file = "video/soundtrack_sweet_dreams_60s.wav"
with wave.open(out_file, "w") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    stereo = np.empty((TOTAL_SAMPLES * 2,), dtype=np.int16)
    stereo[0::2] = (left * 32767.0).astype(np.int16)
    stereo[1::2] = (right * 32767.0).astype(np.int16)
    wf.writeframes(stereo.tobytes())

print(f"Generated Eurythmics 'Sweet Dreams' Soundtrack: {out_file} (125 BPM in C minor, 60.0s)")
