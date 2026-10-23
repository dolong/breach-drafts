"""Render every recipe in sounds.py → wav/ogg/mp3 + manifest.json.  Run: python3 build.py [out_dir]"""
import json, os, subprocess, sys, time
import numpy as np
from scipy.io import wavfile
import dsp
from sounds import REG

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
TIER_GAIN = {"dice": -12, "ui": -9, "combat": -6, "big": 0}
for sub in ("wav", "ogg", "mp3"):
    os.makedirs(os.path.join(OUT, sub), exist_ok=True)


def write(name, y):
    pcm = np.clip(y + np.random.default_rng(1).uniform(-1, 1, len(y)) / 65536, -1, 1)
    wav = os.path.join(OUT, "wav", name + ".wav")
    wavfile.write(wav, dsp.SR, (pcm * 32767).astype(np.int16))
    q = ["-hide_banner", "-loglevel", "error", "-y", "-i", wav]
    subprocess.run(["ffmpeg", *q, "-c:a", "libvorbis", "-q:a", "6", os.path.join(OUT, "ogg", name + ".ogg")], check=True)
    subprocess.run(["ffmpeg", *q, "-c:a", "libmp3lame", "-b:a", "160k", os.path.join(OUT, "mp3", name + ".mp3")], check=True)


manifest = {"source_pack": "generated:breach-boss-sfx-v1", "sample_rate": dsp.SR, "format": "16-bit mono; ogg (vorbis q6) primary, mp3 160k fallback",
            "tiers_db": TIER_GAIN, "clips": []}
t0 = time.time()
KEEP = set(os.environ["KEEP"].split(",")) if os.environ.get("KEEP") else None
for e in REG:
    if KEEP and e["id"] not in KEEP:
        continue
    names = [e["id"]] if not e["variants"] else [f'{e["id"]}_{i + 1:02d}' for i in range(e["variants"])]
    files = []
    for i, nm in enumerate(names):
        dsp.reseed(nm)
        y = np.asarray(e["fn"](i), float)
        if e["loop"]:
            y = y * 10 ** ((e["target"] - dsp.loudness_db(y)) / 20)
            y = y * min(1.0, 10 ** (-1 / 20) / np.abs(y).max())
        else:
            y = dsp.master(y, e["target"], keep_len=e["keep_len"])
        write(nm, y)
        files.append({"name": nm, "ogg": f"ogg/{nm}.ogg", "mp3": f"mp3/{nm}.mp3", "duration_ms": round(len(y) / dsp.SR * 1000),
                      "peak_db": round(20 * np.log10(np.abs(y).max()), 1)})
        print(f"{nm:28s} {len(y) / dsp.SR:5.2f}s  peak {files[-1]['peak_db']:5.1f} dB")
    manifest["clips"].append({"id": e["id"], "source": f'generated:{e["id"]}', "tier": e["tier"], "gain_db": TIER_GAIN[e["tier"]],
                              "loop": e["loop"], "round_robin": len(files) > 1, "event": e["event"], "trigger": e["trigger"], "files": files})
with open(os.path.join(OUT, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print(f"done: {sum(len(c['files']) for c in manifest['clips'])} files in {time.time() - t0:.1f}s")
