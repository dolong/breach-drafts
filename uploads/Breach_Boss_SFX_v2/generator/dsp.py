"""Small chiptune DSP kit: band-limited oscillators, pixel noise, filters, envelopes, fx."""
import numpy as np
from scipy import signal

SR = 44100
rng = np.random.default_rng(0)


def reseed(name):
    """deterministic per-sound randomness, so re-running the script gives identical files"""
    import zlib
    global rng
    rng = np.random.default_rng(zlib.crc32(name.encode()))


def N(d):
    return max(1, int(round(d * SR)))


def tt(d):
    return np.arange(N(d)) / SR


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)


def canvas(d):
    return np.zeros(N(d))


def place(buf, clip, at, gain=1.0):
    i = N(at) if at > 0 else 0
    if i >= len(buf):
        return buf
    end = min(len(buf), i + len(clip))
    buf[i:end] += clip[: end - i] * gain
    return buf


# ---------- envelopes ----------
def ad(d, a=0.002, curve=5.0):
    """fast attack, exponential decay that lands on ~0 at d"""
    t = tt(d)
    e = (np.exp(-curve * t / d) - np.exp(-curve)) / (1 - np.exp(-curve))
    if a > 0:
        e *= np.minimum(1.0, t / a)
    return e


def pts(points, d):
    """piecewise-linear envelope from [(t, v), ...]"""
    t = tt(d)
    return np.interp(t, [p[0] for p in points], [p[1] for p in points])


def gate(d, a=0.003, r=0.012, s=1.0):
    t = tt(d)
    e = np.full_like(t, s)
    e *= np.minimum(1.0, t / max(a, 1e-4))
    e *= np.clip((d - t) / max(r, 1e-4), 0, 1)
    return e


def glide(f0, f1, d, tau=None):
    """exponential glide; tau = time constant (s) for a fast 'drop', else even exp over d"""
    t = tt(d)
    if tau:
        return f1 + (f0 - f1) * np.exp(-t / tau)
    return f0 * (f1 / f0) ** (t / d)


# ---------- oscillators ----------
def _blep(ph, dt):
    y = np.zeros_like(ph)
    m = ph < dt
    x = ph[m] / dt[m]
    y[m] = x + x - x * x - 1
    m = ph > 1 - dt
    x = (ph[m] - 1) / dt[m]
    y[m] = x * x + x + x + 1
    return y


def osc(freq, kind="square", duty=0.5, d=None, phase0=0.0):
    if np.isscalar(freq):
        freq = np.full(N(d), float(freq))
    freq = np.asarray(freq, float)
    dt = np.clip(freq / SR, 1e-7, 0.49)
    ph = (phase0 + np.concatenate([[0.0], np.cumsum(dt)[:-1]])) % 1.0
    if kind == "sine":
        return np.sin(2 * np.pi * ph)
    if kind == "saw":
        return 2 * ph - 1 - _blep(ph, dt)
    if kind == "square":
        y = np.where(ph < duty, 1.0, -1.0)
        y += _blep(ph, dt)
        y -= _blep((ph - duty) % 1.0, dt)
        return y - (2 * duty - 1)
    if kind == "tri":  # NES-style 16-step triangle
        tri = 2 * np.abs(2 * ph - 1) - 1
        return np.round(tri * 7.5) / 7.5
    if kind == "tri_smooth":
        return 2 * np.abs(2 * ph - 1) - 1
    raise ValueError(kind)


def noise(d):
    return rng.uniform(-1, 1, N(d))


def sh_noise(d, rate):
    """sample-and-hold 'pixel' noise; rate in Hz (scalar or array)"""
    n = N(d)
    rate = np.broadcast_to(np.asarray(rate, float), (n,))
    idx = np.floor(np.cumsum(rate / SR)).astype(int)
    vals = rng.uniform(-1, 1, idx.max() + 2)
    return vals[idx]


def metal_noise(d, rate, period=93):
    """NES short-mode periodic noise: metallic, pitched"""
    n = N(d)
    rate = np.broadcast_to(np.asarray(rate, float), (n,))
    pat = rng.choice([-1.0, 1.0], period)
    idx = np.floor(np.cumsum(rate / SR)).astype(int) % period
    return pat[idx]


def smooth_rand(d, rate, amt):
    """slow random wobble, ±amt"""
    n = N(d)
    k = max(2, int(d * rate) + 3)
    pts_ = rng.uniform(-1, 1, k)
    return np.interp(np.linspace(0, k - 1, n), np.arange(k), pts_) * amt


