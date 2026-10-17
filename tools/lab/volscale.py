from common import *
FEE,SLIP=0.001,0.0005
U={s:b for s,b in B.items() if len(b)>=3000}
A={s:atr(b,100) for s,b in U.items()}   # slower ATR for stops
rows=[]
for N in [120,200,300,450]:
    for mode,vals in [("pct",[.04,.06,.08,.10]),("atr",[6,10,15,20,30])]:
        for v in vals:
            for s,b in U.items():
                kw=dict(sl_is_atr=1,sl_atr=v) if mode=="atr" else {}
                T=sim(b,N,0.0,v if mode=="pct" else 0.06,fee=FEE,slip=SLIP,ATR=A[s],**kw)
                a,t,al=split_stats(T)
                rows.append(dict(N=N,mode=mode,v=v,sym=s,y1=a["net"]*100,y2=t["net"]*100,dd=al["dd"]*100))
R=pd.DataFrame(rows); R.to_pickle("volscale.pkl")
g=R.groupby(["N","mode","v"]).agg(med_y1=("y1","median"),med_y2=("y2","median"),prof_both=("y1",lambda x:0),med_dd=("dd","median")).round(1)
g["prof_both"]=R.assign(pb=(R.y1>0)&(R.y2>0)).groupby(["N","mode","v"]).pb.sum()
print(g.to_string())
