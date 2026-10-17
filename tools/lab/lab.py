"""OG X research lab: fast C simulator + data cache. Usage: from lab import *"""
import ctypes, os, glob, numpy as np, pandas as pd
HERE=os.path.dirname(os.path.abspath(__file__)); DATA="/home/claude/predictum/data"
CACHE=os.path.join(HERE,"cache45.npz")
lib=ctypes.CDLL(os.path.join(HERE,"sim.so"))
class P(ctypes.Structure):
    _fields_=[(k,ctypes.c_double) for k in ["sl","fee","slip","be_trig","be_lock","trail","trail_atr","partial_tp","partial_frac"]]+[("time_stop",ctypes.c_int),("sl_is_atr",ctypes.c_int),("sl_atr",ctypes.c_double)]
dp=ctypes.POINTER(ctypes.c_double); ip=ctypes.POINTER(ctypes.c_int); bp=ctypes.POINTER(ctypes.c_ubyte)
lib.run.argtypes=[ctypes.c_int]+[dp]*6+[bp,bp,dp,P,ip,ip,ip,dp,dp,ctypes.c_int]; lib.run.restype=ctypes.c_int
SPLIT=pd.Timestamp("2026-01-01")
def resample(d, tf="45min"):
    return d.resample(tf,origin="start_day",label="left",closed="left").agg({"open":"first","high":"max","low":"min","close":"last","volume":"sum"}).dropna()
def build_cache(tf="45min", path=None):
    out={}
    for f in sorted(glob.glob(DATA+"/*_15m_recent.csv.gz")):
        sym=os.path.basename(f).split("_15m")[0]
        d=pd.read_csv(f); d["t"]=pd.to_datetime(d.time_ms,unit="ms"); d=d.set_index("t")[["open","high","low","close","volume"]].astype(float)
        b=resample(d,tf); out[sym]=b
    pd.to_pickle(out, path or CACHE.replace(".npz",f"_{tf}.pkl")); return out
_C={}
def bars(tf="45min"):
    if tf not in _C:
        p=CACHE.replace(".npz",f"_{tf}.pkl")
        _C[tf]=pd.read_pickle(p) if os.path.exists(p) else build_cache(tf)
    return _C[tf]
def atr(b,n=14):
    pc=b.close.shift(1); tr=pd.concat([b.high-b.low,(b.high-pc).abs(),(b.low-pc).abs()],axis=1).max(axis=1)
    return tr.rolling(n).mean().bfill().values
def levels(b,N,buf):
    up=(b.high.rolling(N).max().shift(1)*(1-buf)).fillna(0).values
    dn=(b.low.rolling(N).min().shift(1)*(1+buf)).fillna(0).values
    return up,dn
def sim(b,N,buf,sl,fee=0.0008,slip=0.0,okL=None,okS=None,ATR=None,up=None,dn=None,**kw):
    n=len(b); a=lambda x: np.ascontiguousarray(x,dtype=np.float64)
    O,H,L,C=a(b.open.values),a(b.high.values),a(b.low.values),a(b.close.values)
    if up is None: up,dn=levels(b,N,buf)
    up,dn=a(up),a(dn)
    okL=np.ascontiguousarray(np.ones(n,np.uint8) if okL is None else okL.astype(np.uint8))
    okS=np.ascontiguousarray(np.ones(n,np.uint8) if okS is None else okS.astype(np.uint8))
    ATR=a(np.zeros(n) if ATR is None else ATR)
    p=P(sl=sl,fee=fee,slip=slip,**{k:v for k,v in kw.items() if k in dict(P._fields_)})
    m=n; te,tx,td=(np.zeros(m,np.int32) for _ in range(3)); tr,tm=np.zeros(m),np.zeros(m)
    c=lambda x,t: x.ctypes.data_as(t)
    k=lib.run(n,c(O,dp),c(H,dp),c(L,dp),c(C,dp),c(up,dp),c(dn,dp),c(okL,bp),c(okS,bp),c(ATR,dp),p,c(te,ip),c(tx,ip),c(td,ip),c(tr,dp),c(tm,dp),m)
    T=pd.DataFrame(dict(ent=b.index[te[:k]],exit=b.index[tx[:k]],dir=td[:k],ret=tr[:k],mfe=tm[:k],ei=te[:k]))
    return T
def stats(r):
    r=np.asarray(r)
    if len(r)==0: return dict(n=0,net=0.0,dd=0.0,pf=0.0,win=0.0)
    eq=np.cumprod(1+r); dd=(1-eq/np.maximum.accumulate(eq)).max(); g,l=r[r>0].sum(),-r[r<0].sum()
    return dict(n=len(r),net=eq[-1]-1,dd=dd,pf=g/l if l>0 else 9.99,win=(r>0).mean())
def split_stats(T):
    a=T[T.ent<SPLIT].ret; t=T[T.ent>=SPLIT].ret
    return stats(a),stats(t),stats(T.ret)
V22=(180,.006,.06); V5=(210,0,.06); E=(450,0,.08)
PRESETS={"BTC":V22,"BTC5":V5,"ETH":E,"ZEC":V5,"DOGE":E,"QNT":E,"1000PEPE":V5,"XRP":E,"AAVE":E,"SOL":V5,"PAXG":V22,
 "SUI":(700,.01,.04),"UNI":(70,.006,.08),"ARB":(60,.006,.10),"STRK":(170,.01,.08),"WLD":(60,0,.04),"TAO":(60,0,.10),"EGLD":(680,.01,.10),
 "BCH":V5,"PENGU":E,"DASH":E,"1000BONK":E,"AERO":E,"BOME":E,"ENJ":E,"GALA":E,"RENDER":E,"VVV":E,
 "MINA":V22,"SEI":V22,"POL":V22,"GRT":V22,"RAYSOL":V5,"BLUR":V5,"KMNO":V5,
 "S":(60,.006,.10),"XLM":(180,0,.04),"KAIA":(700,0,.03),"SAND":(660,.01,.08),"AR":(680,0,.10),"TRX":(700,.006,.03)}
def sym(k): return ("BTC" if k=="BTC5" else k)+"USDT"
