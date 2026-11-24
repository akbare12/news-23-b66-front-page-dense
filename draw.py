#!/usr/bin/env python3
"""news-23 b66 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
1024x1024 front page, 31 stories. PIL only in this file; main.py is stdlib-only."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(draw, x_right, y, label, fill):
    f = font(FB, 9)
    tw = draw.textlength(label, font=f)
    w = int(tw) + 10
    x0 = x_right - w
    draw.rounded_rectangle([x0, y, x_right, y + 12], radius=2, fill=fill)
    draw.text((x0 + 5, y + 1), label, font=f, fill="white")
    return x0

def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 58], fill="black")
    d.text((10, 8), "THE WORLD TODAY", font=font(FB, 40), fill="white")
    dt = "MONDAY 23 NOVEMBER 2026"
    d.text((W - 10 - d.textlength(dt, font=font(FB, 16)), 20), dt,
           font=font(FB, 16), fill="#f5c518")

    # ---------- kicker ----------
    kick = ("AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  "
            "US lead over China at record low  \u00b7  Anthropic IPO $107.3B")
    d.text((10, 60), kick, font=font(FB, 16), fill="#b91c1c")

    # ---------- number strip: 5 cols x 2 rows ----------
    nums = [
        ("-3.3%", "KOSPI", "#b91c1c"),
        ("5.3", "US-CHINA POWER GAP", "#1d4ed8"),
        ("11,762", "EBOLA CASES, DRC", "#15803d"),
        ("10T won", "SEOUL STABILISATION FUND", "#92400e"),
        ("2%", "BILLIONAIRE TAX IN PARIS", "#6b21a8"),
        ("$450M", "SKUBAL DEAL", "#6b21a8"),
        ("165", "RUSSIAN MISSILES/WEEK", "#b91c1c"),
        ("12,000", "CLEARED IN MANCHESTER", "#1d4ed8"),
        ("264 kg", "EXPLOSIVES SEIZED", "#92400e"),
        ("$107.3B", "ANTHROPIC IPO", "#6b21a8"),
    ]
    col_w = W // 5
    for i, (val, lab, col) in enumerate(nums):
        r, c = divmod(i, 5)
        x = c * col_w + 10
        y = 78 + r * 27
        d.text((x, y + 1), val, font=font(FB, 17), fill=col)
        d.text((x, y + 17), lab, font=font(FB, 10), fill="#111111")

    # ---------- region bar ----------
    regions = [("ASIA-PACIFIC 7", "#0f766e", 7), ("AMERICAS 8", "#1d4ed8", 8),
               ("MIDDLE EAST 6", "#92400e", 6), ("EUROPE 5", "#6b21a8", 5),
               ("AFRICA 3", "#b91c1c", 3), ("WORLD 2", "#4b5563", 2)]
    x = 0
    for name, col, n in regions:
        w = int(round(n / 31 * W))
        d.rectangle([x, 132, x + w, 152], fill=col)
        f = font(FB, 13)
        tw = d.textlength(name, font=f)
        d.text((x + (w - tw) / 2, 135), name, font=f, fill="white")
        x += w

    # ---------- UTC strip ----------
    utc = ("THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   "
           "~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles")
    d.text((10, 154), utc, font=font(F, 11), fill="#111111")
    ap = "~ APPROX"
    d.text((W - 10 - d.textlength(ap, font=font(F, 11)), 154), ap,
           font=font(F, 11), fill="#6b7280")

    # ---------- heroes ----------
    heroes = [
        dict(kind="kospi", strip="KOSPI 4,708.54   \u00b7   -161 PTS",
             head="AI ROUT HITS ASIA",
             body=("Kospi closes -3.3% to 4,708.54, sheds 161 pts; "
                   "intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%."),
             src="KOREA EXCHANGE"),
        dict(kind="guterres", strip="UN   \u00b7   BRIDGETOWN",
             head="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
             body=("UN chief urges global AI safety rules at the Bridgetown "
                   "summit; 150 back a risk framework."),
             src="UNITED NATIONS"),
        dict(kind="power", strip="ASIA POWER INDEX 2026",
             head="US LEAD OVER CHINA AT RECORD LOW",
             body=("Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, "
                   "narrowest since 2018. India third at 40.5."),
             src="LOWY INSTITUTE"),
    ]
    hx0 = [6, 348, 690]
    hw = 328
    for h, x0 in zip(heroes, hx0):
        # scene 168-282
        if h["kind"] == "kospi":
            d.rectangle([x0, 168, x0 + hw, 282], fill="#0b1e3a")
            # buildings (max 52px tall, bottom zone)
            import random
            rnd = random.Random(66)
            bx = x0 + 8
            while bx < x0 + hw - 14:
                bw = rnd.randint(16, 26)
                bh = rnd.randint(28, 52)
                d.rectangle([bx, 282 - bh, bx + bw, 282], fill="#12294d")
                for wy in range(282 - bh + 6, 278, 9):
                    for wx in range(bx + 3, bx + bw - 3, 7):
                        if rnd.random() < 0.55:
                            d.rectangle([wx, wy, wx + 3, wy + 4], fill="#f5c518")
                bx += bw + 4
            # chart line in LOWER zone only (y 240-272), clear of the -3.3% text
            pts = [(x0 + 10, 268), (x0 + 45, 252), (x0 + 80, 260),
                   (x0 + 115, 244), (x0 + 150, 256), (x0 + 185, 242),
                   (x0 + 220, 252), (x0 + 255, 240), (x0 + 290, 248),
                   (x0 + 318, 238)]
            d.line(pts, fill="#f59e0b", width=3)
            for px, py in pts:
                d.ellipse([px - 3, py - 3, px + 3, py + 3], fill="#fbbf24")
            d.text((x0 + 8, 172), "-3.3%", font=font(FB, 30), fill="#ef4444")
        elif h["kind"] == "guterres":
            d.rectangle([x0, 168, x0 + hw, 282], fill="#0f766e")
            d.text((x0 + 10, 176), "150 DELEGATES", font=font(FB, 26), fill="#f5c518")
            d.text((x0 + 10, 206), "BACK A RISK", font=font(FB, 26), fill="#f5c518")
            d.text((x0 + 10, 236), "FRAMEWORK", font=font(FB, 26), fill="#f5c518")
            cx, cy, r = x0 + hw - 52, 225, 42
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline="white", width=2)
            d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline="white", width=1)
            d.line([cx - r, cy, cx + r, cy], fill="white", width=1)
            d.line([cx - r + 8, cy - r // 2, cx + r - 8, cy - r // 2], fill="white", width=1)
            d.line([cx - r + 8, cy + r // 2, cx + r - 8, cy + r // 2], fill="white", width=1)
        else:
            d.rectangle([x0, 168, x0 + hw, 282], fill="#fef3c7")
            d.text((x0 + 10, 172), "NARROWEST SINCE 2018", font=font(FB, 13), fill="#111111")
            gp = "GAP 5.3"
            d.text((x0 + hw - 10 - d.textlength(gp, font=font(FB, 13)), 172), gp,
                   font=font(FB, 13), fill="#92400e")
            bars = [("78.9", "US", "#1e3a5f", 86), ("73.6", "CHINA", "#b91c1c", 81),
                    ("40.5", "INDIA", "#b45309", 45)]
            bx = x0 + 22
            for val, lab, col, bh in bars:
                d.rectangle([bx, 282 - bh, bx + 62, 282], fill=col)
                # value + label drawn AFTER the bar, in white inside it
                d.text((bx + 31 - d.textlength(val, font=font(FB, 15)) / 2, 282 - bh + 4),
                       val, font=font(FB, 15), fill="white")
                d.text((bx + 31 - d.textlength(lab, font=font(FB, 11)) / 2, 282 - bh + 22),
                       lab, font=font(FB, 11), fill="white")
                bx += 100
        # black strip under scene
        d.rectangle([x0, 282, x0 + hw, 298], fill="black")
        d.text((x0 + 8, 285), h["strip"], font=font(FB, 11), fill="white")
        # headline (clear gap below strip)
        lines = wrap(d, h["head"], font(FB, 20), hw - 8)[:2]
        y = 302
        for ln in lines:
            d.text((x0, y), ln, font=font(FB, 20), fill="#111111")
            y += 21
        # body 2 lines (11px, clear of the chip below)
        blines = wrap(d, h["body"], font(F, 11), hw - 8)[:2]
        y = 346
        for ln in blines:
            d.text((x0, y), ln, font=font(F, 11), fill="#111111")
            y += 14
        # source + chip
        d.text((x0, 376), h["src"], font=font(F, 10), fill="#6b7280")
        chip(d, x0 + hw, 374, "REPORTED", "#1d4ed8")

    # ---------- MORE OF THE DAY bar ----------
    d.rectangle([0, 386, W, 404], fill="black")
    d.text((10, 389), "MORE OF THE DAY  \u2014  10 STORIES", font=font(FB, 13), fill="white")

    # ---------- 10 cards ----------
    cards = [
        ("AMERICAS", "#b91c1c", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.",
         "Reuters", "REPORTED"),
        ("FBI", "#7f1d1d", "FBI PROBES NCIC HACK", "NCIC database hacked.",
         "AP", "REPORTED"),
        ("WHITE HOUSE", "#92400e", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.",
         "Reuters", "REPORTED"),
        ("MARKETS", "#1d4ed8", "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.",
         "Bloomberg", "REPORTED"),
        ("SPORT", "#b91c1c", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.",
         "AP", "REPORTED"),
        ("SPORT", "#b91c1c", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.",
         "ESPN", "REPORTED"),
        ("LEGAL", "#6b21a8", "STATES SUE SPACEX", "Ten states challenge AI claims.",
         "AP", "REPORTED"),
        ("TECH", "#1d4ed8", "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.",
         "WSJ", "REPORTED"),
        ("EUROPE", "#6b21a8", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.",
         "AP", "CLAIM"),
        ("SPACE", "#4b5563", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.",
         "Reuters", "CLAIM"),
    ]
    for i, (cat, col, head, body, src, tag) in enumerate(cards):
        r, c = divmod(i, 5)
        x0 = 6 + c * 204
        y0 = 406 + r * 74
        # header strip
        d.rectangle([x0, y0, x0 + 196, y0 + 16], fill=col)
        d.text((x0 + 5, y0 + 2), cat, font=font(FB, 10), fill="white")
        num = str(i + 1)
        d.text((x0 + 196 - 5 - d.textlength(num, font=font(FB, 10)), y0 + 2),
               num, font=font(FB, 10), fill="white")
        # headline, up to 2 lines
        hlines = wrap(d, head, font(FB, 12), 188)[:2]
        y = y0 + 19
        for ln in hlines:
            d.text((x0, y), ln, font=font(FB, 12), fill="#111111")
            y += 13
        # body 1 line
        d.text((x0, y0 + 48), body, font=font(F, 10), fill="#111111")
        # source + chip at bottom (clear of body)
        d.text((x0, y0 + 62), src, font=font(F, 9), fill="#6b7280")
        chip(d, x0 + 196, y0 + 59, tag, "#1d4ed8" if tag == "REPORTED" else "#b91c1c")

    # ---------- WHERE IT HAPPENED / ALSO bar ----------
    d.rectangle([0, 554, W, 572], fill="black")
    d.text((10, 557), "WHERE IT HAPPENED", font=font(FB, 13), fill="white")
    d.text((340, 557), "ALSO ON MONDAY", font=font(FB, 13), fill="white")

    # ---------- map ----------
    d.rectangle([6, 578, 330, 820], fill="#f3f4f6")
    for gx in range(6, 331, 16):
        d.line([gx, 578, gx, 820], fill="#e5e7eb", width=1)
    for gy in range(578, 821, 16):
        d.line([6, gy, 330, gy], fill="#e5e7eb", width=1)
    d.ellipse([20, 610, 200, 770], fill="#bbf7d0")
    d.ellipse([160, 600, 320, 750], fill="#bbf7d0")
    d.ellipse([215, 730, 305, 785], fill="#bbf7d0")
    pins = [(262, 640), (60, 720), (285, 620), (75, 690), (95, 665),
            (200, 665), (55, 640), (30, 700), (70, 730), (95, 745),
            (210, 625), (225, 645), (250, 610)]
    for i, (px, py) in enumerate(pins, 1):
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill="#b91c1c", outline="white", width=1)
        lab = str(i)
        d.text((px - d.textlength(lab, font=font(FB, 9)) / 2, py - 5),
               lab, font=font(FB, 9), fill="white")
    leg = ["Pins 1\u201313:  1 Seoul  \u00b7  2 Bridgetown  \u00b7  3 Beijing",
           "4 Washington  \u00b7  5 New York  \u00b7  6 Tehran  \u00b7  7 Chicago",
           "8 SF  \u00b7  9 Denver  \u00b7  10 Austin  \u00b7  11 Warsaw  \u00b7  12 Kyiv  \u00b7  13 Moscow"]
    y = 788
    for ln in leg:
        d.text((10, y), ln, font=font(F, 9), fill="#111111")
        y += 11

    # ---------- ALSO list ----------
    also = [
        "Paris: 100+ back 2% billionaire tax",
        "Manchester: 12,000 cleared",
        "Zelenskyy: 165 missiles in a week",
        "COP31: the day after pact rejected",
        "Benghazi: UN demands port probe",
        "Israel unity talks resume",
        "Gaza: two killed in Israeli strike",
        "West Bank settler attacks",
        "Iran war: no deal in sight",
        "Lebanon seizes 264 kg explosives",
        "Bahrain: strike hits plant, 2 hurt",
        "Sudan: defences down drones",
        "DRC: fighting traps Ebola teams",
        "Bangladesh: Hasina jailed if she returns",
        "Seoul minister quits in exam row",
        "SK Telecom -7.3% as hype cools",
        "China eases margin rules",
        "Seoul readies 10T-won fund",
    ]
    f_also = font(F, 12)
    for i, item in enumerate(also):
        col, row = divmod(i, 9)
        x = 340 + col * 340
        y = 580 + row * 26
        d.text((x, y), f"{14 + i}. {item}", font=f_also, fill="#111111")

    # ---------- DATE CHECK ----------
    d.rectangle([6, 826, 1018, 906], outline="#b91c1c", width=2)
    d.text((12, 832), "DATE CHECK", font=font(FB, 13), fill="#b91c1c")
    right = "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY"
    d.text((1012 - d.textlength(right, font=font(FB, 10)), 834), right,
           font=font(FB, 10), fill="#b91c1c")
    leftout = ("LEFT OUT \u2014 NOT 23 NOV:  Dems 258 seats (22 Nov)  \u00b7  "
               "Sparta II fire (22 Nov)  \u00b7  El Chapo captured (22 Nov)  \u00b7  "
               "EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  "
               "ICJ Myanmar (19 Nov)")
    f_lo = font(F, 12)
    while d.textlength(leftout, font=f_lo) > 994 and f_lo.size > 9:
        f_lo = font(F, f_lo.size - 1)
    d.text((12, 852), leftout, font=f_lo, fill="#111111")
    notyet = ("NOT YET:  Dymer search continues (14 missing)  \u00b7  "
             "4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  "
             "WHO evacuating trapped Ebola staff")
    d.text((12, 874), notyet, font=font(F, 12), fill="#111111")

    # ---------- sources ----------
    d.text((10, 912),
           "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
           font=font(F, 10), fill="#6b7280")
    d.text((10, 928),
           "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.",
           font=font(F, 10), fill="#6b7280")
    d.text((10, 938),
           "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
           font=font(F, 10), fill="#6b7280")

    # ---------- bottom bar ----------
    d.rectangle([0, 950, W, H], fill="black")
    foot = "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
    ff = font(FB, 18)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 978), foot, font=ff, fill="#f5c518")

    img.save(OUT, "PNG")
    print("saved", OUT, os.path.getsize(OUT), "bytes")

if __name__ == "__main__":
    main()
