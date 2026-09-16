import numpy as np
import wave
import struct

SAMPLE_RATE = 44100
DURATION = 60.0
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION)
BPM = 168.0
BEAT_DUR = 60.0 / BPM          # 0.357142857 s
SIXTEENTH = BEAT_DUR / 4.0      # 0.089285714 s
EIGHTH = BEAT_DUR / 2.0         # 0.178571428 s
BAR_DUR = BEAT_DUR * 4.0        # 1.428571428 s

left = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
right = np.zeros(TOTAL_SAMPLES, dtype=np.float32)

def midi_to_freq(m):
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))

# MIDI Note Numbers
NOTE_B1 = 35
NOTE_E1 = 28
NOTE_A1 = 33
NOTE_D2 = 38
NOTE_G1 = 31
NOTE_FSH1 = 30

NOTE_B2 = 47
NOTE_E2 = 40
NOTE_A2 = 45
NOTE_D3 = 50
NOTE_G2 = 43
NOTE_FSH2 = 42

NOTE_GSH3 = 56
NOTE_A3 = 57
NOTE_B3 = 59
NOTE_CS4 = 61
NOTE_D4 = 62
NOTE_E4 = 64
NOTE_FSH4 = 66
NOTE_G4 = 67
NOTE_GSH4 = 68
NOTE_A4 = 69
NOTE_B4 = 71
NOTE_CS5 = 73
NOTE_D5 = 74
NOTE_E5 = 76
NOTE_FSH5 = 78

# ==============================================================================
# 1. LINNDRUM RHYTHM SECTION (Authentic Take On Me Drum Machine)
# ==============================================================================
num_bars = int(DURATION / BAR_DUR) + 1

# Pre-generate LinnDrum samples
def make_linn_kick():
    k_dur = 0.16
    k_samples = int(k_dur * SAMPLE_RATE)
    kt = np.linspace(0, k_dur, k_samples, endpoint=False)
    # Pitch drop from 180Hz down to 52Hz with quick transient click
    k_pitch = 180.0 * np.exp(-kt * 45.0) + 52.0
    k_phase = 2 * np.pi * np.cumsum(k_pitch) / SAMPLE_RATE
    body = np.sin(k_phase) * np.exp(-kt * 22.0)
    # Transient click (first 10ms)
    click = np.sin(2 * np.pi * 1200 * kt) * np.exp(-kt * 300.0)
    snd = (body * 0.85 + click * 0.35) * 0.85
    return np.clip(snd, -0.9, 0.9)

def make_linn_snare():
    s_dur = 0.22
    s_samples = int(s_dur * SAMPLE_RATE)
    st = np.linspace(0, s_dur, s_samples, endpoint=False)
    # Gated white noise
    noise = (np.random.rand(s_samples) * 2.0 - 1.0) * np.exp(-st * 15.0)
    # Resonant body tone around 220Hz
    body = np.sin(2 * np.pi * 220 * st) * np.exp(-st * 28.0)
    snd = (noise * 0.65 + body * 0.40) * 0.72
    return np.clip(snd, -0.85, 0.85)

def make_hihat(open_hat=False):
    h_dur = 0.14 if open_hat else 0.04
    h_samples = int(h_dur * SAMPLE_RATE)
    ht = np.linspace(0, h_dur, h_samples, endpoint=False)
    decay = 18.0 if open_hat else 80.0
    env = np.exp(-ht * decay)
    # Metallic high frequency noise
    noise = (np.random.rand(h_samples) * 2.0 - 1.0)
    # Bandpass/Highpass simulation
    h_snd = (noise * env) * (0.28 if open_hat else 0.18)
    return h_snd

def make_tambourine():
    t_dur = 0.08
    t_samples = int(t_dur * SAMPLE_RATE)
    tt = np.linspace(0, t_dur, t_samples, endpoint=False)
    env = np.exp(-tt * 40.0)
    t_snd = (np.random.rand(t_samples) * 2.0 - 1.0) * env * 0.16
    return t_snd

kick_raw = make_linn_kick()
snare_raw = make_linn_snare()
hh_closed = make_hihat(open_hat=False)
hh_open = make_hihat(open_hat=True)
tamb_raw = make_tambourine()

