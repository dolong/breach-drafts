from mix import *
def radio(x): return drive(hp(lp(x,4800),280)*1.3,1.2)
# ───────── VICTORY (plays at win()) ─────────
def victory_base(c):
    c.put(S('Impact_021'),0.0,-3); c.put(cap(S('Sub_Drop_2'),2.0,1.0),0.0,-6)
    c.put(S('Power_Up_Bright'),0.0,-4,align=0.05)                                   # bright, successful crash-shimmer
    st=S('Stinger_8'); c.put(cap(st,2.6,1.0),0.05,-3)                               # trailer stinger blooms (C# major), peaks ~0.8s
    org=pitch(seg(S('Discovery_01-03'),3.5,6.5),1); c.put(fade(org,0.35,1.0),0.25,-9)  # warm organ chord, same key
def fireworks(c, times=(1.0,1.6,2.1), gains=(-10,-12,-14)):
    fw=S('053_Very_strong'); segs=[(4.4,5.4),(6.75,7.6),(8.9,9.7)]
    for (a,b),t,g in zip(segs,times,gains): c.put(fade(seg(fw,a,b),0.01,0.3),t,g)
def v_triumph():
    c=Canvas(3.4); victory_base(c); fireworks(c); return verb(c.y,2.2,-12)
def v_objective():
    c=Canvas(3.4); victory_base(c); fireworks(c,(1.4,2.0,2.5),(-12,-14,-16))
    v=from_onset(S('Objective_Completed')); c.put(verb(radio(v),0.9,-14),0.85,-2)
    return verb(c.y,2.2,-12)
def v_fireworks():
    c=Canvas(3.4); c.put(S('Impact_021'),0.0,-4); c.put(S('Power_Up_Bright'),0.0,-3,align=0.05)
    fw=S('033_Strong_blast')
    for (a,b),t,g in zip([(2.9,4.4),(5.4,6.9),(7.4,8.9)],(0.05,0.55,1.05),(-3,-5,-6)): c.put(fade(seg(fw,a,b),0.01,0.5),t,g)
    c.put(fade(seg(S('Multi_Close_01-04'),1.85,3.6),0.02,0.6),1.3,-7)               # crackle shower
    org=pitch(seg(S('Discovery_01-03'),3.5,6.5),1); c.put(fade(org,0.5,1.0),0.3,-13)
    return verb(c.y,2.4,-11)
# ───────── DEFEAT (plays at lose(); final blow at 620ms) ─────────
BLOW=0.62
def defeat_base(c):
    for t,src,g,st in ((0.00,'Impact_038',-9,0),(0.17,'Boom_005',-8,0),(0.33,'Impact_038',-7,-2),(0.48,'Angry_E',-6,0)):
        c.put(cap(pitch(S(src),st),0.35,0.15),t,g)                                   # hull bursts
    c.put(S('Ruin_B'),BLOW,0); c.put(S('Boom_091'),BLOW,-1); c.put(cap(S('Sub_Drop_2'),3.0,1.5),BLOW,-4); c.put(S('Downer_Fast_12'),BLOW,-5)
    sd=pitch(seg(S('shut_down_SpaceShip'),25.8,30.0),2); c.put(fade(sd,0.15,1.8),BLOW+0.13,-10)   # the ship powers down
    c.put(S('Weapon_Power_Down_04'),BLOW+0.06,-10)
def d_dark():
    c=Canvas(4.0); defeat_base(c); c.put(cap(S('Stinger-Low13'),3.3,1.5),BLOW,-6); return verb(c.y,2.4,-13)
def d_mission_failed():
    c=Canvas(4.0); defeat_base(c); c.put(cap(S('Stinger-Low13'),3.3,1.5),BLOW,-8)
    v=S('missionFailed'); c.put(verb(radio(v),0.8,-14),1.45,-1,align=0.12); return verb(c.y,2.4,-13)
def d_requiem():
    c=Canvas(4.0); defeat_base(c); c.put(S('Failure_01-10'),1.05,-3); return verb(c.y,2.6,-11)
TAKES={"victory":[("V1 · Triumph","Impact and sub drop, a bright successful shimmer, a trailer stinger and organ chord blooming in the same key, distant fireworks",v_triumph),
                  ("V2 · Objective completed","V1 with a radio announcer: “Objective completed”",v_objective),
                  ("V3 · Fireworks","Shimmer hit, then three big firework bursts with sparkle and a crackle shower",v_fireworks)],
       "defeat":[("D1 · Ship goes dark","Hull bursts, the final blow at 0.62s, then the ship powers down over a low, dark drone",d_dark),
                 ("D2 · Mission failed","D1 with the ship’s AI over the radio: “Mission failed”",d_mission_failed),
                 ("D3 · Requiem","Hull bursts, the final blow, power-down, then a small sad orchestral sting",d_requiem)]}
