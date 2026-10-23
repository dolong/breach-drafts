from mix import *
from recipes2 import chest
def xfade(a, b, d=0.08):
    n=N(d); w=np.linspace(0,1,n)[:,None]; return np.vstack([a[:-n], a[-n:]*(1-w)+b[:n]*w, b[n:]])
SEMIS=2; K=2**(SEMIS/12)
def handcrank_parts():
    s=S('Sherman_M4A1_t11')
    cycle1=xfade(seg(s,0.30,1.95), seg(s,4.95,5.60))                    # crank up, let it sag
    cycle2=xfade(seg(s,0.90,2.60), seg(s,4.95,5.90))                    # crank up again, release under the reveal
    full=xfade(cycle1, cycle2)
    top_src=(len(cycle1)/SR-0.08)+(2.20-0.90)                           # where cycle 2 reaches full speed (source seconds)
    return pitch(full,SEMIS), top_src/K, (len(cycle1)/SR-0.08)/K
def bunker_twice():
    x, top, c2 = handcrank_parts(); LEAD=0.05; reveal=LEAD+top; L=reveal+1.1
    c=Canvas(L)
    c.put(fade(chest(x,-12,-8),0.04,0),LEAD,0)
    c.put(cap(S('Impact_045'),1.2,0.5),0.0,-6)                          # the alarm being thrown
    c.put(cap(S('Impact_045'),1.0,0.5),LEAD+c2,-10)                     # second heave on the crank
    m=lp(chest(pitch(seg(S('Siren_M_16'),0.3,6.0),2),-12,None) if False else pitch(seg(S('Siren_M_16'),0.3,6.0),2),1800)
    c.put(fade(m,1.0,0),reveal+0.25,-14,align=(3.0-0.3)/2**(2/12))     # the city siren, far off
    r=S('Riser_078'); pk=t_at(r,-1); c.put(fade(seg(r,pk-1.6,pk),0.4,0.02),reveal-1.6,-13)
    c.put(ramp(rev(seg(S('Boom_040'),0,1.2)),2.0),reveal-1.2,-12)
    y=verb(c.y,0.7,-8,damp=6000); y=verb(y,2.6,-14,damp=4000)          # concrete room, then outside
    n=N(reveal); n1=N(LEAD+c2); g=np.ones(len(y))
    g[:n1]=np.linspace(0.6,0.8,n1); g[n1:n]=np.linspace(0.75,1.0,n-n1)**1.3   # second crank pushes harder
    g[n:]=np.linspace(1,0,len(y)-n)**1.5*0.6
    return y*g[:,None], reveal, LEAD+c2
def bunker_loop():
    s=S('Sherman_M4A1_t11'); cyc=xfade(seg(s,0.90,2.30), seg(s,4.95,5.60)); x=pitch(cyc,SEMIS)
    n=N(0.12); body=x[:-n].copy(); body[:n]=body[:n]*np.linspace(0,1,n)[:,None]+x[-n:]*np.linspace(1,0,n)[:,None]
    return chest(body,-12,-8)
