# Space Dice SFX

Mapped from **Helton Yan's Pixel Combat — Single Files**. 45 game events, 6 rotating
variants each = **270 sounds**, delivered as OGG (primary) + MP3 (fallback).

```
ogg/       270 × Vorbis q5, 44.1kHz 16-bit stereo   (7.1 MB total)
mp3/       270 × LAME V4 ~165kbps                   (5.9 MB total)
src-wav/   270 × original 96kHz/24-bit WAV          (499 MB — reference only, safe to delete)
manifest.json   event → files, tier, gain, duration, source stem, design note
```

Clip lengths are 0.30s–2.89s (368s of audio total). The sources were all padded to a
flat 2.5s; that padding is gone.

## Naming

`<group>_<event>_<NN>.ogg` — e.g. `dice_roll_shake_03.ogg`, `big_breach_explosion_01.ogg`.
Groups: `dice`, `hull`, `big`, `card`, `econ`, `ui`, `route`.
Variants are `_01`–`_06`; rotate them so repeated events never sound identical.

## Volume tiers (already baked into the files)

| tier | gain | applies to |
| --- | --- | --- |
| `dice` | −12 dB | all dice sounds + the hull heartbeat loop |
| `ui` | −9 dB | cards, economy, UI, route/race, hull warnings |
| `big` | 0 dB | breach, run over, launch, jettison, greed bonus |

Play everything at unity gain — the separation is in the files. Measured peaks by group:

```
big    -11.4 .. -1.0 dBFS      card   -22.2 .. -10.5
dice   -26.7 .. -12.7          econ   -19.4 ..  -9.6
hull   -22.2 ..  -9.5          route  -23.2 .. -10.9
ui     -20.5 .. -10.2
```

Nothing clips; loudest file is −1.0 dBFS.

## Processing notes

- Resampled 96k → 44.1k **before** the tier gain, so the tier offsets are exact. Resampling
  a bitcrushed transient costs ~7 dB of peak on its own; applying gain first makes the tiers drift.
- **No fade-in.** A 3 ms fade cost ~7 dB of attack on short clicks — on this pack the transient
  *is* the sound. Sources start at sample 0 with no DC offset, so there is no click risk.
- **Trailing silence trimmed** at −70 dB keeping a 150 ms tail, then an 8 ms fade-out anchored
  at the real end so the cut cannot click. Every source was padded to a flat 2.5 s — a UI click
  was 0.24 s of audio and 2.26 s of nothing. This barely changes OGG size (Vorbis compresses
  silence to almost nothing) but it matters at runtime: `onended` now fires when the sound
  actually stops instead of seconds later, and voice slots free up immediately.
- Leading-silence trim at −60 dB is in the chain but was a no-op: none of these sources have
  leading silence.
- True-peak limited at −0.1 dBFS as a clip guard for the 0 dB tier.
- Tier gain is applied to the **delivered** (44.1k) audio, so `−12 / −9 / 0` are exact
  offsets from each source's own post-resample peak, preserving Helton Yan's balance
  *within* each tier rather than flattening everything to one level.

## Still to do in code (per the design map)

These are pitch/timing effects, not separate files — apply at playback:

- `dice_die_land_slot` — pitch **+2 semitones** on the last die of a roll
- `dice_die_land_hull` — pitch **down** as the hull total rises
- `hull_hull_heartbeat` — loop at **60 bpm**, low volume, only while hull is 6–7
- `big_breach_shatter` — fire **80 ms after** `big_breach_explosion`
- `big_run_over` — follow with **1 full second of silence**
- `big_launch_reveal` — fire after `big_launch_ignition`, on the ship reveal
- `card_asteroid_extra_roll` — pitch **up** on each repeat
- `ui_counter_tick` — pitch **up a semitone per tick**
- `dice_reroll_swipe` + `dice_reroll_coin` — **layered**, played together
- `econ_coin_fly` per coin, then `econ_coin_land` on landing

## Loading

`manifest.json` is keyed by event name and lists every variant path:

```js
const man = await (await fetch('manifest.json')).json();
const canOgg = !!new Audio().canPlayType('audio/ogg; codecs="vorbis"');
const pick = ev => {
  const e = man.events[ev];
  const list = canOgg ? e.ogg : e.mp3;
  return list[(Math.random() * list.length) | 0];
};
new Audio(pick('dice_roll_shake')).play();
```
