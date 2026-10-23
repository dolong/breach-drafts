"""Merge the processed pack clips into the v2 manifest.
Usage: python3 merge_manifest.py path/to/v2/manifest.json manifest_pack.json > manifest.json
Pack entries replace v2 entries with the same id; generated entries are kept as they are."""
import json, sys
base, pack = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
ids = {c["id"] for c in pack["clips"]}
base["clips"] = [c for c in base["clips"] if c["id"] not in ids] + pack["clips"]
base["source_pack"] = "mixed: generated:breach-boss-sfx-v2 + Helton Yan Pixel Combat (CC BY 4.0), pack clips processed v3"
json.dump(base, sys.stdout, indent=2, ensure_ascii=False)
