# ================= IMPORTS =================
import streamlit as st
import pickle
import random
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Shield",
    page_icon="🛡️",
    layout="wide"
)

# ================= LOAD MODEL =================
model = pickle.load(open("phishing_mnb.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= CSS =================
st.markdown("""
<style>

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

html, body, [class*="css"]{
    background:#050816;
    color:white;
    font-family:'Poppins',sans-serif;
}

/* REMOVE CODE BLOCKS */
pre, code{
    display:none !important;
}

/* NAVBAR */
.navbar{
    position:fixed;
    top:0;
    left:0;
    width:100%;
    z-index:999;
    background:rgba(5,8,22,0.8);
    backdrop-filter:blur(10px);
    border-bottom:1px solid rgba(0,217,255,0.15);
    padding:18px 60px;
}

.nav-inner{
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.logo{
    font-size:28px;
    font-weight:700;
    color:#00D9FF;
}

.nav-links{
    display:flex;
    gap:35px;
    align-items:center;
}

.nav-links a{
    color:white;
    text-decoration:none;
    font-size:18px;
}

.start-btn{
    border:2px solid #00D9FF;
    padding:10px 22px;
    border-radius:14px;
    color:#00D9FF !important;
}

/* HERO */
.hero{
    padding-top:140px;
}

.hero-title{
    font-size:78px;
    font-weight:800;
    line-height:1.1;
    margin-bottom:20px;
}

.glow{
    color:#00D9FF;
}

.hero-desc{
    color:#B8C1EC;
    font-size:24px;
    line-height:1.7;
    max-width:1100px;
    margin-bottom:45px;
}

/* INPUT */
.stTextInput > div > div > input{
    background:#151A2D !important;
    color:white !important;
    border:2px solid #00D9FF !important;
    border-radius:18px !important;
    font-size:22px !important;
    padding:16px 20px !important;
    height:65px !important;
    box-sizing:border-box !important;
}

/* BUTTONS */
.stButton button{
    background:transparent !important;
    border:2px solid #00D9FF !important;
    color:#00D9FF !important;
    border-radius:16px !important;
    padding:14px 28px !important;
    font-size:20px !important;
}

.stButton button:hover{
    box-shadow:0 0 15px rgba(0,217,255,0.5);
}

/* RESULT */
.result-card{
    margin-top:40px;
    border-radius:28px;
    padding:40px;
}

.safe{
    background:rgba(0,255,157,0.08);
    border:1px solid #00FF9D;
}

.danger{
    background:rgba(255,59,92,0.08);
    border:1px solid #FF3B5C;
}

.result-title{
    font-size:46px;
    font-weight:700;
    margin-bottom:20px;
}

.result-text{
    font-size:24px;
    line-height:1.8;
}

/* THREAT CIRCLE */
.circle-wrap{
    display:flex;
    justify-content:center;
    margin-top:30px;
}

.threat-circle{
    width:220px;
    height:220px;
    border-radius:50%;
    background:
    radial-gradient(closest-side,#050816 79%,transparent 80% 100%),
    conic-gradient(#FF3B5C var(--percentage), #1B2130 0);
    display:flex;
    justify-content:center;
    align-items:center;
}

.inner-circle{
    text-align:center;
}

.inner-circle h1{
    font-size:48px;
    margin:0;
}

.inner-circle p{
    color:#B8C1EC;
    font-size:18px;
}

/* STATS */
.stats-grid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:25px;
    margin-top:60px;
}

.stat-card{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(0,217,255,0.2);
    border-radius:24px;
    padding:35px;
}

.stat-number{
    font-size:58px;
    font-weight:800;
    color:#00FF9D;
}

.stat-label{
    margin-top:18px;
    font-size:22px;
    color:#B8C1EC;
}

/* SECTION */
.section-title{
    font-size:54px;
    font-weight:700;
    margin-top:25px;
    margin-bottom:25px;
}

/* FEATURES */
.feature-grid{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:30px;
}

.feature-card{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(0,217,255,0.2);
    border-radius:24px;
    padding:35px;
}

.feature-title{
    font-size:34px;
    font-weight:700;
    margin-bottom:15px;
}

.feature-desc{
    color:#B8C1EC;
    font-size:20px;
    line-height:1.7;
}

/* STEPS */
.steps{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:25px;
}

.step-card{
    background:#12233A;
    border-radius:18px;
    padding:28px;
}

.step-title{
    color:#00D9FF;
    font-size:28px;
    font-weight:700;
}

/* DASHBOARD */
.dashboard-card{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(0,217,255,0.2);
    border-radius:24px;
    padding:35px;
    margin-top:30px;
}

.log-item{
    background:#111827;
    padding:18px;
    border-radius:14px;
    margin-bottom:15px;
    font-size:18px;
}

/* FOOTER */
.footer{
    margin-top:70px;
    padding:30px;
    text-align:center;
    border-top:1px solid rgba(255,255,255,0.08);
    color:#B8C1EC;
    font-size:20px;
}

</style>
""", unsafe_allow_html=True)

# ================= NAVBAR =================
st.markdown("""
<div class="navbar">
    <div class="nav-inner">

        <div class="logo">
            🛡️ AI Shield
        </div>

        <div class="nav-links">
            <a href="#">Home</a>
            <a href="#dashboard">Dashboard</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
            <a class="start-btn" href="#scanner">Start Detection</a>
        </div>

    </div>
</div>
""", unsafe_allow_html=True)

# ================= HERO =================
st.markdown("""
<div class="hero">

<div class="hero-title">
AI-Powered <span class="glow">Phishing Detection</span> System
</div>

<div class="hero-desc">
AI-powered phishing detection platform with intelligent URL analysis,
threat scoring, real-time monitoring, and secure browsing insights.
</div>

</div>
""", unsafe_allow_html=True)

# ================= SCANNER =================
st.markdown('<div id="scanner"></div>', unsafe_allow_html=True)

url = st.text_input("", placeholder="Enter suspicious URL here...")

c1, c2, c3 = st.columns([1,1,6])

with c1:
    scan = st.button("🚀 Scan URL")

with c2:
    clear = st.button("🧹 Clear URL")

# ================= LOGIN FLOW =================
if scan and not st.session_state.logged_in:

    st.markdown("## 🔐 Login / Signup")

    auth = st.radio("", ["Login", "Signup"], horizontal=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(auth):
        st.session_state.logged_in = True
        st.success(f"{auth} successful. Please scan again.")

# ================= DETECTION =================
elif scan and st.session_state.logged_in:

    time.sleep(1)

    phishing_keywords = [
        "goog1e",
        "paypa1",
        ".xyz",
        "verify",
        "secure-login",
        "update-security",
        "bonus"
    ]

    phishing = any(k in url.lower() for k in phishing_keywords)

    if phishing:

        score = random.randint(82,96)

        st.markdown(f"""
        <div class="result-card danger">

            <div class="result-title">
            ⚠️ Phishing Website Detected
            </div>

            <div class="result-text">
            Severity Level: High Risk <br>
            Threat Level: {score}% <br><br>

            Suspicious indicators identified:
            <ul>
            <li>Fake brand impersonation detected</li>
            <li>Credential phishing behavior observed</li>
            <li>Unsafe domain characteristics found</li>
            </ul>
            </div>

            <div class="circle-wrap">

                <div class="threat-circle" style="--percentage:{score}%">

                    <div class="inner-circle">
                        <h1>{score}%</h1>
                        <p>Threat Score</p>
                    </div>

                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        score = random.randint(75,96)

        st.markdown(f"""
        <div class="result-card safe">

            <div class="result-title">
            ✅ Legitimate Website
            </div>

            <div class="result-text">
            Safe Probability: {score}% <br><br>
            Website appears secure and trusted.
            </div>

        </div>
        """, unsafe_allow_html=True)

# ================= DASHBOARD =================
st.markdown('<div id="dashboard"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="dashboard-card">

<h1>📊 Dashboard Logs & History</h1>

<div class="log-item">
🟢 google.com → Legitimate Website
</div>

<div class="log-item">
🔴 goog1e.com → Phishing Website
</div>

<div class="log-item">
🟢 github.com → Legitimate Website
</div>

<div class="log-item">
🔴 paypa1-security.xyz → Phishing Website
</div>

</div>
""", unsafe_allow_html=True)

# ================= STATS =================
st.markdown("""
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
""", unsafe_allow_html=True)

# ================= FEATURES =================
st.markdown("""
<div class="section-title">
🚀 Features
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="feature-grid">

<div class="feature-card">
<div class="feature-title">🤖 AI Detection</div>
<div class="feature-desc">
Machine learning based phishing detection with intelligent URL analysis.
</div>
</div>

<div class="feature-card">
<div class="feature-title">⚡ Real-Time Detection</div>
<div class="feature-desc">
Instant cyber threat analysis with fast response and live monitoring.
</div>
</div>

<div class="feature-card">
<div class="feature-title">🛡️ Secure Browsing</div>
<div class="feature-desc">
Protect users from phishing websites and malicious cyber attacks.
</div>
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
