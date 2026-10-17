import pandas as pd, numpy as np, os, itertools, json
D="/home/claude/predictum/data_bybit/full/"
S=pd.read_csv("/home/claude/predictum/research/x/x_signals_full.csv")
S=S[S.coin!="SERAPH"].reset_index(drop=True)
def b45(f):
    d=pd.read_csv(D+f); d["t"]=pd.to_datetime(d.time_ms,unit="ms"); d=d.set_index("t")[["open","high","low","close"]].astype(float)
    return d, d.resample("45min",origin="start_day",label="left",closed="left").agg({"open":"first","high":"max","low":"min","close":"last"}).dropna()
B={}
for i,r in S.iterrows():
    B[i]=b45(f"{r.coin}USDT_15m_{pd.Timestamp(r.id_time_utc):%Y%m%d}_full.csv")
Ns=list(range(40,801,10)); bufs=[x/1000 for x in range(0,16)]
res={}
info=[]
for i,r in S.iterrows():
    m15,b=B[i]; t=pd.Timestamp(r.id_time_utc)
    if t not in b.index: info.append((r.coin,"no bar")); continue
    k=b.index.get_loc(t); H=b.high.values; L=b.low.values
    long=r.side=="Long"
    ok=set()
    for N in Ns:
        if k-N-9<0: continue
        for bf in bufs:
            def lvl(j): return (H[j-N:j].max()*(1-bf)) if long else (L[j-N:j].min()*(1+bf))
            hit=lambda j: H[j]>=lvl(j) if long else L[j]<=lvl(j)
            if hit(k) and not any(hit(j) for j in range(k-8,k)): ok.add((N,bf))
    res[i]=ok
    # days since last N-high: lookback where candle is new high
    hh=0
    for N in range(10,len(H[:k])):
        if (H[k]>=H[k-N:k].max()) if long else (L[k]<=L[k-N:k].min()): hh=N
        else: break
    info.append((r.coin,r.id_time_utc,"newhigh over",hh,"bars"))
cnt={}
for i,ok in res.items():
    for p in ok: cnt[p]=cnt.get(p,0)+1
best=sorted(cnt.items(),key=lambda x:-x[1])[:15]
print("signals:",len(res)); print(best)
for x in info: print(x)
json.dump({str(i):sorted([list(p) for p in ok]) for i,ok in res.items()},open("ok.json","w"))
