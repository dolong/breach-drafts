import numpy as np, subprocess, json, os, tempfile
from scipy.signal import resample_poly
from scipy.io import wavfile
from ana import kweight, env_db
exec(open('final.py').read())
SRC=96000
def load96(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-map","0:a:0","-f","f32le","-ac","2","-"],capture_output=True,check=True).stdout
    return np.frombuffer(raw,dtype=np.float32).reshape(-1,2).astype(np.float64)
from scipy.signal import lfilter
def kw(x,fs):
    K=np.tan(np.pi*1681.974450955533/fs); Vh=10**(3.999843853973347/20); Vb=Vh**0.4996667741545416; Q=0.7071752369554196
    a0=1+K/Q+K*K; b=[(Vh+Vb*K/Q+K*K)/a0,2*(K*K-Vh)/a0,(Vh-Vb*K/Q+K*K)/a0]; a=[1,2*(K*K-1)/a0,(1-K/Q+K*K)/a0]
    K=np.tan(np.pi*38.13547087602444/fs); Q=0.5003270373238773; a0=1+K/Q+K*K
    return lfilter([1,-2,1],[1,2*(K*K-1)/a0,(1-K/Q+K*K)/a0],lfilter(b,a,x,axis=0),axis=0)
def mom_max(x,sr):
    w=int(0.4*sr); y=kw(np.vstack([x,np.zeros((w,2))]),sr); p=(y**2).sum(1); c=np.concatenate([[0],np.cumsum(p)]); h=int(0.01*sr)
    return -0.691+10*np.log10(max((c[i+w]-c[i])/w for i in range(0,len(p)-w,h))+1e-20)
def tp(x): return 20*np.log10(np.abs(resample_poly(x,4,1,axis=0)).max()+1e-12)
os.makedirs("out/wav",exist_ok=True); os.makedirs("out/ogg",exist_ok=True); os.makedirs("out/mp3",exist_ok=True)
clips=[]; report=[]
for cid,stem,tier,ev,trig,cap,target,vars_ in FINAL:
    files=[]
    for n,v in enumerate(vars_,1):
        src=f"wav/{stem}_HY_PC-{v:03d}.wav"; x=load96(src)
        a=np.abs(x).max(1); pk=a.max()
        on=max(int(np.argmax(a>pk*10**(-45/20)))-int(0.002*SRC),0)
        e=env_db(x,SRC); nat=np.where(e>e.max()-60)[0][-1]
        end=nat; capped=False
        if cap and (nat-on)>cap/1000*SRC: end=on+int(cap/1000*SRC); capped=True
        y=x[on:end].copy(); L=len(y)
        fi=min(int(0.002*SRC),L); y[:fi]*=np.linspace(0,1,fi)[:,None]
        fl=int(L*0.35) if capped else min(int(0.02*SRC),L)
        y[L-fl:]*=(0.5*(1+np.cos(np.linspace(0,np.pi,fl))))[:,None]
        y44=resample_poly(y,147,320,axis=0)
        y44*=10**((target-mom_max(y44,44100))/20)
        t=tp(y44); limited=False
        if t>-1.0: y44*=10**((-1.0-t)/20); limited=True
        # 16-bit TPDF dither
        q=y44*32767+ (np.random.rand(*y44.shape)-np.random.rand(*y44.shape))
        pcm=np.clip(np.round(q),-32768,32767).astype(np.int16)
        name=f"{cid}_{n:02d}"; wp=f"out/wav/{name}.wav"; wavfile.write(wp,44100,pcm)
        subprocess.run(["ffmpeg","-v","error","-y","-i",wp,"-map_metadata","-1","-c:a","libvorbis","-q:a","5",f"out/ogg/{name}.ogg"],check=True)
        subprocess.run(["ffmpeg","-v","error","-y","-i",wp,"-map_metadata","-1","-c:a","libmp3lame","-q:a","2",f"out/mp3/{name}.mp3"],check=True)
        f=pcm.astype(np.float64)/32768; ef=env_db(f,44100); af=np.abs(f).max(1); onf=np.argmax(af>af.max()*0.01)
        hit=(np.argmax(ef>=ef.max()-3)-onf)/44.1
        files.append({"name":name,"ogg":f"ogg/{name}.ogg","mp3":f"mp3/{name}.mp3","from":os.path.basename(src),
                      "duration_ms":round(len(pcm)/44.1),"hit_ms":round(hit),"lufs_m_max":round(mom_max(f,44100),1),"true_peak_db":round(tp(f),1),"capped":capped})
        report.append((cid,n,len(pcm)/44.1,hit,mom_max(f,44100),tp(f),capped,limited))
    clips.append({"id":cid,"source":stem,"tier":tier,"gain_db":TIER[tier],"loop":False,"round_robin":True,"event":ev,"trigger":trig,
                  "lufs_target":target,"max_ms":cap,"files":files})
json.dump({"source_pack":"Helton Yan Pixel Combat (CC BY 4.0)","processing":"trimmed to onset (2ms pre-roll), length-capped per moment with cosine fade, normalised to per-id LUFS-M max, ≤ −1 dBTP, 44.1kHz 16-bit TPDF-dithered; OGG Vorbis q5 + MP3 V2","clips":clips},
          open("out/manifest_pack.json","w"),indent=2,ensure_ascii=False)
for cid in dict.fromkeys(r[0] for r in report):
    R=[r for r in report if r[0]==cid]
    print(f"{cid:22s} n={len(R)} len {min(r[2] for r in R):5.0f}-{max(r[2] for r in R):5.0f}ms  hit {min(r[3] for r in R):3.0f}-{max(r[3] for r in R):3.0f}ms  LUFSm {min(r[4] for r in R):6.1f}..{max(r[4] for r in R):6.1f}  TP≤{max(r[5] for r in R):5.1f}  capped {sum(r[6] for r in R)}  TPlimited {sum(r[7] for r in R)}")
