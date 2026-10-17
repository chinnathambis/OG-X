from common import *
from portfolio import sub_equity, port, pstats
FEE,SLIP=0.001,0.0005
U=[s for s,b in B.items() if len(b)>=3000 and b.index[0]<=pd.Timestamp("2024-11-01")]
def trendmask(b,span_days,btc):
    bpd={"45min":32,"2h":12,"4h":6,"1D":1}
    c=b.close; per=bpd[TF]
    ema=c.ewm(span=max(int(15*per),3)).mean()
    be=btc.close.ewm(span=max(int(15*per),3)).mean(); bt=(btc.close>be).reindex(b.index).ffill().fillna(False).values
    sh=lambda x: np.r_[x[:1],x[:-1]]
    u=sh((c>ema).values)&sh(bt); d=sh((c<ema).values)&sh(~bt); return u,d
rows=[]
for TF,per in [("45min",32),("2h",12),("4h",6),("1D",1)]:
    BB=bars(TF); btc=BB["BTCUSDT"]
    for days_ch in [7,14,20,30,55]:
        N=max(int(days_ch*per),5)
        for sl in [.08,.12,.20]:
            for filt in [False,True]:
                C=[]
                for s in U:
                    b=BB[s]; 
                    m=trendmask(b,15,btc) if filt else (None,None)
                    C.append(sub_equity(sim(b,N,0,sl,fee=FEE,slip=SLIP,okL=m[0],okS=m[1])))
                r=pstats(port(C),f"{TF} {days_ch}d ch sl{int(sl*100)} {'trend' if filt else 'raw'}"); rows.append(r)
        print(TF,days_ch,flush=True)
R=pd.DataFrame(rows); R.to_csv("tf_basket.csv",index=False)
print(R.sort_values("all net%",ascending=False).head(25).to_string())
