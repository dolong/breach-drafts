import numpy as np, subprocess, os
from scipy.signal import resample_poly, lfilter
from scipy.ndimage import minimum_filter1d, maximum_filter1d
from scipy.io import wavfile
def kw(x,fs):
    K=np.tan(np.pi*1681.974450955533/fs); Vh=10**(3.999843853973347/20); Vb=Vh**0.4996667741545416; Q=0.7071752369554196
    a0=1+K/Q+K*K; b=[(Vh+Vb*K/Q+K*K)/a0,2*(K*K-Vh)/a0,(Vh-Vb*K/Q+K*K)/a0]; a=[1,2*(K*K-1)/a0,(1-K/Q+K*K)/a0]
    K=np.tan(np.pi*38.13547087602444/fs); Q=0.5003270373238773; a0=1+K/Q+K*K
    return lfilter([1,-2,1],[1,2*(K*K-1)/a0,(1-K/Q+K*K)/a0],lfilter(b,a,x,axis=0),axis=0)
def mom_max(x,sr=44100):
    w=int(0.4*sr); y=kw(np.vstack([x,np.zeros((w,2))]),sr); p=(y**2).sum(1); c=np.concatenate([[0],np.cumsum(p)]); h=int(0.01*sr)
    return -0.691+10*np.log10(max((c[i+w]-c[i])/w for i in range(0,len(p)-w,h))+1e-20)
def tp(x): return 20*np.log10(np.abs(resample_poly(x,4,1,axis=0)).max()+1e-12)
def limit(x, ceil_db=-1.0, sr=44100, look=0.004, rel=0.08):
    c=10**(ceil_db/20); pk=maximum_filter1d(np.abs(resample_poly(x,4,1,axis=0)).max(1),9)[::4][:len(x)]
    g=np.minimum(1, c/np.maximum(pk,1e-9)); L=int(look*sr); g=minimum_filter1d(g, 2*L+1)
    a=np.exp(-1/(rel*sr)); out=np.empty_like(g); cur=1.0
    for i,v in enumerate(g):
        cur = v if v<cur else v+(cur-v)*a
        out[i]=cur
    return x*out[:,None]
def finish(y48, name, outdir, target=-14.0, tail_db=-60, max_len=None):
    x=resample_poly(y48,147,160,axis=0)
    e=np.abs(x).max(1); thr=e.max()*10**(tail_db/20); idx=np.where(e>thr)[0]
    end=min(len(x), idx[-1]+int(0.02*44100)) if len(idx) else len(x)
    if max_len: end=min(end,int(max_len*44100))
    x=x[:end].copy(); n=min(int(0.02*44100),len(x)); x[len(x)-n:]*=np.linspace(1,0,n)[:,None]
    for _ in range(3):
        x*=10**((target-mom_max(x))/20); x=limit(x)
    x=limit(x, -1.0)
    q=x*32767+(np.random.rand(*x.shape)-np.random.rand(*x.shape)); pcm=np.clip(np.round(q),-32768,32767).astype(np.int16)
    for d in ("wav","ogg","mp3"): os.makedirs(f"{outdir}/{d}",exist_ok=True)
    wp=f"{outdir}/wav/{name}.wav"; wavfile.write(wp,44100,pcm)
    subprocess.run(["ffmpeg","-v","error","-y","-i",wp,"-c:a","libvorbis","-q:a","5",f"{outdir}/ogg/{name}.ogg"],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",wp,"-c:a","libmp3lame","-q:a","2",f"{outdir}/mp3/{name}.mp3"],check=True)
    f=pcm/32768.0
    return dict(name=name, duration_ms=round(len(pcm)/44.1), lufs_m_max=round(mom_max(f),1), true_peak_db=round(tp(f),1))
