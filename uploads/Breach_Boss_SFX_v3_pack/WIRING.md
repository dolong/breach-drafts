# SFX — boss encounters v3 (Jump Gate v2, Marauder Gate, Mother Core Gate v2, Garganta Gate)

This replaces the v2 brief. Every semantic id is unchanged, so hooks already wired from v2 keep working. v3 changes which files sit behind seven ids, ships the pack clips already converted, and moves two timings.

## 1. Upload

- **From this zip:** upload everything in `ogg/` and `mp3/` to R2 as-is (131 files across 22 ids). They're already trimmed, length-capped, loudness-matched and converted to 44.1kHz OGG with an MP3 fallback. Don't convert or re-normalise anything.
- **From the v2 zip:** the 18 generated files, unchanged.
- **Manifest:** run `python3 merge_manifest.py <v2 manifest.json> manifest_pack.json > manifest.json`. Pack entries replace the v2 entries with the same id, and the generated entries stay as they are.
- `hull_hit` has **5** files, not 6. Round-robin across whatever the manifest lists.

## 2. What changed from v2

| id | v2 pick | v3 | Why |
|---|---|---|---|
| boss_engage | Mecha Morale | **Mecha Lock In** | Morale holds for 2s+; a confirm tap needs to land and get out |
| fleet_shot_mid | Laser Bursts | Laser Bursts, **cut to 450ms** | The full clip is a 1.2s+ stream that smears the volley; the first 450ms is the burst |
| fleet_shot_big | Mecha White Laser | **Mecha Purple Laser** | Same family, decays naturally by ~0.9s instead of holding for 1.5s |
| boss_hit_heavy | Mecha Intense Hit | **Mecha Armor Piercer** | Intense Hit has no attack transient (a 2s rumble); Armor Piercer hits in 7–40ms |
| hull_hit | Mecha Damage | **Bass Hit** (variants 1–5) | Mecha Damage swells in over ~100ms, so hits felt late; Bass Hit variant 6 has the same swell and was dropped. `Thud` was ruled out because it's already the missed-die sound |
| ship_destroyed | Mecha Detonator | **Mecha Multiple Bangs** | Detonator is a flat buzz; Multiple Bangs reads as an explosion chain |
| mothercore_beam | Mecha Laser Release | **Mecha Black Laser** | Laser Release variants ran 0.4s to 2.7s, so the beam changed size every fight; Black Laser is a steady ~1.85s across all six |

The other 15 picks stayed. All of them are trimmed and capped to their moment (lengths below).

## 3. Pack clips

| id | Pack stem | Files | Length |
|---|---|---|---|
| gate_jump_charge | DSGNMisc_MOVEMENT-Mecha Large Takeoff | 6 | 1385–1438 ms |
| gate_jump_exit | MAGSpel_CAST-Teleport Downer | 6 | 1500 ms |
| boss_engage | DSGNSynth_BUFF-Mecha Lock In | 6 | 763–900 ms |
| gate_decoy | DSGNMisc_SKILL RELEASE-Flare Gun | 6 | 1413–1483 ms |
| fleet_shot | DSGNMisc_PROJECTILE-Laser Shot | 6 | 600 ms |
| fleet_shot_mid | DSGNMisc_PROJECTILE-Laser Bursts | 6 | 450 ms |
| fleet_shot_big | DSGNMisc_SKILL IMPACT-Mecha Purple Laser | 6 | 912–948 ms |
| boss_hit | DSGNMisc_HIT-Laser Hit | 6 | 390–468 ms |
| boss_hit_heavy | DSGNMisc_HIT-Mecha Armor Piercer | 6 | 900 ms |
| boss_hit_crit | DSGNMisc_SKILL IMPACT-Critical Strike | 6 | 1000 ms |
| shield_up | DSGNSynth_BUFF-Bonus Max Shield | 6 | 918–950 ms |
| shield_block | DSGNTonl_SKILL IMPACT-Deflected Hit | 6 | 700 ms |
| hull_hit | DSGNImpt_EXPLOSION-Bass Hit | 5 | 900 ms |
| hull_hit_heavy | DSGNImpt_EXPLOSION-Mecha Core Damage | 6 | 1200 ms |
| ship_destroyed | DSGNImpt_EXPLOSION-Mecha Multiple Bangs | 6 | 1400 ms |
| boss_phase2_overdrive | DSGNSynth_CAST-Mecha Speeding | 6 | 2000 ms |
| marauder_shot | DSGNMisc_HIT-Mecha Laser Pistol | 6 | 450 ms |
| marauder_charge | DSGNSynth_CAST-Mecha Laser Prepare | 6 | 1319–1449 ms |
| mothercore_shot | DSGNTonl_SKILL RELEASE-Tiny Energy Sphere | 6 | 240 ms |
| mothercore_beam | DSGNMisc_SKILL IMPACT-Mecha Black Laser | 6 | 1852–1885 ms |
| garganta_regrow | DSGNMisc_CAST-Slime Ball | 6 | 871–968 ms |
| garganta_bite_layer | DSGNMisc_HIT-Mecha Gore Cruncher | 6 | 600 ms |

