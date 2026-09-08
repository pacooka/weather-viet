import re

data = {
 "האנוי": {
   "13/09": (14, None), "14/09": (55,1), "15/09": (55,1), "16/09": (25,None),
   "17/09": (16,None), "18/09": (75,4.5), "19/09": (71,4), "20/09": (65,2),
   "21/09": (70,4), "22/09": (65,4),
 },
 "פו-לונג": {
   "13/09": (55,1), "14/09": (7,None), "15/09": (3,None), "16/09": (55,2),
   "17/09": (20,None), "18/09": (25,None),
 },
 "נין-בין": {
   "13/09": (22,None), "14/09": (55,2), "15/09": (62,1), "16/09": (58,2),
   "17/09": (25,None), "18/09": (76,8.5), "19/09": (62,5), "20/09": (65,2),
   "21/09": (65,5), "22/09": (65,5.5),
 },
 "סאפא": {
   "13/09": (3,None), "14/09": (9,None), "15/09": (60,1.5), "16/09": (68,3.5),
   "17/09": (74,2.5), "18/09": (60,2), "19/09": (61,2), "20/09": (66,2),
   "21/09": (59,3.5), "22/09": (70,6),
 },
 "מפרץ הא-לונג": {
   "13/09": (25,None), "14/09": (4,None), "15/09": (3,None), "16/09": (49,1),
   "17/09": (20,None), "18/09": (20,None), "19/09": (55,1),
 },
 "הוי-אן": {
   "13/09": (76,12), "14/09": (70,6), "15/09": (65,1.5), "16/09": (55,1),
   "17/09": (78,7), "18/09": (75,2), "19/09": (59,1), "20/09": (25,None),
   "21/09": (25,None), "22/09": (56,1),
 },
 "פו-קוק": {
   "13/09": (67,4), "14/09": (71,6), "15/09": (76,10.5), "16/09": (64,3.5),
   "17/09": (75,7.5), "18/09": (75,8), "19/09": (65,2), "20/09": (64,3),
 },
 "נה-טראנג": {
   "13/09": (58,1), "14/09": (61,1), "15/09": (55,2), "16/09": (65,2),
   "17/09": (62,3.5), "18/09": (55,2), "19/09": (60,3), "20/09": (67,4),
   "21/09": (55,0.5), "22/09": (61,1),
 },
}

path = "/sessions/funny-intelligent-cannon/mnt/scratch/index.html"
h = open(path, encoding="utf-8").read()

div_open_before = h.count("<div")
div_close_before = h.count("</div>")
wrow_before = h.count('<div class="wrow">')
wcard_before = len(re.findall(r'class="wcard"', h))

parts = re.split(r'(wcard-head"><span>⋮⋮</span>)([^<]+)(</div>)', h)
# parts: [pre, marker1, name1, marker3, body1, marker1, name2, marker3, body2, ...]
added = 0
for idx in range(2, len(parts), 4):
    name = parts[idx]
    body_idx = idx + 2
    loc_data = data.get(name.strip())
    if not loc_data:
        continue
    body = parts[body_idx]
    pattern = re.compile(r'(<div class="wdate">(\d\d/\d\d)</div>.*?<span class="lo">\d+°</span>)')
    def repl(m):
        global added
        full, date = m.group(1), m.group(2)
        if date in loc_data:
            pct, hours = loc_data[date]
            hours_attr = f' data-hours="{hours}"' if hours is not None else ''
            added += 1
            return full + f'<br><span class="wrain"{hours_attr}>{pct}% גשם</span>'
        return full
    parts[body_idx] = pattern.sub(repl, body)

h2 = ''.join(parts)

div_open_after = h2.count("<div")
div_close_after = h2.count("</div>")
wrow_after = h2.count('<div class="wrow">')
wcard_after = len(re.findall(r'class="wcard"', h2))
wrain_after = h2.count('class="wrain"')

print("added:", added)
print("div_open before/after:", div_open_before, div_open_after)
print("div_close before/after:", div_close_before, div_close_after)
print("wrow before/after:", wrow_before, wrow_after)
print("wcard before/after:", wcard_before, wcard_after)
print("wrain_after:", wrain_after)

ok = (div_open_before == div_open_after and div_close_before == div_close_after
      and wrow_before == wrow_after and div_open_after == div_close_after
      and wcard_before == wcard_after == 8)
if ok:
    open(path, "w", encoding="utf-8").write(h2)
    print("SAVED")
else:
    print("SAFETY CHECK FAILED - NOT SAVED")
