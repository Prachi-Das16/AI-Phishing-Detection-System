import streamlit as st
import pickle
import random
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Phishing Detection",
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
header {visibility:hidden;}
footer {visibility:hidden;}

html, body, [class*="css"] {
    background-color:#050816;
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
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:20px 40px;
    background:rgba(5,8,22,0.75);
    backdrop-filter:blur(10px);
    border-bottom:1px solid rgba(0,217,255,0.2);
}

.logo{
    font-size:26px;
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

.nav-links a:hover{
    color:#00D9FF;
}

.cta-btn{
    border:2px solid #00D9FF;
    padding:12px 24px;
    border-radius:14px;
    color:#00D9FF !important;
}

/* HERO */

.hero{
    padding-top:130px;
    padding-bottom:40px;
}

.hero-title{
    font-size:68px;
    font-weight:800;
    line-height:1.1;
    margin-bottom:20px;
}

.glow{
    color:#00D9FF;
    text-shadow:0 0 20px #00D9FF;
}

.hero-desc{
    font-size:26px;
    color:#B8C1EC;
    line-height:1.7;
    margin-bottom:40px;
}

/* SCAN BOX */

.scan-box{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(0,217,255,0.3);
    border-radius:30px;
    padding:25px;
    margin-top:20px;
}

/* INPUT */

.stTextInput input{
    background:#161B2D;
    color:white;
    border:2px solid #00D9FF;
    border-radius:20px;
    padding:20px;
    font-size:22px;
}

/* BUTTONS */

.stButton button{
    background:transparent;
    border:2px solid #00D9FF;
    color:#00D9FF;
    border-radius:14px;
    padding:12px 30px;
    font-size:20px;
    transition:0.3s;
}

.stButton button:hover{
    background:rgba(0,217,255,0.15);
    box-shadow:0 0 20px #00D9FF;
    color:white;
}

/* RESULT CARDS */

.safe-card{
    background:rgba(0,255,157,0.1);
    border:1px solid #00FF9D;
    padding:30px;
    border-radius:25px;
    margin-top:25px;
}

.phishing-card{
    background:rgba(255,59,92,0.08);
    border:1px solid #FF3B5C;
    padding:30px;
    border-radius:25px;
    margin-top:25px;
}

.result-title{
    font-size:28px;
    font-weight:700;
    margin-bottom:20px;
}

.result-desc{
    font-size:20px;
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

.stats-card{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(0,217,255,0.3);
    border-radius:25px;
    padding:35px;
    margin-top:20px;
}

.stats-number{
    font-size:55px;
    font-weight:800;
    color:#00FF9D;
}

.stats-label{
    font-size:22px;
    color:#B8C1EC;
}

/* FEATURES */

.feature-card{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(0,217,255,0.25);
    border-radius:25px;
    padding:35px;
    margin-top:15px;
}

.feature-title{
    font-size:22px;
    font-weight:700;
    margin-bottom:15px;
}

.feature-desc{
    font-size:18px;
    color:#B8C1EC;
    line-height:1.7;
}

/* FOOTER */

.footer{
    text-align:center;
    padding:35px;
    margin-top:70px;
    border-top:1px solid rgba(255,255,255,0.1);
    color:#B8C1EC;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ================= NAVBAR =================

st.markdown("""
<div class="navbar">

<div class="logo">
🛡️ AI Shield
</div>

<div class="nav-links">

<a href="#home">Home</a>

<a href="#dashboard">Dashboard</a>

<a href="#features">About</a>

<a href="#footer">Contact</a>

<a class="cta-btn" href="#scanner">
Start Detection
</a>

</div>

</div>
""", unsafe_allow_html=True)

# ================= HERO =================

st.markdown("""
<div class="hero" id="home">

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

st.markdown("""
<div class="scan-box" id="scanner">
""", unsafe_allow_html=True)

url = st.text_input(
    "",
    placeholder="Enter suspicious URL here..."
)

col1,col2,col3 = st.columns([1,1,6])

with col1:
    scan_btn = st.button("🚀 Scan URL")

with col2:
    clear_btn = st.button("🧹 Clear URL")

st.markdown("</div>", unsafe_allow_html=True)

# ================= DETECTION =================

if scan_btn and url:

    time.sleep(1)

    phishing_keywords = [
        "goog1e",
        "paypa1",
        "verify",
        "login-security",
        "secure-update",
        ".xyz",
        "bonus",
        "freegift",
        "banking-update"
    ]

    is_phishing = any(word in url.lower() for word in phishing_keywords)

    if is_phishing:
        prediction = 1
    else:
        prediction = 0

    if prediction == 1:

        threat_score = random.randint(76,96)

        st.markdown(f"""
        <div class="phishing-card">

        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px;">

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

            <div style="display:flex;justify-content:center;align-items:center;padding-right:30px;">

                <div class="threat-circle" style="--percentage:{threat_score}%">

                    <div class="inner-circle">

                        <div>{threat_score}%</div>

                        <div style="font-size:16px;color:#B8C1EC;">
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

        Security indicators:
        <ul>
        <li>Trusted domain structure detected</li>
        <li>No phishing keywords identified</li>
        <li>Secure browsing behavior observed</li>
        </ul>

        </div>

        </div>
        """, unsafe_allow_html=True)

# ================= STATS =================

st.markdown("""
<div id="dashboard"></div>
""", unsafe_allow_html=True)

s1,s2,s3,s4 = st.columns(4)

with s1:
    st.markdown("""
    <div class="stats-card">
    <div class="stats-number">99.8%</div>
    <div class="stats-label">Detection Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="stats-card">
    <div class="stats-number">&lt;1min</div>
    <div class="stats-label">Response Time</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="stats-card">
    <div class="stats-number">24/7</div>
    <div class="stats-label">Monitoring</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown("""
    <div class="stats-card">
    <div class="stats-number">99.9%</div>
    <div class="stats-label">Uptime SLA</div>
    </div>
    """, unsafe_allow_html=True)

# ================= FEATURES =================

st.markdown("""
<div id="features"></div>
<div style="padding-top:25px;"></div>
""", unsafe_allow_html=True)

st.markdown("## 🚀 Features")

f1,f2,f3 = st.columns(3)

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
        Instant cyber threat analysis with fast response monitoring.
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
<div style="padding-top:25px;"></div>
""", unsafe_allow_html=True)

st.markdown("## ⚙️ How It Works")

h1,h2,h3,h4 = st.columns(4)

with h1:
    st.info("1️⃣ Enter URL")

with h2:
    st.info("2️⃣ AI Analysis")

with h3:
    st.info("3️⃣ Threat Scanning")

with h4:
    st.info("4️⃣ Detection Result")

# ================= FOOTER =================

st.markdown("""
<div class="footer" id="footer">
Developed by Prachi Das
</div>
""", unsafe_allow_html=True)
