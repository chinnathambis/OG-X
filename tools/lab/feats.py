from common import *
FEE,SLIP=0.001,0.0005
STRATS={"v22":V22,"v5":V5,"eth":E}
btc=B["BTCUSDT"]; bema=btc.close.ewm(span=480).mean(); bret7=btc.close.pct_change(224)
rows=[]
for s,b in B.items():
    if len(b)<3000: continue
    c=b.close; ema=c.ewm(span=480).mean(); ema_d=c.ewm(span=32*50).mean()
    a14=pd.Series(atr(b,14),index=b.index); atrp=a14/c
    vol=b.volume; vr=vol.rolling(4).sum()/(vol.rolling(200).mean()*4)
    ret7=c.pct_change(224); 
    br=bret7.reindex(b.index).ffill(); bt=(btc.close>bema).reindex(b.index).ffill()
    for nm,(N,bf,sl) in STRATS.items():
        up,dn=levels(b,N,bf); width=pd.Series(up/np.where(dn>0,dn,np.nan)-1,index=b.index)
        wpct=width.rolling(1000,min_periods=200).rank(pct=True)
        apct=atrp.rolling(1000,min_periods=200).rank(pct=True)
        T=sim(b,N,bf,sl,fee=FEE,slip=SLIP)
        if len(T)==0: continue
        i=T.ei.values; j=np.maximum(i-1,0); d=T.dir.values
        prev=np.r_[np.nan,T.ret.values[:-1]]
        rows.append(pd.DataFrame(dict(sym=s,strat=nm,ent=T.ent,dir=d,ret=T.ret,mfe=T.mfe,
            btc_aligned=np.where(d==1,bt.values[j],1-bt.values[j]),
            coin_aligned=np.where(d==1,(c>ema).values[j],(c<ema).values[j]),
            long_trend_aligned=np.where(d==1,(c>ema_d).values[j],(c<ema_d).values[j]),
            vol_ratio=vr.values[j], atr_pct=apct.values[j], width_pct=wpct.values[j], width=width.values[j],
            rs_btc=d*(ret7.values[j]-br.values[j]), mom7=d*ret7.values[j],
            hour=T.ent.dt.hour.values, prev_ret=prev)))
F=pd.concat(rows,ignore_index=True); F["test"]=F.ent>=SPLIT
F.to_pickle("trades_feats.pkl"); print(len(F), F.groupby("test").size().to_dict())
