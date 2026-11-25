#!/usr/bin/env python3
"""Compose the front page of The Daily Globe — Wednesday, November 25, 2026.
Rendered at 2x supersample (2048x2048) and downscaled to 1024x1024."""
from PIL import Image, ImageDraw, ImageFont
import os

S = 2                      # supersample factor
W = 1024 * S               # canvas width  (2048)
H = 1024 * S               # canvas height (2048)
PAPER = (248, 244, 234)
INK = (20, 18, 14)
ACCENT = (125, 26, 18)
BOXBG = (238, 231, 214)
GREY = (84, 78, 66)

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(HERE, "lead-photo.png")
OUT = os.path.join(HERE, "entry.png")

NOTO = "/usr/share/fonts/truetype/noto/"
DEJA = "/usr/share/fonts/truetype/dejavu/"


def font(path, size):
    return ImageFont.truetype(path, size)


def masthead_font(size):
    for p in (NOTO + "NotoSerifDisplay-Black.ttf", DEJA + "DejaVuSerif-Bold.ttf"):
        if os.path.exists(p):
            return font(p, size)
    return font(DEJA + "DejaVuSerif.ttf", size)


def serif(size, bold=False, italic=False):
    name = "NotoSerif-%s.ttf" % ("Bold" if bold else
                                 "Italic" if italic else "Regular")
    p = NOTO + name
    if not os.path.exists(p):
        p = DEJA + ("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf")
    return font(p, size)


