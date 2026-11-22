import html
import json
import os
import re

import altair as alt
import joblib
import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FreshWatch AI", page_icon="🥬", layout="wide")

# ------------------------------------------------------------------
# Sidebar: Theme Selection & App Settings
# ------------------------------------------------------------------
st.sidebar.markdown("### 🎨 Display Theme")
theme_mode = st.sidebar.radio(
    "Choose Theme",
    options=["🌙 Dark", "☀️ Light"],
    index=0,
    horizontal=True,
    help="By default, FreshWatch runs in Dark mode. You can toggle to Light mode anytime.",
)
is_dark = theme_mode == "🌙 Dark"

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 Conversational AI Engine")
gemini_api_key = st.sidebar.text_input(
    "Gemini API Key (Optional for Gemini Calling)",
    type="password",
    value=os.environ.get("GEMINI_API_KEY", ""),
    help="Get a free key from aistudio.google.com to power full conversational Gemini Voice Calling. If left blank, FreshWatch runs its built-in Multi-Turn Reasoning Engine 100% offline!",
)

# Theme Palettes
if is_dark:
    PALETTE = {
        "High": {"main": "#ef4444", "soft": "rgba(239, 68, 68, 0.22)", "text": "#fca5a5"},
        "Medium": {"main": "#f59e0b", "soft": "rgba(245, 158, 11, 0.22)", "text": "#fcd34d"},
        "Safe": {"main": "#10b981", "soft": "rgba(16, 185, 129, 0.22)", "text": "#6ee7b7"},
    }
    GREEN = "#10b981"
    THEME_VARS = """
    :root {
        --bg: #0e1412;
        --sidebar-bg: #141c19;
        --card: #18231f;
        --card-hover: #1e2c27;
        --line: #26362e;
        --meter-bg: #22312a;
        --ink: #f0f5f2;
        --muted: #94a59c;
        --btn-bg: #23332c;
        --btn-text: #f0f5f2;
        --btn-border: #3b5247;
        --btn-hover-bg: #2c4037;
        --btn-hover-text: #ffffff;
        --btn-hover-border: #10b981;
        --primary: #10b981;
        --primary-hover: #059669;
        --hero-bg: linear-gradient(135deg, #122c21 0%, #17382b 100%);
        --hero-border: #23543e;
        --input-bg: #131c18;
        --input-border: #2c3e35;
        --input-text: #f0f5f2;
    }
    """
else:
    PALETTE = {
        "High": {"main": "#d64545", "soft": "#fbe7e4", "text": "#a52a2a"},
        "Medium": {"main": "#e0a526", "soft": "#fbf1d6", "text": "#7a5800"},
        "Safe": {"main": "#3f9a6e", "soft": "#e3f2ea", "text": "#22664a"},
    }
    GREEN = "#1f4d3a"
    THEME_VARS = """
    :root {
        --bg: #faf7f1;
        --sidebar-bg: #f1ebdd;
        --card: #fffdf8;
        --card-hover: #f7f2e7;
        --line: #e8dfcc;
        --meter-bg: #efe8d8;
        --ink: #1f2a24;
        --muted: #6b756e;
        --btn-bg: #ffffff;
        --btn-text: #1f2a24;
        --btn-border: #dcd4c3;
        --btn-hover-bg: #f5eee0;
        --btn-hover-text: #141d18;
        --btn-hover-border: #1f4d3a;
        --primary: #1f4d3a;
        --primary-hover: #17392b;
        --hero-bg: #1f4d3a;
        --hero-border: #17392b;
        --input-bg: #ffffff;
        --input-border: #dcd4c3;
        --input-text: #1f2a24;
    }
    """

REQUIRED = ["product", "stock", "daily_sales", "days_left"]


def flat(s):
    """Join multi-line HTML into one line so Markdown never breaks it."""
    return "".join(line.strip() for line in s.strip().splitlines())


# ------------------------------------------------------------------
# Global CSS Stylesheet
# ------------------------------------------------------------------
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&display=swap');

{THEME_VARS}

/* Base Body & App */
.stApp {{
    background-color: var(--bg) !important;
    color: var(--ink) !important;
}}

[data-testid="stSidebar"] {{
    background-color: var(--sidebar-bg) !important;
    border-right: 1px solid var(--line) !important;
}}

.stApp, .stApp p, .stApp label, .stApp li, .stApp span, .stApp div {{
    font-family: 'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif !important;
}}

.stApp p, .stApp label, .stApp li, .stApp span {{
    color: var(--ink);
}}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
    font-family: 'Fraunces', Georgia, serif !important;
    color: var(--ink) !important;
}}

[data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span {{
    color: var(--ink) !important;
}}

[data-testid="stDeployButton"], [data-testid="stAppDeployButton"], .stDeployButton,
footer, #MainMenu {{
    display: none !important;
}}

header[data-testid="stHeader"] {{
    background: transparent !important;
}}

.block-container {{
    max-width: 1200px;
    padding-top: 1.6rem;
    padding-bottom: 3.5rem;
}}

/* ---------- HERO BANNER ---------- */
.hero {{
    display: grid;
    grid-template-columns: 1.15fr .85fr;
    align-items: center;
    gap: 24px;
    background: var(--hero-bg);
    border: 1px solid var(--hero-border);
    border-radius: 26px;
    padding: 36px 44px;
    margin-bottom: 24px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}}
.hero .kick {{
    color: #e3b95c !important;
    font-weight: 700;
    font-size: .78rem;
    letter-spacing: .16em;
    text-transform: uppercase;
}}
.hero .ht {{
    font-family: 'Fraunces', Georgia, serif !important;
    color: #f7f1e3 !important;
    font-size: 2.6rem;
    line-height: 1.08;
    margin: 12px 0 14px 0;
    font-weight: 600;
}}
.hero .hp {{
    color: rgba(247, 241, 227, .88) !important;
    font-size: 1.01rem;
    max-width: 480px;
    line-height: 1.55;
}}
.hero svg {{
    width: 100%;
    height: auto;
    max-height: 240px;
    display: block;
}}
@media (max-width: 820px) {{
    .hero {{ grid-template-columns: 1fr; padding: 26px; }}
    .hero .art {{ display: none; }}
    .hero .ht {{ font-size: 2.0rem; }}
}}

/* ---------- SUMMARY TILES ---------- */
.tile {{
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    height: 100%;
    transition: transform 0.15s ease;
}}
.tile:hover {{
    transform: translateY(-2px);
}}
.tile .t {{
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--muted) !important;
    font-size: .85rem;
    font-weight: 600;
}}
.tile .d {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--c);
}}
.tile .n {{
    font-family: 'Fraunces', Georgia, serif;
    font-size: 2.3rem;
    font-weight: 600;
    color: var(--ink) !important;
    line-height: 1.15;
    margin-top: 6px;
}}
.tile .s {{
    color: var(--muted) !important;
    font-size: .82rem;
}}

/* ---------- STOCK HEALTH BAR ---------- */
.health {{
    display: flex;
    height: 14px;
    border-radius: 99px;
    overflow: hidden;
    gap: 3px;
    background: var(--meter-bg);
    margin: 20px 0 10px 0;
}}
.legend {{
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    color: var(--muted) !important;
    font-size: .85rem;
}}
.legend span {{
    color: var(--muted) !important;
}}
.legend i {{
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    margin-right: 7px;
}}

/* ---------- SECTION HEADINGS ---------- */
.sec {{
    margin: 32px 0 14px 0;
}}
.sec .st {{
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.55rem;
    font-weight: 600;
    color: var(--ink) !important;
}}
.sec .ss {{
    color: var(--muted) !important;
    font-size: .92rem;
    margin-top: 2px;
}}

/* ---------- PRODUCT CARDS ---------- */
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
    gap: 16px;
}}
.pcard {{
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 18px 20px 16px 20px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}
.pcard:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.14);
}}
.pcard .ptop {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.pcard .emo {{
    width: 48px;
    height: 48px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    background: var(--soft);
}}
.pcard .chip {{
    font-size: .78rem;
    font-weight: 700;
    padding: 5px 11px;
    border-radius: 99px;
    background: var(--soft);
    color: var(--tx);
}}
.pcard .pname {{
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--ink) !important;
    margin-top: 12px;
}}
.pcard .psub {{
    color: var(--muted) !important;
    font-size: .86rem;
    margin-top: 1px;
}}
.pcard .meter {{
    height: 8px;
    border-radius: 99px;
    background: var(--meter-bg);
    overflow: hidden;
    margin: 14px 0 6px 0;
}}
.pcard .meter div {{
    height: 100%;
    border-radius: 99px;
    background: var(--c);
}}
.pcard .pfoot {{
    display: flex;
    justify-content: space-between;
    color: var(--muted) !important;
    font-size: .82rem;
}}
.pcard .pfoot span {{
    color: var(--muted) !important;
}}
.pcard .pfoot b {{
    color: var(--tx) !important;
    font-size: .92rem;
}}
.pcard .todo {{
    background: var(--soft);
    color: var(--tx) !important;
    border-radius: 12px;
    padding: 10px 12px;
    font-weight: 700;
    font-size: .88rem;
    margin-top: 12px;
}}
.pcard .loss {{
    color: var(--muted) !important;
    font-size: .8rem;
    margin-top: 8px;
}}

/* Chips for safe products */
.chips span {{
    display: inline-block;
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 99px;
    padding: 7px 15px;
    margin: 0 8px 8px 0;
    font-size: .9rem;
    color: var(--ink) !important;
}}

/* Empty states */
.empty {{
    background: var(--card);
    border: 1px dashed var(--line);
    border-radius: 18px;
    padding: 24px;
    color: var(--muted) !important;
    text-align: center;
    font-size: .95rem;
}}

