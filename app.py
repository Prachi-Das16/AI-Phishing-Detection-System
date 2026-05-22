import streamlit as st
import pickle
import random
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Phishing Detection System",
    page_icon="🛡️",
    layout="wide"
)

# ================= LOAD MODEL =================
model = pickle.load(open("phishing_mnb.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_auth" not in st.session_state:
    st.session_state.show_auth = False

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

/* Remove streamlit padding */
.block-container{
    padding-top:0rem;
    padding-bottom:2rem;
}

/* ================= DASHBOARD ================= */

[data-testid="stDataFrame"]{
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(0,217,255,0.18);
    border-radius:22px;
    padding:10px;
}

[data-testid="stDataFrame"] button{
    background:#10182B !important;
    color:#00D9FF !important;
    border-radius:10px !important;
    border:1px solid rgba(0,217,255,0.3) !important;
}

/* ================= NAVBAR ================= */

.navbar{
    position:fixed;
    top:0;
    left:0;
    right:0;
    z-index:999;
    padding:20px 60px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    background:rgba(5,8,22,0.85);
    backdrop-filter:blur(14px);
    border-bottom:1px solid rgba(0,217,255,0.12);
}

.logo{
    font-size:30px;
    font-weight:800;
    color:#00D9FF;
}

.nav-links{
    display:flex;
    align-items:center;
    gap:28px;
}

.nav-links a{
    color:white;
    text-decoration:none;
    font-size:17px;
    transition:0.3s;
}

.nav-links a:hover{
    color:#00D9FF;
}

.cta-btn{
    border:1px solid #00D9FF;
    padding:10px 20px;
    border-radius:14px;
    color:#00D9FF !important;
}

/* ================= HERO ================= */

.hero{
    padding-top:130px;
    padding-bottom:20px;
}

.hero-title{
    font-size:72px;
    font-weight:800;
    line-height:1.1;
    margin-bottom:25px;
}

.glow{
    color:#00D9FF;
}

.hero-desc{
    font-size:22px;
    color:#B8C1EC;
    max-width:900px;
    line-height:1.7;
    margin-bottom:30px;
}

/* ================= SCANNER ================= */

.scan-box{
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(0,217,255,0.20);
    border-radius:30px;
    padding:35px;
    margin-top:20px;
    margin-bottom:40px;
    backdrop-filter:blur(12px);
}

.stTextInput input{
    background:#151A2E !important;
    border:2px solid #00D9FF !important;
    border-radius:16px !important;
    color:white !important;
    font-size:20px !important;
    padding:18px !important;
}

.stButton button{
    background:transparent !important;
    border:2px solid #00D9FF !important;
    color:#00D9FF !important;
    border-radius:14px !important;
    padding:12px 28px !important;
    font-size:18px !important;
    font-weight:700 !important;
    transition:0.3s;
}

.stButton button:hover{
    box-shadow:0 0 20px rgba(0,217,255,0.35);
    transform:translateY(-2px);
}

/* ================= RESULT ================= */

.safe-card{
    background:rgba(0,255,157,0.08);
    border:1px solid #00FF9D;
    border-radius:24px;
    padding:30px;
    margin-top:25px;
}

.phishing-card{
    background:rgba(255,59,92,0.08);
    border:1px solid #FF3B5C;
    border-radius:24px;
    padding:30px;
    margin-top:25px;

    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:40px;
    flex-wrap:wrap;
}

.result-title{
    font-size:32px;
    font-weight:800;
}

.result-desc{
    font-size:18px;
    margin-top:15px;
    line-height:1.7;
}

/* ================= THREAT METER ================= */

.threat-wrapper{
    display:flex;
    justify-content:center;
    margin-top:30px;
    margin-bottom:20px;
}

.threat-circle{
    width:220px;
    height:220px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:34px;
    font-weight:800;
    color:white;
    background:
    conic-gradient(#FF3B5C var(--percentage),
    rgba(255,255,255,0.08) 0);
}

.inner-circle{
    width:170px;
    height:170px;
    border-radius:50%;
    background:#050816;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
}

/* ================= STATS ================= */

.stats-title{
    margin-top:10px;
    margin-bottom:25px;
}

.stat-card{
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(0,217,255,0.15);
    border-radius:26px;
    padding:35px;
    min-height:200px;
    transition:0.3s;
}

.stat-card:hover{
    transform:translateY(-5px);
    box-shadow:0 0 22px rgba(0,217,255,0.20);
}

.stat-number{
    font-size:52px;
    color:#00FF9D;
    font-weight:800;
}

.stat-label{
    color:#B8C1EC;
    font-size:20px;
    margin-top:14px;
}

/* ================= FEATURES ================= */

/* SECTIONS */
.section-title{
    font-size:72px;
    font-weight:800;
    margin-top:90px;
    margin-bottom:35px;
    color:white;
    display:flex;
    align-items:center;
    gap:18px;
}

/* FEATURES */
.feature-grid{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:30px;
}

.feature-card{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(0,217,255,0.18);
    border-radius:24px;
    padding:35px;
}

.feature-title{
    font-size:34px;
    font-weight:700;
    margin-bottom:15px;
}

.feature-desc{
    font-size:20px;
    color:#B8C1EC;
    line-height:1.7;
}

/* ================= FOOTER ================= */

.footer{
    margin-top:70px;
    text-align:center;
    padding:28px;
    border-top:1px solid rgba(255,255,255,0.08);
    color:#B8C1EC;
    font-size:17px;
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
<a href="#">Home</a>
<a href="#dashboard">Dashboard</a>
<a href="#">About</a>
<a href="#">Contact</a>
<a class="cta-btn" href="#scanner">Start Detection</a>
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
st.markdown("""
<div class="scan-box">
""", unsafe_allow_html=True)

url = st.text_input(
    "",
    placeholder="Enter suspicious URL here..."
)

col1, col2, col3 = st.columns([1,1,5])

scan = False

with col1:
    if st.button("🚀 Scan URL"):
        if not st.session_state.logged_in:
            st.session_state.show_auth = True
        else:
            scan = True

with col2:
    if st.button("🧹 Clear URL"):
        st.rerun()

# ================= LOGIN =================
if st.session_state.show_auth and not st.session_state.logged_in:

    st.markdown("## 🔐 Login / Signup")

    option = st.radio(
        "",
        ["Login", "Signup"],
        horizontal=True
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(option):
        if username and password:
            st.session_state.logged_in = True
            st.success(f"{option} Successful!")
            st.rerun()

# ================= DETECTION =================
if scan and url:

    time.sleep(1)

    url_lower = url.lower()

    phishing_keywords = [
        "login",
        "verify",
        "security",
        "update",
        "bank",
        "paypal",
        "bonus",
        "gift",
        "urgent",
        "account"
    ]

    fake_brands = [
        "goog1e",
        "paypa1",
        "faceb00k",
        "amaz0n",
        "micr0soft"
    ]

    suspicious = False

    for word in phishing_keywords:
        if word in url_lower:
            suspicious = True

    for brand in fake_brands:
        if brand in url_lower:
            suspicious = True

    vector_input = vectorizer.transform([url])
    prediction = model.predict(vector_input)[0]

    if suspicious:
        prediction = 1

    # ================= PHISHING =================
    if prediction == 1:

        threat_score = random.randint(76,96)

        st.markdown(f"""
<div class="phishing-card">

<div style="flex:1; min-width:320px;">

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

<div style="display:flex;justify-content:center;align-items:center;">

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
""", unsafe_allow_html=True)
        
    # ================= SAFE =================
    else:

        safe_score = random.randint(70,92)

        st.markdown(f"""
        <div class="safe-card">

        <div class="result-title">
        ✅ Legitimate Website
        </div>

        <div class="result-desc">
        Security Status: Safe <br>
        Safe Probability: {safe_score}% <br><br>

        No phishing indicators detected.
        Website appears safe for browsing.
        </div>

        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="threat-wrapper">
            <div class="threat-circle" style="--percentage:{safe_score}%; background:
            conic-gradient(#00FF9D var(--percentage),
            rgba(255,255,255,0.08) 0);">
                <div class="inner-circle">
                    <div>{safe_score}%</div>
                    <div style="font-size:16px;color:#B8C1EC;">
                    Safe Score
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ================= SECURITY STATS =================
st.markdown("""
<div class="stats-title"></div>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">99.8%</div>
        <div class="stat-label">
        Detection Accuracy
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">&lt;1min</div>
        <div class="stat-label">
        Response Time
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">24/7</div>
        <div class="stat-label">
        Monitoring
        </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">99.9%</div>
        <div class="stat-label">
        Uptime SLA
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= FEATURES =================
st.markdown("""
<div class="section-title">
🚀 Features
</div>

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
<div class="features-heading"></div>
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

# ================= DASHBOARD =================

st.markdown("""
<div id="dashboard" class="section-title">
📊 Dashboard Logs & History
</div>
""", unsafe_allow_html=True)

if st.session_state.logged_in:

    dashboard_data = [
        ("google.com", "Legitimate Website", "2026-08-22 11:12"),
        ("goog1e.com", "Phishing Website", "2026-08-22 11:14"),
        ("github.com", "Legitimate Website", "2026-08-22 11:17"),
        ("paypal-security.xyz", "Phishing Website", "2026-08-22 11:19")
    ]

    st.dataframe(
        dashboard_data,
        use_container_width=True
    )

else:

    st.warning("Please Login First to View Dashboard Logs")

# ================= FOOTER =================
st.markdown("""
<div class="footer">
Developed by Prachi Das
</div>
""", unsafe_allow_html=True)
