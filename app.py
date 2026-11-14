import datetime
import html
import json
import re

import altair as alt
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="FreshWatch", page_icon="🥬", layout="wide")

# ==================================================================
# ✏️ EDIT THIS BLOCK: your details for the website footer
# Keep the quotes "" . If you leave a value empty, it is simply not shown.
# ==================================================================
OWNER_NAME = "Sanskar Jaiswal"
OWNER_ROLE = "Owner & Developer"
OWNER_BIO = (
    "AIML engineering student and developer of intelligent web applications. "
    "I created FreshWatch to demonstrate how machine learning and predictive analytics "
    "can help retailers reduce food waste."
)
COMPANY_TAGLINE = "Smarter shelves. Less waste."
COMPANY_ABOUT = (
    "~ FreshWatch is a predictive analytics platform for perishable inventory. "
    "~ Its machine learning model scores every product on its likelihood of expiring unsold, "
    "~ estimates the financial exposure, and recommends timely actions such as markdowns, "
    "~ combo offers or supplier returns, helping retailers cut shrinkage and protect margins."
)
EMAIL = "sanskaraiml@gmail.com"         # example: "yourname@gmail.com"
INSTAGRAM = "sanskaarr.r"     # only your username, example: "sanskar.codes"
LINKEDIN_URL = "https://www.linkedin.com/in/sanskar-jaiswal-a59467380"  # full link, example: "https://www.linkedin.com/in/yourname"
GITHUB_URL = "https://github.com/sanskaraiml-debug"    # full link, example: "https://github.com/yourname"
# ==================================================================

# ------------------------------------------------------------------
# Session memory for products the user adds
# ------------------------------------------------------------------
if "my_products" not in st.session_state:
    st.session_state.my_products = []
if "last_added" not in st.session_state:
    st.session_state.last_added = None
if "add_msg" not in st.session_state:
    st.session_state.add_msg = None
if "entry_version" not in st.session_state:
    st.session_state.entry_version = 0

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

/* Top bar (holds the page tabs) */
header[data-testid="stHeader"] {{
    background: var(--bg) !important;
    border-bottom: 1px solid var(--line) !important;
}}

