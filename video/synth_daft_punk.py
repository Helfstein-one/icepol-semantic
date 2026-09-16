import numpy as np
import wave

SAMPLE_RATE = 44100
DURATION = 60.0
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION)
BPM = 123.0
BEAT_DUR = 60.0 / BPM          # ~0.4878 s
SIXTEENTH = BEAT_DUR / 4.0      # ~0.12195 s
EIGHTH = BEAT_DUR / 2.0         # ~0.2439 s
BAR_DUR = BEAT_DUR * 4.0        # ~1.9512 s

left = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
right = np.zeros(TOTAL_SAMPLES, dtype=np.float32)

def midi_to_freq(m):
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))

# MIDI Notes (Key: E minor)
# E1=28, G1=31, A1=33, B1=35, C2=36, D2=38, E2=40
# E3=52, G3=55, A3=57, B3=59, C4=60, D4=62, E4=64, FSH4=66, G4=67, A4=69, B4=71, C5=72, D5=74, E5=76
NOTE_E1 = 28
NOTE_G1 = 31
NOTE_A1 = 33
NOTE_B1 = 35
NOTE_C2 = 36
NOTE_D2 = 38
NOTE_E2 = 40
NOTE_FSH2 = 42
NOTE_G2 = 43
NOTE_A2 = 45
NOTE_B2 = 47

NOTE_E3 = 52
NOTE_G3 = 55
NOTE_A3 = 57
NOTE_B3 = 59
NOTE_C4 = 60
NOTE_D4 = 62
NOTE_E4 = 64
NOTE_FSH4 = 66
NOTE_G4 = 67
NOTE_A4 = 69
NOTE_B4 = 71
NOTE_C5 = 72
NOTE_D5 = 74
NOTE_E5 = 76

# ==============================================================================
# 1. ROLAND TR-909 FRENCH HOUSE DRUM MACHINE (Pumping 4-on-the-Floor)
# ==============================================================================
def make_909_kick():
    k_dur = 0.20
    k_samples = int(k_dur * SAMPLE_RATE)
    kt = np.linspace(0, k_dur, k_samples, endpoint=False)
    # 909 punch: pitch drops from 160Hz to 48Hz with punchy mid transient
    k_pitch = 160.0 * np.exp(-kt * 38.0) + 48.0
    k_phase = 2 * np.pi * np.cumsum(k_pitch) / SAMPLE_RATE
    body = np.sin(k_phase) * np.exp(-kt * 16.0)
    click = np.sin(2 * np.pi * 1800 * kt) * np.exp(-kt * 280.0)
    snd = (body * 0.90 + click * 0.35) * 0.95
    return np.clip(snd, -0.95, 0.95)

def make_909_clap():
    c_dur = 0.22
    c_samples = int(c_dur * SAMPLE_RATE)
    ct = np.linspace(0, c_dur, c_samples, endpoint=False)
    # Multi-tap handclap bursts
    bursts = np.zeros(c_samples)
    for delay in [0.0, 0.012, 0.024, 0.038]:
        d_idx = int(delay * SAMPLE_RATE)
        b_len = c_samples - d_idx
        if b_len > 0:
            bt = np.linspace(0, b_len / SAMPLE_RATE, b_len, endpoint=False)
            bursts[d_idx:] += (np.random.rand(b_len) * 2.0 - 1.0) * np.exp(-bt * 35.0)
    body = np.sin(2 * np.pi * 1100 * ct) * np.exp(-ct * 25.0)
    snd = (bursts * 0.70 + body * 0.30) * 0.75
    return np.clip(snd, -0.85, 0.85)

def make_909_open_hat():
    h_dur = 0.18
    h_samples = int(h_dur * SAMPLE_RATE)
    ht = np.linspace(0, h_dur, h_samples, endpoint=False)
    env = np.exp(-ht * 14.0)
    # Bright metallic sizzle
    noise = (np.random.rand(h_samples) * 2.0 - 1.0) * env * 0.32
    return noise

def make_909_closed_hat():
    h_dur = 0.04
    h_samples = int(h_dur * SAMPLE_RATE)
    ht = np.linspace(0, h_dur, h_samples, endpoint=False)
    env = np.exp(-ht * 75.0)
    noise = (np.random.rand(h_samples) * 2.0 - 1.0) * env * 0.20
    return noise

kick_raw = make_909_kick()
clap_raw = make_909_clap()
hat_open_raw = make_909_open_hat()
hat_closed_raw = make_909_closed_hat()

