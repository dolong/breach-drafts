"""Breach boss-battle SFX recipes. Each recipe returns a mono float array at 44.1 kHz."""
import numpy as np
import dsp
from dsp import (SR, N, tt, mtof, canvas, place, ad, pts, gate, glide, osc, noise, sh_noise, metal_noise,
                 smooth_rand, lp, hp, bp, svf, drive, crush, echo, verb, kick, laser, ring, crackle, boom,
                 growl, note)

REG = []


def sfx(id, tier, event, trigger, loop=False, keep_len=False, variants=0, target=-15.0):
    def deco(fn):
        REG.append(dict(id=id, fn=fn, tier=tier, event=event, trigger=trigger, loop=loop,
                        keep_len=keep_len, variants=variants, target=target))
        return fn
    return deco


def R():
    return dsp.rng


def curve(points, d, log=True):
    t = tt(d)
    ts = [p[0] for p in points]
    vs = np.array([p[1] for p in points], float)
    return np.exp(np.interp(t, ts, np.log(vs))) if log else np.interp(t, ts, vs)


def vacuum(d=0.2, gain=0.5):
    """the black-flash suck-in before a reveal"""
    return hp(noise(d), 1500) * pts([(0, 0), (d * 0.95, gain), (d, 0)], d)


def snap(dense=1.0):
    y = canvas(0.06)
    for i, dt_ in enumerate([0, 0.007, 0.017, 0.03][: 3 + int(dense > 1)]):
        place(y, hp(noise(0.006), 1500) * ad(0.006, 0.0002, 3), dt_, 1 - 0.22 * i)
    return y


def stab(root_m, d, notes=(0, 7, 12), bend_cents=100, cut=3500, amt=2.5):
    t = tt(d)
    bend = 2 ** ((bend_cents * np.exp(-t / 0.03)) / 1200)
    s = sum(osc(mtof(root_m + n) * bend * (1 + 0.003 * i), "saw") for i, n in enumerate(notes))
    return drive(lp(s, cut) * ad(d, 0.002, 3.5) * 0.5, amt)


def fm(fc, fmod, idx0, d, decay=3.0):
    t = tt(d)
    if np.isscalar(fc):
        fc = np.full_like(t, float(fc))
    idx = idx0 * np.exp(-decay * t / d)
    ph = 2 * np.pi * np.cumsum(fc) / SR
    return np.sin(ph + np.sin(2 * np.pi * fmod * t) * idx)


def klax(f, d=0.14):
    t = tt(d)
    fa = f * 2 ** ((-40 * np.exp(-t / 0.012)) / 1200)  # scoop up into the note
    a = osc(fa, "square", 0.25) + 0.55 * osc(fa * 0.5, "square", 0.5) + 0.22 * osc(fa * 2.0, "square", 0.125)
    return a * gate(d, 0.002, 0.01)


def am(d, rate_curve, depth=0.5, square=False):
    ph = 2 * np.pi * np.cumsum(np.broadcast_to(rate_curve, (N(d),))) / SR
    m = np.sign(np.sin(ph)) if square else np.sin(ph)
    return 1 - depth * (0.5 + 0.5 * m)


# ════════════════ ENCOUNTER FLOW (Jump Gate v2) ════════════════

@sfx("gate_jump_charge", "big", "Ships stream into the gate", "Jump Gate v2 · jump() — at phase 'jump' (replaces tone(180 → 900 saw))")
def gate_jump_charge(v):
    d = 0.95
    t = tt(d)
    f = curve([(0, 180), (0.72, 900), (0.95, 900)], d)
    s = osc(f, "saw") + 0.7 * osc(f * 1.004, "saw") + 0.4 * osc(f * 0.5, "square")
    s = svf(s * 0.4, curve([(0, 500), (0.72, 7000), (0.95, 5000)], d), 1.4, "lp")
    s *= am(d, curve([(0, 7), (0.95, 32)], d), 0.35)
    s *= pts([(0, 0), (0.05, 0.35), (0.72, 1.0), (0.86, 0.9), (0.95, 0)], d)
    riser = hp(noise(d), 3000) * pts([(0, 0), (0.72, 0.5), (0.95, 0)], d)
    return crush(s + riser * 0.5, 7)


@sfx("gate_jump_exit", "big", "White flash as the fleet exits the gate", "Jump Gate v2 · jump() — with the white flash at t (replaces tone(1200 → 300 triangle))")
def gate_jump_exit(v):
    y = canvas(0.75)
    zap = osc(glide(1200, 300, 0.25, tau=0.08), "tri_smooth") * ad(0.25, 0.001, 3)
    place(zap, osc(glide(2400, 600, 0.2, tau=0.06), "square", 0.125) * ad(0.2, 0.001, 4), 0, 0.5)
    place(y, zap, 0, 0.8)
    place(y, hp(noise(0.3), 2500) * ad(0.3, 0.001, 5), 0, 0.5)
    place(y, kick(90, 35, 0.4, tau=0.06), 0, 0.9)
    place(y, ring(1760, 0.6, decay=5), 0, 0.15)
    return verb(y, 0.25, 1.0, tail=0.3)


