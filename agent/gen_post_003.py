#!/usr/bin/env python3
"""Post #003 ia.aujourdhui — Comparatif ChatGPT vs Gemini vs Claude (gratuit, juin 2026).
Genere les slides Insta 1080x1350 et TikTok 1080x1920."""
from PIL import Image, ImageDraw, ImageFont
import os

BG_TOP = (12, 12, 28)
BG_BOT = (28, 16, 58)
ACCENT = (124, 92, 255)
ACCENT2 = (64, 224, 208)
WHITE = (245, 245, 250)
GREY = (165, 165, 185)

FB = "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
if not os.path.exists(FB):
    FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def gradient_bg(W, H):
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / H
        r = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

class Layout:
    def __init__(self, W, H, s):
        self.W, self.H, self.s = W, H, s

def draw_footer(d, L, page, total):
    f = font(FB, int(34 * L.s))
    d.text((80, L.H - int(90 * L.s)), "@ia.aujourdhui", font=f, fill=GREY)
    txt = f"{page}/{total}"
    d.text((L.W - 80 - d.textlength(txt, font=f), L.H - int(90 * L.s)), txt, font=f, fill=GREY)

def deco(d, L):
    d.rectangle([80, int(80 * L.s), 220, int(80 * L.s) + 16], fill=ACCENT)

def slide_cover(L, total):
    img = gradient_bg(L.W, L.H)
    d = ImageDraw.Draw(img)
    deco(d, L)
    d.text((80, int(170 * L.s)), "COMPARATIF 2026", font=font(FB, int(40 * L.s)), fill=ACCENT2)
    y = int(265 * L.s)
    fT = font(FB, int(88 * L.s))
    for line in wrap(d, "ChatGPT vs Gemini vs Claude : lequel choisir en gratuit ?", fT, L.W - 160):
        d.text((80, y), line, font=fT, fill=WHITE)
        y += int(108 * L.s)
    y += int(40 * L.s)
    fS = font(FR, int(48 * L.s))
    for line in wrap(d, "Le vrai match de juin 2026, sans payer un centime.", fS, L.W - 160):
        d.text((80, y), line, font=fS, fill=GREY)
        y += int(62 * L.s)
    d.text((80, L.H - int(220 * L.s)), "Swipe pour le verdict", font=font(FB, int(54 * L.s)), fill=ACCENT)
    draw_footer(d, L, 1, total)
    return img

def slide_item(L, idx, total, label, name, tagline, points):
    img = gradient_bg(L.W, L.H)
    d = ImageDraw.Draw(img)
    deco(d, L)
    d.text((80, int(140 * L.s)), label, font=font(FB, int(44 * L.s)), fill=ACCENT2)
    d.text((80, int(215 * L.s)), name, font=font(FB, int(86 * L.s)), fill=WHITE)
    y = int(345 * L.s)
    fT = font(FR, int(48 * L.s))
    for line in wrap(d, tagline, fT, L.W - 160):
        d.text((80, y), line, font=fT, fill=ACCENT2)
        y += int(62 * L.s)
    y += int(45 * L.s)
    fP = font(FR, int(45 * L.s))
    for p in points:
        d.ellipse([80, y + int(16 * L.s), 104, y + int(16 * L.s) + 24], fill=ACCENT)
        for line in wrap(d, p, fP, L.W - 240):
            d.text((140, y), line, font=fP, fill=WHITE)
            y += int(58 * L.s)
        y += int(26 * L.s)
    draw_footer(d, L, idx, total)
    return img

