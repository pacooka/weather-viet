# -*- coding: utf-8 -*-
import json, re, sys, datetime
sys.path.insert(0, "/sessions/serene-gifted-brown/mnt/WeatherViet")
from build_data2 import c, tr, tr_hourly, icon_for

REPO = "/tmp/gh_deploy_2"

LOC_ORDER = ["האנוי","פו-לונג","נין-בין","סאפא","מפרץ הא-לונג","הוי-אן","פו-קוק","נה-טראנג"]

RAW = {
"האנוי": [
 (13,87,76,80,1.5,"Times of clouds and sun with a passing shower or two"),
 (14,84,74,89,2.5,"Cloudy with occasional rain in the afternoon"),
 (15,83,75,90,3.5,"Occasional rain in the morning; otherwise, cloudy"),
 (16,86,75,95,4,"Remaining cloudy with showers, some heavy"),
 (17,88,76,59,1,"A heavy thunderstorm in the morning; otherwise, variable clouds"),
 (18,91,76,56,1,"Mostly cloudy; a morning thunderstorm in parts of the area followed by a little rain in the afternoon"),
 (19,96,78,55,2,"Mostly cloudy and hot with occasional rain"),
 (20,99,79,55,2,"Mainly cloudy and hot with occasional rain"),
 (21,100,79,9,None,"Partly sunny; very hot and humid"),
 (22,92,77,55,2,"Mostly cloudy and hot with occasional rain"),
 (23,91,78,7,None,"Mostly sunny, hot and less humid"),
 (24,92,77,0,None,"Plenty of sunshine with low humidity"),
 (25,89,74,5,None,"Plenty of sunshine"),
 (26,88,78,56,1,"A blend of sun and clouds with a thunderstorm in the area in the afternoon"),
 (27,87,77,62,1,"Mostly cloudy with a couple of showers and a thunderstorm in the afternoon"),
],
"פו-לונג": [
 (13,85,74,60,0.5,"Mostly cloudy with a passing shower in the afternoon"),
 (14,79,74,95,5,"Cloudy; a shower in the morning followed by heavy showers in the afternoon; watch for flooding"),
 (15,80,73,75,2,"A little morning rain; otherwise, cloudy"),
 (16,85,73,93,5,"Remaining cloudy with showers"),
 (17,89,74,91,3.5,"Periods of rain"),
 (18,88,74,62,3.5,"Rain at times"),
 (19,87,73,63,2,"Considerable cloudiness; a couple of morning showers and a thunderstorm followed by a little rain in the afternoon"),
 (20,88,74,55,2.5,"Mainly cloudy with a little rain"),
 (21,89,76,55,2,"Mostly cloudy; a thunderstorm in spots in the morning followed by a little rain in the afternoon"),
 (22,91,75,55,2,"Mostly cloudy and hot with a little rain"),
 (23,91,75,55,1,"A little rain in the morning; otherwise, very warm with clouds giving way to sun"),
 (24,90,76,1,None,"Less humid with plenty of sunshine"),
 (25,88,72,5,None,"Sunny"),
 (26,87,74,62,1,"Mostly cloudy with a couple of showers and a thunderstorm in the afternoon"),
 (27,86,76,59,1,"Mostly cloudy with a couple of showers in the afternoon"),
],
"נין-בין": [
 (13,83,75,70,1.5,"Breezy in the morning; cloudy and not as warm with a passing shower or two in the afternoon"),
 (14,82,74,91,3,"Considerable cloudiness with periods of rain, some heavy in the afternoon; watch for flash flooding"),
 (15,81,74,75,3,"Cloudy with occasional rain in the afternoon"),
 (16,83,75,90,3,"Cloudy with a couple of showers in the afternoon"),
 (17,88,75,91,3,"Periods of rain"),
 (18,89,77,55,2,"Mostly cloudy with a little rain"),
 (19,87,76,55,2,"Considerable cloudiness with a little rain"),
 (20,88,77,55,2,"Cloudy most of the time; a thunderstorm in spots in the morning followed by a little rain in the afternoon"),
 (21,89,78,40,0.5,"A thunderstorm in parts of the area in the morning; otherwise, mostly cloudy"),
 (22,91,77,49,1,"A morning shower in spots; otherwise, mostly cloudy and hot"),
 (23,91,77,11,None,"Sunny, hot and less humid"),
 (24,90,78,0,None,"Low humidity with plenty of sunshine"),
 (25,88,76,5,None,"Sunshine"),
 (26,86,78,65,2,"Mostly cloudy with a couple of showers and a thunderstorm in the afternoon"),
 (27,85,78,65,2,"Intervals of clouds and sunshine with a couple of showers and a thunderstorm in the afternoon"),
],
"סאפא": [
 (13,74,62,9,None,"Sunny to partly cloudy and pleasant"),
 (14,70,62,55,1,"Mostly cloudy with a thundershower in spots"),
 (15,74,61,67,2,"Times of sun and clouds with a brief shower or two in the afternoon"),
 (16,73,61,55,2,"A morning thunderstorm in parts of the area; otherwise, periods of clouds and sunshine"),
 (17,74,62,55,2.5,"Intervals of clouds and sunshine with a thunderstorm"),
 (18,67,57,55,2.5,"Mostly cloudy with a thundershower in parts of the area"),
 (19,75,60,55,2,"A sun-and-cloud mix with a thundershower in parts of the area"),
 (20,74,59,55,2,"Partial sunshine with a thundershower in spots"),
 (21,76,60,55,1,"A thundershower in spots in the morning; otherwise, partly sunny"),
 (22,74,59,55,2,"Partly sunny with a thunderstorm in spots"),
 (23,71,57,55,2,"Some sunshine giving way to clouds; a thundershower in spots in the morning followed by a little rain in the afternoon"),
 (24,72,56,55,1,"Mostly cloudy with a little rain in the afternoon"),
 (25,73,59,25,None,"Partly sunny"),
 (26,73,57,25,None,"Periods of clouds and sunshine"),
 (27,72,61,55,2.5,"Mostly cloudy and humid with a little rain"),
],
"מפרץ הא-לונג": [
 (13,84,78,71,1.5,"Mostly cloudy with a couple of showers in the afternoon"),
 (14,85,76,88,3,"A steady morning breeze; otherwise, cloudy with periods of rain in the afternoon"),
 (15,81,75,75,1.5,"Cloudy with a little rain in the afternoon"),
 (16,83,76,70,1.5,"A couple of soaking morning showers; otherwise, mostly cloudy"),
 (17,86,75,65,1.5,"A couple of morning thunderstorms; otherwise, intervals of clouds and sunshine"),
 (18,90,76,55,1,"A touch of rain in the morning; otherwise, mostly cloudy"),
 (19,87,76,56,1,"A touch of morning rain; otherwise, clouds giving way to some sun"),
 (20,86,77,55,0.5,"A touch of rain in the morning; otherwise, clouds yielding to sun"),
 (21,88,78,40,0.5,"A shower in spots in the morning; otherwise, partly sunny and humid"),
 (22,87,77,55,1,"Mostly cloudy with a touch of rain in the afternoon"),
 (23,86,73,1,None,"Partly sunny and less humid"),
 (24,82,70,1,None,"Mostly sunny"),
 (25,87,75,10,None,"Mostly sunny"),
 (26,86,78,65,2,"A couple of morning showers and a thunderstorm; otherwise, cloudy"),
 (27,85,77,56,1,"A morning thunderstorm; otherwise, intervals of clouds and sunshine"),
],
"הוי-אן": [
 (13,86,78,97,3,"Cloudy with drenching rain in the afternoon"),
 (14,88,78,75,1.5,"Cloudy with occasional rain in the afternoon"),
 (15,89,78,90,3,"Remaining cloudy with periods of rain in the afternoon"),
 (16,89,78,89,1.5,"Mostly cloudy with a couple of showers in the afternoon"),
 (17,90,77,69,2,"Considerable clouds with a little rain in the afternoon"),
 (18,89,78,65,2,"Some sun, then increasing clouds with a little rain in the afternoon"),
 (19,88,78,60,3,"Mainly cloudy with a little rain"),
 (20,87,77,65,3.5,"Solid cloud cover with a little rain"),
 (21,92,77,60,3.5,"Periods of rain"),
 (22,91,77,55,1,"Mostly cloudy with a little rain in the afternoon"),
 (23,92,77,55,2,"Mostly cloudy with a little rain"),
 (24,93,78,60,3,"Periods of rain"),
 (25,89,71,20,None,"Times of sun and clouds"),
 (26,86,75,55,1,"Periods of clouds and sunshine with a thundershower in the afternoon"),
 (27,87,74,55,1,"A thundershower in the morning; otherwise, increasing amounts of sun"),
],
"פו-קוק": [
 (13,88,82,59,3,"Mostly cloudy; a morning thunderstorm followed by a little rain in the afternoon"),
 (14,89,82,95,6,"Periods of rain"),
 (15,87,82,58,3,"Overcast with a touch of rain"),
 (16,89,82,80,3,"Periods of rain in the morning; otherwise, cloudy"),
 (17,88,82,98,7,"Cloudy; thunderstorms in the morning followed by periods of rain in the afternoon"),
 (18,90,81,69,8,"Rain at times"),
 (19,84,80,74,4,"Dull and dreary; a couple of morning thunderstorms followed by periods of rain in the afternoon"),
 (20,83,79,85,6,"Rain ending in the morning; considerable cloudiness"),
 (21,85,80,65,2,"A bit of morning rain; otherwise, remaining cloudy"),
 (22,87,79,25,None,"Variable cloudiness"),
 (23,87,79,55,1,"Some sun, then turning cloudy with a shower in the area in the afternoon"),
 (24,86,80,58,2,"Cloudy with a bit of rain"),
 (25,85,82,57,1,"Cloudy; a passing morning shower followed by a thunderstorm in spots in the afternoon"),
 (26,87,81,25,None,"Remaining cloudy"),
 (27,88,82,55,1,"Intervals of clouds and sunshine with a shower in the area"),
],
"נה-טראנג": [
 (13,90,77,57,1,"Cloudy with a little rain in the afternoon"),
 (14,88,76,75,1.5,"Cloudy with a little rain in the afternoon"),
 (15,89,76,85,2.5,"Mostly cloudy; a passing morning shower followed by a couple of thunderstorms in the afternoon"),
 (16,89,77,65,1,"Mostly cloudy with a couple of thunderstorms in the afternoon"),
 (17,88,77,70,2.5,"Cloudy with a little rain in the afternoon"),
 (18,88,74,55,2.5,"Cloudy; a thunderstorm in spots in the morning followed by a little rain in the afternoon"),
 (19,90,75,70,2,"A blanket of clouds with periods of rain in the afternoon"),
 (20,91,76,56,3,"Still cloudy with a little rain"),
 (21,89,77,75,2,"Mostly cloudy with periods of rain in the afternoon"),
 (22,91,77,63,3,"Periods of rain"),
 (23,89,78,62,4,"Periods of rain"),
 (24,87,77,75,6,"Rain"),
 (25,87,74,55,1,"Cloudy with a thundershower in spots"),
 (26,87,74,55,0.5,"Periods of clouds and sunshine with a thundershower in spots in the afternoon"),
 (27,88,75,58,0.5,"A passing shower in the morning; otherwise, intervals of clouds and sunshine"),
],
}

