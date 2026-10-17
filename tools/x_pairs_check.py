import sys, glob, pandas as pd, numpy as np
sys.path.insert(0,"/home/claude/predictum/tools"); import tune_presets as T
D="/home/claude/predictum/data_bybit/full/"
ST={"X 200/0.9/8":(200,.009,.08),"BTC v2.2":(180,.006,.06),"BTC v.5":(210,0,.06),"ETH":(450,0,.08)}
rows=[]
for f in sorted(glob.glob(D+"*_full.csv")):
    coin=f.split("/")[-1].split("USDT")[0]; date=f.split("_")[-2]
    d=pd.read_csv(f); d["t"]=pd.to_datetime(d.time_ms,unit="ms"); d=d.set_index("t")
    b=d.resample("45min",origin="start_day",label="left",closed="left").agg({"open":"first","high":"max","low":"min","close":"last"}).dropna()
    row=dict(coin=coin,date=date,days=round(len(b)*45/1440))
    for k,(N,bf,sl) in ST.items():
        s=T.stats([r for i,r in T.run(b,N,bf,sl)]); row[k]=round(s["net"]*100); row[k+" n"]=s["n"]
    rows.append(row)
R=pd.DataFrame(rows); pd.set_option("display.width",220); print(R.to_string())
for k in ST: print(k, "median",R[k].median(),"profitable",(R[k]>0).sum(),"/",len(R))
R.to_csv("x_pairs_og.csv",index=False)
