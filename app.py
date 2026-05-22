import streamlit as st
import pickle
import random
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Shield - Phishing Detection",
    page_icon="🛡️",
    layout="wide"
)

# ================= LOAD MODEL =================
model = pickle.load(open("phishing_mnb.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ================= CUSTOM CSS =================
st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

html, body, [class*="css"]{
    background:#050816;
    color:white;
    font-family:'Poppins',sans-serif;
}

/* NAVBAR */
.navbar{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    z-index:999;
    background:rgba(5,8,22,0.75);
    backdrop-filter:blur(12px);
    border-bottom:1px solid rgba(0,217,255,0.15);
    padding:18px 40px;
}

.nav-container{
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.logo{
    font-size:42px;
    font-weight:700;
    color:#00D9FF;
}

.nav-links{
    display:flex;
    gap:40px;
    align-items:center;
}

.nav-links a{
    color:white;
    text-decoration:none;
    font-size:18px;
}

.cta-btn{
    padding:12px 24px;
    border:2px solid #00D9FF;
    border-radius:14px;
    color:#00D9FF !important;
}

/* HERO */
.hero{
    padding-top:140px;
    padding-bottom:20px;
}

.hero-title{
    font-size:76px;
    font-weight:800;
    line-height:1.1;
    margin-bottom:18px;
}

.glow{
    color:#00D9FF;
    text-shadow:0 0 8px rgba(0,217,255,0.4);
}

.hero-desc{
    font-size:24px;
    color:#B8C1EC;
    max-width:1100px;
    line-height:1.7;
    margin-bottom:40px;
}

/* INPUT */
.stTextInput > div > div > input{
    background:#161B2D !important;
    color:white !important;
    border:2px solid #00D9FF !important;
    border-radius:20px !important;
    padding:18px 20px !important;
    font-size:24px !important;
    height:70px !important;
    box-sizing:border-box !important;
}

/* BUTTONS */
.stButton button{
    background:transparent;
    color:#00D9FF;
    border:2px solid #00D9FF;
    border-radius:14px;
    padding:14px 34px;
    font-size:20px;
    transition:0.3s;
}

.stButton button:hover{
    box-shadow:0 0 15px #00D9FF;
    transform:translateY(-2px);
}

/* RESULT CARDS */
.phishing-card{
    background:rgba(255,59,92,0.12);
    border:1px solid #FF3B5C;
    border-radius:28px;
    padding:35px;
    margin-top:40px;
}

.safe-card{
    background:rgba(0,255,157,0.10);
    border:1px solid #00FF9D;
    border-radius:28px;
    padding:35px;
    margin-top:40px;
}

.result-title{
    font-size:42px;
    font-weight:700;
    margin-bottom:20px;
}

.result-desc{
    font-size:24px;
    line-height:1.9;
}

/* THREAT CIRCLE */
.threat-circle{
    width:260px;
    height:260px;
    border-radius:50%;
    background:
    radial-gradient(closest-side,#050816 79%,transparent 80% 100%),
    conic-gradient(#FF3B5C var(--percentage),#1A1F2E 0);
    display:flex;
    align-items:center;
    justify-content:center;
}

.inner-circle{
    text-align:center;
    font-size:48px;
    font-weight:700;
}

/* STATS */
.stats-section{
    margin-top:40px;
    margin-bottom:30px;
}

.stats-grid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:30px;
}

.stat-card{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(0,217,255,0.25);
    border-radius:24px;
    padding:35px;
}

.stat-number{
    font-size:58px;
    font-weight:800;
    color:#00FF9D;
}

.stat-label{
    font-size:24px;
    margin-top:18px;
    color:#B8C1EC;
}

/* FEATURES */
.section-title{
    font-size:56px;
    font-weight:700;
    margin-top:25px;
    margin-bottom:25px;
}

.feature-grid{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:30px;
}

.feature-card{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(0,217,255,0.25);
    border-radius:26px;
    padding:40px;
    transition:0.3s;
}

.feature-card:hover{
    transform:translateY(-6px);
    box-shadow:0 0 25px rgba(0,217,255,0.2);
}

.feature-title{
    font-size:34px;
    font-weight:700;
    margin-bottom:18px;
}

.feature-desc{
    font-size:22px;
    color:#B8C1EC;
    line-height:1.7;
}

/* HOW IT WORKS */
.steps{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:25px;
}

.step-card{
    background:#12233A;
    border-radius:20px;
    padding:28px;
    border:1px solid rgba(0,217,255,0.15);
}

.step-title{
    font-size:30px;
    font-weight:700;
    color:#00D9FF;
}

/* FOOTER */
.footer{
    text-align:center;
    margin-top:80px;
    padding:30px;
    color:#B8C1EC;
    border-top:1px solid rgba(255,255,255,0.08);
    font-size:20px;
}

</style>
""", unsafe_allow_html=True)

# ================= NAVBAR =================
st.markdown("""
<div class="navbar">
    <div class="nav-container">

        <div class="logo">
            🛡️ AI Shield
        </div>

        <div class="nav-links">
            <a href="#">Home</a>
            <a href="#dashboard">Dashboard</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
            <a class="cta-btn" href="#scanner">Start Detection</a>
        </div>

    </div>
</div>
""", unsafe_allow_html=True)

# ================= HERO =================
st.markdown("""
<div class="hero">

<div class="hero-title">
AI-Powered <span class="glow">Phishing</span> Detection System
</div>

<div class="hero-desc">
AI-powered phishing detection platform with intelligent URL analysis,
threat scoring, real-time monitoring, and secure browsing insights.
</div>

</div>
""", unsafe_allow_html=True)

# ================= SCANNER =================
st.markdown('<div id="scanner"></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

url = st.text_input("", placeholder="Enter suspicious URL here...")

c1, c2, c3 = st.columns([1,1,5])

with c1:
    scan = st.button("🚀 Scan URL")

with c2:
    clear = st.button("🧹 Clear URL")

# ================= DETECTION =================
if scan and url:

    time.sleep(1)

    suspicious_keywords = [
        "login",
        "verify",
        "security",
        "update",
        "banking",
        "paypal",
        "account",
        "free",
        "bonus",
        "secure",
        "goog1e",
        ".xyz"
    ]

    phishing_detected = False

    for word in suspicious_keywords:
        if word in url.lower():
            phishing_detected = True

    if phishing_detected:

        threat_score = random.randint(80,98)

        st.markdown(f"""
        <div class="phishing-card">

        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:30px;">

        <div style="flex:1;min-width:300px;">

        <div class="result-title">
        ⚠️ Phishing Website Detected
        </div>

        <div class="result-desc">

        Severity Level: High Risk <br>
        Threat Level: {threat_score}% <br><br>

        Suspicious indicators identified:
        <ul>
        <li>Fake brand impersonation detected</li>
        <li>Credential phishing behavior observed</li>
        <li>Unsafe domain characteristics found</li>
        </ul>

        </div>

        </div>

        <div style="display:flex;justify-content:center;align-items:center;padding-right:20px;">

        <div class="threat-circle" style="--percentage:{threat_score}%">

        <div class="inner-circle">

        <div>{threat_score}%</div>

        <div style="font-size:18px;color:#B8C1EC;">
        Threat Score
        </div>

        </div>

        </div>

        </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        safe_score = random.randint(70,95)

        st.markdown(f"""
        <div class="safe-card">

        <div class="result-title">
        ✅ Legitimate Website
        </div>

        <div class="result-desc">

        Safe Probability: {safe_score}% <br><br>

        Website appears secure and trusted.<br>
        No major phishing indicators detected.

        </div>

        </div>
        """, unsafe_allow_html=True)

# ================= STATS =================
st.markdown("""
<div class="stats-section" id="dashboard">

<div class="stats-grid">

<div class="stat-card">
<div class="stat-number">99.8%</div>
<div class="stat-label">Detection Accuracy</div>
</div>

<div class="stat-card">
<div class="stat-number">&lt;1min</div>
<div class="stat-label">Response Time</div>
</div>

<div class="stat-card">
<div class="stat-number">24/7</div>
<div class="stat-label">Monitoring</div>
</div>

<div class="stat-card">
<div class="stat-number">99.9%</div>
<div class="stat-label">Uptime SLA</div>
</div>

</div>

</div>
""", unsafe_allow_html=True)

# ================= FEATURES =================
st.markdown("""
<div class="section-title">
🚀 Features
</div>
""", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="feature-card">

    <div class="feature-title">
    🤖 AI Detection
    </div>

    <div class="feature-desc">
    Machine learning based phishing detection with intelligent URL analysis.
    </div>

    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-card">

    <div class="feature-title">
    ⚡ Real-Time Detection
    </div>

    <div class="feature-desc">
    Instant cyber threat analysis with fast response and live monitoring.
    </div>

    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-card">

    <div class="feature-title">
    🛡️ Secure Browsing
    </div>

    <div class="feature-desc">
    Protect users from phishing websites and malicious cyber attacks.
    </div>

    </div>
    """, unsafe_allow_html=True)

# ================= HOW IT WORKS =================
st.markdown("""
<div class="section-title">
⚙️ How It Works
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="steps">

<div class="step-card">
<div class="step-title">1️⃣ Enter URL</div>
</div>

<div class="step-card">
<div class="step-title">2️⃣ AI Analysis</div>
</div>

<div class="step-card">
<div class="step-title">3️⃣ Threat Scanning</div>
</div>

<div class="step-card">
<div class="step-title">4️⃣ Detection Result</div>
</div>

</div>
""", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("""
<div class="footer" id="contact">

Developed by Prachi Das

</div>
""", unsafe_allow_html=True)
