import sys, itertools, pickle
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tune_presets as t, pandas as pd, numpy as np
sym=sys.argv[1]; b=t.load45(sym); idx=b.index; rows=[]
NS=list(range(60,401,20))+list(range(450,1001,50))
for N,buf,sl in itertools.product(NS,[0,0.003,0.006,0.01,0.015],[0.03,0.04,0.05,0.06,0.08,0.10]):
    tr=t.run(b,N,buf,sl)
    a=[r for i,r in tr if idx[i]<t.SPLIT]; e=[r for i,r in tr if idx[i]>=t.SPLIT]
    sa,se=t.stats(a),t.stats(e)
    rows.append(dict(sym=sym,N=N,buf=buf,sl=sl,**{'a_'+k:v for k,v in sa.items()},**{'e_'+k:v for k,v in se.items()}))
pd.DataFrame(rows).to_csv(f'grid_{sym}.csv', index=False)
