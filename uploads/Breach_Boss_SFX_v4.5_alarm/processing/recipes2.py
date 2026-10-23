from mix import *
def chest(x, semis=-12, gain=-12):
    """add a sub-octave 'chest' copy of a voice so it reads as a bigger body"""
    c=lp(pitch(x,semis),300)[:len(x)]; c=np.vstack([c,np.zeros((max(0,len(x)-len(c)),2))]); return x+c*db(gain)
def rasp(x, amt=1.8, mix=-6):
    """throat rasp: saturate the 300 Hz–3 kHz band and blend it back in"""
    b=hp(lp(x,3000),300); return x+drive(b*amt,2.0)*db(mix)
def voice(x, semis, rasp_db=-6, chest_db=-12):
    return chest(rasp(pitch(x,semis),1.8,rasp_db),-12,chest_db)
def snap_at(c, x, T, gain): c.put(x,T,gain,align=t_at(x,-6))
def bite_common(c, T, wind, snaps, roar, roar_gain=-5, roar_at=0.47, wind_gain=-6):
    w=wind[:N(T)]; c.put(ramp(w,1.8),T,wind_gain,align=len(w)/SR)
    for x,g in snaps: snap_at(c,x,T,g)
    a=t_at(roar,-6); c.put(cap(roar,a+(1.4-roar_at),0.45),roar_at,roar_gain,align=a)

DIRS={}
def dragon_bite():
    T=0.385; c=Canvas(1.4)
    f=S('FIREWhsh'); pk=t_at(f,-6); wind=voice(seg(f,max(0,pk-0.30),pk+0.1),-3)
    bite_common(c,T,wind,[(seg(S('Zombie_Bite_04'),0.3,2.0),0),(S('bone_crunch_-_hard_-_5'),-5),(cap(S('Impact_045'),0.8,0.3),-5)],
                voice(from_onset(S('GRWL_ROAR')),-4),-7)
    fl=S('Dragon_Trap_03'); c.put(cap(seg(fl,t_at(fl,-6)),0.9,0.5),0.5,-13)     # fire crackle tail
    return verb(c.y,1.4,-15)
def dragon_hurt():
    c=Canvas(0.65); c.put(cap(voice(from_onset(S('GRWL_ROAR')),-3),0.6,0.25),0,0)
    c.put(cap(voice(from_onset(S('Camel_D')),-6,-9,-14),0.55,0.25),0.01,-5); return c.y
def beast_bite():
    T=0.385; c=Canvas(1.4)
    wind=voice(seg(S('CREABeast'),0.25,1.2),-5)
    meat=from_onset(seg(S('Eating_Meat'),0.9,1.6))
    bite_common(c,T,wind,[(meat,0),(from_onset(S('Mouthy_chomping')),-5),(cap(S('Impact_045'),0.8,0.3),-6)],
                voice(from_onset(S('Camel_A')),-6),-6,0.47,-10)
    return verb(c.y,1.3,-15)
def beast_hurt():
    c=Canvas(0.65); c.put(cap(voice(from_onset(S('Camel_C')),-5),0.6,0.25),0,0)
    c.put(cap(voice(from_onset(S('bear_pain')),-6,-9,-14),0.55,0.25),0.0,-5); return c.y
def leviathan_bite():
    T=0.385; c=Canvas(1.6)
    h=from_onset(S('snake_hiss_03'),-24); h2=from_onset(S('Creature_Hiss_4'))
    wind=pitch(h,-4)[:N(0.5)]; wind=wind[:min(len(wind),N(0.5))]
    w2=pitch(h2,-6)[:N(0.5)]; n=min(len(wind),len(w2)); wind=wind[:n]+w2[:n]*db(-4)
    roar=voice(from_onset(seg(S('Large_Herbivore'),6.9,9.5)),-7,-6,-10)
    c2=Canvas(1.6); bite_common(c2,T,wind,[(S('Monster_Bite_3'),0),(S('Bone_Cracking_34'),-6),(cap(S('Boom_036'),1.0,0.4),-3)],roar,-6,0.5)
    return verb(c2.y,1.8,-13)
def leviathan_hurt():
    c=Canvas(0.7); c.put(cap(voice(from_onset(S('Seals_08')),-7),0.62,0.25),0,0)
    c.put(cap(voice(from_onset(seg(S('Large_Herbivore'),6.9,8.5)),-6,-9,-14),0.6,0.3),0.0,-6); return c.y

# ───────── v4.2: Leviathan bite set (v1 = the approved leviathan_bite) ─────────
LEV=[  # (hiss A, start, pitch), (hiss B, pitch), roar segment start/end in Large_Herbivore, roar pitch
    (('snake_hiss_03',0.0,-4),('Creature_Hiss_4',-6),(6.9,9.5),-7),
    (('snake_hiss_03',0.25,-5),('Hisses_Dry_11',-5),(0.15,3.0),-7),
    (('snake_hiss_03',0.12,-3),('Creature_Hiss_4',-7),(4.95,6.6),-8),
]
def leviathan_bite_v(v):
    (ha,hs,hp_),(hb,hbp),(r0,r1),rp=LEV[v]; T=0.385
    if v==0: return leviathan_bite()
    h=from_onset(seg(S(ha),hs),-24); h2=from_onset(S(hb))
    a=pitch(h,hp_)[:N(0.5)]; b=pitch(h2,hbp)[:N(0.5)]; n=min(len(a),len(b)); wind=a[:n]+b[:n]*db(-4)
    roar=voice(from_onset(seg(S('Large_Herbivore'),r0,r1)),rp,-6,-10)
    c=Canvas(1.6); bite_common(c,T,wind,[(S('Monster_Bite_3'),0),(S('Bone_Cracking_34'),-6),(cap(S('Boom_036'),1.0,0.4),-3)],roar,-6,0.5)
    return verb(c.y,1.8,-13)
