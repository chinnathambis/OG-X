from common import *
FEE,SLIP=0.001,0.0005
LV=[0,-.07,-.15,-.25]
def dca_trades(b,N,bf,final_sl,w):
    T=sim(b,N,bf,final_sl,fee=0,slip=SLIP)   # stop at final level, flips as usual
    H,L=b.high.values,b.low.values; idx={t:i for i,t in enumerate(b.index)}
    out=[]
    for _,t in T.iterrows():
        i0,i1=idx[t.ent],idx[t.exit]; d=t.dir; e=1.0
        # price path relative to entry
        if d==1: worst=np.minimum.accumulate(L[i0:i1+1])/1.0
        else: worst=np.maximum.accumulate(H[i0:i1+1])
        ent_px=None
        # recover entry px and exit px from ret: ret=(px_exit/ent-1)*d (fee 0)
        # approximate entry px with level: use first bar open-based? use ret directly
        r_last=t.ret  # move from entry to exit for 1 unit
        # adverse excursion over trade
        mae = (L[i0:i1+1].min()/b.close.values[i0]-1) if d==1 else (b.close.values[i0]/H[i0:i1+1].max()-1)
        filled=[k for k,l in enumerate(LV) if mae<=l]
        # each add k bought at (1+LV[k]) relative to entry; exit at (1+r_last) relative to entry
        exitrel=1+r_last
        pnl=sum(w[k]*(exitrel/(1+LV[k])-1) for k in filled)
        out.append(pnl/sum(w) - FEE*len(filled)/len(LV))   # per unit of max capital
    return np.array(out), T
rows=[]
for nm,w in [("no DCA (preset stop)",None),("1-1-2-3, stop -30%",[1,1,2,3]),("1-1-2-4, stop -30%",[1,1,2,4]),("1-1-1-1, stop -30%",[1,1,1,1]),("entry only, stop -30%",[1,0,0,0])]:
    res=[]
    for k in PRESETS:
        N,bf,sl=PRESETS[k]; b=B[sym(k)]
        if w is None:
            T=sim(b,N,bf,sl,fee=FEE,slip=SLIP); r=T.ret.values
        else:
            r,T=dca_trades(b,N,bf,.30,w)
        a=stats(r[(T.ent<SPLIT).values]); t=stats(r[(T.ent>=SPLIT).values]); f=stats(r)
        res.append((a["net"]*100,t["net"]*100,f["dd"]*100,r.min()*100))
    R=np.array(res); rows.append(dict(plan=nm,med_y1=round(np.median(R[:,0])),med_y2=round(np.median(R[:,1])),med_dd=round(np.median(R[:,2])),worst_trade_med=round(np.median(R[:,3]),1),worst_trade_min=round(R[:,3].min(),1)))
print(pd.DataFrame(rows).to_string())
