"""Swap the v4 sounds into the game's current manifest.
Usage: python3 merge_manifest.py assets/sfx/boss/manifest.json manifest_v4.json > manifest.new.json
Entries with the same id are replaced; everything else is kept."""
import json, sys
base, new = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
ids = {c["id"] for c in new["clips"]}
base["clips"] = [c for c in base["clips"] if c["id"] not in ids] + new["clips"]
json.dump(base, sys.stdout, indent=2, ensure_ascii=False)
