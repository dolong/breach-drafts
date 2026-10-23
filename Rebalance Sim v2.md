# Boss rebalance v2 (one life per ship) — simulation

1500 fights per cell. Each cell: win % / ships lost / rounds. S, E, B = short, expected, big fleet.

Setup: opening barrage off. Gold 80/120/160. Fleet = the real ship order (Herald Deflector, Warden Decoy, Kestrel Redline, Sovereign Bounty, Barnacle Broadside, Siren Deflector). Bot plays the highest-value card (wing fire and ×2 counted), Deflector when 2+ hits or a beam/devour is incoming, and one 10-gold reroll on a 1. Volley 1s do not count as misfires.

Final cycles: Mother Core S2 [2, 2, BEAM, EXPOSED] · Garganta S2 [2, 2, DEVOUR, INHALE] · Garganta S3 [2, DEVOUR, 3, DEVOUR, INHALE]. Everything else as briefed.

## Marauder S1

| Rank | 1 | 2 | 3 | 4 | 5 | 6 | Expected | Target |
|---|---|---|---|---|---|---|---|---|
| Cadet | S 21 / 0.8 / 2.1 | E 92 / 0.3 / 1.5 | E 95 / 0.5 / 2.5 | B 100 / 0.1 / 2.2 | B 100 / 0.2 / 2.2 | B 100 / 0.3 / 2.4 | **93% / 0.4** | 95% / 0.2 ✓ |
| Lieutenant | S 22 / 0.8 / 2.2 | E 94 / 0.2 / 1.5 | E 97 / 0.3 / 2.5 | B 100 / 0.1 / 2.2 | B 100 / 0.1 / 2.3 | B 100 / 0.2 / 2.4 | **95% / 0.3** | — |
| Commander | S 23 / 0.8 / 2.1 | E 95 / 0.2 / 1.5 | E 99 / 0.2 / 2.5 | B 100 / 0.0 / 2.2 | B 100 / 0.1 / 2.2 | B 100 / 0.1 / 2.4 | **97% / 0.2** | — |

## Marauder S2

| Rank | 1 | 2 | 3 | 4 | 5 | 6 | Expected | Target |
|---|---|---|---|---|---|---|---|---|
| Cadet | S 1 / 1.0 / 2.3 | S 24 / 1.7 / 3.5 | E 85 / 1.2 / 2.1 | E 98 / 1.3 / 2.5 | B 99 / 1.5 / 2.8 | B 100 / 1.7 / 3.1 | **91% / 1.2** | 87% / 1.5 ✓ |
| Lieutenant | S 1 / 1.0 / 2.3 | S 30 / 1.6 / 3.9 | E 92 / 0.7 / 2.1 | E 99 / 0.8 / 2.5 | B 100 / 1.0 / 2.8 | B 100 / 1.1 / 3.1 | **96% / 0.8** | 93% / 1 ✓ |
| Commander | S 1 / 1.0 / 2.3 | S 34 / 1.5 / 4.1 | E 97 / 0.4 / 2.1 | E 100 / 0.5 / 2.5 | B 100 / 0.5 / 2.8 | B 100 / 0.6 / 3.0 | **98% / 0.4** | 97% / 0.6 ✓ |

## Marauder S3

| Rank | 1 | 2 | 3 | 4 | 5 | 6 | Expected | Target |
|---|---|---|---|---|---|---|---|---|
| Cadet | S 0 / 1.0 / 1.8 | S 6 / 1.9 / 2.9 | S 5 / 2.9 / 4.1 | E 73 / 2.3 / 4.7 | E 87 / 2.4 / 4.8 | B 98 / 1.9 / 4.0 | **80% / 2.4** | 76% / 2.6 ✓ |
| Lieutenant | S 0 / 1.0 / 1.8 | S 7 / 1.9 / 3.2 | S 16 / 2.7 / 5.2 | E 87 / 1.5 / 4.9 | E 96 / 1.5 / 5.0 | B 100 / 1.2 / 3.9 | **92% / 1.5** | 89% / 1.7 ✓ |
| Commander | S 0 / 1.0 / 1.8 | S 11 / 1.9 / 3.7 | S 36 / 2.3 / 6.6 | E 96 / 0.8 / 5.0 | E 99 / 0.9 / 5.0 | B 100 / 0.6 / 3.8 | **98% / 0.8** | 97% / 0.9 ✓ |
| Admiral (5–6, 3 roll) | S 0 / 1.0 / 1.8 | S 8 / 1.9 / 3.2 | S 14 / 2.8 / 5.1 | E 90 / 1.2 / 4.9 | E 98 / 1.0 / 5.0 | B 100 / 0.8 / 3.9 | **94% / 1.1** | — |
| Admiral (4–6, 3 roll) | S 0 / 1.0 / 1.8 | S 12 / 1.8 / 3.7 | S 33 / 2.3 / 6.6 | E 98 / 0.5 / 5.0 | E 100 / 0.4 / 5.0 | B 100 / 0.3 / 3.8 | **99% / 0.5** | — |