/* ---------- BUTTONS (CLEAR VISIBILITY & HIGH CONTRAST) ---------- */
.stButton > button,
button[data-testid="stBaseButton-secondary"],
[data-testid="stDownloadButton"] > button {{
    background-color: var(--btn-bg) !important;
    color: var(--btn-text) !important;
    border: 1px solid var(--btn-border) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 8px 16px !important;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.2s ease !important;
}}

.stButton > button:hover,
button[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stDownloadButton"] > button:hover {{
    background-color: var(--btn-hover-bg) !important;
    color: var(--btn-hover-text) !important;
    border-color: var(--btn-hover-border) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.16) !important;
}}

/* Primary Submit Buttons */
button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-primaryFormSubmit"] {{
    background-color: var(--primary) !important;
    color: #ffffff !important;
    border: 1px solid var(--primary) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 10px 20px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.2s ease !important;
}}

button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover {{
    background-color: var(--primary-hover) !important;
    border-color: var(--primary-hover) !important;
    transform: translateY(-1px) !important;
}}

/* Inputs & Selectboxes */
div[data-baseweb="input"] input,
div[data-baseweb="base-input"] input,
[data-testid="stChatInput"] textarea {{
    background-color: var(--input-bg) !important;
    color: var(--input-text) !important;
    border-color: var(--input-border) !important;
}}

div[data-baseweb="input"],
div[data-baseweb="base-input"] {{
    background-color: var(--input-bg) !important;
    border-color: var(--input-border) !important;
    border-radius: 8px !important;
}}

div[data-baseweb="select"] > div {{
    background-color: var(--input-bg) !important;
    color: var(--input-text) !important;
    border-color: var(--input-border) !important;
    border-radius: 8px !important;
}}
div[data-baseweb="select"] * {{
    color: var(--input-text) !important;
}}

/* Tabs */
.stTabs [role="tab"] {{
    color: var(--muted) !important;
    font-weight: 600 !important;
    padding: 10px 18px !important;
    font-size: 0.95rem !important;
}}
.stTabs [role="tab"][aria-selected="true"] {{
    color: var(--ink) !important;
}}
.stTabs [data-baseweb="tab-highlight"] {{
    background-color: var(--primary) !important;
}}
.stTabs [data-baseweb="tab-border"] {{
    background-color: var(--line) !important;
}}

/* Chat Messages */
[data-testid="stChatMessage"] {{
    background-color: var(--card) !important;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    margin-bottom: 12px !important;
}}

/* Metric Cards */
[data-testid="stMetric"] {{
    background-color: var(--card) !important;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
}}
[data-testid="stMetricValue"] {{
    color: var(--ink) !important;
}}
[data-testid="stMetricLabel"] {{
    color: var(--muted) !important;
}}

.foot {{
    color: var(--muted) !important;
    font-size: .82rem;
    margin-top: 56px;
    text-align: center;
    border-top: 1px solid var(--line);
    padding-top: 20px;
}}
</style>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def show_df(df, **kwargs):
    try:
        st.dataframe(df, width="stretch", hide_index=True, **kwargs)
    except Exception:
        st.dataframe(df, use_container_width=True, hide_index=True, **kwargs)


def show_chart(chart):
    try:
        st.altair_chart(chart, width="stretch")
    except Exception:
        st.altair_chart(chart, use_container_width=True)


@st.cache_resource
def load_model_and_metrics():
    """Load the saved model. If files are missing or incompatible, retrain automatically."""
    try:
        mdl = joblib.load("wastage_model.pkl")
        with open("metrics.json") as f:
            met = json.load(f)
        return mdl, met
    except Exception:
        from train_model import train
        return train(save=False)


model, metrics = load_model_and_metrics()

# Expanded Product Icons List (Including Pulses, Rice, Grains)
PRODUCT_ICONS = [
    ("rice", "🍚"), ("dal", "🥣"), ("pulse", "🌾"), ("atta", "🌾"), ("grain", "🌾"),
    ("milk", "🥛"), ("bread", "🍞"), ("curd", "🥣"), ("yogurt", "🥣"), ("yoghurt", "🥣"),
    ("paneer", "🧀"), ("cheese", "🧀"), ("butter", "🧈"), ("biscuit", "🍪"), ("cookie", "🍪"),
    ("juice", "🧃"), ("egg", "🥚"), ("chip", "🍟"), ("ice cream", "🍦"), ("chocolate", "🍫"),
    ("noodle", "🍜"), ("cold drink", "🥤"), ("drink", "🥤"), ("soda", "🥤"), ("water", "💧"),
    ("apple", "🍎"), ("banana", "🍌"), ("tomato", "🍅"), ("tea", "🍵"),
    ("coffee", "☕"), ("candy", "🍬"), ("cake", "🍰"), ("chicken", "🍗"), ("meat", "🥩"),
    ("fish", "🐟"), ("salmon", "🐟"), ("fruit", "🍓"), ("strawberry", "🍓"), ("spinach", "🥬"),
    ("veg", "🥦"), ("broccoli", "🥦"), ("pasta", "🍝"), ("pizza", "🍕"), ("mushroom", "🍄"),
    ("burger", "🍔"), ("bun", "🥯"), ("bagel", "🥯"), ("croissant", "🥐"), ("muffin", "🧁"),
    ("toast", "🍞"), ("sauce", "🥫"), ("jam", "🍓"), ("honey", "🍯"), ("oil", "🫒"),
    ("coconut", "🥥"), ("tofu", "🧊"), ("smoothie", "🥤"), ("orange", "🍊"), ("grape", "🍇"),
    ("carrot", "🥕"), ("capsicum", "🫑"), ("garlic", "🧄"), ("cream", "🥛"), ("pav", "🥖"),
]


def icon_for(name):
    n = str(name).lower()
    for key, emoji in PRODUCT_ICONS:
        if re.search(r"\b" + re.escape(key), n):
            return emoji
    return "📦"


# ------------------------------------------------------------------
# Prediction Logic
# ------------------------------------------------------------------
def build_features(df):
    f = df[["stock", "daily_sales", "days_left"]].astype(float).copy()
    f["expected_sales"] = f["daily_sales"] * f["days_left"]
    f["leftover"] = f["stock"] - f["expected_sales"]
    return f


def risk_level(chance, high_thr, med_thr):
    if chance >= high_thr:
        return "High"
    if chance >= med_thr:
        return "Medium"
    return "Safe"


def suggest_action(risk, days_left):
    if risk == "High":
        if days_left <= 3:
            return "Give a 40% discount or return to the supplier today"
        if days_left <= 7:
            return "Give a 20-30% discount or make a combo offer"
        return "Move to the front shelf and give a 10-15% discount"
    if risk == "Medium":
        return "Keep watching and place it in a visible spot"
    return "No action needed"


def short_action(risk, days_left):
    if risk == "High":
        if days_left <= 3:
            return "Discount 40% or return it"
        if days_left <= 7:
            return "Discount 20–30% or make a combo"
        return "Front shelf and 10–15% off"
    if risk == "Medium":
        return "Keep an eye on it"
    return "All good, no action needed"


def add_predictions(df, high_thr, med_thr):
    out = df.copy()
    out["wastage_chance"] = (model.predict_proba(build_features(out))[:, 1] * 100).round(0)
    out["risk"] = out["wastage_chance"].apply(lambda c: risk_level(c, high_thr, med_thr))
    out["action"] = out.apply(lambda r: suggest_action(r["risk"], r["days_left"]), axis=1)
    if "price" in out.columns:
        leftover_units = (out["stock"] - out["daily_sales"] * out["days_left"]).clip(lower=0)
        out["est_loss"] = (leftover_units * out["price"]).round(0)
    return out.sort_values("wastage_chance", ascending=False).reset_index(drop=True)


