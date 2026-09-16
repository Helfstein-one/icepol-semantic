import numpy as np
import wave
import struct

SAMPLE_RATE = 44100
DURATION = 85.0
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

# MIDI Note definitions (Key: G minor)
G1 = 31; A1 = 33; BB1 = 34; C2 = 36; D2 = 38; EB2 = 39; F2 = 41
G2 = 43; A2 = 45; BB2 = 46; C3 = 48; D3 = 50; EB3 = 51; F3 = 53
G3 = 55; A3 = 57; BB3 = 58; C4 = 60; D4 = 62; EB4 = 63; F4 = 65
G4 = 67; A4 = 69; BB4 = 70; C5 = 72; D5 = 74; EB5 = 75; F5 = 77
G5 = 79; A5 = 81; BB5 = 82; C6 = 84; D6 = 86

# ==============================================================================
# 1. DRUM MACHINE (Roland TR-909 Eurodance Kit)
# ==============================================================================
def make_909_kick():
    k_dur = 0.22
    k_samples = int(k_dur * SAMPLE_RATE)
    kt = np.linspace(0, k_dur, k_samples, endpoint=False)
    # Punchy pitch drop from 220Hz down to 50Hz
    k_pitch = 220.0 * np.exp(-kt * 40.0) + 50.0
    k_phase = 2 * np.pi * np.cumsum(k_pitch) / SAMPLE_RATE
    body = np.sin(k_phase) * np.exp(-kt * 16.0)
    # Attack transient click
    click = np.sin(2 * np.pi * 1400 * kt) * np.exp(-kt * 350.0)
    snd = (body * 0.90 + click * 0.35) * 0.88
    return np.clip(snd, -0.95, 0.95)

def make_909_snare_clap():
    s_dur = 0.25
    s_samples = int(s_dur * SAMPLE_RATE)
    st = np.linspace(0, s_dur, s_samples, endpoint=False)
    # Snappy 90s clap bursts + snare noise
    noise = (np.random.rand(s_samples) * 2.0 - 1.0)
    # Multi-tap clap transient in first 30ms
    clap_env = np.exp(-st * 18.0)
    for tap in [0.008, 0.018, 0.028]:
        tap_idx = int(tap * SAMPLE_RATE)
        if tap_idx < s_samples:
            clap_env[tap_idx:] += np.exp(-(st[tap_idx:] - tap) * 25.0) * 0.5
    # Tonal body at 210 Hz
    tone = np.sin(2 * np.pi * 210 * st) * np.exp(-st * 30.0)
    snd = (noise * clap_env * 0.70 + tone * 0.30) * 0.75
    return np.clip(snd, -0.9, 0.9)

def make_909_hat(open_hat=False):
    h_dur = 0.20 if open_hat else 0.045
    h_samples = int(h_dur * SAMPLE_RATE)
    ht = np.linspace(0, h_dur, h_samples, endpoint=False)
    decay = 14.0 if open_hat else 70.0
    env = np.exp(-ht * decay)
    f1 = np.sin(2 * np.pi * 3700 * ht)
    f2 = np.sin(2 * np.pi * 5400 * ht)
    f3 = np.sin(2 * np.pi * 7800 * ht)
    noise = (np.random.rand(h_samples) * 2.0 - 1.0)
    metallic = (f1 * f2 + f3 + noise * 1.5) * 0.4
    snd = metallic * env * (0.32 if open_hat else 0.16)
    return np.clip(snd, -0.8, 0.8)

def make_909_crash():
    c_dur = 2.0
    c_samples = int(c_dur * SAMPLE_RATE)
    ct = np.linspace(0, c_dur, c_samples, endpoint=False)
    env = np.exp(-ct * 3.5)
    noise = (np.random.rand(c_samples) * 2.0 - 1.0)
    snd = noise * env * 0.28
    return np.clip(snd, -0.7, 0.7)

kick_snd = make_909_kick()
snare_snd = make_909_snare_clap()
hat_closed = make_909_hat(open_hat=False)
hat_open = make_909_hat(open_hat=True)
crash_snd = make_909_crash()

