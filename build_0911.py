# -*- coding: utf-8 -*-
import json, re, sys, os
sys.path.insert(0, "/sessions/affectionate-keen-brown/mnt/WeatherViet")
from build_data2 import c, tr_hourly, icon_for, COND_MAP
from build_main3 import COND_MAP as COND_MAP2
COND_MAP.update(COND_MAP2)

MORE = {
"breezy; a p.m. shower or two": "רוחות; ממטר אחר הצהריים או שניים",
"breezy, p.m. rain, some heavy": "רוחות, גשם אחר הצהריים, לעיתים כבד",
"showers around in the p.m.": "ממטרים באזור אחר הצהריים",
"hot; a little morning rain": "חם; מעט גשם בבוקר",
"hot with occasional rain": "חם עם גשם מדי פעם",
"hot; a bit of morning rain": "חם; מעט גשם בבוקר",
"abundant sunshine": "הרבה שמש בהיר",
"an afternoon thundershower": "ממטר סופה אחר הצהריים",
"some brightening": "התבהרות חלקית",
"occasional morning rain": "גשם מדי פעם בבוקר",
"a shower in the morning": "ממטר בבוקר",
"a little a.m. rain; overcast": "מעט גשם בבוקר; שמיים מכוסים",
"thickening clouds": "עננות מתעבה",
"downpours in the a.m.; cloudy": "ממטרים עזים בבוקר; מעונן",
"a morning thunderstorm or two": "סופת רעמים אחת או שתיים בבוקר",
"increasing cloudiness": "עננות גוברת",
"clouds and sun": "עננים ושמש",
"rain; breezy in the afternoon": "גשם; רוחות אחר הצהריים",
"overcast with a touch of rain": "שמיים מעוננים עם קורטוב גשם",
"a.m. rain; otherwise, cloudy": "גשם בבוקר; אחרת מעונן",
"still cloudy; a couple of morning thunderstorms followed by a little rain in the afternoon": "עדיין מעונן; כמה סופות רעמים בבוקר ולאחר מכן מעט גשם אחר הצהריים",
"turning cloudy": "מתכסה בעננים",
"a touch of morning rain; otherwise, clouds giving way to some sun": "קורטוב גשם בבוקר; אחר כך מתבהר בהדרגה",
"rather cloudy with a touch of rain": "מעונן למדי עם קורטוב גשם",
"a couple of morning thunderstorms; otherwise, intervals of clouds and sunshine": "כמה סופות רעמים בבוקר; אחרת לסירוגין עננים ושמש",
"heavy showers in the morning; remaining cloudy": "ממטרים כבדים בבוקר; ממשיך מעונן",
"cloudy and a steady breeze; periods of rain in the afternoon": "מעונן ורוחות קבועות; גשם לסירוגין אחר הצהריים",
"some sun, then turning cloudy with a couple of showers in the afternoon": "מעט שמש, ואז מתכסה בעננים עם ממטרים אחר הצהריים",
"a thunderstorm on the prowl in the morning; otherwise, mostly cloudy": "סופת רעמים משוטטת בבוקר; אחרת מעונן ברובו",
"mostly cloudy and hot; a thunderstorm in parts of the area in the morning followed by a little rain in the afternoon": "מעונן ברובו וחם; סופת רעמים באזור בבוקר ולאחר מכן מעט גשם אחר הצהריים",
"mostly cloudy and hot with occasional rain": "מעונן ברובו וחם עם גשם מדי פעם",
"mainly cloudy with occasional rain": "מעונן בעיקר עם גשם מדי פעם",
"occasional rain in the morning; otherwise, hot with clouds yielding to sun": "גשם מדי פעם בבוקר; אחרת חם עם עננים מתפזרים לטובת שמש",
"occasional morning rain; otherwise, hot with clouds giving way to sun": "גשם מדי פעם בבוקר; אחרת חם עם התבהרות הדרגתית",
"mostly cloudy with occasional rain; hot and humid": "מעונן ברובו עם גשם מדי פעם; חם ולח",
"breezy at times in the morning; otherwise, cloudy with occasional rain in the afternoon": "רוחות לעיתים בבוקר; אחרת מעונן עם גשם מדי פעם אחר הצהריים",
"cloudy and windy; rain most of the time in the afternoon": "מעונן ורוחות; גשם רוב הזמן אחר הצהריים",
"rather cloudy with a little rain in the afternoon": "מעונן למדי עם מעט גשם אחר הצהריים",
"mainly cloudy with a little rain": "מעונן בעיקר עם מעט גשם",
"hot with rain": "חם עם גשם",
"a brief morning shower or two; otherwise, partly sunny": "ממטר קצר או שניים בבוקר; אחרת שמש חלקית",
"variable clouds with a couple of showers": "עננות משתנה עם כמה ממטרים",
"a couple of morning t-storms": "כמה סופות רעמים בבוקר",
"cloudy; a thunderstorm in the morning followed by a thundershower in the afternoon": "מעונן; סופת רעמים בבוקר ולאחר מכן ממטר סופה אחר הצהריים",
"still cloudy": "עדיין מעונן",
"a drenching thunderstorm in the morning, becoming breezy in the afternoon with a little rain": "סופת רעמים חזקה בבוקר, ורוחות עם מעט גשם אחר הצהריים",
"periods of rain in the morning; otherwise, cloudy": "גשם לסירוגין בבוקר; אחרת מעונן",
"cloudy; thunderstorms in the morning followed by periods of rain in the afternoon": "מעונן; סופות רעמים בבוקר ולאחר מכן גשם לסירוגין אחר הצהריים",
"a couple of showers in the morning; otherwise, remaining cloudy": "כמה ממטרים בבוקר; אחרת ממשיך מעונן",
"considerable cloudiness with a little rain": "עננות ניכרת עם מעט גשם",
"mostly cloudy; a thunderstorm in parts of the area in the morning followed by a little rain in the afternoon": "מעונן ברובו; סופת רעמים באזור בבוקר ולאחר מכן מעט גשם אחר הצהריים",
"remaining cloudy with a little rain": "ממשיך מעונן עם מעט גשם",
"cloudy; a passing shower in the morning followed by a passing thunderstorm in the afternoon": "מעונן; ממטר חולף בבוקר ולאחר מכן סופת רעמים חולפת אחר הצהריים",
"cloudy with a thundershower in spots": "מעונן עם ממטר סופה במקומות",
"cloudy; a passing morning shower followed by a thunderstorm in spots in the afternoon": "מעונן; ממטר חולף בבוקר ולאחר מכן סופת רעמים במקומות אחר הצהריים",
"mostly cloudy with a couple of thunderstorms": "מעונן ברובו עם כמה סופות רעמים",
}
COND_MAP.update(MORE)
MORE2 = {'mostly cloudy with a bit of rain in the afternoon': 'מעונן ברובו עם מעט גשם אחר הצהריים', 'occasional rain in the morning; otherwise, cloudy': 'גשם מדי פעם בבוקר; אחרת מעונן', 'cloudy with showers': 'מעונן עם ממטרים', 'cloudy with showers and thunderstorms': 'מעונן עם ממטרים וסופות רעמים', 'breezy in the morning; otherwise, some sun, then turning cloudy with a stray shower in the afternoon': 'רוחות בבוקר; אחרת מעט שמש, ואז מתכסה בעננים עם ממטר בודד אחר הצהריים', 'cloudy with a couple of showers in the afternoon': 'מעונן עם כמה ממטרים אחר הצהריים', 'rather cloudy with a little rain': 'מעונן למדי עם מעט גשם', 'cloudy with periods of rain in the afternoon': 'מעונן עם גשם לסירוגין אחר הצהריים', 'mostly cloudy with a touch of rain': 'מעונן ברובו עם קורטוב גשם', 'cloudy with a couple of showers': 'מעונן עם כמה ממטרים', 'sunshine and some clouds': 'שמש ומעט עננים', 'periods of rain; breezy in the afternoon': 'גשם לסירוגין; רוחות אחר הצהריים'}
COND_MAP.update(MORE2)