def add_sound(snd, start_t, pan=0.5, vol=1.0):
    idx = int(start_t * SAMPLE_RATE)
    s_len = len(snd)
    if idx + s_len >= TOTAL_SAMPLES:
        s_len = TOTAL_SAMPLES - idx
    if idx < 0 or s_len <= 0:
        return
    left[idx:idx+s_len] += snd[:s_len] * (1.0 - pan) * vol
    right[idx:idx+s_len] += snd[:s_len] * pan * vol

for bar in range(num_bars):
    b_start = bar * BAR_DUR
    
    # 1. Kicks: Beat 1, Beat 3, Beat 3.5 (Syncopated "and" of 3)
    add_sound(kick_raw, b_start + 0.0 * BEAT_DUR, pan=0.5, vol=0.95)
    add_sound(kick_raw, b_start + 2.0 * BEAT_DUR, pan=0.5, vol=0.88)
    add_sound(kick_raw, b_start + 2.5 * BEAT_DUR, pan=0.5, vol=0.92) # The signature syncopation!

    # 2. Snares: Beat 2, Beat 4 (With gated stereo tail)
    add_sound(snare_raw, b_start + 1.0 * BEAT_DUR, pan=0.48, vol=0.85)
    add_sound(snare_raw, b_start + 3.0 * BEAT_DUR, pan=0.52, vol=0.88)

    # 3. Tambourine on Beats 2 and 4
    add_sound(tamb_raw, b_start + 1.0 * BEAT_DUR, pan=0.7, vol=0.7)
    add_sound(tamb_raw, b_start + 3.0 * BEAT_DUR, pan=0.7, vol=0.7)

    # 4. Hi-Hats: 16ths across all 4 beats
    for s in range(16):
        s_time = b_start + s * SIXTEENTH
        # Open hi-hat on 14 (the "and" of 4) before next bar!
        if s == 14:
            add_sound(hh_open, s_time, pan=0.35, vol=0.9)
        elif s % 2 == 0:
            add_sound(hh_closed, s_time, pan=0.40, vol=0.75) # 8th note accent
        else:
            add_sound(hh_closed, s_time, pan=0.45, vol=0.45) # 16th ghost note

# ==============================================================================
# 2. YAMAHA DX7 + MINIMOOG BOUNCING BASSLINE (Staccato Octaves)
# ==============================================================================
def play_dx7_bass(midi_pitch, start_t, dur, vol=0.38):
    idx = int(start_t * SAMPLE_RATE)
    s_len = int(dur * SAMPLE_RATE)
    if idx + s_len >= TOTAL_SAMPLES:
        s_len = TOTAL_SAMPLES - idx
    if s_len <= 0:
        return
    f = midi_to_freq(midi_pitch)
    bt = np.linspace(0, dur, s_len, endpoint=False)
    # DX7 Solid Bass emulation: FM modulation (Carrier f, Modulator 2f)
    mod_env = np.exp(-bt * 18.0)
    modulator = 1.8 * np.sin(2 * np.pi * (2 * f) * bt) * mod_env
    carrier = np.sin(2 * np.pi * f * bt + modulator)
    
    # Minimoog analog sub-thump (sawtooth)
    analog_saw = 2.0 * (f * bt % 1.0) - 1.0
    
    amp_env = np.exp(-bt * 12.0) * (1.0 - np.exp(-bt * 300.0))
    snd = (carrier * 0.70 + analog_saw * 0.30) * amp_env * vol
    left[idx:idx+s_len] += snd * 0.88
    right[idx:idx+s_len] += snd * 0.88

# Chord progression in 8-bar cycles:
# Verse: Bm (2 bars) -> E (2 bars) -> A (2 bars) -> D (1 bar) -> F#m (1 bar)
# Chorus (from bar 20 onwards): D (2 bars) -> A (2 bars) -> Bm (2 bars) -> G (2 bars)
verse_bass_chords = [
    (NOTE_B1, 8),    # Bm (2 bars = 8 beats)
    (NOTE_E1, 8),    # E  (2 bars)
    (NOTE_A1, 8),    # A  (2 bars)
    (NOTE_D2, 4),    # D  (1 bar)
    (NOTE_FSH1, 4)   # F#m(1 bar)
]

