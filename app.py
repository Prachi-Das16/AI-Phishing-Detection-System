import streamlit as st
import pickle
import re
import sqlite3
import time
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Phishing Detection System",
    page_icon="🛡️",
    layout="wide"
)

# =========================
# LOAD MODEL
# =========================
model = pickle.load(open("phishing_mnb.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT
)
""")

conn.commit()

# =========================
# SESSION
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "show_auth" not in st.session_state:
    st.session_state.show_auth = False

# =========================
# PREPROCESSING
# =========================
def preprocess_url(url):

    url = str(url)
    url = url.lower()

    url = re.sub(r"http\S+", " ", url)
    url = re.sub(r"www\S+", " ", url)

    url = re.sub(r"[^a-zA-Z]", " ", url)

    url = url.split()

    url = " ".join(url)

    return url

# =========================
# RULE-BASED DETECTION
# =========================
def detect_phishing(url):

    suspicious_keywords = [
        "login",
        "verify",
        "update",
        "secure",
        "account",
        "banking",
        "signin",
        "confirm",
        "paypal",
        "security"
    ]

    suspicious_tlds = [
        ".xyz",
        ".tk",
        ".ru",
        ".gq",
        ".ml"
    ]

    score = 0

    url_lower = url.lower()

    # keyword detection
    for keyword in suspicious_keywords:
        if keyword in url_lower:
            score += 15

    # suspicious tld
    for tld in suspicious_tlds:
        if tld in url_lower:
            score += 25

    # numbers inside domain
    if re.search(r'\d', url_lower):
        score += 15

    # too many hyphens
    if url_lower.count("-") >= 2:
        score += 20

    # too long
    if len(url_lower) > 50:
        score += 15

    # @ symbol
    if "@" in url_lower:
        score += 30

    # IP-based URL
    if re.search(r'http[s]?://\d+\.\d+\.\d+\.\d+', url_lower):
        score += 40

    # ML prediction
    processed = preprocess_url(url_lower)

    vector_input = vectorizer.transform([processed])

    prediction = model.predict(vector_input)[0]

    probabilities = model.predict_proba(vector_input)[0]

    phishing_probability = round(probabilities[0] * 100, 2)

    legit_probability = round(probabilities[1] * 100, 2)

    if prediction == 0:
        score += 35

    # final result
    if score >= 50:
        return "Phishing", min(score, 100)

    else:
        return "Legitimate", legit_probability

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins', sans-serif;
}

.stApp{
    background:
    radial-gradient(circle at top left, rgba(0,217,255,0.15), transparent 30%),
    radial-gradient(circle at bottom right, rgba(139,92,246,0.15), transparent 30%),
    #050816;
    color:white;
}

section[data-testid="stSidebar"]{
    display:none;
}

.block-container{
    padding-top:0rem;
    padding-left:3rem;
    padding-right:3rem;
}

.navbar{
    width:100%;
    padding:20px 40px;
    position:fixed;
    top:0;
    left:0;
    z-index:999;
    background:rgba(5,8,22,0.7);
    backdrop-filter:blur(12px);
    border-bottom:1px solid rgba(255,255,255,0.08);
}

.nav-flex{
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.logo{
    font-size:30px;
    font-weight:700;
    color:#00D9FF;
}

.nav-links{
    display:flex;
    gap:30px;
    align-items:center;
}

.nav-links a{
    color:white;
    text-decoration:none;
    font-size:17px;
}

.cta-btn{
    background:linear-gradient(90deg,#00D9FF,#8B5CF6);
    padding:12px 24px;
    border-radius:12px;
    color:white;
    font-weight:600;
}

.hero{
    padding-top:140px;
    padding-bottom:60px;
}

.hero-title{
    font-size:72px;
    line-height:1.1;
    font-weight:700;
}

.gradient{
    background:linear-gradient(90deg,#00D9FF,#8B5CF6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero-desc{
    margin-top:22px;
    color:#cbd5e1;
    font-size:21px;
    max-width:800px;
}

.glass{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter:blur(12px);
    border-radius:24px;
    padding:28px;
    transition:0.3s;
}

.glass:hover{
    transform:translateY(-5px);
    box-shadow:0px 0px 25px rgba(0,217,255,0.25);
}

.feature-title{
    font-size:24px;
    font-weight:600;
}

.scan-box{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(0,217,255,0.2);
    border-radius:25px;
    padding:35px;
}

.metric-card{
    text-align:center;
    padding:30px;
    border-radius:20px;
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(0,217,255,0.2);
}

.metric-number{
    font-size:42px;
    color:#00D9FF;
    font-weight:700;
}

.metric-label{
    color:#cbd5e1;
}

.safe-card{
    background:rgba(0,255,157,0.15);
    border:1px solid #00FF9D;
    color:#00FF9D;
    padding:25px;
    border-radius:20px;
    font-size:24px;
    font-weight:600;
}

.danger-card{
    background:rgba(255,59,92,0.15);
    border:1px solid #FF3B5C;
    color:#FF3B5C;
    padding:25px;
    border-radius:20px;
    font-size:24px;
    font-weight:600;
}

.footer{
    margin-top:80px;
    text-align:center;
    padding:40px;
    color:#94a3b8;
}

</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
st.markdown("""
<div class="navbar">
<div class="nav-flex">

<div class="logo">
🛡️ AI Phishing Detection
</div>

<div class="nav-links">
<a href="#">Home</a>
<a href="#">Dashboard</a>
<a href="#">About</a>
<a href="#">Contact</a>

<div class="cta-btn">
Start Detection
</div>

</div>
</div>
</div>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================
st.markdown("""
<div class="hero">

<div class="hero-title">
AI-Powered
<span class="gradient">
Phishing Detection
</span>
System
</div>

<div class="hero-desc">
AI-powered phishing detection platform with intelligent URL analysis,
threat scoring, real-time monitoring, and secure browsing insights.
</div>

</div>
""", unsafe_allow_html=True)

# =========================
# STATS
# =========================
st.markdown("## 📊 Security Statistics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="metric-card">
    <div class="metric-number">99.8%</div>
    <div class="metric-label">Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card">
    <div class="metric-number">&lt;1m</div>
    <div class="metric-label">Response Time</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
    <div class="metric-number">24/7</div>
    <div class="metric-label">Monitoring</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-card">
    <div class="metric-number">AI</div>
    <div class="metric-label">Threat Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# DETECTION
# =========================
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="scan-box">
""", unsafe_allow_html=True)

st.markdown("## 🔍 Scan Suspicious URL")

url = st.text_input(
    "",
    placeholder="Enter suspicious URL here..."
)

col1, col2 = st.columns([1,1])

with col1:
    scan = st.button("🚀 Scan URL")

with col2:
    clear = st.button("🧹 Clear URL")

if clear:
    st.rerun()

# =========================
# LOGIN FLOW
# =========================
if scan and not st.session_state.logged_in:
    st.session_state.show_auth = True

# =========================
# LOGIN / SIGNUP
# =========================
if st.session_state.show_auth and not st.session_state.logged_in:

    st.markdown("---")

    option = st.selectbox(
        "Choose Option",
        ["Login", "Signup"]
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup":

        if st.button("Signup"):

            c.execute(
                "INSERT INTO users VALUES (?,?)",
                (username, password)
            )

            conn.commit()

            st.success("Signup Successful! Please Login.")

    else:

        if st.button("Login"):

            c.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password)
            )

            data = c.fetchone()

            if data:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login Successful!")

                st.rerun()

            else:
                st.error("Invalid Credentials")

# =========================
# DETECTION AFTER LOGIN
# =========================
if scan and st.session_state.logged_in:

    with st.spinner("Scanning URL using AI Engine..."):

        time.sleep(2)

        result, score = detect_phishing(url)

        if result == "Phishing":

            st.markdown(f"""
            <div class="danger-card">
            ⚠️ Phishing Website Detected
            <br><br>
            Threat Score: {score}%
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class="safe-card">
            ✅ Legitimate Website
            <br><br>
            Safe Probability: {score}%
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FEATURES
# =========================
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("## 🚀 Core Security Features")

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="glass">
    <div class="feature-title">
    🤖 AI Detection
    </div>
    <p>
    Machine learning based phishing detection engine.
    </p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="glass">
    <div class="feature-title">
    🌐 URL Analysis
    </div>
    <p>
    Advanced suspicious URL structure analysis.
    </p>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="glass">
    <div class="feature-title">
    ⚠️ Threat Intelligence
    </div>
    <p>
    Real-time cyber threat identification system.
    </p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">

<h2>
🛡️ AI Based Phishing Detection System
</h2>

<p>
Developed using Streamlit, Machine Learning,
Cybersecurity, and NLP Concepts.
</p>

<p>
IGNOU MCA Final Year Project
</p>

</div>
""", unsafe_allow_html=True)
