import numpy as np
import wave

sample_rate = 44100
duration = 40.0  # 40 seconds
bpm = 112
beat_dur = 60.0 / bpm
sixteenth = beat_dur / 4.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# -------------------------------------------------------------------
# Track 1: Upbeat / Funky Warm Rhodes Piano (Groovy 9th / 13th chords)
# Key: Eb Major / C minor (Warm, happy, uplifting & pleasant)
# 1. Ebmaj9 (Eb3=155.56, G3=196.00, Bb3=233.08, D4=293.66, F4=349.23)
# 2. Cm9    (C3=130.81,  Eb3=155.56, G3=196.00,  Bb3=233.08, D4=293.66)
# 3. Fm9    (F2=87.31,   C3=130.81,  Eb3=155.56, Ab3=207.65, C4=261.63)
# 4. Bb13   (Bb2=116.54, D3=146.83,  F3=174.61,  Ab3=207.65, G4=392.00)
# -------------------------------------------------------------------
rhodes_l = np.zeros_like(t)
rhodes_r = np.zeros_like(t)

chord_dur = beat_dur * 4.0  # 1 measure per chord
total_measures = int(duration / chord_dur) + 1

chords = [
    [155.56, 196.00, 233.08, 293.66, 349.23], # Ebmaj9
    [130.81, 155.56, 196.00, 233.08, 293.66], # Cm9
    [87.31,  130.81, 155.56, 207.65, 261.63], # Fm9
    [116.54, 146.83, 174.61, 207.65, 392.00]  # Bb13
]

# Upbeat funky syncopated comping rhythm (offsets in beats):
# Hit on beat 1 (0.0), beat 2.5 (1.5), beat 3.5 (2.5), beat 4.25 (3.25)
comp_offsets = [0.0, beat_dur * 1.5, beat_dur * 2.5, beat_dur * 3.25]
comp_lengths = [beat_dur * 1.2, beat_dur * 0.8, beat_dur * 0.6, beat_dur * 0.6]

for m in range(total_measures):
    chord = chords[m % len(chords)]
    for off, plen in zip(comp_offsets, comp_lengths):
        t_hit = m * chord_dur + off
        if t_hit >= duration:
            break
        i_start = int(t_hit * sample_rate)
        i_end = min(int((t_hit + plen) * sample_rate), len(t))
        th = t[i_start:i_end] - t_hit
        
        # Crisp Rhodes bell attack + smooth pleasant decay (no harsh clipping)
        env = (1.0 - np.exp(-th * 60.0)) * np.exp(-th * 3.5)

        for tone in chord:
            # Soft harmonics (pure, warm and energetic)
            s1 = np.sin(2 * np.pi * tone * th)
            s2 = 0.20 * np.sin(2 * np.pi * (tone * 2) * th)
            # Stereo chorus panning
            pan_l = 1.0 + 0.15 * np.sin(2 * np.pi * 4.2 * th)
            pan_r = 1.0 + 0.15 * np.sin(2 * np.pi * 4.2 * th + np.pi / 2)
            
            note_sig = (s1 + s2) * env * 0.13
            rhodes_l[i_start:i_end] += note_sig * pan_l
            rhodes_r[i_start:i_end] += note_sig * pan_r

# -------------------------------------------------------------------
# Track 2: Upbeat Funky Slap / Fingerstyle Bass (Groovy & Bouncy)
# Notes follow: Eb, C, F, Bb with lively walking octaves
# -------------------------------------------------------------------
bass = np.zeros_like(t)

bass_roots = [77.78, 65.41, 43.65, 58.27] # Eb2, C2, F1, Bb1

for m in range(total_measures):
    root = bass_roots[m % len(bass_roots)]
    # Funky bass pattern: 1, 2.5, 3, 3.75, 4.5
    b_pattern = [
        (0.0, root, beat_dur * 0.7),
        (beat_dur * 1.5, root * 2.0, beat_dur * 0.4), # octave bounce
        (beat_dur * 2.0, root, beat_dur * 0.6),
        (beat_dur * 3.0, root * (9.0/8.0), beat_dur * 0.4), # passing note
        (beat_dur * 3.5, root * (5.0/4.0), beat_dur * 0.4)
    ]
    for b_off, b_freq, b_len in b_pattern:
        t_b = m * chord_dur + b_off
        if t_b >= duration:
            break
        ib_s = int(t_b * sample_rate)
        ib_e = min(int((t_b + b_len) * sample_rate), len(t))
        tb = t[ib_s:ib_e] - t_b
        
        # Punchy round bass envelope
        env_b = (1.0 - np.exp(-tb * 50.0)) * np.exp(-tb * 4.5)
        # Sine fundamental + gentle 2nd harmonic for acoustic bite
        bw = (np.sin(2 * np.pi * b_freq * tb) + 0.3 * np.sin(2 * np.pi * b_freq * 2 * tb)) * env_b * 0.45
        bass[ib_s:ib_e] += bw

# -------------------------------------------------------------------
# Track 3: Energetic yet Soft Funky Groove Drums (112 BPM)
# Bouncy kick + crisp wooden snare rim + swing hi-hats
# -------------------------------------------------------------------
drums_l = np.zeros_like(t)
drums_r = np.zeros_like(t)
total_beats = int(duration / beat_dur)