# ------------------------------------------------------------------
# Comprehensive Default Supermarket Catalog (40 Items With Staples)
# ------------------------------------------------------------------
def get_default_inventory():
    return pd.DataFrame([
        # --- Supermarket Staples (Pulses, Rice, Grains) ---
        {"product": "Royal Basmati Rice (5kg)", "stock": 45, "daily_sales": 2.5, "days_left": 60, "price": 420},
        {"product": "Toor Dal / Yellow Pulses (1kg)", "stock": 38, "daily_sales": 2.0, "days_left": 45, "price": 145},
        {"product": "Moong Dal / Green Gram Pulses (1kg)", "stock": 30, "daily_sales": 1.5, "days_left": 40, "price": 130},
        {"product": "Chana Dal / Bengal Gram Pulses (1kg)", "stock": 25, "daily_sales": 1.2, "days_left": 35, "price": 115},
        {"product": "Whole Wheat Chakki Atta (5kg)", "stock": 40, "daily_sales": 3.0, "days_left": 50, "price": 240},

        # --- Dairy & Chilled Items ---
        {"product": "Fresh Cow Milk (1L)", "stock": 24, "daily_sales": 3.0, "days_left": 3, "price": 32},
        {"product": "Whole Wheat Bread", "stock": 22, "daily_sales": 5.0, "days_left": 3, "price": 45},
        {"product": "Farm Eggs (Pack of 12)", "stock": 50, "daily_sales": 8.0, "days_left": 10, "price": 85},
        {"product": "Fresh Malai Paneer (200g)", "stock": 28, "daily_sales": 1.5, "days_left": 4, "price": 95},
        {"product": "Greek Yogurt Berry (200g)", "stock": 35, "daily_sales": 2.0, "days_left": 4, "price": 45},
        {"product": "Salted Table Butter (500g)", "stock": 30, "daily_sales": 2.5, "days_left": 25, "price": 58},
        {"product": "Mozzarella Cheese Block", "stock": 20, "daily_sales": 1.2, "days_left": 7, "price": 130},
        {"product": "Fresh Cream (250ml)", "stock": 18, "daily_sales": 1.2, "days_left": 5, "price": 65},
        {"product": "Organic Spiced Tofu (200g)", "stock": 18, "daily_sales": 1.0, "days_left": 4, "price": 75},
        {"product": "Almond Unsweetened Milk", "stock": 15, "daily_sales": 1.0, "days_left": 18, "price": 120},
        {"product": "Curd Cup Classic (400g)", "stock": 40, "daily_sales": 4.0, "days_left": 5, "price": 35},

        # --- Bakery & Fresh Snacks ---
        {"product": "French Butter Croissants (2pk)", "stock": 16, "daily_sales": 1.8, "days_left": 2, "price": 70},
        {"product": "Burger Buns Sesame (4pk)", "stock": 22, "daily_sales": 3.0, "days_left": 4, "price": 40},
        {"product": "Chocolate Chip Muffins (2pk)", "stock": 18, "daily_sales": 1.8, "days_left": 3, "price": 60},
        {"product": "Soft Pav Buns (Pack of 6)", "stock": 26, "daily_sales": 4.5, "days_left": 3, "price": 30},
        {"product": "Garlic Herb Toast Slices", "stock": 15, "daily_sales": 1.5, "days_left": 12, "price": 50},

        # --- Fresh Fruits & Vegetables ---
        {"product": "Robusta Bananas (1 Dozen)", "stock": 45, "daily_sales": 5.5, "days_left": 3, "price": 55},
        {"product": "Sweet Strawberries Box (250g)", "stock": 18, "daily_sales": 1.2, "days_left": 2, "price": 120},
        {"product": "Fresh Baby Spinach (250g)", "stock": 25, "daily_sales": 3.0, "days_left": 2, "price": 25},
        {"product": "White Button Mushrooms (200g)", "stock": 20, "daily_sales": 2.0, "days_left": 3, "price": 55},
        {"product": "Organic Salad Tomatoes (1kg)", "stock": 35, "daily_sales": 4.5, "days_left": 5, "price": 40},
        {"product": "Shimla Red Apples (1kg)", "stock": 40, "daily_sales": 3.5, "days_left": 14, "price": 160},
        {"product": "Fresh Broccoli Crown (500g)", "stock": 16, "daily_sales": 1.5, "days_left": 4, "price": 65},
        {"product": "Sweet Nagpur Oranges (1kg)", "stock": 32, "daily_sales": 3.0, "days_left": 10, "price": 90},

        # --- Fresh Meat & Seafood ---
        {"product": "Boneless Chicken Breast (500g)", "stock": 14, "daily_sales": 2.5, "days_left": 2, "price": 190},
        {"product": "Atlantic Salmon Fillet (250g)", "stock": 10, "daily_sales": 1.0, "days_left": 2, "price": 380},

        # --- Juices & Cold Beverages ---
        {"product": "Cold Pressed Orange Juice (500ml)", "stock": 28, "daily_sales": 2.0, "days_left": 4, "price": 85},
        {"product": "Tender Coconut Water (200ml)", "stock": 30, "daily_sales": 4.0, "days_left": 9, "price": 50},
        {"product": "Cold Brew Hazelnut Coffee", "stock": 18, "daily_sales": 1.5, "days_left": 5, "price": 99},
        {"product": "Alphonso Mango Smoothie", "stock": 22, "daily_sales": 2.0, "days_left": 4, "price": 75},

        # --- Packaged Staples & Snacks ---
        {"product": "Digestive Wheat Biscuits", "stock": 65, "daily_sales": 4.0, "days_left": 45, "price": 30},
        {"product": "Spicy Masala Potato Chips", "stock": 50, "daily_sales": 5.0, "days_left": 30, "price": 20},
        {"product": "70% Dark Cocoa Chocolate", "stock": 35, "daily_sales": 1.5, "days_left": 60, "price": 95},
        {"product": "Instant Masala Noodles (4pk)", "stock": 80, "daily_sales": 7.0, "days_left": 40, "price": 56},
        {"product": "Pure Mountain Honey (250g)", "stock": 25, "daily_sales": 0.8, "days_left": 90, "price": 145},
    ])


def load_inventory(uploaded):
    if uploaded is None:
        return get_default_inventory(), None
    try:
        df = pd.read_csv(uploaded)
        df.columns = [c.strip().lower() for c in df.columns]
        missing = [c for c in REQUIRED if c not in df.columns]
        if missing:
            return None, f"Your CSV is missing these columns: {', '.join(missing)}"
        keep = REQUIRED + (["price"] if "price" in df.columns else [])
        df = df[keep].copy()
        for col in keep[1:]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna()
        if df.empty:
            return None, "No valid rows found in your CSV."
        return df, None
    except Exception as exc:
        return None, f"Could not read the CSV: {exc}"


# ------------------------------------------------------------------
# HTML Components
# ------------------------------------------------------------------
HERO = flat(
    """
<div class="hero">
  <div>
    <div class="kick">Predictive Supermarket Intelligence</div>
    <div class="ht">Sell it before it expires.</div>
    <div class="hp">FreshWatch is a forward-looking machine learning system that predicts perishable
    stockouts and spoilage before they occur, prescribing staged markdowns and conversational voice-enabled inventory calling.</div>
  </div>
  <div class="art">
  <svg viewBox="0 0 380 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Store shelves">
  <rect x="14" y="10" width="352" height="214" rx="16" fill="#1b4938"/>
  <rect x="14" y="88" width="352" height="8" fill="#e9dfc4"/>
  <rect x="14" y="160" width="352" height="8" fill="#e9dfc4"/>
  <rect x="14" y="224" width="352" height="8" rx="4" fill="#e9dfc4"/>
  <path d="M38 88V40l12-12h26l12 12v48z" fill="#f7f1e3"/><rect x="38" y="52" width="50" height="22" fill="#6aa5d9"/>
  <path d="M104 88V40l12-12h26l12 12v48z" fill="#f7f1e3"/><rect x="104" y="52" width="50" height="22" fill="#e3b95c"/>
  <rect x="182" y="46" width="30" height="42" rx="6" fill="#d98c5f"/><rect x="190" y="30" width="14" height="18" rx="3" fill="#d98c5f"/>
  <rect x="226" y="52" width="46" height="36" rx="8" fill="#9bc4a8"/><rect x="226" y="44" width="46" height="10" rx="4" fill="#f7f1e3"/>
  <ellipse cx="68" cy="140" rx="42" ry="20" fill="#d9a35f"/>
  <path d="M50 134q8 -8 16 0M70 132q8 -8 16 0" stroke="#b9803f" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M130 160l6-40h34l6 40z" fill="#f7f1e3"/><rect x="132" y="132" width="42" height="12" fill="#e08a7a"/>
  <path d="M190 160l6-40h34l6 40z" fill="#f7f1e3"/><rect x="192" y="132" width="42" height="12" fill="#9bc4a8"/>
  <rect x="262" y="112" width="44" height="48" rx="8" fill="#e3b95c"/><rect x="262" y="126" width="44" height="14" fill="#f7f1e3"/>
  <rect x="36" y="178" width="56" height="46" rx="4" fill="#d98c5f"/><rect x="36" y="190" width="56" height="10" fill="#f7f1e3"/>
  <rect x="104" y="188" width="34" height="36" rx="6" fill="#6aa5d9"/>
  <rect x="146" y="188" width="34" height="36" rx="6" fill="#9bc4a8"/>
  <rect x="188" y="188" width="34" height="36" rx="6" fill="#e3b95c"/>
  <rect x="236" y="176" width="64" height="48" rx="4" fill="#f7f1e3"/><rect x="236" y="190" width="64" height="12" fill="#c8643a"/>
  <g transform="translate(300 14)"><path d="M30 0v26" stroke="#f7f1e3" stroke-width="3"/>
  <circle cx="30" cy="52" r="28" fill="#c8643a" stroke="#f7f1e3" stroke-width="4"/>
  <path d="M30 52V36M30 52l12 8" stroke="#f7f1e3" stroke-width="4" stroke-linecap="round"/></g>
  </svg>
  </div>
</div>
"""
)


def tile(label, value, sub, color):
    return flat(
        f'<div class="tile" style="--c:{color}"><div class="t"><span class="d"></span>{label}</div>'
        f'<div class="n">{value}</div><div class="s">{sub}</div></div>'
    )


def health_bar(n_high, n_med, n_safe):
    total = max(n_high + n_med + n_safe, 1)
    parts = [("High", n_high, "Act today"), ("Medium", n_med, "Keep watching"), ("Safe", n_safe, "Looking fine")]
    segs = "".join(
        f'<div style="width:{n / total * 100:.1f}%;background:{PALETTE[k]["main"]}"></div>'
        for k, n, _ in parts if n > 0
    )
    legend = "".join(
        f'<span><i style="background:{PALETTE[k]["main"]}"></i>{label} · {n}</span>'
        for k, n, label in parts
    )
    return flat(f'<div class="health">{segs}</div><div class="legend">{legend}</div>')


def section(title, sub):
    return flat(f'<div class="sec"><div class="st">{title}</div><div class="ss">{sub}</div></div>')