def _alarm_bus(d, cycles, with_impact=True, drone_f=110.0):
    y = canvas(d)
    kl = canvas(d)
    for c in cycles:
        place(kl, klax(660), c, 0.55)
        place(kl, klax(440), c + 0.14, 0.55)
    kl = lp(crush(kl * 0.6, 6) / 0.6, 6500)
    place(y, kl, 0, 1.0)
    drone = lp(osc(drone_f, "saw", d=d), 600)
    if with_impact:
        drone *= pts([(0, 0), (0.05, 0.25), (0.84, 0.25), (d, 0)], d)
        place(y, kick(120, 32, 0.45, tau=0.05, click=0.4), 0, 1.0)
        place(y, boom(1.0, d=0.35), 0, 0.3)
        place(y, kick(80, 30, 0.3, tau=0.05, click=0.1), 0.42, 0.5)  # second shudder
    else:
        drone *= 0.25
    place(y, drone, 0, 0.5)
    return y


@sfx("encounter_alarm", "big", "SURPRISE ENCOUNTER — gate flips red, ship-wide klaxon", "Jump Gate v2 · alarm() (replaces the three 660/440 square tone pairs)")
def encounter_alarm(v):
    y = _alarm_bus(1.25, [0, 0.28, 0.56])
    return echo(y, 0.085, 0.28, 4)


@sfx("encounter_alarm_loop", "big", "Seamless klaxon loop, if the alarm ever needs to hold longer than 1.1s", "Optional — loop while waiting (e.g. if reveal is ever gated on a tap)", loop=True)
def encounter_alarm_loop(v):
    P = 0.56
    y = _alarm_bus(3 * P, [k * 0.28 for k in range(6)], with_impact=False, drone_f=62 / P)
    y = echo(y, 0.085, 0.28, 4)
    return y[N(P): N(P) + N(P)]


@sfx("reveal_marauder", "big", "Marauder reveal stinger — corsair power-chord, name slam at 0.96s", "Jump Gate v2 · reveal() when boss = marauder (replaces both reveal tones)")
def reveal_marauder(v):
    y = canvas(1.9)
    place(y, vacuum(), 0, 0.5)
    place(y, stab(45, 0.7), 0.2, 0.55)
    place(y, kick(130, 35, 0.5, tau=0.05, click=0.5), 0.2, 0.9)
    place(y, boom(1.5, d=0.5), 0.2, 0.35)
    place(y, lp(osc(glide(80, 40, 0.9), "saw") * ad(0.9, 0.01, 2.5), 900), 0.2, 0.4)
    for i, m in enumerate([69, 67, 64, 62]):
        place(y, note(mtof(m), 0.085, "square", 0.25, r=0.01), 0.52 + i * 0.1, 0.2)
    place(y, osc(glide(110, 70, 0.3), "square") * ad(0.3, 0.002, 3), 0.96, 0.4)
    place(y, kick(140, 30, 0.6, tau=0.05, click=0.6), 0.96, 1.0)
    place(y, stab(33, 0.8), 0.96, 0.55)
    place(y, hp(noise(0.12), 2000) * ad(0.12, 0.001, 4), 0.96, 0.4)
    return verb(y, 0.3, 1.2, tail=0.5)


@sfx("reveal_mothercore", "big", "Mother Core reveal stinger — FM foundry hit, scanning arpeggio, metal slam at 0.96s", "Jump Gate v2 · reveal() when boss = mothercore (replaces both reveal tones)")
def reveal_mothercore(v):
    y = canvas(2.0)
    place(y, vacuum(), 0, 0.5)
    place(y, fm(55, 110, 9, 1.0, 4) * ad(1.0, 0.002, 3), 0.2, 0.8)
    place(y, ring(440, 1.2, decay=5), 0.2, 0.3)
    place(y, kick(120, 32, 0.5, click=0.4), 0.2, 0.8)
    place(y, lp(osc(glide(80, 40, 0.9), "saw") * ad(0.9, 0.01, 2.5), 700), 0.2, 0.35)
    for i, m in enumerate([69, 72, 74, 76, 79, 81, 84, 86, 88, 91]):
        place(y, note(mtof(m), 0.035, "square", 0.125, r=0.008), 0.42 + i * 0.05, 0.12)
    place(y, osc(glide(110, 70, 0.3), "square") * ad(0.3, 0.002, 3), 0.96, 0.4)
    place(y, kick(150, 30, 0.6, click=0.5), 0.96, 1.0)
    place(y, lp(metal_noise(0.35, glide(3500, 1200, 0.35), 93), 5000) * ad(0.35, 0.001, 5), 0.96, 0.45)
    place(y, fm(55, 82.5, 6, 0.9, 3) * ad(0.9, 0.002, 2.5), 0.96, 0.6)
    t = tt(0.9)
    hum = (np.sin(2 * np.pi * 55 * t) + np.sin(2 * np.pi * 55.8 * t)) * pts([(0, 0), (0.1, 0.3), (0.9, 0)], 0.9)
    place(y, hum, 1.1, 0.5)
    return verb(y, 0.35, 1.3, tail=0.5)