# ---------- filters ----------
def _sos(kind, fc, order=2):
    if kind == "band":
        lo, hi = fc
        return signal.butter(order, [max(20, lo), min(SR * 0.45, hi)], "band", fs=SR, output="sos")
    return signal.butter(order, min(SR * 0.45, max(20, fc)), kind, fs=SR, output="sos")


def lp(x, fc, order=2):
    return signal.sosfilt(_sos("low", fc, order), x)


def hp(x, fc, order=2):
    return signal.sosfilt(_sos("high", fc, order), x)


def bp(x, lo, hi, order=2):
    return signal.sosfilt(_sos("band", (lo, hi), order), x)


def svf(x, fc, q=0.707, mode="lp"):
    """time-varying TPT state-variable filter (fc may be an array)"""
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    g = np.tan(np.pi * np.clip(fc, 20, SR * 0.45) / SR)
    k = 1.0 / q
    a1 = 1.0 / (1.0 + g * (g + k))
    a2 = g * a1
    a3 = g * a2
    out = np.empty_like(x)
    ic1 = ic2 = 0.0
    xs = x.tolist()
    A1, A2, A3 = a1.tolist(), a2.tolist(), a3.tolist()
    o = out
    if mode == "lp":
        for i, v0 in enumerate(xs):
            v3 = v0 - ic2
            v1 = A1[i] * ic1 + A2[i] * v3
            v2 = ic2 + A2[i] * ic1 + A3[i] * v3
            ic1 = 2 * v1 - ic1
            ic2 = 2 * v2 - ic2
            o[i] = v2
    elif mode == "bp":
        for i, v0 in enumerate(xs):
            v3 = v0 - ic2
            v1 = A1[i] * ic1 + A2[i] * v3
            v2 = ic2 + A2[i] * ic1 + A3[i] * v3
            ic1 = 2 * v1 - ic1
            ic2 = 2 * v2 - ic2
            o[i] = v1
    else:
        for i, v0 in enumerate(xs):
            v3 = v0 - ic2
            v1 = A1[i] * ic1 + A2[i] * v3
            v2 = ic2 + A2[i] * ic1 + A3[i] * v3
            ic1 = 2 * v1 - ic1
            ic2 = 2 * v2 - ic2
            o[i] = v0 - k * v1 - v2
    return out


# ---------- fx ----------
def drive(x, amt):
    return np.tanh(x * amt) / np.tanh(amt)


def crush(x, bits):
    q = 2 ** (bits - 1)
    return np.round(x * q) / q


def hold(x, rate):
    """sample-rate reduction"""
    step = SR / rate
    idx = (np.floor(np.arange(len(x)) / step) * step).astype(int)
    return x[np.minimum(idx, len(x) - 1)]


def echo(x, delay, fb=0.35, taps=5, tail=0.0):
    d = N(delay)
    y = np.concatenate([x, np.zeros(N(tail))]) if tail else x.copy()
    src = y.copy()
    for k in range(1, taps + 1):
        s = k * d
        if s >= len(y):
            break
        y[s:] += src[: len(y) - s] * (fb ** k)
    return y


def verb(x, mix=0.2, size=1.0, tail=0.6, damp=4000):
    y = np.concatenate([x, np.zeros(N(tail))])
    wet = np.zeros_like(y)
    for dl, g in [(0.0297, 0.80), (0.0371, 0.78), (0.0411, 0.76), (0.0437, 0.74)]:
        D = int(dl * size * SR)
        a = np.zeros(D + 1)
        a[0] = 1
        a[-1] = -g
        wet += signal.lfilter([1.0], a, y)
    for dl, g in [(0.005, 0.7), (0.0017, 0.7)]:
        D = int(dl * SR)
        b = np.zeros(D + 1)
        b[0] = -g
        b[-1] = 1
        a = np.zeros(D + 1)
        a[0] = 1
        a[-1] = -g
        wet = signal.lfilter(b, a, wet)
    wet = lp(wet, damp)
    return y + wet * mix * 0.25


def fade(x, fin=0.001, fout=0.01):
    x = x.copy()
    a, b = N(fin), N(fout)
    if a > 1:
        x[:a] *= np.linspace(0, 1, a)
    if b > 1:
        x[-b:] *= np.linspace(1, 0, b) ** 2
    return x


# ---------- building blocks ----------
def kick(f0=150, f1=40, d=0.3, tau=0.035, click=0.25):
    f = glide(f0, f1, d, tau=tau)
    y = osc(f, "sine") * ad(d, 0.001, 4.5)
    c = hp(noise(0.012), 2000) * ad(0.012, 0.0005, 3) * click
    return place(y, c, 0)


