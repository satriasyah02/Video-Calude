"""Generate the HyperFrames project for the rendang-cumi unboxing short.

Times are absolute output-timeline seconds (from edit/segmap.json word anchors).
"""
import json, sys, os

PROJ = sys.argv[1]
TOTAL = 83.25

# palette
RED, GOLD, CREAM, INK = "#8B1E0F", "#F2B705", "#FFF4E0", "#2A1208"

# ---------- label specs ----------
# kind: card (title + optional kicker), stamp, chip, pin, count, hook, endcard
SCENES = [
    {"id": "hook", "start": 0.0, "end": 4.0, "items": [
        {"kind": "hook", "id": "hk", "t": 0.0, "end": 3.95,
         "l1": "MAMAKU BIKIN", "l2": "RENDANG", "l3": "CUMI?!", "t2": 0.08, "t3": 1.36},
    ]},
    {"id": "setup", "start": 4.0, "end": 16.85, "items": [
        {"kind": "chip", "id": "kamis", "t": 13.57, "end": 15.10, "text": "Dikirim sejak Kamis lalu", "y": 1060},
        {"kind": "stamp", "id": "basi", "t": 15.22, "end": 16.80, "text": "BASI?", "y": 850},
    ]},
    {"id": "unbox", "start": 16.85, "end": 21.93, "items": [
        {"kind": "chip", "id": "ff", "t": 16.95, "end": 21.80, "text": "UNBOXING  ▶▶ x6", "y": 1060, "dark": True},
    ]},
    {"id": "padang", "start": 21.93, "end": 27.04, "items": [
        {"kind": "pin", "id": "pin", "t": 22.81, "end": 25.70, "text": "PADANG", "y": 870},
        {"kind": "card", "id": "koran", "t": 25.87, "end": 27.00, "kicker": "KORAN", "title": "PADANG EKSPRES", "y": 900, "size": 74},
    ]},
    {"id": "peyek", "start": 31.50, "end": 35.00, "items": [
        {"kind": "card", "id": "peyek", "t": 31.62, "end": 34.95, "kicker": "CEMILAN #1", "title": "PEYEK KACANG", "y": 860},
        {"kind": "chip", "id": "hancur", "t": 33.17, "end": 34.95, "text": "(udah hancur di jalan)", "y": 1070},
    ]},
    {"id": "dakak", "start": 35.90, "end": 41.90, "items": [
        {"kind": "card", "id": "dakak", "t": 36.02, "end": 41.85, "kicker": "CEMILAN #2", "title": "DAKAK-DAKAK", "y": 860},
        {"kind": "count", "id": "cnt", "t": 38.36, "end": 41.85, "steps": [["x3", 38.36], ["x4", 39.06], ["x5", 39.56]], "y": 1075},
    ]},
    {"id": "rendang", "start": 43.90, "end": 56.00, "items": [
        {"kind": "card", "id": "rdg", "t": 44.19, "end": 46.60, "kicker": "YANG SPESIAL", "title": "RENDANG", "y": 870},
        {"kind": "chip", "id": "sapi", "t": 48.84, "end": 51.45, "text": "Daging sapi lagi susah dicari", "y": 1060},
        {"kind": "hook", "id": "rc", "t": 51.68, "end": 55.95,
         "l1": "", "l2": "RENDANG", "l3": "CUMI!", "t2": 51.68, "t3": 52.96, "y": 960},
    ]},
    {"id": "umroh", "start": 67.60, "end": 76.20, "items": [
        {"kind": "card", "id": "umr", "t": 67.75, "end": 69.70, "kicker": "OLEH-OLEH", "title": "UMROH", "y": 870},
        {"kind": "card", "id": "zz", "t": 69.82, "end": 72.20, "kicker": "OLEH-OLEH UMROH", "title": "AIR ZAMZAM", "y": 870},
        {"kind": "card", "id": "krm", "t": 73.45, "end": 74.88, "kicker": "UDAH GEPENG", "title": "KURMA", "y": 870},
        {"kind": "card", "id": "ckl", "t": 74.93, "end": 76.15, "kicker": "DAN", "title": "COKLAT", "y": 870},
    ]},
    {"id": "endcard", "start": 79.70, "end": TOTAL, "items": [
        {"kind": "endcard", "id": "end", "t": 80.25, "end": TOTAL, "big": "PART 2", "sub": "Nyobain Rendang Cumi", "cta": "Follow biar nggak ketinggalan"},
    ]},
]