def slide_verdict(L, idx, total):
    img = gradient_bg(L.W, L.H)
    d = ImageDraw.Draw(img)
    deco(d, L)
    d.text((80, int(140 * L.s)), "LE VERDICT", font=font(FB, int(44 * L.s)), fill=ACCENT2)
    d.text((80, int(215 * L.s)), "Selon ton usage", font=font(FB, int(80 * L.s)), fill=WHITE)
    rows = [
        ("Exposés, recherches, Google Docs", "Gemini"),
        ("Polyvalence, images, vocal", "ChatGPT"),
        ("Rédaction, code, confidentialité", "Claude"),
    ]
    y = int(400 * L.s)
    fA = font(FR, int(44 * L.s))
    fB = font(FB, int(56 * L.s))
    for usage, winner in rows:
        d.rounded_rectangle([80, y, L.W - 80, y + int(210 * L.s)], radius=28, outline=ACCENT, width=3)
        yy = y + int(30 * L.s)
        for line in wrap(d, usage, fA, L.W - 220):
            d.text((110, yy), line, font=fA, fill=GREY)
            yy += int(56 * L.s)
        d.text((110, yy + int(8 * L.s)), winner, font=fB, fill=ACCENT2)
        y += int(250 * L.s)
    draw_footer(d, L, idx, total)
    return img

def slide_cta(L, total):
    img = gradient_bg(L.W, L.H)
    d = ImageDraw.Draw(img)
    deco(d, L)
    y = int(300 * L.s)
    fT = font(FB, int(84 * L.s))
    for line in wrap(d, "Un comparatif IA comme ça chaque semaine.", fT, L.W - 160):
        d.text((80, y), line, font=fT, fill=WHITE)
        y += int(104 * L.s)
    y += int(35 * L.s)
    fS = font(FR, int(50 * L.s))
    for line in wrap(d, "Abonne-toi et enregistre ce post pour le retrouver avant tes partiels.", fS, L.W - 160):
        d.text((80, y), line, font=fS, fill=GREY)
        y += int(66 * L.s)
    bx, by = 80, y + int(80 * L.s)
    d.rounded_rectangle([bx, by, bx + 460, by + 110], radius=55, fill=ACCENT)
    d.text((bx + 60, by + 24), "+ S'abonner", font=font(FB, 52), fill=WHITE)
    draw_footer(d, L, total, total)
    return img

CONTENT = [
    ("cover",),
    ("item", "ROUND 1", "ChatGPT", "Le plus polyvalent du game.",
     ["GPT-5.5 accessible gratuitement : environ 10 messages toutes les 5 h",
      "Ensuite, bascule automatique sur un modèle plus léger",
      "Fort partout : texte, images, mode vocal"]),
    ("item", "ROUND 2", "Gemini", "L'arme secrète des étudiants Google.",
     ["Gemini 3.5 Flash en gratuit, limites rechargées toutes les 5 h",
      "Intégré à Gmail, Docs et YouTube",
      "Bonus : NotebookLM pour transformer tes cours en fiches"]),
    ("item", "ROUND 3", "Claude", "Le nouveau, sorti il y a 3 jours.",
     ["Claude Fable 5 disponible en gratuit depuis le 9 juin 2026",
      "Excellent en rédaction, raisonnement et code",
      "N'entraîne pas ses modèles sur tes conversations par défaut"]),
    ("verdict",),
    ("item", "L'ASTUCE", "Utilise les 3", "Pourquoi choisir, en fait ?",
     ["Les 3 sont gratuits, avec des limites séparées",
      "Quand l'un est à court de messages, passe au suivant",
      "Résultat : de l'IA quasi illimitée, pour 0 euro"]),
    ("cta",),
]

def render(L, outdir):
    os.makedirs(outdir, exist_ok=True)
    total = len(CONTENT)
    for i, c in enumerate(CONTENT, start=1):
        if c[0] == "cover":
            img = slide_cover(L, total)
        elif c[0] == "verdict":
            img = slide_verdict(L, i, total)
        elif c[0] == "cta":
            img = slide_cta(L, total)
        else:
            img = slide_item(L, i, total, c[1], c[2], c[3], c[4])
        img.save(f"{outdir}/slide_{i}.png")
        print(f"{outdir}/slide_{i}.png")

if __name__ == "__main__":
    render(Layout(1080, 1350, 1.0), "post_003")
    render(Layout(1080, 1920, 1.42), "post_003/tiktok")