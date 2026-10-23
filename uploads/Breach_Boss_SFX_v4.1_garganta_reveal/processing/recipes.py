from mix import *
REG=[]
def sfx(id, tier, target, event, trigger, alt=None, variants=1, keep_len=False, max_len=None):
    def deco(fn): REG.append(dict(id=id,tier=tier,target=target,event=event,trigger=trigger,alt=alt,variants=variants,keep_len=keep_len,max_len=max_len,fn=fn)); return fn
    return deco
def riser_into(at_end, dur, gain, c):
    r=S('Riser_088'); pk=t_at(r,-1); c.put(fade(seg(r,pk-dur,pk),0.05,0.01), at_end-dur, gain)

# ───────── ALARM ─────────
@sfx("encounter_alarm","big",-12.5,"Red alert before a boss reveal — ship klaxon, sub hit, riser cresting into the reveal","Jump Gate v2 · alarm() (ends as reveal() fires at +1100ms)", alt="A", max_len=1.1)
def alarm_A(v):
    c=Canvas(1.1)
    c.put(cap(pitch(S('Alarm_Fast_DDM23'),3),1.1,0.04),0,0)          # 3 klaxon cycles, 0.42s apart
    c.put(lp(seg(S('ALARM-7'),0,1.1),2500),0,-8)                      # big ship alarm body underneath
    c.put(cap(S('Impact_045'),0.9,0.3),0,-5)                          # punch on the first cycle
    riser_into(1.1,1.0,-10,c)
    return c.y
@sfx("encounter_alarm","big",-12.5,"Red alert — cinematic two-tone trailer alarm, boom, riser into the reveal","Jump Gate v2 · alarm()", alt="B", max_len=1.1)
def alarm_B(v):
    c=Canvas(1.1)
    c.put(seg(S('Foreboding_E'),0,1.1),0,0)
    c.put(seg(S('Trepidation_E'),0,1.1),0,-7)
    c.put(lp(seg(S('ALARM-7'),0,1.1),2000),0,-11)
    c.put(cap(S('Boom_036'),1.0,0.4),0,-4)
    riser_into(1.1,1.0,-10,c)
    return c.y
@sfx("encounter_alarm_loop","big",-13,"Klaxon loop (2 cycles, seamless) if the reveal ever waits on a tap","Jump Gate v2 · loop until reveal()", keep_len=True)
def alarm_loop(v):
    k=pitch(S('Alarm_Fast_DDM23'),3); P=0.5*2**(-3/12)
    return fade(seg(k,P,3*P),0.002,0.002)

# ───────── BOSS APPEARS ─────────
@sfx("boss_warp_in","big",-13.5,"Boss materialises — reversed swell sucks in, cinematic slam + sub drop at 0.42s","boss files · warpIn() (flash at +420ms)", max_len=1.6)
def warp_in(v):
    c=Canvas(1.6)
    c.put(ramp(rev(seg(S('Dramatic_E'),0,0.42)),2.5),0,-9)
    c.put(S('Smash_B'),0.42,0); c.put(S('Downer_Fast_12'),0.42,-4); c.put(cap(S('Impact_038'),1.0,0.4),0.42,-7)
    return fade(verb(c.y,1.3,-16),0,0.35)
def inhale_into(c, at=0.22, gain=-5):
    h=rev(from_onset(S('Dragon_Short_Huff'))[:N(0.5)]); c.put(ramp(h,0.8),at,gain,align=len(h)/SR)
@sfx("reveal_garganta","big",-13,"Garganta reveal — breath in, dragon roar on the colour flash, bite + T-Rex roar on the name slam","Jump Gate v2 · reveal() when boss = garganta (hits at +0.22s and +0.96s)", alt="A", max_len=2.4)
def rg_A(v):
    c=Canvas(2.4); inhale_into(c)
    c.put(S('Boom_091'),0.22,-1)
    r=pitch(S('Dragon_Roaring_4'),-3); s0=0.32-t_at(r,-6); c.put(cap(r,0.92-s0,0.32),s0,-2,0)
    c.put(S('Smash_B'),0.96,-2)
    b=S('Monster_Bite_3'); c.put(b,0.96,-4,align=t_at(b,-6))
    t=pitch(S('T-Rex_roar_03'),-2); c.put(t,0.96,0,align=t_at(t,-6))
    c.put(S('Downer_Fast_12'),0.96,-6)
    return fade(verb(c.y,1.6,-13),0,0.4)