TAIL = json.load(open(f"{REPO}/_tail2830.json", encoding="utf-8"))

def build_days(loc):
    days = []
    for (day,hiF,loF,rain,hours,cond) in RAW[loc]:
        code, typhoon = icon_for(cond)
        days.append({"day":day,"hi_c":c(hiF),"lo_c":c(loF),"rain":rain,"hours":hours,
                     "code":code,"typhoon":typhoon,"cond_he":tr(cond),"tier":"near"})
    for row in TAIL[loc]:
        typh, dstr, code, alt, hi, lo, wrainblk, hattr, hrs, rainpct = row
        d = int(dstr)
        days.append({"day":d,"hi_c":int(hi),"lo_c":int(lo),
                     "rain": int(rainpct) if rainpct else None,
                     "hours": float(hrs) if hrs else None,
                     "code":code,"typhoon":bool(typh),"cond_he":alt,"tier":"far"})
    return days

ALL = {loc: build_days(loc) for loc in LOC_ORDER}

def wrain_span(day):
    if day["rain"] is None: return ""
    if day["hours"] is not None:
        hrs = day["hours"]
        hrs_str = str(int(hrs)) if float(hrs)==int(hrs) else str(hrs)
        return f'<br><span class="wrain" data-hours="{hrs_str}">{day["rain"]}% גשם</span>'
    return f'<br><span class="wrain">{day["rain"]}% גשם</span>'

