import os
import pandas as pd
def load(sym):
    d=pd.read_csv(os.path.join(os.environ.get("PREDICTUM_DATA", "data"), f"{sym}_15m.csv"))
    d['t']=pd.to_datetime(d.time_ms,unit='ms'); d=d.set_index('t')[['open','high','low','close','volume']]
    return d
def rs(d,rule):
    return d.resample(rule,origin='start_day',label='left',closed='left').agg({'open':'first','high':'max','low':'min','close':'last','volume':'sum'}).dropna()
import pandas as pd
btc15="""5.2.20 18:00 L|16.2.20 16:30 S|5.3.20 9:00 L|8.3.20 15:00 S|19.3.20 15:45 L|13.4.20 0:00 S|16.4.20 22:30 L|23.4.20 13:30 L|10.5.20 0:00 S|18.5.20 1:30 L|21.5.20 14:15 S|28.5.20 12:00 L|11.6.20 16:30 S|22.6.20 16:30 L|25.6.20 3:00 S|6.7.20 15:45 L|14.7.20 11:15 S|21.7.20 7:30 L|11.8.20 20:15 S|17.8.20 12:45 L|21.8.20 21:00 S|1.9.20 5:15 L|3.9.20 12:00 S|13.9.20 3:00 L|21.9.20 11:15 S|28.9.20 0:00 L|1.10.20 15:45 S|8.10.20 14:15 L|26.11.20 3:00 S|30.11.20 14:15 L|8.12.20 22:30 S|15.12.20 1:30 L|20.1.21 15:45 S|29.1.21 8:15 L|4.2.21 8:15 L|6.2.21 0:00 L|23.2.21 8:15 S|26.2.21 7:30 S|28.2.21 6:00 S|3.3.21 12:00 L|9.3.21 0:45 L|22.3.21 20:15 S|29.3.21 8:15 L|7.4.21 11:15 S|10.4.21 3:45 L|18.4.21 0:45 S|28.4.21 19:30 L|30.4.21 15:00 L|8.5.21 7:30 L|12.5.21 21:45 S"""
btc15pk=[92.5,157.02,25.86,1353.2,248.87,42.64,16.17,382.72,73.8,-60,55.27,128.74,54.52,20.84,39.54,19.05,8.56,310.45,12.97,42.18,39.96,23.49,137.37,66.04,45.38,17.23,17.41,811.92,90.54,20.55,54.4,1167.84,172.56,107.83,4.97,505.73,63.65,18,25.53,10.48,175.93,73.39,55.26,17.67,89.89,263.66,15.09,43.88,10.12,856.18]
eth="""22.3.21 20:15 S|31.3.21 18:00 L|19.5.21 3:00 S|4.7.21 6:45 L|13.7.21 5:15 S|24.7.21 16:30 L|7.9.21 15:00 S|20.9.21 12:00 S|6.10.21 12:45 L|16.11.21 0:45 S|30.11.21 11:15 L|4.12.21 4:30 S|29.12.21 23:15 S|4.2.22 15:00 L|18.2.22 14:15 S|18.3.22 14:15 L|11.4.22 9:00 S|15.7.22 20:15 L|19.8.22 21:45 S|9.9.22 12:00 L|15.9.22 15:00 S|23.10.22 21:45 L|8.11.22 18:00 S|30.11.22 0:00 L|16.12.22 9:00 S|4.1.23 3:00 L|10.2.23 15:45 S|16.2.23 15:45 L|3.3.23 1:30 S|13.3.23 15:00 L"""
ethpk=[94.86,1321.25,447.39,38.71,140.98,832.99,7.88,110.35,362.3,88.21,41.71,97.38,411.25,135.05,180.44,252.44,717.27,577.71,134.74,33.07,190.68,240.89,239.47,64.36,47.8,374.06,32.4,9.87,114.24,82.81]
def parse(s,pk):
    r=[]
    for x,p in zip(s.split('|'),pk):
        d,t,side=x.split(); r.append((pd.to_datetime(d+' '+t,format='%d.%m.%y %H:%M'),side,p))
    return pd.DataFrame(r,columns=['t','side','pk'])
BTC15=parse(btc15,btc15pk); ETH=parse(eth,ethpk)
import numpy as np, pandas as pd
def sim2(d,N,buf,sl,tpx,mode='touch'):
    H,L,O=d.high.values,d.low.values,d.open.values
    up=(d.high.rolling(N).max().shift(1)*(1-buf)).values; dn=(d.low.rolling(N).min().shift(1)*(1+buf)).values
    pos=0; last=0; ent=0; out=[]
    for i in range(N+1,len(d)):
        if pos==1:
            if L[i]<=ent*(1-sl) or H[i]>=ent*(1+tpx): pos=0
        elif pos==-1:
            if H[i]>=ent*(1+sl) or L[i]<=ent*(1-tpx): pos=0
        if H[i]>=up[i] and pos!=1:
            if pos==-1 or last!=1 or pos==0:
                pos=1; last=1; ent=max(O[i],up[i]); out.append((i,1)); continue
        if L[i]<=dn[i] and pos!=-1:
            pos=-1; last=-1; ent=min(O[i],dn[i]); out.append((i,-1))
    return out

# ---- reproduce the 50/50 fit ----
if __name__ == "__main__":
    b = rs(load('BTCUSDT'), '45min')
    sig = sim2(b, 210, 0, 0.06, 1e9)
    got = {(b.index[i], s) for i, s in sig}
    tr = {(t, 1 if s == 'L' else -1) for t, s in zip(BTC15.t, BTC15.side)}
    print("BTC v.5 matched", len(got & tr), "/", len(tr))
