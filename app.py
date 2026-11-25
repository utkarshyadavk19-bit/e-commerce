import os
import time
import pickle
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Shopper Intent AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "entered_app" not in st.session_state:
    st.session_state.entered_app = False

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 18% 12%, #172554 0%, #0b1120 48%, #050811 100%);
}
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-18px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(22px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes floatSlow {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-7px); }
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(56, 189, 248, 0.35); }
    50% { box-shadow: 0 0 36px rgba(99, 102, 241, 0.72); }
}
@keyframes barGrow { from { width: 0%; } }

.cover-card {
    background: linear-gradient(145deg, rgba(30, 41, 59, 0.78), rgba(15, 23, 42, 0.94));
    border: 1px solid rgba(99, 102, 241, 0.38);
    border-radius: 24px;
    padding: 32px 28px 24px 28px;
    margin: 8px auto 18px auto;
    box-shadow: 0 20px 55px rgba(0, 0, 0, 0.55);
    text-align: center;
    animation: fadeSlideDown 0.7s ease-out;
}
.cover-pill {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1px;
    color: #93c5fd;
    background: rgba(59, 130, 246, 0.16);
    border: 1px solid rgba(96, 165, 250, 0.4);
    margin-bottom: 12px;
    animation: floatSlow 3.2s ease-in-out infinite;
}
.cover-title {
    font-size: 2.6rem;
    font-weight: 900;
    line-height: 1.15;
    margin: 0 0 10px 0;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399, #38bdf8);
    background-size: 250% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 5.5s linear infinite;
}
.cover-sub {
    color: #cbd5e1;
    font-size: 1.02rem;
    max-width: 700px;
    margin: 0 auto 18px auto;
    line-height: 1.5;
}
.feature-card {
    background: rgba(15, 23, 42, 0.78);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    animation: fadeSlideUp 0.8s ease-out;
    transition: transform 0.25s ease, border-color 0.25s ease;
}
.feature-card:hover {
    transform: translateY(-5px);
    border-color: rgba(56, 189, 248, 0.55);
}
.feature-title { color: #f8fafc; font-size: 1rem; font-weight: 700; margin: 10px 0 5px 0; }
.feature-desc { color: #94a3b8; font-size: 0.86rem; margin: 0; }

.hero-box {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.94));
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 18px;
    padding: 18px 24px;
    margin-bottom: 16px;
    animation: fadeSlideDown 0.55s ease-out;
}
.hero-title {
    font-size: 1.9rem;
    font-weight: 800;
    margin: 0 0 4px 0;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399, #38bdf8);
    background-size: 250% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 6s linear infinite;
}
.hero-sub { color: #94a3b8; font-size: 0.92rem; margin: 0; }
.card-header {
    font-size: 1rem;
    font-weight: 700;
    color: #e2e8f0;
    padding-bottom: 8px;
    margin-bottom: 12px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #4f46e5, #0ea5e9);
    border: none;
    border-radius: 14px;
    padding: 0.8rem 1.4rem;
    font-size: 1.06rem;
    font-weight: 800;
    color: #ffffff;
    animation: pulseGlow 2.8s infinite;
    transition: transform 0.25s ease;
}
div.stButton > button[kind="primary"]:hover { transform: translateY(-3px) scale(1.015); }

.result-card {
    border-radius: 18px;
    padding: 22px;
    text-align: center;
    animation: fadeSlideUp 0.55s cubic-bezier(0.16, 1, 0.3, 1);
}
.result-buy {
    background: linear-gradient(145deg, rgba(16, 185, 129, 0.16), rgba(6, 78, 59, 0.3));
    border: 1.5px solid rgba(52, 211, 153, 0.55);
    box-shadow: 0 0 28px rgba(16, 185, 129, 0.22);
}
.result-nobuy {
    background: linear-gradient(145deg, rgba(245, 158, 11, 0.14), rgba(120, 53, 15, 0.26));
    border: 1.5px solid rgba(251, 191, 36, 0.5);
    box-shadow: 0 0 28px rgba(245, 158, 11, 0.18);
}
.signal-row { margin: 11px 0; text-align: left; }
.signal-label { display: flex; justify-content: space-between; font-size: 0.86rem; color: #cbd5e1; margin-bottom: 4px; }
.signal-track { width: 100%; height: 9px; background: rgba(148, 163, 184, 0.16); border-radius: 999px; overflow: hidden; }
.signal-fill { height: 100%; border-radius: 999px; animation: barGrow 1s ease-out; }
</style>
""", unsafe_allow_html=True)

# ---------------- VIEW 1: CLICK-TO-OPEN FRONT COVER ----------------
if not st.session_state.entered_app:
    st.markdown("""
<style>
section[data-testid="stSidebar"] { display: none; }
button[data-testid="collapsedControl"] { display: none; }
</style>
""", unsafe_allow_html=True)

    cover_svg = """
<svg viewBox="0 0 760 210" width="100%" style="max-width:720px; height:auto; margin:8px auto 0 auto; display:block;">
<defs>
<linearGradient id="bgG" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#1e293b" stop-opacity="0.95"/>
<stop offset="100%" stop-color="#0f172a" stop-opacity="0.98"/>
</linearGradient>
<linearGradient id="ac1" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#38bdf8"/><stop offset="100%" stop-color="#818cf8"/>
</linearGradient>
<linearGradient id="ac2" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#34d399"/><stop offset="100%" stop-color="#0ea5e9"/>
</linearGradient>
</defs>
<rect x="8" y="8" width="744" height="194" rx="20" fill="url(#bgG)" stroke="rgba(99,102,241,0.45)" stroke-width="1.5"/>
<circle cx="130" cy="105" r="62" fill="rgba(56,189,248,0.1)" stroke="rgba(56,189,248,0.35)" stroke-width="1.5"/>
<path d="M100 86 h12 l10 40 h40 l10-26 h-44" fill="none" stroke="url(#ac1)" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="127" cy="140" r="6" fill="#34d399"/><circle cx="158" cy="140" r="6" fill="#34d399"/>
<path d="M210 105 C255 105,255 62,305 62" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6 4"/>
<path d="M210 105 L305 105" fill="none" stroke="#818cf8" stroke-width="2" stroke-dasharray="6 4"/>
<path d="M210 105 C255 105,255 148,305 148" fill="none" stroke="#34d399" stroke-width="2" stroke-dasharray="6 4"/>
<circle cx="310" cy="62" r="10" fill="#0ea5e9" stroke="#e0f2fe" stroke-width="2"/>
<circle cx="310" cy="105" r="10" fill="#6366f1" stroke="#e0e7ff" stroke-width="2"/>
<circle cx="310" cy="148" r="10" fill="#10b981" stroke="#d1fae5" stroke-width="2"/>
<line x1="322" y1="62" x2="405" y2="85" stroke="rgba(148,163,184,0.45)" stroke-width="2"/>
<line x1="322" y1="105" x2="405" y2="85" stroke="rgba(148,163,184,0.45)" stroke-width="2"/>
<line x1="322" y1="105" x2="405" y2="126" stroke="rgba(148,163,184,0.45)" stroke-width="2"/>
<line x1="322" y1="148" x2="405" y2="126" stroke="rgba(148,163,184,0.45)" stroke-width="2"/>
<circle cx="415" cy="85" r="12" fill="#818cf8" stroke="#ffffff" stroke-width="2"/>
<circle cx="415" cy="126" r="12" fill="#34d399" stroke="#ffffff" stroke-width="2"/>
<rect x="475" y="38" width="240" height="134" rx="16" fill="rgba(15,23,42,0.88)" stroke="rgba(52,211,153,0.45)" stroke-width="1.5"/>
<text x="495" y="65" fill="#94a3b8" font-size="11" font-weight="700" letter-spacing="1">CONVERSION FORECAST</text>
<rect x="500" y="118" width="22" height="36" rx="5" fill="#38bdf8" opacity="0.65"/>
<rect x="534" y="100" width="22" height="54" rx="5" fill="#818cf8" opacity="0.8"/>
<rect x="568" y="84" width="22" height="70" rx="5" fill="#34d399"/>
<rect x="602" y="70" width="22" height="84" rx="5" fill="url(#ac2)"/>
<text x="642" y="110" fill="#34d399" font-size="24" font-weight="800">92%</text>
<text x="642" y="128" fill="#cbd5e1" font-size="10">ACCURACY</text>
</svg>
"""

    custom_cover = "cover.png" if os.path.exists("cover.png") else ("cover.jpg" if os.path.exists("cover.jpg") else None)
    visual_block = "" if custom_cover else cover_svg

    st.markdown(f"""
<div class="cover-card">
<div class="cover-pill">B.TECH MACHINE LEARNING PROJECT • LIVE WEB DEMO</div>
<div class="cover-title">Online Shoppers Purchasing Intention</div>
<p class="cover-sub">An interactive machine learning web app that analyses real-time e-commerce browsing signals—page values, bounce rates, session duration, and seasonality—to predict whether a visitor will purchase.</p>
{visual_block}
</div>
""", unsafe_allow_html=True)

    if custom_cover:
        st.image(custom_cover, use_container_width=True)

    _, mid_btn, _ = st.columns([1.2, 1.6, 1.2])
    with mid_btn:
        if st.button("🚀 Click to Open Predictor App", type="primary", use_container_width=True):
            st.session_state.entered_app = True
            st.rerun()

    st.write("")
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown("""
<div class="feature-card">
<svg width="44" height="44" viewBox="0 0 48 48">
<circle cx="24" cy="24" r="22" fill="rgba(56,189,248,0.14)" stroke="#38bdf8" stroke-width="1.5"/>
<rect x="13" y="25" width="5" height="11" rx="2" fill="#38bdf8"/>
<rect x="21" y="19" width="5" height="17" rx="2" fill="#818cf8"/>
<rect x="29" y="13" width="5" height="23" rx="2" fill="#34d399"/>
</svg>
<div class="feature-title">12,330 Shopper Sessions</div>
<p class="feature-desc">Cleaned with IQR outlier handling, One-Hot Encoding, and StandardScaler preprocessing.</p>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="feature-card">
<svg width="44" height="44" viewBox="0 0 48 48">
<circle cx="24" cy="24" r="22" fill="rgba(129,140,248,0.14)" stroke="#818cf8" stroke-width="1.5"/>
<circle cx="16" cy="18" r="3.5" fill="#38bdf8"/><circle cx="32" cy="18" r="3.5" fill="#34d399"/>
<circle cx="24" cy="31" r="4" fill="#818cf8"/>
<line x1="18" y1="20" x2="23" y2="28" stroke="#cbd5e1" stroke-width="1.5"/>
<line x1="30" y1="20" x2="25" y2="28" stroke="#cbd5e1" stroke-width="1.5"/>
</svg>
<div class="feature-title">4 ML Models Benchmarked</div>
<p class="feature-desc">Logistic Regression, Decision Tree, Random Forest, and KNN/SVM up to 92% accuracy.</p>
</div>
""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class="feature-card">
<svg width="44" height="44" viewBox="0 0 48 48">
<circle cx="24" cy="24" r="22" fill="rgba(52,211,153,0.14)" stroke="#34d399" stroke-width="1.5"/>
<path d="M13 28 A11 11 0 0 1 35 28" fill="none" stroke="#34d399" stroke-width="3" stroke-linecap="round"/>
<line x1="24" y1="28" x2="31" y2="19" stroke="#f8fafc" stroke-width="2.5" stroke-linecap="round"/>
<circle cx="24" cy="28" r="3" fill="#38bdf8"/>
</svg>
<div class="feature-title">Instant Live Inference</div>
<p class="feature-desc">Real-time purchase probability gauge with animated engagement health bars.</p>
</div>
""", unsafe_allow_html=True)

    st.stop()

# ---------------- VIEW 2: MAIN PREDICTOR APP ----------------
@st.cache_resource
def load_artifacts():
    with open("best_shopper_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("feature_columns.pkl", "rb") as f:
        feature_cols = pickle.load(f)
    return model, scaler, feature_cols

model, scaler, feature_cols = load_artifacts()

MONTHS = ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
VISITOR_TYPES = ["Returning_Visitor", "New_Visitor", "Other"]

PRESETS = {
    "high": {"product_pages": 25, "product_duration": 950.0, "admin_pages": 4, "page_values": 35.0, "bounce_rate": 0.005, "exit_rate": 0.015, "month": "Nov", "visitor_type": "Returning_Visitor", "is_weekend": True},
    "mid": {"product_pages": 12, "product_duration": 380.0, "admin_pages": 1, "page_values": 8.0, "bounce_rate": 0.030, "exit_rate": 0.050, "month": "Oct", "visitor_type": "New_Visitor", "is_weekend": True},
    "low": {"product_pages": 2, "product_duration": 25.0, "admin_pages": 0, "page_values": 0.0, "bounce_rate": 0.150, "exit_rate": 0.200, "month": "May", "visitor_type": "Returning_Visitor", "is_weekend": False},
}

for k, v in PRESETS["high"].items():
    if k not in st.session_state:
        st.session_state[k] = v

def apply_preset(key):
    for k, v in PRESETS[key].items():
        st.session_state[k] = v

with st.sidebar:
    if st.button("🏠 Back to Front Cover", use_container_width=True):
        st.session_state.entered_app = False
        st.rerun()
    st.divider()
    st.markdown("### ⚡ Quick Demo Presets")
    st.button("🟢 High-Intent Festive Buyer", use_container_width=True, on_click=apply_preset, args=("high",))
    st.button("🟡 Borderline New Visitor", use_container_width=True, on_click=apply_preset, args=("mid",))
    st.button("🔴 Casual Window Shopper", use_container_width=True, on_click=apply_preset, args=("low",))
    st.divider()
    st.markdown(f"**Model:** `{type(model).__name__}`  \n**Features:** `{len(feature_cols)}`  \n**Scaler:** `StandardScaler`")

st.markdown("""
<div class="hero-box">
<div class="hero-title">🛒 Online Shoppers Purchasing Intention</div>
<p class="hero-sub">Adjust visitor browsing signals below or select a quick preset from the sidebar to forecast conversion probability.</p>
</div>
""", unsafe_allow_html=True)

tab_predict, tab_visuals = st.tabs(["🎯 Live Predictor", "🖼️ Project Visuals & Pipeline"])

with tab_predict:
    left_col, right_col = st.columns([1.25, 1], gap="large")

    with left_col:
        with st.container(border=True):
            st.markdown('<div class="card-header">📊 Browsing & Engagement Metrics</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                product_pages = st.number_input("Product Pages Visited", 0, 300, step=1, key="product_pages")
                product_duration = st.number_input("Time on Product Pages (sec)", 0.0, 5000.0, step=10.0, key="product_duration")
                admin_pages = st.number_input("Account / Admin Pages", 0, 50, step=1, key="admin_pages")
            with c2:
                page_values = st.slider("Page Values", 0.0, 100.0, step=0.5, key="page_values")
                bounce_rate = st.slider("Bounce Rate", 0.0, 0.20, step=0.005, format="%.3f", key="bounce_rate")
                exit_rate = st.slider("Exit Rate", 0.0, 0.20, step=0.005, format="%.3f", key="exit_rate")

        with st.container(border=True):
            st.markdown('<div class="card-header">🗓️ Session Context</div>', unsafe_allow_html=True)
            s1, s2, s3 = st.columns([1, 1.3, 0.9])
            with s1:
                month = st.selectbox("Month", MONTHS, key="month")
            with s2:
                visitor_type = st.selectbox("Visitor Type", VISITOR_TYPES, key="visitor_type")
            with s3:
                st.write("")
                st.write("")
                is_weekend = st.checkbox("Weekend Visit", key="is_weekend")

        predict_clicked = st.button("🚀 Predict Purchase Intention", type="primary", use_container_width=True)

    with right_col:
        if predict_clicked:
            with st.status("Running ML inference pipeline...", expanded=True) as status:
                st.write("Encoding session features...")
                time.sleep(0.2)
                input_df = pd.DataFrame(0.0, index=[0], columns=feature_cols)
                input_df.at[0, "ProductRelated"] = product_pages
                input_df.at[0, "ProductRelated_Duration"] = product_duration
                input_df.at[0, "Administrative"] = admin_pages
                input_df.at[0, "Administrative_Duration"] = admin_pages * 25.0
                input_df.at[0, "PageValues"] = page_values
                input_df.at[0, "BounceRates"] = bounce_rate
                input_df.at[0, "ExitRates"] = exit_rate
                input_df.at[0, "Weekend"] = 1 if is_weekend else 0

                for col, val in [("OperatingSystems", 2), ("Browser", 2), ("Region", 1), ("TrafficType", 2)]:
                    if col in input_df.columns:
                        input_df.at[0, col] = val
                if f"Month_{month}" in input_df.columns:
                    input_df.at[0, f"Month_{month}"] = 1
                if f"VisitorType_{visitor_type}" in input_df.columns:
                    input_df.at[0, f"VisitorType_{visitor_type}"] = 1

                st.write("Scaling with StandardScaler...")
                time.sleep(0.2)
                input_scaled = scaler.transform(input_df)

                st.write(f"Predicting with {type(model).__name__}...")
                time.sleep(0.2)
                prediction = int(model.predict(input_scaled)[0])
                prob = float(model.predict_proba(input_scaled)[0][1]) if hasattr(model, "predict_proba") else float(prediction)
                status.update(label="Prediction complete!", state="complete", expanded=False)

            pct = prob * 100
            arc_len = 283.0
            target_offset = arc_len * (1.0 - prob)

            if prediction == 1:
                card_class, stroke_color = "result-buy", "#34d399"
                verdict_title = "HIGH INTENT: WILL PURCHASE"
                verdict_sub = "Strong conversion signals detected for this shopper session."
                badge_svg = '<svg width="50" height="50" viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="rgba(52,211,153,0.18)" stroke="#34d399" stroke-width="2"/><path d="M18 33 l9 9 l19 -20" fill="none" stroke="#34d399" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
                st.balloons()
                st.toast("High Purchase Intent Detected!", icon="🛒")
            else:
                card_class, stroke_color = "result-nobuy", "#fbbf24"
                verdict_title = "LOW INTENT: WILL NOT PURCHASE"
                verdict_sub = "Window-shopping behaviour detected. Consider showing a quick exit offer."
                badge_svg = '<svg width="50" height="50" viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="rgba(251,191,36,0.16)" stroke="#fbbf24" stroke-width="2"/><circle cx="32" cy="32" r="10" fill="none" stroke="#fbbf24" stroke-width="3.5"/><line x1="39" y1="39" x2="47" y2="47" stroke="#fbbf24" stroke-width="4" stroke-linecap="round"/></svg>'
                st.toast("Low Purchase Intent Detected", icon="👀")

            pv_score = min(100, int((page_values / 50.0) * 100))
            eng_score = min(100, int((product_duration / 1200.0) * 100))
            retention_score = max(0, min(100, int((1.0 - (bounce_rate + exit_rate) / 0.40) * 100)))

            st.markdown(f"""
<style>
@keyframes sweepGauge {{ from {{ stroke-dashoffset: {arc_len}; }} to {{ stroke-dashoffset: {target_offset:.1f}; }} }}
.gauge-arc {{ stroke-dasharray: {arc_len}; stroke-dashoffset: {target_offset:.1f}; animation: sweepGauge 1.1s cubic-bezier(0.22, 1, 0.36, 1) forwards; }}
</style>
<div class="result-card {card_class}">
{badge_svg}<br/>
<svg viewBox="0 0 220 130" width="220" height="130">
<path d="M 20 110 A 90 90 0 0 1 200 110" fill="none" stroke="rgba(148,163,184,0.22)" stroke-width="16" stroke-linecap="round"/>
<path class="gauge-arc" d="M 20 110 A 90 90 0 0 1 200 110" fill="none" stroke="{stroke_color}" stroke-width="16" stroke-linecap="round"/>
<text x="110" y="92" text-anchor="middle" fill="#f8fafc" font-size="30" font-weight="800">{pct:.1f}%</text>
<text x="110" y="114" text-anchor="middle" fill="#94a3b8" font-size="11" letter-spacing="1">PURCHASE PROBABILITY</text>
</svg>
<h3 style="color:{stroke_color}; margin: 4px 0; font-weight: 800;">{verdict_title}</h3>
<p style="color:#cbd5e1; font-size:0.9rem; margin-bottom: 14px;">{verdict_sub}</p>
<div class="signal-row"><div class="signal-label"><span>Page Value Strength</span><span>{pv_score}%</span></div><div class="signal-track"><div class="signal-fill" style="width:{pv_score}%; background:linear-gradient(90deg,#38bdf8,#818cf8);"></div></div></div>
<div class="signal-row"><div class="signal-label"><span>Product Engagement Depth</span><span>{eng_score}%</span></div><div class="signal-track"><div class="signal-fill" style="width:{eng_score}%; background:linear-gradient(90deg,#34d399,#0ea5e9);"></div></div></div>
<div class="signal-row"><div class="signal-label"><span>Session Retention Health</span><span>{retention_score}%</span></div><div class="signal-track"><div class="signal-fill" style="width:{retention_score}%; background:linear-gradient(90deg,#a78bfa,#34d399);"></div></div></div>
</div>
""", unsafe_allow_html=True)
        else:
            with st.container(border=True):
                st.markdown("""
<div style="text-align:center; padding: 48px 20px;">
<svg width="92" height="92" viewBox="0 0 100 100" style="margin-bottom:10px; animation: floatSlow 3s ease-in-out infinite;">
<circle cx="50" cy="50" r="44" fill="rgba(99,102,241,0.14)" stroke="#818cf8" stroke-width="2" stroke-dasharray="6 4"/>
<path d="M28 58 A22 22 0 0 1 72 58" fill="none" stroke="#38bdf8" stroke-width="5" stroke-linecap="round"/>
<line x1="50" y1="58" x2="64" y2="41" stroke="#34d399" stroke-width="4" stroke-linecap="round"/>
<circle cx="50" cy="58" r="5" fill="#f8fafc"/>
</svg>
<h3 style="color:#e2e8f0; margin-bottom:8px;">Ready to Predict</h3>
<p style="color:#94a3b8; font-size:0.93rem;">Pick a quick preset in the sidebar or adjust the session inputs, then hit <b>Predict Purchase Intention</b>.</p>
</div>
""", unsafe_allow_html=True)

with tab_visuals:
    st.markdown("### 🔄 End-to-End ML Workflow")
    st.markdown("""
<svg viewBox="0 0 920 105" width="100%" style="height:auto; margin-bottom:18px;">
<rect x="8" y="18" width="150" height="66" rx="14" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
<text x="83" y="46" text-anchor="middle" fill="#38bdf8" font-size="13" font-weight="700">1. UCI Dataset</text>
<text x="83" y="66" text-anchor="middle" fill="#cbd5e1" font-size="11">12,330 Sessions</text>
<path d="M162 51 L192 51" stroke="#64748b" stroke-width="2.5"/>
<rect x="196" y="18" width="156" height="66" rx="14" fill="#1e293b" stroke="#818cf8" stroke-width="1.5"/>
<text x="274" y="46" text-anchor="middle" fill="#818cf8" font-size="13" font-weight="700">2. Preprocessing</text>
<text x="274" y="66" text-anchor="middle" fill="#cbd5e1" font-size="11">IQR • OHE • Scaling</text>
<path d="M356 51 L386 51" stroke="#64748b" stroke-width="2.5"/>
<rect x="390" y="18" width="156" height="66" rx="14" fill="#1e293b" stroke="#a78bfa" stroke-width="1.5"/>
<text x="468" y="46" text-anchor="middle" fill="#a78bfa" font-size="13" font-weight="700">3. 4 ML Models</text>
<text x="468" y="66" text-anchor="middle" fill="#cbd5e1" font-size="11">87% – 92% Accuracy</text>
<path d="M550 51 L580 51" stroke="#64748b" stroke-width="2.5"/>
<rect x="584" y="18" width="150" height="66" rx="14" fill="#1e293b" stroke="#34d399" stroke-width="1.5"/>
<text x="659" y="46" text-anchor="middle" fill="#34d399" font-size="13" font-weight="700">4. Best Model</text>
<text x="659" y="66" text-anchor="middle" fill="#cbd5e1" font-size="11">Pickled Pipeline</text>
<path d="M738 51 L768 51" stroke="#64748b" stroke-width="2.5"/>
<rect x="772" y="18" width="140" height="66" rx="14" fill="#1e293b" stroke="#fbbf24" stroke-width="1.5"/>
<text x="842" y="46" text-anchor="middle" fill="#fbbf24" font-size="13" font-weight="700">5. Live App</text>
<text x="842" y="66" text-anchor="middle" fill="#cbd5e1" font-size="11">Streamlit Cloud</text>
</svg>
""", unsafe_allow_html=True)

    st.markdown("### 📈 Model Charts & Screenshots")
    gallery = [
        ("model_comparison.png", "Step 6: Classification Model Accuracy Comparison"),
        ("confusion_matrix.png", "Step 7: Winning Model Confusion Matrix"),
        ("eda_chart.png", "Step 3: Exploratory Data Analysis (EDA)")
    ]
    found = [(f, cap) for f, cap in gallery if os.path.exists(f)]
    if found:
        cols = st.columns(min(2, len(found)), gap="medium")
        for idx, (img_file, caption) in enumerate(found):
            with cols[idx % len(cols)]:
                with st.container(border=True):
                    st.image(img_file, caption=caption, use_container_width=True)
    else:
        st.info("Upload `model_comparison.png`, `confusion_matrix.png`, or `eda_chart.png` to your GitHub repo root to display your Colab charts here automatically.")

# --- END OF APP.PY ---