## 4. Shared rules

- **Round-robin:** play every id round-robin across its files, and never play the same file twice in a row.
- **Jitter:** give combat-tier plays a random `playbackRate` of 0.96–1.04 and volume ±1.5dB.
- **No jitter on choreographed clips:** `encounter_alarm`, `reveal_*`, `boss_warp_in`, `garganta_bite`, `boss_death`, `fleet_defeat`.
- **Buses:** dice −12dB, UI −9dB, combat −6dB, big 0dB. Each clip's `tier` says which bus it goes on.
- **Lengths are baked in.** Each pack clip is already capped to its moment with a fade, so play every file to its end. Delete v2's "fade it out at the next event" handling.
- **Loudness is baked in.** Pack clips carry per-id loudness so bigger hits are louder before the bus (1-damage shot −17, 2–3 −15.5, 4+ −14 LUFS-M). Don't normalise at runtime.
- **Clips marked *existing*** are already on R2 from the first SFX map. If one is missing, list it in your reply instead of substituting another clip.

## 5. Jump Gate v2

Delete the silent `tone()` hook and every `tone(...)` call.

| Where | Play |
|---|---|
| `countUp()`, each odd tick | *existing* `DSGNTonl_INTERFACE-Tonal Click`, +1 semitone per tick |
| `countUp()`, SECTOR SECURED | *existing* `DSGNMisc_SKILL IMPACT-Dramatic Finish` |
| `jump()`, at phase `'jump'` | `gate_jump_charge` |
| `jump()`, white flash | `gate_jump_exit`, **120ms before the flash** if `jump()` can schedule it (the clip swells to its peak 100–170ms in); otherwise on the flash |
| `alarm()`, at the start | `encounter_alarm`; it ends as `reveal()` fires at +1100ms. Duck music −10dB for 1.2s |
| `reveal()`, at the start | `reveal_marauder` / `reveal_mothercore` / `reveal_garganta`. Each has hits built in at +0.22s (colour flash) and +0.96s (name slam) |
| `fight()` | `boss_engage` |
| `decoy()` | `gate_decoy` |
| `letGo()` | *existing* `DSGNTonl_USABLE-Coin Toss` |
| `settle()` with kind `'won'` | *existing* `Coin Toss`, then *existing* `DSGNTonl_USABLE-Whimsy Coin` (prestige) 150ms later |

`encounter_alarm_loop` is spare. Use it only if the reveal is ever gated on a tap: loop it from the OGG and stop it on the reveal.

## 6. Boss fights (all three files unless noted)