def product_card(r):
    pal = PALETTE[r["risk"]]
    chance = int(r["wastage_chance"])
    days = int(r["days_left"])
    if days <= 0:
        when = "Expires today"
    elif days == 1:
        when = "Expires tomorrow"
    else:
        when = f"{days} days left"
    loss = ""
    if ("est_loss" in r.index and pd.notna(r["est_loss"]) and r["est_loss"] > 0
            and r["risk"] != "Safe"):
        loss = f'<div class="loss">About ₹{int(r["est_loss"]):,} could go to waste</div>'
    return flat(
        f'<div class="pcard" style="--c:{pal["main"]};--soft:{pal["soft"]};--tx:{pal["text"]}">'
        f'<div class="ptop"><div class="emo">{icon_for(r["product"])}</div><div class="chip">{when}</div></div>'
        f'<div class="pname">{html.escape(str(r["product"]))}</div>'
        f'<div class="psub">{int(r["stock"])} in stock · {r["daily_sales"]:.1f} sold/day</div>'
        f'<div class="meter"><div style="width:{chance}%"></div></div>'
        f'<div class="pfoot"><span>Chance it goes to waste</span><b>{chance}%</b></div>'
        f'<div class="todo">{short_action(r["risk"], days)}</div>{loss}</div>'
    )


# ------------------------------------------------------------------
# Multi-Turn Context-Aware Query Engine & Gemini Live Bridge
# ------------------------------------------------------------------
def pretty(df):
    return df.rename(
        columns={
            "product": "Product", "stock": "Stock", "daily_sales": "Daily sales",
            "days_left": "Days left", "wastage_chance": "Wastage chance (%)",
            "risk": "Risk", "action": "Suggested action",
            "price": "Price (₹)", "est_loss": "Estimated loss (₹)",
        }
    ).copy()


ALIASES = {
    "rice": ["rice", "chawal", "चावल", "arroz", "riz", "reis", "arisi", "biyyam", "basmati"],
    "pulse": ["pulse", "pulses", "dal", "daal", "दाल", "दालें", "lenteja", "lentejas", "lentil", "gram", "toor", "moong", "chana"],
    "milk": ["milk", "doodh", "दूध", "leche", "lait", "milch", "paal"],
    "bread": ["bread", "roti", "ब्रेड", "pan", "pain", "brot", "bun", "pav", "croissant"],
    "paneer": ["paneer", "cottage cheese", "पनीर", "queso"],
    "egg": ["egg", "eggs", "anda", "अंडा", "अंडे", "huevo", "oeuf", "ei", "muttai"],
    "banana": ["banana", "bananas", "kela", "केला", "plátano", "banane"],
    "tomato": ["tomato", "tomatoes", "tamatar", "टमाटर", "tomate"],
    "chicken": ["chicken", "murga", "चिकन", "pollo", "poulet", "hähnchen"],
    "salmon": ["salmon", "fish", "machli", "मछली", "pescado", "poisson"],
    "butter": ["butter", "makkhan", "मक्खन", "mantequilla", "beurre"],
    "yogurt": ["yogurt", "curd", "dahi", "दही"],
    "flour": ["atta", "flour", "wheat", "गेहूं", "आटा", "harina"],
    "mushroom": ["mushroom", "mushrooms", "khumb"],
    "spinach": ["spinach", "palak", "पालक", "espinaca"],
    "apple": ["apple", "apples", "seb", "सेब", "manzana", "pomme"],
    "coffee": ["coffee", "cafe", "कॉफ़ी", "kaffee"],
    "juice": ["juice", "ras", "जूस", "zumo", "jus"],
    "honey": ["honey", "shehed", "शहद", "miel", "honig"],
    "noodle": ["noodle", "noodles", "maggi", "ramen"],
}


def find_matching_products(q, data):
    q_clean = q.lower().strip()
    words = re.findall(r"\w+", q_clean)
    matches = []

    # 1. Alias match
    matched_keys = set()
    for standard_key, syn_list in ALIASES.items():
        if any(syn in q_clean for syn in syn_list):
            matched_keys.add(standard_key)

    for idx, row in data.iterrows():
        p_name = str(row["product"]).lower()
        if any(mk in p_name for mk in matched_keys):
            matches.append(row)
            continue
        for w in words:
            if len(w) >= 3 and w in p_name:
                matches.append(row)
                break

    if matches:
        return pd.DataFrame(matches).drop_duplicates(subset=["product"])
    return pd.DataFrame()


def query_gemini_calling(question, data, api_key, conversation_history):
    """Conversational Gemini 1.5 Flash query with full multi-turn memory & live inventory grounding."""
    try:
        inv_summary = []
        for _, r in data.iterrows():
            inv_summary.append(
                f"- {r['product']}: Stock={int(r['stock'])}, DailySales={r['daily_sales']:.1f}/day, "
                f"DaysLeft={int(r['days_left'])}, Price=₹{int(r.get('price', 0))}, "
                f"Risk={r['risk']} ({int(r['wastage_chance'])}% waste chance), Action={r['action']}"
            )
        inv_text = "\n".join(inv_summary)

        sys_prompt = f"""You are FreshWatch AI, an expert supermarket inventory intelligence assistant on a live phone call with the store manager.
You have access to the exact live database of 40 products with their current stock, daily sales velocity, days until expiration, unit price, wastage probability predicted by our Random Forest ML model, and recommended markdown action.

Live Supermarket Database:
{inv_text}

Rules for Your Voice Responses:
1. Speak directly in the caller's language (Hindi, English, Spanish, etc.) naturally and conversationally.
2. Keep responses brief (1-3 spoken sentences), ideal for an audio phone call.
3. Be completely grounded in the database numbers. Never hallucinate fake quantities or prices.
4. Handle follow-up cross-questions seamlessly (e.g. if the caller says "What about paneer?" and then asks "When will it expire?" or "Why is the risk high?").
5. Explain 'Why': if asked why a product has high wastage risk, explain that stock exceeds expected sales before expiry!"""

        contents = []
        # Add history
        for m in conversation_history[-6:]:  # Keep last 3 turns
            contents.append({
                "role": "user" if m["role"] == "user" else "model",
                "parts": [{"text": m["text"]}]
            })
        contents.append({"role": "user", "parts": [{"text": question}]})

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "system_instruction": {"parts": [{"text": sys_prompt}]},
            "contents": contents,
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 200}
        }
        res = requests.post(url, headers=headers, json=payload, timeout=8)
        if res.status_code == 200:
            ans = res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            # Find any matched product to show table
            matched = find_matching_products(question, data)
            tbl = pretty(matched) if not matched.empty else None
            return ans, tbl
        else:
            return None, None
    except Exception:
        return None, None


