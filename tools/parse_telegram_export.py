import re,html,sys,json,glob
D="/mnt/user-data/uploads/Downloads/Telegram Desktop/ChatExport_2026-10-17/"
files=["messages.html"]+[f"messages{i}.html" for i in range(2,7)]
out=[]
for f in files:
    t=open(D+f,encoding="utf-8").read()
    for m in re.finditer(r'<div class="message default clearfix( joined)?" id="message(\d+)">(.*?)(?=<div class="message (?:default|service))',t,re.S):
        body=m.group(3)
        d=re.search(r'class="pull_right date details" title="([^"]+)"',body)
        tx=re.search(r'<div class="text">(.*?)</div>\s*(?:<div class="signature|</div>)',body,re.S)
        txt=""
        if tx: txt=html.unescape(re.sub(r'<[^>]+>','',tx.group(1).replace("<br>","\n"))).strip()
        img=re.findall(r'href="(photos/[^"]+)"',body)
        rep=re.search(r'GoToMessage\((\d+)\)',body)
        out.append(dict(id=int(m.group(2)),date=d.group(1) if d else "",text=txt,photo=img[0] if img else "",reply=int(rep.group(1)) if rep else None))
json.dump(out,open("msgs.json","w"),ensure_ascii=False)
print(len(out)); print(out[0]["date"], "→", out[-1]["date"])
