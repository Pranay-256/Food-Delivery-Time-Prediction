import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import pickle
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG  — must be the very first Streamlit call
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Food Delivery Time Predictor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS  — dark gold/teal theme (mirrors T20 analyzer)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap" rel="stylesheet">

<style>

/* ── Root design tokens ───────────────────────────────────── */
:root {
    --bg-base:      #0d1117;
    --bg-card:      #161b22;
    --bg-card2:     #1c2330;
    --border:       #2a3444;
    --gold:         #c9a84c;
    --gold-light:   #e0c070;
    --teal:         #2dd4bf;
    --teal-dim:     #1a9e8f;
    --text-primary: #e6edf3;
    --text-muted:   #8b949e;
    --text-accent:  #c9a84c;
    --danger:       #e05252;
    --success:      #3fb950;
}

/* ── Base ─────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

/* ── Streamlit chrome ─────────────────────────────────────── */
.stApp { background-color: var(--bg-base) !important; }
header[data-testid="stHeader"] {
    background: var(--bg-base) !important;
    border-bottom: 1px solid var(--border);
}
.main .block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}

/* ── Dataframe ────────────────────────────────────────────── */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    background: var(--bg-card) !important;
    padding: 4px;
}
div[data-testid="stDataFrame"] > div { background: var(--bg-card) !important; }
div[data-testid="stDataFrame"] * { color: var(--text-primary) !important; }
div[data-testid="stDataFrame"] thead { background: rgba(201,168,76,0.08) !important; }