def tr(cond):
    key = cond.strip().lower()
    return COND_MAP.get(key, cond)

LOC_ORDER = ["האנוי","פו-לונג","נין-בין","סאפא","מפרץ הא-לונג","הוי-אן","פו-קוק","נה-טראנג"]

MONTHLY = {
"האנוי": {13:(89,76,"Times of clouds and sun"),14:(86,75,"A little afternoon rain"),15:(88,74,"A bit of rain in the morning"),
16:(88,80,"Downpours in the afternoon"),17:(84,78,"A morning t-storm; cloudy"),18:(89,75,"A bit of afternoon rain"),
19:(90,76,"Mostly sunny"),20:(92,78,"An afternoon shower in spots"),21:(91,77,"Rain most of the time"),
22:(84,78,"Cloudy, a shower and t-storm"),23:(89,74,"Plenty of sunshine"),24:(88,75,"Mostly sunny"),
25:(89,74,"Plenty of sunshine"),26:(89,75,"Mostly sunny"),27:(88,78,"A couple of morning showers"),
28:(87,78,"A stray afternoon t-shower"),29:(88,77,"Intervals of bright sunshine"),30:(88,76,"Shifting clouds and sun")},
"נין-בין": {13:(84,73,"Breezy; a p.m. shower or two"),14:(82,75,"Breezy, p.m. rain, some heavy"),
15:(85,75,"Occasional afternoon rain"),16:(86,76,"Showers around in the p.m."),17:(87,77,"Periods of rain"),
18:(87,76,"Rather cloudy, a little rain"),19:(86,77,"Occasional rain"),20:(90,77,"A couple of morning t-storms"),
21:(91,78,"Hot; a little morning rain"),22:(91,77,"Hot with occasional rain"),23:(92,78,"Hot; a bit of morning rain"),
24:(87,76,"Mostly sunny"),25:(88,76,"Sunshine"),26:(87,76,"Abundant sunshine"),27:(87,78,"A stray afternoon t-shower"),
28:(86,78,"An afternoon thundershower"),29:(86,78,"Sunshine and a few clouds"),30:(87,77,"A stray afternoon t-shower")},
"סאפא": {13:(75,60,"Sunshine and pleasant"),14:(71,60,"Partly sunny and pleasant"),15:(68,58,"A couple of afternoon showers"),
16:(75,60,"A shower and thunderstorm"),17:(71,63,"Couple of thunderstorms"),18:(72,60,"A thundershower in spots"),
19:(73,59,"A brief afternoon shower"),20:(74,60,"Mostly sunny"),21:(75,61,"Times of clouds and sun"),
22:(72,60,"Cloudy and humid with showers"),23:(73,57,"Mostly sunny"),24:(72,58,"Partly sunny"),25:(73,59,"Partly sunny"),
26:(73,60,"A bit of rain in the morning"),27:(72,61,"A little afternoon rain"),28:(72,61,"Morning rain; cloudy, humid"),
29:(71,60,"Humid; rain in the morning"),30:(72,61,"Cloudy, a little rain; humid")},
"פו-לונג": {13:(88,74,"Partly sunny"),14:(81,73,"Some brightening"),15:(83,73,"Occasional morning rain"),
16:(82,78,"Cloudy with showers"),17:(80,77,"Rain"),18:(84,73,"Rain at times"),19:(89,75,"Mostly cloudy, a little rain"),
20:(91,76,"Shifting clouds and sun"),21:(89,75,"Rain"),22:(84,77,"Cloudy, a shower and t-storm"),
23:(88,72,"Plenty of sunshine"),24:(87,73,"Mostly sunny"),25:(88,72,"Sunny"),26:(87,73,"Mostly sunny"),
27:(87,76,"A shower in the morning"),28:(86,76,"Couple of thunderstorms"),29:(86,75,"A little morning rain; cloudy"),
30:(85,76,"A little a.m. rain; overcast")},
"מפרץ הא-לונג": {13:(88,76,"Thickening clouds"),14:(82,76,"Occasional afternoon rain"),15:(85,75,"A little afternoon rain"),
16:(81,78,"Downpours in the a.m.; cloudy"),17:(82,77,"A morning thunderstorm or two"),18:(85,76,"Mostly cloudy, a little rain"),
19:(86,76,"Mostly sunny"),20:(86,76,"A little afternoon rain"),21:(84,77,"Windy with periods of rain"),
22:(83,78,"A shower and thunderstorm"),23:(88,74,"Plenty of sunshine"),24:(87,74,"Increasing cloudiness"),
25:(87,75,"Mostly sunny"),26:(86,76,"Mostly sunny"),27:(86,78,"Clouds and sun"),28:(85,78,"More sunshine than clouds"),
29:(87,77,"Partial sunshine"),30:(87,77,"Clouds and sun")},
"הוי-אן": {13:(87,77,"Rain"),14:(88,78,"Occasional afternoon rain"),15:(88,78,"Occasional afternoon rain"),
16:(90,77,"A few afternoon showers"),17:(90,77,"A bit of afternoon rain"),18:(91,77,"A little afternoon rain"),
19:(90,76,"Mainly cloudy, a little rain"),20:(93,78,"Rain most of the time"),21:(91,77,"Periods of rain"),
22:(91,77,"Periods of rain"),23:(92,78,"Rather cloudy, a little rain"),24:(88,72,"Mostly cloudy"),
25:(89,71,"Times of sun and clouds"),26:(88,71,"Times of clouds and sun"),27:(88,73,"Turning cloudy"),
28:(89,74,"Mostly cloudy"),29:(88,74,"A passing morning shower"),30:(87,72,"Sunshine and some clouds")},
"פו-קוק": {13:(87,80,"A heavy t-storm in the a.m."),14:(89,81,"Rain; breezy in the afternoon"),
15:(87,80,"Overcast with a touch of rain"),16:(90,81,"A.M. rain; otherwise, cloudy"),17:(86,79,"Morning t-storms, then rain"),
18:(85,80,"Rain at times"),19:(84,79,"A couple of morning t-storms"),20:(85,80,"Rain most of the time"),
21:(85,79,"Rain"),22:(84,80,"Rain"),23:(85,81,"A morning thunderstorm"),24:(86,80,"A.M. rain; otherwise, cloudy"),
25:(85,82,"A t-storm around in the p.m."),26:(85,82,"A shower and thunderstorm"),27:(87,81,"Showers around in the p.m."),
28:(86,82,"A shower and thunderstorm"),29:(86,81,"A shower and thunderstorm"),30:(85,82,"Cloudy, a t-shower in spots")},
"נה-טראנג": {13:(88,77,"A little afternoon rain"),14:(90,75,"A bit of afternoon rain"),15:(90,74,"Rather cloudy, a little rain"),
16:(95,77,"A little afternoon rain"),17:(94,76,"Mostly cloudy, afternoon rain"),18:(92,76,"A couple of morning t-storms"),
19:(93,77,"Cloudy with a little rain"),20:(92,78,"Cloudy with a little rain"),21:(93,77,"A few morning showers"),
22:(89,74,"A couple of morning showers"),23:(88,74,"A couple of thunderstorms"),24:(87,75,"A brief t-storm in the p.m."),
25:(87,74,"Cloudy with a stray t-shower"),26:(88,74,"Cloudy with a stray t-shower"),27:(88,75,"A shower and thunderstorm"),
28:(87,73,"Showers around in the morning"),29:(87,74,"A sun-and-cloud mix"),30:(88,73,"A passing morning shower")},
}