def sans(size, bold=False):
    p = DEJA + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return font(p, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 56                     # margin (28 px at final scale)
CW = W - 2 * M             # content width


def rule(y, thick=3, x0=M, x1=W - M, color=INK):
    d.rectangle([x0, y, x1, y + thick], fill=color)


def centered(text, y, fnt, color=INK, spacing=0):
    if spacing:
        text = (" " * 0).join(list(text.replace(" ", "\u2002")))
    w = d.textlength(text, font=fnt)
    d.text(((W - w) / 2, y), text, font=fnt, fill=color)
    return y + fnt.size


def wrap(text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def column(x, y, width, text, fnt, leading, max_y, color=INK):
    for ln in wrap(text, fnt, width):
        if y + leading > max_y:
            break
        d.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def headline(x, y, width, text, size, align="left", color=INK):
    fnt = serif(size, bold=True)
    for ln in wrap(text, fnt, width):
        if align == "center":
            w = d.textlength(ln, font=fnt)
            d.text((x + (width - w) / 2, y), ln, font=fnt, fill=color)
        else:
            d.text((x, y), ln, font=fnt, fill=color)
        y += int(size * 1.12)
    return y


# ---------------------------------------------------------------- folio line
f_folio = sans(25)
d.text((M, 30), "Vol. CXII . . . No. 328", font=f_folio, fill=GREY)
t = "THE WORLD'S PAPER OF RECORD"
w = d.textlength(t, font=f_folio)
d.text(((W - w) / 2, 30), t, font=f_folio, fill=GREY)
t = "Price $2.50"
w = d.textlength(t, font=f_folio)
d.text((W - M - w, 30), t, font=f_folio, fill=GREY)
rule(66, 3)

# ---------------------------------------------------------------- masthead
f_mast = masthead_font(172)
t = "The Daily Globe"
w = d.textlength(t, font=f_mast)
d.text(((W - w) / 2, 78), t, font=f_mast, fill=INK)
rule(268, 6)
rule(280, 2)

# ---------------------------------------------------------------- date bar
f_date = sans(30, bold=True)
d.text((M, 294), "NEW YORK", font=f_date, fill=INK)
t = "WEDNESDAY, NOVEMBER 25, 2026"
w = d.textlength(t, font=f_date)
d.text(((W - w) / 2, 294), t, font=f_date, fill=INK)
t = "LATE CITY FINAL"
w = d.textlength(t, font=f_date)
d.text((W - M - w, 294), t, font=f_date, fill=INK)
rule(338, 3)

# ---------------------------------------------------------------- lead story
f_kick = sans(30, bold=True)
t = "DAY THREE OF THE MEDITERRANEAN CRISIS"
w = d.textlength(t, font=f_kick)
d.text(((W - w) / 2, 358), t, font=f_kick, fill=ACCENT)

y = headline(M, 396, CW,
             "MOSCOW DELIVERS ITS \u2018ANSWER\u2019: MISSILE SALVOS OVER THE MED",
             104, align="center")
f_deck = serif(37, italic=True)
for ln in wrap("38 warships open live-fire drills off Libya; NATO invokes "
               "Article 4 and rushes a carrier group east as allied jets "
               "scramble for a second night", f_deck, CW - 160):
    w = d.textlength(ln, font=f_deck)
    d.text(((W - w) / 2, y + 8), ln, font=f_deck, fill=(52, 48, 40))
    y += 50

# ---------------------------------------------------------------- lead photo
TOP = 748
COLW = 520
LX = M                    # left column x
CX = M + COLW + 44        # centre column x
RX = W - M - COLW         # right column x
photo = Image.open(PHOTO).convert("RGB")
PW, PH = 788, 660
px, py = CX, TOP
scale = max(PW / photo.width, PH / photo.height)
photo = photo.resize((int(photo.width * scale) + 1,
                      int(photo.height * scale) + 1), Image.LANCZOS)
ox = (photo.width - PW) // 2
oy = (photo.height - PH) // 2
img.paste(photo.crop((ox, oy, ox + PW, oy + PH)), (px, py))
d.rectangle([px, py, px + PW, py + PH], outline=INK, width=3)
f_cap = serif(25, italic=True)
cap = ("A Russian frigate fires a Kalibr cruise missile at dawn on Tuesday, "
       "opening Exercise Otvet in the eastern Mediterranean.")
yy = py + PH + 12
for ln in wrap(cap, f_cap, PW):
    d.text((px, yy), ln, font=f_cap, fill=(52, 48, 40))
    yy += 32
f_cred = sans(21)
t = "RUSSIAN DEFENCE MINISTRY / VIA REUTERS"
d.text((px, yy + 2), t, font=f_cred, fill=GREY)

# ---------------------------------------------------------------- lead text
f_body = serif(27)
f_by = sans(24, bold=True)
LEAD_MAX = 1536

y = TOP
d.text((LX, y), "By MARCUS HALE and ANNA PETROVA", font=f_by, fill=INK)
y += 40
y = column(LX, y, COLW,
       "MOSCOW \u2014 Russia answered the sinking of the corvette Merkury "
       "before dawn on Wednesday, opening live-fire missile drills in "
       "the eastern Mediterranean and warning that any vessel approaching "
       "its task force \u201cwill be treated as a combatant.\u201d The Defence "
       "Ministry said 38 warships, led by the frigate Admiral Kasatonov, "
       "had fired 14 Kalibr missiles at targets off the Libyan coast in "
       "the first salvo of Exercise Otvet \u2014 \u201canswer\u201d in "
       "Russian.", f_body, 36, LEAD_MAX)
column(LX, y + 10, COLW,
       "\u201cThe answer has been delivered,\u201d the ministry\u2019s "
       "spokesman, Maj. Gen. Viktor Sorokin, said in a televised briefing. "
       "\u201cIt will continue until those who raised a hand against the "
       "Russian fleet understand the price.\u201d", f_body, 36, LEAD_MAX)

y = TOP
column(RX, y, COLW,
       "In Brussels, NATO ambassadors met under Article 4 for the second "
       "time in three days. The alliance ordered the carrier Gerald R. Ford "
       "and its strike group east, and allied jets scrambled twice "
       "overnight near Crete. \u201cWe do not seek a wider war,\u201d the "
       "secretary general said. \u201cBut an alliance that does not answer "
       "an answer invites a third act.\u201d Ukraine, whose drones sank "
       "the Merkury off Benghazi on Sunday, said its forces were "
       "\u201cwatching, and ready.\u201d", f_body, 36, 1252)

# teaser line under the photo caption, centre column
f_tease = serif(26, italic=True)
t = "Full coverage of the crisis: Pages A6\u2013A9"
w = d.textlength(t, font=f_tease)
d.text((CX + (PW - w) / 2, 1500), t, font=f_tease, fill=ACCENT)

# fact box, right column
BX, BY, BW2 = RX, 1272, COLW
d.rectangle([BX, BY, BX + BW2, BY + 196], fill=BOXBG, outline=INK, width=2)
f_bh = sans(25, bold=True)
d.text((BX + 18, BY + 12), "THE CRISIS AT A GLANCE", font=f_bh, fill=ACCENT)
f_bb = sans(24)
facts = ["38 Russian warships in the eastern Med",
         "14 Kalibr missiles fired before dawn",
         "Carrier Gerald R. Ford ordered east",
         "Article 4 talks: second in three days",
         "Brent crude $118.42, up 6.9 percent"]
yy = BY + 52
for fct in facts:
    d.text((BX + 18, yy), "\u2022 " + fct, font=f_bb, fill=INK)
    yy += 29

# ---------------------------------------------------------------- bottom band
rule(1560, 4)
BAND = 1584
BWID, BGAP = 448, 48
f_bh2 = serif(43, bold=True)
f_bb2 = serif(25)


def band(i, head, text):
    x = M + i * (BWID + BGAP)
    yy = headline(x, BAND, BWID, head, 43)
    column(x, yy + 4, BWID, text, f_bb2, 33, 1906)
    if i:
        d.line([x - BGAP // 2, BAND, x - BGAP // 2, 1900], fill=GREY, width=2)


band(0, "OIL TOPS $118 ON DAY THREE",
     "LONDON \u2014 The Hormuz blockade entered its third day with 214 "
     "tankers at anchor. The I.E.A. weighed a stockpile release; "
     "Washington promised a naval escort plan \u201cwithin days.\u201d")
band(1, "ISLAND STATES WIN COURT DATE",
     "THE HAGUE \u2014 The World Court will hear the island nations\u2019 "
     "$212 billion climate suit on March 9. \u201cFor 30 years we made "
     "speeches,\u201d Tuvalu\u2019s premier said. \u201cNow we will make "
     "arguments.\u201d")
band(2, "HUANG\u2019S ROBOTS ROLL OFF THE LINE",
     "DETROIT \u2014 The first thousand of Mr. Huang\u2019s million robots "
     "\u201cclocked in\u201d Tuesday at Nvidia\u2019s $8 billion robot "
     "city. \u201cOn Monday I promised a million,\u201d he said. "
     "\u201cToday the first thousand arrived.\u201d")
band(3, "SKUBAL SIGNS, QUEENS ERUPTS",
     "Tarik Skubal signed his ten-year, $450 million contract at Citi "
     "Field, then threw 22 pitches to 3,000 roaring fans. \u201cI "
     "didn\u2019t come here for the money,\u201d he said. \u201cI came "
     "to win in October.\u201d")

# ---------------------------------------------------------------- strips
rule(1918, 3)
f_strip = sans(23)
d.text((M, 1932),
       "WEATHER  New York 46\u00b0/38\u00b0 rain late \u2022 Washington "
       "50\u00b0/39\u00b0 \u2022 Chicago 41\u00b0/30\u00b0 snow flurries "
       "\u2022 London 48\u00b0/41\u00b0 \u2022 Kyiv 37\u00b0/28\u00b0 snow "
       "\u2022 Benghazi 70\u00b0/59\u00b0 clear", font=f_strip, fill=INK)
d.text((M, 1964),
       "MARKETS  Dow 44,182 \u2212641 \u2022 Nasdaq 21,940 \u22122.1% "
       "\u2022 Brent $118.42 +6.9% \u2022 Gold $4,118 +1.8% \u2022 Nvidia "
       "$171.20 \u22123.4% \u2022 Fed holds, hints at Dec. cut",
       font=f_strip, fill=INK)
t = ("AND FINALLY: Marmalade the cat, missing nine years in Ohio, came "
     "home Monday through his own cat flap, ate a bowl of tuna and "
     "slept. \u201cSame attitude,\u201d his owner said.")
w = d.textlength(t, font=serif(24, italic=True))
d.text(((W - w) / 2, 1998), t, font=serif(24, italic=True), fill=(52, 48, 40))

# ---------------------------------------------------------------- save
img = img.resize((1024, 1024), Image.LANCZOS)
img.save(OUT)
print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")