def add_snd(snd, start_t, pan=0.5, vol=1.0):
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
    
    # 1. Four-on-the-Floor 909 Kick (Beats 1, 2, 3, 4)
    for b in range(4):
        # Filter sweep intro on first 2 bars (muffled kick opening up)
        k_vol = 0.95
        add_snd(kick_raw, b_start + b * BEAT_DUR, pan=0.5, vol=k_vol)
        
        # 2. Open Hi-Hat on the offbeat (The classic French House groove!)
        add_snd(hat_open_raw, b_start + b * BEAT_DUR + EIGHTH, pan=0.6, vol=0.85)

    # 3. 909 Clap on Beats 2 and 4
    add_snd(clap_raw, b_start + 1.0 * BEAT_DUR, pan=0.48, vol=0.88)
    add_snd(clap_raw, b_start + 3.0 * BEAT_DUR, pan=0.52, vol=0.92)

    # 4. Closed 16th Hi-hats with swing
    for s in range(16):
        if s % 2 == 0 and s % 4 != 2:
            add_snd(hat_closed_raw, b_start + s * SIXTEENTH, pan=0.4, vol=0.55)

# ==============================================================================
# 2. THE FUNKY DAFT PUNK BASSLINE (Bernard Edwards / Chic Slap Groove)
# ==============================================================================
# Iconic "Around the World" funky bassline in E minor:
# Pattern across 4 bars (64 sixteenths):
# Bar 1 (Em): E1, E1, -, G1, A1, -, B1, D2, -, E2, -, D2, B1, -, A1, G1
# Bar 2 (C -> D): C2, C2, -, E2, G2, -, A2, -, D2, D2, -, FSH2, A2, -, B2, -
# Repeated with infectious bounce!
daft_bass_pattern = [
    # Bar 1 (Em)
    (NOTE_E1, 0, 1.8), (NOTE_E1, 2, 1.2), (NOTE_G1, 4, 1.2), (NOTE_A1, 6, 1.8),
    (NOTE_B1, 8, 1.8), (NOTE_D2, 10, 1.8), (NOTE_E2, 12, 1.8), (NOTE_D2, 14, 1.2),
    
    # Bar 2 (Em continuation)
    (NOTE_B1, 16, 1.8), (NOTE_A1, 18, 1.2), (NOTE_G1, 20, 1.8), (NOTE_E1, 22, 1.8),
    (NOTE_G1, 24, 1.8), (NOTE_A1, 26, 1.8), (NOTE_B1, 28, 1.8), (NOTE_D2, 30, 1.2),
    
    # Bar 3 (C)
    (NOTE_C2, 32, 1.8), (NOTE_C2, 34, 1.2), (NOTE_E2, 36, 1.8), (NOTE_G2, 38, 1.8),
    (NOTE_A2 if 'NOTE_A2' in locals() else 45, 40, 1.8), (NOTE_G2, 42, 1.2), (NOTE_E2, 44, 1.8), (NOTE_C2, 46, 1.2),
    
    # Bar 4 (D)
    (NOTE_D2, 48, 1.8), (NOTE_D2, 50, 1.2), (NOTE_FSH2 if 'NOTE_FSH2' in locals() else 42, 52, 1.8), (NOTE_A2, 54, 1.8),
    (NOTE_B2 if 'NOTE_B2' in locals() else 47, 56, 1.8), (NOTE_A2, 58, 1.2), (NOTE_FSH2, 60, 1.8), (NOTE_D2, 62, 1.2)
]

def play_funk_bass(midi_pitch, start_t, dur, vol=0.40):
    idx = int(start_t * SAMPLE_RATE)
    s_len = int(dur * SAMPLE_RATE)
    if idx + s_len >= TOTAL_SAMPLES:
        s_len = TOTAL_SAMPLES - idx
    if s_len <= 0:
        return
    f = midi_to_freq(midi_pitch)
    bt = np.linspace(0, dur, s_len, endpoint=False)
    
    # Resonant Funky Filter Envelope (Mu-Tron / Envelope Filter)
    filt = np.exp(-bt * 14.0)
    # Sawtooth with sub-sine
    saw = 2.0 * (f * bt % 1.0) - 1.0
    sub = np.sin(2 * np.pi * (f * 0.5) * bt)
    
    # Plucky slap transient
    pluck = np.sin(2 * np.pi * (f * 3.0) * bt) * np.exp(-bt * 60.0)
    
    amp = np.exp(-bt * 9.0) * (1.0 - np.exp(-bt * 350.0))
    raw = (saw * 0.65 + sub * 0.35 + pluck * 0.25) * amp * vol
    
    # French touch sidechain ducking on beat (simulated by dipping right at beat)
    rel_beat = (start_t % BEAT_DUR) / BEAT_DUR
    if rel_beat < 0.25:
        raw *= (0.6 + 0.4 * (rel_beat / 0.25))
        
    left[idx:idx+s_len] += raw * 0.90
    right[idx:idx+s_len] += raw * 0.90

