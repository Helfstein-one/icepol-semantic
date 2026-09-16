import numpy as np
import wave
import struct

SAMPLE_RATE = 44100
DURATION = 60.0
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION)
BPM = 168.0
BEAT_DUR = 60.0 / BPM  # ~0.35714 s
SIXTEENTH = BEAT_DUR / 4.0 # ~0.08928 s

t = np.linspace(0, DURATION, TOTAL_SAMPLES, endpoint=False)

# Left and right audio buffers
left = np.zeros(TOTAL_SAMPLES, dtype=np.float32)
right = np.zeros(TOTAL_SAMPLES, dtype=np.float32)

# Helper: Note to freq
def midi_to_freq(m):
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))

# Notes definitions (Key: B minor)
# B3=59, C#4=61, D4=62, E4=64, F#4=66, G#4=68, A4=69, B4=71, C#5=73, D5=74, E5=76, F#5=78
NOTE_B2 = 47
NOTE_E2 = 40
NOTE_A2 = 45
NOTE_D3 = 50
NOTE_G2 = 43
NOTE_FSH2 = 42

NOTE_B3 = 59
NOTE_CS4 = 61
NOTE_D4 = 62
NOTE_E4 = 64
NOTE_FSH4 = 66
NOTE_GSH4 = 68
NOTE_A4 = 69
NOTE_B4 = 71
NOTE_CS5 = 73
NOTE_D5 = 74
NOTE_E5 = 76
NOTE_FSH5 = 78

# --- 1. DRUMS (LinnDrum style @ 168 BPM) ---
num_beats = int(DURATION / BEAT_DUR)
for b in range(num_beats):
    beat_t = b * BEAT_DUR
    idx = int(beat_t * SAMPLE_RATE)
    
    # Kick: beats 1, 2, 3, 4 (pumping four-on-the-floor synth-pop)
    kick_len = int(0.18 * SAMPLE_RATE)
    if idx + kick_len < TOTAL_SAMPLES:
        kt = np.linspace(0, 0.18, kick_len, endpoint=False)
        k_env = np.exp(-kt * 28.0)
        k_freq = 150.0 * np.exp(-kt * 32.0) + 42.0
        k_phase = 2 * np.pi * np.cumsum(k_freq) / SAMPLE_RATE
        kick_sound = 0.55 * np.sin(k_phase) * k_env
        # slight punch distortion
        kick_sound = np.clip(kick_sound * 1.3, -0.6, 0.6)
        left[idx:idx+kick_len] += kick_sound
        right[idx:idx+kick_len] += kick_sound

    # Snare: beats 2 and 4 (punchy 80s gated snare)
    if b % 2 == 1:
        snare_len = int(0.20 * SAMPLE_RATE)
        if idx + snare_len < TOTAL_SAMPLES:
            st = np.linspace(0, 0.20, snare_len, endpoint=False)
            s_env = np.exp(-st * 18.0)
            noise = (np.random.rand(snare_len) * 2.0 - 1.0) * s_env
            body = np.sin(2 * np.pi * 210 * st) * np.exp(-st * 30.0)
            snare_sound = 0.38 * (noise * 0.75 + body * 0.45)
            left[idx:idx+snare_len] += snare_sound * 0.95
            right[idx:idx+snare_len] += snare_sound * 1.05

# 16th Hi-hats & Tambourine
num_sixteenths = int(DURATION / SIXTEENTH)
for s in range(num_sixteenths):
    st_time = s * SIXTEENTH
    idx = int(st_time * SAMPLE_RATE)
    hh_len = int(0.045 * SAMPLE_RATE)
    if idx + hh_len < TOTAL_SAMPLES:
        ht = np.linspace(0, 0.045, hh_len, endpoint=False)
        # Open hat on upbeats (s % 4 == 2)
        if s % 4 == 2:
            hh_env = np.exp(-ht * 22.0)
            vol = 0.22
        elif s % 2 == 0:
            hh_env = np.exp(-ht * 65.0)
            vol = 0.16
        else:
            hh_env = np.exp(-ht * 85.0)
            vol = 0.10
        hh_noise = (np.random.rand(hh_len) * 2.0 - 1.0) * hh_env * vol
        pan = 0.4 + 0.2 * np.sin(s * 0.7)
        left[idx:idx+hh_len] += hh_noise * pan
        right[idx:idx+hh_len] += hh_noise * (1.0 - pan)