# ---------- SFX (visual hit time, file, volume) ----------
DUR = {"pop": 0.72, "whoosh": 0.575, "whoosh-short": 0.575, "impact-bass-1": 2.116, "sparkle": 1.802, "click-soft": 0.366}
PEAK = {"pop": 0.12, "whoosh": 0.162, "whoosh-short": 0.162, "impact-bass-1": 0.073,
        "sparkle": 0.027, "click-soft": 0.073}
SFX = [
    (1.36, "impact-bass-1", 0.35),
    (13.57, "pop", 0.9),
    (15.22, "impact-bass-1", 0.25),
    (16.95, "whoosh", 0.55),
    (21.80, "whoosh-short", 0.45),
    (22.81, "pop", 0.9),
    (25.87, "click-soft", 1.0),
    (31.62, "pop", 0.9),
    (36.02, "pop", 0.9),
    (38.36, "click-soft", 1.0),
    (39.06, "click-soft", 1.0),
    (39.56, "click-soft", 1.0),
    (44.19, "pop", 0.9),
    (48.84, "click-soft", 1.0),
    (52.96, "impact-bass-1", 0.35),
    (67.75, "sparkle", 0.35),
    (69.82, "pop", 0.9),
    (73.45, "pop", 0.8),
    (74.93, "pop", 0.8),
    (80.25, "sparkle", 0.4),
]

FPS = 30
IN_D, OUT_D = 0.35, 0.25


def css_common():
    return f"""
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .wrap {{ position: absolute; left: 0; right: 0; display: flex; justify-content: center; }}
    .card {{ display: flex; flex-direction: column; align-items: center; gap: 10px;
             background: {CREAM}; border-radius: 30px; padding: 26px 48px 30px;
             box-shadow: 0 14px 0 {RED}, 0 24px 50px rgba(0,0,0,.35); }}
    .kicker {{ font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 34px; letter-spacing: .08em;
               color: {INK}; background: {GOLD}; padding: 4px 18px; border-radius: 10px; }}
    .title {{ font-family: 'Archivo Black', sans-serif; font-size: 88px; line-height: 1; color: {RED};
              letter-spacing: -.01em; white-space: nowrap; }}
    .chip {{ font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 44px; color: {INK};
             background: {GOLD}; padding: 14px 34px; border-radius: 999px; white-space: nowrap;
             box-shadow: 0 10px 30px rgba(0,0,0,.30); }}
    .chip.dark {{ background: rgba(20,10,6,.82); color: {CREAM}; }}
    .stamp {{ font-family: 'Archivo Black', sans-serif; font-size: 170px; line-height: 1; color: {RED};
              border: 14px solid {RED}; border-radius: 26px; padding: 6px 40px 18px; background: rgba(255,244,224,.88); }}
    .hookbox {{ display: flex; flex-direction: column; align-items: center; gap: 6px; }}
    .h1 {{ font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 56px; color: {CREAM};
           background: {RED}; padding: 6px 26px; border-radius: 12px; letter-spacing: .04em; }}
    .h2 {{ font-family: 'Archivo Black', sans-serif; font-size: 150px; line-height: .95; color: {CREAM};
           -webkit-text-stroke: 10px {INK}; paint-order: stroke fill; }}
    .h3 {{ font-family: 'Archivo Black', sans-serif; font-size: 210px; line-height: .95; color: {GOLD};
           -webkit-text-stroke: 12px {INK}; paint-order: stroke fill; }}
    .pin {{ display: flex; align-items: center; gap: 18px; background: {CREAM}; border-radius: 999px;
            padding: 14px 40px 14px 22px; box-shadow: 0 12px 34px rgba(0,0,0,.32); }}
    .pin svg {{ width: 72px; height: 72px; }}
    .pin span {{ font-family: 'Archivo Black', sans-serif; font-size: 72px; color: {RED}; }}
    .count {{ font-family: 'Archivo Black', sans-serif; font-size: 120px; color: {GOLD};
              -webkit-text-stroke: 9px {INK}; paint-order: stroke fill; position: absolute; }}
    .endbox {{ display: flex; flex-direction: column; align-items: center; gap: 18px; }}
    .big {{ font-family: 'Archivo Black', sans-serif; font-size: 190px; line-height: .9; color: {GOLD};
            -webkit-text-stroke: 12px {INK}; paint-order: stroke fill; }}
    .sub {{ font-family: 'Archivo Black', sans-serif; font-size: 64px; color: {RED}; background: {CREAM};
            padding: 10px 32px; border-radius: 18px; }}
    .cta {{ font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 40px; color: {CREAM};
            background: rgba(20,10,6,.8); padding: 10px 28px; border-radius: 999px; }}
    """


