#!/usr/bin/env python3
"""
CuddleNine — 0 to 12 Months Baby Care Guide
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
pdfmetrics.registerFont(TTFont("NotoDev", FONT_DIR + "Noto Serif Devanagari/static/NotoSerifDevanagari-Regular.ttf"))
pdfmetrics.registerFont(TTFont("NotoDev-Bold", FONT_DIR + "Noto Serif Devanagari/static/NotoSerifDevanagari-Bold.ttf"))
pdfmetrics.registerFont(TTFont("NotoDev-Semi", FONT_DIR + "Noto Serif Devanagari/static/NotoSerifDevanagari-SemiBold.ttf"))

# ==================== PAGE SETUP ====================
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 0.7 * inch

class ColoredBox(Flowable):
    """A colored rounded box with title and content"""
    def __init__(self, title, content, bg_color, border_color, title_color=WHITE, width=None, icon=""):
        Flowable.__init__(self)
        self.title = title
        self.content = content
        self.bg_color = bg_color
        self.border_color = border_color
        self.title_color = title_color
        self.box_width = width or (PAGE_WIDTH - 2 * MARGIN)
        self.icon = icon
        self._height = None

    def wrap(self, availWidth, availHeight):
        self.box_width = min(self.box_width, availWidth)
        # Approximate height
        styles = getSampleStyleSheet()
        content_style = ParagraphStyle(
            'BoxContent',
            fontName='NotoDev',
            fontSize=9,
            leading=13,
            textColor=DARK_GRAY,
        )
        p = Paragraph(self.content, content_style)
        w, h = p.wrap(self.box_width - 20, 1000)
        self._height = h + 36  # title + padding
        return self.box_width, self._height

    def draw(self):
        self.canv.setFillColor(self.bg_color)
        self.canv.setStrokeColor(self.border_color)
        self.canv.setLineWidth(1.5)
        self.canv.roundRect(0, 0, self.box_width, self._height, 8, fill=1, stroke=1)
        
        # Title bar
        self.canv.setFillColor(self.border_color)
        self.canv.roundRect(0, self._height - 22, self.box_width, 22, 8, fill=1, stroke=0)
        self.canv.rect(0, self._height - 22, self.box_width, 10, fill=1, stroke=0)
        
        self.canv.setFillColor(self.title_color)
        self.canv.setFont("NotoDev-Bold", 10)
        self.canv.drawString(10, self._height - 16, self.icon + " " + self.title)
        
        # Content
        styles = getSampleStyleSheet()
        content_style = ParagraphStyle(
            'BoxContent',
            fontName='NotoDev',
            fontSize=9,
            leading=13,
            textColor=DARK_GRAY,
        )
        p = Paragraph(self.content, content_style)
        p.wrapOn(self.canv, self.box_width - 20, self._height - 30)
        p.drawOn(self.canv, 10, 8)


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
        fontName='NotoDev',
        fontSize=14,
        textColor=PINK,
        alignment=TA_CENTER,
        spaceAfter=12,
        leading=20
    ))
    
    styles.add(ParagraphStyle(
        name='ChapterTitle',
        fontName='NotoDev-Bold',
        fontSize=18,
        textColor=DARK_BLUE,
        spaceBefore=12,
        spaceAfter=10,
        leading=24
    ))
    
    styles.add(ParagraphStyle(
        name='SectionTitle',
        fontName='NotoDev-Bold',
        fontSize=13,
        textColor=PINK,
        spaceBefore=10,
        spaceAfter=6,
        leading=18
    ))
    
    styles.add(ParagraphStyle(
        name='BodyHindi',
        fontName='NotoDev',
        fontSize=10,
        textColor=DARK_GRAY,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=15,
        firstLineIndent=0
    ))
    
    styles.add(ParagraphStyle(
        name='BodyHindiCenter',
        fontName='NotoDev',
        fontSize=10,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=15
    ))
    
    styles.add(ParagraphStyle(
        name='BulletHindi',
        fontName='NotoDev',
        fontSize=9.5,
        textColor=DARK_GRAY,
        leftIndent=15,
        spaceAfter=3,
        leading=14
    ))
    
    styles.add(ParagraphStyle(
        name='WarningTitle',
        fontName='NotoDev-Bold',
        fontSize=11,
        textColor=WARNING_RED,
        spaceBefore=8,
        spaceAfter=4,
        leading=15
    ))
    
    styles.add(ParagraphStyle(
        name='TipTitle',
        fontName='NotoDev-Bold',
        fontSize=11,
        textColor=TIP_GREEN,
        spaceBefore=8,
        spaceAfter=4,
        leading=15
    ))
    
    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='NotoDev-Bold',
        fontSize=9,
        textColor=WHITE,
        alignment=TA_CENTER,
        leading=12
    ))
    
    styles.add(ParagraphStyle(
        name='TableCell',
        fontName='NotoDev',
        fontSize=8.5,
        textColor=DARK_GRAY,
        leading=12
    ))
    
    styles.add(ParagraphStyle(
        name='FooterText',
        fontName='NotoSans',
        fontSize=8,
        textColor=MED_GRAY,
        alignment=TA_CENTER
    ))
    
    styles.add(ParagraphStyle(
        name='MonthHeader',
        fontName='NotoDev-Bold',
        fontSize=16,
        textColor=WHITE,
        alignment=TA_CENTER,
        leading=20
    ))
    
    return styles


def add_header_bar(story, text, bg_color=DARK_BLUE):
    """Add a colored header bar"""
    data = [[Paragraph(text, ParagraphStyle(
        'HeaderBar',
        fontName='NotoDev-Bold',
        fontSize=14,
        textColor=WHITE,
        alignment=TA_CENTER,
        leading=18
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
        ('FONTNAME', (0, 0), (-1, 0), 'NotoDev-Bold'),
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
    output_path = "/home/workdir/artifacts/CuddleNine_Baby_Care_Guide.pdf"
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
        "<b>0 से 12 महीने की संपूर्ण बेबी केयर गाइड</b>",
        ParagraphStyle('CoverMain', fontName='NotoDev-Bold', fontSize=16, textColor=DARK_BLUE, alignment=TA_CENTER, leading=22)
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "नए माता-पिता के लिए स्टेप-बाय-स्टेप प्रैक्टिकल गाइड<br/>हर महीने क्या करें, क्या खिलाएं, क्या लगाएं — सब कुछ विस्तार से",
        ParagraphStyle('CoverDesc', fontName='NotoDev', fontSize=11, textColor=MED_GRAY, alignment=TA_CENTER, leading=16)
    ))
    
    story.append(Spacer(1, 30))
    
    # Feature boxes on cover
    features = [
        ["🕐 पहले 24 घंटे की घंटे-दर-घंटे गाइड", "🍼 0–12 महीने फीडिंग प्लान"],
        ["😴 स्लीप शेड्यूल हर महीने का", "🧴 स्किनकेयर व हाइजीन टिप्स"],
        ["💉 वैक्सीनेशन चार्ट (भारत)", "⚠️ रेड फ्लैग्स व इमरजेंसी"],
        ["🎁 5 प्रिंटेबल बोनस चेकलिस्ट", "❤️ माता-पिता की मानसिक सेहत"],
    ]
    
    feat_data = []
    for row in features:
        feat_data.append([
            Paragraph(row[0], ParagraphStyle('Feat', fontName='NotoDev', fontSize=9, textColor=DARK_GRAY, alignment=TA_CENTER)),
            Paragraph(row[1], ParagraphStyle('Feat', fontName='NotoDev', fontSize=9, textColor=DARK_GRAY, alignment=TA_CENTER)),
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
    add_header_bar(story, "📚 विषय सूची (Table of Contents)")
    
    toc_items = [
        ("1.", "पहले 24 घंटे — घंटे-दर-घंटे गाइड", "3"),
        ("2.", "महीना 1 (0–30 दिन) — एडजस्ट होने का महीना", "5"),
        ("3.", "महीना 2 — मुस्कान का महीना", "6"),
        ("4.", "महीना 3 — बात-चीत का महीना", "7"),
        ("5.", "महीना 4 — रोलिंग का महीना", "8"),
        ("6.", "महीना 5 — पकड़ने का महीना", "9"),
        ("7.", "महीना 6 — सॉलिड फूड शुरू! 🎉", "10"),
        ("8.", "महीना 7 — खाने का असली स्वाद", "11"),
        ("9.", "महीना 8 — क्रॉल का महीना", "12"),
        ("10.", "महीना 9 — खड़े होने की तैयारी", "13"),
        ("11.", "महीना 10 — स्टेप्स का महीना", "14"),
        ("12.", "महीना 11 — चलने की प्रैक्टिस", "15"),
        ("13.", "महीना 12 — जन्मदिन! चलने का महीना", "16"),
        ("14.", "वैक्सीनेशन चार्ट (भारत का राष्ट्रीय कार्यक्रम)", "17"),
        ("15.", "⚠️ रेड फ्लैग्स — कब डॉक्टर को दिखाएं", "18"),
        ("16.", "🎁 बोनस चेकलिस्ट्स", "19"),
    ]
    
    toc_data = []
    for num, title, page in toc_items:
        toc_data.append([
            Paragraph(num, ParagraphStyle('TocNum', fontName='NotoSans-Bold', fontSize=10, textColor=DARK_BLUE)),
            Paragraph(title, ParagraphStyle('TocTitle', fontName='NotoDev', fontSize=10, textColor=DARK_GRAY)),
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
    add_header_bar(story, "🕐 अध्याय 1: पहले 24 घंटे — घंटे-दर-घंटे गाइड", DARK_BLUE)
    
    story.append(Paragraph(
        "नए माता-पिता के लिए सबसे महत्वपूर्ण समय। यह गाइड आपको बताएगी कि डिलीवरी के तुरंत बाद क्या करना है, क्या लगाना है और क्या खिलाना है।",
        styles['BodyHindi']
    ))
    story.append(Spacer(1, 8))
    
    # Hour 0-2
    story.append(Paragraph("⏰ घंटा 0–2 (डिलीवरी के तुरंत बाद)", styles['SectionTitle']))
    story.append(Paragraph("<b>क्या होता है:</b>", styles['BodyHindi']))
    story.append(Paragraph("• बेबी को मां की छाती पर रखा जाता है (स्किन-टू-स्किन) — यह सबसे पहला और सबसे महत्वपूर्ण स्टेप है", styles['BulletHindi']))
    story.append(Paragraph("• नर्स बेबी को पोछकर साफ करती है", styles['BulletHindi']))
    story.append(Paragraph("• पहली फीड (कोलोस्ट्रम) — <b>पहली घंटे में स्तनपान शुरू करना चाहिए</b>", styles['BulletHindi']))
    
    story.append(Paragraph("<b>🧴 क्या लगाना चाहिए:</b>", styles['BodyHindi']))
    story.append(Paragraph("• <b>कुछ नहीं लगाना!</b> नया बेबी प्लेन रहता है — पाउडर, ऑयल, कुछ भी नहीं", styles['BulletHindi']))
    story.append(Paragraph("• सिर्फ कॉटन कपड़े से हल्का पोछना", styles['BulletHindi']))
    
    story.append(Paragraph("<b>🍼 क्या खिलाना चाहिए:</b>", styles['BodyHindi']))
    story.append(Paragraph("• सिर्फ मां का पहला दूध (कोलोस्ट्रम) — पीला, पतला, बहुत पावरफुल", styles['BulletHindi']))
    story.append(Paragraph("• फॉर्मूला की जरूरत तभी जब डॉक्टर बोले", styles['BulletHindi']))
    
    story.append(Spacer(1, 6))
    
    # Hour 2-6
    story.append(Paragraph("⏰ घंटा 2–6", styles['SectionTitle']))
    story.append(Paragraph("<b>क्या होता है:</b>", styles['BodyHindi']))
    story.append(Paragraph("• बेबी का पहला डायपर — पहला स्टूल 'मेकोनियम' (काला-हरा) — यह <b>नॉर्मल</b> है", styles['BulletHindi']))
    story.append(Paragraph("• नर्स बेबी को मेजर करती है — वजन, लंबाई, सिर का आकार", styles['BulletHindi']))
    story.append(Paragraph("• मां को आराम देना जरूरी है", styles['BulletHindi']))
    
    story.append(Paragraph("<b>🧴 क्या लगाना चाहिए:</b>", styles['BodyHindi']))
    story.append(Paragraph("• नाभि (अम्बिलिकल कॉर्ड स्टंप) — <b>सूखा रखना है, कोई तेल/पाउडर नहीं</b>", styles['BulletHindi']))
    story.append(Paragraph("• डायपर के ऊपर का हिस्सा फोल्ड करके रखें ताकि स्टंप गीला न हो", styles['BulletHindi']))
    
    story.append(Paragraph("<b>🍼 क्या खिलाना चाहिए:</b>", styles['BodyHindi']))
    story.append(Paragraph("• हर <b>2 घंटे में फीड</b> — चाहे बेबी मांगे या न मांगे", styles['BulletHindi']))
    story.append(Paragraph("• बेबी सोता भी है तो जगाकर फीड करवाना (पहले दिन महत्वपूर्ण)", styles['BulletHindi']))
    
    story.append(Spacer(1, 6))
    
    # Hour 6-12
    story.append(Paragraph("⏰ घंटा 6–12", styles['SectionTitle']))
    story.append(Paragraph("<b>क्या होता है:</b>", styles['BodyHindi']))
    story.append(Paragraph("• बेबी का पहला पेशाब — 24 घंटे के अंदर होना चाहिए", styles['BulletHindi']))
    story.append(Paragraph("• शरीर ठंडा होता है — बेबी को <b>कैप + मिटन्स + सॉक्स</b> पहनाना", styles['BulletHindi']))
    story.append(Paragraph("• बेबी ज्यादातर सोता है — यह नॉर्मल है", styles['BulletHindi']))
    
    story.append(Paragraph("<b>🧴 क्या लगाना चाहिए:</b>", styles['BodyHindi']))
    story.append(Paragraph("• कॉटन नैपीज या डायपर्स — हर 2-3 घंटे में बदलें", styles['BulletHindi']))
    story.append(Paragraph("• वेट वाइप्स नहीं — सिर्फ <b>कॉटन + गुनगुने पानी</b> से पोछना (पहले 15-20 दिन)", styles['BulletHindi']))
    
    story.append(Paragraph("<b>🍼 क्या खिलाना चाहिए:</b>", styles['BodyHindi']))
    story.append(Paragraph("• सिर्फ ब्रेस्टमिल्क — <b>पानी भी नहीं</b> (0-6 महीने में पानी नहीं देते)", styles['BulletHindi']))
    story.append(Paragraph("• फॉर्मूला वाले बेबीज: स्टरलाइज्ड बॉटल, गुनगुना दूध (रूम टेम्परेचर)", styles['BulletHindi']))
    
    story.append(PageBreak())
    
    # Hour 12-24
    story.append(Paragraph("⏰ घंटा 12–24", styles['SectionTitle']))
    story.append(Paragraph("<b>क्या होता है:</b>", styles['BodyHindi']))
    story.append(Paragraph("• बेबी थोड़ा पीला दिखता है? — यह फिजियोलॉजिकल जॉन्डिस हो सकता है — डॉक्टर चेक करें", styles['BulletHindi']))
    story.append(Paragraph("• बेबी का पहला फुल बाथ नहीं — सिर्फ <b>स्पंज बाथ</b> (कॉर्ड गिरने तक)", styles['BulletHindi']))
    story.append(Paragraph("• मां का दूध आना शुरू — स्तन थोड़ा हार्ड होगा — वार्म कंप्रेस से आराम", styles['BulletHindi']))
    
    story.append(Paragraph("<b>🧴 क्या लगाना चाहिए:</b>", styles['BodyHindi']))
    story.append(Paragraph("• स्पंज बाथ के लिए: गुनगुना पानी + सॉफ्ट कॉटन टॉवल", styles['BulletHindi']))
    story.append(Paragraph("• नाभि पर कुछ नहीं — बस सूखा और साफ", styles['BulletHindi']))
    story.append(Paragraph("• बेबी लोशन/ऑयल — पहले 24 घंटे में अवॉइड (स्किन सेंसिटिव होती है)", styles['BulletHindi']))
    
    story.append(Paragraph("<b>🍼 क्या खिलाना चाहिए:</b>", styles['BodyHindi']))
    story.append(Paragraph("• 8–12 बार फीड हो सकती है — जितना मांगे उतना", styles['BulletHindi']))
    story.append(Paragraph("• फॉर्मूला: 30-60 ml हर 3 घंटे (डॉक्टर के हिसाब से)", styles['BulletHindi']))
    
    story.append(Spacer(1, 10))
    
    # Red flags box
    story.append(Paragraph("⚠️ रेड फ्लैग्स — तुरंत डॉक्टर को बुलाएं:", styles['WarningTitle']))
    red_flags = [
        "बेबी सांस नहीं ले पा रहा या सांस में आवाज आ रही है",
        "बॉडी टेम्परेचर 97°F से कम या 99.5°F से ज्यादा",
        "बेबी 4+ घंटे से फीडिंग नहीं ले रहा",
        "पेशाब 24 घंटे में नहीं हुआ",
        "स्किन/होंठ नीले पड़ रहे हैं",
    ]
    for rf in red_flags:
        story.append(Paragraph(f"• {rf}", styles['BulletHindi']))
    
    story.append(Spacer(1, 12))
    
    # Summary table
    story.append(Paragraph("📋 सारांश टेबल — पहले 24 घंटे", styles['SectionTitle']))
    
    summary_headers = ["समय", "क्या करें", "क्या न करें"]
    summary_rows = [
        ["0–2 घंटे", "स्किन-टू-स्किन + पहली फीड", "पाउडर/ऑयल लगाना"],
        ["2–6 घंटे", "कॉर्ड सूखा रखें, 2 घंटे में फीड", "डायपर स्टंप पर टच न करें"],
        ["6–12 घंटे", "कैप-मिटन्स पहनाएं, कॉटन से पोछें", "वेट वाइप्स यूज"],
        ["12–24 घंटे", "स्पंज बाथ, जॉन्डिस चेक", "फुल बाथ, पानी खिलाना"],
    ]
    
    story.append(create_info_table(summary_headers, summary_rows, [1.3*inch, 2.6*inch, 2.5*inch]))
    
    story.append(PageBreak())
    
    # ========== MONTHLY CHAPTERS ==========
    
    months_data = [
        {
            "title": "महीना 1 (0–30 दिन) — एडजस्ट होने का महीना",
            "color": DARK_BLUE,
            "feeding": [
                "सिर्फ ब्रेस्टमिल्क या फॉर्मूला — कुछ और नहीं",
                "हर 2-3 घंटे में फीड — दिन में 8-12 बार",
                "पानी, शहद, ग्लूकोज — बिल्कुल नहीं (शहद में बैक्टीरिया होता है — खतरनाक!)",
            ],
            "apply": [
                "नाभि (कॉर्ड स्टंप): सूखा रखें, कुछ मत लगाएं — 7-15 दिन में गिर जाती है",
                "स्किन: पहले 2-3 हफ्ते सिर्फ कॉटन + पानी से पोछना — साबुन अवॉइड",
                "डायपर एरिया: कॉटन क्लॉथ से पोछें, रैश हो तो जिंक ऑक्साइड क्रीम पतली लेयर",
                "मसाज: 2-3 हफ्ते बाद शुरू करें — तिल का तेल या नारियल तेल (पहले पैच टेस्ट)",
            ],
            "sleep": "16-18 घंटे — पर हर 2 घंटे में फीड के लिए जगाना",
            "milestones": "आंखें फोकस करती हैं, आवाज पर रिएक्शन, गर्दन थोड़ी कंट्रोल",
            "warning": "जॉन्डिस चेक करें (स्किन/होंठ पीले) — 24 घंटे से ज्यादा रहे तो डॉक्टर",
            "activity": "स्किन-टू-स्किन कॉन्टैक्ट बढ़ाएं, सॉफ्ट लुलाबीज गाएं",
        },
        {
            "title": "महीना 2 — मुस्कान का महीना",
            "color": PINK,
            "feeding": [
                "सिर्फ मिल्क — पैटर्न बनने लगता है (हर 3 घंटे)",
                "मां के खाने से दूध का स्वाद बदलता है — प्याज-लहसुन अवॉइड",
            ],
            "apply": [
                "अब जेंटल बेबी सोप (बुधवार-शनिवार अल्टरनेट डेज) से नहाना शुरू",
                "क्रैडल कैप (सर पर छिलकेदार परत) — नारियल तेल लगाकर 15 मिनट रखें, फिर सॉफ्ट ब्रश से हल्का साफ करें",
                "नाखून हमेशा काटे हुए रखें (बेबी अपने आप को खरोंच लेता है)",
            ],
            "sleep": "15-16 घंटे — रात का फीड अभी भी जरूरी",
            "milestones": "🎉 सोशल स्माइल! पहली मुस्कान इसी महीने आती है, कूइंग साउंड्स (गू-गू)",
            "warning": "अत्यधिक रोना या फीडिंग रिफ्यूजल — डॉक्टर से बात करें",
            "activity": "टमी टाइम 2-3 मिनट रोज शुरू करें — गर्दन मजबूत बनेगी",
        },
        {
            "title": "महीना 3 — बात-चीत का महीना",
            "color": DARK_BLUE,
            "feeding": [
                "सिर्फ मिल्क — फीड थोड़ी लंबे इंटरवल पर (3-4 घंटे)",
                "फॉर्मूला बेबी: अब 90-120 ml तक हो सकता है",
            ],
            "apply": [
                "मसाज रोज — दोपहर 3-4 बजे के आसपास (धूप के समय) — पेट, हाथ, पैर की हल्की एक्सरसाइज",
                "फेस क्रीम — सिर्फ अगर स्किन ड्राई हो तो फ्रagrance-फ्री बेबी लोशन",
            ],
            "sleep": "14-16 घंटे — कुछ बेबीज 5-6 घंटे रात को सो जाते हैं",
            "milestones": "हाथ खोलते-बंद करते हैं, रैटल की आवाज पर मुड़ते हैं, पहली हंसी!",
            "warning": "सिर का कंट्रोल न हो या आंखें क्रॉस रहें — चेकअप करवाएं",
            "activity": "रंग-बिरंगे खिलौने दिखाएं — 20-30 सेमी दूर से (आई ट्रैकिंग प्रैक्टिस)",
        },
        {
            "title": "महीना 4 — रोलिंग का महीना",
            "color": PINK,
            "feeding": [
                "सिर्फ मिल्क — लेकिन अब फीडिंग डिस्ट्रेक्शन होती है (दूध पीते-पीते इधर-उधर देखता है) — शांत कमरे में फीड करें",
            ],
            "apply": [
                "टीथिंग शुरू हो सकता है (थूक ज्यादा, चीजें मुंह में) — सिलिकॉन टीथर दे सकते हैं (स्टरलाइज्ड)",
                "नेल कटर से हर हफ्ते नाखून काटें",
            ],
            "sleep": "14-15 घंटे — स्लीप रिग्रेशन आ सकता है (रात में उठना) — नॉर्मल है, 2-3 हफ्ते में ठीक",
            "milestones": "🎉 रोल ओवर! (पेट से पीठ/पीठ से पेट) — इसलिए कभी बेड पर अकेले मत छोड़ो — गिर सकता है!",
            "warning": "रोलिंग के बाद हमेशा निगरानी रखें, बेबी प्रूफिंग शुरू करें",
            "activity": "टमी टाइम 10 मिनट तक बढ़ाएं, 'आ-ऊ' की आवाज कॉपी करें",
        },
        {
            "title": "महीना 5 — पकड़ने का महीना",
            "color": DARK_BLUE,
            "feeding": [
                "सिर्फ मिल्क — शेड्यूल और सेट हो गया",
                "आयरन स्टोर्स कम होने लगते हैं — डॉक्टर से आयरन ड्रॉप्स पूछें",
            ],
            "apply": [
                "टीथिंग जेल नहीं (डॉक्टर के बिना) — टीथर + हल्की मालिश काफी है",
                "हेयर ऑयल — हफ्ते में 2 बार से ज्यादा नहीं (डैंड्रफ बढ़ता है)",
            ],
            "sleep": "14 घंटे — 2-3 नैप्स दिन में",
            "milestones": "चीजें पकड़ लेता है, अपने पैरों को मुंह तक ले जाता है, स्ट्रेंजर एंग्जायटी शुरू",
            "warning": "वजन नहीं बढ़ रहा या बहुत रोना — डॉक्टर से सलाह लें",
            "activity": "रैटल पकड़वाएं, 'हाई फाइव' प्रैक्टिस — हैंड्स क्लैपिंग सिखाएं",
        },
        {
            "title": "महीना 6 — सॉलिड फूड शुरू! 🎉",
            "color": PINK,
            "feeding": [
                "पहला सॉलिड: दाल का पानी या राइस सीरियल (सेरेलैक) — 1-2 चम्मच सुबह, फीड के बाद",
                "नया खाना 3 दिन रूल: एक नया खाना 3 दिन तक दें — एलर्जी चेक करें",
                "क्या दे सकते हैं: मूंग दाल पानी, मैशेड बनाना, सेब प्यूरी, गाजर प्यूरी, चावल",
                "क्या नहीं: शहद (खतरनाक!), गाय का दूध (अभी नहीं), नमक-चीनी, ड्राई फ्रूट्स पूरा (पाउडर करके थोड़ा), सिट्रस फ्रूट्स",
            ],
            "apply": [
                "दांत आ रहे हों तो: बेबी टूथब्रश (फिंगर ब्रश) — पानी से ही ब्रश",
                "फेस क्रीम — खाना खाते वक्त लगता है — पछा हुआ खाना पोछते रहना (स्किन खराब होती है)",
            ],
            "sleep": "14 घंटे — 2 नैप्स",
            "milestones": "बैठना शुरू (सपोर्ट के साथ), अपना नाम सुनकर मुड़ता है, बैबलिंग ('बा-बा', 'दा-दा')",
            "warning": "6वें महीने वैक्सीनेशन + आयरन/कैल्शियम ड्रॉप्स — डॉक्टर विजिट जरूरी",
            "activity": "सपोर्टेड सिटिंग प्रैक्टिस, नए स्वादों का परिचय धीरे-धीरे",
        },
    ]
    
    for i, month in enumerate(months_data):
        add_header_bar(story, f"🍼 अध्याय {i+2}: {month['title']}", month['color'])
        
        story.append(Paragraph("🍼 फीडिंग (क्या खिलाना है):", styles['SectionTitle']))
        for item in month['feeding']:
            story.append(Paragraph(f"• {item}", styles['BulletHindi']))
        
        story.append(Paragraph("🧴 क्या लगाना चाहिए:", styles['SectionTitle']))
        for item in month['apply']:
            story.append(Paragraph(f"• {item}", styles['BulletHindi']))
        
        story.append(Paragraph(f"<b>😴 नींद:</b> {month['sleep']}", styles['BodyHindi']))
        story.append(Paragraph(f"<b>👶 माइलस्टोन्स:</b> {month['milestones']}", styles['BodyHindi']))
        story.append(Paragraph(f"<b>🎯 एक्टिविटी:</b> {month['activity']}", styles['BodyHindi']))
        
        if month.get('warning'):
            story.append(Paragraph(f"⚠️ <b>ध्यान दें:</b> {month['warning']}", styles['WarningTitle']))
        
        story.append(Spacer(1, 8))
        if i < len(months_data) - 1:
            story.append(PageBreak())
    
    story.append(PageBreak())
    
    # Months 7-12
    months_data_2 = [
        {
            "title": "महीना 7 — खाने का असली स्वाद",
            "color": DARK_BLUE,
            "feeding": [
                "अब 2 मील्स + मिल्क",
                "खिचड़ी (दाल-चावल मैशेड), बनाना, सेब, सूजी खीर (बिना चीनी)",
                "अंडे की जर्दी शुरू कर सकते हैं (अगर वेजिटेरियन नहीं) — 3 दिन रूल फॉलो",
                "पानी: 50-100 ml दिन भर (कप से सिखाना शुरू)",
            ],
            "apply": [
                "अब दांत आ रहे हैं तो फिंगर ब्रश रोज — पानी से साफ करें",
                "नेल केयर — हफ्ते में 1 बार काटें",
            ],
            "sleep": "13-14 घंटे — 2 नैप्स",
            "milestones": "सपोर्ट के बिना बैठता है, एक चीज से दूसरी हाथ में देता है, 'मामा-पापा' टाइप साउंड्स",
            "activity": "रस्सी के खिलौने खींचने दें, 'क्लैप-क्लैप' करें",
        },
        {
            "title": "महीना 8 — क्रॉल का महीना",
            "color": PINK,
            "feeding": [
                "2-3 मील्स + मिल्क — अब फिंगर फूड्स दें: स्टीम्ड कैरट स्टिक्स, बनाना पीसेस (अपने हाथ से खाना सीखता है)",
                "आटा हलवा, दलिया, दही (प्रोबायोटिक, डाइजेशन के लिए बेस्ट)",
            ],
            "apply": [
                "सनस्क्रीन! अब बाहर जाता है — SPF 30+ बेबी सनस्क्रीन (10 बजे से 4 बजे के बीच अवॉइड)",
                "मच्छर प्रोटेक्शन — रिपेलेंट नहीं — मच्छरदानी या फुल स्लीव्स",
            ],
            "sleep": "13-14 घंटे — नैप्स 2 से घटकर 1 हो सकते हैं",
            "milestones": "🎉 क्रॉल! घुटनों पे चलना शुरू। इसलिए घर बेबी-प्रूफ करें: सॉकेट कवर्स, नीचे से साफ, टेबल के कोने पर कुशन",
            "activity": "'व्हेयर इज द बॉल?' — चीजों के नाम बोलें, स्टैकिंग कप्स",
        },
        {
            "title": "महीना 9 — खड़े होने की तैयारी",
            "color": DARK_BLUE,
            "feeding": [
                "3 मील्स + मिल्क (फैमिली का खाना — बिना मिर्ची-नमक, अलग निकाल कर)",
                "रोटी (सॉफ्ट, छोटे टुकड़े) दे सकते हैं",
                "पनीर (क्रंबल) — प्रोटीन के लिए",
            ],
            "apply": [
                "दांत ब्रश — अब राइस-ग्रेन साइज फ्लोराइड टूथपेस्ट (डॉक्टर से पूछ कर) — 2 बार रोज",
                "हेयर वॉश — हफ्ते में 2 बार",
            ],
            "sleep": "13-14 घंटे — 1-2 नैप्स",
            "milestones": "खड़े होने की कोशिश (फर्नीचर पकड़ के), वेविंग बाई-बाई, ऑब्जेक्ट परमानेंस (छुपाने पे ढूंढता है — 'पीकाबू' खेलें!)",
            "activity": "वॉकर नहीं (टोज़ पे चलना सीखता है — गलत पोश्चर) — पुश वॉकर या फर्नीचर से खड़ा होने दें",
        },
        {
            "title": "महीना 10 — स्टेप्स का महीना",
            "color": PINK,
            "feeding": [
                "3 मील्स + 1 स्नैक + मिल्क",
                "सब कुछ जो घर में बन रहा है — हल्दी, जीरा पाउडर हल्का सीजनिंग ओके",
                "गाय का दूध अभी भी अवॉइड — 1 साल तक ब्रेस्टमिल्क/फॉर्मूला",
            ],
            "apply": [
                "ब्रश रूटीन सेट — रात के फीड के बाद ब्रश (दूध में शुगर — टूथ डिके होता है)",
                "कैविटी चेक: दांत पे काले दाग दिखें तो डेंटिस्ट (पेडियाट्रिक) दिखाएं",
            ],
            "sleep": "12-14 घंटे — 1 नैप सेटल होने लगती है",
            "milestones": "🎉 क्रूजिंग! (फर्नीचर पकड़ के साइड-साइड चलना), पहले शब्द! ('मामा' या 'पापा' — समझ के बोलता है)",
            "activity": "बॉल फेंकना, फूल दिखाना, नाम बताना ('ये कप है')",
        },
        {
            "title": "महीना 11 — चलने की प्रैक्टिस",
            "color": DARK_BLUE,
            "feeding": [
                "3 मील्स + 2 स्नैक्स + मिल्क",
                "अंडा (फुल) — अगर शुरू नहीं किया तो अब कर सकते हैं",
                "चीजें जो अवॉइड अभी भी: पूरा ड्राई फ्रूट (चोक रिस्क — पाउडर करें), पॉपकॉर्न, चिप्स, शहद, जूस",
            ],
            "apply": [
                "अब दांत 4-8 आ गए हैं — ब्रश 2 बार रोज नॉन-नेगोशिएबल",
                "नेल चेक — खुद चलने लगा है, पैर के नाखून भी काटें",
            ],
            "sleep": "12-13 घंटे — 1 नैप (दोपहर 2-3 घंटे)",
            "milestones": "एक हाथ से सपोर्ट से चलना, खुद बैठना-खड़ा होना, यूटेंसिल्स से खेलना (खाना थाल में फेंकना — नॉर्मल है, इग्नोर करें 😄)",
            "activity": "'गिव मी द बॉल' — इंस्ट्रक्शंस फॉलो करता है, स्टैकिंग रिंग्स",
        },
        {
            "title": "महीना 12 — 🎉 हैप्पी बर्थडे! चलने का महीना",
            "color": PINK,
            "feeding": [
                "अब गाय का दूध शुरू कर सकते हैं (डॉक्टर के हिसाब से) — 300-400 ml/दिन मैक्स (ज्यादा दूध = आयरन की कमी + खाना कम खाएगा)",
                "3 मील्स + 2 स्नैक्स — अब फैमिली के साथ टेबल पे बिठाएं — खाने की हैबिट्स अभी बनती हैं",
                "केक/चॉकलेट (बर्थडे के दिन) — कुछ चम्मच टेस्ट — ज्यादा नहीं (शुगर हैबिट मत डालो)",
            ],
            "apply": [
                "ब्रश 2 बार — राइस-ग्रेन फ्लोराइड टूथपेस्ट",
                "सनस्क्रीन रोज जब बाहर जाए",
                "अब फुल बाथ डेली हो सकता है",
            ],
            "sleep": "12-13 घंटे — रात को 10-11 घंटे सॉलिड स्लीप + 1 नैप",
            "milestones": "🎉 वॉकिंग! (कुछ बच्चे 9वें महीने में भी चल लेते हैं — लेट वॉकिंग 15-16 महीने तक नॉर्मल), 2-3 शब्द बोलना, खुद स्पून से खाना (गड़बड़ करेगा — होने दें!)",
            "activity": "राइम्स के साथ डांस, बॉल फेंकना-कैच करना, पिक्चर बुक्स दिखाना",
        },
    ]
    
    for i, month in enumerate(months_data_2):
        add_header_bar(story, f"🍼 अध्याय {i+8}: {month['title']}", month['color'])
        
        story.append(Paragraph("🍽️ फीडिंग (क्या खिलाना है):", styles['SectionTitle']))
        for item in month['feeding']:
            story.append(Paragraph(f"• {item}", styles['BulletHindi']))
        
        story.append(Paragraph("🧴 क्या लगाना चाहिए:", styles['SectionTitle']))
        for item in month['apply']:
            story.append(Paragraph(f"• {item}", styles['BulletHindi']))
        
        story.append(Paragraph(f"<b>😴 नींद:</b> {month['sleep']}", styles['BodyHindi']))
        story.append(Paragraph(f"<b>👶 माइलस्टोन्स:</b> {month['milestones']}", styles['BodyHindi']))
        story.append(Paragraph(f"<b>🎯 एक्टिविटी:</b> {month['activity']}", styles['BodyHindi']))
        
        story.append(Spacer(1, 8))
        if i < len(months_data_2) - 1:
            story.append(PageBreak())
    
    story.append(PageBreak())
    
    # ========== VACCINATION ==========
    add_header_bar(story, "💉 अध्याय 14: वैक्सीनेशन चार्ट (भारत का राष्ट्रीय कार्यक्रम)", DARK_BLUE)
    
    story.append(Paragraph(
        "यह चार्ट भारत सरकार के राष्ट्रीय टीकाकरण कार्यक्रम (UIP) पर आधारित है। हमेशा अपने बाल रोग विशेषज्ञ से पुष्टि करें क्योंकि कुछ वैक्सीन प्राइवेट में भी उपलब्ध होती हैं।",
        styles['BodyHindi']
    ))
    story.append(Spacer(1, 8))
    
    vax_headers = ["उम्र", "वैक्सीन", "नोट"]
    vax_rows = [
        ["जन्म पर", "BCG, Hepatitis B (Birth dose), OPV-0", "अस्पताल में"],
        ["6 हफ्ते", "DTwP/DTaP-1, IPV-1, Hep B-2, Hib-1, Rotavirus-1, PCV-1", "पहला प्रमुख शॉट"],
        ["10 हफ्ते", "DTwP/DTaP-2, IPV-2, Hib-2, Rotavirus-2, PCV-2", ""],
        ["14 हफ्ते", "DTwP/DTaP-3, IPV-3, Hib-3, Rotavirus-3, PCV-3", ""],
        ["6 महीने", "Influenza-1 (optional), Hep B-3", ""],
        ["7 महीने", "Influenza-2 (optional)", ""],
        ["9 महीने", "MMR-1, Typhoid Conjugate", ""],
        ["12 महीने", "Hepatitis A-1", ""],
    ]
    
    story.append(create_info_table(vax_headers, vax_rows, [1.2*inch, 3.8*inch, 1.4*inch]))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("💡 मां का नुस्खा:", styles['TipTitle']))
    story.append(Paragraph("• वैक्सीनेशन के दिन बेबी को अच्छी नींद दिलाएं, हल्का खाना खिलाएं", styles['BulletHindi']))
    story.append(Paragraph("• टीके के बाद हल्का बुखार आ सकता है — पैरासिटामोल सिरप डॉक्टर की सलाह से", styles['BulletHindi']))
    story.append(Paragraph("• इंजेक्शन वाली जगह पर ठंडा कपड़ा रख सकते हैं", styles['BulletHindi']))
    
    story.append(PageBreak())
    
    # ========== RED FLAGS ==========
    add_header_bar(story, "⚠️ अध्याय 15: रेड फ्लैग्स — कब डॉक्टर को दिखाएं", WARNING_RED)
    
    story.append(Paragraph(
        "ये संकेत दिखें तो तुरंत बाल रोग विशेषज्ञ या नजदीकी अस्पताल जाएं। इंतजार न करें।",
        styles['BodyHindi']
    ))
    story.append(Spacer(1, 8))
    
    emergency_items = [
        ("सांस लेने में समस्या", "सांस तेज, घरघराहट, पसलियां अंदर खिंच रही हों, नीले होंठ"),
        ("तेज बुखार", "3 महीने से कम उम्र में 100.4°F (38°C) या उससे ज्यादा"),
        ("फीडिंग रिफ्यूजल", "8-12 घंटे से कुछ नहीं खा रहा/पी रहा"),
        ("अत्यधिक उल्टी", "हरे या खून वाली उल्टी, या हर फीड के बाद जोरदार उल्टी"),
        ("डिहाइड्रेशन", "सूखे होंठ, धँसी आँखें, 6+ घंटे से पेशाब नहीं, फॉन्टानेल धँसा"),
        ("दौरे (Seizures)", "शरीर में झटके, आँखें ऊपर की ओर, होश खोना"),
        ("जॉन्डिस बढ़ना", "पीलापन फैल रहा हो, बेबी सुस्त हो"),
        ("नाभि से मवाद/खून", "लालिमा, बदबू, बुखार के साथ"),
        ("अत्यधिक रोना", "3+ घंटे लगातार, शांत न होना, पेट कठोर"),
        ("चोट/गिरना", "सिर पर चोट, उल्टी, सुस्ती, आँखों में बदलाव"),
    ]
    
    for title, desc in emergency_items:
        story.append(Paragraph(f"<b>🚨 {title}:</b> {desc}", styles['BodyHindi']))
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("📞 इमरजेंसी नंबर्स याद रखें:", styles['SectionTitle']))
    story.append(Paragraph("• एम्बुलेंस: 108 / 102", styles['BulletHindi']))
    story.append(Paragraph("• अपना बाल रोग विशेषज्ञ + नजदीकी अस्पताल का नंबर सेव रखें", styles['BulletHindi']))
    story.append(Paragraph("• पॉइजन कंट्रोल: 1800-116-117 (भारत)", styles['BulletHindi']))
    
    story.append(PageBreak())
    
    # ========== BONUSES ==========
    add_header_bar(story, "🎁 अध्याय 16: बोनस चेकलिस्ट्स (प्रिंटेबल)", PINK)
    
    story.append(Paragraph(
        "ये चेकलिस्ट्स प्रिंट करके रखें। रोज इस्तेमाल करें — ट्रैकिंग आसान हो जाएगी।",
        styles['BodyHindi']
    ))
    story.append(Spacer(1, 10))
    
    # Bonus 1
    story.append(Paragraph("1️⃣ फीडिंग ट्रैकर (एक दिन का)", styles['SectionTitle']))
    feed_headers = ["समय", "प्रकार (Breast/Formula)", "मात्रा / अवधि", "नोट्स"]
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
    story.append(Paragraph("2️⃣ न्यूबॉर्न शॉपिंग चेकलिस्ट", styles['SectionTitle']))
    shop_items = [
        "☐ कपड़े (बॉडीसूट, नाइटसूट, कैप, मिटन्स, सॉक्स) — 6-8 सेट",
        "☐ डायपर्स (न्यूबॉर्न साइज) + वेट वाइप्स (या कॉटन)",
        "☐ बेबी ब्लैंकेट / स्वैडल — 2-3",
        "☐ थर्मामीटर (डिजिटल)",
        "☐ नेल क्लिपर / फाइल",
        "☐ बेबी टब या स्पंज बाथ सेट",
        "☐ माइल्ड बेबी सोप + शैंपू",
        "☐ जिंक ऑक्साइड क्रीम (डायपर रैश)",
        "☐ नारियल/तिल तेल (मसाज)",
        "☐ कार सीट (एज-अप्रोप्रिएट)",
        "☐ स्ट्रोलर / कैरियर",
        "☐ बॉटल + स्टरलाइजर (अगर फॉर्मूला)",
    ]
    for item in shop_items:
        story.append(Paragraph(item, styles['BulletHindi']))
    
    story.append(Spacer(1, 12))
    
    # Bonus 3
    story.append(Paragraph("3️⃣ स्लीप लॉग (एक हफ्ते का)", styles['SectionTitle']))
    sleep_headers = ["दिन", "रात की नींद", "नैप 1", "नैप 2", "टोटल"]
    sleep_rows = [
        ["सोम", "____ घं", "____", "____", "____"],
        ["मंगल", "____ घं", "____", "____", "____"],
        ["बुध", "____ घं", "____", "____", "____"],
        ["गुरु", "____ घं", "____", "____", "____"],
        ["शुक्र", "____ घं", "____", "____", "____"],
        ["शनि", "____ घं", "____", "____", "____"],
        ["रवि", "____ घं", "____", "____", "____"],
    ]
    story.append(create_info_table(sleep_headers, sleep_rows, [1.1*inch, 1.3*inch, 1.2*inch, 1.2*inch, 1.1*inch]))
    
    story.append(PageBreak())
    
    # Bonus 4 & 5
    story.append(Paragraph("4️⃣ वैक्सीनेशन रिमाइंडर", styles['SectionTitle']))
    story.append(Paragraph("• जन्म: BCG, Hep B, OPV-0 — तारीख: __________", styles['BulletHindi']))
    story.append(Paragraph("• 6 हफ्ते: __________", styles['BulletHindi']))
    story.append(Paragraph("• 10 हफ्ते: __________", styles['BulletHindi']))
    story.append(Paragraph("• 14 हफ्ते: __________", styles['BulletHindi']))
    story.append(Paragraph("• 6 महीने: __________", styles['BulletHindi']))
    story.append(Paragraph("• 9 महीने: __________", styles['BulletHindi']))
    story.append(Paragraph("• 12 महीने: __________", styles['BulletHindi']))
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("5️⃣ इमरजेंसी कॉन्टैक्ट कार्ड", styles['SectionTitle']))
    story.append(Paragraph("• बाल रोग विशेषज्ञ: _________________ फोन: _______________", styles['BulletHindi']))
    story.append(Paragraph("• नजदीकी अस्पताल: _________________ फोन: _______________", styles['BulletHindi']))
    story.append(Paragraph("• एम्बुलेंस: 108", styles['BulletHindi']))
    story.append(Paragraph("• पिता/मां का अल्टरनेट नंबर: _________________", styles['BulletHindi']))
    story.append(Paragraph("• परिवार का इमरजेंसी कॉन्टैक्ट: _________________", styles['BulletHindi']))
    story.append(Paragraph("• ब्लड ग्रुप (बेबी): ________  एलर्जी: _______________", styles['BulletHindi']))
    
    story.append(Spacer(1, 20))
    
    # Final notes
    add_header_bar(story, "✅ हर महीने याद रखने वाली 3 बातें", TIP_GREEN)
    story.append(Paragraph("1. <b>वैक्सीनेशन चार्ट फॉलो करें</b> — कभी स्किप मत करें", styles['BodyHindi']))
    story.append(Paragraph("2. <b>वजन चेक:</b> हर महीने वजन नहीं बढ़ रहा तो डॉक्टर को दिखाएं", styles['BodyHindi']))
    story.append(Paragraph("3. <b>3 दिन रूल:</b> हर नया खाना 3 दिन तक — एलर्जी (दाने, उल्टी, लूज मोशन) हो तो रुक जाएं", styles['BodyHindi']))
    
    story.append(Spacer(1, 30))
    
    # Back cover message
    story.append(HRFlowable(width="100%", thickness=1.5, color=PINK, spaceBefore=10, spaceAfter=15))
    
    story.append(Paragraph(
        "CuddleNine के साथ",
        ParagraphStyle('Back1', fontName='NotoSans-Bold', fontSize=16, textColor=DARK_BLUE, alignment=TA_CENTER, spaceAfter=6)
    ))
    story.append(Paragraph(
        "Little Care, Big Love",
        ParagraphStyle('Back2', fontName='NotoDev', fontSize=14, textColor=PINK, alignment=TA_CENTER, spaceAfter=12)
    ))
    story.append(Paragraph(
        "आपका बेबी का पहला साल सुरक्षित, खुशहाल और प्यार भरा हो।<br/>यह गाइड सिर्फ शुरुआत है — हर बच्चा अलग होता है। हमेशा अपने डॉक्टर की सलाह लें।",
        ParagraphStyle('Back3', fontName='NotoDev', fontSize=10, textColor=MED_GRAY, alignment=TA_CENTER, leading=15)
    ))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "© CuddleNine  •  Educational Guide Only  •  Not a Substitute for Professional Medical Advice",
        ParagraphStyle('BackDisc', fontName='NotoSans', fontSize=7, textColor=MED_GRAY, alignment=TA_CENTER)
    ))
    
    # Build
    doc.build(story, canvasmaker=HeaderFooterCanvas)
    print(f"✅ PDF created successfully: {output_path}")
    return output_path


if __name__ == "__main__":
    build_pdf()