## Mother Core S1

| Rank | 1 | 2 | 3 | 4 | 5 | 6 | Expected | Target |
|---|---|---|---|---|---|---|---|---|
| Cadet | S 2 / 1.0 / 2.0 | E 45 / 1.5 / 2.2 | E 62 / 1.9 / 3.0 | B 45 / 3.0 / 4.4 | B 64 / 3.3 / 4.6 | B 67 / 4.0 / 5.5 | **53% / 1.7** | 48% / 1.6 ✓ |
| Lieutenant | S 2 / 1.0 / 2.0 | E 50 / 1.4 / 2.4 | E 74 / 1.4 / 3.3 | B 67 / 2.3 / 4.8 | B 85 / 2.3 / 5.0 | B 86 / 2.7 / 5.8 | **62% / 1.4** | — |
| Commander | S 2 / 1.0 / 2.0 | E 55 / 1.3 / 2.7 | E 87 / 0.9 / 3.5 | B 85 / 1.4 / 5.2 | B 95 / 1.4 / 5.3 | B 97 / 1.5 / 5.9 | **71% / 1.1** | — |

## Mother Core S2

| Rank | 1 | 2 | 3 | 4 | 5 | 6 | Expected | Target |
|---|---|---|---|---|---|---|---|---|
| Cadet | S 0 / 1.0 / 1.2 | S 3 / 2.0 / 2.0 | E 34 / 2.4 / 4.9 | E 47 / 3.0 / 5.5 | B 31 / 4.3 / 4.5 | B 32 / 5.3 / 5.7 | **40% / 2.7** | 41% / 2.6 ✓ |
| Lieutenant | S 0 / 1.0 / 1.3 | S 6 / 1.9 / 2.3 | E 51 / 2.0 / 5.6 | E 70 / 2.2 / 6.1 | B 61 / 3.4 / 5.5 | B 62 / 4.1 / 6.8 | **60% / 2.1** | 67% / 1.8 ✓ |
| Commander | S 0 / 1.0 / 1.2 | S 11 / 1.8 / 2.7 | E 70 / 1.4 / 6.4 | E 86 / 1.4 / 6.6 | B 86 / 2.1 / 6.2 | B 90 / 2.4 / 7.4 | **78% / 1.4** | 84% / 1 ✓ |

## Mother Core S3

| Rank | 1 | 2 | 3 | 4 | 5 | 6 | Expected | Target |
|---|---|---|---|---|---|---|---|---|
| Cadet | S 0 / 1.0 / 1.2 | S 0 / 2.0 / 2.1 | S 2 / 3.0 / 3.3 | E 21 / 3.6 / 6.8 | E 39 / 4.1 / 7.4 | B 13 / 5.7 / 6.5 | **30% / 3.9** | 27% / 3.8 ✓ |
| Lieutenant | S 0 / 1.0 / 1.2 | S 1 / 2.0 / 2.4 | S 6 / 2.9 / 4.3 | E 45 / 3.0 / 7.9 | E 68 / 3.1 / 8.5 | B 36 / 5.0 / 8.4 | **57% / 3.0** | 61% / 2.6 ✓ |
| Commander | S 0 / 1.0 / 1.2 | S 2 / 2.0 / 2.9 | S 20 / 2.6 / 6.0 | E 74 / 1.9 / 9.3 | E 91 / 1.8 / 9.2 | B 73 / 3.4 / 10.2 | **82% / 1.8** | 86% / 1.4 ✓ |
| Admiral (5–6, 3 roll) | S 0 / 1.0 / 1.2 | S 1 / 2.0 / 2.4 | S 6 / 2.9 / 4.3 | E 56 / 2.5 / 8.5 | E 80 / 2.4 / 8.9 | B 56 / 4.1 / 9.4 | **68% / 2.4** | — |
| Admiral (4–6, 3 roll) | S 0 / 1.0 / 1.2 | S 2 / 2.0 / 3.0 | S 19 / 2.6 / 5.9 | E 84 / 1.3 / 9.6 | E 97 / 1.0 / 9.4 | B 92 / 1.9 / 10.8 | **90% / 1.1** | — |

## Garganta S1