PIN_SVG = (f'<svg viewBox="0 0 24 24"><path fill="{RED}" d="M12 2C7.6 2 4 5.6 4 10c0 5.8 8 12 8 12s8-6.2 8-12c0-4.4-3.6-8-8-8z"/>'
           f'<circle cx="12" cy="10" r="3.2" fill="{CREAM}"/></svg>')


def item_html(it, s0):
    """Return (html, js) for one item; times local to the scene."""
    i, t, end = it["id"], round(it["t"] - s0, 3), round(it["end"] - s0, 3)
    dur = round(end - t, 3)
    y = it.get("y", 1080)
    k = it["kind"]
    js = []
    pop_in = lambda sel, at, rot=-3: js.append(
        f'tl.fromTo("{sel}", {{scale:.4, opacity:0, rotation:{rot-8}}}, {{scale:1, opacity:1, rotation:{rot}, duration:{IN_D}, ease:"back.out(2.2)"}}, {at});')
    pop_out = lambda sel, at: js.append(
        f'tl.to("{sel}", {{scale:.85, opacity:0, duration:{OUT_D}, ease:"power2.in"}}, {at});')
    out_at = round(end - OUT_D - 1 / FPS, 3)

    if k == "card":
        size = it.get("size", 88)
        html = (f'<div id="{i}-w" class="wrap clip" data-start="{t}" data-duration="{dur}" style="top:{y}px">'
                f'<div id="{i}-c" class="card"><span class="kicker">{it["kicker"]}</span>'
                f'<span class="title" style="font-size:{size}px">{it["title"]}</span></div></div>')
        pop_in(f"#{i}-c", t); pop_out(f"#{i}-c", out_at)
    elif k == "chip":
        cls = "chip dark" if it.get("dark") else "chip"
        html = (f'<div id="{i}-w" class="wrap clip" data-start="{t}" data-duration="{dur}" style="top:{y}px">'
                f'<div id="{i}-c" class="{cls}">{it["text"]}</div></div>')
        js.append(f'tl.fromTo("#{i}-c", {{y:40, opacity:0}}, {{y:0, opacity:1, duration:.3, ease:"power3.out"}}, {t});')
        pop_out(f"#{i}-c", out_at)
    elif k == "stamp":
        html = (f'<div id="{i}-w" class="wrap clip" data-start="{t}" data-duration="{dur}" style="top:{y}px">'
                f'<div id="{i}-c" class="stamp">{it["text"]}</div></div>')
        js.append(f'tl.fromTo("#{i}-c", {{scale:2.4, opacity:0, rotation:-4}}, {{scale:1, opacity:1, rotation:-9, duration:.22, ease:"power4.in"}}, {t});')
        js.append(f'tl.fromTo("#{i}-c", {{x:0}}, {{x:10, duration:.05, yoyo:true, repeat:3, ease:"none"}}, {round(t+.22,3)});')
        pop_out(f"#{i}-c", out_at)
    elif k == "pin":
        html = (f'<div id="{i}-w" class="wrap clip" data-start="{t}" data-duration="{dur}" style="top:{y}px">'
                f'<div id="{i}-c" class="pin">{PIN_SVG}<span>{it["text"]}</span></div></div>')
        js.append(f'tl.fromTo("#{i}-c", {{y:-90, opacity:0}}, {{y:0, opacity:1, duration:.45, ease:"bounce.out"}}, {t});')
        pop_out(f"#{i}-c", out_at)
    elif k == "count":
        parts, n = [], len(it["steps"])
        for j, (txt, st) in enumerate(it["steps"]):
            st_l = round(st - s0, 3)
            en_l = round(it["steps"][j + 1][1] - s0, 3) if j + 1 < n else end
            parts.append(f'<div id="{i}-{j}" class="wrap clip" data-start="{st_l}" data-duration="{round(en_l-st_l,3)}" style="top:{y}px">'
                         f'<div id="{i}-{j}c" class="count" style="position:static">{txt}</div></div>')
            js.append(f'tl.fromTo("#{i}-{j}c", {{scale:1.8, opacity:0}}, {{scale:1, opacity:1, duration:.2, ease:"back.out(3)"}}, {st_l});')
            if j + 1 == n:
                pop_out(f"#{i}-{j}c", out_at)
        html = "".join(parts)
    elif k == "hook":
        t2, t3 = round(it["t2"] - s0, 3), round(it["t3"] - s0, 3)
        l1 = f'<div id="{i}-1" class="h1">{it["l1"]}</div>' if it["l1"] else ""
        html = (f'<div id="{i}-w" class="wrap clip" data-start="{t}" data-duration="{dur}" style="top:{y if "y" in it else 860}px">'
                f'<div id="{i}-box" class="hookbox">{l1}<div id="{i}-2" class="h2">{it["l2"]}</div>'
                f'<div id="{i}-3" class="h3">{it["l3"]}</div></div></div>')
        if it["l1"]:
            js.append(f'tl.fromTo("#{i}-1", {{opacity:1, y:0}}, {{opacity:1, y:0, duration:.01}}, 0);')  # on screen at frame 0
        js.append(f'tl.fromTo("#{i}-2", {{opacity:0, y:50}}, {{opacity:1, y:0, duration:.3, ease:"power3.out"}}, {t2});')
        js.append(f'tl.fromTo("#{i}-3", {{opacity:0, scale:2.2, rotation:-6}}, {{opacity:1, scale:1, rotation:-4, duration:.2, ease:"power4.in"}}, {t3});')
        js.append(f'tl.fromTo("#{i}-box", {{x:0}}, {{x:12, duration:.045, yoyo:true, repeat:5, ease:"none"}}, {round(t3+.2,3)});')
        js.append(f'tl.to("#{i}-3", {{scale:1.06, duration:.6, yoyo:true, repeat:1, ease:"sine.inOut"}}, {round(t3+.5,3)});')
        pop_out(f"#{i}-box", out_at)
    elif k == "endcard":
        html = (f'<div id="{i}-w" class="wrap clip" data-start="{t}" data-duration="{dur}" style="top:1000px">'
                f'<div class="endbox"><div id="{i}-b" class="big">{it["big"]}</div>'
                f'<div id="{i}-s" class="sub">{it["sub"]}</div><div id="{i}-c" class="cta">{it["cta"]}</div></div></div>')
        js.append(f'tl.fromTo("#{i}-b", {{scale:.3, opacity:0, rotation:-12}}, {{scale:1, opacity:1, rotation:-4, duration:.4, ease:"back.out(2)"}}, {t});')
        js.append(f'tl.fromTo("#{i}-s", {{y:40, opacity:0}}, {{y:0, opacity:1, duration:.3, ease:"power3.out"}}, {round(t+.25,3)});')
        js.append(f'tl.fromTo("#{i}-c", {{y:30, opacity:0}}, {{y:0, opacity:1, duration:.3, ease:"power3.out"}}, {round(t+.5,3)});')
    else:
        raise ValueError(k)
    return html, js