def card_html(loc):
    days = ALL[loc]
    rows = []
    for day in days:
        typhoon_attr = ' data-typhoon="true"' if day["typhoon"] else ""
        icon = f'<img class="wicon" data-icon="{day["code"]}" alt="{day["cond_he"]}">'
        rows.append(f'<div class="wrow"{typhoon_attr}><div class="wdate">{day["day"]:02d}/09</div>{icon}'
            f'<div class="wtemps"><span class="hi">{day["hi_c"]}°</span><span class="lo">{day["lo_c"]}°</span>{wrain_span(day)}</div></div>')
    return f'<div class="wcard"><div class="wcard-head"><span>⋮⋮</span>{loc}</div><div class="wcard-body">{"".join(rows)}</div></div>'

cards_html = "".join(card_html(loc) for loc in LOC_ORDER)
print("N_CARDS", cards_html.count('class="wcard"'))
print("N_WRAIN", cards_html.count('class="wrain"'))
print("N_ROWS", cards_html.count('class="wrow"'))

BUILD_ISO = "2026-09-13T05:30:00+07:00"
TIME_STR = "13/09/2026, 05:30"

HOURLY_EXTRA = {"clear":"בהיר","mostly clear":"בהיר ברובו"}
def tr_h(cond):
    key = cond.strip().lower()
    if key in HOURLY_EXTRA: return HOURLY_EXTRA[key]
    return tr_hourly(cond)
