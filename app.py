import time
import pickle
import pandas as pd
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Shopper Intent AI",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Animations & Modern Dark Glass Theme
st.markdown("""
<style>
/* Animated dark radial background */
.stApp {
    background: radial-gradient(circle at 15% 15%, #162238 0%, #0b0f19 55%, #070a12 100%);
}

/* Smooth entrance animations */
@keyframes fadeSlideDown {
    0% { opacity: 0; transform: translateY(-18px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes fadeSlideUp {
    0% { opacity: 0; transform: translateY(22px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes floatBadge {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes barGrow {
    from { width: 0%; }
}

/* Hero Banner */
.hero-box {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.78), rgba(15, 23, 42, 0.9));
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 18px;
    padding: 24px 28px;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    animation: fadeSlideDown 0.7s ease-out;
}

.hero-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.6px;
    color: #a5b4fc;
    background: rgba(99, 102, 241, 0.16);
    border: 1px solid rgba(99, 102, 241, 0.4);
    margin-bottom: 10px;
    animation: floatBadge 3s ease-in-out infinite;
}

.hero-title {
    font-size: 2.15rem;
    font-weight: 800;
    margin: 0 0 6px 0;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399, #38bdf8);
    background-size: 250% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 6s linear infinite;
}

.hero-sub {
    color: #94a3b8;
    font-size: 0.98rem;
    margin: 0;
}

/* Section Card Headers */
.card-header {
    font-size: 1.05rem;
    font-weight: 700;
    color: #e2e8f0;
    padding-bottom: 8px;
    margin-bottom: 12px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}

/* Glowing Primary Button */
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #4f46e5, #0ea5e9);
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1.2rem;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.4px;
    color: #ffffff;
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.45);
    transition: all 0.25s ease;
}

div.stButton > button[kind="primary"]:hover {
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 10px 28px rgba(14, 165, 233, 0.6);
}

/* Animated Result Card */
.result-card {
    border-radius: 18px;
    padding: 24px;
    margin-top: 12px;
    text-align: center;
    animation: fadeSlideUp 0.55s cubic-bezier(0.16, 1, 0.3, 1);
}

.result-buy {
    background: linear-gradient(145deg, rgba(16, 185, 129, 0.16), rgba(6, 78, 59, 0.28));
    border: 1.5px solid rgba(52, 211, 153, 0.55);
    box-shadow: 0 0 28px rgba(16, 185, 129, 0.22);
}

.result-nobuy {
    background: linear-gradient(145deg, rgba(245, 158, 11, 0.14), rgba(120, 53, 15, 0.26));
    border: 1.5px solid rgba(251, 191, 36, 0.5);
    box-shadow: 0 0 28px rgba(245, 158, 11, 0.18);
}

/* Animated Signal Bars */
.signal-row {
    margin: 12px 0;
    text-align: left;
}

.signal-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.88rem;
    color: #cbd5e1;
    margin-bottom: 5px;
}

.signal-track {
    width: 100%;
    height: 9px;
    background: rgba(148, 163, 184, 0.16);
    border-radius: 999px;
    overflow: hidden;
}

.signal-fill {
    height: 100%;
    border-radius: 999px;
    animation: barGrow 1s ease-out;
}
</style>
""", unsafe_allow_html=True)

# 3. Load Saved Model Artifacts
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

# 4. Session State Initialization & Viva Demo Presets
MONTHS = ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
VISITOR_TYPES = ["Returning_Visitor", "New_Visitor", "Other"]

PRESETS = {
    "high": {
        "product_pages": 25,
        "product_duration": 950.0,
        "admin_pages": 4,
        "page_values": 35.0,
        "bounce_rate": 0.005,
        "exit_rate": 0.015,
        "month": "Nov",
        "visitor_type": "Returning_Visitor",
        "is_weekend": True,
    },
    "low": {
        "product_pages": 2,
        "product_duration": 25.0,
        "admin_pages": 0,
        "page_values": 0.0,
        "bounce_rate": 0.150,
        "exit_rate": 0.200,
        "month": "May",
        "visitor_type": "Returning_Visitor",
        "is_weekend": False,
    },
    "mid": {
        "product_pages": 12,
        "product_duration": 380.0,
        "admin_pages": 1,
        "page_values": 8.0,
        "bounce_rate": 0.030,
        "exit_rate": 0.050,
        "month": "Oct",
        "visitor_type": "New_Visitor",
        "is_weekend": True,
    },
}