NEAR = {
"האנוי": {13:(90,77,"Times of clouds and sun",25,None),14:(84,74,"Mostly cloudy with a bit of rain in the afternoon",55,0.5),
15:(85,75,"Occasional rain in the morning; otherwise, cloudy",90,3.5),16:(87,76,"Cloudy with showers",75,6),
17:(87,77,"A thunderstorm on the prowl in the morning; otherwise, mostly cloudy",55,0.5),
18:(94,78,"Mostly cloudy and hot; a thunderstorm in parts of the area in the morning followed by a little rain in the afternoon",62,2),
19:(98,78,"Mostly cloudy and hot with occasional rain",55,2),20:(91,77,"Mainly cloudy with occasional rain",61,3.5),
21:(93,76,"Occasional rain in the morning; otherwise, hot with clouds yielding to sun",63,3),
22:(94,76,"Occasional morning rain; otherwise, hot with clouds giving way to sun",63,4),
23:(93,77,"Mostly cloudy with occasional rain; hot and humid",5,None),24:(88,75,"Mostly sunny",20,None),25:(89,74,"Plenty of sunshine",5,None)},
"נין-בין": {13:(86,74,"Breezy in the morning; otherwise, some sun, then turning cloudy with a stray shower in the afternoon",55,0.5),
14:(84,74,"Cloudy and windy; rain most of the time in the afternoon",90,3),
15:(84,74,"Breezy at times in the morning; otherwise, cloudy with occasional rain in the afternoon",75,2),
16:(86,76,"Cloudy with a couple of showers in the afternoon",75,1.5),17:(85,77,"Periods of rain",60,4),18:(86,78,"Rain at times",60,3),
19:(87,77,"Mainly cloudy with a little rain",58,2),20:(90,76,"Rather cloudy with a little rain",57,2),
21:(89,77,"Periods of rain",62,4),22:(90,78,"Hot with rain",76,8),23:(88,75,"Plenty of sunshine",5,None),
24:(87,76,"Mostly sunny",20,None),25:(88,76,"Sunshine",5,None)},
"סאפא": {13:(75,60,"Partly sunny and pleasant",3,None),14:(68,58,"Mostly sunny",9,None),
15:(75,60,"Times of sun and clouds with a couple of showers, mainly later",60,1.5),
16:(74,59,"Mostly cloudy with showers and thunderstorms",68,3.5),
17:(74,60,"Mostly cloudy with a couple of showers and a thunderstorm, mainly later",74,2.5),
18:(71,61,"Mostly cloudy with a couple of showers and a thunderstorm",60,2),
19:(71,61,"Mainly cloudy; a couple of thundershowers in the morning followed by a thundershower in spots in the afternoon",61,2),
20:(74,62,"Sunshine interrupted by clouds at times with a couple of showers and a thunderstorm, mainly early in the day",66,2),
21:(73,60,"Humid with periods of rain",59,3.5),22:(72,60,"Cloudy and humid with showers",70,6)},
"פו-לונג": {13:(89,75,"Times of clouds and sun",8,None),14:(85,73,"Mostly cloudy with a little rain in the afternoon",56,1),
15:(86,74,"A little morning rain; otherwise, mostly cloudy",65,1.5),16:(88,75,"Variable clouds with a couple of showers",55,2),
17:(88,73,"Mostly cloudy with a little rain",56,2),18:(88,75,"Rain at times",64,3.5),19:(87,74,"Occasional rain",60,2.5),
20:(88,75,"Partly sunny",13,None),21:(85,76,"Cloudy with a couple of showers and a thunderstorm",65,5),
22:(84,77,"Cloudy with a couple of showers and a thunderstorm",65,4),23:(83,76,"Cloudy with showers and thunderstorms",65,4)},
"מפרץ הא-לונג": {13:(88,76,"Some sun, then turning cloudy with a couple of showers in the afternoon",60,1),
14:(83,76,"Cloudy and a steady breeze; periods of rain in the afternoon",90,3),15:(86,75,"Cloudy with periods of rain in the afternoon",90,3),
16:(86,76,"Heavy showers in the morning; remaining cloudy",80,3),
17:(84,76,"A couple of morning thunderstorms; otherwise, intervals of clouds and sunshine",66,2),
18:(85,77,"Rather cloudy with a touch of rain",59,3),19:(86,77,"A touch of morning rain; otherwise, clouds giving way to some sun",55,1),
20:(85,78,"Rain most of the time",60,3),21:(86,75,"Mostly cloudy with a touch of rain",55,2.5),22:(85,76,"Periods of rain",60,3.5),
23:(88,74,"Plenty of sunshine",5,None),24:(87,74,"Increasing cloudiness",20,None),25:(87,75,"Mostly sunny",10,None)},
"הוי-אן": {13:(86,77,"Rain",94,6.5),14:(89,77,"Mostly cloudy with occasional rain in the afternoon",56,0.5),
15:(89,78,"Cloudy with a little rain in the afternoon",65,2),16:(90,78,"Cloudy with a couple of showers",66,3),
17:(91,77,"Mostly cloudy with a little rain in the afternoon",55,1),18:(91,78,"Considerable cloudiness with a little rain",58,3),
19:(90,78,"Occasional rain",61,3.5),20:(89,77,"Rain",77,11),21:(91,78,"Rain",77,5),
22:(90,75,"A couple of showers in the morning; otherwise, remaining cloudy",56,1),23:(86,71,"Partly sunny",20,None),
24:(88,72,"Mostly cloudy",25,None)},
"פו-קוק": {13:(87,80,"A drenching thunderstorm in the morning, becoming breezy in the afternoon with a little rain",86,4),
14:(89,81,"Periods of rain; breezy in the afternoon",91,3.5),15:(87,80,"Overcast with a touch of rain",57,2),
16:(90,81,"Periods of rain in the morning; otherwise, cloudy",74,2),
17:(86,79,"Cloudy; thunderstorms in the morning followed by periods of rain in the afternoon",64,5),18:(85,80,"Rain at times",61,5.5),
19:(84,79,"Still cloudy; a couple of morning thunderstorms followed by a little rain in the afternoon",68,4),
20:(85,80,"Rain most of the time",69,4),21:(85,79,"Rain",75,4.5),22:(84,80,"Rain",76,9),
23:(85,81,"Cloudy; a thunderstorm in the morning followed by a thundershower in the afternoon",58,2),
24:(86,80,"Occasional rain in the morning; otherwise, cloudy",70,2),
25:(85,82,"Cloudy; a passing morning shower followed by a thunderstorm in spots in the afternoon",57,1)},
"נה-טראנג": {13:(90,77,"Cloudy with a little rain in the afternoon",63,2),14:(93,76,"Cloudy with a little rain in the afternoon",56,0.5),
15:(90,76,"Mostly cloudy with a little rain",55,1.5),16:(89,74,"Mostly cloudy with a little rain in the afternoon",55,1),
17:(94,78,"Mostly cloudy with a little rain in the afternoon",55,1),
18:(91,76,"Mostly cloudy; a thunderstorm in parts of the area in the morning followed by a little rain in the afternoon",65,2.5),
19:(90,76,"Occasional rain",66,5),20:(90,77,"Rain most of the time",62,3.5),21:(92,78,"Periods of rain",61,3.5),
22:(90,76,"Remaining cloudy with a little rain",55,2),23:(88,74,"Mostly cloudy with a couple of thunderstorms",57,2),
24:(87,75,"Cloudy; a passing shower in the morning followed by a passing thunderstorm in the afternoon",55,1),
25:(87,74,"Cloudy with a thundershower in spots",55,1)},
}