def smart_multiturn_reply(question, data, api_key=""):
    """Context-aware multi-turn reasoning engine with Gemini Live integration and pronoun resolution."""
    if "context_product" not in st.session_state:
        st.session_state.context_product = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 1. Try Gemini API first if key provided
    if api_key and api_key.strip():
        gemini_ans, gemini_tbl = query_gemini_calling(question, data, api_key.strip(), st.session_state.chat_history)
        if gemini_ans:
            return gemini_ans, gemini_tbl

    # 2. Local Multi-Turn & Cross-Question Reasoning Engine
    q = question.lower()
    high = data[data["risk"] == "High"]
    medium = data[data["risk"] == "Medium"]
    safe = data[data["risk"] == "Safe"]

    # Check for direct product mention
    matched_df = find_matching_products(question, data)

    # Detect cross-question pronouns (e.g., "it", "its", "this", "why", "इसकी", "इसका", "क्यों", "este", "por qué")
    is_pronoun_ref = any(w in q for w in ["it", "its", "this", "that", "why", "इसकी", "इसका", "क्यों", "इसे", "esto", "este", "por qué", "vence", "expire"])
    
    # If no product in query, but pronoun used and we have context_product:
    if matched_df.empty and is_pronoun_ref and st.session_state.context_product:
        p_row = data[data["product"] == st.session_state.context_product]
        if not p_row.empty:
            matched_df = p_row

    if not matched_df.empty:
        # Save focused product to context memory
        st.session_state.context_product = matched_df.iloc[0]["product"]
        p = matched_df.iloc[0]
        name = p["product"]
        stock = int(p["stock"])
        days = int(p["days_left"])
        rate = p["daily_sales"]
        price = int(p.get("price", 0))
        risk = p["risk"]
        chance = int(p["wastage_chance"])
        action = p["action"]
        expected = rate * days
        leftover = max(stock - expected, 0)
        loss = int(leftover * price)

        is_hindi = any(w in question for w in ["कितना", "स्टॉक", "कब", "एक्सपायर", "दाल", "चावल", "दाम", "कीमत", "बचा", "क्यों", "इसकी", "इसका"])
        is_spanish = any(w in q for w in ["cuanto", "cuánto", "arroz", "lenteja", "caduca", "vence", "precio", "queda", "por qué", "este"])

        # Cross-question: "Why is the risk so high?" / "Why?"
        if any(w in q for w in ["why", "reason", "kyun", "क्यों", "por qué"]):
            if is_hindi:
                ans = f"**{name}** का वेस्टेज जोखिम {chance}% क्यों है? क्योंकि स्टॉक **{stock} पैकेट** है और बिक्री दर मात्र **{rate:.1f} पैकेट/दिन** है। {days} दिनों में सिर्फ **{int(expected)} पैकेट** बिकेंगे, जिससे **{int(leftover)} पैकेट (₹{loss:,})** सीधे एक्सपायर होकर बर्बाद हो जाएंगे!"
            elif is_spanish:
                ans = f"¿Por qué **{name}** tiene {chance}% de riesgo? Porque tiene **{stock} unidades** y solo vende **{rate:.1f}/día**. En {days} días solo se venderán **{int(expected)}**, dejando **{int(leftover)} unidades (₹{loss:,})** en merma total."
            else:
                ans = f"**Why {name} is at {chance}% risk:** You have **{stock} units**, but with a sales velocity of only **{rate:.1f} units/day**, you will only sell **{int(expected)} units** before the {days}-day expiry deadline! That leaves **{int(leftover)} units (₹{loss:,} loss)** to spoil on the shelf."
            return ans, pretty(matched_df)

        # Cross-question: "What should I do?" / "What action?" / "What discount?"
        if any(w in q for w in ["action", "what should", "discount", "kya kare", "क्या करें", "qué hacer"]):
            if is_hindi:
                ans = f"**{name}** के लिए तुरंत सुझाव: **{action}**। अगर आप 25-30% डिस्काउंट देंगे तो बिक्री दर बढ़कर सारा स्टॉक समय से पहले बिक जाएगा।"
            else:
                ans = f"**Recommended Action for {name}:** {action}. Applying this markdown immediately accelerates daily velocity to liquidate the {int(leftover)} surplus units before expiry."
            return ans, pretty(matched_df)

        # Cross-question: Expiry timeline
        if any(w in q for w in ["expire", "expiry", "when", "days left", "kab", "कब", "vence", "caduca"]):
            if is_hindi:
                ans = f"**{name}** की एक्सपायरी में **{days} दिन** बाकी हैं। वर्तमान में {stock} पैकेट स्टॉक में हैं (जोखिम: {risk})।"
            else:
                ans = f"**{name}** will expire in **{days} days** (Selling {rate:.1f} units/day, currently {risk} Risk with {chance}% waste probability)."
            return ans, pretty(matched_df)

        # Cross-question: Stock count
        if any(w in q for w in ["stock", "how much", "how many", "quantity", "left", "kitna", "कितना", "cuanto", "queda"]):
            if len(matched_df) > 1:
                total_stock = int(matched_df["stock"].sum())
                ans = f"Found **{len(matched_df)} varieties** with a total of **{total_stock} units in stock**:\n" + "\n".join([f"• **{r['product']}**: {int(r['stock'])} units, {int(r['days_left'])} days left ({r['risk']} risk)" for _, r in matched_df.iterrows()])
            else:
                if is_hindi:
                    ans = f"**{name}** का कुल स्टॉक **{stock} पैकेट** है (प्रतिदिन बिक्री: {rate:.1f})।"
                else:
                    ans = f"You have **{stock} units** of **{name}** left in stock (Current rate: {rate:.1f} units/day, {days} days to expiry)."
            return ans, pretty(matched_df)

        # General Product Profile
        if is_hindi:
            ans = f"**{name} स्थिति**: स्टॉक: **{stock}** · दिन बाकी: **{days}** · कीमत: **₹{price}** · जोखिम: **{risk} ({chance}%)**। सुझाव: *{action}*।"
        else:
            ans = f"**{name} Profile:** Stock: {stock} units · Expiry: {days} days · Price: ₹{price} · Risk: **{risk} ({chance}% chance)**. Action: {action}."
        return ans, pretty(matched_df)

    # 3. High-level supermarket queries
    if any(w in q for w in ["discount", "action", "what should", "do today"]):
        if high.empty:
            return "🎉 No products need emergency discounts today. All shelves are healthy.", None
        return "These products need urgent markdowns or supplier returns today:", pretty(high[["product", "days_left", "action"]])

    if any(w in q for w in ["money", "loss", "rupee", "cost", "₹", "worth"]):
        total = int(high["est_loss"].sum()) if "est_loss" in high.columns else 0
        return f"Estimated financial loss at risk in critical items: **₹{total:,}**.", pretty(high[["product", "est_loss"]]) if not high.empty else None

    if any(w in q for w in ["urgent", "first", "most", "priority"]):
        top = data.iloc[0]
        st.session_state.context_product = top["product"]
        return f"Most urgent: **{top['product']}** ({int(top['wastage_chance'])}% waste chance, {int(top['days_left'])} days left). Action: *{top['action']}*.", None

    return ("I am listening! You can ask initial or cross-questions such as:  \n"
            "• *'How much paneer do I have?'* $\\rightarrow$ *'When will it expire?'* $\\rightarrow$ *'Why is the risk high?'*  \n"
            "• *'How many stocks of pulses left?'*  \n"
            "• *'दाल का कितना स्टॉक बचा है?'* (Hindi)  \n"
            "• *'What is most urgent to discount today?'*"), None


# ------------------------------------------------------------------
# Sidebar: Inventory & Settings
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📦 Supermarket Inventory")
    uploaded = st.file_uploader("Upload Inventory CSV", type="csv")

    sample_data = get_default_inventory().head(15)
    st.download_button(
        "📥 Download Sample CSV",
        sample_data.to_csv(index=False),
        "freshwatch_sample_inventory.csv",
        "text/csv",
    )

    st.markdown("---")
    st.markdown("### ⚙️ Alert Thresholds")
    high_thr = st.number_input("Act today risk threshold (%)", min_value=50, max_value=95, value=80, step=5)
    med_thr = st.number_input("Keep watching risk threshold (%)", min_value=10, max_value=90, value=50, step=5)
    if med_thr >= high_thr:
        med_thr = high_thr - 5
        st.caption("Adjusted so watch level remains below action level.")

    st.markdown("---")
    with st.expander("ℹ️ About the ML Core"):
        st.write(
            "**Architecture**: Random Forest Classifier (100 Trees)  \n"
            "**Features**: Stock, Daily Sales, Days to Expiry, Expected Sales, Leftover Units.  \n"
            "**Goal**: Classify stockout probability vs spoilage risk before it happens.  \n"
            "**Advantage over Tally**: Tally is an accounting ledger that only records past write-offs. FreshWatch predicts future loss to enable progressive liquidation."
        )

inventory, error = load_inventory(uploaded)
if error:
    st.sidebar.error(error)
    inventory, _ = load_inventory(None)
    st.sidebar.info("Showing standard supermarket inventory instead.")

data = add_predictions(inventory, high_thr, med_thr)
high = data[data["risk"] == "High"]
medium = data[data["risk"] == "Medium"]
safe = data[data["risk"] == "Safe"]
order = ["High", "Medium", "Safe"]

# ------------------------------------------------------------------
# Top of Page (Hero Banner & KPI Tiles)
# ------------------------------------------------------------------
st.markdown(HERO, unsafe_allow_html=True)

t1, t2, t3, t4 = st.columns(4)
t1.markdown(tile("Act today", len(high), "urgent discount / return", PALETTE["High"]["main"]),
            unsafe_allow_html=True)
t2.markdown(tile("Keep watching", len(medium), "moderate wastage risk", PALETTE["Medium"]["main"]),
            unsafe_allow_html=True)
t3.markdown(tile("Looking fine", len(safe), "expected to sell fully", PALETTE["Safe"]["main"]),
            unsafe_allow_html=True)
if "est_loss" in high.columns:
    t4.markdown(tile("Money at risk", f"₹{int(high['est_loss'].sum()):,}", "in critical items", "#e67e22"),
                unsafe_allow_html=True)
else:
    t4.markdown(tile("Units at risk", int(high["stock"].sum()), "units in critical items", "#e67e22"),
                unsafe_allow_html=True)

st.markdown(health_bar(len(high), len(medium), len(safe)), unsafe_allow_html=True)

# ------------------------------------------------------------------
# Product Cards (High & Medium Risk Alerts)
# ------------------------------------------------------------------
st.markdown(section("Act today", "These items are projected to expire before selling out."), unsafe_allow_html=True)
if high.empty:
    st.markdown('<div class="empty">🎉 Nothing urgent today! Your inventory shelves are healthy.</div>',
                unsafe_allow_html=True)
else:
    cards = "".join(product_card(r) for _, r in high.head(12).iterrows())
    st.markdown(f'<div class="grid">{cards}</div>', unsafe_allow_html=True)
    if len(high) > 12:
        st.caption(f"+ {len(high) - 12} more products need action. Check 'All products' tab for full list.")

if not medium.empty:
    st.markdown(section("Keep an eye on", "Moderate risk: consider moving them to prominent shelves."),
                unsafe_allow_html=True)
    cards = "".join(product_card(r) for _, r in medium.head(8).iterrows())
    st.markdown(f'<div class="grid">{cards}</div>', unsafe_allow_html=True)

