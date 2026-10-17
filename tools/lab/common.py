import sys; sys.path.insert(0,"/home/claude/predictum/tools/lab")
from lab import *
B=bars()
KEYS=[k for k in PRESETS if k!="BTC5"]+["BTC5"]
def preset_table(fn, keys=KEYS):
    """fn(key,b,N,buf,sl)->trades df. Returns per-preset stats df."""
    rows=[]
    for k in keys:
        N,bf,sl=PRESETS[k]; b=B[sym(k)]; T=fn(k,b,N,bf,sl)
        a,t,f=split_stats(T)
        rows.append(dict(key=k,n=f["n"],full=f["net"]*100,y1=a["net"]*100,y2=t["net"]*100,dd=f["dd"]*100,pf=f["pf"],win=f["win"]*100))
    return pd.DataFrame(rows)
def summ(R,label):
    return dict(variant=label,med_full=round(R.full.median()),med_2026=round(R.y2.median(),1),prof_full=int((R.full>0).sum()),prof_2026=int((R.y2>0).sum()),med_dd=round(R.dd.median()),med_pf=round(R.pf.median(),2),n=len(R))
