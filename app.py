import html
import json
import re

import altair as alt
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="FreshWatch", page_icon="🥬", layout="wide")

# ------------------------------------------------------------------
# Session memory for products the user adds
# ------------------------------------------------------------------
if "my_products" not in st.session_state:
    st.session_state.my_products = []
if "last_added" not in st.session_state:
    st.session_state.last_added = None
if "add_msg" not in st.session_state:
    st.session_state.add_msg = None

# ------------------------------------------------------------------
# Sidebar: Theme Selection (Dark by default)
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

/* Font: applied to text elements only (NOT to every span/div, which breaks the icons) */
.stApp, .stApp p, .stApp label, .stApp li, .stApp button, .stApp input,
.stApp textarea, .stApp [role="tab"] {{
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
    padding: 38px 46px;
    margin-bottom: 26px;
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
    font-size: 2.7rem;
    line-height: 1.08;
    margin: 12px 0 14px 0;
    font-weight: 600;
}}
.hero .hp {{
    color: rgba(247, 241, 227, .88) !important;
    font-size: 1.02rem;
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
    .hero {{ grid-template-columns: 1fr; padding: 28px; }}
    .hero .art {{ display: none; }}
    .hero .ht {{ font-size: 2.1rem; }}
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
    font-size: 2.4rem;
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
    margin: 22px 0 10px 0;
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
    margin: 36px 0 14px 0;
}}
.sec .st {{
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--ink) !important;
}}
.sec .ss {{
    color: var(--muted) !important;
    font-size: .93rem;
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
.pcard .mine {{
    font-family: 'DM Sans', system-ui, sans-serif;
    font-size: .64rem;
    font-weight: 700;
    letter-spacing: .05em;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 99px;
    margin-left: 8px;
    background: var(--primary);
    color: #ffffff !important;
    vertical-align: middle;
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

.stButton > button:active,
button[data-testid="stBaseButton-secondary"]:active {{
    transform: translateY(0px) !important;
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

/* ---------- INPUTS & SELECTBOXES ---------- */
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

/* ---------- TABS ---------- */
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

/* ---------- CHAT MESSAGES ---------- */
[data-testid="stChatMessage"] {{
    background-color: var(--card) !important;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    margin-bottom: 12px !important;
}}

/* ---------- METRIC CARDS ---------- */
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

/* Expanders */
[data-testid="stExpander"] {{
    background-color: var(--card) !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
}}
[data-testid="stExpander"] summary {{
    color: var(--ink) !important;
}}

.foot {{
    color: var(--muted) !important;
    font-size: .82rem;
    margin-top: 56px;
    text-align: center;
    border-top: 1px solid var(--line);
    padding-top: 20px;
}}

/* ---------- ICON FONT FIX (keeps upload / arrow / chat icons from showing as text) ---------- */
.stApp [data-testid="stIconMaterial"],
.stApp span[data-testid="stIconMaterial"],
.stApp .material-symbols-rounded,
.stApp span.material-symbols-rounded {{
    font-family: "Material Symbols Rounded", "Material Symbols Outlined" !important;
    font-weight: normal !important;
    font-style: normal !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    font-feature-settings: "liga" !important;
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

# Expanded Product Icons List
PRODUCT_ICONS = [
    ("milk", "🥛"), ("bread", "🍞"), ("curd", "🥣"), ("yogurt", "🥣"), ("yoghurt", "🥣"),
    ("paneer", "🧀"), ("cheese", "🧀"), ("butter", "🧈"), ("biscuit", "🍪"), ("cookie", "🍪"),
    ("juice", "🧃"), ("egg", "🥚"), ("chip", "🍟"), ("ice cream", "🍦"), ("chocolate", "🍫"),
    ("noodle", "🍜"), ("cold drink", "🥤"), ("drink", "🥤"), ("soda", "🥤"), ("water", "💧"),
    ("rice", "🍚"), ("apple", "🍎"), ("banana", "🍌"), ("tomato", "🍅"), ("tea", "🍵"),
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
# Prediction logic
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
# Comprehensive Default Supermarket Catalog (35+ Products)
# ------------------------------------------------------------------
def get_default_inventory():
    return pd.DataFrame([
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


def read_product_csv(file):
    """Read a CSV with product, stock, daily_sales, days_left (+ optional price)."""
    try:
        df = pd.read_csv(file)
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


def load_inventory(uploaded):
    if uploaded is None:
        return get_default_inventory(), None
    return read_product_csv(uploaded)


# ------------------------------------------------------------------
# "Add my product" logic (runs as callbacks, before the page redraws)
# ------------------------------------------------------------------
def upsert_my_products(rows):
    """Add products to the user's list. Same name = update that product."""
    index = {p["product"].strip().lower(): i for i, p in enumerate(st.session_state.my_products)}
    for row in rows:
        key = row["product"].strip().lower()
        if key in index:
            st.session_state.my_products[index[key]] = row
        else:
            st.session_state.my_products.append(row)
            index[key] = len(st.session_state.my_products) - 1


def add_product_callback():
    name = str(st.session_state.get("np_name", "")).strip()
    if not name:
        st.session_state.add_msg = ("error", "Please type a product name first.")
        return
    row = {
        "product": name,
        "stock": int(st.session_state.np_stock),
        "daily_sales": float(st.session_state.np_sales),
        "days_left": int(st.session_state.np_days),
        "price": float(st.session_state.np_price),
    }
    upsert_my_products([row])
    st.session_state.last_added = row
    st.session_state.add_msg = ("success", f"Added “{name}” to your inventory. It now shows in the lists above.")
    st.session_state.np_name = ""


def remove_product_callback():
    name = st.session_state.get("rm_name")
    st.session_state.my_products = [p for p in st.session_state.my_products if p["product"] != name]
    last = st.session_state.last_added
    if last is not None and last["product"] == name:
        st.session_state.last_added = None


def clear_products_callback():
    st.session_state.my_products = []
    st.session_state.last_added = None


# ------------------------------------------------------------------
# HTML Components
# ------------------------------------------------------------------
HERO = flat(
    """
<div class="hero">
  <div>
    <div class="kick">Supermarket Stock Monitor</div>
    <div class="ht">Sell it before it expires.</div>
    <div class="hp">FreshWatch uses machine learning to predict which grocery and perishable items
    risk expiring on your shelves, so your team can discount, re-arrange, or return them proactively.</div>
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
        for k, n,
    )