@sfx("reveal_garganta", "big", "Garganta reveal stinger — low growl and sub drop, jaw snap at 0.96s", "Jump Gate v2 · reveal() when boss = garganta (replaces both reveal tones)")
def reveal_garganta(v):
    y = canvas(2.1)
    place(y, vacuum(), 0, 0.5)
    g = growl(1.0, 95, 62, rough=30) * pts([(0, 0), (0.06, 1), (0.6, 0.7), (1.0, 0)], 1.0)
    place(y, g, 0.2, 0.9)
    place(y, lp(osc(glide(55, 40, 0.9), "saw") * ad(0.9, 0.01, 2.2), 500), 0.2, 0.7)
    place(y, kick(90, 28, 0.7, tau=0.07, click=0.2), 0.2, 1.0)
    place(y, snap(2), 0.96, 0.8)
    place(y, osc(glide(110, 70, 0.3), "square") * ad(0.3, 0.002, 3), 0.96, 0.3)
    place(y, kick(110, 25, 0.7, tau=0.06, click=0.3), 0.96, 1.0)
    place(y, growl(0.9, 120, 55, rough=38) * ad(0.9, 0.01, 2.5), 0.96, 0.8)
    return verb(y, 0.35, 1.5, tail=0.6, damp=2500)


@sfx("boss_engage", "combat", "FIGHT / ENGAGE confirm — short power stab", "Jump Gate v2 · fight(); boss files · engage()")
def boss_engage(v):
    y = canvas(0.6)
    place(y, stab(45, 0.45, cut=4500), 0, 0.6)
    place(y, kick(140, 40, 0.3, click=0.5), 0, 0.8)
    place(y, hp(noise(0.05), 2500) * ad(0.05, 0.0005, 4), 0, 0.4)
    place(y, note(mtof(81), 0.05, "square", 0.25, r=0.01), 0.03, 0.15)
    place(y, note(mtof(88), 0.08, "square", 0.25, r=0.02), 0.09, 0.15)
    return y


@sfx("gate_decoy", "combat", "DECOY — flare launches, pops, fizzes, beacon pings", "Jump Gate v2 · decoy()")
def gate_decoy(v):
    y = canvas(1.0)
    wh = svf(noise(0.3), glide(500, 4500, 0.3), 2.0, "bp") * pts([(0, 0), (0.2, 1), (0.3, 0)], 0.3)
    place(y, wh, 0, 0.7)
    place(y, boom(0.6, d=0.3, bright=1.3), 0.27, 0.5)
    fz = hp(noise(0.65), 3500) * pts([(0, 0), (0.02, 0.35), (0.65, 0)], 0.65) + crackle(0.65, 140, 1, 0.1, 3000) * 0.8
    place(y, fz, 0.3, 0.5)
    for dt_ in [0.38, 0.58]:
        place(y, note(1760, 0.05, "square", 0.25, r=0.01), dt_, 0.15)
        place(y, note(2637, 0.05, "square", 0.25, r=0.01), dt_ + 0.055, 0.1)
    return y


# ════════════════ FIGHT — SHARED ════════════════

@sfx("boss_warp_in", "big", "Boss materialises — reverse swell into impact at 0.42s", "boss files · warpIn() (flash lands at +420ms)")
def boss_warp_in(v):
    y = canvas(1.05)
    d = 0.42
    t = tt(d)
    sw = osc(glide(200, 1400, d), "saw") * 0.5 + hp(noise(d), 1000) * 0.7
    sw = svf(sw, glide(400, 8000, d), 1.2, "lp") * (t / d) ** 2.2
    place(y, sw, 0, 0.8)
    place(y, kick(130, 30, 0.5, click=0.5), d, 1.0)
    place(y, boom(1.2, d=0.45), d, 0.5)
    place(y, osc(glide(1600, 200, 0.3, tau=0.07), "square", 0.25) * ad(0.3, 0.001, 4), d, 0.25)
    place(y, ring(880, 0.6, decay=6), d, 0.2)
    return verb(y, 0.25, 1.1, tail=0.3)


@sfx("boss_intent", "ui", "New boss intent shown (FIRES n / BITES n)", "boss files · startRound() when the NEXT tag changes")
def boss_intent(v):
    y = canvas(0.3)
    place(y, note(1318.5, 0.05, "square", 0.125, r=0.01), 0, 0.5)
    place(y, note(987.8, 0.07, "square", 0.125, r=0.02), 0.075, 0.45)
    place(y, kick(200, 80, 0.08, click=0), 0, 0.3)
    return y


