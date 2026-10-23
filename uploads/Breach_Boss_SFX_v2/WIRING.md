# SFX — boss encounters v2 (Jump Gate v2, Marauder Gate, Mother Core Gate v2, Garganta Gate)

This replaces the v1 boss SFX brief. Every hook uses a **semantic id**, and the manifest `source` field says whether that id is a Pixel Combat clip or a generated one. Code only ever asks for the id.

## 1. New pack clips to convert

These 22 stems aren't on R2 yet.
- For each stem, take files `-001` to `-006`. The exact source filenames are in each clip's `convert_from` in `manifest.json`.
- Convert to 44.1kHz 16-bit OGG, plus an MP3 fallback.
- Trim leading silence.
- Name the files `<id>_01` to `<id>_06` and upload them to R2.

| id | Pack stem |
|---|---|
| gate_jump_charge | DSGNMisc_MOVEMENT-Mecha Large Takeoff |
| gate_jump_exit | MAGSpel_CAST-Teleport Downer |
| boss_engage | DSGNSynth_CAST-Mecha Morale |
| gate_decoy | DSGNMisc_SKILL RELEASE-Flare Gun |
| fleet_shot | DSGNMisc_PROJECTILE-Laser Shot |
| fleet_shot_mid | DSGNMisc_PROJECTILE-Laser Bursts |
| fleet_shot_big | DSGNMisc_SKILL IMPACT-Mecha White Laser |
| boss_hit | DSGNMisc_HIT-Laser Hit |
| boss_hit_heavy | DSGNImpt_EXPLOSION-Mecha Intense Hit |
| boss_hit_crit | DSGNMisc_SKILL IMPACT-Critical Strike |
| shield_up | DSGNSynth_BUFF-Bonus Max Shield |
| shield_block | DSGNTonl_SKILL IMPACT-Deflected Hit |
| hull_hit | DSGNImpt_EXPLOSION-Mecha Damage |
| hull_hit_heavy | DSGNImpt_EXPLOSION-Mecha Core Damage |
| ship_destroyed | DSGNImpt_EXPLOSION-Mecha Detonator |
| boss_phase2_overdrive | DSGNSynth_CAST-Mecha Speeding |
| marauder_shot | DSGNMisc_HIT-Mecha Laser Pistol |
| marauder_charge | DSGNSynth_CAST-Mecha Laser Prepare |
| mothercore_shot | DSGNTonl_SKILL RELEASE-Tiny Energy Sphere |
| mothercore_beam | DSGNMisc_SKILL RELEASE-Mecha Laser Release |
| garganta_regrow | DSGNMisc_CAST-Slime Ball |
| garganta_bite_layer | DSGNMisc_HIT-Mecha Gore Cruncher |

## 2. Generated clips

The zip contains 18 generated files in `ogg/` and `mp3/`. Upload them as-is: their names are already the semantic ids. These cover what the pack has no equivalent for:
- the encounter alarm (the pack has no klaxon);
- the three reveal stingers and the warp-in, which are timed to their animations;
- the intent blips;
- the boss death chain, the victory fanfare and the defeat;
- Mother Core's core open and core seal;
- all of Garganta's creature sounds (inhale, maw shut, bite, hurt, frenzy).

## 3. Shared rules

- **Round-robin:** play every id round-robin across its files, and never play the same file twice in a row.
- **Jitter:** give combat-tier plays a random `playbackRate` of 0.96–1.04 and volume ±1.5dB.
- **No jitter on choreographed clips:** `encounter_alarm`, `reveal_*`, `boss_warp_in`, `garganta_bite`, `boss_death`, `fleet_defeat`.
- **Buses:** add a **combat** bus at −6dB beside the existing dice −12, UI −9 and big 0. Each clip's `tier` says which bus it goes on.
- **Pack clip lengths:** I picked the pack clips by name, so their lengths are unknown. If any pack clip runs past its moment, fade it out at the next event rather than letting it overlap the next turn.
- **Clips marked *existing*** are already on R2 from the first SFX map. If one is missing, list it in your reply instead of substituting another clip.