four_bar_sixteenths = 64
num_bass_loops = int((DURATION / SIXTEENTH) / four_bar_sixteenths) + 1
for l in range(num_bass_loops):
    base_s = l * four_bar_sixteenths
    for pitch, s_pos, dur_s in daft_bass_pattern:
        t_note = (base_s + s_pos) * SIXTEENTH
        if t_note < DURATION - 0.2:
            play_funk_bass(pitch, t_note, dur_s * SIXTEENTH, vol=0.42)

# ==============================================================================
# 3. DISCO FUNK GUITAR / CLAVINET OFFBEAT CHORDS
# ==============================================================================
def play_disco_stab(notes, start_t, dur, vol=0.18):
    idx = int(start_t * SAMPLE_RATE)
    s_len = int(dur * SAMPLE_RATE)
    if idx + s_len >= TOTAL_SAMPLES:
        s_len = TOTAL_SAMPLES - idx
    if s_len <= 0:
        return
    ct = np.linspace(0, dur, s_len, endpoint=False)
    env = np.exp(-ct * 18.0) * (1.0 - np.exp(-ct * 200.0))
    sig_l = np.zeros(s_len, dtype=np.float32)
    sig_r = np.zeros(s_len, dtype=np.float32)
    for n in notes:
        f = midi_to_freq(n)
        # Pulse wave clavinet + phaser
        phase = (f * ct) % 1.0
        pulse = np.where(phase < 0.25, 1.0, -1.0)
        sig_l += pulse * 0.5
        sig_r += pulse * 0.5
    left[idx:idx+s_len] += sig_l * env * vol * 0.8
    right[idx:idx+s_len] += sig_r * env * vol * 1.2

# Em [G3, B3, E4] -> C [G3, C4, E4] -> D [A3, D4, FSH4]
funk_chords = [
    ([NOTE_G3, NOTE_B3, NOTE_E4], 8),   # Em
    ([NOTE_G3, NOTE_C4, NOTE_E4], 4),   # C
    ([NOTE_A3, NOTE_D4, NOTE_FSH4], 4)  # D
]

c_beat = 0
total_beats = int(DURATION / BEAT_DUR)
while c_beat < total_beats:
    for notes, b_len in funk_chords:
        for b in range(b_len):
            if c_beat >= total_beats:
                break
            b_t = c_beat * BEAT_DUR
            # Offbeat 8th note stab (classic French Touch house)
            play_disco_stab(notes, b_t + EIGHTH, SIXTEENTH * 1.4, vol=0.20)
            c_beat += 1

# ==============================================================================
# 4. VOCODER ROBOT HOOK ("Around the World" & "Harder, Better, Faster, Stronger")
# ==============================================================================
# Part A: "Around the world, around the world" (Bar 2 to 16)
# Notes: E4 -> G4 -> A4 -> G4 -> E4 -> D4 -> E4
around_the_world_phrase = [
    (NOTE_E4, 0.0, 0.7), (NOTE_G4, 0.75, 0.7), (NOTE_A4, 1.5, 0.9), (NOTE_G4, 2.5, 0.7),
    (NOTE_E4, 3.25, 0.7), (NOTE_D4, 4.0, 0.7), (NOTE_E4, 4.75, 2.2)
]

# Part B: "Work it, make it, do it, makes us / Harder, better, faster, stronger" (From 26s onwards!)
# B4, B4, B4, A4, G4, E4
harder_better_phrase = [
    # "Work it, make it, do it, makes us"
    (NOTE_B4, 0.0, 0.4), (NOTE_B4, 0.5, 0.4), (NOTE_B4, 1.0, 0.4), (NOTE_A4, 1.5, 0.4),
    (NOTE_G4, 2.0, 0.5), (NOTE_E4, 2.5, 1.0),
    
    # "Harder, better, faster, stronger"
    (NOTE_B4, 4.0, 0.4), (NOTE_B4, 4.5, 0.4), (NOTE_B4, 5.0, 0.4), (NOTE_D5, 5.5, 0.5),
    (NOTE_C5, 6.0, 0.4), (NOTE_B4, 6.5, 0.4), (NOTE_A4, 7.0, 1.2),
    
    # "More than, ever, hour, after"
    (NOTE_G4, 8.0, 0.4), (NOTE_G4, 8.5, 0.4), (NOTE_G4, 9.0, 0.4), (NOTE_A4, 9.5, 0.4),
    (NOTE_B4, 10.0, 0.5), (NOTE_G4, 10.5, 1.0),
    
    # "Our work is never over"
    (NOTE_E4, 12.0, 0.4), (NOTE_G4, 12.5, 0.4), (NOTE_A4, 13.0, 0.4), (NOTE_G4, 13.5, 0.4),
    (NOTE_E4, 14.0, 1.8)
]

