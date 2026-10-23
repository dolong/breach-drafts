import numpy as np, subprocess, json, os
from scipy.signal import lfilter
SR=48000
def load(path, sr=SR):
    raw=subprocess.run(["ffmpeg","-v","error","-i",path,"-map","0:a:0","-f","f32le","-ac","2","-ar",str(sr),"-"],capture_output=True,check=True).stdout
    return np.frombuffer(raw,dtype=np.float32).reshape(-1,2).astype(np.float64)
def kweight(x):
    b1=[1.53512485958697,-2.69169618940638,1.19839281085285]; a1=[1,-1.69065929318241,0.73248077421585]
    b2=[1.0,-2.0,1.0]; a2=[1,-1.99004745483398,0.99007225036621]
    return lfilter(b2,a2,lfilter(b1,a1,x,axis=0),axis=0)
def mom_max(x, sr=SR):
    y=kweight(np.vstack([x,np.zeros((int(0.4*sr),2))]))
    p=(y**2).sum(axis=1)
    w=int(0.4*sr); c=np.concatenate([[0],np.cumsum(p)])
    hop=int(0.01*sr); vals=[(c[i+w]-c[i])/w for i in range(0,len(p)-w,hop)]
    return -0.691+10*np.log10(max(vals)+1e-20)
def env_db(x, sr=SR, win=0.005):
    m=np.abs(x).max(axis=1); n=int(win*sr)
    k=np.ones(n)/n; e=np.sqrt(np.convolve(m**2,k,'same'))
    return 20*np.log10(e+1e-12)
def metrics(path):
    x=load(path); pk=np.abs(x).max()
    a=np.abs(x).max(axis=1); thr=pk*10**(-40/20)
    on=np.argmax(a>thr)
    e=env_db(x); ep=e.max()
    above=np.where(e>ep-60)[0]; end=above[-1] if len(above) else len(x)
    above30=np.where(e>ep-30)[0]; end30=above30[-1]
    pkt=np.argmax(e)
    # spectral centroid of the body
    seg=x[on:end].mean(axis=1); 
    S=np.abs(np.fft.rfft(seg*np.hanning(len(seg)))); f=np.fft.rfftfreq(len(seg),1/SR)
    cen=(S*f).sum()/S.sum()
    return dict(dur=len(x)/SR, lead=on/SR, attack=(pkt-on)/SR, body=(end30-on)/SR, tail=(end-on)/SR,
                peak_db=20*np.log10(pk), mmax=mom_max(x), cen=cen)
if __name__=="__main__":
    exec(open('pack.py').read())
    out={}
    for cid,stem,tier,ev,trig in PACK:
        rows=[metrics(f"wav/{stem}_HY_PC-{i:03d}.wav") for i in range(1,7)]
        out[cid]=rows
        r=lambda k: f"{min(x[k] for x in rows):.2f}-{max(x[k] for x in rows):.2f}"
        print(f"{cid:22s} dur {r('dur'):10s} lead {r('lead'):9s} atk {r('attack'):9s} body(-30) {r('body'):9s} tail(-60) {r('tail'):9s} LUFSm {r('mmax'):12s} cen {np.mean([x['cen'] for x in rows]):6.0f}Hz")
    json.dump(out,open('metrics.json','w'),indent=1)
