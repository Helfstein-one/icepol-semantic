import subprocess
import os

ffmpeg = "/opt/homebrew/bin/ffmpeg"

# Scene list with durations (seconds)
scenes = [
    ("video/scene1_terminal.png", 5.5),
    ("video/scene2_home.png", 5.5),
    ("video/scene3_duckdb.png", 5.5),
    ("video/scene4_llm.png", 5.0),
    ("video/scene5_query.png", 6.0),
    ("video/scene6_mermaid.png", 5.0),
    ("video/scene7_outro.png", 3.5),
]

# Generate individual scene video clips
temp_clips = []
for idx, (img, dur) in enumerate(scenes):
    clip_path = f"video/clip_{idx+1}.mp4"
    cmd = [
        ffmpeg,
        "-y",
        "-loop", "1",
        "-i", img,
        "-t", str(dur),
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-r", "30",
        "-c:v", "libx264",
        "-preset", "fast",
        clip_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    temp_clips.append(clip_path)
    print(f"Generated clip {clip_path} ({dur}s)")

# Concat file
concat_txt = "video/concat.txt"
with open(concat_txt, "w") as f:
    for clip in temp_clips:
        f.write(f"file '{os.path.basename(clip)}'\n")

# Final render combining video + 80s soundtrack
output_mp4 = "video/icepol_demo_80s.mp4"
audio_file = "video/soundtrack_80s.wav"

cmd_final = [
    ffmpeg,
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_txt,
    "-i", audio_file,
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "18",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-movflags", "+faststart",
    output_mp4
]

subprocess.run(cmd_final, check=True)
print(f"Rendered final video: {output_mp4}")

# Cleanup temp clips
for clip in temp_clips:
    try: os.remove(clip)
    except: pass
try: os.remove(concat_txt)
except: pass

print("Done! Video is ready in video/icepol_demo_80s.mp4")
