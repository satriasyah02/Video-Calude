
# ---------- captions (word-level, output timeline) ----------
CAP_Y = 1235
# title cards already say these words on screen: hook, body "RENDANG CUMI!", end card
CAP_SKIP = [(0.0, 3.95), (51.6, 56.0), (80.2, 999)]
FIX = {"ma-mamaku": "mamaku"}


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
        if len(cur) >= 4 or w["text"][-1:] in ".?!," or gap >= 0.6 or (gap >= 0.15 and len(cur) >= 2):
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
        spans = " ".join(f'<span id="{gid}w{j}" class="cw">{clean(w["text"])}</span>' for j, w in enumerate(g["words"]))
        d = round(g["end"] - g["start"], 3)
        html.append(f'<div id="{gid}" class="capg clip" data-start="{g["start"]}" data-duration="{d}" style="top:{CAP_Y}px">'
                    f'<div id="{gid}i" class="capi" style="font-size:{size}px">{spans}</div></div>')
        js.append(f'tl.fromTo("#{gid}i", {{y:18, opacity:0}}, {{y:0, opacity:1, duration:.12, ease:"power2.out"}}, {g["start"]});')
        for j, w in enumerate(g["words"]):
            ws = round(max(g["start"], w["start"]), 3)
            js.append(f'tl.fromTo("#{gid}w{j}", {{color:"#FFFFFF", scale:1}}, {{color:"{GOLD}", scale:1.08, duration:.08, ease:"power2.out"}}, {ws});')
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
    .cw {{ display: inline-block; }}
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
