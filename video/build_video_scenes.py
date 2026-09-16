import subprocess
import os
import time

pwd = os.path.abspath(os.path.curdir)
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def capture_html(html_file, output_png, window_size="1440,900"):
    file_url = f"file://{pwd}/{html_file}"
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        f"--window-size={window_size}",
        f"--screenshot={output_png}",
        file_url
    ]
    subprocess.run(cmd, check=True)
    print(f"Captured {output_png}")

print("Preparing HTML scenes...")
