import numpy as np
import wave

sample_rate = 44100
duration = 60.0  # 60 seconds
bpm = 118  # Modern Talking classic Euro Disco tempo
beat_dur = 60.0 / bpm
sixteenth = beat_dur / 4.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# -------------------------------------------------------------
# Key: G# minor / B Major (Classic Modern Talking "Cheri Cheri Lady")
# Chords:
# 1. G#m  (G#2=103.83, B2=123.47, D#3=155.56, G#3=207.65)
# 2. C#m  (C#2=69.30,  E2=82.41,  G#2=103.83, C#3=138.59)
# 3. F#   (F#2=92.50,  A#2=116.54, C#3=138.59, F#3=185.00)
# 4. B    (B2=123.47,  D#3=155.56, F#3=185.00, B3=246.94)
# -------------------------------------------------------------

chord_dur = beat_dur * 4.0  # 1 measure per chord
total_measures = int(duration / chord_dur) + 1

# -------------------------------------------------------------
# 1. ICONIC EURO-DISCO BASSLINE (Dieter Bohlen Octave Bass)
# 16th note galloping octave bass (Root, Octave, Octave, Octave...)
# -------------------------------------------------------------
bass = np.zeros_like(t)
total_16ths = int(duration / sixteenth)

roots = [103.83, 69.30, 92.50, 123.47]  # G#2, C#2, F#2, B2

