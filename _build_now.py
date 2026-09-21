# -*- coding: utf-8 -*-
import json, re, datetime, sys
sys.path.insert(0,'/tmp/bld')
from data import RAW
from tr import TR

REPO="/tmp/wv"
LOC_ORDER=["האנוי","פו-לונג","נין-בין","סאפא","מפרץ הא-לונג","הוי-אן","פו-קוק","נה-טראנג"]
HE_COND={"su":"שמש","pa":"מעונן חלקית","cl":"מעונן","sh":"ממטרים","ts":"סופות רעמים"}

def f2c(f): return round((f-32)*5/9)

HEDGE=["in spots","in parts of the area","a stray","stray ","around in","in places"]
def icon_for(cond, rain):
    low=cond.lower()
    storm = any(w in low for w in ["thunderstorm","t-storm","t-shower","thundershower","tstorm"])
    hedged = any(h in low for h in HEDGE)
    main = low.split(";")[0]
    if storm and not hedged:
        return "ts"
    if storm and hedged:
        # main clause decides
        if "sun" in main and "cloud" not in main: return "pa"
        if "sun" in main: return "pa"
        return "cl"
    if any(w in low for w in ["rain","shower","drench","downpour","overcast with a touch"]):
        # rain dominant -> sh, unless only "a little/touch of" with a sunny main clause
        if ("little rain" in low or "touch of rain" in low) and "cloud" in main and "sun" not in main:
            return "cl"
        return "sh"
    if "sun" in low and "cloud" in low: return "pa"
    if "sun" in low: return "su"
    if "cloud" in low: return "cl"
    return "pa"

data={}
for loc,days in RAW.items():
    for d,(hiF,loF,cond,rain) in days.items():
        data[f"{loc}|{d:02d}/09"]={"hi":f2c(hiF),"lo":f2c(loF),"code":icon_for(cond,rain),
                                   "rain":rain,"cond":TR[cond],"typhoon":False,"tier":"near"}

def wrain(r):
    return "" if r is None else f'<br><span class="wrain">{r}% גשם</span>'

def card_html(loc):
    rows=[]
    for dd in range(21,31):
        day=data.get(f"{loc}|{dd:02d}/09")
        if not day: continue
        code=day["code"]; alt=day.get("cond") or HE_COND.get(code,"")
        rows.append(f'<div class="wrow"><div class="wdate">{dd:02d}/09</div>'
                    f'<img class="wicon" data-icon="{code}" alt="{alt}" title="{alt}">'
                    f'<div class="wtemps"><span class="hi">{day["hi"]}°</span>'
                    f'<span class="lo">{day["lo"]}°</span>{wrain(day.get("rain"))}</div></div>')
    return (f'<div class="wcard"><div class="wcard-head"><span>⋮⋮</span>{loc}</div>'
            f'<div class="wcard-body">{"".join(rows)}</div></div>')

cards_html="".join(card_html(l) for l in LOC_ORDER)

import subprocess
NOW=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
BUILD_ISO=NOW.strftime("%Y-%m-%dT%H:%M:00+07:00")
TIME_STR=NOW.strftime("%d/%m/%Y, %H:%M")

# ---- hourly (DEGRADED: derived from today's daily forecast, no live hourly scrape) ----
STEPS=[1.0,0.95,0.85,0.7,0.55,0.4]
hourly={}
for loc in LOC_ORDER:
    d=data.get(f"{loc}|21/09")
    if not d: continue
    hi,lo,code=d["hi"],d["lo"],d["code"]; r=d.get("rain") or 0
    hourly[loc]=[{"t":round(lo+(hi-lo)*f),"c":d.get("cond") or HE_COND.get(code,""),"r":r,"i":code} for f in STEPS]

# ---- forecast change diff ----
old=json.load(open(f"{REPO}/forecast_snapshot.json",encoding="utf-8"))
old_data=old.get("data",{})
# The previous run mislabeled its own generatedAt (wrote 14:00 while running at 09:15 ICT).
# Use the real commit timestamp of the previous deploy so the relative-time label is truthful.
_ct=subprocess.check_output(["git","-C",REPO,"log","-1","--format=%aI","--","forecast_snapshot.json"]).decode().strip()
prev_gen=datetime.datetime.fromisoformat(_ct).astimezone(datetime.timezone(datetime.timedelta(hours=7))).isoformat()
RANK={"su":0,"pa":1,"cl":2,"sh":3,"ts":4}
def classify(o,n):
    has_code="code" in o
    dr=(RANK.get(n["code"],2)-RANK.get(o["code"],2)) if has_code else 0
    dhi=n["hi"]-o["hi"]; dlo=n["lo"]-o["lo"]
    drain=(n.get("rain") or 0)-(o.get("rain") or 0)
    if not(abs(dr)>=2 or abs(dhi)>=4 or abs(dlo)>=4 or abs(drain)>=25): return None
    sev=abs(dr)*10+abs(dhi)+abs(dlo)+abs(drain)/10
    worse=dr>0 or dhi>2 or drain>15
    return ("worse" if worse else "better"),sev
changes=[]
for k,n in data.items():
    o=old_data.get(k)
    if not o: continue
    res=classify(o,n)
    if res: changes.append((res[1],res[0],k,o,n))
changes.sort(key=lambda x:-x[0]); top=changes[:3]

def rel(p,nn):
    try:
        pp=datetime.datetime.fromisoformat(p); n2=datetime.datetime.fromisoformat(nn)
        h=(n2-pp).total_seconds()/3600
        if h<1: return "לפני פחות משעה"
        if h<1.5: return "לפני כשעה"
        if h<24: return f"לפני כ-{round(h)} שעות"
        if h<48: return "לפני יום"
        return f"לפני כ-{round(h/24)} ימים"
    except Exception: return "לאחרונה"
