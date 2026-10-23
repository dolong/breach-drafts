# Boss encounters

Open any .dc.html in a browser. Keep `support.js` and `assets/` in the same folder as the encounter files.

- **Marauder (Chance Encounter).dc.html** – baseline fight. HP 8/10/14. Its no-attack round ("Charging") gives no damage bonus.
- **Marauder Boarding Raid.dc.html** – v2 Marauder. Three lanes; dock up to 3 ships as guards (GUN: lane takes that number or higher · SHIELD: stops the first raider). Match a raider's number with a die to destroy it. A raider that reaches a ship drags it off; shoot it before it escapes to get the ship back. Empty lanes: -2 hull per boarder. Props: difficulty, captorSpeed (1/2 steps per round), skipIntro.
- **Mother Core Deflect.dc.html** – v3. Core with one ring of 4/5/6 numbered slots per layer (3 layers), fleet of up to 6 in an arc below (bigger fleets: 6 most recent fight). Beams lock on to ships each round with an "N+" badge; a die ≥ N on the badge deflects it, otherwise the ship is vaporized at END ROUND. Beams: 1, 2 after layer 1, 3 in Overdrive. SHIELD (Warden, Barnacle): beams need 2 less. GUN (Herald, Kestrel, Sovereign): +1 die per round while alive. Props: difficulty, fleetSize, skipIntro.
- **Mother Core Lock v2.dc.html** – column layout. Core on top, shield layers as rows over 4 columns (sector 2: 4/3/2 slots, sector 3: 4/4/3/2), one ship per column underneath. Only the bottom unbroken row is active; a ship drills the slot directly above it. Lit columns (1, then 2 after layer 2) fire at END ROUND. Any die moves a ship one column (swaps if occupied). Reserve ships refill lost columns. After the last layer, the core opens one slot whose number changes each round. Props: sector, fleetSize, skipIntro.
- **Mother Core Deflect v1.2.dc.html** – v1.1 with fewer slots on screen: only the current ring is shown (4 slots, one per ship spoke; last ring 2, then the core). Hidden rings appear as dim markers around the core. A turn moves a ring one slot so each ship faces a new number. A broken ring shatters and the next rises out of the core, numbers flipping in on the Ladder. Top bar is a "RING n / 3" counter. Wrecks no longer block a position.
- **Mother Core Deflect v1.1.dc.html** – visual pass on v1 (rings). Same rules. No outlines: rings shown only by colour-coded slots (outer blue, middle violet, inner red, matching the bar). Ships hover/drift/flicker, barrel-roll when moved. Beam telegraphed by the core's emitter swivelling + red charge glow + blinking lock-on reticle + trembling + warning tone; the beam is drawn only when it fires. Dodging a locked spot = NEAR MISS stamp on the Ladder. Kestrel: 1 free move per round. Cosmetic ambient potshots. Ring turn slides slots with a whoosh trail. Props: difficulty, sound, skipIntro.
- **Mother Core Deflect v1.dc.html** – copy of Mother Core Lock (v1 rings).
- **Mother Core Deflect v3.dc.html** – copy of Mother Core Deflect.
- **Mother Core Lock.dc.html** – v2 Mother Core. Radial board: 3 rings of numbered slots around the core, 4 ships on an 8-position orbit. A ship fills only the slots on its spoke; filled slots stay; a full ring shatters; rings turn 1 step per round (middle ring counter-clockwise). Lit spokes fire at round end and destroy the ship under them (Warden's shield absorbs one). Any die moves a ship 1 step. Wrecks block their position. After the last ring, fill the core's single slot to win.
- **Mother Core.dc.html** – boss. HP 16/20/26. "Core Exposed" round: your damage ×2. Overdrive at ≤50% HP: every attack +1.
- **Garganta Chase v2.dc.html** – no numbers on Garganta, no labels. Ships fly in a staggered, hovering formation (drag to reorder before launch); the one nearest the maw is the back ship. Distance is literal (auto-zooms to fit). The surge is a red danger zone rising from the maw: ships inside at END ROUND are eaten. Port dice push immediately; dice on the back ship's ports fire backward and shrink the zone. Warden at the back survives one bite. Drop unchanged. Win = reach the gate (it grows as you close in); +10 prestige per ship kept, UNTOUCHED ×1.5 run score.
- **Garganta Chase.dc.html** – v2 Garganta, The Chase. Vertical: gate above, Garganta's maw rising from below, your fleet a column in between (order chosen before the fight; the back is eaten first). Any die in a ship's port pushes the fleet up by its number (Kestrel 2 ports, Sovereign ×2). Three eyes on its head: match a number to hit, each hit slows the coming SURGE by 4. Ships the maw passes are eaten back-first. DROP a ship and it stops to eat, no surge that round. Reach the gate to escape, or put out all 3 eyes in one round: it sinks, the screen flips, fight it face-on for ×2. Props: difficulty, sound, skipIntro.
- **Garganta.dc.html** – hardest boss (v4). HP 18/22/28. "Inhales" round: your damage ×2. Frenzy at ≤50% HP: attacks +1. Heals +1 HP per round. Any bite that gets past your Block destroys one ship for the rest of the fight.

Shared rules: hull 8. Each round you pick a tactic card, roll dice, then place each die on a ship:
- Warden takes 1–2 (Block 2)
- Herald takes 3+ (1 damage)
- Kestrel takes 5+ (2 damage)
- Sovereign takes 6 (4 damage)

Any die you don't place hits your own hull for 1. Each enemy repeats a fixed 4-step attack pattern [A, B, 0, C]: two attacks, a no-attack round, then the big hit.

Difficulty (easy/normal/hard) and skipIntro are props at the top of each file.
