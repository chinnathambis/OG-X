import pandas as pd, numpy as np
D="/home/claude/predictum/data_bybit/full/"
S=pd.read_csv("/home/claude/predictum/research/x/x_signals_full.csv"); S=S[S.coin!="SERAPH"].reset_index(drop=True)
TPS=[.01,.02,.03,.04,.08,.20]
rows=[]
for i,r in S.iterrows():
    d=pd.read_csv(D+f"{r.coin}USDT_15m_{pd.Timestamp(r.id_time_utc):%Y%m%d}_full.csv"); d["t"]=pd.to_datetime(d.time_ms,unit="ms"); d=d.set_index("t").astype(float)
    t0=pd.Timestamp(r.id_time_utc)+pd.Timedelta("45min")
    w=d.loc[t0:t0+pd.Timedelta(days=30)]
    if len(w)<10: rows.append(dict(coin=r.coin)); continue
    e=r.current_price; L=r.side=="Long"
    fav=(w.high/e-1) if L else (e/w.low-1)
    adv=(w.low/e-1) if L else (e/w.high-1)   # negative
    cummin=adv.cummin().values; f=fav.values
    def tps_before(stop):  # TPs hit before adverse reaches -stop
        hit=0
        for k in range(len(f)):
            if cummin[k]<=-stop: 
                # same bar ambiguity: count TPs hit on this bar only if fav before? conservative: no
                break
            while hit<6 and f[k]>=TPS[hit]: hit+=1
        return hit, (cummin<=-stop).any()
    tp8,st8=tps_before(.08); tp7,_=tps_before(.07); tp15,_=tps_before(.15); tp25,_=tps_before(.25); tpall,_=tps_before(9)
    first_tp1=np.argmax(f>=.01) if (f>=.01).any() else None
    mae_before_tp1 = cummin[first_tp1] if first_tp1 is not None else cummin[-1]
    rows.append(dict(coin=r.coin,date=r.id_time_utc[:10],score=r.score,peak30=f.max()*100,mae30=cummin[-1]*100,
        mae_pre_tp1=mae_before_tp1*100,tps_any=tpall,tps_before_8=tp8,stop8_hit=st8 and tp8<6,tps_before_dca1=tp7,tps_before_dca3=tp25))
R=pd.DataFrame(rows); pd.set_option("display.width",200)
print(R.round(1).to_string())
R.to_csv("x_outcomes.csv",index=False)