HOURLY_RAW = {
"האנוי": [(88,30,"Mostly sunny"),(86,20,"Mostly sunny"),(84,20,"Partly cloudy"),(82,15,"Partly cloudy"),(80,10,"Clear"),(79,7,"Clear")],
"נין-בין": [(85,25,"Mostly sunny"),(83,25,"Mostly cloudy"),(81,25,"Mostly cloudy"),(80,25,"Partly cloudy"),(79,20,"Partly cloudy"),(79,20,"Clear")],
"סאפא": [(73,20,"Partly sunny"),(70,25,"Intermittent clouds"),(66,30,"Mostly cloudy"),(63,35,"Cloudy"),(61,40,"Cloudy"),(60,40,"Cloudy")],
"פו-לונג": [(84,25,"Mostly sunny"),(81,25,"Mostly cloudy"),(79,25,"Mostly cloudy"),(77,25,"Cloudy"),(76,25,"Cloudy"),(75,25,"Cloudy")],
"מפרץ הא-לונג": [(83,35,"Mostly cloudy w/ t-storms"),(82,40,"Mostly cloudy w/ t-storms"),(81,35,"Partly sunny w/ t-storms"),(80,30,"Partly sunny"),(79,25,"Partly sunny"),(79,20,"Mostly sunny")],
"הוי-אן": [(85,50,"Thunderstorms"),(83,30,"Mostly cloudy"),(81,25,"Mostly cloudy"),(80,25,"Cloudy"),(79,25,"Cloudy"),(79,25,"Cloudy")],
"פו-קוק": [(87,45,"Cloudy"),(85,50,"Cloudy"),(84,55,"Cloudy"),(83,60,"Rain"),(82,65,"Showers"),(81,70,"Rain")],
"נה-טראנג": [(88,40,"Mostly cloudy"),(85,25,"Cloudy"),(82,20,"Cloudy"),(80,20,"Cloudy"),(79,20,"Cloudy"),(78,20,"Cloudy")],
}
hourly_data = {}
for loc, hours in HOURLY_RAW.items():
    arr = []
    for tf, r, cond in hours:
        code, typ = icon_for(cond)
        arr.append({"t": c(tf), "c": tr_h(cond), "r": r, "i": code})
    hourly_data[loc] = arr

