import os
import subprocess

OUTPUT_DIR = "video"
AUDIO_FILE = "video/soundtrack_take_on_me_60s.wav"
FINAL_VIDEO = "video/icepol_user_journey_take_on_me.mp4"

# 10 Scene PNGs and durations (Total = 60s)
scenes_meta = [
    ("cheri_s1.png", 6),   # GitHub Top
    ("cheri_s2.png", 6),   # GitHub README scroll
    ("cheri_s3.png", 6),   # Terminal git clone
    ("cheri_s4.png", 6),   # Terminal make seed & podman
    ("cheri_s5.png", 6),   # Chat UI Welcome
    ("cheri_s6.png", 5),   # Chat UI Asking question
    ("cheri_s7.png", 7),   # Chat UI DuckDB results
    ("cheri_s8.png", 6),   # Chat UI Mermaid ERD
    ("cheri_s9.png", 6),   # Langfuse Tracing waterfall
    ("cheri_s10.png", 6),  # Token cost breakdown
]

clip_files = []
concat_lines = []

for i, (png_name, dur) in enumerate(scenes_meta):
    png_path = os.path.join(OUTPUT_DIR, png_name)
    clip_path = os.path.join(OUTPUT_DIR, f"tom_clip_{i}.mp4")
    print(f"Encoding clip {i}: {png_name} ({dur}s)...")
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", png_path,
        "-c:v", "libx264", "-t", str(dur), "-pix_fmt", "yuv420p",
        "-r", "25", clip_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    clip_files.append(clip_path)
    concat_lines.append(f"file '{os.path.abspath(clip_path)}'")

concat_list_path = os.path.join(OUTPUT_DIR, "concat_tom.txt")
with open(concat_list_path, "w") as f:
    f.write("\n".join(concat_lines) + "\n")

print("Stitching clips and mixing soundtrack...")
cmd_final = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_list_path,
    "-i", AUDIO_FILE,
    "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    FINAL_VIDEO
]
subprocess.run(cmd_final, check=True)

# Cleanup clips
for c in clip_files:
    if os.path.exists(c):
        os.remove(c)
if os.path.exists(concat_list_path):
    os.remove(concat_list_path)

print(f"Generated Take On Me User Journey Video: {FINAL_VIDEO}")
