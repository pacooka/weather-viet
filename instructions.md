# Permanent rule: "(שעון ויאטנם)" timestamp suffix — NEVER include it in a filled value

**This bug has recurred 5+ times (confirmed again 2026-09-05 on the 15:30 VN scheduled run).**

`template.html` hardcodes the suffix `(שעון ויאטנם)` directly after every `__TIME__`
placeholder (header line, currency-updated line, and similarly after other
inline timestamps). When filling `__TIME__` (or any other timestamp
placeholder) during a run:

- The value you substitute must be **plain** `DD/MM/YYYY, HH:MM` — for example
  `05/09/2026, 15:30` — with **no** trailing `(שעון ויאטנם)` of your own.
- Do **not** blanket-replace `__TIME__` with a string that already contains
  the suffix. The template supplies the suffix itself; adding it again
  produces a doubled/leftover `(שעון ויאטנם) (שעון ויאטנם)` in the raw HTML.
- Before deploying, grep the built file for the literal substring
  `שעון ויאטנם) (שעון ויאטנם` (doubled) — it must return zero matches.

## Defense added 2026-09-05 (do not remove)

Because this kept recurring despite the rule above, `template.html`'s
client-side time-conversion script (the IIFE right after
`<meta http-equiv="refresh"...>` near the top of `<head>`) now defensively
collapses any accidental doubled/tripled `(שעון ויאטנם)` run into a single
one *before* running its timestamp regex. This makes the **visible page**
immune to this bug even if a future run reintroduces it — visitors will
always see one correctly-converted local time, never a leftover literal
`(שעון ויאטנם)`.

This client-side patch is a safety net, not a license to keep making the
mistake. Still follow the rule above every run: fill `__TIME__` with a bare
`DD/MM/YYYY, HH:MM` value, never with the suffix already appended.

## Separately: how the timestamp is actually displayed to visitors

The header/currency/etc. timestamps are generated using **Vietnam time**
baked into the HTML at build time. A client-side script (same IIFE as above)
converts every one of these on page load into the *visitor's own local
time* (via a fixed Vietnam UTC+7 offset — Vietnam has no DST), so what a
visitor in Israel sees is already their own local time, not Vietnam time,
even though the underlying markup is generated in Vietnam time and still
carries the `(שעון ויאטנם)` label until JS runs. This is intentional
(added 2026-08-28 per Nir) — do not remove this conversion script or revert
to showing raw Vietnam time unconverted.
