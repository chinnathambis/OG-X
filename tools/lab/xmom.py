from common import *
from portfolio import sub_equity, port, pstats
FEE,SLIP=0.001,0.0005
U=[s for s,b in B.items() if len(b)>=3000 and b.index[0]<=pd.Timestamp("2024-11-01")]
# daily close matrix -> momentum ranks (known at prior day close)
D=pd.concat({s:B[s].close.resample("1D").last() for s in U},axis=1)
btc=B["BTCUSDT"]; bema=btc.close.ewm(span=480).mean(); BT=(btc.close>bema)
rows=[]
for look in [7,14,30,60]:
    mom=D.pct_change(look); rk=mom.rank(axis=1,pct=True).shift(1)   # yesterday's rank
    for top in [0.2,0.33,0.5]:
        for filt in ["mom only","mom+trend"]:
            for side in ["both","long only"]:
                C=[]
                for s in U:
                    b=B[s]; r=rk[s].reindex(b.index,method="ffill").fillna(0.5).values
                    okL=r>=1-top; okS=(r<=top) if side=="both" else np.zeros(len(b),bool)
                    if filt=="mom+trend":
                        c=b.close; ema=c.ewm(span=480).mean(); sh=lambda x: np.r_[x[:1],x[:-1]]
                        bt=BT.reindex(b.index).ffill().fillna(False).values
                        okL=okL&sh((c>ema).values)&sh(bt); okS=okS&sh((c<ema).values)&sh(~bt)
                    C.append(sub_equity(sim(b,640,0,.12,fee=FEE,slip=SLIP,okL=okL,okS=okS)))
                rows.append(pstats(port(C),f"mom{look}d top{int(top*100)}% {filt} {side}"))
    print(look,flush=True)
R=pd.DataFrame(rows); R.to_csv("xmom.csv",index=False); print(R.sort_values("all net%",ascending=False).head(15).to_string()); print(R[R.portfolio.str.contains("long only")].sort_values("all net%",ascending=False).head(5).to_string())