@sfx("boss_intent_danger", "combat", "Big intent shown — CORE BEAM / DEVOUR / FIRES 4+", "boss files · startRound() when the intent is the max or ≥4")
def boss_intent_danger(v):
    y = canvas(0.8)
    for i in range(3):
        t = tt(0.08)
        f = 1568 * 2 ** ((-30 * t / 0.08) / 1200)
        place(y, osc(f, "square", 0.25) * gate(0.08, 0.002, 0.01), i * 0.12, 0.45)
        place(y, lp(osc(110, "square", d=0.09), 900) * gate(0.09, 0.002, 0.02), i * 0.12, 0.35)
    t = tt(0.45)
    threat = np.sin(2 * np.pi * 55 * t) * pts([(0, 0), (0.1, 1), (0.45, 0)], 0.45)
    place(y, threat, 0.32, 0.5)
    return crush(y, 7)


@sfx("fleet_shot", "combat", "Your ship fires a bolt", "boss files · fireSeq() → muzzle(); one play per ship (340ms apart)", variants=4)
def fleet_shot(v):
    f0 = [1800, 1500, 2100, 1650][v]
    f1 = [320, 280, 380, 300][v]
    tau = [0.035, 0.045, 0.03, 0.04][v]
    duty = [0.25, 0.125, 0.25, 0.5][v]
    s = laser(f0, f1, 0.22, tau, "square", duty)
    place(s, laser(f0 * 1.5, f1 * 1.5, 0.12, tau * 0.8, "square", 0.5), 0, 0.35)
    place(s, hp(noise(0.02), 3000) * ad(0.02, 0.0005, 3), 0, 0.5)
    return echo(crush(s, 7), 0.06, 0.25, 3, tail=0.12)


@sfx("boss_hit", "combat", "Bolt hits the boss", "boss files · hitEnemy() when dmg < 4 and not ×2", variants=3)
def boss_hit(v):
    y = canvas(0.32)
    n = sh_noise(0.14, glide(9000, 1800, 0.14, tau=0.04)) * ad(0.14, 0.001, 3.5)
    place(y, n, 0, 0.8)
    place(y, osc(glide(240 - 20 * v, 70, 0.14, tau=0.03), "square") * ad(0.14, 0.001, 4), 0, 0.5)
    place(y, ring(1200 + v * 170, 0.18, decay=7), 0, 0.3)
    return drive(y, 1.8)


@sfx("boss_hit_heavy", "combat", "Heavy hit on the boss", "boss files · hitEnemy() when dmg ≥ 4 (same moment as the bigger shake)")
def boss_hit_heavy(v):
    y = canvas(0.6)
    place(y, crush(boom(1.3, d=0.5), 6), 0, 0.7)
    place(y, kick(140, 30, 0.5, click=0.5), 0, 0.9)
    place(y, osc(glide(300, 60, 0.25, tau=0.05), "square") * ad(0.25, 0.001, 3.5), 0, 0.4)
    return drive(y, 1.6)


@sfx("boss_hit_crit", "combat", "×2 hit on an open core / inhaling maw", "boss files · hitEnemy() when exposed() is true (play instead of boss_hit)")
def boss_hit_crit(v):
    y = canvas(0.75)
    place(y, kick(150, 32, 0.45, click=0.6), 0, 0.9)
    place(y, boom(1.1, d=0.4, bright=1.3), 0, 0.5)
    place(y, ring(1500, 0.6, decay=4.5), 0, 0.45)
    place(y, ring(2250, 0.45, decay=5), 0.005, 0.25)
    place(y, note(1760, 0.06, "square", 0.125, r=0.015), 0.05, 0.22)
    place(y, note(2637, 0.12, "square", 0.125, r=0.04), 0.11, 0.22)
    return verb(y, 0.2, 0.9, tail=0.2)


@sfx("shield_up", "combat", "Block added — SHIELDS UP card or a block ship firing", "boss files · addBlock() / shieldFx()")
def shield_up(v):
    d = 0.65
    t = tt(d)
    f = curve([(0, 440), (0.45, 1320), (0.65, 1320)], d)
    vib = 2 ** ((20 / 1200) * np.sin(2 * np.pi * 9 * t))
    s = osc(f * vib, "tri_smooth") + 0.6 * osc(f * 1.5 * vib * 1.003, "tri_smooth") + 0.25 * osc(f * 2.0, "square", 0.125)
    amp = pts([(0, 0), (0.05, 0.8), (0.45, 1), (0.65, 0)], d)
    sh = hp(noise(d), 6000) * amp * 0.25 * (0.5 + 0.5 * np.sin(2 * np.pi * 24 * t))
    y = s * amp * 0.4 + sh
    place(y, ring(2637, 0.25, decay=6), 0.4, 0.25)
    return y


@sfx("shield_block", "combat", "Incoming damage BLOCKED — deflect ting and ricochet", "boss files · resolveEnemy() when blocked > 0")
def shield_block(v):
    y = canvas(0.45)
    place(y, ring(1800, 0.4, decay=7), 0, 0.6)
    place(y, osc(glide(900, 2600, 0.12), "square", 0.125) * ad(0.12, 0.001, 2.5), 0.01, 0.25)
    place(y, hp(noise(0.015), 3000) * ad(0.015, 0.0005, 3), 0, 0.5)
    place(y, kick(180, 60, 0.12, click=0.3), 0, 0.4)
    return y