TIER_NEAR_DAYS = set(range(11,26))

def build_location_days(loc):
    days = []
    for d in range(13,31):
        tier = "near" if d in TIER_NEAR_DAYS else "far"
        src = "monthly"
        if tier == "near" and loc in NEAR and d in NEAR[loc]:
            hi,lo,cond,rain,hours = NEAR[loc][d]
            src = "near10day"
        else:
            hi,lo,cond = MONTHLY[loc][d]
            rain, hours = None, None
            if tier == "near": src = "monthly-fallback"
        code, typhoon = icon_for(cond)
        heb = tr(cond)
        days.append({"day": d, "hi_f": hi, "lo_f": lo, "hi_c": c(hi), "lo_c": c(lo),
            "cond_en": cond, "cond_he": heb, "code": code, "typhoon": typhoon,
            "rain": rain, "hours": hours, "tier": tier, "src": src})
    return days

ALL = {loc: build_location_days(loc) for loc in LOC_ORDER}

untranslated = []
for loc in LOC_ORDER:
    for d in ALL[loc]:
        if d["cond_he"] == d["cond_en"] and re.search(r"[A-Za-z]", d["cond_he"]):
            untranslated.append((loc, d["day"], d["cond_en"]))
print("UNTRANSLATED:", untranslated)

with open("/tmp/gh_deploy_X/_all_days.json","w",encoding="utf-8") as f:
    json.dump(ALL, f, ensure_ascii=False)
print("OK", sum(len(v) for v in ALL.values()))
