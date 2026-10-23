# Boss SFX v4 — alarm, boss appearance, Garganta's voice

Swap-in only: **no code changes**. Same ids and the same timings as before.

## Install
1. Copy `ogg/` and `mp3/` into `assets/sfx/boss/`, overwriting files with the same name. Delete any older files for these ids first, so stale variants can't play.
2. `python3 merge_manifest.py assets/sfx/boss/manifest.json manifest_v4.json > manifest.new.json`, then replace `manifest.json` with it.
3. Leave `alt_B/` out of the game unless told to use a B take.

## What changed (12 ids, all were generated synth sounds)
| id | Files | Timing contract (unchanged) |
|---|---|---|
| encounter_alarm | 1 | Ends at 1100ms, as `reveal()` fires |
| encounter_alarm_loop | 1 | Seamless loop, 841ms |
| boss_warp_in | 1 | Slam at +420ms with the flash |
| reveal_garganta / reveal_mothercore / reveal_marauder | 1 each | Hits at +0.22s (colour flash) and +0.96s (name slam) |
| boss_phase2_frenzy | 1 | Starts on the call |
| garganta_inhale | 1 | Starts on the call |
| garganta_hurt | **4** | Layer on `boss_hit`, round-robin |
| garganta_bite | **3** | Jaw snap at +385ms; `garganta_bite_layer` still at +335ms |
| garganta_maw_shut | **2** | Clamp at +20ms |

Keep the no-jitter rule for `encounter_alarm`, `reveal_*`, `boss_warp_in` and `garganta_bite`.

## Credit
Sonniss GDC bundle sounds need no attribution. Keep the existing line: "Sound effects: Helton Yan — Pixel Combat (CC BY 4.0)."
