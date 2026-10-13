#!/usr/bin/env python3
"""
CuddleNine — 0 to 12 Months Baby Care Guide (English)
Improved Design Version
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, white, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle,
    KeepTogether, HRFlowable, Flowable, Frame, PageTemplate, BaseDocTemplate,
    FrameBreak, NextPageTemplate
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

# ==================== COLORS ====================
PRIMARY = HexColor("#3B82F6")       # Modern blue
PRIMARY_DARK = HexColor("#1E40AF")
ACCENT = HexColor("#EC4899")        # Soft pink/magenta
ACCENT_LIGHT = HexColor("#FDF2F8")
SOFT_BLUE = HexColor("#EFF6FF")
SOFT_GREEN = HexColor("#ECFDF5")
SOFT_RED = HexColor("#FEF2F2")
SOFT_AMBER = HexColor("#FFFBEB")
DARK = HexColor("#1F2937")
MED = HexColor("#4B5563")
LIGHT = HexColor("#9CA3AF")
BG_LIGHT = HexColor("#F9FAFB")
WHITE = white
BORDER = HexColor("#E5E7EB")

# ==================== FONTS ====================
FONT_DIR = "/usr/share/fonts/SlidesCarnival/google/"
pdfmetrics.registerFont(TTFont("NotoSans", FONT_DIR + "Noto Sans/static/NotoSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NotoSans-Bold", FONT_DIR + "Noto Sans/static/NotoSans-Bold.ttf"))

PAGE_W, PAGE_H = A4
MARGIN = 0.65 * inch


class RoundedBox(Flowable):
    """Colored rounded content box"""
    def __init__(self, title, content_lines, bg_color, border_color, title_color=None, icon=""):
        Flowable.__init__(self)
        self.title = title
        self.content_lines = content_lines
        self.bg_color = bg_color
        self.border_color = border_color
        self.title_color = title_color or border_color
        self.icon = icon
        self.box_width = PAGE_W - 2 * MARGIN
        self._height = 0

    def wrap(self, availWidth, availHeight):
        self.box_width = min(self.box_width, availWidth)
        # Calculate height
        line_h = 13
        title_h = 22 if self.title else 0
        padding = 16
        self._height = title_h + len(self.content_lines) * line_h + padding
        return self.box_width, self._height

    def draw(self):
        c = self.canv
        # Background
        c.setFillColor(self.bg_color)
        c.setStrokeColor(self.border_color)
        c.setLineWidth(1.2)
        c.roundRect(0, 0, self.box_width, self._height, 6, fill=1, stroke=1)

        y = self._height - 14
        if self.title:
            c.setFillColor(self.title_color)
            c.setFont("NotoSans-Bold", 10)
            c.drawString(12, y, f"{self.icon}  {self.title}" if self.icon else self.title)
            y -= 16

        c.setFillColor(DARK)
        c.setFont("NotoSans", 9)
        for line in self.content_lines:
            c.drawString(14, y, line)
            y -= 13


class ColoredBar(Flowable):
    """Full-width colored section header"""
    def __init__(self, text, bg_color=PRIMARY, text_color=WHITE):
        Flowable.__init__(self)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.box_width = PAGE_W - 2 * MARGIN
        self._height = 28

    def wrap(self, availWidth, availHeight):
        self.box_width = min(self.box_width, availWidth)
        return self.box_width, self._height

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg_color)
        c.roundRect(0, 0, self.box_width, self._height, 5, fill=1, stroke=0)
        c.setFillColor(self.text_color)
        c.setFont("NotoSans-Bold", 11)
        c.drawCentredString(self.box_width / 2, 9, self.text)


class HeaderFooterCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for i, page in enumerate(self.pages):
            self.__dict__.update(page)
            if i > 0:  # skip cover
                self._draw_footer(i + 1, page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def _draw_footer(self, page_num, total):
        # Top thin accent line
        self.setStrokeColor(ACCENT)
        self.setLineWidth(1.5)
        self.line(MARGIN, PAGE_H - 0.4 * inch, PAGE_W - MARGIN, PAGE_H - 0.4 * inch)

        # Bottom
        self.setStrokeColor(BORDER)
        self.setLineWidth(0.6)
        self.line(MARGIN, 0.42 * inch, PAGE_W - MARGIN, 0.42 * inch)

        self.setFont("NotoSans", 8)
        self.setFillColor(LIGHT)
        self.drawString(MARGIN, 0.25 * inch, "CuddleNine  •  Little Care, Big Love")
        self.drawRightString(PAGE_W - MARGIN, 0.25 * inch, f"{page_num}  /  {total}")


def styles():
    s = getSampleStyleSheet()

    s.add(ParagraphStyle(name='CoverBrand', fontName='NotoSans-Bold', fontSize=32,
                         textColor=PRIMARY_DARK, alignment=TA_CENTER, spaceAfter=4, leading=38))
    s.add(ParagraphStyle(name='CoverTag', fontName='NotoSans', fontSize=13,
                         textColor=ACCENT, alignment=TA_CENTER, spaceAfter=10, leading=18))
    s.add(ParagraphStyle(name='CoverMain', fontName='NotoSans-Bold', fontSize=15,
                         textColor=DARK, alignment=TA_CENTER, leading=20, spaceAfter=6))
    s.add(ParagraphStyle(name='CoverDesc', fontName='NotoSans', fontSize=10,
                         textColor=MED, alignment=TA_CENTER, leading=15))

    s.add(ParagraphStyle(name='H1', fontName='NotoSans-Bold', fontSize=14,
                         textColor=PRIMARY_DARK, spaceBefore=4, spaceAfter=8, leading=18))
    s.add(ParagraphStyle(name='H2', fontName='NotoSans-Bold', fontSize=11,
                         textColor=ACCENT, spaceBefore=10, spaceAfter=4, leading=15))
    s.add(ParagraphStyle(name='Body', fontName='NotoSans', fontSize=9.5,
                         textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=5, leading=13.5))
    s.add(ParagraphStyle(name='BulletItem', fontName='NotoSans', fontSize=9,
                         textColor=DARK, leftIndent=12, spaceAfter=2.5, leading=12.5))
    s.add(ParagraphStyle(name='Small', fontName='NotoSans', fontSize=8.5,
                         textColor=MED, leading=12))
    s.add(ParagraphStyle(name='CenterSmall', fontName='NotoSans', fontSize=8,
                         textColor=LIGHT, alignment=TA_CENTER))
    s.add(ParagraphStyle(name='Warn', fontName='NotoSans-Bold', fontSize=10,
                         textColor=HexColor("#DC2626"), spaceBefore=6, spaceAfter=3, leading=13))
    s.add(ParagraphStyle(name='Tip', fontName='NotoSans-Bold', fontSize=10,
                         textColor=HexColor("#059669"), spaceBefore=6, spaceAfter=3, leading=13))
    s.add(ParagraphStyle(name='TH', fontName='NotoSans-Bold', fontSize=8.5,
                         textColor=WHITE, alignment=TA_CENTER, leading=11))
    s.add(ParagraphStyle(name='TC', fontName='NotoSans', fontSize=8,
                         textColor=DARK, leading=11))
    s.add(ParagraphStyle(name='TOCNum', fontName='NotoSans-Bold', fontSize=9.5,
                         textColor=PRIMARY))
    s.add(ParagraphStyle(name='TOCTitle', fontName='NotoSans', fontSize=9.5,
                         textColor=DARK))
    s.add(ParagraphStyle(name='TOCPage', fontName='NotoSans', fontSize=9.5,
                         textColor=ACCENT, alignment=TA_RIGHT))
    return s


def make_table(headers, rows, widths):
    st = styles()
    data = [[Paragraph(h, st['TH']) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), st['TC']) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'NotoSans-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
        ('TOPPADDING', (0, 0), (-1, 0), 7),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, SOFT_BLUE]),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
    ]))
    return t


def month_page(story, st, num, title, color, feeding, apply, sleep, milestones, activity, note=None):
    story.append(ColoredBar(f"Chapter {num}  ·  {title}", color))
    story.append(Spacer(1, 10))

    # Feeding box
    story.append(Paragraph("Feeding", st['H2']))
    for item in feeding:
        story.append(Paragraph(f"•  {item}", st['BulletItem']))

    # Apply box
    story.append(Paragraph("What to Apply / Care", st['H2']))
    for item in apply:
        story.append(Paragraph(f"•  {item}", st['BulletItem']))

    # Info row
    story.append(Spacer(1, 6))
    info_data = [
        [Paragraph(f"<b>Sleep</b><br/>{sleep}", st['Small']),
         Paragraph(f"<b>Milestones</b><br/>{milestones}", st['Small'])],
    ]
    info_t = Table(info_data, colWidths=[3.3*inch, 3.3*inch])
    info_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), SOFT_BLUE),
        ('BACKGROUND', (1, 0), (1, 0), ACCENT_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(info_t)

    story.append(Spacer(1, 6))
    story.append(Paragraph(f"<b>Activity idea:</b> {activity}", st['Body']))

    if note:
        story.append(Paragraph(f"⚠  {note}", st['Warn']))

    story.append(Spacer(1, 6))


def build():
    out = "/home/workdir/artifacts/CuddleNine_Baby_Care_Guide_English_v2.pdf"
    logo = "/home/workdir/artifacts/cuddlenine_logo.png"

    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=0.55*inch, bottomMargin=0.6*inch,
        title="CuddleNine — 0 to 12 Months Baby Care Guide",
        author="CuddleNine",
    )

    st = styles()
    story = []

    # ========== COVER ==========
    story.append(Spacer(1, 30))
    if os.path.exists(logo):
        img = Image(logo, width=2.6*inch, height=2.05*inch)
        img.hAlign = 'CENTER'
        story.append(img)

    story.append(Spacer(1, 12))
    story.append(Paragraph("CuddleNine", st['CoverBrand']))
    story.append(Paragraph("Little Care, Big Love", st['CoverTag']))
    story.append(HRFlowable(width="50%", thickness=2, color=ACCENT, spaceBefore=4, spaceAfter=14, hAlign='CENTER'))
    story.append(Paragraph("Complete 0–12 Months Baby Care Guide", st['CoverMain']))
    story.append(Paragraph(
        "A practical, step-by-step handbook for new parents.<br/>What to do, what to feed, what to apply — every month clearly explained.",
        st['CoverDesc']
    ))

    story.append(Spacer(1, 22))

    # Feature grid
    feats = [
        ["First 24 Hours Guide", "0–12 Month Feeding Plan"],
        ["Monthly Sleep Schedules", "Skincare & Hygiene Tips"],
        ["Vaccination Chart", "Red Flags & Emergencies"],
        ["5 Printable Checklists", "Parent Wellness Notes"],
    ]
    fdata = []
    for row in feats:
        fdata.append([
            Paragraph(f"●  {row[0]}", ParagraphStyle('f', fontName='NotoSans', fontSize=9, textColor=DARK, alignment=TA_CENTER)),
            Paragraph(f"●  {row[1]}", ParagraphStyle('f', fontName='NotoSans', fontSize=9, textColor=DARK, alignment=TA_CENTER)),
        ])
    ft = Table(fdata, colWidths=[3.2*inch, 3.2*inch])
    ft.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), ACCENT_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, ACCENT),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, ACCENT),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(ft)

    story.append(Spacer(1, 36))
    story.append(Paragraph(
        "© CuddleNine  ·  Educational purposes only  ·  Always consult your pediatrician",
        st['CenterSmall']
    ))
    story.append(PageBreak())

    # ========== TOC ==========
    story.append(ColoredBar("Table of Contents"))
    story.append(Spacer(1, 12))

    toc = [
        ("01", "First 24 Hours — Hour-by-Hour Guide", "3"),
        ("02", "Month 1 (0–30 Days) — Adjustment", "5"),
        ("03", "Month 2 — The Smile Month", "6"),
        ("04", "Month 3 — Communication", "7"),
        ("05", "Month 4 — Rolling Over", "8"),
        ("06", "Month 5 — Grasping", "9"),
        ("07", "Month 6 — Solids Begin!", "10"),
        ("08", "Month 7 — Real Food Taste", "11"),
        ("09", "Month 8 — Crawling", "12"),
        ("10", "Month 9 — Standing Ready", "13"),
        ("11", "Month 10 — First Steps", "14"),
        ("12", "Month 11 — Walking Practice", "15"),
        ("13", "Month 12 — Happy Birthday!", "16"),
        ("14", "Vaccination Chart", "17"),
        ("15", "Red Flags — When to Call Doctor", "18"),
        ("16", "Bonus Printable Checklists", "19"),
    ]
    tdata = []
    for num, title, pg in toc:
        tdata.append([
            Paragraph(num, st['TOCNum']),
            Paragraph(title, st['TOCTitle']),
            Paragraph(pg, st['TOCPage']),
        ])
    tt = Table(tdata, colWidths=[0.45*inch, 5.4*inch, 0.5*inch])
    tt.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW', (0, 0), (-1, -2), 0.3, BORDER),
    ]))
    story.append(tt)
    story.append(PageBreak())

    # ========== CHAPTER 1: 24 HOURS ==========
    story.append(ColoredBar("Chapter 1  ·  First 24 Hours — Hour by Hour"))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "The most important window for new parents. Follow this timeline carefully for feeding, care, and safety.",
        st['Body']
    ))

    # Hour blocks
    hours = [
        ("Hours 0–2  ·  Right After Birth", PRIMARY, [
            "Place baby skin-to-skin on mother’s chest immediately",
            "Start breastfeeding within the first hour (colostrum is pure gold)",
            "Do NOT apply powder, oil, or lotion — keep skin plain",
            "Only wipe gently with soft cotton cloth",
        ]),
        ("Hours 2–6", ACCENT, [
            "First stool is black-green meconium — completely normal",
            "Nurse measures weight, length, head size",
            "Keep umbilical cord stump dry — no oil or powder",
            "Feed every 2 hours even if baby is sleeping (wake if needed)",
        ]),
        ("Hours 6–12", PRIMARY, [
            "First urine should appear within 24 hours",
            "Dress baby in cap + mittens + socks to prevent heat loss",
            "Change diapers every 2–3 hours",
            "Avoid wet wipes — use cotton + lukewarm water only",
            "No water to drink — only breast milk or formula",
        ]),
        ("Hours 12–24", ACCENT, [
            "Watch for mild jaundice (yellow tint) — get checked if concerned",
            "Only sponge bath until cord falls off — no full tub bath",
            "Mother’s milk comes in — breasts may feel full; warm compress helps",
            "8–12 feeds in 24 hours is normal — feed on demand",
        ]),
    ]

    for title, col, items in hours:
        story.append(Spacer(1, 6))
        story.append(Paragraph(title, ParagraphStyle('ht', fontName='NotoSans-Bold', fontSize=10, textColor=col, spaceBefore=4, spaceAfter=3)))
        for it in items:
            story.append(Paragraph(f"•  {it}", st['BulletItem']))

    story.append(Spacer(1, 10))
    story.append(Paragraph("⚠  Red Flags — Call Doctor Immediately", st['Warn']))
    for rf in [
        "Difficulty breathing or unusual breathing sounds",
        "Temperature below 97°F or above 99.5°F",
        "No feed for 4+ hours",
        "No urine within 24 hours",
        "Blue lips or skin",
    ]:
        story.append(Paragraph(f"•  {rf}", st['BulletItem']))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Quick Summary", st['H2']))
    story.append(make_table(
        ["Time", "Do This", "Avoid This"],
        [
            ["0–2 hrs", "Skin-to-skin + first feed", "Powder / oil"],
            ["2–6 hrs", "Keep cord dry, feed every 2h", "Touching the stump"],
            ["6–12 hrs", "Cap, mittens, cotton wipes", "Wet wipes"],
            ["12–24 hrs", "Sponge bath, jaundice check", "Full bath or water"],
        ],
        [1.2*inch, 2.7*inch, 2.5*inch]
    ))
    story.append(PageBreak())

    # ========== MONTHS 1-6 ==========
    months1 = [
        (2, "Month 1 (0–30 Days) · Adjustment", PRIMARY,
         ["Only breast milk or formula — nothing else",
          "Feed every 2–3 hours (8–12 times/day)",
          "Never give water, honey, or glucose water"],
         ["Keep umbilical stump dry — falls off in 7–15 days",
          "First 2–3 weeks: cotton + water only (no soap)",
          "Thin zinc oxide layer for diaper rash",
          "Start oil massage after 2–3 weeks (patch test first)"],
         "16–18 hrs (wake for feeds)",
         "Eyes focus, reacts to sound, slight neck control",
         "Skin-to-skin contact and soft lullabies",
         "Check jaundice — see doctor if yellow tint lasts >24 hrs"),
        (3, "Month 2 · The Smile Month", ACCENT,
         ["Only milk — pattern settles to ~every 3 hours",
          "Mother’s diet can affect milk taste"],
         ["Start mild baby soap on alternate days",
          "Cradle cap: coconut oil 15 min then soft brush",
          "Keep nails short (babies scratch themselves)"],
         "15–16 hrs (night feeds still needed)",
         "Social smile appears! Cooing sounds begin",
         "Tummy time 2–3 minutes daily",
         "Excessive crying or feeding refusal → consult doctor"),
        (4, "Month 3 · Communication", PRIMARY,
         ["Only milk — intervals stretch to 3–4 hours",
          "Formula babies may take 90–120 ml per feed"],
         ["Daily gentle massage (afternoon preferred)",
          "Fragrance-free lotion only if skin is dry"],
         "14–16 hrs (some sleep 5–6 hrs at night)",
         "Opens/closes hands, turns to sound, first laughter",
         "Colorful toys at 20–30 cm for eye tracking",
         "Poor head control or crossed eyes → get checked"),
        (5, "Month 4 · Rolling Over", ACCENT,
         ["Only milk — baby may get distracted while feeding",
          "Feed in a quiet room if needed"],
         ["Teething may start — offer sterilized silicone teether",
          "Trim nails weekly"],
         "14–15 hrs (sleep regression common)",
         "Rolls over! Never leave alone on bed or sofa",
         "Increase tummy time to 10 min, copy sounds",
         "Start baby-proofing the house now"),
        (6, "Month 5 · Grasping", PRIMARY,
         ["Only milk — schedule more regular",
          "Ask doctor about iron drops"],
         ["No teething gel without advice — teether + massage enough",
          "Hair oil max twice a week"],
         "14 hrs · 2–3 naps",
         "Grasps objects, brings feet to mouth, stranger anxiety",
         "Rattles, high-fives, hand clapping games",
         "Weight not increasing or excessive crying → doctor"),
        (7, "Month 6 · Solids Begin!", ACCENT,
         ["First solid: rice cereal or lentil water — 1–2 spoons after milk",
          "3-day rule: one new food for 3 days to check allergy",
          "Safe: mashed banana, apple, carrot, rice, moong dal water",
          "Avoid: honey, cow’s milk, salt, sugar, whole nuts, citrus"],
         ["Finger brush with water only if teeth appearing",
          "Wipe face often during meals"],
         "14 hrs · 2 naps",
         "Sits with support, responds to name, babbling",
         "Supported sitting practice, introduce tastes slowly",
         "6-month vaccines + iron/calcium check recommended"),
    ]

    for num, title, col, feed, apply, sleep, mile, act, note in months1:
        month_page(story, st, num, title, col, feed, apply, sleep, mile, act, note)
        story.append(PageBreak())

    # ========== MONTHS 7-12 ==========
    months2 = [
        (8, "Month 7 · Real Food Taste", PRIMARY,
         ["2 meals + milk",
          "Khichdi, banana, apple, unsweetened semolina porridge",
          "Egg yolk possible (if not vegetarian) — 3-day rule",
          "Water 50–100 ml/day from a cup"],
         ["Daily finger brush with water",
          "Weekly nail care"],
         "13–14 hrs · 2 naps",
         "Sits without support, transfers objects, mama/papa sounds",
         "Pull toys, clapping games",
         None),
        (9, "Month 8 · Crawling", ACCENT,
         ["2–3 meals + milk",
          "Finger foods: steamed carrot sticks, banana pieces",
          "Wheat porridge, dalia, curd (great for digestion)"],
         ["SPF 30+ baby sunscreen when outdoors",
          "Prefer mosquito net / full sleeves over chemical sprays"],
         "13–14 hrs (naps may drop to 1)",
         "Crawling starts! Baby-proof sockets, floor, sharp corners",
         "Name objects, stacking cups, “Where is the ball?”",
         None),
        (10, "Month 9 · Standing Ready", PRIMARY,
         ["3 meals + milk (family food without chili/salt)",
          "Soft roti pieces and crumbled paneer okay"],
         ["Brush twice daily — rice-grain fluoride toothpaste (ask doctor)",
          "Hair wash twice a week"],
         "13–14 hrs · 1–2 naps",
         "Stands holding furniture, waves bye-bye, looks for hidden toys",
         "Avoid baby walkers — allow furniture cruising or push toys",
         None),
        (11, "Month 10 · First Steps", ACCENT,
         ["3 meals + 1 snack + milk",
          "Most home-cooked food okay with light seasoning",
          "Still no cow’s milk until 12 months"],
         ["Brush after night feed (milk sugar causes decay)",
          "Black spots on teeth → pediatric dentist"],
         "12–14 hrs · one nap settling",
         "Cruising sideways, first meaningful words",
         "Throw ball, name objects, show flowers",
         None),
        (12, "Month 11 · Walking Practice", PRIMARY,
         ["3 meals + 2 snacks + milk",
          "Full egg can be introduced",
          "Still avoid whole nuts, popcorn, chips, honey, juice"],
         ["4–8 teeth common — brushing twice daily non-negotiable",
          "Trim toenails too"],
         "12–13 hrs · 1 afternoon nap",
         "Walks with one-hand support, independent sit/stand",
         "Simple instructions, stacking rings",
         None),
        (13, "Month 12 · Happy Birthday!", ACCENT,
         ["Cow’s milk can start (max 300–400 ml/day)",
          "3 meals + 2 snacks — seat at family table",
          "Birthday treat: a few spoons only — avoid sugar habit"],
         ["Brush twice daily with fluoride toothpaste",
          "Daily sunscreen outdoors",
          "Full daily bath is fine"],
         "12–13 hrs · solid night sleep + 1 nap",
         "Walking! (normal range 9–16 months), 2–3 words, tries spoon",
         "Dance to rhymes, ball games, picture books",
         None),
    ]

    for num, title, col, feed, apply, sleep, mile, act, note in months2:
        month_page(story, st, num, title, col, feed, apply, sleep, mile, act, note)
        story.append(PageBreak())

    # ========== VACCINATION ==========
    story.append(ColoredBar("Chapter 14  ·  Vaccination Chart"))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Based on standard immunization schedules. Always confirm with your pediatrician — recommendations can vary by country and individual needs.",
        st['Body']
    ))
    story.append(Spacer(1, 6))
    story.append(make_table(
        ["Age", "Vaccines", "Notes"],
        [
            ["At Birth", "BCG, Hep B (birth), OPV-0", "Usually in hospital"],
            ["6 Weeks", "DTwP/DTaP-1, IPV-1, Hep B-2, Hib-1, Rota-1, PCV-1", "First major set"],
            ["10 Weeks", "DTwP/DTaP-2, IPV-2, Hib-2, Rota-2, PCV-2", ""],
            ["14 Weeks", "DTwP/DTaP-3, IPV-3, Hib-3, Rota-3, PCV-3", ""],
            ["6 Months", "Influenza-1 (optional), Hep B-3", ""],
            ["9 Months", "MMR-1, Typhoid Conjugate", ""],
            ["12 Months", "Hepatitis A-1", ""],
        ],
        [1.15*inch, 3.9*inch, 1.4*inch]
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Parent Tip", st['Tip']))
    story.append(Paragraph("• Keep baby well-rested and lightly fed on vaccine day", st['BulletItem']))
    story.append(Paragraph("• Mild fever is common — use paracetamol only as advised by doctor", st['BulletItem']))
    story.append(Paragraph("• Cool cloth on injection site can comfort the baby", st['BulletItem']))
    story.append(PageBreak())

    # ========== RED FLAGS ==========
    story.append(ColoredBar("Chapter 15  ·  Red Flags — When to Call the Doctor", HexColor("#DC2626")))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Seek medical help immediately if you notice any of these signs. Do not wait.",
        st['Body']
    ))
    story.append(Spacer(1, 6))

    flags = [
        ("Breathing Difficulty", "Fast breathing, wheezing, chest pulling in, blue lips"),
        ("High Fever", "100.4°F (38°C) or higher in a baby under 3 months"),
        ("Feeding Refusal", "Nothing eaten or drunk for 8–12 hours"),
        ("Forceful / Green Vomit", "Projectile vomiting or green/bloody vomit"),
        ("Dehydration", "Dry lips, sunken eyes, no urine 6+ hours, sunken soft spot"),
        ("Seizures", "Body jerks, eyes rolling, loss of consciousness"),
        ("Worsening Jaundice", "Yellow color spreading + baby becoming lethargic"),
        ("Umbilical Infection", "Pus, redness, foul smell, or fever around cord"),
        ("Inconsolable Crying", "Crying hard for 3+ hours, hard abdomen"),
        ("Head Injury / Fall", "Vomiting, drowsiness, or eye changes after a fall"),
    ]
    for title, desc in flags:
        story.append(Paragraph(f"<b>▶ {title}</b>  —  {desc}", st['Body']))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Keep These Numbers Ready", st['H2']))
    story.append(Paragraph("• Local emergency / ambulance number", st['BulletItem']))
    story.append(Paragraph("• Your pediatrician + nearest hospital", st['BulletItem']))
    story.append(Paragraph("• Poison control (India: 1800-116-117)", st['BulletItem']))
    story.append(PageBreak())

    # ========== BONUSES ==========
    story.append(ColoredBar("Chapter 16  ·  Bonus Printable Checklists", ACCENT))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Print these pages and keep them handy for daily tracking.", st['Body']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Feeding Tracker (One Day)", st['H2']))
    story.append(make_table(
        ["Time", "Type", "Amount / Duration", "Notes"],
        [["____:____", "☐ Breast  ☐ Formula", "________", ""],
         ["____:____", "☐ Breast  ☐ Formula", "________", ""],
         ["____:____", "☐ Breast  ☐ Formula", "________", ""],
         ["____:____", "☐ Breast  ☐ Formula", "________", ""],
         ["____:____", "☐ Breast  ☐ Formula", "________", ""],
         ["____:____", "☐ Breast  ☐ Formula", "________", ""]],
        [1.2*inch, 2.1*inch, 1.6*inch, 1.5*inch]
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("2. Newborn Shopping Checklist", st['H2']))
    for item in [
        "Clothes (bodysuits, sleepsuits, caps, mittens, socks) — 6–8 sets",
        "Newborn diapers + cotton / wipes",
        "Blankets / swaddles — 2–3",
        "Digital thermometer",
        "Nail clipper + mild soap & shampoo",
        "Zinc oxide cream + massage oil",
        "Car seat + stroller / carrier",
        "Bottles + sterilizer (if formula feeding)",
    ]:
        story.append(Paragraph(f"☐  {item}", st['BulletItem']))

    story.append(Spacer(1, 8))
    story.append(Paragraph("3. Sleep Log (One Week)", st['H2']))
    story.append(make_table(
        ["Day", "Night Sleep", "Nap 1", "Nap 2", "Total"],
        [["Mon", "____ hrs", "____", "____", "____"],
         ["Tue", "____ hrs", "____", "____", "____"],
         ["Wed", "____ hrs", "____", "____", "____"],
         ["Thu", "____ hrs", "____", "____", "____"],
         ["Fri", "____ hrs", "____", "____", "____"],
         ["Sat", "____ hrs", "____", "____", "____"],
         ["Sun", "____ hrs", "____", "____", "____"]],
        [1.0*inch, 1.3*inch, 1.2*inch, 1.2*inch, 1.1*inch]
    ))
    story.append(PageBreak())

    story.append(Paragraph("4. Vaccination Reminder", st['H2']))
    for item in [
        "Birth: BCG, Hep B, OPV-0 — Date: __________",
        "6 Weeks: __________",
        "10 Weeks: __________",
        "14 Weeks: __________",
        "6 Months: __________",
        "9 Months: __________",
        "12 Months: __________",
    ]:
        story.append(Paragraph(f"•  {item}", st['BulletItem']))

    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Emergency Contact Card", st['H2']))
    for item in [
        "Pediatrician: _________________  Phone: _______________",
        "Nearest Hospital: _________________  Phone: _______________",
        "Ambulance / Emergency: _________________",
        "Parent alternate number: _________________",
        "Family emergency contact: _________________",
        "Baby’s blood group: ________   Allergies: _______________",
    ]:
        story.append(Paragraph(f"•  {item}", st['BulletItem']))

    story.append(Spacer(1, 16))
    story.append(ColoredBar("3 Things to Remember Every Month", HexColor("#059669")))
    story.append(Spacer(1, 8))
    story.append(Paragraph("1. Follow the vaccination schedule — never skip doses", st['Body']))
    story.append(Paragraph("2. Monitor weight monthly — see doctor if not increasing", st['Body']))
    story.append(Paragraph("3. Use the 3-day rule for every new food — stop if rash, vomiting or loose stools appear", st['Body']))

    story.append(Spacer(1, 28))
    story.append(HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceBefore=4, spaceAfter=12))
    story.append(Paragraph("With CuddleNine", ParagraphStyle('b1', fontName='NotoSans-Bold', fontSize=14, textColor=PRIMARY_DARK, alignment=TA_CENTER, spaceAfter=3)))
    story.append(Paragraph("Little Care, Big Love", ParagraphStyle('b2', fontName='NotoSans', fontSize=12, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=8)))
    story.append(Paragraph(
        "May your baby’s first year be safe, happy and full of love.<br/>Every baby is unique — this guide is a starting point. Always follow your doctor’s advice.",
        ParagraphStyle('b3', fontName='NotoSans', fontSize=9, textColor=MED, alignment=TA_CENTER, leading=13)
    ))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "© CuddleNine  ·  Educational guide only  ·  Not a substitute for professional medical advice",
        st['CenterSmall']
    ))

    doc.build(story, canvasmaker=HeaderFooterCanvas)
    print(f"✅ Improved design PDF created: {out}")
    return out


if __name__ == "__main__":
    build()