.block-container {{
    max-width: 1200px;
    padding-top: 5rem;
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
.sec.first {{
    margin-top: 6px;
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

/* ---------- SITE FOOTER ---------- */
.sitefoot {{
    margin-top: 64px;
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 22px;
    overflow: hidden;
}}
.sitefoot .sf-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 34px;
    padding: 36px 40px 30px 40px;
}}
.sitefoot .sf-logo {{
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--ink) !important;
}}
.sitefoot .sf-tag {{
    color: var(--primary) !important;
    font-weight: 700;
    font-size: .78rem;
    letter-spacing: .1em;
    text-transform: uppercase;
    margin-top: 4px;
}}
.sitefoot .sf-h {{
    font-weight: 700;
    font-size: .78rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--ink) !important;
    margin-bottom: 12px;
}}
.sitefoot .sf-text {{
    color: var(--muted) !important;
    font-size: .92rem;
    line-height: 1.6;
}}
.sitefoot .sf-owner {{
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--ink) !important;
}}
.sitefoot .sf-role {{
    color: var(--primary) !important;
    font-size: .82rem;
    font-weight: 600;
    margin: 2px 0 10px 0;
}}
.sitefoot a.sf-link {{
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--ink) !important;
    text-decoration: none !important;
    font-size: .92rem;
    padding: 6px 0;
    word-break: break-all;
}}
.sitefoot a.sf-link:hover {{
    color: var(--primary) !important;
}}
.sitefoot a.sf-link svg {{
    width: 18px;
    height: 18px;
    flex: none;
}}
.sitefoot .sf-bottom {{
    border-top: 1px solid var(--line);
    padding: 16px 40px;
    color: var(--muted) !important;
    font-size: .82rem;
    text-align: center;
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


def show_editor(df, **kwargs):
    try:
        return st.data_editor(df, width="stretch", hide_index=True, **kwargs)
    except Exception:
        return st.data_editor(df, use_container_width=True, hide_index=True, **kwargs)


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
# "Add my product" logic
# ------------------------------------------------------------------
def parse_number(text):
    """Turn typed text into a number. Returns None if blank or not a number."""
    s = str(text).strip().replace(",", "")
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def rows_from_entry(table):
    """Read the typed entry table. Returns (list of products, list of problems)."""
    rows, problems = [], []
    for i, r in table.reset_index(drop=True).iterrows():
        name = "" if pd.isna(r["Product"]) else str(r["Product"]).strip()
        stock, sales, days, price = r["Stock"], r["Sales per day"], r["Days left"], r["Price"]
        if not name and all(pd.isna(v) for v in (stock, sales, days, price)):
            continue  # completely blank row
        if not name:
            problems.append(f"Row {i + 1}: the product name is missing")
            continue
        if any(pd.isna(v) for v in (stock, sales, days)):
            problems.append(f"Row {i + 1} ({name}): please fill stock, sales per day and days left")
            continue
        rows.append(
            {
                "product": name,
                "stock": int(stock),
                "daily_sales": float(sales),
                "days_left": int(days),
                "price": float(price) if pd.notna(price) else float("nan"),
            }
        )
    return rows, problems


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


def remove_product_callback():
    name = st.session_state.get("rm_name")
    st.session_state.my_products = [p for p in st.session_state.my_products if p["product"] != name]
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
        for k, n, label in parts
    )
    return flat(f'<div class="health">{segs}</div><div class="legend">{legend}</div>')


def section(title, sub, first=False):
    cls = "sec first" if first else "sec"
    return flat(f'<div class="{cls}"><div class="st">{title}</div><div class="ss">{sub}</div></div>')


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
    mine_tag = ""
    if "mine" in r.index and bool(r["mine"]):
        mine_tag = '<span class="mine">Added by you</span>'
    return flat(
        f'<div class="pcard" style="--c:{pal["main"]};--soft:{pal["soft"]};--tx:{pal["text"]}">'
        f'<div class="ptop"><div class="emo">{icon_for(r["product"])}</div><div class="chip">{when}</div></div>'
        f'<div class="pname">{html.escape(str(r["product"]))}{mine_tag}</div>'
        f'<div class="psub">{int(r["stock"])} in stock · {r["daily_sales"]:.1f} sold/day</div>'
        f'<div class="meter"><div style="width:{chance}%"></div></div>'
        f'<div class="pfoot"><span>Chance it goes to waste</span><b>{chance}%</b></div>'
        f'<div class="todo">{short_action(r["risk"], days)}</div>{loss}</div>'
    )


# ------------------------------------------------------------------
# Chatbot Logic
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


def chatbot_reply(question, data):
    q = question.lower()
    high = data[data["risk"] == "High"]
    medium = data[data["risk"] == "Medium"]
    safe = data[data["risk"] == "Safe"]

    if any(w in q for w in ["discount", "action", "what should", "do today"]):
        if high.empty:
            return "No product needs a discount right now.", None
        return "These products need action today:", pretty(high[["product", "days_left", "action"]])
    if any(w in q for w in ["money", "loss", "rupee", "cost", "₹", "worth"]):
        if "est_loss" not in data.columns:
            return "Add a price column to your CSV to see money at risk.", None
        total = int(high["est_loss"].sum())
        return (f"Estimated money at risk in high-risk items: **₹{total:,}**.",
                pretty(high[["product", "est_loss"]]) if not high.empty else None)
    if any(w in q for w in ["urgent", "first", "most", "priority"]):
        if data.empty:
            return "No products found.", None
        top = data.iloc[0]
        return (f"Most urgent: **{top['product']}** with a {int(top['wastage_chance'])}% wastage chance "
                f"and {int(top['days_left'])} days left. {top['action']}."), None
    if any(w in q for w in ["high", "risk", "waste"]):
        if high.empty:
            return "No high-risk products right now.", None
        return (f"{len(high)} product(s) are at high wastage risk:",
                pretty(high[["product", "stock", "days_left", "wastage_chance"]]))
    if any(w in q for w in ["medium", "watch"]):
        if medium.empty:
            return "No medium-risk products right now.", None
        return "These products need watching:", pretty(medium[["product", "stock", "days_left", "wastage_chance"]])
    if any(w in q for w in ["expir", "10 days", "soon", "tomorrow"]):
        soon = data[data["days_left"] <= 10].sort_values("days_left")
        if soon.empty:
            return "Nothing expires within 10 days.", None
        return "Products expiring within 10 days:", pretty(soon[["product", "days_left", "stock", "risk"]])
    if "safe" in q:
        if safe.empty:
            return "No products are in the safe range.", None
        return "These products are safe:", pretty(safe[["product", "stock", "days_left"]])
    if any(w in q for w in ["summary", "how many", "overview", "count"]):
        return (f"Total {len(data)} products: **{len(high)} high**, **{len(medium)} medium**, "
                f"**{len(safe)} safe**."), None
    return ("You can ask: Which products are at high risk? What should I discount today? "
            "What is expiring soon? What is most urgent? How much money is at risk?"), None


# ------------------------------------------------------------------
# Sidebar: Inventory & Settings
# ------------------------------------------------------------------
def read_threshold(label, default, low, high_limit, key):
    """A typed box for a percentage. Falls back to the default if the text is not valid."""
    text = st.text_input(label, value=str(default), key=key)
    value = parse_number(text)
    if value is None or value < low or value > high_limit:
        st.caption(f"Type a number between {low} and {high_limit}. Using {default} for now.")
        return default
    return int(value)


with st.sidebar:
    st.markdown("---")
    st.markdown("### 📦 Inventory Data")
    uploaded = st.file_uploader("Upload Inventory CSV", type="csv")

    # Sample inventory download with rich default set
    sample_data = get_default_inventory().head(15)
    st.download_button(
        "📥 Download Sample CSV",
        sample_data.to_csv(index=False),
        "freshwatch_sample_inventory.csv",
        "text/csv",
    )

    st.markdown("---")
    st.markdown("### ⚙️ Alert Thresholds")
    high_thr = read_threshold("Act today risk threshold (%)", 80, 50, 95, "thr_high")
    med_thr = read_threshold("Keep watching risk threshold (%)", 50, 10, 90, "thr_med")
    if med_thr >= high_thr:
        med_thr = high_thr - 5
        st.caption("Adjusted so watch level remains below action level.")

    st.markdown("---")
    with st.expander("ℹ️ About the ML Model"):
        st.write(
            "**Architecture**: Random Forest Classifier  \n"
            "**Key Features**: Stock, Daily Sales, Days to Expiry, Expected Sales, and Projected Leftover.  \n"
            "**Goal**: Classify whether stock will spoil or reach expiry before complete sale.  \n"
            "**Training Data**: 5,000 synthetic supermarket transactions."
        )

base_inventory, error = load_inventory(uploaded)
if error:
    st.sidebar.error(error)
    base_inventory, _ = load_inventory(None)
    st.sidebar.info("Showing standard supermarket inventory instead.")

# Combine the main list with the products the user added
base_inventory = base_inventory.copy()
base_inventory["mine"] = False
if st.session_state.my_products:
    mine_df = pd.DataFrame(st.session_state.my_products)
    mine_df["mine"] = True
    inventory = pd.concat([base_inventory, mine_df], ignore_index=True)
else:
    inventory = base_inventory

data = add_predictions(inventory, high_thr, med_thr)
high = data[data["risk"] == "High"]
medium = data[data["risk"] == "Medium"]
safe = data[data["risk"] == "Safe"]
order = ["High", "Medium", "Safe"]


SVG_OPEN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round">')
ICON_MAIL = SVG_OPEN + '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'
ICON_INSTAGRAM = (SVG_OPEN + '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/>'
                  '<path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/>'
                  '<line x1="17.5" x2="17.51" y1="6.5" y2="6.5"/></svg>')
ICON_LINKEDIN = (SVG_OPEN + '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/>'
                 '<rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg>')
ICON_GITHUB = (SVG_OPEN + '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/>'
               '<path d="M9 18c-4.51 2-5-2-7-2"/></svg>')


def footer_link(href, icon, label):
    return (f'<a class="sf-link" href="{html.escape(href, quote=True)}" target="_blank" '
            f'rel="noopener noreferrer">{icon}<span>{html.escape(label)}</span></a>')


def page_footer():
    """Website footer: about the company, about the owner and contact links."""
    links = []
    email = EMAIL.strip()
    if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        links.append(footer_link(f"mailto:{email}", ICON_MAIL, email))
    handle = INSTAGRAM.strip().lstrip("@")
    if re.fullmatch(r"[A-Za-z0-9._]{1,30}", handle):
        links.append(footer_link(f"https://www.instagram.com/{handle}", ICON_INSTAGRAM, f"@{handle}"))
    for url, icon, label in ((LINKEDIN_URL, ICON_LINKEDIN, "LinkedIn"), (GITHUB_URL, ICON_GITHUB, "GitHub")):
        url = url.strip()
        if url.lower().startswith(("http://", "https://")):
            links.append(footer_link(url, icon, label))

    columns = [
        '<div><div class="sf-logo">🥬 FreshWatch</div>'
        f'<div class="sf-tag">{html.escape(COMPANY_TAGLINE)}</div></div>',
        f'<div><div class="sf-h">About the company</div><div class="sf-text">{html.escape(COMPANY_ABOUT)}</div></div>',
    ]
    if OWNER_NAME.strip():
        role = f'<div class="sf-role">{html.escape(OWNER_ROLE)}</div>' if OWNER_ROLE.strip() else ""
        columns.append(
            '<div><div class="sf-h">About the owner</div>'
            f'<div class="sf-owner">{html.escape(OWNER_NAME)}</div>{role}'
            f'<div class="sf-text">{html.escape(OWNER_BIO)}</div></div>'
        )
    if links:
        columns.append('<div><div class="sf-h">Get in touch</div>' + "".join(links) + "</div>")

    built_by = f" · Built by {html.escape(OWNER_NAME)}" if OWNER_NAME.strip() else ""
    year = datetime.date.today().year
    st.markdown(
        flat(
            '<div class="sitefoot"><div class="sf-grid">' + "".join(columns) + "</div>"
            f'<div class="sf-bottom">© {year} FreshWatch. All rights reserved.{built_by} · '
            "Python, Scikit-Learn &amp; Streamlit</div></div>"
        ),
        unsafe_allow_html=True,
    )


# ==================================================================
# PAGE: Home
# ==================================================================
def page_home():
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

    st.markdown(section("Act today", "These items are projected to expire before selling out."),
                unsafe_allow_html=True)
    if high.empty:
        st.markdown('<div class="empty">🎉 Nothing urgent today! Your inventory shelves are healthy.</div>',
                    unsafe_allow_html=True)
    else:
        cards = "".join(product_card(r) for _, r in high.head(12).iterrows())
        st.markdown(f'<div class="grid">{cards}</div>', unsafe_allow_html=True)
        if len(high) > 12:
            st.caption(f"+ {len(high) - 12} more products need action. Open the 'All products' tab for the full list.")

    if not medium.empty:
        st.markdown(section("Keep an eye on", "Moderate risk: consider moving them to prominent shelves."),
                    unsafe_allow_html=True)
        cards = "".join(product_card(r) for _, r in medium.head(8).iterrows())
        st.markdown(f'<div class="grid">{cards}</div>', unsafe_allow_html=True)
        if len(medium) > 8:
            st.caption(f"+ {len(medium) - 8} more products under watch in 'All products'.")

    if not safe.empty:
        st.markdown(section("Looking fine", "These products have healthy sales velocity."),
                    unsafe_allow_html=True)
        chips = "".join(
            f'<span>{icon_for(p)} {html.escape(str(p))}{" ★" if m else ""}</span>'
            for p, m in zip(safe["product"].head(20), safe["mine"].head(20))
        )
        st.markdown(f'<div class="chips">{chips}</div>', unsafe_allow_html=True)

    page_footer()


# ==================================================================
# PAGE: Add my product
# ==================================================================
def page_add():
    st.markdown(section("Add my product",
                        "Type your products into the table like a spreadsheet, then press Add. "
                        "The table clears so you can start fresh.", first=True),
                unsafe_allow_html=True)

    msg = st.session_state.add_msg
    if msg:
        if msg[0] == "success":
            st.success(msg[1])
        else:
            st.error(msg[1])
        st.session_state.add_msg = None

    blank = pd.DataFrame(
        {
            "Product": pd.Series([None] * 5, dtype="object"),
            "Stock": pd.Series([None] * 5, dtype="float"),
            "Sales per day": pd.Series([None] * 5, dtype="float"),
            "Days left": pd.Series([None] * 5, dtype="float"),
            "Price": pd.Series([None] * 5, dtype="float"),
        }
    )
    entry = show_editor(
        blank,
        num_rows="dynamic",
        key=f"entry_table_{st.session_state.entry_version}",
        column_config={
            "Product": st.column_config.TextColumn("Product name", width="large"),
            "Stock": st.column_config.NumberColumn("Stock quantity", min_value=0, step=1, format="%d"),
            "Sales per day": st.column_config.NumberColumn("Average sales per day", min_value=0.0, format="%.1f"),
            "Days left": st.column_config.NumberColumn("Days left to expiry", min_value=0, step=1, format="%d"),
            "Price": st.column_config.NumberColumn("Price per unit (₹)", min_value=0.0, format="%.0f"),
        },
    )
    st.caption("Click a cell and type. Press Enter or Tab to move on. Price is optional. "
               "Need more rows? Click the empty row at the bottom of the table.")

    if st.button("Add to my inventory", type="primary", key="btn_add_products"):
        rows, problems = rows_from_entry(entry)
        if problems:
            st.error("Please fix this first: " + " | ".join(problems))
        elif not rows:
            st.error("Type at least one product in the table first.")
        else:
            upsert_my_products(rows)
            st.session_state.last_added = rows
            names = ", ".join(r["product"] for r in rows)
            st.session_state.add_msg = (
                "success",
                f"Added {len(rows)} product(s): {names}. They now show on the Home and All products tabs.",
            )
            st.session_state.entry_version += 1  # clears the table for the next entry
            st.rerun()

    last = st.session_state.last_added
    if last:
        st.markdown(section("Just added", "Here is what the model says about your new products."),
                    unsafe_allow_html=True)
        preview = add_predictions(pd.DataFrame([{**row, "mine": True} for row in last]), high_thr, med_thr)
        cards = "".join(product_card(r) for _, r in preview.iterrows())
        st.markdown(f'<div class="grid">{cards}</div>', unsafe_allow_html=True)

    st.markdown(section("Your added products", "Products you added stay while this page is open."),
                unsafe_allow_html=True)
    if not st.session_state.my_products:
        st.markdown('<div class="empty">You have not added any products yet.</div>', unsafe_allow_html=True)
    else:
        mine_table = pd.DataFrame(st.session_state.my_products)[["product", "stock", "daily_sales", "days_left", "price"]]
        show_df(pretty(mine_table))
        st.selectbox("Choose a product to remove", [p["product"] for p in st.session_state.my_products],
                     key="rm_name")
        r1, r2, r3 = st.columns(3)
        r1.button("Remove selected", on_click=remove_product_callback, key="btn_remove")
        r2.button("Clear all my products", on_click=clear_products_callback, key="btn_clear")
        r3.download_button("📥 Save my products (CSV)", mine_table.to_csv(index=False),
                           "my_products.csv", "text/csv")

    st.markdown(section("Bring back saved products",
                        "A page refresh clears your list. Upload the CSV you saved to restore it."),
                unsafe_allow_html=True)
    saved = st.file_uploader("Saved products CSV", type="csv", key="saved_csv")
    if saved is not None:
        sig = (saved.name, saved.size)
        if st.session_state.get("saved_sig") != sig:
            st.session_state.saved_sig = sig
            saved_df, saved_err = read_product_csv(saved)
            if saved_err:
                st.error(saved_err)
            else:
                if "price" not in saved_df.columns:
                    saved_df["price"] = float("nan")
                rows = [
                    {"product": str(r.product).strip(), "stock": int(r.stock),
                     "daily_sales": float(r.daily_sales), "days_left": int(r.days_left),
                     "price": float(r.price)}
                    for r in saved_df.itertuples() if str(r.product).strip()
                ]
                upsert_my_products(rows)
                st.session_state.add_msg = ("success", f"Loaded {len(rows)} saved products.")
                st.rerun()

    page_footer()


# ==================================================================
# PAGE: All products
# ==================================================================
def page_products():
    st.markdown(section("All products", "Every product with its risk, filterable and downloadable.", first=True),
                unsafe_allow_html=True)
    f_col, _ = st.columns([1, 3])
    level = f_col.selectbox("Filter by risk level", ["All"] + order)
    view = data if level == "All" else data[data["risk"] == level]
    shown = view.copy()
    shown["product"] = [
        f"{icon_for(p)} {p}" + (" ★" if m else "") for p, m in zip(shown["product"], shown["mine"])
    ]
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
    st.caption("★ marks products you added yourself.")
    st.download_button("📥 Download Current Report (CSV)", view.drop(columns=["mine"]).to_csv(index=False),
                       "wastage_report.csv", "text/csv")
    page_footer()


# ==================================================================
# PAGE: Try a product
# ==================================================================
def page_try():
    st.markdown(section("Try a product", "Check any product without adding it to your inventory.", first=True),
                unsafe_allow_html=True)
    col_form, col_res = st.columns(2, gap="large")
    with col_form:
        with st.form("single_product"):
            name = st.text_input("Product name", placeholder="e.g. Organic Alphonso Mangoes")
            a, b = st.columns(2)
            stock_txt = a.text_input("Stock quantity", placeholder="e.g. 30")
            sales_txt = b.text_input("Sold per day", placeholder="e.g. 2")
            c, d = st.columns(2)
            days_txt = c.text_input("Days left to expiry", placeholder="e.g. 5")
            price_txt = d.text_input("Price per unit (₹)", placeholder="e.g. 80 (optional)")
            go = st.form_submit_button("Predict Expiry Risk", type="primary")
    with col_res:
        if go:
            stock_in = parse_number(stock_txt)
            sales_in = parse_number(sales_txt)
            days_in = parse_number(days_txt)
            price_in = parse_number(price_txt)
            missing = [label for label, v in [("stock", stock_in), ("sold per day", sales_in),
                                              ("days left", days_in)] if v is None or v < 0]
            if missing:
                st.error("Please type a valid number for: " + ", ".join(missing) + ".")
            else:
                price_val = price_in if (price_in is not None and price_in >= 0) else float("nan")
                single = pd.DataFrame(
                    [{"product": name.strip() or "Product", "stock": stock_in, "daily_sales": sales_in,
                      "days_left": days_in, "price": price_val}]
                )
                res = add_predictions(single, high_thr, med_thr).iloc[0]
                expected = sales_in * days_in
                left_units = max(stock_in - expected, 0)
                st.markdown(f'<div class="grid">{product_card(res)}</div>', unsafe_allow_html=True)
                note = (f"Projected sales: {expected:.0f} units before expiry | "
                        f"Estimated leftover: {left_units:.0f} units")
                if pd.notna(price_val):
                    note += f" (₹{left_units * price_val:,.0f})"
                st.caption(note + ".")
        else:
            st.markdown('<div class="empty">Type the product details on the left and click '
                        '<b>Predict Expiry Risk</b> to see the AI diagnosis.</div>', unsafe_allow_html=True)
    page_footer()


# ==================================================================
# PAGE: Ask the assistant
# ==================================================================
def page_chat():
    st.markdown(section("Ask the assistant", "Ask in plain words about your stock, discounts and risk.", first=True),
                unsafe_allow_html=True)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant",
             "text": "Hello! I am your FreshWatch assistant. Ask me anything about stock, discounts, expiring items, or financial risk.",
             "table": None}
        ]

    st.markdown("##### Quick Queries")
    q_cols = st.columns(4)
    quick = ["Which products are at high risk?", "What should I discount today?",
             "What is expiring soon?", "How much money is at risk?"]
    clicked = None
    for col, text in zip(q_cols, quick):
        if col.button(text, key=f"q_{text}"):
            clicked = text

    typed = st.chat_input("Type your question (e.g., 'What is most urgent?' or 'Show money at risk')")
    question = clicked or typed
    if question:
        st.session_state.messages.append({"role": "user", "text": question, "table": None})
        answer, table = chatbot_reply(question, data)
        st.session_state.messages.append({"role": "assistant", "text": answer, "table": table})

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])
            if msg["table"] is not None:
                show_df(msg["table"])
    page_footer()


