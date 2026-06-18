#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

BG_TOP = (12, 12, 28)
BG_BOT = (28, 16, 58)
ACCENT = (124, 92, 255)
ACCENT2 = (64, 224, 208)
WHITE = (245, 245, 250)
GREY = (165, 165, 185)

FB = "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"

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

def draw_footer(d, W, H, page, total):
    fs = int(H * 0.025)
    d.text((80, H - int(H*0.067)), "@ia.aujourdhui", font=font(FB, fs), fill=GREY)
    txt = f"{page}/{total}"
    d.text((W - 80 - d.textlength(txt, font=font(FB, fs)), H - int(H*0.067)), txt,
           font=font(FB, fs), fill=GREY)

def deco(d):
    d.rectangle([80, 80, 220, 96], fill=ACCENT)

def slide_cover(W, H, total):
    img = gradient_bg(W, H)
    d = ImageDraw.Draw(img)
    deco(d)
    tsize = int(W*0.037)
    d.text((80, 180), "ASTUCES IA — RECHERCHE DE STAGE", font=font(FB, tsize), fill=ACCENT2)
    title = "5 prompts IA gratuits pour décrocher ton stage cet été"
    y = 280
    tfs = int(W*0.085)
    for line in wrap(d, title, font(FB, tfs), W - 160):
        d.text((80, y), line, font=font(FB, tfs), fill=WHITE)
        y += int(tfs*1.22)
    sub = "CV, lettre de motivation, entretien : tout avec un chatbot gratuit."
    y += 40
    sfs = int(W*0.044)
    for line in wrap(d, sub, font(FR, sfs), W - 160):
        d.text((80, y), line, font=font(FR, sfs), fill=GREY)
        y += int(sfs*1.3)
    d.text((80, H - int(H*0.16)), "Swipe ->", font=font(FB, int(W*0.05)), fill=ACCENT)
    draw_footer(d, W, H, 1, total)
    return img

def slide_prompt(W, H, idx, total, num, title, prompt_text, tip):
    img = gradient_bg(W, H)
    d = ImageDraw.Draw(img)
    deco(d)
    d.text((80, 150), f"{num}", font=font(FB, int(W*0.13)), fill=ACCENT)
    tfs = int(W*0.062)
    y0 = 150 + int(W*0.15)
    for line in wrap(d, title, font(FB, tfs), W - 160):
        d.text((80, y0), line, font=font(FB, tfs), fill=WHITE)
        y0 += int(tfs*1.2)
    y = y0 + 30
    # boite prompt
    box_pad = 36
    pfs = int(W*0.036)
    plines = wrap(d, prompt_text, font(FR, pfs), W - 160 - 2*box_pad)
    box_h = box_pad*2 + len(plines) * int(pfs*1.35)
    d.rounded_rectangle([80, y, W-80, y+box_h], radius=24, outline=ACCENT2, width=3)
    yy = y + box_pad
    for line in plines:
        d.text((80+box_pad, yy), line, font=font(FR, pfs), fill=ACCENT2)
        yy += int(pfs*1.35)
    y = y + box_h + 50
    tipfs = int(W*0.038)
    d.ellipse([80, y + 14, 104, y + 38], fill=ACCENT)
    for line in wrap(d, tip, font(FR, tipfs), W - 240):
        d.text((140, y), line, font=font(FR, tipfs), fill=WHITE)
        y += int(tipfs*1.3)
    draw_footer(d, W, H, idx, total)
    return img

def slide_cta(W, H, total):
    img = gradient_bg(W, H)
    d = ImageDraw.Draw(img)
    deco(d)
    title = "Un conseil IA utile chaque jour."
    y = 320
    tfs = int(W*0.082)
    for line in wrap(d, title, font(FB, tfs), W - 160):
        d.text((80, y), line, font=font(FB, tfs), fill=WHITE)
        y += int(tfs*1.22)
    y += 30
    sub = "Abonne-toi pour ne rien rater, et enregistre ce post pour tes prochaines candidatures."
    sfs = int(W*0.044)
    for line in wrap(d, sub, font(FR, sfs), W - 160):
        d.text((80, y), line, font=font(FR, sfs), fill=GREY)
        y += int(sfs*1.3)
    bx, by = 80, y + 80
    bw, bh = int(W*0.42), int(W*0.1)
    d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=bh//2, fill=ACCENT)
    d.text((bx + 50, by + bh//4), "+ S'abonner", font=font(FB, int(W*0.046)), fill=WHITE)
    draw_footer(d, W, H, total, total)
    return img

PROMPTS = [
    ("1", "Reformuler ton CV",
     "\"Voici mon CV [colle le texte]. Reformule chaque expérience en 2 lignes percutantes avec des verbes d'action, pour un stage en [domaine].\"",
     "Colle aussi l'offre de stage : l'IA adapte le vocabulaire aux mots-clés attendus."),
    ("2", "Générer une lettre de motivation",
     "\"Écris une lettre de motivation courte (200 mots) pour ce stage chez [entreprise], à partir de mon profil [colle ton CV] et de l'offre [colle l'annonce].\"",
     "Relis toujours et personnalise une phrase à la main : un recruteur repère un texte 100% générique."),
    ("3", "S'entraîner à l'entretien",
     "\"Simule un entretien pour ce poste de stagiaire [poste]. Pose-moi 5 questions une par une et donne-moi un retour après chaque réponse.\"",
     "Demande explicitement un retour critique, sinon l'IA reste trop gentille."),
    ("4", "Préparer tes questions au recruteur",
     "\"Donne-moi 5 questions intelligentes à poser en fin d'entretien pour un stage en [domaine], qui montrent que je me suis renseigné sur l'entreprise.\"",
     "Pose une question sur un projet récent de l'entreprise : ça marque toujours plus qu'une question générique."),
    ("5", "Vérifier le ton et les fautes",
     "\"Relis cette lettre de motivation [colle le texte] : corrige les fautes et signale les phrases trop familières ou trop prétentieuses.\"",
     "À faire en tout dernier, une fois le fond du texte validé par toi-même."),
]

def build(W, H, outdir, prefix):
    total = len(PROMPTS) + 2
    slide_cover(W, H, total).save(f"{outdir}/{prefix}_1.png")
    for i, (num, title, prompt_text, tip) in enumerate(PROMPTS, start=2):
        slide_prompt(W, H, i, total, num, title, prompt_text, tip).save(f"{outdir}/{prefix}_{i}.png")
    slide_cta(W, H, total).save(f"{outdir}/{prefix}_{total}.png")
    print("OK", prefix, total, "slides")

import os
home = os.path.expanduser("~/work/post_007")
build(1080, 1350, f"{home}/insta", "slide")
build(1080, 1920, f"{home}/tiktok", "tiktok")