for k, v in PRESETS["high"].items():
    if k not in st.session_state:
        st.session_state[k] = v

def apply_preset(preset_key):
    for k, v in PRESETS[preset_key].items():
        st.session_state[k] = v

# 5. Sidebar: Viva Quick-Test Controls
with st.sidebar:
    st.markdown("### ⚡ Quick Demo Presets")
    st.caption("Load realistic shopper profiles in one click during your presentation.")
    st.button("🟢 High-Intent Festive Buyer", use_container_width=True, on_click=apply_preset, args=("high",))
    st.button("🟡 Borderline New Visitor", use_container_width=True, on_click=apply_preset, args=("mid",))
    st.button("🔴 Casual Window Shopper", use_container_width=True, on_click=apply_preset, args=("low",))
    st.divider()
    st.markdown("### 🧠 Model Pipeline")
    st.markdown(
        f"**Algorithm:** `{type(model).__name__}`  \n"
        f"**Features:** `{len(feature_cols)} encoded columns`  \n"
        f"**Scaler:** `StandardScaler`"
    )

# 6. Animated Hero Banner
st.markdown("""
<div class="hero-box">
<div class="hero-badge">LIVE ML PREDICTION ENGINE</div>
<div class="hero-title">🛒 Online Shoppers Purchasing Intention</div>
<p class="hero-sub">Adjust real-time e-commerce session metrics below or pick a sidebar preset to predict conversion probability.</p>
</div>
""", unsafe_allow_html=True)

# 7. Main Layout: Inputs on Left, Live Prediction & Gauge on Right
left_col, right_col = st.columns([1.25, 1], gap="large")

