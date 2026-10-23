from mix import *
from recipes2 import chest
from recipes6 import xfade, SEMIS, K
def bunker_twice_full(gap=0.12, semis=SEMIS, rel_end=6.90):
    Kx=2**(semis/12)
    s=S('Sherman_M4A1_t11')
    # crank 1: wind up, then let it run all the way down (808 → ~400 Hz) before cranking again
    c1=fade(xfade(seg(s,0.30,2.05), seg(s,4.95,rel_end)),0,0.45)
    # crank 2: wind up from the bottom, hold, then release under the reveal
    c2=xfade(seg(s,0.30,2.60), seg(s,4.95,7.40))
    c1=pitch(c1,semis); c2=pitch(c2,semis)
    LEAD=0.05; t2=LEAD+len(c1)/SR+gap; reveal=t2+(2.20-0.30)/Kx; L=reveal+1.9
    c=Canvas(L); c.put(fade(chest(c1,-12,-8),0.04,0),LEAD,0); c.put(fade(chest(c2,-12,-8),0.03,0),t2,0)
    c.put(cap(S('Impact_045'),1.2,0.5),0.0,-6)                      # the alarm being thrown
    c.put(cap(S('Impact_045'),1.0,0.5),t2,-9)                       # second heave on the crank
    m=lp(pitch(seg(S('Siren_M_16'),0.3,6.0),2),1800)
    c.put(fade(m,1.0,0),reveal+0.25,-14,align=(3.0-0.3)/2**(2/12))  # the city siren, far off
    r=S('Riser_078'); pk=t_at(r,-1); c.put(fade(seg(r,pk-1.6,pk),0.4,0.02),reveal-1.6,-13)
    c.put(ramp(rev(seg(S('Boom_040'),0,1.2)),2.0),reveal-1.2,-12)
    y=verb(c.y,0.7,-8,damp=6000); y=verb(y,2.6,-14,damp=4000)
    n1,n2,n=N(t2-gap),N(t2),N(reveal); g=np.ones(len(y))
    g[:max(n1,n2)]=0.7; g[n1:n2]=np.linspace(0.7,0.75,max(0,n2-n1)); g[n2:n]=np.linspace(0.75,1.0,n-n2)**1.3
    g[n:]=0.55*np.linspace(1,0,len(y)-n)**1.2                        # release keeps falling under the reveal, fades out
    return y*g[:,None], reveal, t2