VND_PER_USD_RAW = 26150
ILS_PER_USD_RAW = 3.24
VND_PER_ILS = round(VND_PER_USD_RAW / ILS_PER_USD_RAW)
VND_PER_USD_FMT = f"{VND_PER_USD_RAW:,}"
VND_PER_ILS_FMT = f"{VND_PER_ILS:,}"
ILS_PER_USD_FMT = f"{ILS_PER_USD_RAW:.2f}"

snapshot = {"generatedAt": BUILD_ISO, "data": {}}
for loc in LOC_ORDER:
    for day in ALL[loc]:
        key = f'{loc}|{day["day"]:02d}/09'
        snapshot["data"][key] = {"hi": day["hi_c"], "lo": day["lo_c"], "code": day["code"],
            "rain": day["rain"], "typhoon": day["typhoon"], "tier": day["tier"]}

with open(f"{REPO}/forecast_snapshot.json","r",encoding="utf-8") as f:
    old_snapshot = json.load(f)

RANK = {"su":0,"pa":1,"cl":2,"sh":3,"ts":4}
def classify(old,new):
    if old.get("typhoon") != new.get("typhoon"):
        return ("worse" if new.get("typhoon") else "better"), 100
    dr = RANK.get(new["code"],2) - RANK.get(old["code"],2)
    dhi = new["hi"]-old["hi"]; dlo = new["lo"]-old["lo"]
    dr_rain = (new["rain"] or 0) - (old["rain"] or 0)
    candidate = abs(dr)>=2 or abs(dhi)>=4 or abs(dlo)>=4 or abs(dr_rain)>=25
    if not candidate: return None
    severity = abs(dr)*10+abs(dhi)+abs(dlo)+abs(dr_rain)/10
    worse = dr>0 or dhi>2 or dr_rain>15
    return ("worse" if worse else "better"), severity

changes=[]
old_data = old_snapshot.get("data",{})
for key,new in snapshot["data"].items():
    old = old_data.get(key)
    if not old: continue
    if old.get("tier") != new.get("tier"): continue
    res = classify(old,new)
    if res:
        direction,severity = res
        changes.append((severity,direction,key,old,new))
changes.sort(key=lambda x:-x[0])
top_changes = changes[:3]

prev_gen = old_snapshot.get("generatedAt")
def relative_hebrew(prev_iso, now_iso):
    try:
        p = datetime.datetime.fromisoformat(prev_iso); n = datetime.datetime.fromisoformat(now_iso)
        hours=(n-p).total_seconds()/3600
        if hours<1: return "לפני פחות משעה"
        elif hours<1.5: return "לפני כשעה"
        elif hours<24: return f"לפני כ-{round(hours)} שעות"
        elif hours<48: return "לפני יום"
        else: return f"לפני כ-{round(hours/24)} ימים"
    except Exception: return "לאחרונה"
rel_time = relative_hebrew(prev_gen, BUILD_ISO) if prev_gen else None
print("PREV_GENERATED_AT", prev_gen, "REL_TIME", rel_time, "N_CHANGES", len(top_changes))