for s in range(total_16ths):
    m_idx = (s // 16) % len(roots)
    r_freq = roots[m_idx]
    
    # Octave pattern: Root on beat, Octave on upbeats
    is_downbeat = (s % 2 == 0)
    b_freq = r_freq if is_downbeat else (r_freq * 2.0)
    
    t_start = s * sixteenth
    idx_s = int(t_start * sample_rate)
    idx_e = min(int((t_start + sixteenth) * sample_rate), len(t))
    ts = t[idx_s:idx_e] - t_start
    
    # Punchy analog sawtooth + round square sub
    saw = 2.0 * (ts * b_freq - np.floor(ts * b_freq + 0.5))
    sq = np.sign(np.sin(2 * np.pi * b_freq * ts))
    env_b = np.exp(-ts * 28.0)
    
    # Dieter Bohlen snappy filter punch
    tone = (0.65 * saw + 0.35 * sq) * env_b
    bass[idx_s:idx_e] += np.tanh(tone * 1.8) * 0.48

# -------------------------------------------------------------
# 2. DRUMS & PERCUSSION (LinnDrum / Simmons Euro-Disco Beat)
# 4-on-the-floor kick, snappy 80s snare on 2 & 4, open/closed hi-hats
# -------------------------------------------------------------
drums_l = np.zeros_like(t)
drums_r = np.zeros_like(t)
total_beats = int(duration / beat_dur)

for b in range(total_beats):
    t_beat = b * beat_dur
    ib_start = int(t_beat * sample_rate)
    
    # 1. Punchy Disco Kick on every beat
    k_len = int(0.20 * sample_rate)
    k_end = min(ib_start + k_len, len(t))
    tk = t[ib_start:k_end] - t_beat
    k_freq = 52.0 + 95.0 * np.exp(-tk * 36.0)
    kick = np.sin(2 * np.pi * np.cumsum(k_freq) / sample_rate) * np.exp(-tk * 15.0)
    drums_l[ib_start:k_end] += kick * 0.8
    drums_r[ib_start:k_end] += kick * 0.8
    
    # 2. Snappy Reverb Snare on beats 2 and 4
    if b % 2 == 1:
        s_len = int(0.26 * sample_rate)
        s_end = min(ib_start + s_len, len(t))
        tsn = t[ib_start:s_end] - t_beat
        pop = np.sin(2 * np.pi * 210.0 * np.exp(-tsn * 26.0) * tsn) * np.exp(-tsn * 20.0)
        noise = np.random.uniform(-1.0, 1.0, len(tsn)) * np.exp(-tsn * 12.0)
        snare = (0.4 * pop + 0.6 * noise) * 0.52
        drums_l[ib_start:s_end] += snare
        drums_r[ib_start:s_end] += snare
        
    # 3. 16th Hi-hats with open hi-hat on the "and" of each beat (Classic Euro-Disco!)
    for sub in range(4):
        t_hat = t_beat + sub * sixteenth
        if t_hat >= duration:
            break
        ih_s = int(t_hat * sample_rate)
        is_open = (sub == 2)
        h_len = int((0.14 if is_open else 0.04) * sample_rate)
        ih_e = min(ih_s + h_len, len(t))
        th = t[ih_s:ih_e] - t_hat
        
        decay_rate = 22.0 if is_open else 95.0
        h_vol = 0.28 if is_open else 0.16
        hat = np.random.uniform(-0.1, 0.1, len(th)) * np.exp(-th * decay_rate) * h_vol
        drums_l[ih_s:ih_e] += hat * 0.9
        drums_r[ih_s:ih_e] += hat * 1.1

# -------------------------------------------------------------
# 3. CHERI CHERI LADY SYNTH LEAD MELODY & HOOK
# -------------------------------------------------------------
lead_l = np.zeros_like(t)
lead_r = np.zeros_like(t)

G4s = 415.30  # G#4
B4  = 493.88  # B4
C5s = 554.37  # C#5
D5s = 622.25  # D#5
E5  = 659.25  # E5
F4s = 369.99  # F#4

melody_notes = [
    # Measure 1 (G#m): D#5 -> C#5 -> B4 -> G#4 -> D#5
    (0.0, D5s, 0.75), (0.75, C5s, 0.5), (1.25, B4, 0.75), (2.0, G4s, 1.0), (3.0, D5s, 1.0),
    # Measure 2 (C#m): E5 -> D#5 -> C#5 -> G#4 -> E5
    (4.0, E5, 0.75), (4.75, D5s, 0.5), (5.25, C5s, 0.75), (6.0, G4s, 1.0), (7.0, E5, 1.0),
    # Measure 3 (F#): D#5 -> C#5 -> B4 -> F#4 -> D#5
    (8.0, D5s, 0.75), (8.75, C5s, 0.5), (9.25, B4, 0.75), (10.0, F4s, 1.0), (11.0, D5s, 1.0),
    # Measure 4 (B -> G#m): B4 -> C#5 -> D#5 -> B4 -> G#4
    (12.0, B4, 0.75), (12.75, C5s, 0.5), (13.25, D5s, 0.75), (14.0, B4, 0.75), (15.0, G4s, 1.0)
]

melody_loop_dur = beat_dur * 16.0
total_melody_loops = int(duration / melody_loop_dur) + 1

for ml in range(total_melody_loops):
    base_t = ml * melody_loop_dur
    for off, freq, dur_b in melody_notes:
        t_note = base_t + off * beat_dur
        if t_note >= duration:
            break
        in_s = int(t_note * sample_rate)
        in_len = int(dur_b * beat_dur * sample_rate)
        in_e = min(in_s + in_len, len(t))
        tn = t[in_s:in_e] - t_note
        
        env_n = (1.0 - np.exp(-tn * 90.0)) * np.exp(-tn * 2.8)
        vib = 1.0 + 0.007 * np.sin(2 * np.pi * 5.8 * tn)
        s_saw = 2.0 * (tn * freq * vib - np.floor(tn * freq * vib + 0.5))
        s_sq = np.sign(np.sin(2 * np.pi * freq * vib * tn))
        
        lead_tone = (0.6 * s_saw + 0.4 * s_sq) * env_n * 0.28
        lead_l[in_s:in_e] += lead_tone * 0.85
        lead_r[in_s:in_e] += lead_tone * 1.15

# Add delay / echo (3/16th delay)
del_samples = int(sixteenth * 3 * sample_rate)
for d in range(1, 4):
    shift = d * del_samples
    if shift < len(t):
        lead_l[shift:] += lead_r[:-shift] * (0.32 ** d)
        lead_r[shift:] += lead_l[:-shift] * (0.32 ** d)

# -------------------------------------------------------------
# 4. EURO-DISCO BRASS CHORDS & STRINGS (Modern Talking Stabs)
# -------------------------------------------------------------
chords_l = np.zeros_like(t)
chords_r = np.zeros_like(t)

pad_chords = [
    [207.65, 246.94, 311.13], # G#m (G#3, B3, D#4)
    [138.59, 164.81, 207.65], # C#m (C#3, E3, G#3)
    [185.00, 233.08, 277.18], # F#  (F#3, A#3, C#4)
    [246.94, 311.13, 369.99]  # B   (B3, D#4, F#4)
]

for m in range(total_measures):
    c_tones = pad_chords[m % len(pad_chords)]
    for stab_off in [beat_dur * 1.0, beat_dur * 1.5, beat_dur * 3.0, beat_dur * 3.5]:
        t_st = m * chord_dur + stab_off
        if t_st >= duration:
            break
        ist_s = int(t_st * sample_rate)
        ist_len = int(0.28 * sample_rate)
        ist_e = min(ist_s + ist_len, len(t))
        tst = t[ist_s:ist_e] - t_st
        
        env_st = np.exp(-tst * 7.5) * np.sin(np.pi * np.clip(tst / 0.28, 0, 1))
        for ct in c_tones:
            stab_tone = np.sin(2 * np.pi * ct * tst) + 0.3 * np.sin(2 * np.pi * (ct * 2) * tst)
            chords_l[ist_s:ist_e] += stab_tone * env_st * 0.06
            chords_r[ist_s:ist_e] += stab_tone * env_st * 0.06

# -------------------------------------------------------------
# MASTER MIX & MODERN TALKING MASTERING
# -------------------------------------------------------------
mix_l = bass * 0.70 + drums_l * 0.75 + lead_l * 0.65 + chords_l * 0.50
mix_r = bass * 0.70 + drums_r * 0.75 + lead_r * 0.65 + chords_r * 0.50

# Fade in (1.0s) & Fade out (2.5s)
fade_in = np.linspace(0.0, 1.0, int(1.0 * sample_rate))
fade_out = np.linspace(1.0, 0.0, int(2.5 * sample_rate))
mix_l[:len(fade_in)] *= fade_in
mix_r[:len(fade_in)] *= fade_in
mix_l[-len(fade_out):] *= fade_out
mix_r[-len(fade_out):] *= fade_out

peak = max(np.max(np.abs(mix_l)), np.max(np.abs(mix_r)))
if peak > 0:
    target = 0.86
    mix_l = (mix_l / peak) * target
    mix_r = (mix_r / peak) * target

output_wav = "video/soundtrack_cheri_cheri_lady_60s.wav"
with wave.open(output_wav, 'w') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    interleaved = np.empty((len(t) * 2,), dtype=np.int16)
    interleaved[0::2] = (mix_l * 32767).astype(np.int16)
    interleaved[1::2] = (mix_r * 32767).astype(np.int16)
    wf.writeframes(interleaved.tobytes())

print(f"Generated Cheri Cheri Lady Soundtrack: {output_wav} (60s, 118 BPM, 44.1kHz stereo)")