@sfx("reveal_garganta","big",-13,"Garganta reveal — beast growl on the colour flash, braam + dragon roar on the name slam","Jump Gate v2 · reveal() when boss = garganta", alt="B", max_len=2.6)
def rg_B(v):
    c=Canvas(2.6); inhale_into(c)
    c.put(S('Impact_021'),0.22,-2)
    g=pitch(S('Taunt2Stun03'),-2); s0=0.30-t_at(g,-6); c.put(cap(g,0.92-s0,0.3),s0,-1)
    br=S('Braam_029'); c.put(cap(br,1.6,0.8),0.96,-1,align=t_at(br,-6))
    d=pitch(S('Creature_Dragon_Roar_01'),-2); c.put(d,0.96,-2,align=t_at(d,-6))
    b=S('Monster_Bite_3'); c.put(b,0.96,-5,align=t_at(b,-6))
    return fade(verb(c.y,1.6,-13),0,0.5)
@sfx("reveal_mothercore","big",-13,"Mother Core reveal — braam on the colour flash, metal slam + sub on the name slam","Jump Gate v2 · reveal() when boss = mothercore", max_len=2.3)
def rmc(v):
    c=Canvas(2.3)
    sw=rev(seg(S('Impact_038'),0,0.3)); c.put(ramp(sw,1.3),0.22,-6,align=0.3)
    c.put(S('Impact_021'),0.22,-3)
    c.put(cap(S('Braam_004'),0.72,0.35),0.22,-4)
    c.put(S('impact_boom_003'),0.96,0)
    hm=S('Haunted_Metal',2); c.put(cap(hm,1.6,0.6),0.96,-3,align=t_at(hm,-1))
    return fade(verb(c.y,1.5,-14),0,0.4)
@sfx("reveal_marauder","big",-13,"Marauder reveal — hit on the colour flash, warship roars past and peaks on the name slam","Jump Gate v2 · reveal() when boss = marauder", max_len=2.2)
def rma(v):
    c=Canvas(2.2)
    sw=rev(seg(S('Angry_E'),0,0.3)); c.put(ramp(sw,1.3),0.22,-6,align=0.3)
    c.put(S('Angry_E'),0.22,-1)
    pb=S('spaceship_passby_021'); pk=t_at(pb,-1); c.put(fade(seg(pb,pk-0.74,pk+0.9),0.3,0.4),0.22,-6)
    c.put(S('Dramatic_E'),0.96,-1); c.put(S('Boom_005'),0.96,-3)
    return fade(verb(c.y,1.4,-15),0,0.4)

# ───────── GARGANTA'S VOICE ─────────
@sfx("boss_phase2_frenzy","big",-13,"Garganta FRENZY — full dragon roar over a braam and sub hit","Garganta · afterPlayer() FRENZY", max_len=2.2)
def frenzy(v):
    c=Canvas(2.2)
    r=from_onset(pitch(S('Dragon_Roaring_4'),-2)); c.put(cap(r,2.1,0.6),0,0)
    c.put(S('Impact_045'),0.05,-3)
    br=S('Braam_029'); c.put(cap(br,1.9,0.8),0.05,-7,align=t_at(br,-6))
    return verb(c.y,1.6,-13)
@sfx("garganta_inhale","combat",-16,"Garganta draws breath — maw open, ×2 damage window","Garganta · startRound() when exposed()", max_len=1.4)
def inhale(v):
    c=Canvas(1.4)
    h=rev(seg(S('Dragon_Long_Huff_2'),0.5,1.8)); c.put(ramp(h,1.0),0,0)
    c.put(ramp(rev(seg(S('Boom_040'),0,1.3)),1.5),0,-10)
    return fade(c.y,0,0.06)
HURT=[('Creature_Monster_Pain_01',-3),('LargeMonster11_Roar03',-4),('BEAST_01_Attack_08',-3),('Screeching_Monster_2-1',-4)]
@sfx("garganta_hurt","combat",-15.5,"Garganta flinches — pained snarl, layered on boss_hit","Garganta · hurt()", variants=4, max_len=0.65)
def hurt(v):
    s,st=HURT[v]; return cap(hp(from_onset(pitch(S(s),st)),60),0.6,0.22)