total_beats = int(DURATION / BEAT_DUR)
cur_b = 0
while cur_b < total_beats:
    for root, num_b in verse_bass_chords:
        for b in range(num_b):
            if cur_b >= total_beats:
                break
            b_t = cur_b * BEAT_DUR
            # 8th note bouncing octave: Root on beat, Octave (+12) on upbeat
            play_dx7_bass(root, b_t, EIGHTH * 0.85, vol=0.40)
            play_dx7_bass(root + 12, b_t + EIGHTH, EIGHTH * 0.80, vol=0.35)
            cur_b += 1

# ==============================================================================
# 3. ROLAND JUNO-60 CHORDS + ACOUSTIC GUITAR 16th STRUMS
# ==============================================================================
def play_juno_stab(notes, start_t, dur, vol=0.18):
    idx = int(start_t * SAMPLE_RATE)
    s_len = int(dur * SAMPLE_RATE)
    if idx + s_len >= TOTAL_SAMPLES:
        s_len = TOTAL_SAMPLES - idx
    if s_len <= 0:
        return
    ct = np.linspace(0, dur, s_len, endpoint=False)
    env = np.exp(-ct * 7.0) * (1.0 - np.exp(-ct * 150.0))
    sig_l = np.zeros(s_len, dtype=np.float32)
    sig_r = np.zeros(s_len, dtype=np.float32)
    for n in notes:
        f = midi_to_freq(n)
        # Roland Juno dual saw with chorus detune
        saw1 = 2.0 * ((f * 0.998) * ct % 1.0) - 1.0
        saw2 = 2.0 * ((f * 1.002) * ct % 1.0) - 1.0
        sig_l += saw1 * 0.5
        sig_r += saw2 * 0.5
    left[idx:idx+s_len] += sig_l * env * vol
    right[idx:idx+s_len] += sig_r * env * vol

def play_acoustic_strum(start_t, vol=0.12):
    idx = int(start_t * SAMPLE_RATE)
    s_len = int(0.06 * SAMPLE_RATE)
    if idx + s_len >= TOTAL_SAMPLES:
        return
    st = np.linspace(0, 0.06, s_len, endpoint=False)
    env = np.exp(-st * 60.0)
    # High-passed acoustic pluck noise + metallic ring
    snd = (np.random.rand(s_len) * 2.0 - 1.0) * env * vol
    left[idx:idx+s_len] += snd * 0.65
    right[idx:idx+s_len] += snd * 0.35

chord_defs = [
    ([NOTE_B3, NOTE_D4, NOTE_FSH4], 8),     # Bm
    ([56, NOTE_B3, NOTE_E4], 8),     # E
    ([NOTE_A3, NOTE_CS4, NOTE_E4], 8),      # A
    ([NOTE_A3, NOTE_D4, NOTE_FSH4], 4),     # D
    ([NOTE_A3, NOTE_CS4, NOTE_FSH4], 4)     # F#m
]

chord_b = 0
while chord_b < total_beats:
    for notes, num_b in chord_defs:
        for b in range(num_b):
            if chord_b >= total_beats:
                break
            b_t = chord_b * BEAT_DUR
            # Juno stab on the offbeat (8th note)
            play_juno_stab(notes, b_t + EIGHTH, EIGHTH * 1.2, vol=0.18)
            # Acoustic guitar strumming on 16th notes (chicka-chicka)
            for s in range(4):
                play_acoustic_strum(b_t + s * SIXTEENTH, vol=0.08)
            chord_b += 1

