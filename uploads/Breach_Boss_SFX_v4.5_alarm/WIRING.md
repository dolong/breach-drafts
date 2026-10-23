# Alarm v4.5 — bunker hand-crank ×2, tighter

Replaces v4.4: the second crank now picks up as the first is dying away at the bottom, instead of after a pause.

## Install
1. Overwrite `encounter_alarm_01` and `encounter_alarm_loop_01` (.ogg and .mp3) in `assets/sfx/boss/`.
2. `python3 merge_manifest.py assets/sfx/boss/manifest.json manifest_v4.5.json > manifest.new.json`, then replace `manifest.json` with it.

## Timing (Jump Gate v2 · `alarm()` → `reveal()`)
| | v4.4 | v4.5 |
|---|---|---|
| Second crank starts | 3395ms | 2797ms |
| `reveal()` fires after `alarm()` starts | +5088ms | **+4490ms** |
| Music duck | 5.4s | **4.8s** |
| File length | 6969ms | 6371ms (keeps winding down under the reveal) |

Don't stop or fade the alarm in code when `reveal()` starts. The loop is unchanged from v4.4.
