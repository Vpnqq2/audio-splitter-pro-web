"""Optimises the artwork (PNG from the designer) into small WebP files in web/img. Optional: the results are already in the project.
Usage: python3 gen/assets.py /path/to/asset_folder"""
import os, sys, numpy as np
from PIL import Image
SRC = sys.argv[1] if len(sys.argv) > 1 else "assets_src"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web", "img")
os.makedirs(OUT, exist_ok=True)
def load(n): return Image.open(os.path.join(SRC, n)).convert("RGBA")
def save(im, name, q=82):
    p = os.path.join(OUT, name); im.save(p, "WEBP", quality=q, method=6); print(name, im.size, os.path.getsize(p) // 1024, "KB")
def fit_w(im, w): return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)

mic = load("microphone.png"); mic = mic.crop(mic.getbbox()); save(fit_w(mic, 860), "hero-mic.webp", 80)
rb = load("04_glowing_wave_ribbon.png"); save(rb.crop((0, 40, rb.width, rb.height)), "ribbon.webp", 80)
save(load("03_equalizer_bars.png"), "eq.webp", 80)
save(fit_w(load("02_audio_waveform.png"), 240), "wave.webp", 85)
save(fit_w(load("06_upload_cloud.png"), 170), "cloud.webp", 88)
sp = load("05_feature_icons.png"); a = np.array(sp)[:, :, 3]
cols = (a > 40).any(axis=0); runs = []; s = None
for i, c in enumerate(cols):
    if c and s is None: s = i
    if not c and s is not None: runs.append((s, i)); s = None
if s is not None: runs.append((s, len(cols)))
rows = np.where((a > 40).any(axis=1))[0]; cy = (rows[0] + rows[-1]) // 2
for (x0, x1), name in zip(runs, ["bolt", "shield", "browser", "lock"]):
    cx = (x0 + x1) // 2; h = 90
    save(sp.crop((cx - h, cy - h, cx + h, cy + h)).resize((128, 128), Image.LANCZOS), f"ic-{name}.webp", 88)
for n in ["vocals", "drums", "bass", "other"]:
    save(fit_w(load(n + ".png"), 300), f"stem-{n}.webp", 82)