BITE=[(('Growl_Dry_14',-3),('T-Rex_roar_03',-2)),(('Dinosaur_Growl_3',-2),('Creature_Roar_13',-3)),(('Roar_Dry_5',-4),('Raptor_roar_08',-2))]
@sfx("garganta_bite","big",-14,"BITE — growl wind-up, lunge, jaw SNAP at 0.385s, roar","Garganta · bite() at the start (snap at +385ms)", variants=3, max_len=1.4)
def bite(v):
    (w,ws),(r,rs)=BITE[v]; T=0.385; c=Canvas(1.4)
    g=from_onset(pitch(S(w),ws))[:N(T)]; c.put(ramp(g,2.0),T,-7,align=len(g)/SR)
    lw=S('creature_attack_whoosh_impact_003'); c.put(lw,T,-6,align=t_at(lw,-1))
    b=S('Monster_Bite_3'); c.put(b,T,0,align=t_at(b,-6))
    c.put(cap(S('Impact_045'),0.8,0.3),T,-4)
    rr=pitch(S(r),rs); a=t_at(rr,-6); c.put(cap(rr,a+(1.35-0.48),0.4),0.48,-6,align=a)
    return verb(c.y,1.2,-16)
@sfx("garganta_maw_shut","big",-15,"MAW SHUTS — heavy jaw clamp, thud, low growl","Garganta · enemyTurn() when atk = 0", variants=2, max_len=0.95)
def maw(v):
    c=Canvas(0.95); b=S('Monster_Bite_3')
    if v==0: c.put(b,0.02,0,align=t_at(b,-6))
    else:
        lw=S('creature_attack_whoosh_impact_003'); c.put(lw,0.02,0,align=t_at(lw,-1)); c.put(b,0.02,-3,align=t_at(b,-6))
    c.put(cap(S('Boom_036'),0.9,0.4),0.02,-4)
    g=from_onset(pitch(S('Growl_Dry_14' if v==0 else 'Dinosaur_Growl_3'),-6)); c.put(cap(g,0.85,0.5),0.06,-9)
    return c.y

# ───────── v4.1: Garganta reveal with a much bigger boom ─────────
def boom_bus(y):
    """Fatten impacts: keep the sub, and add saturated low-mid harmonics (90–700 Hz) so the boom
    still reads on phone and laptop speakers that can't play the sub itself."""
    harm = hp(lp(drive(lp(y,180)*3.0,2.5),700),90)
    return y + harm*db(-3)
def garganta_reveal_v41(take):
    L=2.8; B=Canvas(L); V=Canvas(L)
    inhale_into(V,0.22,-6)
    # colour flash +0.22
    B.put(S('Boom_091'),0.22,0); B.put(S('Impact_021'),0.22,-2); B.put(S('Ruin_B'),0.22,-4)
    if take=="A":
        r=pitch(S('Dragon_Roaring_4'),-3); s0=0.32-t_at(r,-6); V.put(cap(r,0.92-s0,0.32),s0,-5)
    else:
        g=pitch(S('Taunt2Stun03'),-2); s0=0.30-t_at(g,-6); V.put(cap(g,0.92-s0,0.3),s0,-4)
    # name slam +0.96
    B.put(S('Smash_B'),0.96,0); B.put(S('Boom_005'),0.96,-1); B.put(cap(S('Impact_045'),1.2,0.4),0.96,-2)
    B.put(cap(S('PM_CNDP_23'),1.8,0.9),0.96,-5,align=t_at(S('PM_CNDP_23'),-6)); B.put(S('Downer_Fast_12'),0.96,-4)
    b=S('Monster_Bite_3'); V.put(b,0.96,-5,align=t_at(b,-6))
    if take=="A":
        t=pitch(S('T-Rex_roar_03'),-2); V.put(t,0.96,-3,align=t_at(t,-6))
    else:
        br=S('Braam_029'); B.put(cap(br,1.6,0.8),0.96,-3,align=t_at(br,-6))
        d=pitch(S('Creature_Dragon_Roar_01'),-2); V.put(d,0.96,-4,align=t_at(d,-6))
    y = verb(boom_bus(B.y),2.2,-18,damp=1800) + verb(V.y,1.6,-13)
    return fade(y,0,0.6)
@sfx("reveal_garganta","big",-11,"Garganta reveal v4.1 — booming impacts on both hits, roar on top","Jump Gate v2 · reveal() when boss = garganta", alt="A41", max_len=2.8)
def rg41A(v): return garganta_reveal_v41("A")
@sfx("reveal_garganta","big",-11,"Garganta reveal v4.1 (B take)","Jump Gate v2 · reveal() when boss = garganta", alt="B41", max_len=2.8)
def rg41B(v): return garganta_reveal_v41("B")