def scene_file(sc):
    s0 = sc["start"]
    htmls, jss = [], []
    for it in sc["items"]:
        h, j = item_html(it, s0)
        htmls.append(h); jss += j
    W, H = 1080, 1920
    return f"""<template>
  <style>{css_common()}</style>
  <div id="root" data-composition-id="{sc['id']}" data-width="{W}" data-height="{H}">
    {chr(10).join('    ' + h for h in htmls)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join('    ' + j for j in jss)}
    window.__timelines["{sc['id']}"] = tl;
  </script>
</template>
"""


def index_file():
    hosts = []
    for n, sc in enumerate(SCENES):
        d = round(sc["end"] - sc["start"], 3)
        hosts.append(
            f'      <div id="{sc["id"]}" data-composition-id="{sc["id"]}" data-composition-src="compositions/{sc["id"]}.html" '
            f'data-start="{sc["start"]}" data-duration="{d}" data-track-index="2" data-track-kind="graphics" '
            f'data-width="1080" data-height="1920" style="z-index:{10+n}"></div>')
    hosts.append('      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" '
                 f'data-start="0" data-duration="{TOTAL}" data-track-index="1" data-track-kind="captions" '
                 'data-width="1080" data-height="1920" style="z-index:50"></div>')
    sfx = []
    for n, (t, f, vol) in enumerate(SFX):
        st = max(0.0, round(t - PEAK[f] + 1 / FPS, 3))
        sfx.append(f'      <audio id="sfx-{n:02d}" class="clip" src="assets/sfx/{f}.mp3" data-start="{st}" data-duration="{DUR[f]}" '
                   f'data-track-index="{3 + n % 2}" data-volume="{vol}"></audio>')
    return f"""<!doctype html>
<html lang="id" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ width: 100%; height: 100%; position: relative; }}
      #base {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <video id="base" class="clip" src="assets/base.mp4" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-has-audio="true" data-volume="1" playsinline style="z-index:1"></video>
{chr(10).join(hosts)}
{chr(10).join(sfx)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


# ---------- captions (word-level, output timeline) ----------
CAP_Y = 1235
# title cards already say these words on screen: hook, body "RENDANG CUMI!", end card
CAP_SKIP = [(0.0, 3.95), (51.6, 56.0), (79.7, 999)]
FIX = {"ma-mamaku": "mamaku", "express.": "Ekspres."}


def caption_groups(transcript, segmap):
    words = [w for w in json.load(open(transcript))["words"] if w["type"] == "word"]
    out = []
    for sg in segmap:
        if sg["speed"] != 1.0:
            continue
        s0, s1, o0, od = sg["src_start"], sg["src_end"], sg["out_start"], sg["out_dur"]
        for w in words:
            if not (w["start"] >= s0 - 0.01 and w["end"] <= s1 + 0.08):
                continue
            a = o0 + (w["start"] - s0)
            b = min(o0 + od, o0 + (w["end"] - s0))
            if any(lo <= a < hi for lo, hi in CAP_SKIP):
                continue
            out.append({"text": FIX.get(w["text"].lower(), w["text"]), "start": round(a, 3), "end": round(b, 3)})
    groups, cur = [], []
    for j, w in enumerate(out):
        cur.append(w)
        nxt = out[j + 1] if j + 1 < len(out) else None
        gap = (nxt["start"] - w["end"]) if nxt else 99
        orphan_next = (nxt is not None and nxt["text"][-1:] in ".?!" and gap < 0.6 and len(cur) < 5)
        if (len(cur) >= 4 and not orphan_next) or w["text"][-1:] in ".?!" or (w["text"][-1:] == "," and len(cur) >= 2) \
                or gap >= 0.6 or (gap >= 0.15 and len(cur) >= 2 and not orphan_next):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    res = []
    for k, g in enumerate(groups):
        st = max(g[0]["start"] - 0.05, res[-1]["end"] if res else 0.1)
        en = g[-1]["end"] + 0.2
        if k + 1 < len(groups):
            en = min(en, groups[k + 1][0]["start"] - 0.05)
        en = max(en, st + 0.4)
        res.append({"start": round(st, 3), "end": round(en, 3), "words": g})
    for k in range(len(res) - 1):
        if res[k]["end"] > res[k + 1]["start"]:
            res[k]["end"] = res[k + 1]["start"]
    return res


def clean(t):
    return t.rstrip(".,")


def captions_file(groups):
    html, js = [], []
    for k, g in enumerate(groups):
        gid = f"cg{k:03d}"
        txt = " ".join(clean(w["text"]) for w in g["words"])
        size = int(min(68, 880 / max(1, len(txt) * 0.6)))
        spans = "".join(f'<span id="{gid}w{j}" class="cw">{clean(w["text"])}</span>' for j, w in enumerate(g["words"]))
        d = round(g["end"] - g["start"], 3)
        html.append(f'<div id="{gid}" class="capg clip" data-start="{g["start"]}" data-duration="{d}" style="top:{CAP_Y}px">'
                    f'<div id="{gid}i" class="capi" style="font-size:{size}px">{spans}</div></div>')
        js.append(f'tl.fromTo("#{gid}i", {{y:18, opacity:0}}, {{y:0, opacity:1, duration:.12, ease:"power2.out"}}, {g["start"]});')
        for j, w in enumerate(g["words"]):
            ws = round(max(g["start"], w["start"]), 3)
            js.append(f'tl.fromTo("#{gid}w{j}", {{color:"#FFFFFF", scale:1}}, {{color:"{GOLD}", scale:1.05, duration:.08, ease:"power2.out"}}, {ws});')
            if j + 1 < len(g["words"]):
                ne = round(max(ws + 0.09, g["words"][j + 1]["start"]), 3)
                js.append(f'tl.to("#{gid}w{j}", {{color:"#FFFFFF", scale:1, duration:.06}}, {ne});')
    body = "\n".join("    " + h for h in html)
    script = "\n".join("    " + j for j in js)
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .capg {{ position: absolute; left: 0; right: 0; text-align: center; overflow: visible; }}
    .capi {{ display: inline-block; max-width: 940px; font-family: 'Poppins', sans-serif; font-weight: 700;
             line-height: 1.15; color: #FFFFFF; -webkit-text-stroke: 9px #120804; paint-order: stroke fill;
             text-shadow: 0 6px 18px rgba(0,0,0,.45); }}
    .cw {{ display: inline-block; margin: 0 .17em; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{script}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""


os.makedirs(f"{PROJ}/compositions", exist_ok=True)
for sc in SCENES:
    open(f"{PROJ}/compositions/{sc['id']}.html", "w").write(scene_file(sc))
EDIT = os.path.join(os.path.dirname(PROJ.rstrip("/")), "edit")
groups = caption_groups(f"{EDIT}/transcripts/source.json", json.load(open(f"{EDIT}/segmap.json")))
open(f"{PROJ}/compositions/captions.html", "w").write(captions_file(groups))
json.dump(groups, open(f"{EDIT}/captions.json", "w"), indent=1)
print("caption groups", len(groups))
open(f"{PROJ}/index.html", "w").write(index_file())
print("ok", len(SCENES), "scenes", len(SFX), "sfx")
