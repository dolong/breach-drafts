# Alarm v4.3 — bunker hand-crank, cranked twice

## Install
1. Overwrite `encounter_alarm_01` and `encounter_alarm_loop_01` (.ogg and .mp3) in `assets/sfx/boss/`.
2. `python3 merge_manifest.py assets/sfx/boss/manifest.json manifest_v4.3.json > manifest.new.json`, then replace `manifest.json` with it.

## Timing change (Jump Gate v2 · `alarm()` → `reveal()`)
| | Before | Now |
|---|---|---|
| `reveal()` fires after `alarm()` starts | +1100ms | **+3115ms** |
| Music duck | −10dB for 1.2s | −10dB for **3.4s** |
| Alarm when the reveal fires | ends | **keeps playing**: it winds down under the reveal and ends on its own (4203ms total) |

Shape, for matching any visuals: the first crank peaks at about 1557ms and sags, the second heave starts at 1957ms, and it reaches full speed on the reveal at 3115ms.

Don't stop or fade the alarm in code when `reveal()` starts. No jitter on it, same as before.

`encounter_alarm_loop` is one 1635ms crank cycle. Use it only if the reveal ever waits on a tap.

This alarm plays before all three bosses.
