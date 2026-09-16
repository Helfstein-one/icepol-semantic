import os
import subprocess

OUTPUT_DIR = "video"
# Speed multiplier = 1.5x
# Original total duration was 60s -> New total duration = 40s (60 / 1.5)
# Duration per scene (total 8 scenes):
# S1: 4.67s (original 7s / 1.5)
# S2: 4.67s (original 7s / 1.5)
# S3: 5.33s (original 8s / 1.5)
# S4: 5.33s (original 8s / 1.5)
# S5: 4.00s (original 6s / 1.5)
# S6: 5.33s (original 8s / 1.5)
# S7: 5.33s (original 8s / 1.5)
# S8: 5.34s (original 8s / 1.5)
# Sum = 4.67 + 4.67 + 5.33 + 5.33 + 4.00 + 5.33 + 5.33 + 5.34 = 40.0s

clip_durations = [
    ("chat_s1.png", 4.67),
    ("chat_s2.png", 4.67),
    ("chat_s3.png", 5.33),
    ("chat_s4.png", 5.33),
    ("chat_s5.png", 4.00),
    ("chat_s6.png", 5.33),
    ("chat_s7.png", 5.33),
    ("chat_s8.png", 5.34)
]

clip_files = []
for i, (png_name, dur) in enumerate(clip_durations):
    clip_path = os.path.join(OUTPUT_DIR, f"fast_clip_{i}.mp4")
    png_path = os.path.join(OUTPUT_DIR, png_name)
    cmd = [
        "/opt/homebrew/bin/ffmpeg",
        "-y",
        "-loop", "1",
        "-i", png_path,
        "-c:v", "libx264",
        "-t", str(dur),
        "-pix_fmt", "yuv420p",
        "-vf", "scale=1920:1080",
        clip_path
    ]
    subprocess.run(cmd, check=True)
    clip_files.append(clip_path)

concat_path = os.path.join(OUTPUT_DIR, "concat_fast_chat.txt")
with open(concat_path, "w") as f:
    for c in clip_files:
        f.write(f"file '{os.path.abspath(c)}'\n")

final_output = os.path.join(OUTPUT_DIR, "icepol_chat_ui_journey_1.5x_funky_upbeat.mp4")
audio_path = os.path.join(OUTPUT_DIR, "soundtrack_funky_upbeat_lofi_40s.wav")

cmd = [
    "/opt/homebrew/bin/ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_path,
    "-i", audio_path,
    "-c:v", "libx264",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    final_output
]
subprocess.run(cmd, check=True)
print(f"Generated 1.5x Fast Chat Journey Video: {final_output}")
