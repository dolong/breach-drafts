import json, sys, numpy as np
import export
from recipes import REG
from mix import S, t_at
out=sys.argv[1] if len(sys.argv)>1 else 'out'
TIER={"combat":-6,"big":0}
clips={}; rep=[]
for r in REG:
    for v in range(r['variants']):
        y=r['fn'](v)
        base=r['id'] if r['alt'] in (None,'A') else f"alt/{r['id']}_B"
        name=f"{r['id']}_{v+1:02d}" if r['alt'] in (None,'A') else f"{r['id']}_B_{v+1:02d}"
        d=out if r['alt'] in (None,'A') else f"{out}/alt_B"
        if r['keep_len']:
            info=export.finish(y,name,d,r['target'],tail_db=-200)
        else:
            info=export.finish(y,name,d,r['target'],max_len=r['max_len'])
        rep.append((name,info))
        key=(r['id'],r['alt'] or 'A')
        clips.setdefault(key,dict(id=r['id'],option=r['alt'] or 'A',source="sonniss-gdc (royalty-free, no attribution)",tier=r['tier'],gain_db=TIER[r['tier']],
            loop=r['keep_len'],round_robin=r['variants']>1,event=r['event'],trigger=r['trigger'],files=[]))
        pre="" if r['alt'] in (None,'A') else "alt_B/"
        clips[key]['files'].append(dict(name=name,ogg=f"{pre}ogg/{name}.ogg",mp3=f"{pre}mp3/{name}.mp3",**{k:info[k] for k in ('duration_ms','lufs_m_max','true_peak_db')}))
for n,i in rep: print(f"{n:28s} {i['duration_ms']:5d}ms  LUFSm {i['lufs_m_max']:6.1f}  TP {i['true_peak_db']:5.1f}")
json.dump([c for c in clips.values()],open(f"{out}/clips_v4.json","w"),indent=2,ensure_ascii=False)
import mix, os
srcs=sorted(os.path.basename(k) for k in mix._cache)
with open(f"{out}/SOURCES.md","w") as f:
    f.write("# Source files (Sonniss GDC Game Audio Bundles, via the archive.org mirror)\n\nRoyalty-free, commercial use, no attribution required. Not for AI/ML training; don't redistribute the raw files as a sound library.\nFilename prefix = bundle year.\n\n")
    f.writelines(f"- {s[:4]} · {s[6:]}\n" for s in srcs)
