import numpy as np
import wave

sample_rate = 44100
duration = 40.0  # 40 seconds (matching 1.5x video)
bpm = 114
beat_dur = 60.0 / bpm
sixteenth = beat_dur / 4.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# -------------------------------------------------------------
# 1. ICONIC BASSLINE (Policy of Truth style)
# Key: D minor (D1=36.71, D2=73.42, F2=87.31, G2=98.00, C2=65.41)
# 16th note sequencing with syncopation, octave jumps & slide feel
# -------------------------------------------------------------
bass = np.zeros_like(t)
total_16ths = int(duration / sixteenth)

# 16-step pattern for 1 measure of Dm (repeated)
# D2, D1, D2, D2, F2, D2, G2, F2, D2, D1, C2, D2, F2, D2, G2, A2
step_pitches = [
    73.42, 36.71, 73.42, 73.42,
    87.31, 73.42, 98.00, 87.31,
    73.42, 36.71, 65.41, 73.42,
    87.31, 73.42, 98.00, 110.00
]

for s in range(total_16ths):
    f0 = step_pitches[s % len(step_pitches)]
    t_start = s * sixteenth
    idx_s = int(t_start * sample_rate)
    idx_e = min(int((t_start + sixteenth) * sample_rate), len(t))
    ts = t[idx_s:idx_e] - t_start

    # Analog Sawtooth + Sub-bass (Alan Wilder / Minimoog emulation)
    saw = 2.0 * (ts * f0 - np.floor(ts * f0 + 0.5))
    sub = np.sin(2 * np.pi * (f0 / 2.0) * ts)
    
    # Filter envelope with snappy attack & resonant decay
    cutoff_env = np.exp(-ts * 24.0)
    # Saturation / Warm tube warmth
    tone = np.tanh((0.7 * saw + 0.5 * sub) * (1.2 + 1.8 * cutoff_env))
    bass[idx_s:idx_e] += tone * 0.55

# -------------------------------------------------------------
# 2. DRUMS & PERCUSSION (Violator era Gated Snare & 4-on-the-floor)
# -------------------------------------------------------------
drums_l = np.zeros_like(t)
drums_r = np.zeros_like(t)
total_beats = int(duration / beat_dur)

for b in range(total_beats):
    t_beat = b * beat_dur
    ib_start = int(t_beat * sample_rate)

    # 1. Solid Kick on beats 1, 2, 3, 4 (Tight, punchy, industrial dance)
    k_len = int(0.20 * sample_rate)
    k_end = min(ib_start + k_len, len(t))
    tk = t[ib_start:k_end] - t_beat
    k_freq = 48.0 + 85.0 * np.exp(-tk * 38.0)
    kick = np.sin(2 * np.pi * np.cumsum(k_freq) / sample_rate) * np.exp(-tk * 16.0)
    drums_l[ib_start:k_end] += kick * 0.75
    drums_r[ib_start:k_end] += kick * 0.75

    # 2. Classic Gated Reverb Snare on beats 2 and 4
    if b % 2 == 1:
        s_len = int(0.25 * sample_rate)
        s_end = min(ib_start + s_len, len(t))
        tsn = t[ib_start:s_end] - t_beat
        
        # Snare body + white noise bursting through a sharp gate
        body = np.sin(2 * np.pi * 175.0 * np.exp(-tsn * 22.0) * tsn) * np.exp(-tsn * 16.0)
        noise = np.random.uniform(-1.0, 1.0, len(tsn)) * np.exp(-tsn * 10.0)
        # Gated cutoff at 0.22s
        gate = np.where(tsn < 0.22, 1.0, np.exp(-(tsn - 0.22) * 80.0))
        snare = (0.45 * body + 0.55 * noise) * gate * 0.55
        drums_l[ib_start:s_end] += snare
        drums_r[ib_start:s_end] += snare

    # 3. Driving 16th Hi-hats with mechanical shuffle & accents
    for sub in range(4):
        t_hat = t_beat + sub * sixteenth
        if t_hat >= duration:
            break
        ih_s = int(t_hat * sample_rate)
        ih_e = min(ih_s + int(0.04 * sample_rate), len(t))
        th = t[ih_s:ih_e] - t_hat
        accent = 0.24 if (sub in [0, 2]) else 0.14
        h_noise = np.random.uniform(-0.1, 0.1, len(th)) * np.exp(-th * 90.0) * accent
        drums_l[ih_s:ih_e] += h_noise * 0.9
        drums_r[ih_s:ih_e] += h_noise * 1.1

# -------------------------------------------------------------
# 3. ICONIC GUITAR RIFF / SYNTH LEAD (Policy of Truth Slide Riff)
# Slide between D4 -> F4 -> G4 -> F4 -> D4 with chorus and ping-pong delay
# -------------------------------------------------------------
riff_l = np.zeros_like(t)
riff_r = np.zeros_like(t)

