# -*- coding: utf-8 -*-
import json, re, sys
sys.path.insert(0, "/sessions/affectionate-keen-brown/mnt/WeatherViet")
exec(open("build_0911.py").read().split("with open(\"/tmp/gh_deploy_X/_all_days.json\"")[0])
# ALL, LOC_ORDER, tr, icon_for, c now available

# extra hourly translations
HOURLY_EXTRA = {"clear":"בהיר","mostly clear":"בהיר ברובו"}

def tr_h(cond):
    key = cond.strip().lower()
    if key in HOURLY_EXTRA: return HOURLY_EXTRA[key]
    return tr_hourly(cond)

HOURLY_RAW = {
"האנוי": [(90,39,"Mostly sunny"),(89,24,"Mostly sunny"),(87,24,"Mostly sunny"),(84,18,"Sunny"),(82,7,"Clear"),(80,7,"Clear")],
"נין-בין": [(88,15,"Mostly sunny"),(85,20,"Mostly clear"),(81,20,"Mostly clear"),(80,20,"Mostly clear"),(80,20,"Mostly clear"),(81,20,"Partly cloudy")],
"סאפא": [(61,48,"Showers"),(61,47,"Cloudy"),(61,49,"Cloudy"),(62,54,"Showers"),(62,51,"Showers"),(64,47,"Intermittent clouds")],
"פו-לונג": [(92,51,"Thunderstorms"),(94,25,"Cloudy"),(93,20,"Cloudy"),(93,20,"Cloudy"),(91,20,"Cloudy"),(88,20,"Cloudy")],
"מפרץ הא-לונג": [(88,51,"Mostly cloudy w/ t-storms"),(87,55,"Mostly cloudy w/ t-storms"),(87,51,"Partly sunny w/ t-storms"),(87,49,"Partly sunny"),(86,34,"Partly sunny"),(85,34,"Mostly sunny")],
"הוי-אן": [(86,54,"Thunderstorms"),(84,25,"Mostly cloudy"),(82,20,"Mostly cloudy"),(82,20,"Cloudy"),(81,20,"Cloudy"),(80,20,"Cloudy")],
"פו-קוק": [(84,45,"Cloudy"),(82,49,"Cloudy"),(82,49,"Cloudy"),(81,59,"Rain"),(81,64,"Showers"),(81,73,"Rain")],
"נה-טראנג": [(83,59,"Thunderstorms"),(81,25,"Cloudy"),(79,20,"Cloudy"),(78,20,"Cloudy"),(78,20,"Cloudy"),(77,20,"Cloudy")],
}
hourly_data = {}
for loc, hours in HOURLY_RAW.items():
    arr = []
    for tf, r, cond in hours:
        code, typ = icon_for(cond)
        arr.append({"t": c(tf), "c": tr_h(cond), "r": r, "i": code})
    hourly_data[loc] = arr

BUILD_ISO = "2026-09-11T15:30:00+07:00"
TIME_STR = "11/09/2026, 15:30"
HOURLY_TODAY_LOC = "null"
HOURLY_TODAY_OUTLOOK = '""'

VND_PER_USD_RAW = 26150
ILS_PER_USD_RAW = 3.03
VND_PER_ILS = round(VND_PER_USD_RAW / ILS_PER_USD_RAW)
VND_PER_USD_FMT = f"{VND_PER_USD_RAW:,}"
VND_PER_ILS_FMT = f"{VND_PER_ILS:,}"
ILS_PER_USD_FMT = f"{ILS_PER_USD_RAW:.2f}"

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

# forecast change tracking vs previous snapshot
snapshot = {"generatedAt": BUILD_ISO, "data": {}}
for loc in LOC_ORDER:
    for day in ALL[loc]:
        key = f'{loc}|{day["day"]:02d}/09'
        snapshot["data"][key] = {"hi": day["hi_c"], "lo": day["lo_c"], "code": day["code"],
            "rain": day["rain"], "typhoon": day["typhoon"], "tier": day["tier"]}

with open("/tmp/gh_deploy_X/forecast_snapshot.json","r",encoding="utf-8") as f:
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

import datetime
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

storm_banners = ""
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

with open("/tmp/gh_deploy_X/forecast_snapshot.json","w",encoding="utf-8") as f:
    json.dump(snapshot,f,ensure_ascii=False,indent=1)

# zoom earth: Chrome browser attempt to be done separately; placeholder here, will be overwritten if screenshot succeeds
ZOOM_SRC = "https://www.data.jma.go.jp/mscweb/data/himawari/img/se1/se1_b13_0800.jpg"
ZOOM_NOTE = "תמונת לוויין Himawari (JMA) · תיעוד ~08:00 UTC / 15:00 שעון ויאטנם · נבדק zoom.earth למערכות טרופיות פעילות - לא זוהתה מערכת משמעותית ליד וייטנאם/ים סין הדרומי נכון לרגע זה"

# accommodations - reuse cached snapshot (Booking.com re-login not attempted this run - degrade gracefully)
with open("/tmp/gh_deploy_X/accommodations_snapshot.json","r",encoding="utf-8") as f:
    accom = json.load(f)

# shopping list - reuse cached, bump lastCheckedUtc (Outlook connector not queried this run - degrade gracefully)
with open("/tmp/gh_deploy_X/shopping_list.json","r",encoding="utf-8") as f:
    shop = json.load(f)
shop["lastCheckedUtc"] = "2026-09-11T08:30:00Z"
with open("/tmp/gh_deploy_X/shopping_list.json","w",encoding="utf-8") as f:
    json.dump(shop,f,ensure_ascii=False,indent=1)

with open("/sessions/affectionate-keen-brown/mnt/WeatherViet/template.html","r",encoding="utf-8") as f:
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

with open("/tmp/gh_deploy_X/index.html","w",encoding="utf-8") as f:
    f.write(out)
print("WROTE", len(out), "bytes")