/* ── Tabs ─────────────────────────────────────────────────── */
div[data-baseweb="tab-list"] { border-bottom: 1px solid var(--border) !important; gap: 18px; }
div[data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600;
    font-size: 16px !important;
    color: var(--text-muted) !important;
    padding: 10px 6px !important;
    background: transparent !important;
    border: none !important;
    transition: all 0.2s ease;
}
div[data-baseweb="tab"]:hover { color: var(--gold-light) !important; }
div[data-baseweb="tab"][aria-selected="true"] {
    color: var(--gold) !important;
    font-weight: 700 !important;
}
div[data-baseweb="tab-highlight"] {
    background: linear-gradient(90deg, #c9a84c, #e0c070) !important;
    height: 3px !important;
    border-radius: 2px;
}
div[data-baseweb="tab-border"] { background: transparent !important; }

/* ── Sidebar ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Radio buttons ────────────────────────────────────────── */
div[role="radiogroup"] label {
    font-family: 'Rajdhani', sans-serif !important;
    color: var(--text-primary) !important;
    font-size: 14px;
}

/* ── Primary buttons (Predict / Confirm) ──────────────────── */
div.stButton > button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700;
    font-size: 15px;
    letter-spacing: 0.5px;
    background: linear-gradient(135deg, #b8922e 0%, #e0c070 100%) !important;
    color: #0d1117 !important;
    border: none !important;
    border-radius: 8px !important;
    height: 46px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 2px 12px rgba(201,168,76,0.15) !important;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #e0c070 0%, #c9a84c 100%) !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.30) !important;
    transform: translateY(-1px) !important;
}

/* ── Selectbox ────────────────────────────────────────────── */
div[data-baseweb="select"] > div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
div[data-baseweb="select"] span { color: var(--text-primary) !important; }

/* ── Number inputs ────────────────────────────────────────── */
div[data-testid="stNumberInput"] input {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'Rajdhani', sans-serif !important;
}

/* ── Slider ───────────────────────────────────────────────── */
div[data-testid="stSlider"] * { color: var(--text-primary) !important; }

/* ── Expanders ────────────────────────────────────────────── */
div[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    margin-bottom: 10px;
}
div[data-testid="stExpander"] summary {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    color: var(--gold-light) !important;
    padding: 12px 16px !important;
}
div[data-testid="stExpander"] summary:hover {
    background: rgba(201,168,76,0.06) !important;
}
div[data-testid="stExpander"] > div > div {
    padding: 4px 20px 16px 20px !important;
    color: var(--text-primary) !important;
}

/* ── Alerts / messages ────────────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
}

/* ── Dividers ─────────────────────────────────────────────── */
hr { border-color: var(--border) !important; }

/* ── Text / paragraphs ────────────────────────────────────── */
p, li {
    color: var(--text-primary) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px;
    line-height: 1.7;
}
strong { color: var(--text-primary) !important; font-family: 'Rajdhani', sans-serif !important; }
a { color: var(--teal) !important; text-decoration: none; }
a:hover { text-decoration: underline; color: var(--gold-light) !important; }

/* ── Scrollbar ────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPER: gold-accented section heading banner
# ─────────────────────────────────────────────────────────────
def section_heading(icon, title):
    """Renders a left-gold-bordered section heading banner."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, rgba(201,168,76,0.12) 0%, transparent 100%);
        border-left: 3px solid #c9a84c;
        border-radius: 0 8px 8px 0;
        padding: 10px 18px;
        margin: 18px 0 10px 0;
    ">
        <span style="font-family:'Rajdhani',sans-serif; font-weight:700;
                     font-size:20px; color:#e0c070; letter-spacing:0.4px;">
            {icon}&nbsp; {title}
        </span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPER: column info card used in the Dataset tab
# ─────────────────────────────────────────────────────────────
def column_info(title, text):
    """Renders a styled card describing a single dataset column."""
    st.markdown(f"""
    <div style="
        background: #1c2330;
        border: 1px solid #2a3444;
        border-radius: 8px;
        padding: 10px 16px;
        margin-bottom: 8px;
    ">
        <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                  font-size:15px; color:#c9a84c; margin:0 0 4px 0;">{title}</p>
        <p style="font-family:'Rajdhani',sans-serif; font-size:13px;
                  color:#8b949e; margin:0; line-height:1.55;">{text}</p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPER: KPI / stat card
# ─────────────────────────────────────────────────────────────
def kpi_card(icon, label, value, sub=""):
    """Renders a metric highlight card with an icon, label, value, and optional subtitle."""
    sub_html = (
        f"<p style='font-size:12px; color:#8b949e; margin:2px 0 0 0; "
        f"font-family:Rajdhani,sans-serif;'>{sub}</p>"
        if sub else ""
    )
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #1c2330, #161b22);
        border: 1px solid #2a3444;
        border-top: 2px solid #c9a84c;
        border-radius: 10px;
        padding: 16px 18px;
        text-align: center;
        height: 100%;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    ">
        <div style="font-size:26px; margin-bottom:6px;">{icon}</div>
        <p style="font-family:'Rajdhani',sans-serif; font-size:12px;
                  color:#8b949e; margin:0 0 4px 0; text-transform:uppercase;
                  letter-spacing:0.8px;">{label}</p>
        <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                  font-size:22px; color:#e0c070; margin:0; line-height:1.1;">{value}</p>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPER: teal-bordered insight line
# ─────────────────────────────────────────────────────────────
def insight_line(number, text):
    """Renders a numbered insight bullet with a teal left border."""
    st.markdown(f"""
    <div style="
        background: #161b22;
        border: 1px solid #2a3444;
        border-left: 3px solid #2dd4bf;
        border-radius: 0 8px 8px 0;
        padding: 10px 16px;
        margin-bottom: 8px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    ">
        <span style="font-family:'Rajdhani',sans-serif; font-weight:700;
                     font-size:16px; color:#2dd4bf; min-width:24px;">{number}.</span>
        <span style="font-family:'Rajdhani',sans-serif; font-size:14px;
                     color:#e6edf3; line-height:1.6;">{text}</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPER: prediction result banner
# ─────────────────────────────────────────────────────────────
def prediction_banner(minutes):
    """Renders a large, eye-catching prediction result card."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1c2330 0%, #161b22 100%);
        border: 2px solid #c9a84c;
        border-radius: 14px;
        padding: 28px 24px;
        text-align: center;
        box-shadow: 0 6px 32px rgba(201,168,76,0.18);
        margin: 20px 0 10px 0;
    ">
        <div style="font-size:44px; margin-bottom:8px;">🍕</div>
        <p style="font-family:'Rajdhani',sans-serif; font-size:14px;
                  color:#8b949e; margin:0 0 6px 0; text-transform:uppercase;
                  letter-spacing:1px;">Estimated Delivery Time</p>
        <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                  font-size:52px; color:#e0c070; margin:0; line-height:1.1;">
            {minutes:.1f}
            <span style="font-size:22px; color:#c9a84c; font-weight:600;">min</span>
        </p>
        <p style="font-family:'Rajdhani',sans-serif; font-size:13px;
                  color:#8b949e; margin:10px 0 0 0;">
            Predicted by Optimized Random Forest &nbsp;·&nbsp; R² = 0.94
        </p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
def render_footer():
    """Renders the three-column footer with a credit line."""
    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
    <style>
        body { margin:0; padding:0; background:transparent; }
        .footer-wrapper {
            display: flex;
            justify-content: space-around;
            text-align: center;
            padding: 28px 0 8px 0;
            border-top: 1px solid #2a3444;
        }
        .footer-item { flex: 1; }
        .footer-item .title {
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            font-size: 16px;
            color: #c9a84c;
            margin-bottom: 4px;
        }
        .footer-item .subtitle {
            font-family: 'Rajdhani', sans-serif;
            color: #8b949e;
            font-size: 13px;
            margin-top: 0;
        }
        .footer-credit {
            text-align: center;
            font-family: 'Rajdhani', sans-serif;
            color: #8b949e;
            font-size: 13px;
            padding: 12px 0 4px 0;
        }
    </style>

    <div class="footer-wrapper">
        <div class="footer-item">
            <p class="title">&#127381; Instant Predictions</p>
            <p class="subtitle">Get delivery estimates in seconds</p>
        </div>
        <div class="footer-item">
            <p class="title">&#129504; ML-Powered</p>
            <p class="subtitle">Optimized Random Forest · R² 0.94</p>
        </div>
        <div class="footer-item">
            <p class="title">&#128202; Data-Driven</p>
            <p class="subtitle">Trained on 1,000 real delivery records</p>
        </div>
    </div>

    <p class="footer-credit">Developed by Pranay Jha, Pradeep Singh Negi and Pranav Jha &nbsp;|&nbsp; Powered by Python, Scikit-learn &amp; Streamlit</p>
    """, height=240)


# ─────────────────────────────────────────────────────────────
# LOAD MODEL & ENCODERS (cached so they load only once)
# ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    """
    Loads the trained RandomForestRegressor and the dict of LabelEncoders
    from disk. Cached by st.cache_resource so pickle files are read only
    once across all sessions.
    """
    with open("optimized_rf_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("label_encoders.pkl", "rb") as f:
        encoders = pickle.load(f)
    return model, encoders


# ─────────────────────────────────────────────────────────────
# SIDEBAR — page navigation (matches T20 analyzer pattern)
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:12px 0 8px 0;'>
        <span style="font-family:'Rajdhani',sans-serif; font-size:28px;
                     font-weight:700; color:#c9a84c; letter-spacing:1px;">
            🍕 Tool Menu
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Radio drives the two main pages
    page = st.radio("", ["Home", "About"])

    st.markdown("<hr style='border-color:#2a3444; margin:12px 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'Rajdhani',sans-serif; font-size:13px;
                color:#8b949e; line-height:1.9; padding:4px 0;">
        <strong style="color:#c9a84c;">Current Version:</strong> 1.0<br>
        <strong style="color:#c9a84c;">Release Date:</strong> April 2026<br>
        <strong style="color:#c9a84c;">Model:</strong> Random Forest (Optimized)<br>
        <strong style="color:#c9a84c;">R² Score:</strong> 0.94
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MAIN LAYOUT — centered column (mirrors T20 analyzer)
# ─────────────────────────────────────────────────────────────
left, center, right = st.columns([1, 3, 1])

with center:

    # ══════════════════════════════════════════════════════
    # HOME PAGE
    # ══════════════════════════════════════════════════════
    if page == "Home":

        # ── Hero header ───────────────────────────────────
        st.markdown("""
        <div style="text-align:center; padding:24px 0 6px 0;">
            <h1 style="font-family:'Rajdhani',sans-serif; font-weight:700;
                       font-size:38px; color:#e0c070; margin:0; letter-spacing:1px;">
                🍕 Food Delivery Time Predictor
            </h1>
            <p style="font-family:'Rajdhani',sans-serif; font-size:16px;
                      color:#8b949e; margin:6px 0 0 0;">
                ML-Powered Delivery Time Estimation Using Random Forest
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # ── Two tabs: Dataset overview | Test the model ───
        tab1, tab2 = st.tabs(["📂 Dataset", "🔮 Test The Model"])


        # ══════════════════════════════════════════════════
        # TAB 1 — DATASET
        # ══════════════════════════════════════════════════
        with tab1:

            # ── Dataset description ────────────────────────
            section_heading("📋", "About the Dataset")
            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                      margin: -6px 0 12px 0; line-height:1.7;">
                The model was trained on a structured dataset of <strong style="color:#e0c070;">1,000 food delivery
                records</strong>. Each row represents a single delivery and captures the key factors that
                influence how long a delivery takes — from road distance and weather conditions to the
                experience level of the courier and the time of day.
            </p>
            """, unsafe_allow_html=True)

            # ── KPI row: quick dataset stats ──────────────
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                kpi_card("📦", "Total Records",    "1,000",  "Unique deliveries")
            with c2:
                kpi_card("🔢", "Features",         "7",      "Input variables")
            with c3:
                kpi_card("🎯", "Target Variable",  "Delivery Time", "In minutes")
            with c4:
                kpi_card("🌦️", "Weather Types",    "5",      "Clear · Rainy · Foggy · Snowy · Windy")

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Sample data preview ────────────────────────
            section_heading("👁️", "Sample Data Preview")
            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                      margin: -6px 0 10px 0; line-height:1.6;">
                A snapshot of the first 8 rows from the training dataset.
            </p>
            """, unsafe_allow_html=True)

            # Load a small sample for display only
            sample_df = pd.read_csv("Food_Delivery_Times.csv", nrows=8)
            st.dataframe(sample_df, use_container_width=True)

            st.divider()

            # ── Column-by-column breakdown using expanders ─
            section_heading("🗂️", "Dataset Columns Overview")
            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                      margin: -6px 0 12px 0; line-height:1.6;">
                Expand each section below to understand what each column represents
                and how it was used during model training.
            </p>
            """, unsafe_allow_html=True)

            # ── Expander 1: Identifiers ──────────────────
            with st.expander("🔑 Order Identifier", expanded=False):
                column_info("Order_ID",
                    "A unique integer identifier assigned to each delivery order. "
                    "This column was dropped before model training as it carries no "
                    "predictive information — it is purely an index. "
                    "Range: 1 – 1000. Datatype: Integer.")

            # ── Expander 2: Numerical features ───────────
            with st.expander("🔢 Numerical Features (Model Inputs)", expanded=False):
                column_info("Distance_km",
                    "The total road distance (in kilometres) between the restaurant and the delivery address. "
                    "Longer distances generally lead to longer delivery times and are one of the strongest "
                    "predictors in the model. "
                    "Range: 0.59 – 19.99 km. Datatype: Float.")

                column_info("Preparation_Time_min",
                    "The time (in minutes) the restaurant needs to prepare the order before it is handed "
                    "to the courier. Higher preparation times naturally increase total delivery time. "
                    "Range: 5 – 29 minutes. Datatype: Integer.")

                column_info("Courier_Experience_yrs",
                    "The number of years the delivery courier has been working. More experienced couriers "
                    "tend to navigate faster, resulting in shorter delivery times. "
                    "30 missing values were filled with the column median during data cleaning. "
                    "Range: 0 – 9 years. Datatype: Float.")

            # ── Expander 3: Categorical features ─────────
            with st.expander("🏷️ Categorical Features (Model Inputs)", expanded=False):
                column_info("Weather",
                    "Current weather conditions at the time of delivery. "
                    "Adverse weather (Snowy, Rainy, Foggy) typically increases travel time. "
                    "Categories: Clear · Foggy · Rainy · Snowy · Windy. "
                    "Missing values were filled with the mode before encoding. "
                    "Encoded using LabelEncoder before training.")

                column_info("Traffic_Level",
                    "The level of road traffic the courier encounters. "
                    "Higher traffic levels significantly extend delivery time. "
                    "Categories: Low · Medium · High. "
                    "Encoded using LabelEncoder before training.")

                column_info("Time_of_Day",
                    "The part of the day when the delivery takes place. "
                    "Peak hours (Afternoon / Evening) typically see heavier traffic. "
                    "Categories: Morning · Afternoon · Evening · Night. "
                    "Missing values filled with mode. Encoded using LabelEncoder.")

                column_info("Vehicle_Type",
                    "The type of vehicle used by the courier for the delivery. "
                    "Cars tend to carry capacity-heavy orders while Bikes and Scooters "
                    "navigate urban traffic more efficiently. "
                    "Categories: Bike · Car · Scooter. "
                    "Encoded using LabelEncoder before training.")

            # ── Expander 4: Target variable ───────────────
            with st.expander("🎯 Target Variable (Prediction Output)", expanded=False):
                column_info("Delivery_Time_min",
                    "The total time (in minutes) taken to deliver the order from the moment it was placed, "
                    "including both preparation time and travel time. "
                    "This is the variable the model is trained to predict. "
                    "Range: 8 – 153 minutes · Mean: ~56.7 min · Std: ~22.1 min. "
                    "Datatype: Integer.")

            st.divider()

            # ── Model performance summary ──────────────────
            section_heading("📊", "Model Performance at a Glance")
            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                      margin: -6px 0 12px 0; line-height:1.6;">
                The Optimized Random Forest was tuned using <strong style="color:#e0c070;">RandomizedSearchCV
                (100 iterations, 5-fold CV)</strong> and outperforms the default baseline across all metrics.
            </p>
            """, unsafe_allow_html=True)

            # Performance comparison table as cards
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                kpi_card("📈", "R² Score",  "0.94", "vs 0.92 baseline")
            with m2:
                kpi_card("📉", "MAE",       "0.50 min", "vs 0.55 baseline")
            with m3:
                kpi_card("📉", "RMSE",      "0.63 min", "vs 0.67 baseline")
            with m4:
                kpi_card("🌲", "Estimators","781 trees", "Best via tuning")

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Key model insights ─────────────────────────
            section_heading("💡", "Key Dataset Insights")
            insight_line(1, "Distance is the strongest predictor — longer routes consistently produce longer delivery times.")
            insight_line(2, "Adverse weather (Snowy / Rainy) adds measurable delay versus Clear conditions.")
            insight_line(3, "High traffic level can independently increase delivery time regardless of distance.")
            insight_line(4, "More experienced couriers (7–9 yrs) deliver noticeably faster than new couriers (0–1 yr).")
            insight_line(5, "All four categorical features passed the ANOVA test (p < 0.05), confirming statistical significance.")

            st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)


        # ══════════════════════════════════════════════════
        # TAB 2 — TEST THE MODEL
        # ══════════════════════════════════════════════════
        with tab2:

            # Load model artifacts (cached)
            try:
                model, label_encoders = load_artifacts()
            except Exception as e:
                st.error(f"Could not load model files: {e}")
                st.stop()

            section_heading("🔮", "Predict Delivery Time")
            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#8b949e;
                      margin: -6px 0 14px 0; line-height:1.6;">
                Fill in the delivery details below and click <strong style="color:#e0c070;">Predict</strong>
                to get an estimated delivery time from the trained Random Forest model.
            </p>
            """, unsafe_allow_html=True)

            # ── Input form — two-column layout ────────────
            col_left, col_right = st.columns(2)

            # ── Left column: Numerical inputs ─────────────
            with col_left:
                section_heading("🔢", "Numerical Inputs")

                distance_km = st.number_input(
                    "📍 Distance (km)",
                    min_value=0.5,
                    max_value=20.0,
                    value=10.0,
                    step=0.1,
                    help="Road distance from restaurant to delivery address."
                )

                preparation_time = st.number_input(
                    "🍳 Preparation Time (min)",
                    min_value=5,
                    max_value=30,
                    value=15,
                    step=1,
                    help="Time the restaurant needs to prepare the order."
                )

                courier_experience = st.number_input(
                    "🧑‍💼 Courier Experience (years)",
                    min_value=0.0,
                    max_value=9.0,
                    value=3.0,
                    step=0.5,
                    help="Number of years the courier has been delivering."
                )

            # ── Right column: Categorical inputs ──────────
            with col_right:
                section_heading("🏷️", "Categorical Inputs")

                weather_options   = list(label_encoders["Weather"].classes_)
                weather_selected  = st.selectbox(
                    "🌦️ Weather Condition",
                    weather_options,
                    help="Current weather at the time of delivery."
                )

                traffic_options   = list(label_encoders["Traffic_Level"].classes_)
                traffic_selected  = st.selectbox(
                    "🚦 Traffic Level",
                    traffic_options,
                    help="Road traffic level — Low, Medium, or High."
                )

                time_options      = list(label_encoders["Time_of_Day"].classes_)
                time_selected     = st.selectbox(
                    "🕐 Time of Day",
                    time_options,
                    help="Part of the day when the delivery takes place."
                )

                vehicle_options   = list(label_encoders["Vehicle_Type"].classes_)
                vehicle_selected  = st.selectbox(
                    "🏍️ Vehicle Type",
                    vehicle_options,
                    help="Type of vehicle used by the courier."
                )

            st.markdown("")

            # ── Predict button (full width) ────────────────
            predict_clicked = st.button("🔮 Predict Delivery Time", use_container_width=True)

            if predict_clicked:
                try:
                    # Encode categorical inputs using the saved LabelEncoders
                    weather_enc  = label_encoders["Weather"].transform([weather_selected])[0]
                    traffic_enc  = label_encoders["Traffic_Level"].transform([traffic_selected])[0]
                    time_enc     = label_encoders["Time_of_Day"].transform([time_selected])[0]
                    vehicle_enc  = label_encoders["Vehicle_Type"].transform([vehicle_selected])[0]

                    # Build input DataFrame — column order must match training
                    input_df = pd.DataFrame(
                        [[distance_km, weather_enc, traffic_enc, time_enc,
                          vehicle_enc, preparation_time, courier_experience]],
                        columns=[
                            "Distance_km", "Weather", "Traffic_Level", "Time_of_Day",
                            "Vehicle_Type", "Preparation_Time_min", "Courier_Experience_yrs"
                        ]
                    )

                    # Run inference
                    prediction = model.predict(input_df)[0]

                    # Render the large result banner
                    prediction_banner(prediction)

                    # ── Context cards below result ─────────
                    st.markdown("<br>", unsafe_allow_html=True)
                    section_heading("📋", "Inputs Used for Prediction")

                    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
                    with r1c1:
                        kpi_card("📍", "Distance",     f"{distance_km:.1f} km")
                    with r1c2:
                        kpi_card("🍳", "Prep Time",    f"{preparation_time} min")
                    with r1c3:
                        kpi_card("🧑‍💼", "Experience",  f"{courier_experience} yrs")
                    with r1c4:
                        kpi_card("🌦️", "Weather",      weather_selected)

                    st.markdown("<br>", unsafe_allow_html=True)

                    r2c1, r2c2, r2c3 = st.columns(3)
                    with r2c1:
                        kpi_card("🚦", "Traffic",      traffic_selected)
                    with r2c2:
                        kpi_card("🕐", "Time of Day",  time_selected)
                    with r2c3:
                        kpi_card("🏍️", "Vehicle",      vehicle_selected)

                except Exception as e:
                    st.error(f"Prediction failed: {e}")

            # ── Tip section shown when no prediction yet ───
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("💡 Tips for Using the Predictor", expanded=True):
                    insight_line(1, "Distance has the biggest impact — even a few extra kilometres significantly increases estimated time.")
                    insight_line(2, "Select <strong>High</strong> traffic to simulate peak-hour conditions like lunch or dinner rush.")
                    insight_line(3, "Couriers with <strong>0–1 year</strong> of experience tend to take longer than those with <strong>7+ years</strong>.")
                    insight_line(4, "Snowy and Rainy weather conditions add the most delay compared to Clear weather.")
                    insight_line(5, "Prediction accuracy: <strong>MAE ≈ 0.50 min</strong> — results are typically within 1 minute of actual time.")

            st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)


    # ══════════════════════════════════════════════════════
    # ABOUT PAGE
    # ══════════════════════════════════════════════════════
    elif page == "About":

        # ── Hero header ───────────────────────────────────
        st.markdown("""
        <div style="text-align:center; padding:24px 0 6px 0;">
            <h1 style="font-family:'Rajdhani',sans-serif; font-weight:700;
                       font-size:38px; color:#e0c070; margin:0; letter-spacing:1px;">
                🍕 Food Delivery Time Predictor
            </h1>
            <p style="font-family:'Rajdhani',sans-serif; font-size:16px;
                      color:#8b949e; margin:6px 0 0 0;">
                ML-Powered Delivery Time Estimation Using Random Forest
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

#        # ── About the developer ────────────────────────────
#        with st.expander("👨‍💻 About the Developer — Pranay Jha", expanded=False):
#            st.markdown("""
#            <div style="font-family:'Rajdhani',sans-serif; font-size:14px;
#                        color:#e6edf3; line-height:1.8;">
#                Hello! My name is <strong style="color:#e0c070;">Pranay Jha</strong>, and I am currently pursuing a
#                <strong style="color:#e0c070;">Bachelor of Technology (B.Tech) in Computer Science and Engineering</strong>.<br><br>
#                I am actively learning and exploring the fields of
#                <strong style="color:#e0c070;">Machine Learning, Data Science, and Predictive Analytics</strong>.<br><br>
#                This project — <strong style="color:#c9a84c;">Food Delivery Time Predictor</strong> — is part of my
#                learning journey in applied machine learning, demonstrating how real-world regression problems can
#                be solved with ensemble models and deployed as interactive web tools.<br><br>
#                The tool uses Python libraries including
#                <strong style="color:#2dd4bf;">NumPy, Pandas, Scikit-learn, and Streamlit</strong>.
#            </div>
#            """, unsafe_allow_html=True)
#
#            st.markdown("<br>", unsafe_allow_html=True)
#
#            st.markdown("""
#            <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
#                       font-size:17px; color:#c9a84c; margin-bottom:8px;">
#                🚀 Key Highlights
#            </p>
#            """, unsafe_allow_html=True)
#
#            for item in [
#                "Built a <strong>regression model</strong> on real-world structured delivery data",
#                "Performed <strong>data cleaning, EDA, and feature engineering</strong>",
#                "Applied <strong>LabelEncoding</strong> to categorical features for model training",
#                "Tuned hyperparameters using <strong>RandomizedSearchCV (100 iterations, 5-fold CV)</strong>",
#                "Deployed the model as an <strong>interactive Streamlit web application</strong>",
#            ]:
#                st.markdown(f"""
#                <div style="background:#1c2330; border:1px solid #2a3444; border-radius:6px;
#                            padding:8px 14px; margin-bottom:6px; font-family:'Rajdhani',sans-serif;
#                            font-size:14px; color:#e6edf3;">
#                    ▸ &nbsp;{item}
#                </div>
#                """, unsafe_allow_html=True)
#
#            st.markdown("<br>", unsafe_allow_html=True)
#
#            st.markdown("""
#            <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
#                       font-size:17px; color:#c9a84c; margin-bottom:8px;">
#                🔗 Connect With Me
#            </p>
#            """, unsafe_allow_html=True)
#
#            st.markdown("""
#            <div style="display:flex; gap:14px; flex-wrap:wrap;">
#                <a href="https://github.com/Pranay-256" target="_blank"
#                   style="display:inline-flex; align-items:center; gap:8px;
#                          background:#1c2330; border:1px solid #2a3444;
#                          border-radius:8px; padding:10px 18px;
#                          font-family:'Rajdhani',sans-serif; font-size:14px;
#                          color:#e6edf3; text-decoration:none;">
#                    <span style="font-size:18px;">🐙</span>
#                    <strong>GitHub</strong> — Pranay-256
#                </a>
#                <a href="https://www.linkedin.com/in/pranay-jha-6582a937b/" target="_blank"
#                   style="display:inline-flex; align-items:center; gap:8px;
#                          background:#1c2330; border:1px solid #2a3444;
#                          border-radius:8px; padding:10px 18px;
#                          font-family:'Rajdhani',sans-serif; font-size:14px;
#                          color:#e6edf3; text-decoration:none;">
#                    <span style="font-size:18px;">💼</span>
#                    <strong>LinkedIn</strong> — Pranay Jha
#                </a>
#            </div>
#            """, unsafe_allow_html=True)
#            st.markdown("<br>", unsafe_allow_html=True)

        # ── Problem statement ──────────────────────────────
        with st.expander("❗ Problem Statement", expanded=False):
            st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif; font-size:14px;
                        color:#e6edf3; line-height:1.8; margin-bottom:10px;">
                Accurate delivery time estimation is a <strong style="color:#e0c070;">critical challenge</strong>
                for food delivery platforms, restaurants, and logistics operations.
                When estimated times are inaccurate, it leads to customer dissatisfaction,
                poor courier planning, and revenue loss.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                       font-size:17px; color:#c9a84c; margin:8px 0;">⚠️ Key Challenges</p>
            """, unsafe_allow_html=True)

            for item in [
                "Delivery time depends on <strong>multiple interacting factors</strong> (distance, weather, traffic, courier skill)",
                "Simple rule-based estimates <strong>fail in dynamic real-world conditions</strong>",
                "Categorical factors like <strong>weather and traffic are hard to quantify</strong> manually",
                "No easy way to <strong>compare courier performance</strong> against expected baselines",
                "Customers expect <strong>precise ETAs</strong>, not just rough estimates",
            ]:
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-left:3px solid #e05252;
                            border-radius:0 6px 6px 0; padding:8px 14px; margin-bottom:6px;
                            font-family:'Rajdhani',sans-serif; font-size:14px; color:#e6edf3;">
                    {item}
                </div>
                """, unsafe_allow_html=True)

        # ── Objective ──────────────────────────────────────
        with st.expander("🎯 Objective", expanded=False):
            st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif; font-size:14px;
                        color:#e6edf3; line-height:1.8; margin-bottom:10px;">
                The goal is to build a <strong style="color:#e0c070;">reliable, data-driven regression model</strong>
                that predicts food delivery time in minutes based on readily available order and
                environmental information — replacing guesswork with accurate ML-based estimates.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                       font-size:17px; color:#c9a84c; margin:8px 0;">📊 Core Focus Areas</p>
            """, unsafe_allow_html=True)

            for item in [
                "Identify the key <strong>features that drive delivery time</strong>",
                "Train a <strong>Random Forest Regressor</strong> with hyperparameter tuning",
                "Achieve <strong>high predictive accuracy</strong> (target R² > 0.90)",
                "Provide an <strong>interactive tool</strong> for instant predictions",
                "Make the model <strong>transparent and explainable</strong> via dataset documentation",
            ]:
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-left:3px solid #3fb950;
                            border-radius:0 6px 6px 0; padding:8px 14px; margin-bottom:6px;
                            font-family:'Rajdhani',sans-serif; font-size:14px; color:#e6edf3;">
                    ✓ &nbsp;{item}
                </div>
                """, unsafe_allow_html=True)

        # ── Tech stack ─────────────────────────────────────
        with st.expander("🛠️ Tech Stack", expanded=False):
            st.markdown("""
            <p style="font-family:'Rajdhani',sans-serif; font-size:14px; color:#e6edf3;
                      line-height:1.8; margin-bottom:10px;">
                Built using the <strong style="color:#e0c070;">Python ML ecosystem</strong>
                combined with an interactive deployment framework.
            </p>
            """, unsafe_allow_html=True)

            tools = [
                ("🐍 Python",           "Core language for data processing and ML"),
                ("🔢 NumPy",            "Numerical operations and array handling"),
                ("🐼 Pandas",           "Data cleaning, manipulation, and EDA"),
                ("🤖 Scikit-learn",     "LabelEncoder, RandomForestRegressor, RandomizedSearchCV"),
                ("💾 Pickle",           "Serialisation and loading of trained model artifacts"),
                ("🚀 Streamlit",        "Interactive web dashboard for model inference"),
            ]
            for name, desc in tools:
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-radius:8px;
                            padding:10px 16px; margin-bottom:7px;
                            font-family:'Rajdhani',sans-serif; font-size:14px; color:#e6edf3;
                            display:flex; gap:10px; align-items:flex-start;">
                    <strong style="color:#c9a84c; min-width:120px;">{name}</strong>
                    <span style="color:#8b949e;">{desc}</span>
                </div>
                """, unsafe_allow_html=True)

        # ── ML approach ────────────────────────────────────
        with st.expander("🤖 ML Approach & Methodology", expanded=False):

            def ml_block(emoji, title, items):
                """Renders a titled list block inside the ML approach expander."""
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-radius:8px;
                            padding:12px 16px; margin-bottom:10px;">
                    <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                              font-size:17px; color:#c9a84c; margin:0 0 6px 0;">
                        {emoji} {title}
                    </p>
                    {''.join(f"<p style='font-family:Rajdhani,sans-serif; font-size:14px; color:#e6edf3; margin:3px 0;'>▸ &nbsp;{item}</p>" for item in items)}
                </div>
                """, unsafe_allow_html=True)

            ml_block("🧹", "Data Preprocessing", [
                "Dropped Order_ID (non-predictive identifier)",
                "Filled missing Weather, Traffic_Level, Time_of_Day with mode",
                "Filled missing Courier_Experience_yrs with median (30 values)",
                "Applied LabelEncoder to all 4 categorical features",
            ])

            ml_block("🔬", "Feature Selection & Testing", [
                "Pearson correlation for numerical features vs Delivery_Time_min",
                "One-Way ANOVA for categorical features — all 4 passed (p < 0.05)",
                "All 7 features retained based on statistical significance",
            ])

            ml_block("🌲", "Model Training & Tuning", [
                "Baseline: Decision Tree Regressor (R² = ~0.92)",
                "Baseline: Default Random Forest (R² = 0.92)",
                "Tuned: RandomizedSearchCV — 100 iterations, 5-fold CV",
                "Best params: n_estimators=781, max_depth=11, max_features=3, "
                "min_samples_split=3, min_samples_leaf=3",
                "Optimized Random Forest: R² = 0.94, MAE = 0.50, RMSE = 0.63",
            ])

        # ── Version history ────────────────────────────────
        with st.expander("🔄 Version History", expanded=False):

            def version_block(version, date, items):
                """Renders a version changelog block."""
                st.markdown(f"""
                <div style="background:#1c2330; border:1px solid #2a3444; border-radius:8px;
                            padding:12px 16px; margin-bottom:10px;">
                    <p style="font-family:'Rajdhani',sans-serif; font-weight:700;
                              font-size:16px; color:#c9a84c; margin:0 0 4px 0;">
                        Version {version} &nbsp;·&nbsp;
                        <span style="color:#8b949e; font-size:14px; font-weight:500;">{date}</span>
                    </p>
                    {''.join(f"<p style='font-family:Rajdhani,sans-serif; font-size:13px; color:#e6edf3; margin:3px 0;'>— {i}</p>" for i in items)}
                </div>
                """, unsafe_allow_html=True)

            version_block("1.0", "April 2026", [
                "Initial release of Food Delivery Time Predictor",
                "Optimized Random Forest model with R² = 0.94",
                "Full dark-themed Streamlit UI with gold/teal design system",
                "Dataset overview tab with column documentation",
                "Interactive prediction form with instant result banner",
                "About section with developer info, methodology, and version history",
            ])

        st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# FOOTER — rendered on every page
# ─────────────────────────────────────────────────────────────
render_footer()
