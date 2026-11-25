import os
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

# 2. Initialize Cover / Navigation State
if "entered_app" not in st.session_state:
    st.session_state.entered_app = False

# 3. Global Animated CSS Theme
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 18% 12%, #172554 0%, #0b1120 48%, #050811 100%);
}

@keyframes fadeSlideDown {
    0% { opacity: 0; transform: translateY(-20px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes fadeSlideUp {
    0% { opacity: 0; transform: translateY(24px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes floatSlow {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 22px rgba(56, 189, 248, 0.35); }
    50% { box-shadow: 0 0 38px rgba(99, 102, 241, 0.7); }
}

@keyframes barGrow {
    from { width: 0%; }
}

/* Front Cover Container */
.cover-wrapper {
    background: linear-gradient(145deg, rgba(30, 41, 59, 0.72), rgba(15, 23, 42, 0.92));
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 26px;
    padding: 36px 32px 28px 32px;
    margin: 10px auto 22px auto;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.55);
    text-align: center;
    animation: fadeSlideDown 0.75s ease-out;
}

.cover-pill {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1px;
    color: #93c5fd;
    background: rgba(59, 130, 246, 0.16);
    border: 1px solid rgba(96, 165, 250, 0.4);
    margin-bottom: 14px;
    animation: floatSlow 3.2s ease-in-out infinite;
}

.cover-title {
    font-size: 2.75rem;
    font-weight: 900;
    line-height: 1.15;
    margin: 0 0 12px 0;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399, #38bdf8);
    background-size: 250% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 5.5s linear infinite;
}

.cover-subtitle {
    color: #cbd5e1;
    font-size: 1.06rem;
    max-width: 720px;
    margin: 0 auto 24px auto;
    line-height: 1.55;
}

/* Visual Feature Cards on Cover */
.feature-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 18px;
    padding: 20px 18px;
    text-align: center;
    height: 100%;
    transition: transform 0.25s ease, border-color 0.25s ease;
    animation: fadeSlideUp 0.85s ease-out;
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: rgba(56, 189, 248, 0.55);
}

.feature-title {
    color: #f8fafc;
    font-size: 1.02rem;
    font-weight: 700;
    margin: 10px 0 6px 0;
}

.feature-desc {
    color: #94a3b8;
    font-size: 0.88rem;
    margin: 0;
}

/* Dashboard Hero Banner */
.hero-box {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.78), rgba(15, 23, 42, 0.92));
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 18px;
    padding: 20px 26px;
    margin-bottom: 18px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    animation: fadeSlideDown 0.6s ease-out;
}

.hero-title {
    font-size: 1.95rem;
    font-weight: 800;
    margin: 0 0 4px 0;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399, #38bdf8);
    background-size: 250% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 6s linear infinite;
}

.hero-sub {
    color: #94a3b8;
    font-size: 0.94rem;
    margin: 0;
}

.card-header {
    font-size: 1.02rem;
    font-weight: 700;
    color: #e2e8f0;
    padding-bottom: 8px;
    margin-bottom: 12px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}

/* Primary Glowing Buttons */
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #4f46e5, #0ea5e9);
    border: none;
    border-radius: 14px;
    padding: 0.82rem 1.4rem;
    font-size: 1.08rem;
    font-weight: 800;
    letter-spacing: 0.4px;
    color: #ffffff;
    animation: pulseGlow 2.8s infinite;
    transition: all 0.25s ease;
}

div.stButton > button[kind="primary"]:hover {
    transform: translateY(-3px) scale(1.015);
}

/* Result Cards */
.result-card {
    border-radius: 18px;
    padding: 22px;
    margin-top: 8px;
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

.signal-row {
    margin: 12px 0;
    text-align: left;
}

.signal-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.87rem;
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

# ---------------------------------------------------------
# VIEW 1: CLICK-TO-OPEN FRONT COVER PAGE
# ---------------------------------------------------------
if not st.session_state.entered_app:
    # Hide sidebar on the front cover for a true landing-page feel
    st.markdown("""
<style>
section[data-testid="stSidebar"] { display: none; }
button[data-testid="collapsedControl"] { display: none; }
</style>
""", unsafe_allow_html=True)

    # Built-in animated E-Commerce AI Cover Artwork (used automatically unless you upload cover.png)
    cover_svg = """
<svg viewBox="0 0 760 220" width="100%" style="max-width:740px; height:auto; margin: 4px auto 16px auto; display:block;">
<defs>
<linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#1e293b" stop-opacity="0.9"/>
<stop offset="100%" stop-color="#0f172a" stop-opacity="0.95"/>
</linearGradient>
<linearGradient id="accent1" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#38bdf8"/>
<stop offset="100%" stop-color="#818cf8"/>
</linearGradient>
<linearGradient id="accent2" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#34d399"/>
<stop offset="100%" stop-color="#0ea5e9"/>
</linearGradient>
</defs>
<rect x="8" y="8" width="744" height="204" rx="22" fill="url(#bgGrad)" stroke="rgba(99,102,241,0.45)" stroke-width="1.5"/>
<circle cx="135" cy="110" r="66" fill="rgba(56,189,248,0.1)" stroke="rgba(56,189,248,0.35)" stroke-width="1.5"/>
<circle cx="135" cy="110" r="46" fill="rgba(99,102,241,0.15)"/>
<path d="M105 90 h12 l10 42 h42 l10-28 h-46" fill="none" stroke="url(#accent1)" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="132" cy="146" r="6" fill="#34d399"/>
<circle cx="164" cy="146" r="6" fill="#34d399"/>
<path d="M220 110 C265 110, 265 65, 315 65" fill="none" stroke="#38bdf8" stroke-width="2.2" stroke-dasharray="6 5"/>
<path d="M220 110 L315 110" fill="none" stroke="#818cf8" stroke-width="2.2" stroke-dasharray="6 5"/>
<path d="M220 110 C265 110, 265 155, 315 155" fill="none" stroke="#34d399" stroke-width="2.2" stroke-dasharray="6 5"/>
<circle cx="320" cy="65" r="11" fill="#0ea5e9" stroke="#e0f2fe" stroke-width="2"/>
<circle cx="320" cy="110" r="11" fill="#6366f1" stroke="#e0e7ff" stroke-width="2"/>
<circle cx="320" cy="155" r="11" fill="#10b981" stroke="#d1fae5" stroke-width="2"/>
<line x1="332" y1="65" x2="415" y2="90" stroke="rgba(148,163,184,0.45)" stroke-width="2"/>
<line x1="332" y1="110" x2="415" y2="90" stroke="rgba(148,163,184,0.45)" stroke-width="2"/>
<line x1="332" y1="110" x2="415" y2="132" stroke="rgba(148,163,184,0.45)" stroke-width="2"/>
<line x1="332" y1="155" x2="415" y2="132" stroke="rgba(148,163,184,0.45)" stroke-width="2"/>
<circle cx="425" cy="90" r="13" fill="#818cf8" stroke="#ffffff" stroke-width="2"/>
<circle cx="425" cy="132" r="13" fill="#34d399" stroke="#ffffff" stroke-width="2"/>
<rect x="485" y="42" width="235" height="136" rx="16" fill="rgba(15,23,42,0.85)" stroke="rgba(52,211,153,0.45)" stroke-width="1.5"/>
<text x="505" y="70" fill="#94a3b8" font-size="11" font-weight="700" letter-spacing="1">CONVERSION FORECAST</text>
<rect x="510" y="122" width="22" height="36" rx="5" fill="#38bdf8" opacity="0.65"/>