if not safe.empty:
    st.markdown(section("Looking fine", "These products have healthy sales velocity."),
                unsafe_allow_html=True)
    chips = "".join(
        f'<span>{icon_for(p)} {html.escape(str(p))}</span>' for p in safe["product"].head(20)
    )
    st.markdown(f'<div class="chips">{chips}</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# Interactive Tools & Supermarket Modules
# ------------------------------------------------------------------
st.markdown(section("Interactive Systems", "Explore live inventory, talk to the Conversational AI Caller, or run price simulations."),
            unsafe_allow_html=True)

tab_table, tab_call, tab_sim, tab_chat, tab_tally = st.tabs(
    [
        "📋 All Products",
        "📞 Conversational AI Caller (Gemini Style)",
        "⚡ Dynamic Markdown Simulator",
        "💬 Multi-Turn Assistant Chat",
        "⚖️ FreshWatch vs Tally ERP",
    ]
)

# ------------------------------------------------------------------
# TAB 1: ALL PRODUCTS TABLE
# ------------------------------------------------------------------
with tab_table:
    f_col, _ = st.columns([1, 3])
    level = f_col.selectbox("Filter by risk level", ["All"] + order)
    view = data if level == "All" else data[data["risk"] == level]
    shown = view.copy()
    shown["product"] = shown["product"].map(lambda p: f"{icon_for(p)} {p}")
    table_cols = ["product", "stock", "daily_sales", "days_left"]
    if "price" in shown.columns:
        table_cols += ["price", "est_loss"]
    table_cols += ["wastage_chance", "risk", "action"]
    show_df(
        pretty(shown[table_cols]),
        column_config={
            "Wastage chance (%)": st.column_config.ProgressColumn(
                "Chance of waste", min_value=0, max_value=100, format="%d%%"
            ),
            "Daily sales": st.column_config.NumberColumn(format="%.1f"),
        },
    )
    st.download_button("📥 Download Current Report (CSV)", view.to_csv(index=False), "wastage_report.csv", "text/csv")

# ------------------------------------------------------------------
# TAB 2: CONVERSATIONAL AI CALLING ASSISTANT (GEMINI STYLE)
# ------------------------------------------------------------------
with tab_call:
    st.markdown(
        """
        ### 📞 Conversational AI Phone Call (Multi-Turn & Cross-Question Ready)
        This voice assistant behaves like **Gemini Live / Siri**: it remembers the product you just talked about, handles complex cross-questions (*"When will it expire?"*, *"Why is the risk so high?"*, *"What discount should I give?"*), and speaks back aloud in **8+ languages**!
        """
    )

    if gemini_api_key.strip():
        st.success("✨ **Gemini Live Calling Active**: Responses are powered by Google Gemini 1.5 Flash with full conversation reasoning!")
    else:
        st.info("💡 **Local Multi-Turn Engine Active**: Running 100% offline with context memory and pronoun resolution. (Optional: paste a Gemini API Key in the sidebar to enable Gemini Cloud Calling).")

    inv_json = data[["product", "stock", "daily_sales", "days_left", "price", "wastage_chance", "risk", "action"]].to_json(orient="records")

    call_widget_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
      body {{
        margin: 0; padding: 0; background: transparent;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        color: #f0f5f2;
      }}
      .phone-card {{
        max-width: 580px; margin: 10px auto;
        background: #151d1a; border: 1px solid #273730;
        border-radius: 28px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);
      }}
      .phone-header {{
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #273730; padding-bottom: 14px; margin-bottom: 14px;
      }}
      .caller-id {{ font-size: 1.15rem; font-weight: 700; color: #10b981; }}
      .status-pill {{
        font-size: 0.78rem; font-weight: 600; padding: 4px 10px; border-radius: 99px;
        background: rgba(16, 185, 129, 0.15); color: #10b981; border: 1px solid #10b981;
      }}
      .topic-badge {{
        font-size: 0.8rem; background: #1c2722; color: #e3b95c; padding: 4px 10px;
        border-radius: 8px; margin-bottom: 12px; display: inline-block; border: 1px solid #3d4f45;
      }}
      .lang-bar {{
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 14px; background: #1c2622; padding: 8px 14px; border-radius: 12px;
      }}
      select {{
        background: #111815; color: #f0f5f2; border: 1px solid #364b41;
        padding: 6px 12px; border-radius: 8px; font-size: 0.9rem; outline: none; cursor: pointer;
      }}
      .screen {{
        background: #0d1311; border: 1px solid #23312a; border-radius: 18px;
        padding: 16px; min-height: 160px; max-height: 240px; overflow-y: auto; margin-bottom: 14px;
      }}
      .dialogue {{ display: flex; flex-direction: column; gap: 10px; }}
      .bubble {{
        padding: 10px 14px; border-radius: 14px; font-size: 0.92rem; line-height: 1.45; max-width: 88%;
      }}
      .bubble.user {{
        align-self: flex-end; background: #1f3d30; color: #e2f5ec; border: 1px solid #2e5946;
      }}
      .bubble.ai {{
        align-self: flex-start; background: #1a2521; color: #cbd5d0; border: 1px solid #2b3b34;
      }}
      .wave-box {{
        display: flex; justify-content: center; align-items: center; gap: 6px;
        height: 28px; margin: 4px 0;
      }}
      .bar {{
        width: 4px; height: 8px; background: #10b981; border-radius: 99px;
        transition: height 0.1s ease;
      }}
      .speaking .bar {{
        animation: wave 0.8s infinite ease-in-out alternate;
      }}
      .speaking .bar:nth-child(2) {{ animation-delay: 0.15s; }}
      .speaking .bar:nth-child(3) {{ animation-delay: 0.3s; }}
      .speaking .bar:nth-child(4) {{ animation-delay: 0.45s; }}
      .speaking .bar:nth-child(5) {{ animation-delay: 0.6s; }}
      @keyframes wave {{
        0% {{ height: 6px; }}
        100% {{ height: 26px; background: #34d399; }}
      }}
      .actions {{
        display: flex; gap: 10px; justify-content: center; align-items: center; margin-top: 6px;
      }}
      .btn {{
        padding: 11px 20px; border-radius: 14px; font-weight: 700; font-size: 0.95rem;
        cursor: pointer; border: none; transition: all 0.2s; display: flex; align-items: center; gap: 8px;
      }}
      .btn-call {{ background: #10b981; color: #fff; }}
      .btn-call:hover {{ background: #059669; transform: scale(1.02); }}
      .btn-hangup {{ background: #ef4444; color: #fff; display: none; }}
      .btn-hangup:hover {{ background: #dc2626; }}
      .btn-mic {{ background: #24352f; color: #10b981; border: 1px solid #3d584c; }}
      .btn-mic:hover {{ background: #2f453d; }}
      .chips {{
        margin-top: 14px; display: flex; flex-wrap: wrap; gap: 6px; justify-content: center;
      }}
      .chip {{
        background: #1b2621; border: 1px solid #2e4138; color: #9ab0a4;
        font-size: 0.78rem; padding: 5px 10px; border-radius: 99px; cursor: pointer;
      }}
      .chip:hover {{ color: #fff; border-color: #10b981; }}
      .text-input-box {{
        margin-top: 14px; display: flex; gap: 6px;
      }}
      input[type="text"] {{
        flex: 1; background: #0d1311; border: 1px solid #2b3b33; color: #fff;
        padding: 8px 12px; border-radius: 8px; font-size: 0.9rem; outline: none;
      }}
      .send-btn {{
        background: #10b981; color: #fff; border: none; border-radius: 8px;
        padding: 8px 16px; font-weight: 600; cursor: pointer;
      }}
    </style>
    </head>
    <body>

    <div class="phone-card">
      <div class="phone-header">
        <div class="caller-id">📞 FreshWatch Gemini Voice Agent</div>
        <div id="statusPill" class="status-pill">Ready to Call</div>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span id="topicBadge" class="topic-badge">📌 Memory: No product active yet</span>
        <button class="chip" style="margin:0;" onclick="clearMemory()">Reset Memory</button>
      </div>

      <div class="lang-bar">
        <span>🌐 Call Language:</span>
        <select id="langSelect" onchange="onLangChange()">
          <option value="en-US">English (Global / Indian Accent)</option>
          <option value="hi-IN" selected>Hindi (हिंदी)</option>
          <option value="es-ES">Spanish (Español)</option>
          <option value="fr-FR">French (Français)</option>
          <option value="de-DE">German (Deutsch)</option>
          <option value="ta-IN">Tamil (தமிழ்)</option>
          <option value="te-IN">Telugu (తెలుగు)</option>
          <option value="bn-IN">Bengali (বাংলা)</option>
        </select>
      </div>

      <div class="screen" id="screenBox">
        <div class="dialogue" id="dialogueBox">
          <div class="bubble ai">
            Press <b>Start Call</b> or speak. I remember context for cross-questions (e.g. ask <i>'How much paneer left?'</i> then follow up with <i>'When will it expire?'</i> and <i>'Why?'</i>).
          </div>
        </div>
      </div>

      <div id="waveBox" class="wave-box">
        <div class="bar"></div><div class="bar"></div><div class="bar"></div>
        <div class="bar"></div><div class="bar"></div>
      </div>

      <div class="actions">
        <button id="callBtn" class="btn btn-call" onclick="startCall()">🟢 Start Call</button>
        <button id="hangupBtn" class="btn btn-hangup" onclick="endCall()">🔴 End Call</button>
        <button id="micBtn" class="btn btn-mic" onclick="listenMic()" style="display:none;">🎙️ Speak Question</button>
      </div>

      <div class="chips" id="quickChips">
        <span class="chip" onclick="askPreset('How much paneer do I have?')">How much paneer?</span>
        <span class="chip" onclick="askPreset('When will it expire?')">When will it expire? (Follow-up)</span>
        <span class="chip" onclick="askPreset('Why is the risk so high?')">Why? (Cross-question)</span>
        <span class="chip" onclick="askPreset('What discount should I give?')">What discount?</span>
        <span class="chip" onclick="askPreset('दाल का कितना स्टॉक बचा है?')">दाल का कितना स्टॉक है?</span>
      </div>

      <div class="text-input-box">
        <input type="text" id="typeInput" placeholder="Speak or type cross-question here..." onkeydown="if(event.key==='Enter') sendType()">
        <button class="send-btn" onclick="sendType()">Send</button>
      </div>
    </div>

    <script>
      const inventory = {inv_json};
      let inCall = false;
      let recognition = null;
      let focusedProduct = null;

      const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;

      function speak(text, lang) {{
        if (!('speechSynthesis' in window)) return;
        window.speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(text);
        utter.lang = lang || document.getElementById('langSelect').value;
        utter.rate = 1.0;
        utter.pitch = 1.0;

        document.getElementById('waveBox').classList.add('speaking');
        utter.onend = () => {{
          document.getElementById('waveBox').classList.remove('speaking');
        }};
        utter.onerror = () => {{
          document.getElementById('waveBox').classList.remove('speaking');
        }};
        window.speechSynthesis.speak(utter);
      }}

      function addBubble(text, role) {{
        const box = document.getElementById('dialogueBox');
        const b = document.createElement('div');
        b.className = 'bubble ' + role;
        b.innerText = text;
        box.appendChild(b);
        document.getElementById('screenBox').scrollTop = document.getElementById('screenBox').scrollHeight;
      }}

      function clearMemory() {{
        focusedProduct = null;
        document.getElementById('topicBadge').innerText = "📌 Memory: Cleared";
        addBubble("Context memory reset. You can start a new topic.", "ai");
      }}

      function startCall() {{
        inCall = true;
        document.getElementById('callBtn').style.display = 'none';
        document.getElementById('hangupBtn').style.display = 'inline-flex';
        document.getElementById('micBtn').style.display = 'inline-flex';
        document.getElementById('statusPill').innerText = '🟢 Connected (Live)';

        const lang = document.getElementById('langSelect').value;
        let welcome = "Hello! FreshWatch AI is live on call. I remember the product you ask about, so feel free to ask follow-up questions.";
        if (lang === 'hi-IN') welcome = "नमस्ते! फ्रेशवॉच एआई कॉल पर कनेक्ट है। आप किसी भी सामान के बारे में पूछ सकते हैं और उसके बाद 'इसकी एक्सपायरी कब है?' या 'क्यों?' जैसे क्रॉस प्रश्न भी पूछ सकते हैं।";
        if (lang === 'es-ES') welcome = "¡Hola! FreshWatch AI conectado. Puede hacer preguntas de seguimiento como '¿Cuándo vence?' o '¿Por qué?'";

        addBubble(welcome, 'ai');
        speak(welcome, lang);
      }}

      function endCall() {{
        inCall = false;
        window.speechSynthesis.cancel();
        if (recognition) recognition.stop();
        document.getElementById('callBtn').style.display = 'inline-flex';
        document.getElementById('hangupBtn').style.display = 'none';
        document.getElementById('micBtn').style.display = 'none';
        document.getElementById('statusPill').innerText = 'Call Ended';
        document.getElementById('waveBox').classList.remove('speaking');
        addBubble("Call ended. Press Start Call to speak again.", 'ai');
      }}

      function onLangChange() {{
        if (inCall) {{
          const lang = document.getElementById('langSelect').value;
          let msg = "Language switched.";
          if (lang === 'hi-IN') msg = "भाषा बदल दी गई है।";
          if (lang === 'es-ES') msg = "Idioma cambiado.";
          addBubble(msg, 'ai');
          speak(msg, lang);
        }}
      }}

      function listenMic() {{
        if (!SpeechRec) {{
          alert("Microphone recognition not supported in this browser. Please type your question in the box below!");
          return;
        }}
        const lang = document.getElementById('langSelect').value;
        recognition = new SpeechRec();
        recognition.lang = lang;
        recognition.interimResults = false;

        document.getElementById('statusPill').innerText = '🎙️ Listening...';
        recognition.onstart = () => {{
          document.getElementById('waveBox').classList.add('speaking');
        }};
        recognition.onresult = (e) => {{
          const text = e.results[0][0].transcript;
          addBubble(text, 'user');
          resolveAndReply(text, lang);
        }};
        recognition.onerror = () => {{
          document.getElementById('statusPill').innerText = '🟢 Connected';
          document.getElementById('waveBox').classList.remove('speaking');
        }};
        recognition.onend = () => {{
          document.getElementById('statusPill').innerText = '🟢 Connected';
          document.getElementById('waveBox').classList.remove('speaking');
        }};
        recognition.start();
      }}

      function askPreset(q) {{
        if (!inCall) startCall();
        addBubble(q, 'user');
        const lang = document.getElementById('langSelect').value;
        resolveAndReply(q, lang);
      }}

      function sendType() {{
        const input = document.getElementById('typeInput');
        const q = input.value.trim();
        if (!q) return;
        input.value = "";
        if (!inCall) startCall();
        addBubble(q, 'user');
        const lang = document.getElementById('langSelect').value;
        resolveAndReply(q, lang);
      }}

      function resolveAndReply(query, lang) {{
        const q = query.toLowerCase();

        // 1. Direct product extraction
        let found = null;
        if (q.includes("paneer")) found = inventory.find(i => i.product.toLowerCase().includes("paneer"));
        else if (q.includes("rice") || q.includes("chawal") || q.includes("चावल") || q.includes("arroz")) found = inventory.find(i => i.product.toLowerCase().includes("rice"));
        else if (q.includes("milk") || q.includes("doodh") || q.includes("दूध") || q.includes("leche")) found = inventory.find(i => i.product.toLowerCase().includes("cow milk"));
        else if (q.includes("bread") || q.includes("roti") || q.includes("ब्रेड")) found = inventory.find(i => i.product.toLowerCase().includes("bread"));
        else if (q.includes("banana") || q.includes("kela") || q.includes("केला")) found = inventory.find(i => i.product.toLowerCase().includes("banana"));
        else if (q.includes("spinach") || q.includes("palak") || q.includes("पालक")) found = inventory.find(i => i.product.toLowerCase().includes("spinach"));
        else if (q.includes("pulse") || q.includes("dal") || q.includes("daal") || q.includes("दाल")) {{
          const pulses = inventory.filter(i => i.product.toLowerCase().includes("dal") || i.product.toLowerCase().includes("pulse"));
          const total = pulses.reduce((acc, p) => acc + p.stock, 0);
          let reply = "";
          if (lang === 'hi-IN') {{
            reply = "दालों का कुल स्टॉक " + total + " पैकेट है (तूर दाल: 38, मूंग दाल: 30, चना दाल: 25 पैकेट)। सभी सुरक्षित श्रेणी में हैं।";
          }} else {{
            reply = "You have a total of " + total + " units of pulses across Toor Dal (38), Moong Dal (30), and Chana Dal (25).";
          }}
          addBubble(reply, 'ai');
          speak(reply, lang);
          return;
        }}

        // If found, update context
        if (found) {{
          focusedProduct = found;
          document.getElementById('topicBadge').innerText = "📌 Memory: " + found.product;
        }} else if (!found && focusedProduct) {{
          // Pronoun or cross question referencing existing focused product
          const isRef = q.includes("it") || q.includes("this") || q.includes("why") || q.includes("discount") || q.includes("expire") || q.includes("when") || q.includes("stock") || q.includes("price") || q.includes("इसकी") || q.includes("इसका") || q.includes("क्यों") || q.includes("कब");
          if (isRef) {{
            found = focusedProduct;
          }}
        }}

        // If we have an active product (from current or previous turn)
        if (found) {{
          const name = found.product;
          const stock = found.stock;
          const days = found.days_left;
          const rate = found.daily_sales;
          const risk = found.risk;
          const chance = found.wastage_chance;
          const action = found.action;
          const expected = Math.round(rate * days);
          const leftover = Math.max(stock - expected, 0);
          const loss = Math.round(leftover * (found.price || 0));

          let reply = "";

          // Cross-question: "Why is the risk high?" / "Why?"
          if (q.includes("why") || q.includes("reason") || q.includes("क्यों") || q.includes("por qué")) {{
            if (lang === 'hi-IN') {{
              reply = "कारण यह है कि " + name + " का स्टॉक " + stock + " है, लेकिन बिक्री सिर्फ " + rate + " प्रतिदिन है। " + days + " दिनों में सिर्फ " + expected + " बिकेंगे और " + leftover + " पैकेट बर्बाद हो जाएंगे!";
            }} else {{
              reply = "Why is " + name + " at risk? Because you hold " + stock + " units, but sell only " + rate + "/day. In " + days + " days you will only sell " + expected + " units, leaving " + leftover + " units (₹" + loss + ") to expire!";
            }}
          }}
          // Cross-question: "When will it expire?"
          else if (q.includes("expire") || q.includes("when") || q.includes("days") || q.includes("कब") || q.includes("vence")) {{
            if (lang === 'hi-IN') {{
              reply = name + " की एक्सपायरी में " + days + " दिन बाकी हैं। जोखिम " + risk + " (" + chance + "%) है।";
            }} else {{
              reply = name + " will expire in " + days + " days. Current risk is " + risk + " with " + chance + "% wastage probability.";
            }}
          }}
          // Cross-question: "What discount should I give?" / "What action?"
          else if (q.includes("action") || q.includes("discount") || q.includes("क्या करें") || q.includes("descuento")) {{
            if (lang === 'hi-IN') {{
              reply = "सुझाव: " + action + "। इससे बिक्री की गति बढ़ेगी और एक्सपायरी से पहले सारा स्टॉक बिक जाएगा।";
            }} else {{
              reply = "Prescribed Action: " + action + ". This price markdown will accelerate daily velocity to clear the " + leftover + " leftover units.";
            }}
          }}
          // Default state
          else {{
            if (lang === 'hi-IN') {{
              reply = name + " का स्टॉक " + stock + " पैकेट है। एक्सपायरी में " + days + " दिन बाकी हैं और जोखिम स्तर " + risk + " (" + chance + "%) है।";
            }} else {{
              reply = name + " has " + stock + " units in stock, expiring in " + days + " days. Machine learning risk is " + risk + " (" + chance + "% wastage chance).";
            }}
          }}

          addBubble(reply, 'ai');
          speak(reply, lang);
          return;
        }}

        // Fallback general response
        let def = "I can answer about any product and remember follow-up questions! Try asking: 'How much paneer do I have?' then ask 'When will it expire?' or 'Why?'";
        if (lang === 'hi-IN') def = "मैं किसी भी सामान की जानकारी दे सकता हूँ और क्रॉस-प्रश्न भी समझता हूँ! जैसे: 'पनीर कितना है?' पूछकर फिर 'यह कब एक्सपायर होगा?' पूछें।";
        addBubble(def, 'ai');
        speak(def, lang);
      }}
    </script>
    </body>
    </html>
    """
    components.html(call_widget_html, height=620)

# ------------------------------------------------------------------
# TAB 3: DYNAMIC MARKDOWN ELASTICITY SIMULATOR (WHY IT'S NOT TALLY)
# ------------------------------------------------------------------
with tab_sim:
    st.markdown(
        """
        ### ⚡ Dynamic Markdown & Price Elasticity Optimizer
        > **Why FreshWatch is not Tally ERP:** Tally merely records static historical sales (`Stock = In - Out`).  
        > FreshWatch uses **Price Elasticity Modeling** and the **Random Forest Classifier** to simulate how staged discounts stimulate demand to clear stock *before* the expiration cutoff!
        """
    )

    sim_col1, sim_col2 = st.columns([1, 1], gap="large")

    with sim_col1:
        st.markdown("#### 1. Select Product to Optimize")
        candidates = data[data["risk"].isin(["High", "Medium"])]["product"].tolist()
        if not candidates:
            candidates = data["product"].tolist()
        sim_product = st.selectbox("Choose Item", candidates)

        row = data[data["product"] == sim_product].iloc[0]
        st.write(f"**Current Stock**: `{int(row['stock'])} units` | **Days Left**: `{int(row['days_left'])} days`")
        st.write(f"**Base Daily Sales**: `{row['daily_sales']:.1f} units/day` | **Base Price**: `₹{row.get('price', 0):.0f}`")
        st.write(f"**Original Wastage Chance**: `{int(row['wastage_chance'])}% ({row['risk']} Risk)`")

        st.markdown("#### 2. Test Dynamic Markdown Strategy")
        discount_pct = st.slider("Select Promotional Discount (%)", min_value=0, max_value=50, value=25, step=5)
        elasticity = st.slider("Estimated Customer Demand Elasticity", min_value=1.0, max_value=3.5, value=2.0, step=0.25,
                               help="In retail, an elasticity of 2.0 means a 20% discount boosts daily sales volume by ~40%.")

    with sim_col2:
        st.markdown("#### 3. Real-Time ML Outcome Simulation")
        velocity_boost = 1.0 + (elasticity * (discount_pct / 100.0))
        sim_daily_sales = round(row["daily_sales"] * velocity_boost, 2)
        sim_expected_sales = round(sim_daily_sales * row["days_left"], 1)
        sim_leftover = max(row["stock"] - sim_expected_sales, 0)
        unit_price = row.get("price", 0)
        disc_price = round(unit_price * (1 - discount_pct / 100.0), 1)

        sim_df = pd.DataFrame([{
            "stock": row["stock"],
            "daily_sales": sim_daily_sales,
            "days_left": row["days_left"],
            "price": disc_price
        }])
        sim_prob = int((model.predict_proba(build_features(sim_df))[:, 1] * 100).round(0)[0])
        sim_risk = risk_level(sim_prob, high_thr, med_thr)

        m1, m2 = st.columns(2)
        m1.metric("Simulated Daily Velocity", f"{sim_daily_sales:.1f}/day", delta=f"+{((velocity_boost - 1)*100):.0f}% sales boost")
        m2.metric("Simulated Wastage Risk", f"{sim_prob}%", delta=f"{sim_prob - int(row['wastage_chance'])}% risk reduction", delta_color="inverse")

        m3, m4 = st.columns(2)
        orig_loss = int(max(row["stock"] - row["daily_sales"] * row["days_left"], 0) * unit_price)
        new_loss = int(sim_leftover * disc_price)
        capital_saved = max(orig_loss - new_loss, 0)
        m3.metric("Projected Leftover Units", f"{int(sim_leftover)} units", f"-{int(max(row['stock'] - row['daily_sales'] * row['days_left'], 0) - sim_leftover)} saved from trash")
        m4.metric("Capital Recovered", f"₹{capital_saved:,}", "reclaimed from 100% loss")

        if sim_prob < 40:
            st.success(f"✅ Success! Applying a **{discount_pct}% discount** accelerates sales to clear inventory completely before expiry.")
        else:
            st.warning(f"⚠️ A {discount_pct}% discount reduces waste, but is not enough to clear all {int(row['stock'])} units before expiry. Consider a combo deal or 40% liquidation.")

# ------------------------------------------------------------------
# TAB 4: MULTI-TURN ASSISTANT CHAT
# ------------------------------------------------------------------
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant",
             "text": "Hello! I am your FreshWatch inventory assistant. I support multi-turn dialogue and cross-questions (e.g. ask 'How much paneer do I have?' then ask 'When will it expire?' or 'Why is it risky?').",
             "table": None}
        ]

    st.markdown("##### Multi-Turn Cross-Question Flow (Try Clicking in Sequence)")
    seq1, seq2, seq3, seq4 = st.columns(4)
    clicked = None
    if seq1.button("1. How much paneer left?"):
        clicked = "How much paneer left?"
    if seq2.button("2. When will it expire?"):
        clicked = "When will it expire?"
    if seq3.button("3. Why is the risk high?"):
        clicked = "Why is the risk high?"
    if seq4.button("4. What discount to give?"):
        clicked = "What discount should I give?"

    typed = st.chat_input("Type your question or cross-question (e.g. 'How much rice left?' or 'दूध कब एक्सपायर होगा?')")
    question = clicked or typed
    if question:
        st.session_state.messages.append({"role": "user", "text": question, "table": None})
        answer, table = smart_multiturn_reply(question, data, gemini_api_key)
        st.session_state.messages.append({"role": "assistant", "text": answer, "table": table})

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])
            if msg["table"] is not None:
                show_df(msg["table"])

# ------------------------------------------------------------------
# TAB 5: FRESHWATCH VS TALLY ERP & MODEL BENCHMARKS
# ------------------------------------------------------------------
with tab_tally:
    st.markdown(
        """
        ### ⚖️ Why FreshWatch is NOT Tally ERP
        Evaluators often ask: *"What is the difference between an inventory ledger like Tally and your project?"*  
        Here is the fundamental architectural distinction:
        """
    )

    tally_comp = pd.DataFrame([
        {
            "Dimension": "System Philosophy",
            "Traditional Tally ERP": "Retrospective & Historical (Records what already happened).",
            "FreshWatch (Machine Learning)": "Predictive & Prescriptive (Forecasts future wastage before it occurs).",
        },
        {
            "Dimension": "Mathematical Logic",
            "Traditional Tally ERP": "Basic arithmetic ledger subtraction (`Stock = Purchased - Sold`).",
            "FreshWatch (Machine Learning)": "Non-linear Random Forest Classifier over 5 multi-dimensional features.",
        },
        {
            "Dimension": "Expiry & Spoilage",
            "Traditional Tally ERP": "Passive. Only logs a loss write-off *after* the product has already expired.",
            "FreshWatch (Machine Learning)": "Proactive. Identifies shelf surpluses 3 to 14 days in advance.",
        },
        {
            "Dimension": "Pricing Strategy",
            "Traditional Tally ERP": "Static master rates. Does not compute price elasticity.",
            "FreshWatch (Machine Learning)": "Prescribes staged markdowns (10% to 40%) to accelerate demand and salvage capital.",
        },
        {
            "Dimension": "User Interface",
            "Traditional Tally ERP": "Keyboard-driven desktop accounting vouchers.",
            "FreshWatch (Machine Learning)": "Modern Dark-theme dashboard + Conversational Voice AI Calling Assistant (8+ languages).",
        },
    ])
    show_df(tally_comp)

    st.markdown("---")
    st.markdown("### 📊 Machine Learning Model Accuracy & Validation")
    rf_row = next(m for m in metrics["comparison"] if m["model"] == "Random Forest")
    st.markdown(
        f"**Accuracy:** The Random Forest model achieved **{round(rf_row['accuracy'] * 100)}% accuracy** "
        f"on {metrics['test_rows']:,} unseen supermarket test records."
    )
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Accuracy", f"{rf_row['accuracy'] * 100:.1f}%", help="Share of all predictions that were correct")
    p2.metric("Precision", f"{rf_row['precision'] * 100:.1f}%", help="When it flags high risk, how often it is truly at risk")
    p3.metric("Recall", f"{rf_row['recall'] * 100:.1f}%", help="Percentage of actual wasted items successfully caught")
    p4.metric("F1-score", f"{rf_row['f1'] * 100:.1f}%", help="Harmonic balance between precision and recall")

    g1, g2 = st.columns(2, gap="large")
    with g1:
        st.markdown(section("Confusion Matrix", "Evaluated on the 20% test partition."), unsafe_allow_html=True)
        cm = metrics["confusion_matrix"]
        cm_table = pd.DataFrame(
            {
                "Actual Status": ["Actually Sold", "Actually Wasted"],
                "Predicted Sold": [cm[0][0], cm[1][0]],
                "Predicted Wasted": [cm[0][1], cm[1][1]],
            }
        )
        show_df(cm_table)
    with g2:
        st.markdown(section("Feature Importance", "Which parameters weigh the most:"), unsafe_allow_html=True)
        nice = {"stock": "Stock Quantity", "daily_sales": "Daily Sales", "days_left": "Days Left",
                "expected_sales": "Expected Sales", "leftover": "Leftover Units"}
        imp = pd.DataFrame(
            {"Feature": [nice[k] for k in metrics["feature_importance"]],
             "Importance": list(metrics["feature_importance"].values())}
        )
        axis_color = "#cbd5d0" if is_dark else "#1f2a24"
        imp_chart = (
            alt.Chart(imp)
            .mark_bar(size=16, cornerRadiusEnd=4, color=GREEN)
            .encode(
                x=alt.X("Importance:Q", axis=None),
                y=alt.Y("Feature:N", sort="-x", title=None,
                        axis=alt.Axis(labelColor=axis_color, labelFontSize=12)),
                tooltip=["Feature", "Importance"]
            )
            .properties(height=200)
            .configure_axis(grid=False, domain=False, ticks=False)
            .configure_view(strokeWidth=0)
        )
        show_chart(imp_chart)

st.markdown(
    '<div class="foot"><b>FreshWatch</b> · Supermarket Expiry & Wastage Prediction System · '
    "Built with Python, Scikit-Learn & Streamlit</div>",
    unsafe_allow_html=True,
)
