import sys, os, json
sys.path.insert(0, "/home/claude/predictum/tools")
import pandas as pd, numpy as np
import tune_presets as T
D="/home/claude/predictum/data"
def load(sym):
    d=pd.read_csv(f"{D}/{sym}_15m_recent.csv.gz"); d["t"]=pd.to_datetime(d.time_ms,unit="ms"); d=d.set_index("t")
    return d.resample("45min",origin="start_day",label="left",closed="left").agg({"open":"first","high":"max","low":"min","close":"last"}).dropna()
V22=(180,.006,.06); V5=(210,0,.06); ETH=(450,0,.08)
P={ "BTC":V22,"BTC5":V5,"ETH":ETH,"ZEC":V5,"DOGE":ETH,"QNT":ETH,"1000PEPE":V5,"XRP":ETH,"AAVE":ETH,"SOL":V5,"PAXG":V22,
 "SUI":(700,.01,.04),"UNI":(70,.006,.08),"ARB":(60,.006,.10),"STRK":(170,.01,.08),"WLD":(60,0,.04),"TAO":(60,0,.10),"EGLD":(680,.01,.10),
 "BCH":V5,"PENGU":ETH,"DASH":ETH,"1000BONK":ETH,"AERO":ETH,"BOME":ETH,"ENJ":ETH,"GALA":ETH,"RENDER":ETH,"VVV":ETH,
 "MINA":V22,"SEI":V22,"POL":V22,"GRT":V22,"RAYSOL":V5,"BLUR":V5,"KMNO":V5,
 "S":(60,.006,.10),"XLM":(180,0,.04),"KAIA":(700,0,.03),"SAND":(660,.01,.08),"AR":(680,0,.10),"TRX":(700,.006,.03)}
out={}
for k,(N,b,s) in P.items():
    sym=("BTC" if k=="BTC5" else k)+"USDT"
    try: bars=load(sym)
    except Exception as e: print(k,"ERR",e); continue
    tr=T.run(bars,N,b,s); idx=bars.index
    a=[r for i,r in tr if idx[i]<T.SPLIT]; t=[r for i,r in tr if idx[i]>=T.SPLIT]
    sa,st,sall=T.stats(a),T.stats(t),T.stats([r for i,r in tr])
    out[k]=dict(N=N,buf=b,sl=s,y1=round(sa["net"]*100),y2=round(st["net"]*100),n2=st["n"],dd=round(sall["dd"]*100),pf=round(sall["pf"],2),start=str(idx[0].date()))
    print(k,out[k],flush=True)
json.dump(out,open("rate.json","w"),indent=1)
