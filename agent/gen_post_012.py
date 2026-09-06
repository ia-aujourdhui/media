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

OUT_DIR = "/sessions/peaceful-festive-curie/tmp/post_012_new"
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
    label = "{}/{}".format(page, total)
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
                draw.ellipse([margin, y + int(h * 0.012), margin + int(w * 0.018), y + int(h * 0.012) + int(w * 0.018)], fill=VIOLET)
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
        draw.text((margin, h - int(h * 0.14)), "l'actu IA expliquée simplement", font=f_body, fill=GREY)

    draw_footer(draw, w, h, page, total, f_small)
    return img


SLIDES = [
    dict(
        kicker="Actu IA",
        title=[u"Le nouveau modèle d'OpenAI fait peur... à OpenAI elle-même"],
        body=[(None, u"Une première dans l'histoire de la boîte.")],
    ),
    dict(
        kicker="Ce qui s'est passé",
        title=[u"GPT-6 « Astra » vient de sortir"],
        body=[("*", u"Officialisé le 1er septembre 2026 par OpenAI"),
              ("*", u"Classé « Critique » en cybersécurité"),
              ("*", u"Ce niveau n'avait jamais été atteint par un modèle avant lui")],
    ),
    dict(
        kicker="Ce qu'il sait faire n°1",
        title=[u"Trouver des failles que personne ne connaît"],
        body=[("*", u"Score parfait : 100% sur ExploitBench"),
              ("*", u"(le test qui mesure la création d'exploits)"),
              ("*", u"Sur des failles très récentes, il en a découvert 2 inédites tout seul, pendant un test interne")],
    ),
    dict(
        kicker="Ce qu'il sait faire n°2",
        title=[u"S'échapper d'un système ultra protégé"],
        body=[("*", u"Face à un navigateur verrouillé : il a construit un exploit complet et pris le contrôle de l'ordinateur"),
              ("*", u"Face à un système d'exploitation blindé : passage de simple utilisateur à administrateur")],
    ),
    dict(
        kicker="Les garde-fous",
        title=[u"OpenAI a verrouillé l'accès aux fonctions sensibles"],
        body=[("*", u"Seuls quelques testeurs triés sur le volet y ont accès au lancement"),
              ("*", u"Objectif affiché : aider les défenseurs (programme Daybreak), pas les attaquants"),
              ("*", u"Le modèle refuse 91,5% des demandes malveillantes, contre 59% pour le modèle précédent")],
    ),
    dict(
        kicker="Pourquoi ça compte",
        title=[u"La cybersécurité entre dans une nouvelle ère"],
        body=[(None, u"Une IA capable de pirater seule doit aussi savoir se contrôler seule."),
              (None, u"OpenAI a retardé la sortie plusieurs semaines pour renforcer la sécurité."),
              (None, u"Toi, ça te rassure ou ça t'inquiète plus ?")],
    ),
    dict(
        kicker=None,
        title=[u"On vulgarise l'actu IA chaque jour"],
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
        path = os.path.join(out_dir, "{}_{}.png".format(prefix, i))
        img.save(path)
        print("saved " + path)


if __name__ == "__main__":
    build_set(1080, 1350, "slide", OUT_DIR)
    build_set(1080, 1920, "tiktok", os.path.join(OUT_DIR, "tiktok"))
    print("DONE")
