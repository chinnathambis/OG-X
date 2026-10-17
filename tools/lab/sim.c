// OG X research simulator. One position at a time, intrabar breakout entries, flips on opposite signal.
// Order inside a bar: stop/trail/BE check (using levels from previous bars), partial TP, then signals.
#include <math.h>
typedef struct { double sl, fee, slip, be_trig, be_lock, trail, trail_atr, partial_tp, partial_frac; int time_stop; int sl_is_atr; double sl_atr; } P;
int run(int n, const double*O,const double*H,const double*L,const double*C,const double*UP,const double*DN,
        const unsigned char*okL,const unsigned char*okS,const double*ATR,P p,
        int*tEnt,int*tExit,int*tDir,double*tRet,double*tMfe,int maxT){
  int pos=0,nt=0,ent_i=0; double ent=0,stop=0,peak=0,rem=1,got=0,sd=0; int armed=0;
  for(int i=1;i<n;i++){
    if(pos!=0){
      // stop check
      double st=stop;
      if(p.trail>0){ double ts = pos==1? peak*(1-p.trail) : peak*(1+p.trail); if(pos==1? ts>st: ts<st) st=ts; }
      if(p.trail_atr>0 && ATR[i-1]>0){ double ts = pos==1? peak-p.trail_atr*ATR[i-1] : peak+p.trail_atr*ATR[i-1]; if(pos==1? ts>st: ts<st) st=ts; }
      int hit = pos==1? (L[i]<=st) : (H[i]>=st);
      int tstop = p.time_stop>0 && (i-ent_i)>=p.time_stop;
      if(hit || tstop){
        double px = hit ? (pos==1? fmin(O[i],st)*(1-p.slip) : fmax(O[i],st)*(1+p.slip)) : C[i];
        double r = got + rem*((px/ent-1)*pos) - p.fee;
        if(nt<maxT){tEnt[nt]=ent_i;tExit[nt]=i;tDir[nt]=pos;tRet[nt]=r;tMfe[nt]=pos==1?peak/ent-1:ent/peak-1;nt++;}
        pos=0;
      } else {
        // update peak, BE, partial
        if(pos==1){ if(H[i]>peak) peak=H[i]; } else { if(L[i]<peak) peak=L[i]; }
        double fav = pos==1? peak/ent-1 : ent/peak-1;
        if(p.be_trig>0 && !armed && fav>=p.be_trig){ armed=1; double bs = pos==1? ent*(1+p.be_lock):ent*(1-p.be_lock); if(pos==1? bs>stop: bs<stop) stop=bs; }
        if(p.partial_frac>0 && rem>0.999 && fav>=p.partial_tp){ got += p.partial_frac*p.partial_tp; rem -= p.partial_frac; }
      }
    }
    int sigL = UP[i]>0 && H[i]>=UP[i] && pos!=1;
    int sigS = DN[i]>0 && L[i]<=DN[i] && pos!=-1 && !sigL;
    if(sigL||sigS){
      int d = sigL?1:-1;
      double px = d==1? fmax(O[i],UP[i]) : fmin(O[i],DN[i]);
      if(pos!=0){ double xp = pos==1? px*(1-p.slip): px*(1+p.slip);
        double r = got + rem*((xp/ent-1)*pos) - p.fee;
        if(nt<maxT){tEnt[nt]=ent_i;tExit[nt]=i;tDir[nt]=pos;tRet[nt]=r;tMfe[nt]=pos==1?peak/ent-1:ent/peak-1;nt++;}
        pos=0; }
      if( (d==1 && okL[i]) || (d==-1 && okS[i]) ){
        pos=d; ent = d==1? px*(1+p.slip) : px*(1-p.slip); ent_i=i; peak = d==1? fmax(px,C[i]):fmin(px,C[i]); peak=px; rem=1; got=0; armed=0;
        sd = p.sl_is_atr ? p.sl_atr*ATR[i-1]/ent : p.sl;
        stop = d==1? ent*(1-sd) : ent*(1+sd);
      }
    }
  }
  if(pos!=0 && nt<maxT){ double r=got+rem*((C[n-1]/ent-1)*pos)-p.fee; tEnt[nt]=ent_i;tExit[nt]=n-1;tDir[nt]=pos;tRet[nt]=r;tMfe[nt]=pos==1?peak/ent-1:ent/peak-1;nt++; }
  return nt;
}
