#!/usr/bin/env python3
"""
CuddleNine — 0 to 12 Months Baby Care Guide (English Version)
Premium PDF E-book Generator
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle,
    KeepTogether, ListFlowable, ListItem, Flowable, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import os

# ==================== COLORS ====================
DARK_BLUE = HexColor("#4A90D9")
PINK = HexColor("#F48FB1")
SOFT_PINK = HexColor("#FCE4EC")
SOFT_BLUE = HexColor("#E3F2FD")
DARK_GRAY = HexColor("#333333")
MED_GRAY = HexColor("#555555")
LIGHT_GRAY = HexColor("#F5F5F5")
WARNING_RED = HexColor("#E53935")
TIP_GREEN = HexColor("#43A047")
GOLD = HexColor("#FFB300")
WHITE = white

# ==================== FONTS ====================
FONT_DIR = "/usr/share/fonts/SlidesCarnival/google/"
pdfmetrics.registerFont(TTFont("NotoSans", FONT_DIR + "Noto Sans/static/NotoSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NotoSans-Bold", FONT_DIR + "Noto Sans/static/NotoSans-Bold.ttf"))

# ==================== PAGE SETUP ====================
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 0.7 * inch

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
            self.draw_header_footer(i + 1, page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_header_footer(self, page_num, page_count):
        if page_num == 1:  # Skip cover
            return
        # Footer
        self.setStrokeColor(PINK)
        self.setLineWidth(0.5)
        self.line(MARGIN, 0.45 * inch, PAGE_WIDTH - MARGIN, 0.45 * inch)
        
        self.setFont("NotoSans", 8)
        self.setFillColor(MED_GRAY)
        self.drawString(MARGIN, 0.28 * inch, "CuddleNine  •  Little Care, Big Love")
        self.drawRightString(PAGE_WIDTH - MARGIN, 0.28 * inch, f"{page_num} / {page_count}")


def create_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='CoverTitle',
        fontName='NotoSans-Bold',
        fontSize=28,
        textColor=DARK_BLUE,
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=34
    ))
    
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        fontName='NotoSans',
        fontSize=14,
        textColor=PINK,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=20
    ))
    
    styles.add(ParagraphStyle(
        name='ChapterTitle',
        fontName='NotoSans-Bold',
        fontSize=18,
        textColor=DARK_BLUE,
        spaceBefore=12,
        spaceAfter=10,
        leading=24
    ))
    
    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontName='NotoSans-Bold',
        fontSize=12,
        textColor=PINK,
        spaceBefore=10,
        spaceAfter=6,
        leading=16
    ))
    
    styles.add(ParagraphStyle(
        name='BodyEng',
        fontName='NotoSans',
        fontSize=10,
        textColor=DARK_GRAY,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=14,
        firstLineIndent=0
    ))
    
    styles.add(ParagraphStyle(
        name='BodyCenter',
        fontName='NotoSans',
        fontSize=10,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=14
    ))
    
    styles.add(ParagraphStyle(
        name='BulletText',
        fontName='NotoSans',
        fontSize=9.5,
        textColor=DARK_GRAY,
        leftIndent=15,
        spaceAfter=3,
        leading=13
    ))
    
    styles.add(ParagraphStyle(
        name='WarningTitle',
        fontName='NotoSans-Bold',
        fontSize=11,
        textColor=WARNING_RED,
        spaceBefore=8,
        spaceAfter=4,
        leading=15
    ))
    
    styles.add(ParagraphStyle(
        name='TipTitle',
        fontName='NotoSans-Bold',
        fontSize=11,
        textColor=TIP_GREEN,
        spaceBefore=8,
        spaceAfter=4,
        leading=15
    ))
    
    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='NotoSans-Bold',
        fontSize=9,
        textColor=WHITE,
        alignment=TA_CENTER,
        leading=12
    ))
    
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='NotoSans',
        fontSize=8.5,
        textColor=DARK_GRAY,
        leading=12
    ))
    
    return styles


def add_header_bar(story, text, bg_color=DARK_BLUE):
    """Add a colored header bar"""
    data = [[Paragraph(text, ParagraphStyle(
        'HeaderBar',
        fontName='NotoSans-Bold',
        fontSize=13,
        textColor=WHITE,
        alignment=TA_CENTER,
        leading=17
    ))]]
    t = Table(data, colWidths=[PAGE_WIDTH - 2 * MARGIN])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))


def create_info_table(headers, rows, col_widths):
    styles = create_styles()
    data = [[Paragraph(h, styles['TableHeader']) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), styles['TableCell']) for c in row])
    
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_commands = [
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'NotoSans-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, SOFT_BLUE]),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
    ]
    t.setStyle(TableStyle(style_commands))
    return t


def build_pdf():
    output_path = "/home/workdir/artifacts/CuddleNine_Baby_Care_Guide_English.pdf"
    logo_path = "/home/workdir/artifacts/cuddlenine_logo.png"
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=0.6 * inch,
        bottomMargin=0.7 * inch,
        title="CuddleNine — 0 to 12 Months Baby Care Guide",
        author="CuddleNine",
        subject="Complete Baby Care Guide for New Parents",
    )
    
    styles = create_styles()
    story = []
    
    # ========== COVER PAGE ==========
    story.append(Spacer(1, 40))
    
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2.8*inch, height=2.2*inch)
        logo.hAlign = 'CENTER'
        story.append(logo)
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("CuddleNine", styles['CoverTitle']))
    story.append(Paragraph("Little Care, Big Love", styles['CoverSubtitle']))
    story.append(Spacer(1, 10))
    
    # Decorative line
    story.append(HRFlowable(width="60%", thickness=2, color=PINK, spaceBefore=5, spaceAfter=15, hAlign='CENTER'))
    
    story.append(Paragraph(
        "<b>Complete 0 to 12 Months Baby Care Guide</b>",
        ParagraphStyle('CoverMain', fontName='NotoSans-Bold', fontSize=16, textColor=DARK_BLUE, alignment=TA_CENTER, leading=22)
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "A practical step-by-step guide for new parents<br/>What to do, what to feed, what to apply — every month explained in detail",
        ParagraphStyle('CoverDesc', fontName='NotoSans', fontSize=11, textColor=MED_GRAY, alignment=TA_CENTER, leading=16)
    ))
    
    story.append(Spacer(1, 30))
    
    # Feature boxes on cover
    features = [
        ["🕐 First 24 Hours Hour-by-Hour Guide", "🍼 0–12 Months Feeding Plan"],
        ["😴 Sleep Schedule Every Month", "🧴 Skincare & Hygiene Tips"],
        ["💉 Vaccination Chart", "⚠️ Red Flags & Emergencies"],
        ["🎁 5 Printable Bonus Checklists", "❤️ Parent Mental Health"],
    ]
    
    feat_data = []
    for row in features:
        feat_data.append([
            Paragraph(row[0], ParagraphStyle('Feat', fontName='NotoSans', fontSize=9, textColor=DARK_GRAY, alignment=TA_CENTER)),
            Paragraph(row[1], ParagraphStyle('Feat', fontName='NotoSans', fontSize=9, textColor=DARK_GRAY, alignment=TA_CENTER)),
        ])
    
    feat_table = Table(feat_data, colWidths=[3.2*inch, 3.2*inch])
    feat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), SOFT_PINK),
        ('BOX', (0, 0), (-1, -1), 1, PINK),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, PINK),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(feat_table)
    
    story.append(Spacer(1, 40))
    story.append(Paragraph(
        "© CuddleNine  •  For Educational Purposes  •  Always Consult Your Pediatrician",
        ParagraphStyle('Disclaimer', fontName='NotoSans', fontSize=8, textColor=MED_GRAY, alignment=TA_CENTER)
    ))
    
    story.append(PageBreak())
    
    # ========== TABLE OF CONTENTS ==========
    add_header_bar(story, "📚 Table of Contents")
    
    toc_items = [
        ("1.", "First 24 Hours — Hour-by-Hour Guide", "3"),
        ("2.", "Month 1 (0–30 Days) — The Adjustment Month", "5"),
        ("3.", "Month 2 — The Smile Month", "6"),
        ("4.", "Month 3 — The Communication Month", "7"),
        ("5.", "Month 4 — The Rolling Month", "8"),
        ("6.", "Month 5 — The Grasping Month", "9"),
        ("7.", "Month 6 — Solids Start! 🎉", "10"),
        ("8.", "Month 7 — Real Taste of Food", "11"),
        ("9.", "Month 8 — The Crawling Month", "12"),
        ("10.", "Month 9 — Getting Ready to Stand", "13"),
        ("11.", "Month 10 — The Steps Month", "14"),
        ("12.", "Month 11 — Walking Practice", "15"),
        ("13.", "Month 12 — Happy Birthday! Walking Month", "16"),
        ("14.", "Vaccination Chart", "17"),
        ("15.", "⚠️ Red Flags — When to See a Doctor", "18"),
        ("16.", "🎁 Bonus Checklists", "19"),
    ]
    
    toc_data = []
    for num, title, page in toc_items:
        toc_data.append([
            Paragraph(num, ParagraphStyle('TocNum', fontName='NotoSans-Bold', fontSize=10, textColor=DARK_BLUE)),
            Paragraph(title, ParagraphStyle('TocTitle', fontName='NotoSans', fontSize=10, textColor=DARK_GRAY)),
            Paragraph(page, ParagraphStyle('TocPage', fontName='NotoSans', fontSize=10, textColor=PINK, alignment=TA_RIGHT)),
        ])
    
    toc_table = Table(toc_data, colWidths=[0.4*inch, 5.5*inch, 0.5*inch])
    toc_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LINEBELOW', (0, 0), (-1, -2), 0.3, HexColor("#EEEEEE")),
    ]))
    story.append(toc_table)
    
    story.append(PageBreak())
    
    # ========== CHAPTER 1: FIRST 24 HOURS ==========
    add_header_bar(story, "🕐 Chapter 1: First 24 Hours — Hour-by-Hour Guide", DARK_BLUE)
    
    story.append(Paragraph(
        "The most critical time for new parents. This guide tells you exactly what to do, what to apply, and what to feed right after delivery.",
        styles['BodyEng']
    ))
    story.append(Spacer(1, 8))
    
    # Hour 0-2
    story.append(Paragraph("⏰ Hours 0–2 (Immediately After Delivery)", styles['SectionTitle']))
    story.append(Paragraph("<b>What happens:</b>", styles['BodyEng']))
    story.append(Paragraph("• Baby is placed on mother’s chest (skin-to-skin) — this is the most important first step", styles['BulletText']))
    story.append(Paragraph("• Nurse cleans the baby gently", styles['BulletText']))
    story.append(Paragraph("• First feed (colostrum) — <b>breastfeeding should start within the first hour</b>", styles['BulletText']))
    
    story.append(Paragraph("<b>🧴 What to apply:</b>", styles['BodyEng']))
    story.append(Paragraph("• <b>Nothing!</b> Newborn skin should stay plain — no powder, oil, or lotion", styles['BulletText']))
    story.append(Paragraph("• Only gently wipe with a soft cotton cloth", styles['BulletText']))
    
    story.append(Paragraph("<b>🍼 What to feed:</b>", styles['BodyEng']))
    story.append(Paragraph("• Only mother’s first milk (colostrum) — yellowish, thin, and extremely powerful", styles['BulletText']))
    story.append(Paragraph("• Formula only if doctor specifically advises", styles['BulletText']))
    
    story.append(Spacer(1, 6))
    
    # Hour 2-6
    story.append(Paragraph("⏰ Hours 2–6", styles['SectionTitle']))
    story.append(Paragraph("<b>What happens:</b>", styles['BodyEng']))
    story.append(Paragraph("• Baby’s first diaper — first stool is “meconium” (black-green) — this is <b>completely normal</b>", styles['BulletText']))
    story.append(Paragraph("• Nurse measures baby — weight, length, head circumference", styles['BulletText']))
    story.append(Paragraph("• Mother needs rest", styles['BulletText']))
    
    story.append(Paragraph("<b>🧴 What to apply:</b>", styles['BodyEng']))
    story.append(Paragraph("• Umbilical cord stump — <b>keep dry, no oil or powder</b>", styles['BulletText']))
    story.append(Paragraph("• Fold diaper below the stump so it stays dry", styles['BulletText']))
    
    story.append(Paragraph("<b>🍼 What to feed:</b>", styles['BodyEng']))
    story.append(Paragraph("• Feed every <b>2 hours</b> — even if baby is sleeping", styles['BulletText']))
    story.append(Paragraph("• Wake the baby for feeds in the first 24 hours (very important)", styles['BulletText']))
    
    story.append(Spacer(1, 6))
    
    # Hour 6-12
    story.append(Paragraph("⏰ Hours 6–12", styles['SectionTitle']))
    story.append(Paragraph("<b>What happens:</b>", styles['BodyEng']))
    story.append(Paragraph("• Baby’s first urine — should happen within 24 hours", styles['BulletText']))
    story.append(Paragraph("• Body temperature can drop — put on <b>cap + mittens + socks</b>", styles['BulletText']))
    story.append(Paragraph("• Baby sleeps a lot — this is normal", styles['BulletText']))
    
    story.append(Paragraph("<b>🧴 What to apply:</b>", styles['BodyEng']))
    story.append(Paragraph("• Cotton nappies or diapers — change every 2–3 hours", styles['BulletText']))
    story.append(Paragraph("• Avoid wet wipes — use only <b>cotton + lukewarm water</b> for the first 15–20 days", styles['BulletText']))
    
    story.append(Paragraph("<b>🍼 What to feed:</b>", styles['BodyEng']))
    story.append(Paragraph("• Only breast milk — <b>no water</b> (do not give water before 6 months)", styles['BulletText']))
    story.append(Paragraph("• Formula babies: sterilized bottle, room-temperature milk", styles['BulletText']))
    
    story.append(PageBreak())
    
    # Hour 12-24
    story.append(Paragraph("⏰ Hours 12–24", styles['SectionTitle']))
    story.append(Paragraph("<b>What happens:</b>", styles['BodyEng']))
    story.append(Paragraph("• Baby may look a little yellow — this can be physiological jaundice — get it checked by doctor", styles['BulletText']))
    story.append(Paragraph("• No full bath yet — only <b>sponge bath</b> until the cord falls off", styles['BulletText']))
    story.append(Paragraph("• Mother’s milk starts coming in — breasts may feel hard — warm compress helps", styles['BulletText']))
    
    story.append(Paragraph("<b>🧴 What to apply:</b>", styles['BodyEng']))
    story.append(Paragraph("• For sponge bath: lukewarm water + soft cotton towel", styles['BulletText']))
    story.append(Paragraph("• Nothing on the umbilical stump — keep it dry and clean", styles['BulletText']))
    story.append(Paragraph("• Avoid baby lotion/oil in the first 24 hours (skin is very sensitive)", styles['BulletText']))
    
    story.append(Paragraph("<b>🍼 What to feed:</b>", styles['BodyEng']))
    story.append(Paragraph("• 8–12 feeds are normal — feed on demand", styles['BulletText']))
    story.append(Paragraph("• Formula: 30–60 ml every 3 hours (as per doctor’s advice)", styles['BulletText']))
    
    story.append(Spacer(1, 10))
    
    # Red flags box
    story.append(Paragraph("⚠️ RED FLAGS — Call Doctor Immediately:", styles['WarningTitle']))
    red_flags = [
        "Baby is struggling to breathe or making unusual breathing sounds",
        "Body temperature below 97°F or above 99.5°F",
        "Baby has not fed for 4+ hours",
        "No urine within 24 hours",
        "Skin or lips turning blue",
    ]
    for rf in red_flags:
        story.append(Paragraph(f"• {rf}", styles['BulletText']))
    
    story.append(Spacer(1, 12))
    
    # Summary table
    story.append(Paragraph("📋 Summary Table — First 24 Hours", styles['SectionTitle']))
    
    summary_headers = ["Time", "What to Do", "What NOT to Do"]
    summary_rows = [
        ["0–2 hrs", "Skin-to-skin + first feed", "Apply powder or oil"],
        ["2–6 hrs", "Keep cord dry, feed every 2 hrs", "Touch the stump with diaper"],
        ["6–12 hrs", "Cap + mittens, wipe with cotton", "Use wet wipes"],
        ["12–24 hrs", "Sponge bath, check jaundice", "Full bath or give water"],
    ]
    
    story.append(create_info_table(summary_headers, summary_rows, [1.3*inch, 2.6*inch, 2.5*inch]))
    
    story.append(PageBreak())
    
    # ========== MONTHLY CHAPTERS ==========
    
    months_data = [
        {
            "title": "Month 1 (0–30 Days) — The Adjustment Month",
            "color": DARK_BLUE,
            "feeding": [
                "Only breast milk or formula — nothing else",
                "Feed every 2–3 hours — 8–12 times a day",
                "No water, honey, or glucose water (honey can be dangerous for infants)",
            ],
            "apply": [
                "Umbilical stump: Keep dry, apply nothing — it usually falls off in 7–15 days",
                "Skin: For first 2–3 weeks, only cotton + water — avoid soap",
                "Diaper area: Wipe with cotton cloth; use thin layer of zinc oxide cream if rash appears",
                "Massage: Start after 2–3 weeks — sesame or coconut oil (do a patch test first)",
            ],
            "sleep": "16–18 hours — but wake every 2 hours for feeds",
            "milestones": "Eyes begin to focus, reacts to sound, slight neck control",
            "warning": "Check for jaundice (yellow skin/eyes) — see doctor if it lasts more than 24 hours",
            "activity": "Increase skin-to-skin contact, sing soft lullabies",
        },
        {
            "title": "Month 2 — The Smile Month",
            "color": PINK,
            "feeding": [
                "Only milk — feeding pattern starts settling (every 3 hours)",
                "Mother’s diet affects milk taste — avoid heavy onion and garlic if possible",
            ],
            "apply": [
                "Start gentle baby soap (alternate days, e.g., Wednesday & Saturday)",
                "Cradle cap (flaky scalp): Apply coconut oil for 15 minutes, then gently brush",
                "Keep nails trimmed (babies scratch themselves)",
            ],
            "sleep": "15–16 hours — night feeds still needed",
            "milestones": "🎉 Social smile appears! Cooing sounds (goo-goo)",
            "warning": "Excessive crying or feeding refusal — consult doctor",
            "activity": "Start tummy time 2–3 minutes daily — strengthens neck",
        },
        {
            "title": "Month 3 — The Communication Month",
            "color": DARK_BLUE,
            "feeding": [
                "Only milk — intervals stretch to 3–4 hours",
                "Formula babies may take 90–120 ml per feed",
            ],
            "apply": [
                "Daily massage around 3–4 pm (daytime) — gentle exercises for tummy, arms, legs",
                "Face cream only if skin is dry — use fragrance-free baby lotion",
            ],
            "sleep": "14–16 hours — some babies sleep 5–6 hours at night",
            "milestones": "Opens and closes hands, turns toward rattle sounds, first laughter!",
            "warning": "Poor head control or crossed eyes — get checked",
            "activity": "Show colorful toys 20–30 cm away (eye-tracking practice)",
        },
        {
            "title": "Month 4 — The Rolling Month",
            "color": PINK,
            "feeding": [
                "Only milk — baby may get distracted while feeding (looks around) — feed in a quiet room",
            ],
            "apply": [
                "Teething may start (extra drooling, putting things in mouth) — offer sterilized silicone teether",
                "Trim nails every week with a baby nail clipper",
            ],
            "sleep": "14–15 hours — sleep regression is common (night waking) — usually settles in 2–3 weeks",
            "milestones": "🎉 Rolls over! (tummy to back / back to tummy) — never leave baby alone on bed",
            "warning": "After rolling starts, constant supervision is essential — begin baby-proofing",
            "activity": "Increase tummy time to 10 minutes, copy “ah-oo” sounds",
        },
        {
            "title": "Month 5 — The Grasping Month",
            "color": DARK_BLUE,
            "feeding": [
                "Only milk — schedule becomes more regular",
                "Iron stores start depleting — ask doctor about iron drops",
            ],
            "apply": [
                "No teething gel without doctor’s advice — teether + gentle gum massage is enough",
                "Hair oil maximum twice a week (too much causes dandruff)",
            ],
            "sleep": "14 hours — 2–3 naps during the day",
            "milestones": "Grasps objects, brings feet to mouth, stranger anxiety may begin",
            "warning": "Weight not increasing or excessive crying — consult doctor",
            "activity": "Give rattles, practice high-fives and hand clapping",
        },
        {
            "title": "Month 6 — Solids Begin! 🎉",
            "color": PINK,
            "feeding": [
                "First solid: lentil water or rice cereal — 1–2 spoons in the morning after milk",
                "3-day rule: Introduce one new food for 3 days to check for allergy",
                "Safe foods: Moong dal water, mashed banana, apple puree, carrot puree, rice",
                "Avoid: Honey (dangerous), cow’s milk (not yet), salt, sugar, whole dry fruits, citrus",
            ],
            "apply": [
                "If teeth are coming: Use finger brush with water only",
                "Wipe face frequently during meals — leftover food can irritate skin",
            ],
            "sleep": "14 hours — 2 naps",
            "milestones": "Sits with support, turns when name is called, babbling (“ba-ba”, “da-da”)",
            "warning": "6-month vaccination + iron/calcium drops — doctor visit is important",
            "activity": "Supported sitting practice, introduce new tastes slowly",
        },
    ]
    
    for i, month in enumerate(months_data):
        add_header_bar(story, f"🍼 Chapter {i+2}: {month['title']}", month['color'])
        
        story.append(Paragraph("🍼 Feeding (What to Feed):", styles['SectionTitle']))
        for item in month['feeding']:
            story.append(Paragraph(f"• {item}", styles['BulletText']))
        
        story.append(Paragraph("🧴 What to Apply:", styles['SectionTitle']))
        for item in month['apply']:
            story.append(Paragraph(f"• {item}", styles['BulletText']))
        
        story.append(Paragraph(f"<b>😴 Sleep:</b> {month['sleep']}", styles['BodyEng']))
        story.append(Paragraph(f"<b>👶 Milestones:</b> {month['milestones']}", styles['BodyEng']))
        story.append(Paragraph(f"<b>🎯 Activity:</b> {month['activity']}", styles['BodyEng']))
        
        if month.get('warning'):
            story.append(Paragraph(f"⚠️ <b>Note:</b> {month['warning']}", styles['WarningTitle']))
        
        story.append(Spacer(1, 8))
        if i < len(months_data) - 1:
            story.append(PageBreak())
    
    story.append(PageBreak())
    
    # Months 7-12
    months_data_2 = [
        {
            "title": "Month 7 — Real Taste of Food",
            "color": DARK_BLUE,
            "feeding": [
                "Now 2 meals + milk",
                "Khichdi (mashed dal-rice), banana, apple, semolina porridge (no sugar)",
                "Egg yolk can be introduced (if not vegetarian) — follow 3-day rule",
                "Water: 50–100 ml per day (start offering from a cup)",
            ],
            "apply": [
                "Brush teeth daily with finger brush and water",
                "Nail care once a week",
            ],
            "sleep": "13–14 hours — 2 naps",
            "milestones": "Sits without support, transfers objects from one hand to another, “mama-papa” type sounds",
            "activity": "Pull toys on string, practice clapping",
        },
        {
            "title": "Month 8 — The Crawling Month",
            "color": PINK,
            "feeding": [
                "2–3 meals + milk — introduce finger foods: steamed carrot sticks, banana pieces (self-feeding practice)",
                "Wheat porridge, dalia, curd (excellent probiotic for digestion)",
            ],
            "apply": [
                "Sunscreen! Baby goes outside now — SPF 30+ baby sunscreen (avoid 10 am–4 pm peak sun)",
                "Mosquito protection — prefer net or full sleeves over chemical repellents",
            ],
            "sleep": "13–14 hours — naps may reduce from 2 to 1",
            "milestones": "🎉 Crawling begins! Baby-proof the house: socket covers, clear floor, soft corners on tables",
            "activity": "Play “Where is the ball?”, name objects, stacking cups",
        },
        {
            "title": "Month 9 — Getting Ready to Stand",
            "color": DARK_BLUE,
            "feeding": [
                "3 meals + milk (family food without chili/salt, served separately)",
                "Soft roti pieces can be offered",
                "Crumbled paneer for protein",
            ],
            "apply": [
                "Toothbrushing twice daily — rice-grain size fluoride toothpaste (ask doctor first)",
                "Hair wash twice a week",
            ],
            "sleep": "13–14 hours — 1–2 naps",
            "milestones": "Tries to stand holding furniture, waves bye-bye, object permanence (looks for hidden toys — play peekaboo!)",
            "activity": "Avoid baby walkers (can affect posture) — allow standing with furniture or push walker",
        },
        {
            "title": "Month 10 — The Steps Month",
            "color": PINK,
            "feeding": [
                "3 meals + 1 snack + milk",
                "Almost everything cooked at home — light turmeric and cumin is okay",
                "Still avoid cow’s milk — continue breast milk/formula until 1 year",
            ],
            "apply": [
                "Brush after night feed (milk sugar can cause tooth decay)",
                "Check for cavities: black spots on teeth → see pediatric dentist",
            ],
            "sleep": "12–14 hours — one nap starts settling",
            "milestones": "🎉 Cruising! (walking sideways holding furniture), first real words (“mama” or “papa” with meaning)",
            "activity": "Throw ball, show flowers, name objects (“this is a cup”)",
        },
        {
            "title": "Month 11 — Walking Practice",
            "color": DARK_BLUE,
            "feeding": [
                "3 meals + 2 snacks + milk",
                "Full egg can be introduced if not already started",
                "Still avoid: whole dry fruits (choking risk — powder them), popcorn, chips, honey, juice",
            ],
            "apply": [
                "4–8 teeth may be present — brushing twice a day is non-negotiable",
                "Trim toenails too — baby is more mobile now",
            ],
            "sleep": "12–13 hours — 1 nap (2–3 hours in the afternoon)",
            "milestones": "Walks with one-hand support, sits and stands independently, plays with utensils (throwing food is normal — ignore it 😄)",
            "activity": "Simple instructions (“Give me the ball”), stacking rings",
        },
        {
            "title": "Month 12 — 🎉 Happy Birthday! The Walking Month",
            "color": PINK,
            "feeding": [
                "Cow’s milk can be introduced (as per doctor) — max 300–400 ml/day (too much milk reduces appetite and iron)",
                "3 meals + 2 snacks — seat baby at the family table — eating habits form now",
                "Birthday cake/chocolate — just a few spoons for taste — don’t start sugar habit",
            ],
            "apply": [
                "Brush twice daily with rice-grain fluoride toothpaste",
                "Sunscreen every time baby goes outside",
                "Full daily bath is now fine",
            ],
            "sleep": "12–13 hours — 10–11 hours solid night sleep + 1 nap",
            "milestones": "🎉 Walking! (some walk at 9 months, late walking till 15–16 months is normal), says 2–3 words, tries spoon (messy is okay!)",
            "activity": "Dance to rhymes, throw and catch ball, look at picture books",
        },
    ]
    
    for i, month in enumerate(months_data_2):
        add_header_bar(story, f"🍼 Chapter {i+8}: {month['title']}", month['color'])
        
        story.append(Paragraph("🍽️ Feeding (What to Feed):", styles['SectionTitle']))
        for item in month['feeding']:
            story.append(Paragraph(f"• {item}", styles['BulletText']))
        
        story.append(Paragraph("🧴 What to Apply:", styles['SectionTitle']))
        for item in month['apply']:
            story.append(Paragraph(f"• {item}", styles['BulletText']))
        
        story.append(Paragraph(f"<b>😴 Sleep:</b> {month['sleep']}", styles['BodyEng']))
        story.append(Paragraph(f"<b>👶 Milestones:</b> {month['milestones']}", styles['BodyEng']))
        story.append(Paragraph(f"<b>🎯 Activity:</b> {month['activity']}", styles['BodyEng']))
        
        story.append(Spacer(1, 8))
        if i < len(months_data_2) - 1:
            story.append(PageBreak())
    
    story.append(PageBreak())
    
    # ========== VACCINATION ==========
    add_header_bar(story, "💉 Chapter 14: Vaccination Chart", DARK_BLUE)
    
    story.append(Paragraph(
        "This chart is based on the standard immunization schedule. Always confirm with your pediatrician as some vaccines may vary by country or be available privately.",
        styles['BodyEng']
    ))
    story.append(Spacer(1, 8))
    
    vax_headers = ["Age", "Vaccine", "Notes"]
    vax_rows = [
        ["At Birth", "BCG, Hepatitis B (Birth dose), OPV-0", "Usually given in hospital"],
        ["6 Weeks", "DTwP/DTaP-1, IPV-1, Hep B-2, Hib-1, Rotavirus-1, PCV-1", "First major shots"],
        ["10 Weeks", "DTwP/DTaP-2, IPV-2, Hib-2, Rotavirus-2, PCV-2", ""],
        ["14 Weeks", "DTwP/DTaP-3, IPV-3, Hib-3, Rotavirus-3, PCV-3", ""],
        ["6 Months", "Influenza-1 (optional), Hep B-3", ""],
        ["7 Months", "Influenza-2 (optional)", ""],
        ["9 Months", "MMR-1, Typhoid Conjugate", ""],
        ["12 Months", "Hepatitis A-1", ""],
    ]
    
    story.append(create_info_table(vax_headers, vax_rows, [1.2*inch, 3.8*inch, 1.4*inch]))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("💡 Parent Tip:", styles['TipTitle']))
    story.append(Paragraph("• On vaccination day, ensure baby is well-rested and has eaten lightly", styles['BulletText']))
    story.append(Paragraph("• Mild fever after shots is common — use paracetamol syrup only as advised by doctor", styles['BulletText']))
    story.append(Paragraph("• A cool cloth on the injection site can provide comfort", styles['BulletText']))
    
    story.append(PageBreak())
    
    # ========== RED FLAGS ==========
    add_header_bar(story, "⚠️ Chapter 15: Red Flags — When to See a Doctor", WARNING_RED)
    
    story.append(Paragraph(
        "If you notice any of these signs, contact your pediatrician or go to the nearest hospital immediately. Do not wait.",
        styles['BodyEng']
    ))
    story.append(Spacer(1, 8))
    
    emergency_items = [
        ("Breathing Difficulty", "Fast breathing, wheezing, chest retractions, blue lips"),
        ("High Fever", "Temperature 100.4°F (38°C) or higher in a baby under 3 months"),
        ("Feeding Refusal", "Not eating or drinking for 8–12 hours"),
        ("Forceful Vomiting", "Green or bloody vomit, or projectile vomiting after every feed"),
        ("Dehydration", "Dry lips, sunken eyes, no urine for 6+ hours, sunken fontanelle"),
        ("Seizures", "Body jerks, eyes rolling up, loss of consciousness"),
        ("Worsening Jaundice", "Yellow color spreading, baby becoming lethargic"),
        ("Umbilical Infection", "Pus, redness, foul smell, or fever with cord issues"),
        ("Inconsolable Crying", "Crying continuously for 3+ hours, hard abdomen"),
        ("Head Injury / Fall", "Vomiting, drowsiness, or change in eyes after a fall"),
    ]
    
    for title, desc in emergency_items:
        story.append(Paragraph(f"<b>🚨 {title}:</b> {desc}", styles['BodyEng']))
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("📞 Keep These Numbers Handy:", styles['SectionTitle']))
    story.append(Paragraph("• Ambulance: 108 / 102 (India) or your local emergency number", styles['BulletText']))
    story.append(Paragraph("• Save your pediatrician + nearest hospital number", styles['BulletText']))
    story.append(Paragraph("• Poison Control (India): 1800-116-117", styles['BulletText']))
    
    story.append(PageBreak())
    
    # ========== BONUSES ==========
    add_header_bar(story, "🎁 Chapter 16: Bonus Checklists (Printable)", PINK)
    
    story.append(Paragraph(
        "Print these checklists and keep them handy. Daily tracking becomes much easier.",
        styles['BodyEng']
    ))
    story.append(Spacer(1, 10))
    
    # Bonus 1
    story.append(Paragraph("1️⃣ Feeding Tracker (One Day)", styles['SectionTitle']))
    feed_headers = ["Time", "Type (Breast/Formula)", "Amount / Duration", "Notes"]
    feed_rows = [
        ["____ : ____", "☐ Breast  ☐ Formula", "________", ""],
        ["____ : ____", "☐ Breast  ☐ Formula", "________", ""],
        ["____ : ____", "☐ Breast  ☐ Formula", "________", ""],
        ["____ : ____", "☐ Breast  ☐ Formula", "________", ""],
        ["____ : ____", "☐ Breast  ☐ Formula", "________", ""],
        ["____ : ____", "☐ Breast  ☐ Formula", "________", ""],
    ]
    story.append(create_info_table(feed_headers, feed_rows, [1.3*inch, 2.2*inch, 1.5*inch, 1.4*inch]))
    
    story.append(Spacer(1, 12))
    
    # Bonus 2
    story.append(Paragraph("2️⃣ Newborn Shopping Checklist", styles['SectionTitle']))
    shop_items = [
        "☐ Clothes (bodysuits, sleepsuits, caps, mittens, socks) — 6–8 sets",
        "☐ Diapers (newborn size) + wet wipes (or cotton)",
        "☐ Baby blankets / swaddles — 2–3",
        "☐ Digital thermometer",
        "☐ Nail clipper / file",
        "☐ Baby bathtub or sponge bath set",
        "☐ Mild baby soap + shampoo",
        "☐ Zinc oxide cream (for diaper rash)",
        "☐ Coconut / sesame oil (for massage)",
        "☐ Car seat (age-appropriate)",
        "☐ Stroller / carrier",
        "☐ Bottles + sterilizer (if using formula)",
    ]
    for item in shop_items:
        story.append(Paragraph(item, styles['BulletText']))
    
    story.append(Spacer(1, 12))
    
    # Bonus 3
    story.append(Paragraph("3️⃣ Sleep Log (One Week)", styles['SectionTitle']))
    sleep_headers = ["Day", "Night Sleep", "Nap 1", "Nap 2", "Total"]
    sleep_rows = [
        ["Mon", "____ hrs", "____", "____", "____"],
        ["Tue", "____ hrs", "____", "____", "____"],
        ["Wed", "____ hrs", "____", "____", "____"],
        ["Thu", "____ hrs", "____", "____", "____"],
        ["Fri", "____ hrs", "____", "____", "____"],
        ["Sat", "____ hrs", "____", "____", "____"],
        ["Sun", "____ hrs", "____", "____", "____"],
    ]
    story.append(create_info_table(sleep_headers, sleep_rows, [1.1*inch, 1.3*inch, 1.2*inch, 1.2*inch, 1.1*inch]))
    
    story.append(PageBreak())
    
    # Bonus 4 & 5
    story.append(Paragraph("4️⃣ Vaccination Reminder", styles['SectionTitle']))
    story.append(Paragraph("• Birth: BCG, Hep B, OPV-0 — Date: __________", styles['BulletText']))
    story.append(Paragraph("• 6 Weeks: __________", styles['BulletText']))
    story.append(Paragraph("• 10 Weeks: __________", styles['BulletText']))
    story.append(Paragraph("• 14 Weeks: __________", styles['BulletText']))
    story.append(Paragraph("• 6 Months: __________", styles['BulletText']))
    story.append(Paragraph("• 9 Months: __________", styles['BulletText']))
    story.append(Paragraph("• 12 Months: __________", styles['BulletText']))
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("5️⃣ Emergency Contact Card", styles['SectionTitle']))
    story.append(Paragraph("• Pediatrician: _________________ Phone: _______________", styles['BulletText']))
    story.append(Paragraph("• Nearest Hospital: _________________ Phone: _______________", styles['BulletText']))
    story.append(Paragraph("• Ambulance: 108 / Local Emergency Number", styles['BulletText']))
    story.append(Paragraph("• Parent Alternate Number: _________________", styles['BulletText']))
    story.append(Paragraph("• Family Emergency Contact: _________________", styles['BulletText']))
    story.append(Paragraph("• Baby’s Blood Group: ________  Allergies: _______________", styles['BulletText']))
    
    story.append(Spacer(1, 20))
    
    # Final notes
    add_header_bar(story, "✅ 3 Things to Remember Every Month", TIP_GREEN)
    story.append(Paragraph("1. <b>Follow the vaccination chart</b> — never skip doses", styles['BodyEng']))
    story.append(Paragraph("2. <b>Weight check:</b> If weight is not increasing monthly, see the doctor", styles['BodyEng']))
    story.append(Paragraph("3. <b>3-day rule:</b> Introduce every new food for 3 days — stop if allergy signs (rash, vomiting, loose stools) appear", styles['BodyEng']))
    
    story.append(Spacer(1, 30))
    
    # Back cover message
    story.append(HRFlowable(width="100%", thickness=1.5, color=PINK, spaceBefore=10, spaceAfter=15))
    
    story.append(Paragraph(
        "With CuddleNine",
        ParagraphStyle('Back1', fontName='NotoSans-Bold', fontSize=16, textColor=DARK_BLUE, alignment=TA_CENTER, spaceAfter=6)
    ))
    story.append(Paragraph(
        "Little Care, Big Love",
        ParagraphStyle('Back2', fontName='NotoSans', fontSize=14, textColor=PINK, alignment=TA_CENTER, spaceAfter=12)
    ))
    story.append(Paragraph(
        "May your baby’s first year be safe, happy, and full of love.<br/>This guide is just a starting point — every baby is unique. Always follow your doctor’s advice.",
        ParagraphStyle('Back3', fontName='NotoSans', fontSize=10, textColor=MED_GRAY, alignment=TA_CENTER, leading=15)
    ))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "© CuddleNine  •  Educational Guide Only  •  Not a Substitute for Professional Medical Advice",
        ParagraphStyle('BackDisc', fontName='NotoSans', fontSize=7, textColor=MED_GRAY, alignment=TA_CENTER)
    ))
    
    # Build
    doc.build(story, canvasmaker=HeaderFooterCanvas)
    print(f"✅ English PDF created successfully: {output_path}")
    return output_path


if __name__ == "__main__":
    build_pdf()