def play_vocoder_lead(midi_pitch, start_t, dur, vol=0.30):
    idx = int(start_t * SAMPLE_RATE)
    s_len = int(dur * SAMPLE_RATE)
    if idx + s_len >= TOTAL_SAMPLES:
        s_len = TOTAL_SAMPLES - idx
    if s_len <= 0:
        return
    f = midi_to_freq(midi_pitch)
    vt = np.linspace(0, dur, s_len, endpoint=False)
    
    # Daft Punk Vocoder / Antares Auto-tune sound:
    # Rich harmonics (Sawtooth + Pulse) modulated by formant frequencies (vowel resonance)
    carrier = 2.0 * (f * vt % 1.0) - 1.0
    # Formant resonances around 800Hz and 2400Hz (robot vocal timbre)
    formant1 = np.sin(2 * np.pi * 820.0 * vt) * np.exp(-vt * 3.0)
    formant2 = np.sin(2 * np.pi * 2250.0 * vt) * np.exp(-vt * 4.0)
    
    # Sharp envelope
    env = np.minimum(vt / 0.02, 1.0) * np.exp(-vt * 1.5)
    snd = (carrier * 0.65 + formant1 * 0.20 + formant2 * 0.15) * env * vol
    
    # Stereo Flanger & Ping-Pong Delay
    left[idx:idx+s_len] += snd * 0.85
    right[idx:idx+s_len] += snd * 0.85
    
    del_s = int(EIGHTH * SAMPLE_RATE)
    if idx + del_s + s_len < TOTAL_SAMPLES:
        left[idx+del_s:idx+del_s+s_len] += snd * 0.25
        right[idx+del_s:idx+del_s+s_len] += snd * 0.35

# Play "Around the World" theme from bar 2 to 14 (~3.9s to ~27s)
for loop in range(3):
    l_start_b = 8 + loop * 8
    for pitch, b_off, dur_b in around_the_world_phrase:
        n_t = (l_start_b + b_off) * BEAT_DUR
        if n_t + dur_b * BEAT_DUR < 27.0:
            play_vocoder_lead(pitch, n_t, dur_b * BEAT_DUR, vol=0.32)

# Play "Harder, Better, Faster, Stronger" theme from 27.5s to 56s!
hb_start_b = int(27.5 / BEAT_DUR)
for loop in range(2):
    l_start_b = hb_start_b + loop * 16
    for pitch, b_off, dur_b in harder_better_phrase:
        n_t = (l_start_b + b_off) * BEAT_DUR
        if n_t + dur_b * BEAT_DUR < DURATION - 1.0:
            play_vocoder_lead(pitch, n_t, dur_b * BEAT_DUR, vol=0.35)

# ==============================================================================
# 5. FRENCH TOUCH MASTERING (Maximizer, Saturation & High-Pass Filter Sweep)
# ==============================================================================
max_val = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-6)
left = (left / max_val) * 0.90
right = (right / max_val) * 0.90

# Tube / Console saturation (Alesis 3630 compressor style)
left = np.tanh(left * 1.15) * 0.88
right = np.tanh(right * 1.15) * 0.88

# Fades
f_in = int(0.2 * SAMPLE_RATE)
left[:f_in] *= np.linspace(0.0, 1.0, f_in)
right[:f_in] *= np.linspace(0.0, 1.0, f_in)

f_out = int(1.2 * SAMPLE_RATE)
left[-f_out:] *= np.linspace(1.0, 0.0, f_out)
right[-f_out:] *= np.linspace(1.0, 0.0, f_out)

out_file = "video/soundtrack_daft_punk_60s.wav"
with wave.open(out_file, "w") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    stereo = np.empty((TOTAL_SAMPLES * 2,), dtype=np.int16)
    stereo[0::2] = (left * 32767.0).astype(np.int16)
    stereo[1::2] = (right * 32767.0).astype(np.int16)
    wf.writeframes(stereo.tobytes())

print(f"Generated Daft Punk French House Soundtrack: {out_file} (123 BPM in E minor, 60.0s)")