def add_audio(start_s, snd, pan=0.0, vol=1.0):
    idx = int(start_s * SAMPLE_RATE)
    if idx >= TOTAL_SAMPLES or idx + len(snd) <= 0:
        return
    s_idx = max(0, idx)
    snd_start = max(0, -idx)
    s_end = min(TOTAL_SAMPLES, idx + len(snd))
    snd_end = snd_start + (s_end - s_idx)
    
    l_vol = vol * np.sqrt(0.5 * (1.0 - pan))
    r_vol = vol * np.sqrt(0.5 * (1.0 + pan))
    
    left[s_idx:s_end] += snd[snd_start:snd_end] * l_vol
    right[s_idx:s_end] += snd[snd_start:snd_end] * r_vol

# Build Drum Groove across all bars
num_bars = int(DURATION / BAR_DUR) + 2
for bar in range(num_bars):
    b_start = bar * BAR_DUR
    if b_start >= DURATION:
        break
    
    # Crash on section beginnings (bars 1, 9, 17, 25)
    if bar in [0, 8, 16, 24]:
        add_audio(b_start, crash_snd, pan=0.1, vol=0.85)

    # 4-on-the-floor kick
    for beat in range(4):
        k_time = b_start + beat * BEAT_DUR
        add_audio(k_time, kick_snd, pan=0.0, vol=0.95)

    # Snare/Clap on beats 2 and 4 (beats 1 and 3 in 0-indexed)
    add_audio(b_start + 1 * BEAT_DUR, snare_snd, pan=0.05, vol=0.85)
    add_audio(b_start + 3 * BEAT_DUR, snare_snd, pan=-0.05, vol=0.85)

    # Open hi-hat on every 8th offbeat (essential Eurodance bounce)
    for beat in range(4):
        offbeat = b_start + beat * BEAT_DUR + EIGHTH
        add_audio(offbeat, hat_open, pan=0.25, vol=0.65)

    # Rolling 16th closed hats with velocity dynamics
    for sixteenth in range(16):
        h_time = b_start + sixteenth * SIXTEENTH
        if sixteenth % 2 == 0:
            add_audio(h_time, hat_closed, pan=-0.25, vol=0.35)
        elif (sixteenth % 4) != 2:
            add_audio(h_time, hat_closed, pan=-0.20, vol=0.22)

# ==============================================================================
# 2. PUMPING EURODANCE ROLLING BASSLINE (Octave Bounces)
# ==============================================================================
def render_euro_bass(root_low, root_high, dur=0.16):
    s_cnt = int(dur * SAMPLE_RATE)
    t = np.linspace(0, dur, s_cnt, endpoint=False)
    f_low = midi_to_freq(root_low)
    f_high = midi_to_freq(root_high)
    
    env = np.exp(-t * 22.0)
    saw1 = 2.0 * (t * f_low - np.floor(t * f_low + 0.5))
    saw2 = 2.0 * (t * (f_low * 1.004) - np.floor(t * (f_low * 1.004) + 0.5))
    sq = np.sign(np.sin(2 * np.pi * f_low * t))
    oct_saw = 2.0 * (t * f_high - np.floor(t * f_high + 0.5)) * 0.45
    
    snd = (saw1 * 0.4 + saw2 * 0.3 + sq * 0.35 + oct_saw) * env * 0.85
    return np.clip(snd, -0.9, 0.9)

chord_sequence = [
    (G1, G2),   # Gm (bars 0-1)
    (BB1, BB2), # Bb (bars 2-3)
    (EB2, EB3), # Eb (bars 4-5)
    (F2, F3),   # F  (bars 6-7)
]

