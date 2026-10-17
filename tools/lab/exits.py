from common import *
FEE,SLIP=0.001,0.0005
ATRS={k:atr(B[sym(k)]) for k in PRESETS}
V={"base":{}}
for t in [.02,.03,.04,.05,.08]: V[f"BE@{t*100:g}%"]=dict(be_trig=t,be_lock=.002)
for t in [.05,.08,.12,.15,.20,.30]: V[f"trail {t*100:g}%"]=dict(trail=t)
for m in [3,5,8,12]: V[f"trail {m}xATR"]=dict(trail_atr=m)
for ts in [64,128,256,512]: V[f"time {ts} bars"]=dict(time_stop=ts)
for pt in [.02,.03,.05,.08]: V[f"50% @ +{pt*100:g}%"]=dict(partial_tp=pt,partial_frac=.5)
V["50%@3% + BE@3%"]=dict(partial_tp=.03,partial_frac=.5,be_trig=.03,be_lock=.002)
V["50%@5% + BE@5%"]=dict(partial_tp=.05,partial_frac=.5,be_trig=.05,be_lock=.002)
V["BE@5% + trail 15%"]=dict(be_trig=.05,be_lock=.002,trail=.15)
V["trail 8xATR + BE@5%"]=dict(trail_atr=8,be_trig=.05,be_lock=.002)
rows=[]; base=None
for name,kw in V.items():
    R=preset_table(lambda k,b,N,bf,sl: sim(b,N,bf,sl,fee=FEE,slip=SLIP,ATR=ATRS[k],**kw))
    if base is None: base=R
    s=summ(R,name)
    s["better_y1"]=int((R.y1>base.y1+1).sum()); s["better_y2"]=int((R.y2>base.y2+1).sum()); s["better_both"]=int(((R.y1>base.y1+1)&(R.y2>base.y2+1)).sum())
    s["lower_dd"]=int((R.dd<base.dd-1).sum())
    rows.append(s)
D=pd.DataFrame(rows); print(D.to_string()); D.to_csv("exits_presets.csv",index=False)
