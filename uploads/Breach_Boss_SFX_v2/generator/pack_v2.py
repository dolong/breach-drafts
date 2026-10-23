import json
# semantic id, pack stem, tier, event, trigger
PACK = [
 ("gate_jump_charge","DSGNMisc_MOVEMENT-Mecha Large Takeoff","big","Ships stream into the gate","Jump Gate v2 · jump() at phase 'jump'"),
 ("gate_jump_exit","MAGSpel_CAST-Teleport Downer","big","White flash as the fleet exits the gate","Jump Gate v2 · jump() with the white flash"),
 ("boss_engage","DSGNSynth_CAST-Mecha Morale","combat","FIGHT / ENGAGE confirm","Jump Gate v2 · fight(); boss files · engage()"),
 ("gate_decoy","DSGNMisc_SKILL RELEASE-Flare Gun","combat","DECOY flare launches","Jump Gate v2 · decoy()"),
 ("fleet_shot","DSGNMisc_PROJECTILE-Laser Shot","combat","A 1-damage ship fires","fireSeq() muzzle(), dmg 1"),
 ("fleet_shot_mid","DSGNMisc_PROJECTILE-Laser Bursts","combat","A 2–3 damage ship fires","fireSeq() muzzle(), dmg 2–3"),
 ("fleet_shot_big","DSGNMisc_SKILL IMPACT-Mecha White Laser","combat","A 4+ damage ship fires","fireSeq() muzzle(), dmg 4+"),
 ("boss_hit","DSGNMisc_HIT-Laser Hit","combat","Bolt hits the boss","hitEnemy(), dmg < 4"),
 ("boss_hit_heavy","DSGNImpt_EXPLOSION-Mecha Intense Hit","combat","Heavy hit on the boss","hitEnemy(), dmg ≥ 4"),
 ("boss_hit_crit","DSGNMisc_SKILL IMPACT-Critical Strike","combat","×2 hit on an open core / inhaling maw","hitEnemy() when exposed()"),
 ("shield_up","DSGNSynth_BUFF-Bonus Max Shield","combat","Block added","addBlock() / block ship fires"),
 ("shield_block","DSGNTonl_SKILL IMPACT-Deflected Hit","combat","Incoming damage blocked","resolveEnemy() when blocked > 0"),
 ("hull_hit","DSGNImpt_EXPLOSION-Mecha Damage","combat","Your hull takes 1–2","hullHit() n < 3 (not MISS)"),
 ("hull_hit_heavy","DSGNImpt_EXPLOSION-Mecha Core Damage","combat","Your hull takes 3+","hullHit() / biteDmg() n ≥ 3"),
 ("ship_destroyed","DSGNImpt_EXPLOSION-Mecha Detonator","big","A ship is eaten / vaporised","sinkShip(); vaporize() +170ms"),
 ("boss_phase2_overdrive","DSGNSynth_CAST-Mecha Speeding","big","Mother Core OVERDRIVE","Mother Core afterPlayer() OVERDRIVE"),
 ("marauder_shot","DSGNMisc_HIT-Mecha Laser Pistol","combat","Marauder blaster shot","Marauder enemyTurn() each muzzle()"),
 ("marauder_charge","DSGNSynth_CAST-Mecha Laser Prepare","big","Marauder CHARGING round","Marauder enemyTurn() atk 0"),
 ("mothercore_shot","DSGNTonl_SKILL RELEASE-Tiny Energy Sphere","combat","Mother Core plasma shot","Mother Core enemyTurn() each muzzle()"),
 ("mothercore_beam","DSGNMisc_SKILL RELEASE-Mecha Laser Release","big","CORE BEAM fires","Mother Core vaporize() at the start"),
 ("garganta_regrow","DSGNMisc_CAST-Slime Ball","combat","+1 REGROWS","Garganta endRound() regen"),
 ("garganta_bite_layer","DSGNMisc_HIT-Mecha Gore Cruncher","combat","Meat layer on the jaw snap","Garganta bite() +385ms, under garganta_bite"),
]
TIER={"dice":-12,"ui":-9,"combat":-6,"big":0}
m=json.load(open("out2/manifest.json"))
m["source_pack"]="mixed: generated:breach-boss-sfx-v2 + Helton Yan Pixel Combat (CC BY 4.0)"
for cid,stem,tier,ev,trig in PACK:
    m["clips"].append({"id":cid,"source":stem,"tier":tier,"gain_db":TIER[tier],"loop":False,"round_robin":True,"event":ev,"trigger":trig,
      "convert_from":[f"{stem}_HY_PC-{i:03d}.wav" for i in range(1,7)],
      "files":[{"name":f"{cid}_{i:02d}","ogg":f"ogg/{cid}_{i:02d}.ogg","mp3":f"mp3/{cid}_{i:02d}.mp3"} for i in range(1,7)]})
json.dump(m,open("out2/manifest.json","w"),indent=2,ensure_ascii=False)
print(len(m["clips"]), "clips;", len(PACK), "pack stems")