def laser(f0, f1, d, tau=0.04, kind="square", duty=0.25):
    f = glide(f0, f1, d, tau=tau)
    return osc(f, kind, duty) * ad(d, 0.001, 4)


def ring(f, d, partials=((1, 1.0), (2.76, 0.5), (5.40, 0.25), (8.93, 0.12)), decay=6.0):
    t = tt(d)
    y = np.zeros_like(t)
    for r, a in partials:
        y += np.sin(2 * np.pi * f * r * t + rng.uniform(0, 6.28)) * a * np.exp(-decay * (1 + 0.35 * r) * t / d)
    return y * np.minimum(1, t / 0.001)


def crackle(d, density=60, start=1.0, end=0.0, bright=3000):
    n = N(d)
    y = np.zeros(n)
    prob = np.linspace(start, end, n) * density / SR
    hits = rng.random(n) < prob
    y[hits] = rng.uniform(-1, 1, hits.sum())
    y = hp(y, bright)
    # each tick a tiny ring
    return signal.lfilter([1.0], [1.0, -0.6], y)


def boom(size=1.0, d=None, bright=1.0):
    """pixel explosion: S&H noise sweeping down + sub kick + crackle tail"""
    d = d or (0.22 + 0.24 * size)
    rate = glide(9000 * bright, 500, d, tau=d * 0.35)
    n = sh_noise(d, rate)
    n = svf(n, glide(9000 * bright, 250, d, tau=d * 0.3), 0.8, "lp")
    body = n * ad(d, 0.0015, 3.2)
    k = kick(110 + 30 * size, 28, min(d, 0.25 + 0.12 * size), tau=0.05, click=0.0)
    y = canvas(d)
    place(y, body, 0, 1.0)
    place(y, k, 0, 0.55 + 0.12 * size)
    place(y, crackle(d, 40 + 20 * size, 1.0, 0.0) * ad(d, 0.01, 2), 0.02, 0.35)
    return drive(y, 1.6)


def growl(d, f0, f1, rough=32, formants=((600, 1.0), (1050, 0.55), (2400, 0.22)), jitter=0.06, breath=0.35, fcurve=None):
    base = fcurve if fcurve is not None else glide(f0, f1, d)
    f = base[: N(d)] * (1 + smooth_rand(d, 9, jitter))
    src = osc(f, "saw") * (1 + 0.65 * sh_noise(d, rough))
    src = src + noise(d) * breath
    out = np.zeros_like(src)
    for fc, a in formants:
        out += bp(src, fc * 0.78, fc * 1.25) * a
    return out


def note(freq, d, kind="square", duty=0.5, a=0.003, r=0.025, vib=0.0, vib_delay=0.12, vib_rate=6.0, sus=1.0, decay=0.0):
    t = tt(d)
    f = np.full_like(t, float(freq))
    if vib:
        f = f * 2 ** ((vib / 1200.0) * np.sin(2 * np.pi * vib_rate * t) * np.clip((t - vib_delay) / 0.08, 0, 1))
    y = osc(f, kind, duty)
    e = gate(d, a, r, sus)
    if decay:
        e *= np.exp(-decay * t)
    return y * e


# ---------- mastering ----------
def loudness_db(x, win=0.1):
    w = N(win)
    if len(x) < w:
        return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)
    sq = np.convolve(hp(x, 120) ** 2, np.ones(w) / w, "valid")
    return 10 * np.log10(sq.max() + 1e-12)


def master(x, target=-15.0, peak_db=-1.0, trim=True, tail_fade=0.012, keep_len=False):
    x = hp(np.asarray(x, float), 28)
    if trim and not keep_len:
        thr = np.abs(x).max() * 10 ** (-58 / 20)
        idx = np.nonzero(np.abs(x) > thr)[0]
        if len(idx):
            x = x[: min(len(x), idx[-1] + N(0.02))]
    g = 10 ** ((target - loudness_db(x)) / 20)
    x = x * g
    pk = np.abs(x).max()
    lim = 10 ** (peak_db / 20)
    if pk > lim:
        # gentle soft-knee squash above 0.7 of the limit, then hard scale
        x = np.where(np.abs(x) > 0.7 * pk, np.sign(x) * (0.7 * pk + np.tanh((np.abs(x) - 0.7 * pk) / (0.3 * pk)) * 0.3 * pk), x)
        x = x * lim / np.abs(x).max()
    return fade(x, 0.0008, tail_fade)