with left_col:
    with st.container(border=True):
        st.markdown('<div class="card-header">📊 Browsing & Engagement Metrics</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            product_pages = st.number_input("Product Pages Visited", min_value=0, max_value=300, step=1, key="product_pages")
            product_duration = st.number_input("Time on Product Pages (sec)", min_value=0.0, max_value=5000.0, step=10.0, key="product_duration")
            admin_pages = st.number_input("Account / Admin Pages", min_value=0, max_value=50, step=1, key="admin_pages")
        with c2:
            page_values = st.slider("Page Values", min_value=0.0, max_value=100.0, step=0.5, key="page_values")
            bounce_rate = st.slider("Bounce Rate", min_value=0.0, max_value=0.20, step=0.005, format="%.3f", key="bounce_rate")
            exit_rate = st.slider("Exit Rate", min_value=0.0, max_value=0.20, step=0.005, format="%.3f", key="exit_rate")

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
        # Step-by-step animated pipeline status
        with st.status("Running ML inference pipeline...", expanded=True) as status:
            st.write("Encoding session features...")
            time.sleep(0.25)

            input_df = pd.DataFrame(0.0, index=[0], columns=feature_cols)
            input_df.at[0, "ProductRelated"] = product_pages
            input_df.at[0, "ProductRelated_Duration"] = product_duration
            input_df.at[0, "Administrative"] = admin_pages
            input_df.at[0, "Administrative_Duration"] = admin_pages * 25.0
            input_df.at[0, "PageValues"] = page_values
            input_df.at[0, "BounceRates"] = bounce_rate
            input_df.at[0, "ExitRates"] = exit_rate
            input_df.at[0, "Weekend"] = 1 if is_weekend else 0

            for col, default_val in [("OperatingSystems", 2), ("Browser", 2), ("Region", 1), ("TrafficType", 2)]:
                if col in input_df.columns:
                    input_df.at[0, col] = default_val

            month_col = f"Month_{month}"
            if month_col in input_df.columns:
                input_df.at[0, month_col] = 1

            visitor_col = f"VisitorType_{visitor_type}"
            if visitor_col in input_df.columns:
                input_df.at[0, visitor_col] = 1

            st.write("Applying StandardScaler...")
            time.sleep(0.25)
            input_scaled = scaler.transform(input_df)

            st.write(f"Predicting with {type(model).__name__}...")
            time.sleep(0.25)
            prediction = int(model.predict(input_scaled)[0])
            prob = float(model.predict_proba(input_scaled)[0][1]) if hasattr(model, "predict_proba") else float(prediction)

            status.update(label="Prediction complete!", state="complete", expanded=False)

        # Animated SVG Speedometer Gauge calculations
        pct = prob * 100
        arc_len = 283.0
        target_offset = arc_len * (1.0 - prob)

        if prediction == 1:
            card_class = "result-buy"
            stroke_color = "#34d399"
            verdict_title = "HIGH INTENT: WILL PURCHASE"
            verdict_sub = "Strong conversion signals detected for this session."
            st.balloons()
            st.toast("High Purchase Intent Detected!", icon="🛒")
        else:
            card_class = "result-nobuy"
            stroke_color = "#fbbf24"
            verdict_title = "LOW INTENT: WILL NOT PURCHASE"
            verdict_sub = "Visitor shows window-shopping behaviour. Consider triggering an exit discount."
            st.toast("Low Purchase Intent Detected", icon="👀")

        # Visual signal scores (0-100%)
        pv_score = min(100, int((page_values / 50.0) * 100))
        eng_score = min(100, int((product_duration / 1200.0) * 100))
        retention_score = max(0, min(100, int((1.0 - (bounce_rate + exit_rate) / 0.40) * 100)))

        st.markdown(f"""
<style>
@keyframes sweepGauge {{
    from {{ stroke-dashoffset: {arc_len}; }}
    to {{ stroke-dashoffset: {target_offset:.1f}; }}
}}
.gauge-arc {{
    stroke-dasharray: {arc_len};
    stroke-dashoffset: {target_offset:.1f};
    animation: sweepGauge 1.1s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}}
</style>
<div class="result-card {card_class}">
<svg viewBox="0 0 220 130" width="220" height="130">
<path d="M 20 110 A 90 90 0 0 1 200 110" fill="none" stroke="rgba(148,163,184,0.22)" stroke-width="16" stroke-linecap="round"/>
<path class="gauge-arc" d="M 20 110 A 90 90 0 0 1 200 110" fill="none" stroke="{stroke_color}" stroke-width="16" stroke-linecap="round"/>
<text x="110" y="92" text-anchor="middle" fill="#f8fafc" font-size="30" font-weight="800">{pct:.1f}%</text>
<text x="110" y="114" text-anchor="middle" fill="#94a3b8" font-size="11" letter-spacing="1">PURCHASE PROBABILITY</text>
</svg>
<h3 style="color:{stroke_color}; margin: 6px 0 4px 0; font-weight: 800;">{verdict_title}</h3>
<p style="color:#cbd5e1; font-size:0.9rem; margin-bottom: 18px;">{verdict_sub}</p>

<div class="signal-row">
<div class="signal-label"><span>Page Value Strength</span><span>{pv_score}%</span></div>
<div class="signal-track"><div class="signal-fill" style="width:{pv_score}%; background:linear-gradient(90deg,#38bdf8,#818cf8);"></div></div>
</div>

<div class="signal-row">
<div class="signal-label"><span>Product Engagement Depth</span><span>{eng_score}%</span></div>
<div class="signal-track"><div class="signal-fill" style="width:{eng_score}%; background:linear-gradient(90deg,#34d399,#0ea5e9);"></div></div>
</div>

<div class="signal-row">
<div class="signal-label"><span>Session Retention Health</span><span>{retention_score}%</span></div>
<div class="signal-track"><div class="signal-fill" style="width:{retention_score}%; background:linear-gradient(90deg,#a78bfa,#34d399);"></div></div>
</div>
</div>
""", unsafe_allow_html=True)
    else:
        with st.container(border=True):
            st.markdown("""
<div style="text-align:center; padding: 55px 20px;">
<div style="font-size: 3rem; margin-bottom: 10px; animation: floatBadge 2.8s ease-in-out infinite;">🎯</div>
<h3 style="color:#e2e8f0; margin-bottom:8px;">Ready to Predict</h3>
<p style="color:#94a3b8; font-size:0.94rem;">
Choose a preset from the left sidebar or tweak the sliders, then hit <b>Predict Purchase Intention</b> to see the animated probability dial and session signals.
</p>
</div>
""", unsafe_allow_html=True)
