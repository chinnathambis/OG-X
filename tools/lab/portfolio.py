from filters import masks, FEE, SLIP
from common import *
days=pd.date_range("2024-10-01","2026-10-14",freq="D")
def sub_equity(T):
    e=pd.Series(1.0,index=days)
    if len(T)==0: return e
    x=T.groupby(T.exit.dt.floor("D")).ret.apply(lambda r: np.prod(1+r.values))
    x=x.reindex(days).fillna(1.0); return x.cumprod()
def port(curves):
    P=pd.concat(curves,axis=1).mean(axis=1); return P
def pstats(P,lab):
    out={"portfolio":lab}
    for nm,(a,b) in {"2024-25":("2024-10-01","2025-12-31"),"2026":("2026-01-01","2026-10-14"),"all":("2024-10-01","2026-10-14")}.items():
        p=P.loc[a:b]; p=p/p.iloc[0]; out[nm+" net%"]=round((p.iloc[-1]-1)*100,1); out[nm+" maxDD%"]=round((1-p/p.cummax()).max()*100,1)
    r=P.pct_change().dropna(); out["sharpe(d)"]=round(r.mean()/r.std()*np.sqrt(365),2); return out
U={s:b for s,b in B.items() if len(b)>=3000 and b.index[0]<=pd.Timestamp("2024-11-01") and s not in ("BTCUSDT_dup",)}
MS={s:masks(b) for s,b in U.items()}
rows=[]
# A presets
C=[sub_equity(sim(B[sym(k)],*PRESETS[k],fee=FEE,slip=SLIP)) for k in PRESETS]; rows.append(pstats(port(C),"41 presets (in-sample choice)"))
for nm,(N,bf,sl) in {"ETH 450/0/8":E,"v.5 210/0/6":V5,"v2.2 180/0.6/6":V22,"600/0/8":(600,0,.08)}.items():
    for f in ["base","coin+BTC trend","BTC trend"]:
        C=[sub_equity(sim(b,N,bf,sl,fee=FEE,slip=SLIP,okL=MS[s][f][0],okS=MS[s][f][1])) for s,b in U.items()]
        rows.append(pstats(port(C),f"all {len(U)} coins · {nm} · {f}"))
R=pd.DataFrame(rows); print(R.to_string()); R.to_csv("portfolio.csv",index=False)