# ==============================================================================
# 4. THE AUTHENTIC PPG WAVE / JUNO-60 KEYBOARD RIFF
# ==============================================================================
# Exact sheet music transcription of the 4-bar Take On Me synth hook:
# Sixteenth note indexing across the 64 sixteenths (4 bars):
riff_notes = [
    # Bar 1 (Bm): F#4, F#, D, B, -, B, -, E, -, E, -, E, G#, G#, A, B
    (NOTE_FSH4, 0, 1.8),
    (NOTE_FSH4, 2, 1.8),
    (NOTE_D4, 4, 1.8),
    (NOTE_B3, 6, 2.2),
    (NOTE_B3, 9, 1.4),
    (NOTE_E4, 11, 1.8),
    (NOTE_E4, 13, 1.2),
    (NOTE_E4, 14, 0.9),
    (NOTE_GSH4, 15, 1.0),
    # Bar 2 (E): G#, A, B, A, -, A, A, E, -, D, -, F#, -, F#, F#, E
    (NOTE_GSH4, 16, 1.0),
    (NOTE_A4, 17, 1.0),
    (NOTE_B4, 18, 1.8),
    (NOTE_A4, 20, 1.8),
    (NOTE_A4, 22, 1.0),
    (NOTE_A4, 23, 1.0),
    (NOTE_E4, 24, 1.8),
    (NOTE_D4, 26, 1.8),
    (NOTE_FSH4, 28, 1.8),
    (NOTE_FSH4, 30, 1.0),
    (NOTE_FSH4, 31, 0.9),
    # Bar 3 (A): F#, E, -, E, -, F#, -, E, -, D, -, B, -
    (NOTE_FSH4, 32, 1.8),
    (NOTE_E4, 34, 1.8),
    (NOTE_E4, 36, 1.8),
    (NOTE_FSH4, 38, 1.8),
    (NOTE_E4, 40, 2.6),
    (NOTE_D4, 43, 1.4),
    (NOTE_B3, 45, 2.6),
    # Bar 4 (D -> F#m turnaround back into the loop)
    (NOTE_CS4, 48, 1.8),
    (NOTE_D4, 50, 1.8),
    (NOTE_E4, 52, 2.0),
    (NOTE_FSH4, 56, 2.0),
    (NOTE_A4, 60, 2.8)
]

def play_take_on_me_lead(midi_pitch, start_t, dur, vol=0.34):
    idx = int(start_t * SAMPLE_RATE)
    s_len = int(dur * SAMPLE_RATE)
    if idx + s_len >= TOTAL_SAMPLES:
        s_len = TOTAL_SAMPLES - idx
    if s_len <= 0:
        return
    f = midi_to_freq(midi_pitch)
    lt = np.linspace(0, dur, s_len, endpoint=False)
    
    # Filter envelope: snappy attack, resonant cutoff sweep (Juno-60 / PPG)
    filt_env = np.exp(-lt * 12.0)
    # 40% Pulse + Saw + Sub
    phase = (f * lt) % 1.0
    pulse = np.where(phase < 0.40, 1.0, -1.0)
    saw = 2.0 * phase - 1.0
    sub = np.sin(2 * np.pi * (f * 0.5) * lt)
    
    amp_env = np.exp(-lt * 8.5) * (1.0 - np.exp(-lt * 500.0))
    raw_synth = (pulse * 0.50 + saw * 0.35 + sub * 0.15) * amp_env * vol
    
    # Roland Stereo Chorus simulation
    left[idx:idx+s_len] += raw_synth * 0.85
    right[idx:idx+s_len] += raw_synth * 0.75
    
    # 8th-note stereo ping-pong delay tap
    delay_s = int(EIGHTH * SAMPLE_RATE)
    if idx + delay_s + s_len < TOTAL_SAMPLES:
        d_idx = idx + delay_s
        left[d_idx:d_idx+s_len] += raw_synth * 0.18
        right[d_idx:d_idx+s_len] += raw_synth * 0.32

# Play the iconic riff across the 60s
riff_dur_s = 64 * SIXTEENTH # 16 beats = ~5.714 seconds
num_riff_loops = int(DURATION / riff_dur_s) + 1

for loop in range(num_riff_loops):
    loop_start_s = loop * 64
    for pitch, s_offset, dur_s in riff_notes:
        note_time = (loop_start_s + s_offset) * SIXTEENTH
        if note_time < DURATION - 0.2:
            # Add upper octave doubling on loops 4, 5, 8 for extra energy!
            oct_boost = 12 if (loop in [4, 5, 8, 9]) else 0
            play_take_on_me_lead(pitch + oct_boost, note_time, dur_s * SIXTEENTH, vol=0.32)

