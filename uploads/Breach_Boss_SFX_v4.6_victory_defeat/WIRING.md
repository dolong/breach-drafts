# Victory + game over v4.6 — drop-in

Swap-in only: **no code changes**. Same ids, same hooks.

1. Overwrite `boss_victory_01` and `fleet_defeat_01` (.ogg and .mp3) in `assets/sfx/boss/`, and delete any other `boss_victory_*` / `fleet_defeat_*` files so old variants can't play.
2. `python3 merge_manifest.py assets/sfx/boss/manifest.json manifest_v4.6.json > manifest.new.json`, then replace `manifest.json` with it.

| id | Hook | Length | Notes |
|---|---|---|---|
| boss_victory | `win()` | 3400ms | Plays once |
| fleet_defeat | `lose()`, once | 4000ms | Hull bursts and the final blow at **+620ms** are baked in, as before. No jitter |
