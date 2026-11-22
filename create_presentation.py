"""
FreshWatch - PowerPoint Presentation Generator
Creates a professional, clean, non-AI-looking college project presentation.
Run:
    pip install python-pptx
    python create_presentation.py
"""

import sys

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
except ImportError:
    print("\n[!] 'python-pptx' is not installed.")
    print("    Please run:  py -3.13 -m pip install python-pptx")
    print("    Then re-run: py -3.13 create_presentation.py\n")
    sys.exit(1)

# Color Palette (Matches FreshWatch Dark/Emerald Modern Theme)
BG_DARK = RGBColor(14, 20, 18)       # #0e1412
CARD_DARK = RGBColor(24, 35, 31)     # #18231f
CARD_BORDER = RGBColor(38, 54, 46)   # #26362e
TEXT_LIGHT = RGBColor(240, 245, 242) # #f0f5f2
TEXT_MUTED = RGBColor(148, 165, 156) # #94a59c
ACCENT_GREEN = RGBColor(16, 185, 129)# #10b981
ALERT_RED = RGBColor(239, 68, 68)    # #ef4444
ALERT_AMBER = RGBColor(245, 158, 11) # #f59e0b

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_DARK

def add_header(slide, title_text, category="FRESHWATCH · COLLEGE MINI PROJECT"):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8.4), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ACCENT_GREEN

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_LIGHT

