from common import *
from portfolio import pstats
FEE,SLIP=0.001,0.0005
U=[s for s,b in B.items() if len(b)>=3000 and b.index[0]<=pd.Timestamp("2024-11-01")]
# liquidity chosen from Oct-Dec 2024 only (no hindsight)
liq={s:(B[s].close*B[s].volume).loc[:"2024-12-31"].mean() for s in U}
TOP20=[s for s,_ in sorted(liq.items(),key=lambda x:-x[1])[:20]]
days=pd.date_range("2024-10-01","2026-10-14",freq="D")
btc=B["BTCUSDT"]; BT=(btc.close>btc.close.ewm(span=480).mean())
def tmask(b):
    c=b.close; e=c.ewm(span=480).mean(); sh=lambda x: np.r_[x[:1],x[:-1]]; bt=sh(BT.reindex(b.index).ffill().fillna(False).values)
    return sh((c>e).values)&bt, sh((c<e).values)&~bt
def curve(T,b,volsize):
    if len(T)==0: return pd.Series(1.0,index=days)
    r=T.ret.values.copy()
    if volsize:
        a=pd.Series(atr(b,96),index=b.index)/b.close   # ~3-day ATR in %
        w=np.clip(0.01/a.values[np.maximum(T.ei.values-1,0)],0.2,3.0); r=r*w
    x=pd.Series(1+r,index=T.exit.dt.floor("D").values).groupby(level=0).prod().reindex(days).fillna(1.0)
    return x.cumprod()
rows=[]
for uni_name,uni in [("top20 liquid",TOP20),(f"all {len(U)}",U)]:
    for ens_name,chans in [("20d only",[640]),("ensemble 10/20/40/60d",[320,640,1280,1920]),("ensemble 20/40d",[640,1280])]:
        for filt in [False,True]:
            for vs in [False,True]:
                C=[]
                for s in uni:
                    b=B[s]; m=tmask(b) if filt else (None,None)
                    sub=[curve(sim(b,N,0,.12,fee=FEE,slip=SLIP,okL=m[0],okS=m[1]),b,vs) for N in chans]
                    C.append(pd.concat(sub,axis=1).mean(axis=1))
                P=pd.concat(C,axis=1).mean(axis=1)
                rows.append(pstats(P,f"{uni_name} · {ens_name} · {'trend' if filt else 'raw'} · {'vol-size' if vs else 'equal'}"))
    print(uni_name,flush=True)
R=pd.DataFrame(rows); R.to_csv("ensemble.csv",index=False); print(R.to_string()); print("TOP20:",[s.replace('USDT','') for s in TOP20])
