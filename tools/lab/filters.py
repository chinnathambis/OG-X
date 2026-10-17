from common import *
FEE,SLIP=0.001,0.0005
btc=B["BTCUSDT"]; bema=btc.close.ewm(span=480).mean(); BT=(btc.close>bema)
def masks(b):
    c=b.close; ema=c.ewm(span=480).mean(); emad=c.ewm(span=1600).mean()
    bt=BT.reindex(b.index).ffill().fillna(False).values
    v=b.volume; vr=(v.rolling(4).sum()/(v.rolling(200).mean()*4)).values
    a=pd.Series(atr(b,14),index=b.index)/c; ap=a.rolling(1000,min_periods=200).rank(pct=True).fillna(0.5).values
    sh=lambda x: np.r_[x[:1],x[:-1]]
    up_t=sh((c>ema).values); dn_t=sh((c<ema).values); upd=sh((c>emad).values); dnd=sh((c<emad).values); bt=sh(bt); vr=sh(np.nan_to_num(vr,nan=1)); ap=sh(ap)
    M={"base":(None,None),
       "coin trend":(up_t,dn_t),
       "BTC trend":(bt,~bt),
       "coin+BTC trend":(up_t&bt,dn_t&~bt),
       "50d trend":(upd,dnd),
       "volume≥avg":(vr>=1,vr>=1),
       "volatility≥40pct":(ap>=.4,ap>=.4),
       "coin trend+volume":(up_t&(vr>=1),dn_t&(vr>=1)),
       "longs only":(np.ones(len(b),bool),np.zeros(len(b),bool)),
       "longs only+coin trend":(up_t,np.zeros(len(b),bool))}
    return M
if __name__=="__main__":
    STRATS={"v22":V22,"v5":V5,"eth":E}
    rows=[]
    for s,b in B.items():
        if len(b)<3000: continue
        M=masks(b)
        for nm,(N,bf,sl) in STRATS.items():
            for f,(L,S) in M.items():
                T=sim(b,N,bf,sl,fee=FEE,slip=SLIP,okL=L,okS=S)
                a,t,al=split_stats(T)
                rows.append(dict(sym=s,strat=nm,filt=f,y1=a["net"]*100,y2=t["net"]*100,full=al["net"]*100,dd=al["dd"]*100,n=al["n"]))
    R=pd.DataFrame(rows); R.to_pickle("filters_universe.pkl")
    base=R[R.filt=="base"].set_index(["sym","strat"])
    out=[]
    for f,g in R.groupby("filt"):
        g=g.set_index(["sym","strat"])
        out.append(dict(filter=f,med_y1=round(g.y1.median(),1),med_y2=round(g.y2.median(),1),med_full=round(g.full.median(),1),med_dd=round(g.dd.median()),
            prof_both=int(((g.y1>0)&(g.y2>0)).sum()),beats_base_y1=round(((g.y1>base.y1).mean())*100),beats_base_y2=round(((g.y2>base.y2).mean())*100),
            trades=int(g.n.median())))
    print(pd.DataFrame(out).sort_values("med_full",ascending=False).to_string())