INVEST_98W_BANNER = ('<div class="storm-alert storm-alert-change-worse"><span class="storm-alert-icon">🌀</span>'
    '<div class="storm-alert-body"><div class="storm-alert-title"><span class="badge-change-worse">מעקב סערה</span>Invest 98W · מפרץ טונקין / צפון וייטנאם</div>'
    '<div class="storm-alert-desc">מערכת טרופית חלשה (35 קמ"ש, 1006hPa) נצפית ליד מפרץ טונקין, קרובה להאנוי / מפרץ הא-לונג / נין-בין / פו-לונג. לפי JTWC, סיכוי HIGH (גבוה) להתפתחות תוך 24 שעות. עדיין לא הוכרזה כטייפון/סופה טרופית בשם.</div>'
    '<div class="storm-alert-meta">מקור: zoom.earth · נבדק 13/09 כ-05:50 שעון ויאטנם</div></div></div>')

storm_banners = INVEST_98W_BANNER
for severity,direction,key,old,new in top_changes:
    loc,date = key.split("|")
    cls = "storm-alert-change-worse" if direction=="worse" else "storm-alert-change-better"
    badge = "החמרה" if direction=="worse" else "שיפור"
    icon = "📈" if direction=="worse" else "📉"
    badge_cls = "worse" if direction=="worse" else "better"
    desc = f'{loc} ({date}): {old["hi"]}°/{old["lo"]}° → {new["hi"]}°/{new["lo"]}°'
    if new.get("rain") is not None and old.get("rain") is not None:
        desc += f', סיכוי גשם {old["rain"]}%→{new["rain"]}%'
    storm_banners += (f'<div class="storm-alert {cls}"><span class="storm-alert-icon">{icon}</span>'
        f'<div class="storm-alert-body"><div class="storm-alert-title"><span class="badge-change-{badge_cls}">{badge} בתחזית</span>{loc} · {date}</div>'
        f'<div class="storm-alert-desc">{desc}</div>'
        f'<div class="storm-alert-meta">בהשוואה לעדכון הקודם ({rel_time})</div></div></div>')

with open(f"{REPO}/forecast_snapshot.json","w",encoding="utf-8") as f:
    json.dump(snapshot,f,ensure_ascii=False,indent=1)

ZOOM_B64 = open(f"{REPO}/_zoom_b64.txt").read().strip()
ZOOM_SRC = f"data:image/jpeg;base64,{ZOOM_B64}"
ZOOM_NOTE = "צילום מסך חי מ-zoom.earth (לוויין, 13/09 כ-05:50 שעון ויאטנם) - מערכת במעקב: Invest 98W ליד מפרץ טונקין/צפון וייטנאם (סמוך להאנוי/מפרץ הא-לונג/נין-בין/פו-לונג), רוחות כרגע כ-35 קמ\"ש, סיכוי גבוה (HIGH) להתפתחות תוך 24 שעות לפי JTWC - עדיין לא טייפון, אך מומלץ מעקב"

with open(f"{REPO}/accommodations_snapshot.json","r",encoding="utf-8") as f:
    accom = json.load(f)

with open(f"{REPO}/shopping_list.json","r",encoding="utf-8") as f:
    shop = json.load(f)

with open(f"{REPO}/template.html","r",encoding="utf-8") as f:
    tpl = f.read()

