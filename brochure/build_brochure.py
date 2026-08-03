# -*- coding: utf-8 -*-
"""Genera brochure.pdf (brochure commerciale GLAUX AI) con reportlab."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
OUT = os.path.join(HERE, "brochure.pdf")

W, H = A4

BG      = colors.HexColor("#0b0d13")
SURFACE = colors.HexColor("#131722")
SURFACE2= colors.HexColor("#1a1d27")
BORDER  = colors.HexColor("#262b3d")
TEXT    = colors.HexColor("#e2e8f0")
MUTED   = colors.HexColor("#8892a4")
BLUE    = colors.HexColor("#3b82f6")
CYAN    = colors.HexColor("#38bdf8")
DARKBLUE= colors.HexColor("#0e2a4a")

MX = 18 * mm  # margine orizzontale


def wrap_text(text, font, size, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if stringWidth(trial, font, size) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def bg_fill(c, color=BG):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def footer(c, page_label):
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(MX, 12 * mm, "GLAUX AI — Advanced Cyber-Surveillance | Secure Intelligence")
    c.drawRightString(W - MX, 12 * mm, page_label)


def draw_pill(c, x, y, text, fg=CYAN, border=BORDER, bg=SURFACE, font_size=8.5):
    pad = 3.2 * mm
    tw = stringWidth(text, "Helvetica-Bold", font_size)
    w = tw + pad * 2
    h = 6.6 * mm
    c.setFillColor(bg)
    c.setStrokeColor(border)
    c.roundRect(x, y, w, h, h / 2, fill=1, stroke=1)
    c.setFillColor(fg)
    c.setFont("Helvetica-Bold", font_size)
    c.drawString(x + pad, y + h / 2 - font_size * 0.36, text)
    return w


def card(c, x, y, w, h, title, body_lines, icon=None, accent=CYAN, title_size=12, body_size=9.2):
    c.setFillColor(SURFACE)
    c.setStrokeColor(BORDER)
    c.roundRect(x, y, w, h, 3 * mm, fill=1, stroke=1)
    # barra accento in alto (al posto di un'icona: i font base non supportano emoji)
    c.setFillColor(accent)
    c.roundRect(x, y + h - 2.2 * mm, 14 * mm, 2.2 * mm, 1.1 * mm, fill=1, stroke=0)
    ty = y + h - 9 * mm
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", title_size)
    c.drawString(x + 6 * mm, ty - 6.5 * mm, title)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", body_size)
    ly = ty - 13 * mm
    for line in body_lines:
        c.drawString(x + 6 * mm, ly, "•  " + line)
        ly -= 5.2 * mm


def make_pdf():
    c = canvas.Canvas(OUT, pagesize=A4)

    # ---------------- PAGE 1 — Copertina ----------------
    bg_fill(c)
    # bagliore superiore
    c.setFillColor(DARKBLUE)
    c.circle(W / 2, H - 20 * mm, 90 * mm, fill=1, stroke=0)
    bg_fill(c)  # overlay base per attenuare (finto radial) -> ridisegna sotto, poi logo sopra
    c.setFillColor(DARKBLUE)
    c.circle(W / 2, H - 40 * mm, 70 * mm, fill=1, stroke=0)

    try:
        owl = ImageReader(os.path.join(ASSETS, "owl.png"))
        iw, ih = owl.getSize()
        disp_h = 46 * mm
        disp_w = disp_h * iw / ih
        c.drawImage(owl, W / 2 - disp_w / 2, H - 92 * mm, width=disp_w, height=disp_h, mask="auto")
    except Exception:
        pass

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(W / 2, H - 108 * mm, "GLAUX AI")
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, H - 115 * mm, "ADVANCED CYBER-SURVEILLANCE  |  SECURE INTELLIGENCE")

    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 17)
    lines = wrap_text("La videosorveglianza che pensa, non solo registra", "Helvetica-Bold", 17, W - 2 * MX - 20*mm)
    yy = H - 132 * mm
    for ln in lines:
        c.drawCentredString(W / 2, yy, ln)
        yy -= 7.5 * mm

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 10.5)
    lead = ("Sistema di videosorveglianza intelligente, multi-modalita, 100% offline: rileva rapine, "
            "intrusioni, cadute, incendi e situazioni di pericolo in tempo reale, elaborando tutto "
            "localmente e accelerando l'analisi via GPU.")
    yy -= 4 * mm
    for ln in wrap_text(lead, "Helvetica", 10.5, W - 2*MX - 30*mm):
        c.drawCentredString(W / 2, yy, ln)
        yy -= 5.4 * mm

    # pill badges
    badges = ["AI on-device", "Accelerazione GPU", "Nessun video nel cloud", "Auto-ritaratura"]
    total_w = sum(stringWidth(b, "Helvetica-Bold", 8.5) + 6.4*mm for b in badges) + (len(badges)-1)*3*mm
    bx = W/2 - total_w/2
    by = yy - 10*mm
    for b in badges:
        bw = draw_pill(c, bx, by, b)
        bx += bw + 3*mm

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8.5)
    c.drawCentredString(W / 2, 20 * mm, "Brochure commerciale")
    footer(c, "1 / 3")
    c.showPage()

    # ---------------- PAGE 2 — Modalita operative ----------------
    bg_fill(c)
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MX, H - 22 * mm, "MODALITA OPERATIVE")
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MX, H - 30 * mm, "Una piattaforma, cinque modalita di protezione")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9.5)
    c.drawString(MX, H - 36 * mm, "Attivabili singolarmente dalla dashboard, in base al contesto: negozio, casa, struttura, nido.")

    modes = [
        ("!", "Anti-rapina", CYAN, [
            "Rilevamento armi da fuoco e da taglio",
            "Riconoscimento azioni violente (pose/scheletro)",
            "Riconoscimento vocale delle minacce (italiano)",
            "Verifica con AI esterna prima dell'allarme",
        ]),
        ("#", "Anti-intrusione", BLUE, [
            "Ritardo di armamento configurabile",
            "PIN di sicurezza per armare/disarmare",
            "Ritardo prima dell'invio dell'allarme",
            "Filtro anti-falsi-positivi (quadri, poster, foto)",
        ]),
        ("+", "Vigilanza anziani", CYAN, [
            "Rilevamento cadute e immobilita prolungata",
            "Riconoscimento gesti di richiesta d'aiuto",
            "Rilevamento movimento agitato (panico)",
            "Fusione con l'audio (grida, malore)",
        ]),
        ("*", "Baby monitor", BLUE, [
            "Caduta o immobilita prolungata",
            "Uscita dall'inquadratura (culla/stanza)",
            "Vicinanza ad acqua o fiamme",
            "Pianto rilevato acusticamente",
        ]),
        ("^", "Anti-incendio", CYAN, [
            "Analisi colore (YCrCb + HSV) anti-falsi-positivi",
            "Modello AI dedicato fuoco/fumo",
            "Abbinabile a qualsiasi altra modalita",
            "Auto-ritaratura sulla sensibilita",
        ]),
        ("=", "Controllo totale", BLUE, [
            "Dashboard web multi-camera in tempo reale",
            "Accesso protetto da password",
            "Storico eventi esportabile (Excel)",
            "Interruttore generale: nessun alert quando non serve",
        ]),
    ]

    col_w = (W - 2 * MX - 8 * mm) / 2
    card_h = 46 * mm
    gap_y = 6 * mm
    top = H - 44 * mm
    for i, (icon, title, accent, body) in enumerate(modes):
        col = i % 2
        row = i // 2
        x = MX + col * (col_w + 8 * mm)
        y = top - card_h - row * (card_h + gap_y)
        card(c, x, y, col_w, card_h, title, body, icon=icon, accent=accent, title_size=11.5, body_size=8.4)

    footer(c, "2 / 3")
    c.showPage()

    # ---------------- PAGE 3 — Perche + Come funziona + Contatti ----------------
    bg_fill(c)
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MX, H - 22 * mm, "PERCHE GLAUX AI")
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MX, H - 30 * mm, "Progettato per essere affidabile, non solo intelligente")

    whys = [
        ("Offline-first", "L'elaborazione video avviene in locale: nessun flusso continuo verso il cloud. La verifica AI esterna, se attivata, e opzionale e usata solo per confermare un allarme."),
        ("Si auto-ritara", "Ogni modalita impara dai propri falsi positivi: se l'AI di verifica smentisce ripetutamente un allarme, la sensibilita si alza, e si abbassa quando l'ambiente si stabilizza."),
        ("Accelerato via GPU", "Analisi in tempo reale su hardware NVIDIA, con modelli YOLOv8 condivisi tra le modalita per non sprecare risorse."),
        ("Multi-camera, multi-modalita", "Fino a 10 camere, ciascuna con audio dedicato, gestite da un'unica dashboard con notifiche push, email e webhook."),
    ]
    col_w2 = (W - 2 * MX - 8 * mm) / 2
    why_h = 30 * mm
    top2 = H - 36 * mm
    for i, (title, body) in enumerate(whys):
        col = i % 2
        row = i // 2
        x = MX + col * (col_w2 + 8 * mm)
        y = top2 - why_h - row * (why_h + 5 * mm)
        c.setFillColor(SURFACE)
        c.setStrokeColor(BORDER)
        c.roundRect(x, y, col_w2, why_h, 3 * mm, fill=1, stroke=1)
        c.setFillColor(CYAN)
        c.setFont("Helvetica-Bold", 10.5)
        c.drawString(x + 6 * mm, y + why_h - 8 * mm, title)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8.3)
        yy = y + why_h - 14 * mm
        for ln in wrap_text(body, "Helvetica", 8.3, col_w2 - 12 * mm):
            c.drawString(x + 6 * mm, yy, ln)
            yy -= 4.6 * mm

    # Come funziona
    steps_top = top2 - 2*why_h - 5*mm - 14*mm
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MX, steps_top, "COME FUNZIONA")
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MX, steps_top - 7*mm, "Dall'installazione al primo allarme")

    steps = [
        "Collega le camere che hai gia (RTSP, webcam locale o stream cloud).",
        "Scegli la modalita dalla dashboard, anche in combinazione con l'anti-incendio.",
        "Un rilevamento sospetto viene verificato prima di generare una notifica.",
        "Ricevi la notifica ovunque: push (ntfy), email o webhook, con immagini dell'evento.",
    ]
    sy = steps_top - 16*mm
    for i, s in enumerate(steps, start=1):
        c.setFillColor(BLUE)
        c.circle(MX + 3*mm, sy - 1.2*mm, 3.4*mm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawCentredString(MX + 3*mm, sy - 3.1*mm, str(i))
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 9)
        c.drawString(MX + 9*mm, sy - 2.6*mm, s)
        sy -= 7.2*mm

    # CTA band
    cta_h = 28 * mm
    cta_y = 22 * mm
    c.setFillColor(DARKBLUE)
    c.roundRect(MX, cta_y, W - 2*MX, cta_h, 4*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(W/2, cta_y + cta_h - 9*mm, "Porta l'intelligenza artificiale nella tua sicurezza")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W/2, cta_y + cta_h - 15*mm, "Richiedi una demo personalizzata sulle tue camere.")
    c.setFillColor(CYAN)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(W/2, cta_y + cta_h - 22*mm, "www.glauxai.it")

    footer(c, "3 / 3")
    c.showPage()

    c.save()
    print(f"OK: {OUT}")


if __name__ == "__main__":
    make_pdf()