for bar in range(num_bars):
    b_start = bar * BAR_DUR
    if b_start >= DURATION:
        break
    
    prog_idx = (bar // 2) % len(chord_sequence)
    r_low, r_high = chord_sequence[prog_idx]
    
    bass_snd_low = render_euro_bass(r_low, r_high, dur=SIXTEENTH * 0.95)
    bass_snd_high = render_euro_bass(r_high, r_high + 12, dur=SIXTEENTH * 0.95)
    
    for s_idx in range(16):
        note_time = b_start + s_idx * SIXTEENTH
        if s_idx in [2, 6, 10, 14]:
            add_audio(note_time, bass_snd_high, pan=0.0, vol=0.82)
        else:
            add_audio(note_time, bass_snd_low, pan=0.0, vol=0.92)

# ==============================================================================
# 3. KORG M1 HOUSE ORGAN CHORD STABS (Syncopated Upbeats)
# ==============================================================================
def render_m1_organ_chord(chord_midis, dur=0.28):
    s_cnt = int(dur * SAMPLE_RATE)
    t = np.linspace(0, dur, s_cnt, endpoint=False)
    env = np.exp(-t * 16.0)
    
    wave_acc = np.zeros(s_cnt, dtype=np.float32)
    for m in chord_midis:
        freq = midi_to_freq(m)
        h1 = np.sin(2 * np.pi * freq * t)
        h2 = np.sin(2 * np.pi * freq * 2.0 * t) * 0.65
        h3 = np.sin(2 * np.pi * freq * 3.0 * t) * 0.25
        h4 = np.sin(2 * np.pi * freq * 4.0 * t) * 0.40 * np.exp(-t * 40.0)
        wave_acc += (h1 + h2 + h3 + h4)
        
    wave_acc = (wave_acc / len(chord_midis)) * env * 0.75
    return np.clip(wave_acc, -0.85, 0.85)

chord_notes_map = [
    [G3, BB3, D4, G4],   # Gm
    [F3, BB3, D4, F4],   # Bb
    [G3, BB3, EB4, G4],  # Eb
    [F3, A3, C4, F4],    # F
]

for bar in range(num_bars):
    b_start = bar * BAR_DUR
    if b_start >= DURATION:
        break
    
    prog_idx = (bar // 2) % len(chord_notes_map)
    ch_notes = chord_notes_map[prog_idx]
    ch_snd = render_m1_organ_chord(ch_notes, dur=0.24)
    
    stabs_beats = [0.5, 1.0, 2.5, 3.0]
    for sb in stabs_beats:
        t_stab = b_start + sb * BEAT_DUR
        add_audio(t_stab, ch_snd, pan=-0.2, vol=0.68)
        add_audio(t_stab + 0.008, ch_snd, pan=0.2, vol=0.65)

# ==============================================================================
# 4. ICONIC LEAD SYNTH ("WHAT IS LOVE")
# ==============================================================================
def render_lead_note(midi_pitch, dur):
    s_cnt = int(dur * SAMPLE_RATE)
    t = np.linspace(0, dur, s_cnt, endpoint=False)
    freq = midi_to_freq(midi_pitch)
    
    attack = int(0.015 * SAMPLE_RATE)
    decay = int(0.08 * SAMPLE_RATE)
    env = np.ones(s_cnt, dtype=np.float32)
    if attack > 0:
        env[:attack] = np.linspace(0.0, 1.0, attack)
    if attack + decay < s_cnt:
        env[attack:attack+decay] = np.linspace(1.0, 0.82, decay)
        env[attack+decay:] = np.linspace(0.82, 0.65, s_cnt - attack - decay)
    rel_len = min(int(0.04 * SAMPLE_RATE), s_cnt)
    if rel_len > 0:
        env[-rel_len:] *= np.linspace(1.0, 0.0, rel_len)
        
    vibrato = np.sin(2 * np.pi * 5.5 * t) * 0.006 * np.clip((t - 0.2) * 5.0, 0.0, 1.0)
    mod_freq = freq * (1.0 + vibrato)
    phase = 2 * np.pi * np.cumsum(mod_freq) / SAMPLE_RATE
    
    saw1 = 2.0 * (phase / (2 * np.pi) - np.floor(phase / (2 * np.pi) + 0.5))
    saw2 = 2.0 * (phase * 1.006 / (2 * np.pi) - np.floor(phase * 1.006 / (2 * np.pi) + 0.5))
    sq1 = np.sign(np.sin(phase * 0.5)) * 0.25
    
    snd = (saw1 * 0.50 + saw2 * 0.40 + sq1) * env * 0.85
    return np.clip(snd, -0.9, 0.9)

lead_theme = [
    (0.0, BB4, BEAT_DUR * 0.9),
    (0.5 * BEAT_DUR, A4, BEAT_DUR * 0.8),
    (1.0 * BEAT_DUR, G4, BEAT_DUR * 1.2),
    (2.0 * BEAT_DUR, D4, BEAT_DUR * 2.2),
    (4.5 * BEAT_DUR, D4, BEAT_DUR * 0.8),
    (5.0 * BEAT_DUR, F4, BEAT_DUR * 0.8),
    (5.5 * BEAT_DUR, G4, BEAT_DUR * 1.8),
    
    (8.0 * BEAT_DUR, BB4, BEAT_DUR * 0.9),
    (8.5 * BEAT_DUR, A4, BEAT_DUR * 0.8),
    (9.0 * BEAT_DUR, G4, BEAT_DUR * 1.2),
    (10.0 * BEAT_DUR, F4, BEAT_DUR * 2.2),
    (12.5 * BEAT_DUR, D4, BEAT_DUR * 0.8),
    (13.0 * BEAT_DUR, F4, BEAT_DUR * 0.8),
    (13.5 * BEAT_DUR, G4, BEAT_DUR * 1.8),

    (16.0 * BEAT_DUR, G4, BEAT_DUR * 0.9),
    (16.5 * BEAT_DUR, F4, BEAT_DUR * 0.8),
    (17.0 * BEAT_DUR, EB4, BEAT_DUR * 1.2),
    (18.0 * BEAT_DUR, D4, BEAT_DUR * 2.2),
    (20.5 * BEAT_DUR, D4, BEAT_DUR * 0.8),
    (21.0 * BEAT_DUR, F4, BEAT_DUR * 0.8),
    (21.5 * BEAT_DUR, G4, BEAT_DUR * 1.8),

    (24.0 * BEAT_DUR, D4, BEAT_DUR * 0.9),
    (24.5 * BEAT_DUR, F4, BEAT_DUR * 0.9),
    (25.0 * BEAT_DUR, G4, BEAT_DUR * 2.8),
    (28.0 * BEAT_DUR, F4, BEAT_DUR * 1.5),
    (29.5 * BEAT_DUR, G4, BEAT_DUR * 2.2),
]

theme_duration = 8 * BAR_DUR

for rep in range(6):
    rep_offset = rep * theme_duration
    if rep_offset >= DURATION:
        break
    for (rel_t, pitch, d) in lead_theme:
        abs_t = rep_offset + rel_t
        if abs_t + d < DURATION:
            snd = render_lead_note(pitch, d)
            add_audio(abs_t, snd, pan=0.0, vol=0.88)
            add_audio(abs_t + 0.18, snd * 0.32, pan=-0.35, vol=0.55)
            add_audio(abs_t + 0.36, snd * 0.16, pan=0.35, vol=0.40)

# ==============================================================================
# 5. MASTERING (Normalization, Limiter, Fade out)
# ==============================================================================
fade_len = int(2.5 * SAMPLE_RATE)
fade_env = np.linspace(1.0, 0.0, fade_len)
left[-fade_len:] *= fade_env
right[-fade_len:] *= fade_env

left_master = np.tanh(left * 0.72)
right_master = np.tanh(right * 0.72)

peak = max(np.max(np.abs(left_master)), np.max(np.abs(right_master)))
if peak > 0:
    left_master = (left_master / peak) * 0.94
    right_master = (right_master / peak) * 0.94

left_int16 = (left_master * 32767.0).astype(np.int16)
right_int16 = (right_master * 32767.0).astype(np.int16)

interleaved = np.empty((TOTAL_SAMPLES * 2,), dtype=np.int16)
interleaved[0::2] = left_int16
interleaved[1::2] = right_int16

out_path = "video/soundtrack_what_is_love_85s.wav"
with wave.open(out_path, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(interleaved.tobytes())

print(f"Successfully generated 85-second Eurodance 'What Is Love' soundtrack: {out_path}")
