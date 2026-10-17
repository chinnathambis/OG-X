from filters import masks, FEE, SLIP
from common import *
MS={k:masks(B[sym(k)]) for k in PRESETS}
rows=[];base=None
for f in ["base","BTC trend","coin+BTC trend","coin trend","50d trend","volatility≥40pct","volume≥avg"]:
    R=preset_table(lambda k,b,N,bf,sl: sim(b,N,bf,sl,fee=FEE,slip=SLIP,okL=MS[k][f][0],okS=MS[k][f][1]))
    if base is None: base=R
    s=summ(R,f); s["better_both"]=int(((R.y1>base.y1+1)&(R.y2>base.y2+1)).sum()); s["worse_both"]=int(((R.y1<base.y1-1)&(R.y2<base.y2-1)).sum()); s["lower_dd"]=int((R.dd<base.dd-1).sum())
    s["ret/dd"]=round((R.full/R.dd).median(),2)
    rows.append(s)
print(pd.DataFrame(rows).to_string())