for b in range(total_beats):
    t_beat = b * beat_dur
    ib_start = int(t_beat * sample_rate)

    # 1. Four-on-the-floor / funky syncopated kick (punchy but warm)
    # Kicks on 1, 2.5, 3
    is_kick = (b % 4 in [0, 2])
    if is_kick:
        k_len = int(0.22 * sample_rate)
        k_end = min(ib_start + k_len, len(t))
        tk = t[ib_start:k_end] - t_beat
        k_freq = 50.0 + 45.0 * np.exp(-tk * 28.0)
        k_phase = 2 * np.pi * np.cumsum(k_freq) / sample_rate
        kick_val = np.sin(k_phase) * np.exp(-tk * 14.0) * 0.58
        drums_l[ib_start:k_end] += kick_val
        drums_r[ib_start:k_end] += kick_val

    # Extra syncopated kick on the "and" of 2
    if b % 4 == 1:
        t_extra = t_beat + beat_dur * 0.5
        ie_start = int(t_extra * sample_rate)
        ie_end = min(ie_start + int(0.18 * sample_rate), len(t))
        te = t[ie_start:ie_end] - t_extra
        k_freq2 = 50.0 + 40.0 * np.exp(-te * 32.0)
        kick_extra = np.sin(2 * np.pi * np.cumsum(k_freq2) / sample_rate) * np.exp(-te * 16.0) * 0.48
        drums_l[ie_start:ie_end] += kick_extra
        drums_r[ie_start:ie_end] += kick_extra

    # 2. Crisp wooden snare on beats 2 and 4 (satisfying pop without harsh sizzle)
    if b % 2 == 1:
        s_len = int(0.14 * sample_rate)
        s_end = min(ib_start + s_len, len(t))
        ts = t[ib_start:s_end] - t_beat
        pop = np.sin(2 * np.pi * 320.0 * ts) * np.exp(-ts * 45.0)
        sn_noise = np.random.normal(0, 0.12, len(ts)) * np.exp(-ts * 30.0)
        snare_hit = (0.5 * pop + 0.5 * sn_noise) * 0.42
        drums_l[ib_start:s_end] += snare_hit
        drums_r[ib_start:s_end] += snare_hit

    # 3. Funky 16th-note swing hi-hats (shakers / muted cymbals)
    for s_idx in range(4):
        # Slight swing delay on the even 16ths
        swing = 0.02 * beat_dur if (s_idx % 2 == 1) else 0.0
        t_hat = t_beat + s_idx * sixteenth + swing
        if t_hat >= duration:
            break
        ih_start = int(t_hat * sample_rate)
        ih_len = int(0.04 * sample_rate)
        ih_end = min(ih_start + ih_len, len(t))
        th = t[ih_start:ih_end] - t_hat
        
        # Velocity accentuation (groove)
        accent = 0.26 if (s_idx in [0, 2]) else 0.16
        hat_wave = np.random.uniform(-0.1, 0.1, len(th)) * np.exp(-th * 95.0) * accent
        drums_l[ih_start:ih_end] += hat_wave * 0.95
        drums_r[ih_start:ih_end] += hat_wave * 1.05

# -------------------------------------------------------------------
# Track 4: Uplifting Brass / Synth Bells (Subtle Melody Highlights)
# -------------------------------------------------------------------
lead_l = np.zeros_like(t)
lead_r = np.zeros_like(t)

lead_notes = [587.33, 523.25, 466.16, 392.00, 466.16, 523.25] # D5, C5, Bb4, G4, Bb4, C5
for m in range(total_measures):
    for i, l_freq in enumerate(lead_notes):
        t_lead = m * chord_dur + i * (beat_dur * 0.6)
        if t_lead >= duration:
            break
        il_s = int(t_lead * sample_rate)
        il_e = min(il_s + int(0.35 * sample_rate), len(t))
        tl = t[il_s:il_e] - t_lead
        
        env_l = np.exp(-tl * 8.0) * np.sin(np.pi * np.clip(tl / 0.35, 0, 1))
        lead_sound = np.sin(2 * np.pi * l_freq * tl) * env_l * 0.08
        lead_l[il_s:il_e] += lead_sound * 0.8
        lead_r[il_s:il_e] += lead_sound * 1.2

# -------------------------------------------------------------------
# Master Mix Stereo & Smooth Dynamic Limiter
# -------------------------------------------------------------------
mix_l = rhodes_l * 0.70 + bass * 0.55 + drums_l * 0.65 + lead_l * 0.50
mix_r = rhodes_r * 0.70 + bass * 0.55 + drums_r * 0.65 + lead_r * 0.50

# Fade in (1.2s) and Fade out (2.0s)
fade_in = np.linspace(0.0, 1.0, int(1.2 * sample_rate))
fade_out = np.linspace(1.0, 0.0, int(2.0 * sample_rate))
mix_l[:len(fade_in)] *= fade_in
mix_r[:len(fade_in)] *= fade_in
mix_l[-len(fade_out):] *= fade_out
mix_r[-len(fade_out):] *= fade_out

# Peak limiter to comfortable -2dB ceiling
peak = max(np.max(np.abs(mix_l)), np.max(np.abs(mix_r)))
if peak > 0:
    target = 0.78
    mix_l = (mix_l / peak) * target
    mix_r = (mix_r / peak) * target

output_wav = "video/soundtrack_funky_upbeat_lofi_40s.wav"
with wave.open(output_wav, 'w') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    interleaved = np.empty((len(t) * 2,), dtype=np.int16)
    interleaved[0::2] = (mix_l * 32767).astype(np.int16)
    interleaved[1::2] = (mix_r * 32767).astype(np.int16)
    wf.writeframes(interleaved.tobytes())

print(f"Generated Upbeat Funky Soundtrack: {output_wav} (40s, 112 BPM, 44.1kHz stereo)")