replacements = {
    "__CARDS__": cards_html,
    "__STORM_BANNERS__": storm_banners,
    "__ACCOMMODATIONS_DATA__": json.dumps(accom if isinstance(accom,list) else accom.get("bookings",[]), ensure_ascii=False),
    "__ACCOMMODATIONS_UPDATED__": json.dumps(accom.get("updatedAt","") if isinstance(accom,dict) else ""),
    "__HOURLY_DATA__": json.dumps(hourly_data, ensure_ascii=False),
    "__HOURLY_TODAY_LOC__": "null",
    "__HOURLY_TODAY_OUTLOOK__": '""',
    "__ZOOM_EARTH_IMG_SRC__": ZOOM_SRC,
    "__ZOOM_EARTH_IMG_NOTE__": ZOOM_NOTE,
    "__SHOP_ITEMS__": json.dumps(shop.get("items", []), ensure_ascii=False),
    "__SHOP_UPDATED__": json.dumps(shop.get("lastCheckedUtc", "")),
    "__TRAIN_UPDATED__": "11/09/2026",
    "__TRAIN_WEEKDAY_TIMES__": "08:30 · 09:30 · 11:50<br>15:15 · 19:50 · 21:15<br>21:30 · 22:00",
    "__TRAIN_WEEKEND_TIMES__": "06:00 · 09:00 · 09:30<br>11:20 · 15:20 · 17:30<br>18:00 · 18:30 · 19:00<br>19:45 · 20:30 · 21:00",
    "__VND_PER_USD__": VND_PER_USD_FMT,
    "__VND_PER_ILS__": VND_PER_ILS_FMT,
    "__ILS_PER_USD__": ILS_PER_USD_FMT,
    "__VND_PER_USD_RAW__": str(VND_PER_USD_RAW),
    "__ILS_PER_USD_RAW__": str(ILS_PER_USD_RAW),
    "__BUILD_DATE_ISO__": BUILD_ISO,
    "__TIME__": TIME_STR,
}
out = tpl
for k,v in replacements.items():
    out = out.replace(k, v)