@sfx("hull_hit", "combat", "Your hull takes damage (enemy fire or a missed die)", "boss files · hullHit() when n < 3", variants=2)
def hull_hit(v):
    y = canvas(0.45)
    place(y, lp(sh_noise(0.3, glide(5000, 800, 0.3, tau=0.06)), 3000) * ad(0.3, 0.001, 3), 0, 0.8)
    place(y, lp(metal_noise(0.25, 1400 + 260 * v, 93), 2500) * ad(0.25, 0.001, 5), 0, 0.35)
    place(y, kick(100 - 10 * v, 35, 0.4, click=0.3), 0, 0.9)
    place(y, osc(glide(180, 60, 0.2, tau=0.05), "square") * ad(0.2, 0.001, 3), 0, 0.25)
    return drive(y, 2.0)


@sfx("hull_hit_heavy", "combat", "Big hull damage (3+)", "boss files · hullHit() / biteDmg() when n ≥ 3")
def hull_hit_heavy(v):
    y = canvas(0.75)
    place(y, boom(1.6, d=0.6), 0, 0.7)
    place(y, lp(metal_noise(0.35, 1100, 93), 2200) * ad(0.35, 0.001, 4), 0, 0.4)
    place(y, kick(90, 25, 0.6, tau=0.06, click=0.4), 0, 1.0)
    place(y, crackle(0.5, 80, 1, 0, 2500), 0.08, 0.5)
    return drive(y, 1.8)


@sfx("ship_destroyed", "big", "One of your ships is torn out / vaporised for the fight", "Garganta · sinkShip(); Mother Core · vaporize() at +170ms")
def ship_destroyed(v):
    y = canvas(1.0)
    place(y, boom(2.0, d=0.6), 0, 0.8)
    place(y, boom(1.0, d=0.35), 0.12, 0.5)
    place(y, osc(glide(700, 90, 0.6), "square", 0.25) * ad(0.6, 0.002, 2.5), 0.02, 0.22)
    place(y, crackle(0.7, 70, 1, 0, 3000), 0.1, 0.5)
    return y


@sfx("boss_death", "big", "Boss destruction — 10 chain bursts, big blast at 1.46s, three after-bursts; timed to explode()", "boss files · explode() — play once at the start; win() fires at 2.6s", keep_len=True)
def boss_death(v):
    D = 2.75
    y = canvas(D)
    for q in range(10):
        big = q % 2 == 1
        place(y, boom(1.4 if big else 0.8, d=0.42 if big else 0.3), q * 0.14, 0.6 if big else 0.45)
    t = tt(1.46)
    wh = osc(glide(180, 1400, 1.46), "saw") * 0.5 + osc(glide(360, 2800, 1.46), "square", 0.125) * 0.2
    wh = lp(wh, 5000) * pts([(0, 0.05), (1.4, 0.4), (1.46, 0)], 1.46) * am(1.46, 1 / 0.15, 0.6, square=True)
    place(y, wh, 0, 0.6)
    T = 1.46
    place(y, boom(5, d=1.25), T, 1.0)
    place(y, kick(90, 22, 1.0, tau=0.08, click=0.6), T, 1.0)
    for i in range(6):
        place(y, ring(R().uniform(2000, 5200), 0.6, decay=5), T + i * 0.012, 0.12)
    place(y, hp(metal_noise(0.3, 9000, 93), 4000) * ad(0.3, 0.001, 4), T, 0.25)
    for at, sz, dd in [(1.62, 1.4, 0.42), (1.76, 1.4, 0.42), (1.92, 2.2, 0.6)]:
        place(y, boom(sz, d=dd), at, 0.6)
    rum = lp(noise(D - T), 120) * pts([(0, 0), (0.05, 1), (D - T, 0)], D - T)
    place(y, rum, T, 1.2)
    y = verb(y, 0.3, 1.4, tail=0.0)
    return y[: N(D)]


