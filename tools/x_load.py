import pandas as pd, glob
SIG=pd.read_csv('/home/claude/predictum/research/x/x_signals.csv')
def load(coin,ts):
    f=glob.glob(f'/mnt/user-data/uploads/Predictum/data_bybit/{coin}USDT_15m_{pd.Timestamp(ts):%Y%m%d}.csv')[0]
    d=pd.read_csv(f); d['t']=pd.to_datetime(d.time_ms,unit='ms'); d=d.set_index('t')[['open','high','low','close']].astype(float)
    b45=d.resample('45min',origin='start_day',label='left',closed='left').agg({'open':'first','high':'max','low':'min','close':'last'}).dropna()
    return d,b45