## 4. Jump Gate v2

Delete the silent `tone()` hook and every `tone(...)` call.

| Where | Play |
|---|---|
| `countUp()`, each odd tick | *existing* `DSGNTonl_INTERFACE-Tonal Click`, +1 semitone per tick |
| `countUp()`, SECTOR SECURED | *existing* `DSGNMisc_SKILL IMPACT-Dramatic Finish` |
| `jump()`, at phase `'jump'` | `gate_jump_charge` |
| `jump()`, with the white flash | `gate_jump_exit` |
| `alarm()`, at the start | `encounter_alarm`; it ends as `reveal()` fires at +1100ms. Duck music −10dB for 1.2s |
| `reveal()`, at the start | `reveal_marauder` / `reveal_mothercore` / `reveal_garganta`. Each has hits built in at +0.22s (colour flash) and +0.96s (name slam) |
| `fight()` | `boss_engage` |
| `decoy()` | `gate_decoy` |
| `letGo()` | *existing* `DSGNTonl_USABLE-Coin Toss` |
| `settle()` with kind `'won'` | *existing* `Coin Toss`, then *existing* `DSGNTonl_USABLE-Whimsy Coin` (prestige) 150ms later |

`encounter_alarm_loop` is spare. Use it only if the reveal is ever gated on a tap: loop it from the OGG and stop it on the reveal.

## 5. Boss fights (all three files unless noted)

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
| `fireSeq()`, damage ship's `muzzle()` | by the ship's damage: `fleet_shot` (1), `fleet_shot_mid` (2–3), `fleet_shot_big` (4+). Bigger hits sound bigger, so the rule survives the card-only revision |
| `fireSeq()`, block ship firing | `shield_up` |
| `fireSeq()`, repair ship firing | *existing* `UIGlitch_USABLE-Mecha Repair` |
| `hitEnemy()` | `boss_hit_crit` if `exposed()`, else `boss_hit_heavy` if dmg ≥ 4, else `boss_hit` |
| `hurt()`, Garganta | layer `garganta_hurt` on the hit |
| `addBlock()` (SHIELDS UP) | `shield_up` |
| `heal()` (PATCH UP) | *existing* `UIGlitch_USABLE-Mecha Repair` |
| `hullHit()` with label `'MISS'` | *existing* `dice_die_land_hull` only, so a missed die never sounds like enemy fire |
| `hullHit()`, any other call | `hull_hit_heavy` if n ≥ 3, else `hull_hit` |
| `enemyTurn()`, Marauder, each `muzzle()` | `marauder_shot` |
| `enemyTurn()`, Mother Core, each `muzzle()` | `mothercore_shot` |
| `enemyTurn()`, atk 0, Marauder (CHARGING) | `marauder_charge` |
| `enemyTurn()`, atk 0, Mother Core (CORE SEALS) | `mothercore_core_seal` |
| `enemyTurn()`, atk 0, Garganta (MAW SHUTS) | `garganta_maw_shut` |
| `bite()`, Garganta | `garganta_bite` at the start (jaw snap built in at +385ms), plus `garganta_bite_layer` at +385ms |
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

## 6. Acceptance

- **Jump flow:** a takeoff whoosh on JUMP, the teleport sound on the white flash, three klaxon cycles, then the reveal stinger. Its first hit lands on the colour flash and its second on the name slam.
- **Volley:** a 1-damage ship and a 4-damage ship fire audibly different shots. Hits on an open core use Critical Strike.
- **CORE BEAM turn:** danger blips when the intent appears, six plasma shots 120ms apart, a heavy hull hit, then the beam release, then the detonation as the drone vanishes.
- **Garganta bite:** the generated snap and the Gore Cruncher land together on the jaw-shut frame, with no extra hull thud on top.
- **Missed die:** only the dice thud plays.
- **Repetition:** no file plays twice in a row across a fight.

Credit line, unchanged: "Sound effects: Helton Yan — Pixel Combat (CC BY 4.0)."
