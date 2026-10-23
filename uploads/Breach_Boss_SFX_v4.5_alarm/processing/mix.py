"""Tiny layering toolkit for building boss SFX from Sonniss sources (48 kHz stereo float)."""
import numpy as np, glob, subprocess, os
from fractions import Fraction
from scipy.signal import resample_poly, butter, sosfilt, fftconvolve, lfilter
from scipy.ndimage import minimum_filter1d
SR = 48000
_cache = {}
def S(pat, i=0):
    fs = sorted(f for f in glob.glob('src/*.wav') if pat in f)
    assert fs, pat
    f = fs[i]
    if f not in _cache:
        raw = subprocess.run(["ffmpeg","-v","error","-i",f,"-map","0:a:0","-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout
        _cache[f] = np.frombuffer(raw, np.float32).reshape(-1,2).astype(np.float64)
    return _cache[f].copy()
def N(t): return int(round(t*SR))
def env(x, win=0.005):
    m = np.abs(x).max(1); n = max(1, N(win)); return np.sqrt(np.convolve(m**2, np.ones(n)/n, 'same'))
def t_at(x, db=-6):
    """time the envelope first reaches max+db (db<0)"""
    e = 20*np.log10(env(x)+1e-12); return np.argmax(e >= e.max()+db)/SR
def seg(x, a, b=None): return x[N(a): (N(b) if b is not None else None)]
def from_onset(x, db=-30, pre=0.005):
    e = 20*np.log10(env(x)+1e-12); i = max(np.argmax(e >= e.max()+db) - N(pre), 0); return x[i:]
def pitch(x, semis):
    r = Fraction(2**(-semis/12)).limit_denominator(240)   # varispeed: lower pitch = longer
    return resample_poly(x, r.numerator, r.denominator, axis=0)
def rev(x): return x[::-1].copy()
def fade(x, fin=0.0, fout=0.0, shape='cos'):
    x = x.copy(); L = len(x)
    if fin > 0: n = min(N(fin), L); x[:n] *= (0.5-0.5*np.cos(np.linspace(0,np.pi,n)))[:,None]
    if fout > 0: n = min(N(fout), L); x[L-n:] *= (0.5+0.5*np.cos(np.linspace(0,np.pi,n)))[:,None]
    return x
def cap(x, dur, fout=0.15): return fade(x[:N(dur)], 0, min(fout, dur))
def ramp(x, p=1.5):
    t = np.linspace(0,1,len(x))**p; return x*t[:,None]
def lp(x, f, o=4): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x, axis=0)
def hp(x, f, o=4): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x, axis=0)
def db(g): return 10**(g/20)
def drive(x, amt=1.5): return np.tanh(x*amt)/np.tanh(amt)
class Canvas:
    def __init__(s, dur): s.y = np.zeros((N(dur),2))
    def put(s, x, at, gain=0.0, align=0.0):
        """place x so that its point `align` (seconds into x) lands at `at`"""
        st = N(at) - N(align); x = x*db(gain)
        if st < 0: x = x[-st:]; st = 0
        n = min(len(x), len(s.y)-st)
        if n > 0: s.y[st:st+n] += x[:n]
        return s
def verb(x, t60=1.4, wet=-12, damp=3500, pre=0.012, seed=7):
    rng = np.random.default_rng(seed); n = N(t60*1.2); t = np.arange(n)/SR
    ir = rng.standard_normal((n,2))*np.exp(-6.9*t/t60)[:,None]; ir = lp(ir, damp, 2); ir /= np.sqrt((ir**2).sum(0))
    w = np.stack([fftconvolve(x[:,c], ir[:,c])[:len(x)] for c in (0,1)],1)
    w = np.vstack([np.zeros((N(pre),2)), w])[:len(x)]
    return x + w*db(wet)