def add_card(slide, left, top, width, height, title, points, accent_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_DARK
    shape.line.color.rgb = accent_color if accent_color else CARD_BORDER
    shape.line.width = Pt(1.2)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.22)
    tf.margin_bottom = Inches(0.2)

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = accent_color if accent_color else TEXT_LIGHT

    for pt in points:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625) # 16:9 widescreen
    blank_layout = prs.slide_layouts[6]

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(8.0), Inches(3.0))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "SUPERMARKET INVENTORY INTELLIGENCE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    p = tf1.add_paragraph()
    p.text = "FreshWatch"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    p = tf1.add_paragraph()
    p.text = "Predictive Expiry & Wastage Prevention System Using Machine Learning"
    p.font.size = Pt(15)
    p.font.color.rgb = TEXT_MUTED

    p = tf1.add_paragraph()
    p.text = "\nDepartment of Computer Science & Engineering | Academic Mini-Project"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 2: Problem Statement & Practical Motivation
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement: The Perishable Inventory Dilemma")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(4.0), Inches(3.3), 
             "The Reality in Supermarkets", 
             [
                 "Retail grocery margins are thin (2% to 5%), making inventory write-offs disastrous.",
                 "Supermarkets lose 7-10% of dairy, fresh produce, and baked inventory to direct expiry.",
                 "Stock is written off as 100% loss once it crosses the expiration timestamp.",
                 "Discounts applied on the final day fail because footfall cannot absorb excess supply."
             ], ALERT_RED)

    add_card(s2, Inches(5.2), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Why Existing Methods Fail", 
             [
                 "Manual Audits: Labor-intensive; store staff visually inspect dates with high human error.",
                 "Traditional FIFO: Assumes uniform customer buying, ignoring product-specific sales dips.",
                 "Static Reordering: Reorders fixed quantities without factoring in dynamic shelf life.",
                 "Core Objective: Detect unsold surplus 3 to 7 days before expiry to allow staged liquidation."
             ], ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 3: Proposed Architecture & Workflow
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "System Architecture: End-to-End Execution Pipeline")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(2.6), Inches(3.3), 
             "1. Ingestion Layer", 
             [
                 "Supermarket POS log input (CSV or database).",
                 "Tracks 4 fundamental attributes:",
                 "• Current on-shelf stock",
                 "• Daily sales velocity (units/day)",
                 "• Days remaining to expiry date",
                 "• Unit retail price (INR)"
             ])

    add_card(s3, Inches(3.7), Inches(1.8), Inches(2.6), Inches(3.3), 
             "2. Feature & ML Core", 
             [
                 "Feature Engineering engine computes expected demand and surplus.",
                 "Trained Random Forest Classifier evaluates non-linear multi-attribute interactions.",
                 "Outputs exact wastage probability (0% to 100%).",
                 "Triages items into High, Medium, or Safe risk."
             ], ACCENT_GREEN)

    add_card(s3, Inches(6.6), Inches(1.8), Inches(2.6), Inches(3.3), 
             "3. Decision Engine", 
             [
                 "Automated rule-based action generation:",
                 "• 40% discount / Supplier return",
                 "• 20-30% discount / Bundle promotion",
                 "• End-cap shelf repositioning",
                 "Calculates estimated capital at risk (₹).",
                 "Streamlit dashboard & interactive tools."
             ])

    # -------------------------------------------------------------
    # SLIDE 4: Dataset & Feature Engineering
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Dataset Formulation & Mathematical Feature Engineering")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Dataset Synthesis & Realistic Noise", 
             [
                 "5,000 synthetic transaction records representing diverse supermarket inventory.",
                 "Simulates stock [5, 100], daily sales [0.5, 10.0], shelf life [1, 30 days].",
                 "Gaussian Noise added: N(mu=0, sigma=10) to mirror unexpected consumer demand drops.",
                 "Ground Truth Wastage: 1 if Stock > Expected Sales + Noise, else 0.",
                 "Partitioned into 80% Training (4,000 rows) and 20% Unseen Testing (1,000 rows)."
             ])

    add_card(s4, Inches(5.2), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Engineered Features (Why They Matter)", 
             [
                 "Raw values alone do not separate risk well; models struggle to learn products.",
                 "Engineered Feature 1: Expected Sales",
                 "  Formula: expected_sales = daily_sales * days_left",
                 "Engineered Feature 2: Projected Leftover Units",
                 "  Formula: leftover = stock - expected_sales",
                 "Gives the classifier pre-computed physics of supermarket liquidation capacity."
             ], ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 5: Machine Learning Benchmarks
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Model Evaluation & Algorithm Comparison")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Comparative Metrics (1,000 Test Records)", 
             [
                 "Random Forest Classifier (Selected):",
                 "• Accuracy: 95.6% | F1-Score: 0.9469",
                 "• Precision: 94.69% | Recall: 94.69%",
                 "Logistic Regression Benchmark:",
                 "• Accuracy: 95.5% | F1-Score: 0.9456",
                 "• Precision: 94.67% | Recall: 94.44%",
                 "Decision Tree Classifier (max_depth=6):",
                 "• Accuracy: 94.9% | F1-Score: 0.9377"
             ], ACCENT_GREEN)

    add_card(s5, Inches(5.2), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Why Random Forest was Chosen", 
             [
                 "Balanced Precision & Recall: Critical because false positives cause margin erosion, while false negatives cause food waste.",
                 "Ensemble Variance Reduction: Averages 100 decision trees to mitigate overfitting on synthetic noise.",
                 "Handles Non-Linear Boundary Shifts: Far more robust when expanding from synthetic data to real messy store logs.",
                 "Built-in Gini Impurity ranking for explainable AI."
             ])

    # -------------------------------------------------------------
    # SLIDE 6: Feature Importance & Explainability
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Explainable AI: Random Forest Feature Importance")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Gini Importance Weights", 
             [
                 "1. Leftover Units (59.87%):",
                 "   The primary predictor; immediately flags supply-demand mismatch.",
                 "2. Expected Sales (23.23%):",
                 "   Captures velocity multiplied by remaining shelf days.",
                 "3. Days Left (6.75%):",
                 "   Direct expiry urgency indicator.",
                 "4. Stock Level (6.46%):",
                 "   Current shelf footprint.",
                 "5. Daily Sales Rate (3.70%):",
                 "   Individual transaction speed."
             ], ACCENT_GREEN)

    add_card(s6, Inches(5.2), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Engineering Insights for Store Managers", 
             [
                 "High Stock is NOT automatically risky: Eggs with stock=50 and sales=8.0/day sell out completely (Safe).",
                 "Low Stock CAN be highly critical: Salmon with stock=10, sales=1.0/day, and 2 days left wastes 80% of units (High Risk).",
                 "Feature engineering accounts for 83.1% of the total predictive power.",
                 "Proves mathematically why manual single-variable audits fail."
             ])

    # -------------------------------------------------------------
    # SLIDE 7: Confusion Matrix & Financial Risk Analysis
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Confusion Matrix & Error Cost Breakdown")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Test Confusion Matrix (1,000 Items)", 
             [
                 "True Negatives (564):",
                 "• Correctly identified as safe to sell without discounting.",
                 "True Positives (392):",
                 "• Correctly identified as expiry risks in time to take action.",
                 "False Positives (22 - Type I Error):",
                 "• Unnecessary discount warning; cost is a small margin sacrifice.",
                 "False Negatives (22 - Type II Error):",
                 "• Missed items; cost is complete product write-off."
             ])

    add_card(s7, Inches(5.2), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Business Impact & ROI", 
             [
                 "94.69% Recall means out of every 100 items headed for the trash bin, FreshWatch catches ~95 in advance.",
                 "In an average supermarket inventory of 200,000 INR:",
                 "• Prevents estimated 20,000 - 30,000 INR of direct write-offs monthly.",
                 "Low False Alarm rate (2.2%) ensures store managers do not needlessly cannibalize profit margins."
             ], ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 8: Staged Action Engine & Pricing Rules
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Prescriptive Action Engine: Progressive Markdowns")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Automated Staged Pricing Strategy", 
             [
                 "Days Left <= 3 & High Risk (>= 80%):",
                 "• Action: 40% liquidation discount or return to supplier (RTV) today.",
                 "Days Left 4 to 7 & High Risk:",
                 "• Action: 20-30% discount or combine into promotional combo offers.",
                 "Days Left > 7 & High Risk:",
                 "• Action: Relocate to eye-level front shelf and apply modest 10-15% markdown.",
                 "Medium Risk (50% to 79%):",
                 "• Action: Place under watch, monitor daily rate.",
                 "Safe (< 50%): Standard retail price."
             ], ALERT_AMBER)

    add_card(s8, Inches(5.2), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Why Progressive Discounting Works", 
             [
                 "Recovers capital rather than writing off 100% dead loss.",
                 "Selling an item at a 30% discount still recovers the wholesale cost price (COGS).",
                 "Eliminates last-day panic dumping when consumers avoid items expiring in 2 hours.",
                 "Transparent recommendations allow floor managers to execute without data science expertise."
             ], ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 9: User Interface & Dashboard Architecture
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Dashboard Design & Technical Implementation")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Technical Stack & Design", 
             [
                 "Frontend: Streamlit with custom CSS variables.",
                 "Dark Mode by Default: Modern deep emerald palette (#0e1412) with light mode toggle.",
                 "High Contrast Controls: Custom styled buttons and cards for zero visual wash-out.",
                 "Visual KPI Bar: Dynamic segmented health bar for shelf health at a glance.",
                 "Data Grid: Interactive table with custom progress bars and CSV download."
             ])

    add_card(s9, Inches(5.2), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Interactive Capabilities", 
             [
                 "35 Comprehensive SKUs: Dairy, Bakery, Produce, Meats, Beverages, and Dry Goods.",
                 "Try a Product: What-if simulator to diagnose any custom item before stocking.",
                 "Assistant Chatbot: Rule-based natural query processing (e.g., 'What is most urgent?', 'Show money at risk').",
                 "Model Transparency Tab: Real-time confusion matrix and Altair feature importance plot."
             ], ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 10: Limitations & Future Enhancements
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Engineering Limitations & Future Scope")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Current Project Scope", 
             [
                 "Synthetic Dataset: Real POS sales logs were simulated due to commercial confidentiality.",
                 "Static Daily Velocity: Assumes flat daily sales, not yet factoring in weekend shopping spikes.",
                 "Independent Pricing: Does not model cannibalization between competing brands.",
                 "Batch CSV Input: Upload-driven rather than real-time scanner integration."
             ])

    add_card(s10, Inches(5.2), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Production Roadmap", 
             [
                 "Time-Series Forecasting: Integrate Prophet/ARIMA for dynamic day-of-week sales demand.",
                 "Computer Vision Scanner: Barcode & OCR expiry scanning via mobile camera.",
                 "Automated ERP Integration: Webhook synchronization with SAP/Tally POS databases.",
                 "Reinforcement Learning: Dynamically tune discount percentages to maximize revenue."
             ], ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 11: Conclusion & Key Learnings
    # -------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Project Summary & Key Takeaways")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Summary of Achievements", 
             [
                 "Achieved 95.6% classification accuracy with balanced 94.7% precision and recall.",
                 "Transformed theoretical ML classification into a practical managerial decision tool.",
                 "Built a fully functioning, high-contrast, theme-switchable production dashboard.",
                 "Demonstrated quantifiable economic viability for grocery retail management."
             ], ACCENT_GREEN)

    add_card(s11, Inches(5.2), Inches(1.8), Inches(4.0), Inches(3.3), 
             "Key Academic Takeaways", 
             [
                 "Feature engineering often yields higher practical returns than model hyper-parameter tuning.",
                 "Explainability (Feature Importance + Confusion Matrix) is mandatory for user trust in business tools.",
                 "Designing software with actionable recommendations (discounts/returns) provides far more value than simple raw metrics."
             ])

    # Save
    out_path = r"c:\Users\LENOVO\Desktop\expiry_project\FreshWatch_Presentation.pptx"
    prs.save(out_path)
    print(f"\n[+] Successfully generated presentation: {out_path}\n")

if __name__ == "__main__":
    main()
