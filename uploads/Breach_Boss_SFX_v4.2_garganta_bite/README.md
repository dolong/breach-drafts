# Garganta bite v4.2 (Leviathan) — drop-in

1. Overwrite `garganta_bite_01`–`03` (.ogg and .mp3) in `assets/sfx/boss/` with the files here.
2. Delete `garganta_hurt_04.ogg` and `garganta_hurt_04.mp3`.
3. `python3 merge_manifest.py assets/sfx/boss/manifest.json manifest_v4.2.json > manifest.new.json`, then replace `manifest.json` with it.
   This lists the three new bites and drops `garganta_hurt_04` from the hurt round-robin.

Timing is unchanged: the jaw crack lands at +385ms, and `garganta_bite_layer` still plays at +335ms.
