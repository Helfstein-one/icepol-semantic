import numpy as np
import wave
import struct

sample_rate = 44100
duration = 60.0  # 60 seconds
bpm = 126
beat_dur = 60.0 / bpm
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Track 1: Heavy Cyberpunk / Dark Synth Bass (Sawtooth + sub-oscillator + low-pass sweep)
# Notes progression: A1 (55Hz), F1 (43.65Hz), D1 (36.71Hz), E1 (41.2Hz)
bass = np.zeros_like(t)
sixteenth = beat_dur / 4.0
total_16ths = int(duration / sixteenth)

notes_seq = [
    55.0, 55.0, 110.0, 55.0, 55.0, 55.0, 110.0, 55.0, # A1
    43.65, 43.65, 87.3, 43.65, 43.65, 43.65, 87.3, 43.65, # F1
    36.71, 36.71, 73.42, 36.71, 36.71, 36.71, 73.42, 36.71, # D1
    41.2, 41.2, 82.4, 41.2, 41.2, 41.2, 82.4, 41.2 # E1
]

for step in range(total_16ths):
    f0 = notes_seq[step % len(notes_seq)]
    t_start = step * sixteenth
    idx_start = int(t_start * sample_rate)
    idx_end = min(int((t_start + sixteenth) * sample_rate), len(t))
    t_chunk = t[idx_start:idx_end] - t_start
    
    # Sawtooth + sub bass + saturation distortion
    saw = 2.0 * (t_chunk * f0 - np.floor(t_chunk * f0 + 0.5))
    sub = np.sin(2 * np.pi * (f0 / 2.0) * t_chunk)
    env = np.exp(-t_chunk * 14.0)
    note_wave = (0.6 * saw + 0.4 * sub) * env
    # Soft clipping / overdrive
    note_wave = np.tanh(note_wave * 2.2)
    bass[idx_start:idx_end] += note_wave

# Track 2: Cyberpunk Kick Drum (Punchy 909-style pitch sweep)
drums = np.zeros_like(t)
total_beats = int(duration / beat_dur)

for b in range(total_beats):
    t_kick = b * beat_dur
    ik_start = int(t_kick * sample_rate)
    ik_len = int(0.25 * sample_rate)
    ik_end = min(ik_start + ik_len, len(t))
    tk = t[ik_start:ik_end] - t_kick
    
    # Kick pitch envelope (160Hz drop to 45Hz)
    freq_env = 45.0 + 120.0 * np.exp(-tk * 35.0)
    phase = 2 * np.pi * np.cumsum(freq_env) / sample_rate
    kick_wave = np.sin(phase) * np.exp(-tk * 14.0)
    kick_wave = np.tanh(kick_wave * 2.5)
    drums[ik_start:ik_end] += kick_wave * 0.9

    # Snare / Clap on beats 2 and 4
    if b % 2 == 1:
        t_snare = t_kick
        is_start = ik_start
        is_len = int(0.35 * sample_rate)
        is_end = min(is_start + is_len, len(t))
        ts = t[is_start:is_end] - t_snare
        
        # Snare body + gated white noise
        body = np.sin(2 * np.pi * 180.0 * np.exp(-ts * 18.0) * ts) * np.exp(-ts * 15.0)
        noise = np.random.uniform(-1.0, 1.0, len(ts)) * np.exp(-ts * 9.0)
        snare_wave = (0.4 * body + 0.6 * noise) * 0.8
        drums[is_start:is_end] += snare_wave

# Track 3: Cyberpunk Arpeggio (Kavinsky / Perturbator style high-tech synth)
arp = np.zeros_like(t)
arp_freqs = [
    220.0, 261.63, 329.63, 440.0, 523.25, 440.0, 329.63, 261.63, # Am
    174.61, 220.0, 261.63, 349.23, 440.0, 349.23, 261.63, 220.0, # F
    146.83, 174.61, 220.0, 293.66, 349.23, 293.66, 220.0, 174.61, # Dm
    164.81, 196.0, 246.94, 329.63, 392.0, 329.63, 246.94, 196.0   # Em
]

for step in range(total_16ths):
    f_arp = arp_freqs[step % len(arp_freqs)]
    t_start = step * sixteenth
    ia_start = int(t_start * sample_rate)
    ia_end = min(int((t_start + sixteenth) * sample_rate), len(t))
    ta = t[ia_start:ia_end] - t_start
    
    # Pulse wave with fast decay and delay feel
    pulse = np.sign(np.sin(2 * np.pi * f_arp * ta))
    env_a = np.exp(-ta * 22.0)
    arp[ia_start:ia_end] += pulse * env_a * 0.28

# Track 4: Cinematic Neon Pad (Lush stereo background chords)
pad_l = np.zeros_like(t)
pad_r = np.zeros_like(t)
chord_dur = beat_dur * 4.0
total_chords = int(duration / chord_dur)
chords = [
    [220.0, 261.63, 329.63, 440.0], # Am
    [174.61, 220.0, 261.63, 349.23], # F
    [146.83, 174.61, 220.0, 293.66], # Dm
    [164.81, 196.0, 246.94, 329.63]  # Em
]

for c_idx in range(total_chords):
    c_tones = chords[c_idx % len(chords)]
    tc_start = c_idx * chord_dur
    ic_start = int(tc_start * sample_rate)
    ic_end = min(int((tc_start + chord_dur) * sample_rate), len(t))
    tc = t[ic_start:ic_end] - tc_start
    
    # Smooth attack and release envelope
    env_c = np.sin(np.pi * np.clip(tc / chord_dur, 0.0, 1.0))
    for tone in c_tones:
        # Slight detuning for wide stereo chorus
        pad_l[ic_start:ic_end] += np.sin(2 * np.pi * (tone * 0.997) * tc) * env_c * 0.06
        pad_r[ic_start:ic_end] += np.sin(2 * np.pi * (tone * 1.003) * tc) * env_c * 0.06

# Master Mix Stereo
mix_left = bass * 0.65 + drums * 0.75 + arp * 0.5 + pad_l * 0.55
mix_right = bass * 0.65 + drums * 0.75 + arp * 0.45 + pad_r * 0.55

# Master Limiter / Normalization
max_peak = max(np.max(np.abs(mix_left)), np.max(np.abs(mix_right)))
mix_left = (mix_left / max_peak) * 0.94
mix_right = (mix_right / max_peak) * 0.94

# Write WAV file
output_wav = "video/soundtrack_cyberpunk_synthwave_60s.wav"
with wave.open(output_wav, 'w') as wav_file:
    wav_file.setnchannels(2)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    
    # Interleave stereo
    audio_interleaved = np.empty((len(t) * 2,), dtype=np.int16)
    audio_interleaved[0::2] = (mix_left * 32767).astype(np.int16)
    audio_interleaved[1::2] = (mix_right * 32767).astype(np.int16)
    
    wav_file.writeframes(audio_interleaved.tobytes())

print(f"Generated new soundtrack: {output_wav} ({duration}s, 44.1kHz stereo)")