@sfx("boss_victory", "big", "Boss defeated — chiptune fanfare", "boss files · win()")
def boss_victory(v):
    y = canvas(2.2)
    lead = [(0.00, 76, 0.09), (0.10, 81, 0.09), (0.20, 85, 0.09), (0.30, 88, 0.28),
            (0.62, 86, 0.09), (0.72, 85, 0.09), (0.82, 83, 0.09), (0.92, 81, 0.95)]
    harm = [(0.30, 81, 0.28), (0.62, 83, 0.09), (0.72, 81, 0.09), (0.82, 80, 0.09), (0.92, 76, 0.95)]
    bass = [(0.00, 45, 0.28), (0.30, 49, 0.28), (0.62, 40, 0.28), (0.92, 45, 0.95)]
    for at, m, d in lead:
        place(y, note(mtof(m), d, "square", 0.5, r=0.03 if d < 0.2 else 0.25, vib=18 if d > 0.2 else 0, sus=0.9), at, 0.32)
    for at, m, d in harm:
        place(y, note(mtof(m), d, "square", 0.25, r=0.03 if d < 0.2 else 0.25, sus=0.8), at, 0.18)
    for at, m, d in bass:
        place(y, note(mtof(m), d, "tri", r=0.05 if d < 0.5 else 0.3), at, 0.5)
    for at in [0, 0.3, 0.62]:
        place(y, hp(noise(0.08), 1500) * ad(0.08, 0.001, 4), at, 0.25)
    place(y, hp(noise(0.7), 3000) * ad(0.7, 0.002, 3), 0.92, 0.22)
    place(y, kick(120, 40, 0.3, click=0.2), 0.92, 0.5)
    for i, m in enumerate([93, 97, 100, 105]):
        place(y, note(mtof(m), 0.04, "square", 0.125, r=0.015), 0.95 + i * 0.04, 0.1)
    return verb(y, 0.25, 1.0, tail=0.3)


@sfx("fleet_defeat", "big", "Hull gone — hull bursts, final blow at 0.62s, power-down phrase", "boss files · lose() — play once at the start")
def fleet_defeat(v):
    y = canvas(1.9)
    for q in range(5):
        place(y, boom(1.0, d=0.3), q * 0.12, 0.45)
    place(y, kick(100, 25, 0.8, tau=0.07, click=0.5), 0.62, 1.0)
    place(y, boom(2.5, d=0.8), 0.62, 0.6)
    for at, m, d in [(0.75, 64, 0.18), (0.95, 62, 0.18), (1.15, 60, 0.18)]:
        place(y, note(mtof(m), d, "square", 0.5, r=0.04, sus=0.85), at, 0.28)
    d = 0.6
    t = tt(d)
    f = mtof(57) * 2 ** (-np.clip((t - 0.25) / 0.35, 0, 1))
    place(y, osc(f, "square") * pts([(0, 0), (0.005, 0.85), (0.25, 0.8), (0.6, 0)], d), 1.35, 0.28)
    place(y, osc(f * 0.25, "tri") * pts([(0, 0), (0.01, 1), (0.6, 0)], d), 1.35, 0.5)
    return verb(y, 0.25, 1.1, tail=0.3)


@sfx("boss_phase2_overdrive", "big", "Mother Core OVERDRIVE at half HP — overclock whine, three glitch stutters", "Mother Core · afterPlayer() when OVERDRIVE pops (flicker is 3×300ms)")
def boss_phase2_overdrive(v):
    y = canvas(1.4)
    d = 1.0
    wh = osc(glide(150, 1200, d), "saw") + 0.4 * osc(glide(300, 2400, d), "square", 0.125)
    wh = svf(wh * 0.5, glide(800, 6000, d), 1.3, "lp") * pts([(0, 0.2), (0.95, 1), (1.0, 0)], d)
    place(y, wh, 0, 0.55)
    for i, at in enumerate([0, 0.3, 0.6]):
        st = osc(880 * (1.25 ** i), "square", 0.25, d=0.16) * am(0.16, 40, 1.0, square=True)
        st += hp(metal_noise(0.16, 6000, 31), 2000) * 0.5
        place(y, crush(st * ad(0.16, 0.001, 2), 5), at, 0.4)
    place(y, kick(120, 30, 0.35, click=0.6), 1.0, 0.9)
    place(y, lp(metal_noise(0.2, 2200, 93), 4000) * ad(0.2, 0.001, 5), 1.0, 0.4)
    hum = lp(osc(55, "saw", d=0.4), 300) * pts([(0, 0.6), (0.4, 0)], 0.4)
    place(y, hum, 1.0, 0.5)
    return y


@sfx("boss_phase2_frenzy", "big", "Garganta FRENZY at half HP — rising roar with three surges", "Garganta · afterPlayer() when FRENZY pops (flicker is 3×300ms)")
def boss_phase2_frenzy(v):
    d = 1.35
    y = canvas(1.45)
    fc = curve([(0, 80), (0.4, 140), (1.0, 120), (1.35, 60)], d)
    g = growl(d, 0, 0, rough=42, fcurve=fc, formants=((700, 1.0), (1200, 0.6), (2600, 0.3)), breath=0.5)
    env = pts([(0, 0), (0.05, 0.8), (0.3, 0.75), (0.33, 1.0), (0.6, 0.9), (0.63, 1.15), (1.0, 1.0), (1.35, 0)], d)
    place(y, g * env, 0, 0.9)
    place(y, bp(noise(d), 800, 3000) * env * 0.4, 0, 0.6)
    for at in [0, 0.3, 0.6]:
        place(y, kick(80, 28, 0.35, click=0.2), at, 0.6)
    return verb(y, 0.3, 1.4, tail=0.4, damp=2500)


# ════════════════ MARAUDER ════════════════