# The classic 2-measure hook (in Dm):
# Bar 1: D4 (293.66), F4 (349.23), G4 (392.00) slide
# Bar 2: G4 -> F4 -> D4 -> C4 -> D4
riff_measures = int(duration / (beat_dur * 8.0)) + 1
riff_pattern = [
    # (offset_in_beats, freq, duration_in_beats)
    (0.0, 293.66, 0.8),
    (1.0, 293.66, 0.8),
    (2.0, 349.23, 0.8),
    (3.0, 392.00, 1.8), # held over to next bar
    (5.0, 349.23, 0.8),
    (6.0, 293.66, 1.0),
    (7.0, 261.63, 0.5),
    (7.5, 293.66, 0.5)
]

for rm in range(riff_measures):
    m_base = rm * (beat_dur * 8.0)
    for off, rf_freq, plen in riff_pattern:
        t_note = m_base + off * beat_dur
        if t_note >= duration:
            break
        ir_s = int(t_note * sample_rate)
        ir_len = int(plen * beat_dur * sample_rate)
        ir_e = min(ir_s + ir_len, len(t))
        tr = t[ir_s:ir_e] - t_note
        
        # Damped electric guitar pluck / synth brass hybrid
        env_r = (1.0 - np.exp(-tr * 80.0)) * np.exp(-tr * 2.2)
        # Pulse wave with subtle vibrato
        vibrato = 1.0 + 0.008 * np.sin(2 * np.pi * 5.5 * tr)
        lead_wave = np.sin(2 * np.pi * (rf_freq * vibrato) * tr)
        lead_wave += 0.35 * np.sin(2 * np.pi * (rf_freq * 2 * vibrato) * tr)
        lead_wave *= env_r * 0.28
        
        # Stereo ping-pong panning
        riff_l[ir_s:ir_e] += lead_wave * 0.85
        riff_r[ir_s:ir_e] += lead_wave * 1.15

# Add Delay / Echo to the riff (1/8th note delay = beat_dur * 0.5)
delay_samples = int(beat_dur * 0.5 * sample_rate)
decay = 0.35
for d in range(1, 4):
    shift = d * delay_samples
    if shift < len(t):
        riff_l[shift:] += riff_r[:-shift] * (decay ** d)
        riff_r[shift:] += riff_l[:-shift] * (decay ** d)

# -------------------------------------------------------------
# 4. DARK ANALOG SYNTH STRINGS / PADS (Depeche Mode atmosphere)
# Chords: Dm (D3, F3, A3) -> Bb (Bb2, D3, F3) -> C (C3, E3, G3) -> Dm
# -------------------------------------------------------------
pad_l = np.zeros_like(t)
pad_r = np.zeros_like(t)

pad_chords = [
    [146.83, 174.61, 220.00], # Dm
    [116.54, 146.83, 174.61], # Bb
    [130.81, 164.81, 196.00], # C
    [146.83, 174.61, 220.00]  # Dm
]
pad_bar_dur = beat_dur * 4.0
total_pad_bars = int(duration / pad_bar_dur) + 1

for pb in range(total_pad_bars):
    p_chord = pad_chords[pb % len(pad_chords)]
    t_pb = pb * pad_bar_dur
    ip_s = int(t_pb * sample_rate)
    ip_e = min(int((t_pb + pad_bar_dur) * sample_rate), len(t))
    if ip_s >= len(t):
        break
    tp = t[ip_s:ip_e] - t_pb
    
    # Smooth bowing attack and sustained release
    env_p = np.sin(np.pi * np.clip(tp / pad_bar_dur, 0, 1))
    for tone in p_chord:
        # Stereo chorus detuning
        pad_l[ip_s:ip_e] += np.sin(2 * np.pi * (tone * 0.998) * tp) * env_p * 0.05
        pad_r[ip_s:ip_e] += np.sin(2 * np.pi * (tone * 1.002) * tp) * env_p * 0.05

# -------------------------------------------------------------
# MASTER MIX & ANALOG MASTERING
# -------------------------------------------------------------
mix_l = bass * 0.70 + drums_l * 0.75 + riff_l * 0.65 + pad_l * 0.40
mix_r = bass * 0.70 + drums_r * 0.75 + riff_r * 0.65 + pad_r * 0.40

# Smooth fade-in (1.0s) and fade-out (2.0s)
fade_in = np.linspace(0.0, 1.0, int(1.0 * sample_rate))
fade_out = np.linspace(1.0, 0.0, int(2.0 * sample_rate))
mix_l[:len(fade_in)] *= fade_in
mix_r[:len(fade_in)] *= fade_in
mix_l[-len(fade_out):] *= fade_out
mix_r[-len(fade_out):] *= fade_out

# Peak limiter to clean -1.5dB
peak = max(np.max(np.abs(mix_l)), np.max(np.abs(mix_r)))
if peak > 0:
    target = 0.85
    mix_l = (mix_l / peak) * target
    mix_r = (mix_r / peak) * target

output_wav = "video/soundtrack_policy_of_truth_dm_40s.wav"
with wave.open(output_wav, 'w') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    interleaved = np.empty((len(t) * 2,), dtype=np.int16)
    interleaved[0::2] = (mix_l * 32767).astype(np.int16)
    interleaved[1::2] = (mix_r * 32767).astype(np.int16)
    wf.writeframes(interleaved.tobytes())

print(f"Generated Policy of Truth Style Soundtrack: {output_wav} (40s, 114 BPM, 44.1kHz stereo)")
