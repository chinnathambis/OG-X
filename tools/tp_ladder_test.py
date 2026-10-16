import sys, json
sys.path.insert(0,"/home/claude/predictum/tools")
import numpy as np, pandas as pd, tune_presets as T
import importlib.util
src=open("rate.py").read().split("out={}")[0]
exec(src)
FEE=0.0008
def sim(b,N,buf,sl,tps,w,worst=True):
    H,L,O,C=b.high.values,b.low.values,b.open.values,b.close.values
    up=b.high.rolling(N).max().shift(1).values*(1-buf); dn=b.low.rolling(N).min().shift(1).values*(1+buf)
    ipos=0; ent=0; rem=0; got=0; hit=0; res=[]; live=False
    def close_rest(px):
        nonlocal rem,got,live
        if live: res.append(got+rem*((px/ent-1)*ipos)-FEE)
        live=False
    for i in range(N+1,len(b)):
        if ipos!=0:
            fav=H[i] if ipos==1 else L[i]; adv=L[i] if ipos==1 else H[i]
            stop=ent*(1-sl) if ipos==1 else ent*(1+sl)
            sh=(adv<=stop) if ipos==1 else (adv>=stop)
            def take():
                nonlocal hit,rem,got,live
                while live and hit<len(tps):
                    tp=ent*(1+tps[hit]) if ipos==1 else ent/(1+tps[hit])
                    if (fav>=tp if ipos==1 else fav<=tp):
                        q=min(w[hit],rem); got+=q*tps[hit] if ipos==1 else q*(ent/tp-1); rem-=q; hit+=1
                    else: break
                if live and rem<=1e-9: res.append(got-FEE); live=False
            if worst:
                if sh: close_rest(stop); ipos=0
                else: take()
            else:
                take()
                if sh: close_rest(stop); ipos=0
        sig=0
        if H[i]>=up[i] and ipos!=1: sig=1
        elif L[i]<=dn[i] and ipos!=-1: sig=-1
        if sig:
            px=max(O[i],up[i]) if sig==1 else min(O[i],dn[i])
            if ipos!=0: close_rest(px)
            ipos,ent,rem,got,hit,live=sig,px,1.0,0.0,0,True
    if ipos!=0: close_rest(C[-1])
    return res
LAD=[.003,.01,.02,.03,.10]
S={"Hold (now)":([],[]),"TP ladder 20% each":(LAD,[.2]*5),"All out at TP1 0.3%":(LAD,[1,0,0,0,0]),"All out at TP2 1%":(LAD,[0,1,0,0,0]),"All out at TP3 2%":(LAD,[0,0,1,0,0]),"All out at TP5 10%":(LAD,[0,0,0,0,1]),"Half at TP3, rest hold":(LAD,[0,0,.5,0,0])}
rows=[]
for k,(N,bf,sl) in P.items():
    b=load(("BTC" if k=="BTC5" else k)+"USDT")
    for name,(tp,w) in S.items():
        for worst in ([True,False] if tp else [True]):
            r=sim(b,N,bf,sl,tp,w,worst); st=T.stats(r)
            rows.append(dict(coin=k,scen=name,worst=worst,net=st["net"]*100,dd=st["dd"]*100,win=st["win"]*100,n=st["n"]))
    print(k,flush=True,end=" ")
R=pd.DataFrame(rows); R.to_csv("tp_ladder.csv",index=False)