# --- 2. BASSLINE (Staccato Octave Bouncing Synth Bass) ---
# Chord roots progression (each 2 bars = 8 beats):
# Bm (bars 1-2) -> E (bars 3-4) -> A (bars 5-6) -> D - F#m (bars 7-8)
# Repeated in 8-bar cycles: 8 * 4 * BEAT_DUR = 32 beats = ~11.43 seconds per cycle
def play_bass_note(midi_pitch, start_time, duration, vol=0.32):
    idx = int(start_time * SAMPLE_RATE)
    dur_samples = int(duration * SAMPLE_RATE)
    if idx + dur_samples >= TOTAL_SAMPLES:
        dur_samples = TOTAL_SAMPLES - idx
    if dur_samples <= 0:
        return
    freq = midi_to_freq(midi_pitch)
    bt = np.linspace(0, duration, dur_samples, endpoint=False)
    env = np.exp(-bt * 14.0) * (1.0 - np.exp(-bt * 300.0))
    # Sawtooth + sub-oscillator
    osc = 0.65 * (2.0 * (freq * bt % 1.0) - 1.0)
    sub = 0.45 * np.sin(2 * np.pi * (freq * 0.5) * bt)
    snd = (osc + sub) * env * vol
    left[idx:idx+dur_samples] += snd * 0.9
    right[idx:idx+dur_samples] += snd * 0.9

chord_patterns = [
    (NOTE_B2, 8),    # Bm (2 bars)
    (NOTE_E2, 8),    # E  (2 bars)
    (NOTE_A2, 8),    # A  (2 bars)
    (NOTE_D3, 4),    # D  (1 bar)
    (NOTE_FSH2, 4)   # F#m (1 bar)
] # Total 32 beats = 8 bars

total_beats = int(DURATION / BEAT_DUR)
current_beat = 0
while current_beat < total_beats:
    for root_pitch, num_b in chord_patterns:
        for b_in_chord in range(num_b):
            if current_beat >= total_beats:
                break
            b_time = current_beat * BEAT_DUR
            # 8th note bouncing octave: root on downbeat, +12 on upbeat
            play_bass_note(root_pitch, b_time, BEAT_DUR * 0.45, vol=0.36)
            play_bass_note(root_pitch + 12, b_time + BEAT_DUR * 0.5, BEAT_DUR * 0.42, vol=0.30)
            current_beat += 1

# --- 3. SYNTH PADS / CHORDS (Roland Juno Warm Brass/Pads) ---
def play_chord(notes, start_time, duration, vol=0.18):
    idx = int(start_time * SAMPLE_RATE)
    dur_samples = int(duration * SAMPLE_RATE)
    if idx + dur_samples >= TOTAL_SAMPLES:
        dur_samples = TOTAL_SAMPLES - idx
    if dur_samples <= 0:
        return
    ct = np.linspace(0, duration, dur_samples, endpoint=False)
    # Attack and release envelope
    env = np.minimum(ct / 0.05, 1.0) * np.minimum((duration - ct) / 0.08, 1.0)
    chord_sig_l = np.zeros(dur_samples, dtype=np.float32)
    chord_sig_r = np.zeros(dur_samples, dtype=np.float32)
    for n in notes:
        f = midi_to_freq(n)
        # Detuned saws for thick chorus
        saw1 = 2.0 * ((f * 0.998) * ct % 1.0) - 1.0
        saw2 = 2.0 * ((f * 1.002) * ct % 1.0) - 1.0
        chord_sig_l += saw1 * 0.5
        chord_sig_r += saw2 * 0.5
    left[idx:idx+dur_samples] += chord_sig_l * env * vol
    right[idx:idx+dur_samples] += chord_sig_r * env * vol

# Chords sequence matching the bass progression:
# Bm: [B3, D4, F#4]
# E:  [G#3, B3, E4]
# A:  [A3, C#4, E4]
# D:  [A3, D4, F#4]
# F#m:[A3, C#4, F#4]
chord_voicings = [
    ([59, 62, 66], 8), # Bm
    ([56, 59, 64], 8), # E
    ([57, 61, 64], 8), # A
    ([57, 62, 66], 4), # D
    ([57, 61, 66], 4)  # F#m
]