@sfx("marauder_shot", "combat", "Marauder blaster shot", "Marauder · enemyTurn() muzzle(); one per shot, 120ms apart (cap 6)", variants=3)
def marauder_shot(v):
    s = laser([1100, 950, 1250][v], [140, 120, 160][v], 0.2, 0.04, "saw")
    place(s, hp(noise(0.03), 1500) * ad(0.03, 0.0005, 3), 0, 0.6)
    s = crush(drive(s, 3), 6)
    return echo(s, 0.05, 0.2, 2, tail=0.08)


@sfx("marauder_charge", "big", "CHARGING round — weapon whine builds, ready click", "Marauder · enemyTurn() when atk = 0 (glow lasts 900ms)")
def marauder_charge(v):
    d = 1.0
    y = canvas(d)
    f = glide(220, 1760, 0.85)
    c = (osc(f, "square", 0.25) * 0.6 + osc(f * 0.5, "saw") * 0.4) * am(0.85, glide(6, 45, 0.85), 0.8, square=True)
    c *= pts([(0, 0.1), (0.8, 1.0), (0.85, 0)], 0.85)
    place(y, lp(c, 6000), 0, 0.45)
    place(y, note(2637, 0.04, "square", 0.125, r=0.01), 0.88, 0.16)
    place(y, hp(metal_noise(0.05, 7000, 31), 3000) * ad(0.05, 0.0005, 3), 0.88, 0.12)
    return crush(y, 7)


# ════════════════ MOTHER CORE ════════════════

@sfx("mothercore_shot", "combat", "Mother Core plasma shot", "Mother Core · enemyTurn() muzzle(); one per shot, 120ms apart (cap 6)", variants=3)
def mothercore_shot(v):
    d = 0.3
    y = canvas(d)
    car = glide([900, 780, 1020][v], 220, d, tau=0.06)
    place(y, fm(car, 330, 4, d, 4) * ad(d, 0.001, 4), 0, 0.6)
    place(y, osc(glide(220, 80, 0.15, tau=0.04), "sine") * ad(0.15, 0.001, 3), 0, 0.5)
    place(y, lp(noise(0.1), 2000) * ad(0.1, 0.001, 4), 0, 0.3)
    return y


@sfx("mothercore_core_open", "big", "Core opens — clunks, servo, bright 'exposed' chime", "Mother Core · startRound() when exposed() becomes true (CORE EXPOSED · HITS ×2)")
def mothercore_core_open(v):
    y = canvas(1.05)
    for at, f in [(0, 2500), (0.12, 2000)]:
        place(y, kick(160, 40, 0.18, click=0.5), at, 0.6)
        place(y, lp(metal_noise(0.15, f, 93), 4000) * ad(0.15, 0.001, 5), at, 0.4)
    d = 0.45
    sv = svf(osc(glide(300, 700, d), "saw"), 1200, 3.0, "bp") * am(d, 30, 0.4) * pts([(0, 0), (0.05, 1), (0.45, 0)], d)
    place(y, sv, 0.15, 0.5)
    d = 0.7
    hum = (osc(110, "saw", d=d) + osc(165, "saw", d=d) * 0.6)
    hum = svf(hum * 0.4, glide(200, 2500, d), 1.0, "lp") * pts([(0, 0), (0.4, 0.7), (0.7, 0)], d)
    place(y, hum, 0.3, 0.6)
    place(y, note(1760, 0.07, "tri_smooth", r=0.02), 0.62, 0.45)
    place(y, note(2637, 0.2, "tri_smooth", r=0.15), 0.7, 0.45)
    place(y, ring(1760, 0.35, decay=5), 0.62, 0.2)
    return verb(y, 0.25, 1.0, tail=0.3)


@sfx("mothercore_core_seal", "big", "CORE SEALS — servo down, clamp, charge hum builds (900ms glow)", "Mother Core · enemyTurn() when atk = 0")
def mothercore_core_seal(v):
    y = canvas(1.05)
    d = 0.25
    place(y, svf(osc(glide(700, 300, d), "saw"), 1000, 3.0, "bp") * pts([(0, 0), (0.03, 1), (0.25, 0.3)], d), 0, 0.5)
    place(y, kick(140, 30, 0.35, click=0.6), 0.25, 0.9)
    place(y, lp(metal_noise(0.2, 1600, 93), 3500) * ad(0.2, 0.001, 5), 0.25, 0.45)
    place(y, hp(noise(0.03), 2500) * ad(0.03, 0.0005, 3), 0.25, 0.35)
    d = 0.65
    ch = osc(glide(110, 220, d), "saw") * am(d, glide(6, 14, d), 0.5)
    ch = svf(ch, glide(400, 2500, d), 1.2, "lp") * pts([(0, 0), (0.55, 0.8), (0.65, 0)], d)
    place(y, ch, 0.32, 0.5)
    return y


