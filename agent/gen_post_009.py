#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"

BG_TOP = (12, 12, 28)
BG_BOTTOM = (28, 16, 58)
VIOLET = (124, 92, 255)
TURQUOISE = (64, 224, 208)
WHITE = (245, 245, 250)
GREY = (180, 180, 195)

OUT_DIR = "/tmp/post_009_new"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUT_DIR, "tiktok"), exist_ok=True)


def make_gradient(w, h):
    base = Image.new("RGB", (w, h), BG_TOP)
    top = BG_TOP
    bottom = BG_BOTTOM
    for y in range(h):
        t = y / h
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        ImageDraw.Draw(base).line([(0, y), (w, y)], fill=(r, g, b))
    return base


def add_glow_shapes(img, w, h):
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.ellipse([w * 0.55, -h * 0.12, w * 1.25, h * 0.32], fill=VIOLET + (40,))
    d.ellipse([-w * 0.25, h * 0.75, w * 0.35, h * 1.15], fill=TURQUOISE + (35,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"), (0, 0))
    return img


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = (cur + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_footer(draw, w, h, page, total, font_small):
    draw.text((70, h - 80), "@ia.aujourdhui", font=font_small, fill=GREY)
    label = f"{page}/{total}"
    bbox = draw.textbbox((0, 0), label, font=font_small)
    draw.text((w - 70 - (bbox[2] - bbox[0]), h - 80), label, font=font_small, fill=GREY)


def draw_pill(draw, x, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    pad_x, pad_y = 28, 16
    w = bbox[2] - bbox[0] + pad_x * 2
    h = bbox[3] - bbox[1] + pad_y * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=h // 2, fill=fill)
    draw.text((x + pad_x, y + pad_y - bbox[1]), text, font=font, fill=(12, 12, 28))
    return h


def render_slide(w, h, page, total, kicker, title_lines, body_lines=None, cta=False):
    img = make_gradient(w, h)
    img = add_glow_shapes(img, w, h)
    draw = ImageDraw.Draw(img)

    margin = int(w * 0.09)
    max_text_w = w - margin * 2

    f_kicker = ImageFont.truetype(FONT_BOLD, int(w * 0.036))
    f_small = ImageFont.truetype(FONT_REG, int(w * 0.03))
    f_title = ImageFont.truetype(FONT_BOLD, int(w * 0.075))
    f_body = ImageFont.truetype(FONT_REG, int(w * 0.042))

    y = int(h * 0.10)

    if kicker:
        draw_pill(draw, margin, y, kicker.upper(), f_kicker, TURQUOISE)
        y += int(h * 0.08)

    title_full = " ".join(title_lines)
    title_wrapped = wrap_text(draw, title_full, f_title, max_text_w)
    for line in title_wrapped:
        draw.text((margin, y), line, font=f_title, fill=WHITE)
        bbox = draw.textbbox((0, 0), line, font=f_title)
        y += (bbox[3] - bbox[1]) + int(h * 0.018)

    y += int(h * 0.02)

    if body_lines:
        for entry in body_lines:
            if isinstance(entry, tuple):
                marker, text = entry
            else:
                marker, text = None, entry
            if marker:
                draw.ellipse([margin, y + int(h*0.012), margin + int(w*0.018), y + int(h*0.012) + int(w*0.018)], fill=VIOLET)
                text_x = margin + int(w * 0.035)
            else:
                text_x = margin
            wrapped = wrap_text(draw, text, f_body, max_text_w - (text_x - margin))
            for line in wrapped:
                draw.text((text_x, y), line, font=f_body, fill=WHITE)
                bbox = draw.textbbox((0, 0), line, font=f_body)
                y += (bbox[3] - bbox[1]) + int(h * 0.012)
            y += int(h * 0.02)

    if cta:
        f_cta = ImageFont.truetype(FONT_BOLD, int(w * 0.05))
        cta_text = "Abonne-toi @ia.aujourdhui"
        draw_pill(draw, margin, h - int(h * 0.22), cta_text, f_cta, VIOLET)
        draw.text((margin, h - int(h*0.14)), "pour comprendre l'IA sans jargon", font=f_body, fill=GREY)

    draw_footer(draw, w, h, page, total, f_small)
    return img


SLIDES = [
    dict(
        kicker="Actu IA",
        title=["Depuis le 2 août, une loi change ta façon d'utiliser l'IA"],
        body=[(None, "Et presque personne n'en parle.")],
    ),
    dict(
        kicker="C'est quoi",
        title=["L'article 50 de l'AI Act"],
        body=[(None, "La loi européenne sur l'IA impose désormais"),
              (None, "aux chatbots et assistants IA de te dire"),
              (None, "clairement que tu parles à une IA.")],
    ),
    dict(
        kicker="Concrètement",
        title=["Ça touche 4 choses"],
        body=[("*", "Les chatbots et assistants vocaux (ChatGPT, Claude, Gemini...)"),
              ("*", "Les contenus générés par IA (textes, images, vidéos)"),
              ("*", "La reconnaissance d'émotions par IA"),
              ("*", "Les deepfakes et textes IA sur des sujets d'actualité")],
    ),
    dict(
        kicker="Pour toi",
        title=["Ce que tu vas voir changer"],
        body=[("*", "Plus de mentions «ceci est une IA» dans les apps"),
              ("*", "Des watermarks sur les images/vidéos générées"),
              ("*", "Des chatbots obligés de se déclarer dès le début")],
    ),
    dict(
        kicker="Sanctions",
        title=["Jusqu'à 15 millions d'euros"],
        body=[(None, "Ou 3% du chiffre d'affaires mondial pour"),
              (None, "les entreprises qui ne respectent pas la règle."),
              (None, "De quoi motiver tout le monde à jouer le jeu.")],
    ),
    dict(
        kicker="Bon à savoir",
        title=["Comment le repérer"],
        body=[("*", "Regarde les mentions en petit sous les réponses"),
              ("*", "Un badge ou watermark = contenu généré par IA"),
              ("*", "En cas de doute, demande directement à l'outil")],
    ),
    dict(
        kicker=None,
        title=["On décrypte l'IA pour toi chaque semaine"],
        body=None,
        cta=True,
    ),
]


def build_set(w, h, prefix, out_dir):
    total = len(SLIDES)
    for i, s in enumerate(SLIDES, start=1):
        img = render_slide(
            w, h, i, total,
            kicker=s["kicker"],
            title_lines=s["title"],
            body_lines=s["body"],
            cta=s.get("cta", False),
        )
        path = os.path.join(out_dir, f"{prefix}_{i}.png")
        img.save(path)
        print("saved", path)


if __name__ == "__main__":
    build_set(1080, 1350, "slide", OUT_DIR)
    build_set(1080, 1920, "tiktok", os.path.join(OUT_DIR, "tiktok"))
    print("DONE")