rel_time=rel(prev_gen,BUILD_ISO) if prev_gen else "לאחרונה"

banners=""
for sev,dirn,k,o,n in top:
    loc,dt=k.split("|")
    cls="storm-alert-change-worse" if dirn=="worse" else "storm-alert-change-better"
    badge="החמרה" if dirn=="worse" else "שיפור"
    ic="📈" if dirn=="worse" else "📉"
    bc="worse" if dirn=="worse" else "better"
    desc=f'{loc} ({dt}): {o["hi"]}°/{o["lo"]}° → {n["hi"]}°/{n["lo"]}°'
    if n.get("rain") is not None and o.get("rain") is not None:
        desc+=f', סיכוי גשם {o["rain"]}%→{n["rain"]}%'
    banners+=(f'<div class="storm-alert {cls}"><span class="storm-alert-icon">{ic}</span>'
      f'<div class="storm-alert-body"><div class="storm-alert-title">'
      f'<span class="badge-change-{bc}">{badge} בתחזית</span>{loc} · {dt}</div>'
      f'<div class="storm-alert-desc">{desc}</div>'
      f'<div class="storm-alert-meta">בהשוואה לעדכון הקודם ({rel_time})</div></div></div>')

shop=json.load(open(f"{REPO}/shopping_list.json",encoding="utf-8"))
accom=json.load(open(f"{REPO}/accommodations_snapshot.json",encoding="utf-8"))
accom_list = accom.get("bookings",[]) if isinstance(accom,dict) else accom
accom_upd  = accom.get("updatedAt","") if isinstance(accom,dict) else ""
tpl=open(f"{REPO}/template.html",encoding="utf-8").read()

ZOOM_SRC="https://www.data.jma.go.jp/mscweb/data/himawari/img/se1/se1_b13_0540.jpg"
ZOOM_NOTE="תמונת לוויין JMA Himawari (fallback - לא היה דפדפן לצילום Zoom Earth בריצה זו) - "+TIME_STR

VND_USD=26150; ILS_USD=3.24
rep={
"__CARDS__":cards_html,
"__STORM_BANNERS__":banners,
"__ACCOMMODATIONS_DATA__":json.dumps(accom_list,ensure_ascii=False),
"__ACCOMMODATIONS_UPDATED__":json.dumps(accom_upd),
"__HOURLY_DATA__":json.dumps(hourly,ensure_ascii=False),
"__HOURLY_TODAY_LOC__":"null",
"__HOURLY_TODAY_OUTLOOK__":'""',
"__ZOOM_EARTH_IMG_SRC__":ZOOM_SRC,
"__ZOOM_EARTH_IMG_NOTE__":ZOOM_NOTE,
"__SHOP_ITEMS__":json.dumps(shop.get("items",[]),ensure_ascii=False),
"__SHOP_UPDATED__":json.dumps(shop.get("lastCheckedUtc","")),
"__TRAIN_UPDATED__":"11/09/2026",
"__TRAIN_WEEKDAY_TIMES__":"08:30 · 09:30 · 11:50<br>15:15 · 19:50 · 21:15<br>21:30 · 22:00",
"__TRAIN_WEEKEND_TIMES__":"06:00 · 09:00 · 09:30<br>11:20 · 15:20 · 17:30<br>18:00 · 18:30 · 19:00<br>19:45 · 20:30 · 21:00",
"__VND_PER_USD__":f"{VND_USD:,}","__VND_PER_ILS__":f"{round(VND_USD/ILS_USD):,}",
"__ILS_PER_USD__":f"{ILS_USD:.2f}","__VND_PER_USD_RAW__":str(VND_USD),"__ILS_PER_USD_RAW__":str(ILS_USD),
"__BUILD_DATE_ISO__":BUILD_ISO,"__TIME__":TIME_STR,
}
out=tpl
for k,v in rep.items(): out=out.replace(k,v)

ICONS=open('/tmp/bld/icons_block.txt',encoding='utf-8').read()
marker='<script>\nconst defaultItinerary'
assert marker in out
out=out.replace(marker,ICONS+marker,1)

print("LEFTOVER:",set(re.findall(r"__[A-Z_0-9]+__",out)))
print("DOUBLE_SUFFIX:", "(שעון ויאטנם) (שעון ויאטנם)" in out)
o1=len(re.findall(r"<div",out)); c1=len(re.findall(r"</div>",out))
print("DIV",o1,c1,"BALANCED",o1==c1)
print("CARDS",out.count('class="wcard"'),"ROWS",out.count('class="wrow"'),"WRAIN",out.count('class="wrain"'))
print("ICONS_BLOCK",out.count("const ICONS = {"))
print("HOURLY_EMPTY", json.dumps(hourly)=="{}", "N_HOURLY",len(hourly))
print("RAIN_NONE_COUNT",sum(1 for v in data.values() if v["rain"] is None))
print("ACCOM_BARE",rep["__ACCOMMODATIONS_DATA__"].startswith("["),"N_ACCOM",len(accom_list),"N_SHOP",len(shop.get("items",[])))
print("N_CHANGES",len(top),"REL",rel_time,"PREV",prev_gen)
open(f"{REPO}/index.html","w",encoding="utf-8").write(out)
json.dump({"generatedAt":BUILD_ISO,"data":data},open(f"{REPO}/forecast_snapshot.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("WROTE",len(out))
