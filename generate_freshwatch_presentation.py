import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation_with_photos():
    prs = Presentation()
    # 16:9 widescreen format
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette - Clean, Professional White & Deep Green
    BG_WHITE = RGBColor(255, 255, 255)
    BG_LIGHT = RGBColor(248, 250, 252)       # Soft off-white #F8FAFC
    GREEN_PRIMARY = RGBColor(6, 78, 59)      # Forest Green #064E3B
    GREEN_ACCENT = RGBColor(16, 185, 129)    # Emerald Accent #10B981
    GREEN_LIGHT = RGBColor(236, 253, 245)    # Mint light #ECFDF5
    GREEN_BORDER = RGBColor(167, 243, 208)   # Mint border #A7F3D0
    TEXT_MAIN = RGBColor(15, 23, 42)         # Charcoal Slate #0F172A
    TEXT_MUTED = RGBColor(100, 116, 139)     # Slate Grey #64748B
    CARD_BORDER = RGBColor(226, 232, 240)    # Light border #E2E8F0
    RED_ACCENT = RGBColor(220, 38, 38)       # Red #DC2626
    RED_BG = RGBColor(254, 242, 242)         # Red 50 #FEF2F2
    AMBER_ACCENT = RGBColor(217, 119, 6)     # Amber #D97706
    AMBER_BG = RGBColor(255, 251, 235)       # Amber 50 #FFFBEB

    IMG_DIR = "C:/Users/LENOVO/Desktop/expiry_project/presentation_images"

    def set_slide_background(slide, color=BG_LIGHT):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, category, title, subtitle=None):
        cat_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.4), Inches(8), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = GREEN_ACCENT
        p_cat.font.name = "Arial"

        title_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.72), Inches(11.5), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = GREEN_PRIMARY
        p_title.font.name = "Arial"

        if subtitle:
            sub_box = slide.shapes.add_textbox(Inches(0.9), Inches(1.32), Inches(11.5), Inches(0.4))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = TEXT_MUTED
            p_sub.font.name = "Arial"

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    def add_framed_image(slide, img_path, x, y, w, h):
        if os.path.exists(img_path):
            pic = slide.shapes.add_picture(img_path, x, y, w, h)
            return pic
        return None

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (WITH GENUINE MODERN SUPERMARKET PHOTO)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, BG_WHITE)

    # Top green accent bar
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = GREEN_PRIMARY
    top_bar.line.fill.background()

    # Project badge
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(0.65), Inches(3.6), Inches(0.35))
    badge.fill.solid()
    badge.fill.fore_color.rgb = GREEN_LIGHT
    badge.line.color.rgb = GREEN_BORDER
    btf = badge.text_frame
    bp = btf.paragraphs[0]
    bp.text = "COLLEGE MAJOR PROJECT PRESENTATION"
    bp.font.size = Pt(9.5)
    bp.font.bold = True
    bp.font.color.rgb = GREEN_PRIMARY
    bp.alignment = PP_ALIGN.CENTER

    # Title & Subtitle (Left block, width 7.4 inches)
    tbox = s1.shapes.add_textbox(Inches(0.9), Inches(1.15), Inches(7.4), Inches(2.0))
    tf = tbox.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Inventory Analysis 🥬"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = GREEN_PRIMARY
    p1.font.name = "Arial"

    p2 = tf.add_paragraph()
    p2.text = "AI-Powered Supermarket Expiry & Wastage Prediction System"
    p2.font.size = Pt(17)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MAIN
    p2.font.name = "Arial"

    p3 = tf.add_paragraph()
    p3.text = "Predict. Prevent. Save. — A smart system that stops food waste and saves supermarket money."
    p3.font.size = Pt(11.5)
    p3.font.color.rgb = TEXT_MUTED
    p3.font.name = "Arial"

    # Photo: Modern Fresh Produce Supermarket on Right
    img_s1 = os.path.join(IMG_DIR, "slide1_supermarket.jpg")
    add_framed_image(s1, img_s1, Inches(8.5), Inches(1.1), Inches(3.93), Inches(3.5))

    # 4 Quick Feature Cards in the middle
    feature_cards = [
        ("Smart Expiry Prediction", "Uses Machine Learning to find products that might expire soon."),
        ("Dynamic Discounts", "Recommends smart markdowns (10% to 40%) so items sell on time."),
        ("Voice AI Assistant", "Staff can simply speak in Hindi or English to check stock levels."),
        ("Modern Full-Stack", "Built with Next.js 14, Python FastAPI, and SQLite database.")
    ]

    card_w = Inches(1.75)
    for i, (head, desc) in enumerate(feature_cards):
        cx = Inches(0.9) + i * Inches(1.85)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(3.3), Inches(1.75), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_LIGHT
        card.line.color.rgb = CARD_BORDER

        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.12)
        ctf.margin_top = Inches(0.12)

        cp1 = ctf.paragraphs[0]
        cp1.text = head
        cp1.font.size = Pt(10.5)
        cp1.font.bold = True
        cp1.font.color.rgb = GREEN_PRIMARY

        cp2 = ctf.add_paragraph()
        cp2.text = desc
        cp2.font.size = Pt(8.5)
        cp2.font.color.rgb = TEXT_MAIN

    # Section Title for Team Members
    team_title_box = s1.shapes.add_textbox(Inches(0.9), Inches(4.95), Inches(11.5), Inches(0.35))
    ttf = team_title_box.text_frame
    ttp = ttf.paragraphs[0]
    ttp.text = "PROJECT TEAM MEMBERS"
    ttp.font.size = Pt(11)
    ttp.font.bold = True
    ttp.font.color.rgb = GREEN_PRIMARY
    ttp.font.name = "Arial"

    # 4 Equal Team Member Cards
    team_members = [
        "1. Sanskar Jaiswal",
        "2. Samar Mishra",
        "3. Shikhar Sahani",
        "4. Shravan Yadav"
    ]

    for i, name in enumerate(team_members):
        tx = Inches(0.9) + i * Inches(2.95)
        tcard = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tx, Inches(5.35), Inches(2.7), Inches(1.15))
        tcard.fill.solid()
        tcard.fill.fore_color.rgb = GREEN_LIGHT
        tcard.line.color.rgb = GREEN_BORDER
        tcard.line.width = Pt(1.5)

        tctf = tcard.text_frame
        tctf.word_wrap = True
        tctf.margin_left = tctf.margin_right = Inches(0.2)
        tctf.margin_top = Inches(0.22)

        tp1 = tctf.paragraphs[0]
        tp1.text = name
        tp1.font.size = Pt(13)
        tp1.font.bold = True
        tp1.font.color.rgb = GREEN_PRIMARY

        tp2 = tctf.add_paragraph()
        tp2.text = "Team Member"
        tp2.font.size = Pt(10)
        tp2.font.color.rgb = TEXT_MUTED

    add_notes(s1,
        "What to say on Slide 1:\n"
        "\"Good morning, teachers. Today our team is presenting our project, Inventory Analysis.\n"
        "Our team members are Sanskar Jaiswal, Samar Mishra, Shikhar Sahani, and Shravan Yadav.\n"
        "Inventory Analysis is an AI-powered system designed for supermarkets. Normal inventory tools only record food after it is thrown away. Inventory Analysis is different: it predicts which products will expire before they are sold, and suggests smart discounts so supermarkets can sell them on time and stop food waste.\""
    )

    # =========================================================================
    # SLIDE 2: THE REAL-WORLD PROBLEM (WITH GENUINE FOOD WASTE PHOTO)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Real Problem", "Why Do Supermarkets Waste So Much Food?",
               "Supermarkets throw away fresh food every day because current software warns them too late.")

    problems = [
        ("1. Warnings Come Too Late",
         "Regular software only alerts staff on the day food expires. By that time, the food is already spoiled, and the supermarket loses 100% of the money.",
         RED_BG, RED_ACCENT),
        ("2. Slow Sales Cause Waste",
         "Food does not spoil just because of its date. It spoils when a store has too much stock but customers are buying it too slowly.",
         AMBER_BG, AMBER_ACCENT),
        ("3. Manual Paper Checks",
         "Supermarket staff still walk around aisles with paper sheets to check expiry dates. It takes hours and many expiring items get missed.",
         GREEN_LIGHT, GREEN_PRIMARY)
    ]

    for i, (title, desc, bg, acc) in enumerate(problems):
        px = Inches(0.9) + i * Inches(3.9)
        pcard = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, Inches(1.85), Inches(3.7), Inches(2.9))
        pcard.fill.solid()
        pcard.fill.fore_color.rgb = bg
        pcard.line.color.rgb = CARD_BORDER

        ptf = pcard.text_frame
        ptf.word_wrap = True
        ptf.margin_left = ptf.margin_right = Inches(0.25)
        ptf.margin_top = Inches(0.25)

        p = ptf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = acc

        p_desc = ptf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = TEXT_MAIN

    # Lower Row: Banana Example (Width 8.1 in) + Genuine Food Waste Photo on Right (Width 3.1 in)
    ex_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(5.05), Inches(8.1), Inches(1.85))
    ex_box.fill.solid()
    ex_box.fill.fore_color.rgb = BG_WHITE
    ex_box.line.color.rgb = GREEN_ACCENT
    ex_box.line.width = Pt(1.5)

    etf = ex_box.text_frame
    etf.margin_left = Inches(0.25)
    etf.margin_top = Inches(0.18)
    ep1 = etf.paragraphs[0]
    ep1.text = "SIMPLE REAL-WORLD EXAMPLE: The 30-Unit Banana Problem"
    ep1.font.size = Pt(12)
    ep1.font.bold = True
    ep1.font.color.rgb = GREEN_PRIMARY

    ep2 = etf.add_paragraph()
    ep2.text = "• The Situation: A supermarket has 45 packs of bananas with only 3 days left. Customers buy 5 packs per day.\n" \
               "• Without Inventory Analysis: In 3 days, only 15 packs are sold. The remaining 30 packs spoil and get thrown into the garbage.\n" \
               "• With Inventory Analysis: The AI catches this on Day 1, suggests a 25% discount, customers buy them faster, and all 45 packs are sold with zero waste."
    ep2.font.size = Pt(10)
    ep2.font.color.rgb = TEXT_MAIN

    img_s2 = os.path.join(IMG_DIR, "slide2_food_waste.jpg")
    add_framed_image(s2, img_s2, Inches(9.3), Inches(5.05), Inches(3.13), Inches(1.85))

    add_notes(s2,
        "What to say on Slide 2:\n"
        "\"Supermarkets face a huge problem with food waste. Traditional software only warns staff after the food has already expired. By then, it is too late.\n"
        "Look at this simple example: If a shop has 45 bananas with 3 days left, but only sells 5 per day, 30 bananas will definitely spoil unless something is done.\n"
        "Inventory Analysis solves this by warning the manager 3 to 7 days ahead so they can take action early.\""
    )

    # =========================================================================
    # SLIDE 3: OUR SOLUTION: FRESHWATCH (WITH TABLET WORKER PHOTO)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Our Solution", "Inventory Analysis: Predict Before You Waste",
               "A single intelligent system that brings stock tracking, prediction, and pricing together.")

    # Banner (Width 8.2 in) + Photo on Right (Width 3.0 in)
    banner = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.85), Inches(8.2), Inches(0.85))
    banner.fill.solid()
    banner.fill.fore_color.rgb = GREEN_PRIMARY
    banner.line.fill.background()
    btf = banner.text_frame
    btf.margin_left = Inches(0.3)
    btf.margin_top = Inches(0.2)
    bp = btf.paragraphs[0]
    bp.text = "\"Inventory Analysis doesn't just track inventory. It helps predict problems before they become waste.\""
    bp.font.size = Pt(12)
    bp.font.bold = True
    bp.font.color.rgb = BG_WHITE

    img_s3 = os.path.join(IMG_DIR, "slide3_tablet_worker.jpg")
    add_framed_image(s3, img_s3, Inches(9.4), Inches(1.85), Inches(3.03), Inches(1.6))

    # 4 Simple Steps Below
    steps = [
        ("Step 1: Track Stock", "Records all items, expiry dates, purchase costs, and daily sales speed in our database.", GREEN_LIGHT),
        ("Step 2: Predict Risk", "Our Random Forest Machine Learning model calculates the exact chance of wastage.", BG_WHITE),
        ("Step 3: Smart Discounts", "Suggests 10% to 40% discounts or combo deals so products sell before spoiling.", BG_WHITE),
        ("Step 4: AI Voice Help", "Staff can speak to the system by voice in Hindi or English to check stock anytime.", GREEN_LIGHT)
    ]

    for i, (head, desc, bg) in enumerate(steps):
        sx = Inches(0.9) + i * Inches(2.95)
        step_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, Inches(3.6), Inches(2.75), Inches(3.2))
        step_box.fill.solid()
        step_box.fill.fore_color.rgb = bg
        step_box.line.color.rgb = CARD_BORDER

        stf = step_box.text_frame
        stf.word_wrap = True
        stf.margin_left = stf.margin_right = Inches(0.2)
        stf.margin_top = Inches(0.25)

        sp1 = stf.paragraphs[0]
        sp1.text = head
        sp1.font.size = Pt(13)
        sp1.font.bold = True
        sp1.font.color.rgb = GREEN_PRIMARY

        sp2 = stf.add_paragraph()
        sp2.text = desc
        sp2.font.size = Pt(10.5)
        sp2.font.color.rgb = TEXT_MAIN

    add_notes(s3,
        "What to say on Slide 3:\n"
        "\"Inventory Analysis works in four simple steps:\n"
        "1. It tracks all supermarket items and how fast they sell.\n"
        "2. Our Machine Learning model predicts which items might expire soon.\n"
        "3. It suggests smart discounts like 20% or 40% so customers buy them before they spoil.\n"
        "4. Workers can just ask questions by voice in Hindi or English, like 'How much milk or dal is left?'\""
    )

    # =========================================================================
    # SLIDE 4: KEY FEATURES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "System Features", "Main Features of Inventory Analysis",
               "A complete toolkit designed to help supermarket managers make smart decisions every day.")

    features = [
        ("Smart Dashboard", "Shows live cards with healthy stock, at-risk items, and estimated money saved. Includes simple charts showing weekly sales trends."),
        ("Inventory Manager", "Add, edit, and delete products easily. Managers can also upload an entire store inventory using a single Excel or CSV file."),
        ("One-Click Prediction", "Runs our Machine Learning model on all supermarket items with one click, showing which items need attention today."),
        ("Dynamic Pricing Advisor", "Suggests discounts like 10%, 25%, or 40% to clear stock. Managers can click one button to apply the new price to the shelf."),
        ("What-If Simulator", "Simple interactive sliders. Change the sales speed or expiry days to see what will happen before ordering new stock."),
        ("Voice AI Assistant", "Staff can speak by voice in Hindi, English, or Spanish. It gives accurate answers using real store data.")
    ]

    for i, (m_title, m_desc) in enumerate(features):
        col = i % 3
        row = i // 3
        mx = Inches(0.9) + col * Inches(3.9)
        my = Inches(1.85) + row * Inches(2.6)

        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, mx, my, Inches(3.7), Inches(2.4))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_WHITE
        card.line.color.rgb = CARD_BORDER

        mtf = card.text_frame
        mtf.word_wrap = True
        mtf.margin_left = mtf.margin_right = Inches(0.25)
        mtf.margin_top = Inches(0.25)

        p1 = mtf.paragraphs[0]
        p1.text = m_title
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = GREEN_PRIMARY

        p2 = mtf.add_paragraph()
        p2.text = m_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN

    add_notes(s4,
        "What to say on Slide 4:\n"
        "\"Inventory Analysis has six main features:\n"
        "First, a Smart Dashboard for daily alerts.\n"
        "Second, an Inventory Manager to add items or upload CSV files.\n"
        "Third, a Batch Prediction engine.\n"
        "Fourth, a Dynamic Pricing Advisor that recommends discounts.\n"
        "Fifth, an interactive Simulator with sliders to test different scenarios.\n"
        "And sixth, an AI Voice Calling Assistant that speaks Hindi and English.\""
    )

    # =========================================================================
    # SLIDE 5: WHAT MAKES FRESHWATCH DIFFERENT?
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Why We Are Different", "Old Inventory Tools vs. Inventory Analysis",
               "Comparing basic inventory tools (like Tally or simple spreadsheets) with Inventory Analysis.")

    table_shape = s5.shapes.add_table(6, 3, Inches(0.9), Inches(1.85), Inches(11.53), Inches(4.9))
    table = table_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(4.4)
    table.columns[2].width = Inches(4.53)

    diff_table = [
        ("Feature", "Traditional Inventory Systems (Tally / Basic Excel)", "Inventory Analysis Smart Platform"),
        ("When it acts", "Reactive: Records food waste *after* it is thrown into the garbage.", "Predictive: Warns 3 to 7 days *before* food expires so staff can act."),
        ("Product Pricing", "Fixed prices: Staff give random discounts at the very last minute.", "Smart Discounts: Suggests 10% to 40% discounts based on sales speed."),
        ("Technology Used", "Simple tables and manual spreadsheets.", "Machine Learning: Uses a trained Random Forest model (95.6% accuracy)."),
        ("Decision Help", "Just displays numbers; does not give solutions or advice.", "Interactive Simulator: Test what happens before buying or stocking items."),
        ("How Staff Use It", "Complicated computer screens that require special training.", "Voice Assistant: Staff can ask questions naturally in Hindi or English.")
    ]

    for row_idx, row in enumerate(diff_table):
        for col_idx, cell_text in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.text = cell_text
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Arial"
            if row_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = GREEN_PRIMARY
                p.font.size = Pt(11)
                p.font.bold = True
                p.font.color.rgb = BG_WHITE
            elif col_idx == 2:
                cell.fill.solid()
                cell.fill.fore_color.rgb = GREEN_LIGHT
                p.font.size = Pt(10)
                p.font.bold = True
                p.font.color.rgb = GREEN_PRIMARY
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = BG_WHITE
                p.font.size = Pt(10)
                p.font.color.rgb = TEXT_MAIN

    add_notes(s5,
        "What to say on Slide 5:\n"
        "\"Teachers often ask: What is the difference between Inventory Analysis and Tally?\n"
        "The biggest difference is that old tools are reactive—they only tell you what was wasted yesterday.\n"
        "Inventory Analysis is predictive—it tells you what will expire next week and gives you the exact discount to sell it.\n"
        "Also, old software requires complicated computer training, while Inventory Analysis lets any worker speak in Hindi to check stock.\""
    )

    # =========================================================================
    # SLIDE 6: MACHINE LEARNING & PREDICTION ENGINE (WITH DATA ANALYTICS PHOTO)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Machine Learning", "How the Machine Learning Model Works",
               "Our Random Forest model is trained to spot expiry risks with 95.6% accuracy.")

    metrics_data = [
        ("Accuracy", "95.6%", "Correctly identifies at-risk products", GREEN_LIGHT, GREEN_PRIMARY),
        ("Precision", "94.7%", "Very few false alarms", BG_WHITE, TEXT_MAIN),
        ("Recall", "94.7%", "Catches almost all items at risk", BG_WHITE, TEXT_MAIN),
        ("F1-Score", "94.7%", "Balanced and reliable score", GREEN_LIGHT, GREEN_PRIMARY)
    ]

    for i, (m_name, m_val, m_sub, bg, col_c) in enumerate(metrics_data):
        mx = Inches(0.9) + i * Inches(2.95)
        mcard = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, mx, Inches(1.85), Inches(2.75), Inches(1.25))
        mcard.fill.solid()
        mcard.fill.fore_color.rgb = bg
        mcard.line.color.rgb = CARD_BORDER

        mtf = mcard.text_frame
        mtf.margin_left = Inches(0.2)
        mtf.margin_top = Inches(0.16)
        p1 = mtf.paragraphs[0]
        p1.text = m_name.upper()
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_MUTED

        p2 = mtf.add_paragraph()
        p2.text = m_val
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = col_c

        p3 = mtf.add_paragraph()
        p3.text = m_sub
        p3.font.size = Pt(9)
        p3.font.color.rgb = TEXT_MUTED

    # 5 Features Card (Width 5.3 in)
    feat_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(3.3), Inches(5.3), Inches(3.7))
    feat_card.fill.solid()
    feat_card.fill.fore_color.rgb = BG_WHITE
    feat_card.line.color.rgb = CARD_BORDER
    ftf = feat_card.text_frame
    ftf.margin_left = Inches(0.25)
    ftf.margin_top = Inches(0.2)

    fp1 = ftf.paragraphs[0]
    fp1.text = "The 5 Simple Things Our Model Checks:"
    fp1.font.size = Pt(12.5)
    fp1.font.bold = True
    fp1.font.color.rgb = GREEN_PRIMARY

    simple_features = [
        ("1. leftover (Stock − Expected Sales)", "59.9% Importance", "The most important feature. If leftover is high, waste is high."),
        ("2. expected_sales (Daily Sales × Days)", "23.2% Importance", "How many units customers will buy before expiry."),
        ("3. days_left (Days to Expiry)", "6.8% Importance", "How many days remain until expiration."),
        ("4. stock (Units on Shelf)", "6.5% Importance", "Total quantity currently available."),
        ("5. daily_sales (Sales Speed)", "3.7% Importance", "How many units sell on an average day.")
    ]

    for fname, pct, fdesc in simple_features:
        fp = ftf.add_paragraph()
        fp.text = f"• {fname} ({pct}):\n   {fdesc}"
        fp.font.size = Pt(9)
        fp.font.color.rgb = TEXT_MAIN

    # Why Random Forest (Width 3.8 in) + Photo on Right (Width 2.2 in)
    rf_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.4), Inches(3.3), Inches(3.6), Inches(3.7))
    rf_card.fill.solid()
    rf_card.fill.fore_color.rgb = GREEN_LIGHT
    rf_card.line.color.rgb = GREEN_BORDER
    rtf = rf_card.text_frame
    rtf.margin_left = Inches(0.2)
    rtf.margin_top = Inches(0.2)

    rp1 = rtf.paragraphs[0]
    rp1.text = "Why Random Forest?"
    rp1.font.size = Pt(12.5)
    rp1.font.bold = True
    rp1.font.color.rgb = GREEN_PRIMARY

    rf_points = [
        "• 100 Decision Trees vote together for stable, accurate results.",
        "• Handles Non-Linear Risk: Spoilage jumps up fast when <= 3 days left.",
        "• Beat Other Models: Scored 95.6% accuracy, beating Decision Trees.",
        "• Real Mathematical Numbers: Probabilities come from Python model, not LLM guesses."
    ]

    for pt in rf_points:
        rp = rtf.add_paragraph()
        rp.text = pt
        rp.font.size = Pt(9.5)
        rp.font.color.rgb = TEXT_MAIN

    img_s6 = os.path.join(IMG_DIR, "slide6_data_analytics.jpg")
    add_framed_image(s6, img_s6, Inches(10.2), Inches(3.3), Inches(2.23), Inches(3.7))

    add_notes(s6,
        "What to say on Slide 6:\n"
        "\"This slide explains our Machine Learning model. We used a Random Forest Classifier with 100 trees.\n"
        "It achieved 95.6% accuracy and a 94.69% F1-score.\n"
        "The model checks 5 simple numbers: stock, daily sales, days left, expected sales, and leftover items.\n"
        "The most important number is 'leftover'—how many items will remain unsold when expiry day arrives. If leftover is high, the model alerts the manager immediately.\""
    )

    # =========================================================================
    # SLIDE 7: SMART PRICING & WASTE REDUCTION (WITH PRICE TAG PHOTO)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Smart Pricing", "Dynamic Discounts: Sell It Before It Spoils",
               "Inventory Analysis recommends smart discounts to help supermarkets sell items before they spoil.")

    pricing_tiers = [
        ("Urgent: 40% Discount", "When 3 or fewer days are left and risk is high.",
         "Action: Apply a 40% discount immediately so customers buy it today, or return it to the supplier.",
         RED_BG, RED_ACCENT),
        ("High Risk: 25% Discount", "When 4 to 7 days are left and stock is high.",
         "Action: Apply a 20% to 25% discount, or bundle items as a combo (for example: Milk + Bread bundle).",
         AMBER_BG, AMBER_ACCENT),
        ("Watchlist: 10% - 15% Discount", "When sales speed is slowing down.",
         "Action: Feature the item in weekly specials or move it to front entrance shelves to boost sales.",
         GREEN_LIGHT, GREEN_PRIMARY)
    ]

    for i, (t_name, t_trig, t_act, bg, acc) in enumerate(pricing_tiers):
        tx = Inches(0.9) + i * Inches(3.9)
        tcard = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tx, Inches(1.85), Inches(3.7), Inches(3.1))
        tcard.fill.solid()
        tcard.fill.fore_color.rgb = bg
        tcard.line.color.rgb = CARD_BORDER

        ttf = tcard.text_frame
        ttf.margin_left = ttf.margin_right = Inches(0.25)
        ttf.margin_top = Inches(0.25)

        p1 = ttf.paragraphs[0]
        p1.text = t_name
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = acc

        p2 = ttf.add_paragraph()
        p2.text = f"\nWhen to use:\n{t_trig}\n\nWhat to do:\n{t_act}"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_MAIN

    # Manager Control Box (Width 8.2 in) + Genuine Price Tag Photo on Right (Width 3.0 in)
    ctrl_box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(5.15), Inches(8.2), Inches(1.8))
    ctrl_box.fill.solid()
    ctrl_box.fill.fore_color.rgb = BG_WHITE
    ctrl_box.line.color.rgb = GREEN_PRIMARY
    ctrl_box.line.width = Pt(1.5)

    ctf = ctrl_box.text_frame
    ctf.margin_left = Inches(0.25)
    ctf.margin_top = Inches(0.18)
    cp1 = ctf.paragraphs[0]
    cp1.text = "IMPORTANT: The Supermarket Manager Has 100% Control"
    cp1.font.size = Pt(12)
    cp1.font.bold = True
    cp1.font.color.rgb = GREEN_PRIMARY

    cp2 = ctf.add_paragraph()
    cp2.text = "• Inventory Analysis does NOT change prices automatically behind your back.\n" \
               "• It shows: Original Price, Suggested Price, Discount %, and Money Saved.\n" \
               "• The manager reviews the recommendation and clicks 'Apply Discount to Shelf' to confirm the new price."
    cp2.font.size = Pt(10.5)
    cp2.font.color.rgb = TEXT_MAIN

    img_s7 = os.path.join(IMG_DIR, "slide7_price_tag.jpg")
    add_framed_image(s7, img_s7, Inches(9.4), Inches(5.15), Inches(3.03), Inches(1.8))

    add_notes(s7,
        "What to say on Slide 7:\n"
        "\"When an item is at risk of expiring, Inventory Analysis recommends three levels of smart discounts:\n"
        "1. 40% discount if only 3 days are left.\n"
        "2. 25% discount if 4 to 7 days are left, or bundling it into a breakfast combo like Milk and Bread.\n"
        "3. 10% discount if sales are simply slowing down.\n"
        "Important point: Inventory Analysis never changes prices without permission. The store manager always reviews the discount and clicks 'Apply' to confirm.\""
    )

    # =========================================================================
    # SLIDE 8: TECH STACK & ARCHITECTURE (NO STOCK PHOTOS - PURE CLEAN TECH)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Technologies Used", "How Inventory Analysis Is Built (Architecture)",
               "A clean, full-stack web application built using modern and reliable technologies.")

    tech_layers = [
        ("1. Frontend (What the User Sees)",
         "• Next.js 14 & React: Fast and responsive web pages.\n"
         "• Tailwind CSS: Clean green and white supermarket theme.\n"
         "• Collapsible Hamburger Menu (☰): Keeps the screen clean without a permanent sidebar.\n"
         "• Recharts: Interactive charts showing stock trends and risk categories.", GREEN_LIGHT),
        ("2. Backend (Data Processing)",
         "• Node.js & Next.js API Routes: Handles requests and runs calculations.\n"
         "• Prisma ORM: Connects safely to the database without raw SQL queries.", BG_WHITE),
        ("3. Database (Where Data is Saved)",
         "• SQLite (dev.db): Fast and zero-setup local database for products, alerts, and discounts.\n"
         "• PostgreSQL Ready: Can connect to cloud databases by changing one setting.", BG_WHITE),
        ("4. Machine Learning & AI Microservice",
         "• Python FastAPI (Port 8000): Dedicated service running our Random Forest model (`wastage_model.pkl`).\n"
         "• Groq API (LLaMA 3.3): Powers our AI Calling Assistant with natural voice and text answers.", GREEN_LIGHT)
    ]

    for i, (l_title, l_desc, bg) in enumerate(tech_layers):
        ly = Inches(1.85) + i * Inches(1.3)
        lbox = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), ly, Inches(11.53), Inches(1.18))
        lbox.fill.solid()
        lbox.fill.fore_color.rgb = bg
        lbox.line.color.rgb = CARD_BORDER

        ltf = lbox.text_frame
        ltf.word_wrap = True
        ltf.margin_left = Inches(0.3)
        ltf.margin_top = Inches(0.16)

        p1 = ltf.paragraphs[0]
        p1.text = l_title
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = GREEN_PRIMARY

        p2 = ltf.add_paragraph()
        p2.text = l_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN

    add_notes(s8,
        "What to say on Slide 8:\n"
        "\"Here is the technology stack we used to build Inventory Analysis:\n"
        "For the frontend, we used Next.js 14, React, and Tailwind CSS. We designed a clean hamburger drawer menu that opens only when clicked.\n"
        "For the backend and database, we used Node.js and Prisma ORM with SQLite.\n"
        "For Machine Learning, we built a Python FastAPI microservice that runs our Random Forest model on port 8000.\n"
        "For our AI voice assistant, we used the Groq API running LLaMA 3.3.\""
    )

    # =========================================================================
    # SLIDE 9: LIVE APPLICATION WALKTHROUGH
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Live Application", "How the Live Application Works",
               "Tested and running live on localhost:3000 with 40 real supermarket products.")

    live_cards = [
        ("Clean Full-Screen View",
         "The navigation menu stays hidden until the user clicks the hamburger icon (☰). This gives the manager a spacious, full-width screen without clutter."),
        ("40 Real Supermarket Products",
         "Loaded with authentic items: Basmati Rice, Toor Dal, Cow Milk, Paneer, Whole Wheat Bread, Bananas, Spinach, Strawberries, and Chicken Cuts."),
        ("Interactive What-If Sliders",
         "Managers can test decisions before ordering. Move sliders for stock, sales speed, and days left to see the wastage risk update in real time."),
        ("AI Calling Assistant in Hindi & English",
         "Includes a phone-call mode with a timer and voice speaking. Floor workers can simply speak into their microphone to check stock numbers.")
    ]

    for i, (head, desc) in enumerate(live_cards):
        col = i % 2
        row = i // 2
        lx = Inches(0.9) + col * Inches(5.9)
        ly = Inches(1.85) + row * Inches(2.6)

        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, lx, ly, Inches(5.63), Inches(2.4))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_WHITE
        card.line.color.rgb = CARD_BORDER

        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.3)
        ctf.margin_top = Inches(0.25)

        p1 = ctf.paragraphs[0]
        p1.text = head
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = GREEN_PRIMARY

        p2 = ctf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_MAIN

    add_notes(s9,
        "What to say on Slide 9:\n"
        "\"Here is how the live application works on our computer:\n"
        "First, it has a clean screen layout with a hidden hamburger menu.\n"
        "Second, we tested it with 40 real supermarket grocery items like pulses, rice, milk, paneer, and fruits.\n"
        "Third, managers can use simple sliders in our Simulator to test sales scenarios.\n"
        "Fourth, our AI Calling Assistant allows any worker to check stock by speaking in Hindi or English.\""
    )

    # =========================================================================
    # SLIDE 10: PRACTICAL BENEFITS (WITH FRESH PRODUCE PHOTO)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Business Value", "Why Should Supermarkets Use Inventory Analysis?",
               "Real business benefits: saves food, recovers lost revenue, and is easy for staff to use.")

    biz_benefits = [
        ("Cuts Food Waste by Over 70%",
         "Instead of throwing food into dumpsters, supermarkets sell items to customers at smart discounts before expiration.", GREEN_LIGHT),
        ("Recovers Lost Money",
         "Turns what would normally be a 100% financial write-off into recovered revenue. In our 40-item test, Inventory Analysis saved ₹18,066.", BG_WHITE),
        ("Easy for Any Worker to Use",
         "Store staff don't need computer training. They can simply speak into the AI Calling Assistant in Hindi to check pulse and dairy stock.", BG_WHITE),
        ("One-Click Reports & Printing",
         "Download Excel/CSV audit files or print inspection sheets with store manager signature lines in one click.", GREEN_LIGHT)
    ]

    # Left: 4 benefit cards (2 columns, width 3.9 in each, total 8.0 in)
    for i, (b_title, b_desc, bg) in enumerate(biz_benefits):
        col = i % 2
        row = i // 2
        bx = Inches(0.9) + col * Inches(4.1)
        by = Inches(1.85) + row * Inches(2.6)

        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, Inches(3.9), Inches(2.4))
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = CARD_BORDER

        btf = card.text_frame
        btf.word_wrap = True
        btf.margin_left = btf.margin_right = Inches(0.2)
        btf.margin_top = Inches(0.2)

        p1 = btf.paragraphs[0]
        p1.text = b_title
        p1.font.size = Pt(12.5)
        p1.font.bold = True
        p1.font.color.rgb = GREEN_PRIMARY

        p2 = btf.add_paragraph()
        p2.text = b_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN

    # Right: Photo of Beautiful Organized Fresh Produce Market
    img_s10 = os.path.join(IMG_DIR, "slide10_fresh_produce.jpg")
    add_framed_image(s10, img_s10, Inches(9.3), Inches(1.85), Inches(3.13), Inches(5.0))

    add_notes(s10,
        "What to say on Slide 10:\n"
        "\"Why is Inventory Analysis important in the real world?\n"
        "1. It reduces avoidable food waste by over 70%.\n"
        "2. It recovers money for the store. In our sample test, it helped recover ₹18,066.\n"
        "3. Any worker can use it because of our voice feature in Hindi and English.\n"
        "4. It provides one-click reports for store audits and management.\""
    )

    # =========================================================================
    # SLIDE 11: FUTURE PLANS & IMPROVEMENTS (WITH RETAIL TECH SCANNER PHOTO)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Future Scope", "Future Plans & Next Steps",
               "Practical improvements to scale Inventory Analysis to large commercial supermarket chains.")

    future_goals = [
        ("Barcode & Cash Register Sync", "Connect directly with barcode cash counters so stock numbers update instantly as customers make purchases.", BG_WHITE),
        ("Multi-Store Chain Management", "Connect multiple stores together so excess stock in one branch can be transferred to a busier branch before discounting.", GREEN_LIGHT),
        ("Weather & Festival Predictions", "Train the AI to predict higher sales during rainy days, weekends, and major festival seasons like Diwali or Eid.", GREEN_LIGHT),
        ("Automatic Supplier Return Notices", "Send automatic return forms to food suppliers for products that qualify for vendor returns before deadlines pass.", BG_WHITE)
    ]

    for i, (r_title, r_desc, bg) in enumerate(future_goals):
        col = i % 2
        row = i // 2
        rx = Inches(0.9) + col * Inches(4.1)
        ry = Inches(1.85) + row * Inches(2.6)

        card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rx, ry, Inches(3.9), Inches(2.4))
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = CARD_BORDER

        rtf = card.text_frame
        rtf.word_wrap = True
        rtf.margin_left = rtf.margin_right = Inches(0.2)
        rtf.margin_top = Inches(0.2)

        p1 = rtf.paragraphs[0]
        p1.text = f"Goal {i+1}: {r_title}"
        p1.font.size = Pt(12.5)
        p1.font.bold = True
        p1.font.color.rgb = GREEN_PRIMARY

        p2 = rtf.add_paragraph()
        p2.text = r_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MAIN

    img_s11 = os.path.join(IMG_DIR, "slide11_retail_tech.jpg")
    add_framed_image(s11, img_s11, Inches(9.3), Inches(1.85), Inches(3.13), Inches(5.0))

    add_notes(s11,
        "What to say on Slide 11:\n"
        "\"In the future, Inventory Analysis can be improved in four ways:\n"
        "First, connecting with barcode checkout scanners.\n"
        "Second, connecting multiple store branches to move extra stock.\n"
        "Third, predicting sales spikes during festivals or weather changes.\n"
        "Fourth, sending automatic return notices to food suppliers before deadlines.\""
    )

    # =========================================================================
    # SLIDE 12: CONCLUSION & THANK YOU
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, BG_WHITE)

    top_bar = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = GREEN_PRIMARY
    top_bar.line.fill.background()

    stmt_card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.0), Inches(11.53), Inches(2.0))
    stmt_card.fill.solid()
    stmt_card.fill.fore_color.rgb = GREEN_PRIMARY
    stmt_card.line.fill.background()

    stf = stmt_card.text_frame
    stf.margin_left = Inches(0.4)
    stf.margin_top = Inches(0.25)

    p1 = stf.paragraphs[0]
    p1.text = "Inventory Analysis: Predict Today. Act Smarter. Waste Less."
    p1.font.size = Pt(25)
    p1.font.bold = True
    p1.font.color.rgb = BG_WHITE
    p1.alignment = PP_ALIGN.CENTER

    p2 = stf.add_paragraph()
    p2.text = "Helping supermarkets save money and prevent food waste through simple, predictive Machine Learning."
    p2.font.size = Pt(12.5)
    p2.font.color.rgb = GREEN_BORDER
    p2.alignment = PP_ALIGN.CENTER

    takeaways = [
        ("Predictive AI", "Predicts expiry risks days ahead instead of waiting for food to spoil in the store."),
        ("Saves Money", "Recommends smart discounts (10% to 40%) that recover money and reduce waste by 70%+."),
        ("Easy & Practical", "Clean web app with a hidden hamburger menu and voice calling in Hindi and English.")
    ]

    for i, (thead, tdesc) in enumerate(takeaways):
        tx = Inches(0.9) + i * Inches(3.9)
        tcard = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tx, Inches(3.3), Inches(3.7), Inches(2.0))
        tcard.fill.solid()
        tcard.fill.fore_color.rgb = BG_LIGHT
        tcard.line.color.rgb = CARD_BORDER

        ttf = tcard.text_frame
        ttf.margin_left = ttf.margin_right = Inches(0.25)
        ttf.margin_top = Inches(0.22)

        tp1 = ttf.paragraphs[0]
        tp1.text = thead
        tp1.font.size = Pt(13)
        tp1.font.bold = True
        tp1.font.color.rgb = GREEN_PRIMARY

        tp2 = ttf.add_paragraph()
        tp2.text = tdesc
        tp2.font.size = Pt(10)
        tp2.font.color.rgb = TEXT_MAIN

    team_box = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(5.55), Inches(11.53), Inches(0.9))
    team_box.fill.solid()
    team_box.fill.fore_color.rgb = GREEN_LIGHT
    team_box.line.color.rgb = GREEN_BORDER
    team_tf = team_box.text_frame
    team_tf.margin_left = Inches(0.3)
    team_tf.margin_top = Inches(0.12)

    ttp1 = team_tf.paragraphs[0]
    ttp1.text = "PROJECT TEAM MEMBERS: Sanskar Jaiswal  •  Samar Mishra  •  Shikhar Sahani  •  Shravan Yadav"
    ttp1.font.size = Pt(11)
    ttp1.font.bold = True
    ttp1.font.color.rgb = GREEN_PRIMARY
    ttp1.alignment = PP_ALIGN.CENTER

    ttp2 = team_tf.add_paragraph()
    ttp2.text = "Thank You! We are happy to take your questions and show the live demo."
    ttp2.font.size = Pt(11)
    ttp2.font.color.rgb = TEXT_MAIN
    ttp2.alignment = PP_ALIGN.CENTER

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FreshWatch_Presentation.pptx")
    prs.save(out_path)
    # Also save a copy named Inventory_Analysis_Presentation.pptx
    ia_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Inventory_Analysis_Presentation.pptx")
    prs.save(ia_path)
    print(f"[+] Presentation saved to: {out_path} and {ia_path}")
    return out_path

if __name__ == "__main__":
    build_presentation_with_photos()