# ==================================================================
# PAGE: Model accuracy
# ==================================================================
def page_accuracy():
    st.markdown(section("Model accuracy", "How well the model predicts on products it has never seen.", first=True),
                unsafe_allow_html=True)
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
        st.markdown(section("Confusion Matrix", "Evaluated on the 20% test partition."),
                    unsafe_allow_html=True)
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
        st.markdown(section("Feature Importance", "Which parameters weigh the most in predictions:"),
                    unsafe_allow_html=True)
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

    st.markdown(section("Model Benchmarks", "Comparison across three machine learning algorithms:"),
                unsafe_allow_html=True)
    comp = pd.DataFrame(metrics["comparison"]).rename(
        columns={"model": "Model", "accuracy": "Accuracy", "precision": "Precision",
                 "recall": "Recall", "f1": "F1-score"}
    )
    for c in ["Accuracy", "Precision", "Recall", "F1-score"]:
        comp[c] = (comp[c] * 100).round(1)
    show_df(comp, column_config={c: st.column_config.NumberColumn(format="%.1f%%")
                                 for c in ["Accuracy", "Precision", "Recall", "F1-score"]})
    page_footer()


# ==================================================================
# Top navigation: one click opens each page
# ==================================================================
pages = [
    st.Page(page_home, title="Home", icon="🏠", default=True),
    st.Page(page_add, title="Add my product", icon="➕", url_path="add-my-product"),
    st.Page(page_products, title="All products", icon="📋", url_path="all-products"),
    st.Page(page_try, title="Try a product", icon="🔍", url_path="try-a-product"),
    st.Page(page_chat, title="Ask the assistant", icon="💬", url_path="assistant"),
    st.Page(page_accuracy, title="Model accuracy", icon="📊", url_path="model-accuracy"),
]
try:
    nav = st.navigation(pages, position="top")
except TypeError:
    nav = st.navigation(pages)
nav.run()