# ==============================================================================
# 5. SOARING CHORUS HOOK ("Take on me... Take me on...") (from 28s onwards!)
# ==============================================================================
# The unmistakable Morten Harket soaring melody up to high F#5!
# "Take on me": A4, B4, D5, B4, F#5 (high!)
# "Take me on": A4, B4, D5, B4, E5 (high!)
# "I'll be gone": A4, B4, D5, B4, D5, C#5, B4, A4
chorus_vocals = [
    # Phrase 1: "Take on me"
    (NOTE_A4, 0.0, 0.8), (NOTE_B4, 1.0, 0.8), (NOTE_D5, 2.0, 0.8), (NOTE_B4, 3.0, 0.8), (NOTE_FSH5, 4.0, 3.5),
    # Phrase 2: "Take me on"
    (NOTE_A4, 8.0, 0.8), (NOTE_B4, 9.0, 0.8), (NOTE_D5, 10.0, 0.8), (NOTE_B4, 11.0, 0.8), (NOTE_E5, 12.0, 3.5),
    # Phrase 3: "I'll be gone"
    (NOTE_A4, 16.0, 0.8), (NOTE_B4, 17.0, 0.8), (NOTE_D5, 18.0, 0.8), (NOTE_B4, 19.0, 0.8),
    (NOTE_D5, 20.0, 1.0), (NOTE_CS5, 21.0, 1.0), (NOTE_B4, 22.0, 1.0), (NOTE_A4, 23.0, 1.8),
    # Phrase 4: "In a day or two"
    (NOTE_FSH4, 25.0, 1.0), (NOTE_A4, 26.0, 1.0), (NOTE_B4, 27.0, 1.0), (NOTE_D5, 28.0, 3.0)
]

def play_vocal_lead(midi_pitch, start_t, dur, vol=0.26):
    idx = int(start_t * SAMPLE_RATE)
    s_len = int(dur * SAMPLE_RATE)
    if idx + s_len >= TOTAL_SAMPLES:
        s_len = TOTAL_SAMPLES - idx
    if s_len <= 0:
        return
    f = midi_to_freq(midi_pitch)
    vt = np.linspace(0, dur, s_len, endpoint=False)
    # Warm sine + gentle vibrato
    vibrato = 1.0 + 0.008 * np.sin(2 * np.pi * 5.5 * vt) * np.minimum(vt / 0.3, 1.0)
    phase = 2 * np.pi * np.cumsum(f * vibrato) / SAMPLE_RATE
    carrier = np.sin(phase) + 0.3 * np.sin(2 * phase)
    
    # Soft vocal envelope
    env = np.minimum(vt / 0.04, 1.0) * np.exp(-vt * 0.8)
    snd = carrier * env * vol
    left[idx:idx+s_len] += snd * 0.8
    right[idx:idx+s_len] += snd * 0.8
    
    # Big hall reverb delay
    rev_s = int(0.24 * SAMPLE_RATE)
    if idx + rev_s + s_len < TOTAL_SAMPLES:
        left[idx+rev_s:idx+rev_s+s_len] += snd * 0.35
        right[idx+rev_s:idx+rev_s+s_len] += snd * 0.35

# Introduce the soaring chorus melody from 28.5s to 56s!
chorus_start_beat = int(28.5 / BEAT_DUR)
for pitch, b_offset, dur_b in chorus_vocals:
    note_t = (chorus_start_beat + b_offset) * BEAT_DUR
    if note_t + dur_b * BEAT_DUR < DURATION - 1.0:
        play_vocal_lead(pitch, note_t, dur_b * BEAT_DUR, vol=0.28)

# ==============================================================================
# 6. MASTERING, ANALOG TAPE WARMTH & FADES
# ==============================================================================
max_peak = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-6)
left = (left / max_peak) * 0.90
right = (right / max_peak) * 0.90

# Warm soft saturation (SSL Console warmth)
left = np.tanh(left * 1.12) * 0.88
right = np.tanh(right * 1.12) * 0.88

# Smooth fades
f_in = int(0.15 * SAMPLE_RATE)
left[:f_in] *= np.linspace(0.0, 1.0, f_in)
right[:f_in] *= np.linspace(0.0, 1.0, f_in)

f_out = int(1.2 * SAMPLE_RATE)
left[-f_out:] *= np.linspace(1.0, 0.0, f_out)
right[-f_out:] *= np.linspace(1.0, 0.0, f_out)

out_file = "video/soundtrack_take_on_me_60s.wav"
with wave.open(out_file, "w") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    stereo = np.empty((TOTAL_SAMPLES * 2,), dtype=np.int16)
    stereo[0::2] = (left * 32767.0).astype(np.int16)
    stereo[1::2] = (right * 32767.0).astype(np.int16)
    wf.writeframes(stereo.tobytes())

print(f"Generated Authentic 'Take On Me' Soundtrack: {out_file} (168 BPM, LinnDrum, DX7 Bass, Juno-60 Riff & Chorus Vocals)")