c_beat = 0
while c_beat < total_beats:
    for notes, num_b in chord_voicings:
        if c_beat >= total_beats:
            break
        # Play chord per bar (4 beats) with slight staccato groove
        for bar in range(num_b // 4):
            bar_start = (c_beat + bar * 4) * BEAT_DUR
            play_chord(notes, bar_start, BEAT_DUR * 3.8, vol=0.15)
        c_beat += num_b

# --- 4. THE ICONIC "TAKE ON ME" SYNTH LEAD HOOK ---
# Riff in B minor:
# Pattern (each note specified by (midi_pitch, sixteenth_index, sixteenth_duration)):
# Bar 1 (16 sixteenths):
# 0: F#4 (2), 2: F#4 (2), 4: D4 (2), 6: B3 (2), 9: B3 (1), 11: E4 (2), 13: E4 (1), 14: E4 (1), 15: G#4 (1)
# Bar 2 (16 sixteenths):
# 0: G#4 (1), 1: A4 (1), 2: B4 (2), 4: A4 (2), 6: A4 (1), 7: A4 (1), 8: E4 (2), 10: D4 (2), 12: F#4 (2), 14: F#4 (1), 15: F#4 (1)
# Bar 3 (16 sixteenths):
# 0: E4 (2), 2: E4 (2), 4: F#4 (2), 6: E4 (2) ...

take_on_me_riff = [
    # Bar 1
    (NOTE_FSH4, 0, 1.8),
    (NOTE_FSH4, 2, 1.8),
    (NOTE_D4, 4, 1.8),
    (NOTE_B3, 6, 2.4),
    (NOTE_B3, 9, 1.2),
    (NOTE_E4, 11, 1.8),
    (NOTE_E4, 13, 1.0),
    (NOTE_E4, 14, 0.9),
    (NOTE_GSH4, 15, 1.0),
    # Bar 2
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
    # Bar 3
    (NOTE_FSH4, 32, 1.8),
    (NOTE_E4, 34, 1.8),
    (NOTE_E4, 36, 1.8),
    (NOTE_FSH4, 38, 1.8),
    (NOTE_E4, 40, 2.5),
    (NOTE_D4, 43, 1.2),
    (NOTE_B3, 45, 2.5),
    # Bar 4 (lead-in back to top)
    (NOTE_CS4, 48, 1.8),
    (NOTE_D4, 50, 1.8),
    (NOTE_E4, 52, 2.0),
    (NOTE_FSH4, 56, 2.0),
    (NOTE_A4, 60, 2.5)
]

def play_lead_note(midi_pitch, start_time, duration, vol=0.28):
    idx = int(start_time * SAMPLE_RATE)
    dur_samples = int(duration * SAMPLE_RATE)
    if idx + dur_samples >= TOTAL_SAMPLES:
        dur_samples = TOTAL_SAMPLES - idx
    if dur_samples <= 0:
        return
    freq = midi_to_freq(midi_pitch)
    lt = np.linspace(0, duration, dur_samples, endpoint=False)
    # Bright snappy synth envelope
    env = np.exp(-lt * 8.0) * (1.0 - np.exp(-lt * 600.0))
    # Pulse wave (35% duty cycle) + Saw for signature Roland sound
    phase = (freq * lt) % 1.0
    pulse = np.where(phase < 0.35, 1.0, -1.0)
    saw = 2.0 * phase - 1.0
    synth = (pulse * 0.65 + saw * 0.35) * env * vol
    # Stereo panning + Ping Pong delay
    left[idx:idx+dur_samples] += synth * 0.85
    right[idx:idx+dur_samples] += synth * 0.75
    
    # 8th-note delay tap
    delay_samples = int(BEAT_DUR * 0.5 * SAMPLE_RATE)
    d_idx = idx + delay_samples
    if d_idx + dur_samples < TOTAL_SAMPLES:
        left[d_idx:d_idx+dur_samples] += synth * 0.35 * 0.4
        right[d_idx:d_idx+dur_samples] += synth * 0.35 * 0.8

# Play the Take On Me riff starting at 0s, repeating across the 60s
# One full 4-bar riff = 64 sixteenths = 16 beats = ~5.71 seconds
riff_dur_sixteenths = 64
total_riff_repeats = int((DURATION / SIXTEENTH) / riff_dur_sixteenths) + 1

for r in range(total_riff_repeats):
    base_sixteenth = r * riff_dur_sixteenths
    # In middle (bars 16-24), play higher octave for thrilling chorus energy!
    oct_shift = 12 if (r in [3, 4, 7, 8]) else 0
    vol = 0.32 if (r >= 2) else 0.28
    
    for pitch, s_offset, dur_s in take_on_me_riff:
        note_s = base_sixteenth + s_offset
        note_time = note_s * SIXTEENTH
        if note_time < DURATION - 0.2:
            play_lead_note(pitch + oct_shift, note_time, dur_s * SIXTEENTH, vol=vol)

# --- MASTERING / LIMITER ---
# Soft clipping & normalization
max_val = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-6)
left = (left / max_val) * 0.88
right = (right / max_val) * 0.88

# Soft clip saturation for punchy analog warmth
left = np.tanh(left * 1.15) * 0.86
right = np.tanh(right * 1.15) * 0.86

# Fade in (0.3s) and Fade out (1.0s)
fade_in_samples = int(0.3 * SAMPLE_RATE)
left[:fade_in_samples] *= np.linspace(0.0, 1.0, fade_in_samples)
right[:fade_in_samples] *= np.linspace(0.0, 1.0, fade_in_samples)

fade_out_samples = int(1.2 * SAMPLE_RATE)
left[-fade_out_samples:] *= np.linspace(1.0, 0.0, fade_out_samples)
right[-fade_out_samples:] *= np.linspace(1.0, 0.0, fade_out_samples)

# Write 16-bit PCM WAV
out_wav = "video/soundtrack_take_on_me_60s.wav"
with wave.open(out_wav, "w") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    
    # Interleave stereo
    stereo = np.empty((TOTAL_SAMPLES * 2,), dtype=np.int16)
    stereo[0::2] = (left * 32767.0).astype(np.int16)
    stereo[1::2] = (right * 32767.0).astype(np.int16)
    wf.writeframes(stereo.tobytes())

print(f"Generated soundtrack: {out_wav} (168 BPM A-ha 'Take On Me' style, 60.0s)")