| Where | Play |
|---|---|
| `warpIn()` | `boss_warp_in`; its impact lands at +420ms with the flash |
| `engage()` | `boss_engage` |
| `flee()` | *existing* `WHSH_MOVEMENT-Mecha Ship Passby` + *existing* `DSGNTonl_USABLE-Coin Spend` |
| `startRound()`, when the NEXT tag appears | `boss_intent`. Use `boss_intent_danger` instead for the big intent (CORE BEAM, DEVOUR, Marauder FIRES 4+) |
| `startRound()`, Mother Core, when `exposed()` | `mothercore_core_open` instead of the intent blip |
| `startRound()`, Garganta, when `exposed()` | `garganta_inhale` instead of the intent blip |
| `dealAnim()` | *existing* `WHSH_MOVEMENT-Simple Whoosh`, one per card at 60 + i×90ms |
| `pickCard()` | *existing* `UIClick_INTERFACE-Metallic Click` |
| `take()` | *existing* `DSGNMisc_MELEE-Bit Sword` |
| dice roll, land and set | *existing* dice clips, as already wired |
| `lockFx()` | *existing* `dice_slot_fill_flash` |
| `nope()` | *existing* `UIMisc_INTERFACE-Denied` |
| `fireSeq()`, damage ship's `muzzle()` | by the ship's damage: `fleet_shot` (1), `fleet_shot_mid` (2–3), `fleet_shot_big` (4+) |
| `fireSeq()`, block ship firing | `shield_up` |
| `fireSeq()`, repair ship firing | *existing* `UIGlitch_USABLE-Mecha Repair` |
| `hitEnemy()` | `boss_hit_crit` if `exposed()`, else `boss_hit_heavy` if dmg ≥ 4, else `boss_hit` |
| `hurt()`, Garganta | layer `garganta_hurt` on the hit |
| `addBlock()` (SHIELDS UP) | `shield_up` |
| `heal()` (PATCH UP) | *existing* `UIGlitch_USABLE-Mecha Repair` |
| `hullHit()` with label `'MISS'` | *existing* `dice_die_land_hull` only, so a missed die never sounds like enemy fire |
| `hullHit()`, any other call | `hull_hit_heavy` if n ≥ 3, else `hull_hit` |
| `enemyTurn()`, Marauder, each `muzzle()` | `marauder_shot` |
| `enemyTurn()`, Mother Core, each `muzzle()` | `mothercore_shot` (240ms each, so six shots 120ms apart stay six distinct pulses) |
| `enemyTurn()`, atk 0, Marauder (CHARGING) | `marauder_charge` |
| `enemyTurn()`, atk 0, Mother Core (CORE SEALS) | `mothercore_core_seal` |
| `enemyTurn()`, atk 0, Garganta (MAW SHUTS) | `garganta_maw_shut` |
| `bite()`, Garganta | `garganta_bite` at the start (jaw snap built in at +385ms), plus `garganta_bite_layer` at **+335ms**. The crunch peaks ~50ms into the file, so it lands on the jaw-shut frame |
| `resolveEnemy()`, blocked > 0 | `shield_block`, 60ms before any hull hit |
| `biteDmg()`, Garganta | `hull_hit_heavy` / `hull_hit` at −6dB, because the snap already carries the impact |
| `vaporize()`, Mother Core | `mothercore_beam` at the start, then `ship_destroyed` at +170ms |
| `sinkShip()`, Garganta | `ship_destroyed` |
| `afterPlayer()`, OVERDRIVE | `boss_phase2_overdrive` |
| `afterPlayer()`, FRENZY | `boss_phase2_frenzy` |
| `endRound()`, Garganta regen | `garganta_regrow` |
| `explode()` | `boss_death`, **once**. The whole burst chain is baked in, so don't add per-burst sounds |
| `win()` | `boss_victory` |
| `lose()` | `fleet_defeat`, once. The hull bursts and the final blow at 620ms are baked in |

## 7. Acceptance

- **Jump flow:** a takeoff whoosh on JUMP, the teleport swell peaking on the white flash, three klaxon cycles, then the reveal stinger. Its first hit lands on the colour flash and its second on the name slam.
- **Volley:** 1-, 2–3- and 4+-damage ships fire audibly different and progressively louder shots. Hits on an open core use Critical Strike.
- **CORE BEAM turn:** danger blips when the intent appears, six separate plasma pulses 120ms apart, a heavy hull hit, then the beam, then the detonation chain as the drone vanishes.
- **Garganta bite:** the generated snap and the Gore Cruncher land together on the jaw-shut frame, with no extra hull thud on top.
- **Missed die:** only the dice thud plays, and an enemy hull hit sounds clearly different from it.
- **Repetition:** no file plays twice in a row across a fight.

Credit line, unchanged: "Sound effects: Helton Yan — Pixel Combat (CC BY 4.0)."