@sfx("mothercore_beam", "big", "CORE BEAM — charge chirp then a heavy sustained beam", "Mother Core · vaporize() at the start (beam anim is 560ms)")
def mothercore_beam(v):
    y = canvas(0.85)
    place(y, osc(glide(400, 3000, 0.08), "sine") * pts([(0, 0), (0.07, 0.6), (0.08, 0)], 0.08), 0, 0.5)
    d = 0.7
    b = osc(220, "saw", d=d) + osc(330.5, "saw", d=d) * 0.8 + osc(440.9, "saw", d=d) * 0.5 + noise(d) * 0.6
    b = lp(b * 0.4, 5000) * am(d, 45, 0.4) * pts([(0, 1), (0.42, 0.9), (0.67, 0)], d)
    b += fm(110, 55, 5, d, 2) * pts([(0, 1), (0.67, 0)], d) * 0.6
    place(y, crush(drive(b, 2.2), 7), 0.08, 0.7)
    place(y, kick(130, 30, 0.4, click=0.6), 0.08, 0.8)
    return y


# ════════════════ GARGANTA ════════════════

@sfx("garganta_inhale", "big", "Garganta INHALES — maw exposed for ×2", "Garganta · startRound() when exposed() becomes true")
def garganta_inhale(v):
    d = 1.1
    y = canvas(d)
    env = pts([(0, 0), (0.85, 1), (1.0, 0.8), (1.1, 0)], d)
    place(y, svf(noise(d), glide(350, 1600, d), 3.0, "bp") * env, 0, 0.8)
    place(y, growl(d, 55, 70, rough=20, breath=0.6) * env, 0, 0.35)
    place(y, np.sin(2 * np.pi * np.cumsum(glide(900, 1300, d)) / SR) * env, 0, 0.06)
    return y


@sfx("garganta_maw_shut", "big", "MAW SHUTS — heavy clamp, wet crunch, rumble", "Garganta · enemyTurn() when atk = 0")
def garganta_maw_shut(v):
    y = canvas(0.9)
    place(y, snap(2), 0, 0.8)
    place(y, kick(90, 25, 0.5, tau=0.06, click=0.4), 0, 1.0)
    place(y, lp(sh_noise(0.2, glide(3000, 600, 0.2)), 1500) * ad(0.2, 0.001, 3), 0, 0.6)
    place(y, growl(0.8, 72, 52, rough=25) * pts([(0, 0), (0.04, 1), (0.3, 0.6), (0.8, 0)], 0.8), 0.04, 0.9)
    place(y, lp(noise(0.7), 150) * pts([(0, 0), (0.05, 1), (0.7, 0)], 0.7), 0.02, 1.2)
    return y


@sfx("garganta_bite", "big", "BITE — growl windup, lunge whoosh, jaw SNAP at 0.385s, rumble", "Garganta · bite() at the start (impact lands at +385ms)")
def garganta_bite(v):
    y = canvas(1.3)
    T = 0.385
    place(y, growl(0.45, 70, 120, rough=35) * pts([(0, 0), (0.38, 1), (0.45, 0.2)], 0.45), 0, 0.7)
    wh = svf(noise(0.17), glide(300, 2500, 0.17), 2.0, "bp") * pts([(0, 0), (0.16, 1), (0.17, 0)], 0.17)
    place(y, wh, T - 0.17, 0.6)
    place(y, snap(2), T, 1.0)
    place(y, kick(120, 25, 0.6, tau=0.06, click=0.5), T, 1.0)
    place(y, lp(sh_noise(0.25, glide(4000, 700, 0.25)), 2000) * ad(0.25, 0.001, 3), T, 0.6)
    place(y, growl(0.85, 90, 55, rough=28) * pts([(0, 0), (0.04, 1), (0.35, 0.55), (0.85, 0)], 0.85), T + 0.03, 0.8)
    return y


@sfx("garganta_regrow", "combat", "+1 REGROWS — wet organic bubbling", "Garganta · endRound() when regen fires")
def garganta_regrow(v):
    d = 0.6
    y = canvas(d)
    for i in range(6):
        at = R().uniform(0, 0.42)
        f0 = R().uniform(260, 420)
        bl = osc(glide(f0, f0 * 2.1, 0.06), "sine") * ad(0.06, 0.002, 3)
        place(y, bl, at, 0.35)
    t = tt(d)
    sq = bp(noise(d), 200, 900) * (0.5 + 0.5 * np.sin(2 * np.pi * 18 * t)) * pts([(0, 0), (0.25, 1), (0.6, 0)], d)
    place(y, sq, 0, 0.5)
    place(y, osc(glide(220, 440, d), "tri_smooth") * pts([(0, 0), (0.3, 1), (0.6, 0)], d), 0, 0.15)
    return y


@sfx("garganta_hurt", "combat", "Garganta flinches — short pained screech (layer on boss_hit)", "Garganta · hurt()")
def garganta_hurt(v):
    d = 0.45
    fc = curve([(0, 140), (0.08, 260), (0.45, 110)], d)
    g = growl(d, 0, 0, rough=45, fcurve=fc, formants=((800, 1.0), (1400, 0.6), (2800, 0.3)), breath=0.4)
    return g * pts([(0, 0), (0.02, 1), (0.45, 0)], d)