| Rank | 1 | 2 | 3 | 4 | 5 | 6 | Expected | Target |
|---|---|---|---|---|---|---|---|---|
| Cadet | S 1 / 1.0 / 2.0 | E 13 / 1.8 / 2.5 | E 45 / 2.2 / 3.3 | B 47 / 2.9 / 4.0 | B 69 / 3.1 / 4.1 | B 83 / 3.3 / 5.1 | **29% / 2.0** | 33% / 1.9 ✓ |
| Lieutenant | S 0 / 1.0 / 2.0 | E 24 / 1.7 / 2.6 | E 61 / 1.7 / 3.5 | B 70 / 2.1 / 4.5 | B 88 / 2.1 / 4.6 | B 95 / 2.2 / 5.4 | **43% / 1.7** | — |
| Commander | S 1 / 1.0 / 2.0 | E 39 / 1.4 / 2.9 | E 79 / 1.1 / 3.7 | B 92 / 1.1 / 5.1 | B 98 / 1.2 / 5.0 | B 99 / 1.2 / 5.6 | **59% / 1.3** | — |

## Garganta S2

| Rank | 1 | 2 | 3 | 4 | 5 | 6 | Expected | Target |
|---|---|---|---|---|---|---|---|---|
| Cadet | S 0 / 1.0 / 1.2 | S 2 / 2.0 / 2.0 | E 34 / 2.4 / 4.6 | E 43 / 3.0 / 5.2 | B 43 / 4.0 / 4.1 | B 52 / 4.6 / 5.8 | **39% / 2.7** | 34% / 2.6 ✓ |
| Lieutenant | S 0 / 1.0 / 1.2 | S 3 / 2.0 / 2.3 | E 48 / 2.0 / 5.5 | E 69 / 2.2 / 6.1 | B 75 / 2.8 / 5.3 | B 79 / 3.2 / 6.8 | **58% / 2.1** | 62% / 1.7 ✓ |
| Commander | S 0 / 1.0 / 1.2 | S 6 / 1.9 / 2.8 | E 69 / 1.4 / 6.6 | E 88 / 1.3 / 6.8 | B 95 / 1.6 / 6.2 | B 95 / 1.8 / 7.2 | **79% / 1.4** | 83% / 0.9 ✓ |

## Garganta S3

| Rank | 1 | 2 | 3 | 4 | 5 | 6 | Expected | Target |
|---|---|---|---|---|---|---|---|---|
| Cadet | S 0 / 1.0 / 1.2 | S 0 / 2.0 / 1.9 | S 1 / 3.0 / 3.0 | E 14 / 3.7 / 5.2 | E 35 / 4.2 / 5.8 | B 16 / 5.6 / 6.2 | **24% / 3.9** | 24% / 3.6 ✓ |
| Lieutenant | S 0 / 1.0 / 1.2 | S 0 / 2.0 / 2.2 | S 5 / 2.9 / 3.9 | E 35 / 3.2 / 6.9 | E 65 / 3.2 / 7.2 | B 48 / 4.6 / 8.5 | **50% / 3.2** | 61% / 2.2 ✗ |
| Commander | S 0 / 1.0 / 1.2 | S 1 / 2.0 / 2.8 | S 18 / 2.7 / 5.8 | E 69 / 2.1 / 8.9 | E 89 / 1.9 / 8.5 | B 84 / 2.8 / 10.2 | **79% / 2.0** | 87% / 1.1 ✗ |
| Admiral (5–6, 3 roll) | S 0 / 1.0 / 1.2 | S 0 / 2.0 / 2.2 | S 6 / 2.9 / 3.9 | E 43 / 2.9 / 7.7 | E 77 / 2.5 / 8.3 | B 68 / 3.6 / 9.5 | **60% / 2.7** | — |
| Admiral (4–6, 3 roll) | S 0 / 1.0 / 1.2 | S 0 / 2.0 / 2.7 | S 19 / 2.6 / 5.8 | E 77 / 1.6 / 9.6 | E 96 / 1.1 / 9.5 | B 95 / 1.5 / 10.6 | **86% / 1.3** | — |

## SHORT fleets, Sectors 2–3 (Cadet)

- Marauder S2 1 ship: 1%
- Marauder S2 2 ships: 24%
- Marauder S3 1 ship: 0%
- Marauder S3 2 ships: 6%
- Marauder S3 3 ships: 5%
- Mother Core S2 1 ship: 0%
- Mother Core S2 2 ships: 3%
- Mother Core S3 1 ship: 0%
- Mother Core S3 2 ships: 0%
- Mother Core S3 3 ships: 2%
- Garganta S2 1 ship: 0%
- Garganta S2 2 ships: 2%
- Garganta S3 1 ship: 0%
- Garganta S3 2 ships: 0%
- Garganta S3 3 ships: 1%

## Admiral, Sector 3

- Marauder Admiral (5–6, 3 roll): 94/1.1
- Marauder Admiral (4–6, 3 roll): 99/0.5
- Mother Core Admiral (5–6, 3 roll): 68/2.4
- Mother Core Admiral (4–6, 3 roll): 90/1.1
- Garganta Admiral (5–6, 3 roll): 60/2.7
- Garganta Admiral (4–6, 3 roll): 86/1.3