ICONS_SCRIPT = """<script>
(function(){
const ICONS = {
ts: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+CjxwYXRoIGQ9Ik0xNSAzOGMtNi42IDAtMTItNS40LTEyLTEyIDAtNS45IDQuMy0xMC44IDEwLTExLjhDMTQgNyAyMC42IDEgMjguNSAxYzguOCAwIDE2LjEgNi41IDE3LjIgMTUuMUM1Mi4xIDE3IDU3IDIyLjUgNTcgMjljMCA3LjItNS45IDEzLTEzLjEgMTNIMTV6IiBmaWxsPSIjNjM2NmYxIi8+Cjxwb2x5Z29uIHBvaW50cz0iMzQsNDIgMjQsNTggMzEsNTggMjcsNjMgNDEsNDYgMzMsNDYiIGZpbGw9IiNmYmJmMjQiLz4KPC9zdmc+",
sh: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+CjxwYXRoIGQ9Ik0xNSA0MGMtNi42IDAtMTItNS40LTEyLTEyIDAtNS45IDQuMy0xMC44IDEwLTExLjhDMTQgOSAyMC42IDMgMjguNSAzYzguOCAwIDE2LjEgNi41IDE3LjIgMTUuMUM1Mi4xIDE5IDU3IDI0LjUgNTcgMzFjMCA3LjItNS45IDEzLTEzLjEgMTNIMTV6IiBmaWxsPSIjOTRhM2I4Ii8+CjxnIHN0cm9rZT0iIzM4YmRmOCIgc3Ryb2tlLXdpZHRoPSIzLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCI+CjxsaW5lIHgxPSIyMCIgeTE9IjQ4IiB4Mj0iMTYiIHkyPSI1OCIvPgo8bGluZSB4MT0iMzIiIHkxPSI0OCIgeDI9IjI4IiB5Mj0iNTgiLz4KPGxpbmUgeDE9IjQ0IiB5MT0iNDgiIHgyPSI0MCIgeTI9IjU4Ii8+CjwvZz4KPC9zdmc+",
cl: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+CjxwYXRoIGQ9Ik0xNiA0OGMtNyAwLTEzLTUuNy0xMy0xMi43IDAtNi4zIDQuNy0xMS41IDEwLjgtMTIuNUMxNS40IDE0LjIgMjIuNSA4IDMxIDhjOS40IDAgMTcuMiA3IDE4LjQgMTYuMUM1Ni40IDI1IDYyIDMwLjkgNjIgMzhjMCA3LjctNi4zIDE0LTE0IDE0SDE2eiIgZmlsbD0iIzk0YTNiOCIvPgo8L3N2Zz4=",
su: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+CjxjaXJjbGUgY3g9IjMyIiBjeT0iMzIiIHI9IjE0IiBmaWxsPSIjZmJiZjI0Ii8+CjxnIHN0cm9rZT0iI2ZiYmYyNCIgc3Ryb2tlLXdpZHRoPSI0IiBzdHJva2UtbGluZWNhcD0icm91bmQiPgo8bGluZSB4MT0iMzIiIHkxPSI0IiB4Mj0iMzIiIHkyPSIxMiIvPgo8bGluZSB4MT0iMzIiIHkxPSI1MiIgeDI9IjMyIiB5Mj0iNjAiLz4KPGxpbmUgeDE9IjQiIHkxPSIzMiIgeDI9IjEyIiB5Mj0iMzIiLz4KPGxpbmUgeDE9IjUyIiB5MT0iMzIiIHgyPSI2MCIgeTI9IjMyIi8+CjxsaW5lIHgxPSIxMiIgeTE9IjEyIiB4Mj0iMTgiIHkyPSIxOCIvPgo8bGluZSB4MT0iNDYiIHkxPSI0NiIgeDI9IjUyIiB5Mj0iNTIiLz4KPGxpbmUgeDE9IjEyIiB5MT0iNTIiIHgyPSIxOCIgeTI9IjQ2Ii8+CjxsaW5lIHgxPSI0NiIgeTE9IjE4IiB4Mj0iNTIiIHkyPSIxMiIvPgo8L2c+Cjwvc3ZnPg==",
pa: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NCA2NCI+CjxjaXJjbGUgY3g9IjM4IiBjeT0iMjAiIHI9IjExIiBmaWxsPSIjZmJiZjI0Ii8+CjxnIHN0cm9rZT0iI2ZiYmYyNCIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiPgo8bGluZSB4MT0iMzgiIHkxPSIyIiB4Mj0iMzgiIHkyPSI3Ii8+CjxsaW5lIHgxPSI1NiIgeTE9IjIwIiB4Mj0iNjEiIHkyPSIyMCIvPgo8bGluZSB4MT0iNTEiIHkxPSI3IiB4Mj0iNTQiIHkyPSI0Ii8+CjwvZz4KPHBhdGggZD0iTTE0IDQ2Yy02IDAtMTEtNS0xMS0xMSAwLTUuNSA0LTEwIDkuMy0xMC45QzE0IDE4LjcgMjAgMTQgMjcgMTRjOCAwIDE0LjUgNiAxNS42IDEzLjYgNS45LjcgMTAuNCA1LjcgMTAuNCAxMS43IDAgNi41LTUuMyAxMS43LTExLjggMTEuN0gxNHoiIGZpbGw9IiM5NGEzYjgiLz4KPC9zdmc+"
};
document.querySelectorAll('.wicon[data-icon]').forEach(function(img){
  var code = img.getAttribute('data-icon');
  img.src = ICONS[code] || ICONS.pa;
});
})();
</script>
"""
marker = '<script>\nconst defaultItinerary'
assert marker in out, "itinerary script marker not found"
out = out.replace(marker, ICONS_SCRIPT + marker, 1)

leftover = re.findall(r"__[A-Z_]+__", out)
print("LEFTOVER_PLACEHOLDERS:", set(leftover))
double_suffix = "(שעון ויאטנם) (שעון ויאטנם)"
print("DOUBLE_SUFFIX_FOUND:", double_suffix in out)
open_divs = len(re.findall(r"<div", out))
close_divs = len(re.findall(r"</div>", out))
print("DIV_OPEN", open_divs, "DIV_CLOSE", close_divs, "BALANCED", open_divs==close_divs)
icons_count = out.count("const ICONS = {")
print("ICONS_SCRIPT_COUNT", icons_count)

with open(f"{REPO}/index.html","w",encoding="utf-8") as f:
    f.write(out)
print("WROTE", len(out), "bytes")
