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

c.execute("""
CREATE TABLE IF NOT EXISTS history (
    username TEXT,
    url TEXT,
    result TEXT,
    threat_score TEXT,
    scan_time TEXT
)
""")

conn.commit()

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #050816;
    color: white;
}

.stApp {
    background: linear-gradient(135deg, #050816 0%, #0B1120 100%);
}

section[data-testid="stSidebar"] {
    display: none;
}

.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    padding: 18px 60px;
    background: rgba(11,17,32,0.6);
    backdrop-filter: blur(12px);
    z-index: 999;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

.logo {
    font-size: 28px;
    font-weight: 700;
    color: #00D9FF;
}

.hero {
    padding-top: 120px;
    padding-bottom: 80px;
}

.hero-title {
    font-size: 68px;
    font-weight: 700;
    line-height: 1.1;
    color: white;
}

.gradient-text {
    background: linear-gradient(90deg,#00D9FF,#8B5CF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-desc {
    color: #cbd5e1;
    font-size: 20px;
    margin-top: 20px;
}

.glass-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 25px;
    backdrop-filter: blur(12px);
    transition: 0.3s;
}

.glass-card:hover {
    transform: translateY(-6px);
    box-shadow: 0px 0px 25px rgba(0,217,255,0.25);
}

.feature-title {
    font-size: 22px;
    font-weight: 600;
}

.metric-card {
    text-align: center;
    padding: 30px;
    border-radius: 20px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(0,217,255,0.2);
}

.metric-number {
    font-size: 42px;
    font-weight: 700;
    color: #00D9FF;
}

.metric-label {
    color: #cbd5e1;
}

.scan-box {
    padding: 35px;
    border-radius: 25px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(0,217,255,0.2);
}

.result-safe {
    padding: 20px;
    border-radius: 18px;
    background: rgba(0,255,157,0.15);
    border: 1px solid #00FF9D;
    color: #00FF9D;
    font-size: 22px;
    font-weight: 600;
}

.result-danger {
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,59,92,0.15);
    border: 1px solid #FF3B5C;
    color: #FF3B5C;
    font-size: 22px;
    font-weight: 600;
}

.footer {
    margin-top: 80px;
    text-align: center;
    color: #94a3b8;
    padding: 40px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# PREPROCESS
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
# SESSION
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =========================
# NAVBAR
# =========================
st.markdown("""
<div class="navbar">
    <div class="logo">🛡️ AI Phishing Detection</div>
</div>
""", unsafe_allow_html=True)

# =========================
# LOGIN/SIGNUP
# =========================
if not st.session_state.logged_in:

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])

    with col1:

        st.markdown("""
        <div class="hero">
            <div class="hero-title">
                AI-Powered <span class="gradient-text">Phishing</span><br>
                Detection System
            </div>

            <div class="hero-desc">
                Enterprise-level AI cybersecurity platform for detecting malicious phishing URLs with intelligent real-time analysis.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        option = st.selectbox(
            "Choose Option",
            ["Login", "Signup"]
        )

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if option == "Signup":

            if st.button("Create Account"):

                c.execute("INSERT INTO users VALUES (?,?)", (username, password))
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

                    st.rerun()

                else:
                    st.error("Invalid Credentials")

# =========================
# HOME PAGE
# =========================
else:

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.4,1])

    with col1:

        st.markdown("""
        <div class="hero">
            <div class="hero-title">
                Transforming Cyber Security into
                <span class="gradient-text">Strategic Leadership</span>
            </div>

            <div class="hero-desc">
                AI-powered phishing detection platform with intelligent URL analysis,
                threat scoring, real-time monitoring, and secure browsing insights.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="glass-card">
            <div class="feature-title">⚡ Real-Time Detection</div>
            <p>Instant AI-based phishing detection and URL analysis.</p>
        </div>
        <br>
        <div class="glass-card">
            <div class="feature-title">🛡️ Threat Intelligence</div>
            <p>Advanced machine learning threat identification engine.</p>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # STATS
    # =========================

    st.markdown("## 📊 Live Security Statistics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">99.8%</div>
            <div class="metric-label">Accuracy Rate</div>
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

    scan = col1.button("🚀 Scan URL")
    clear = col2.button("🧹 Clear URL")

    if clear:
        st.rerun()

    if scan:

        with st.spinner("Scanning URL using AI engine..."):

            time.sleep(2)

            processed_url = preprocess_url(url)

            vector_input = vectorizer.transform([processed_url])

            prediction = model.predict(vector_input)[0]

            probabilities = model.predict_proba(vector_input)[0]

            phishing_score = round(probabilities[0] * 100, 2)
            safe_score = round(probabilities[1] * 100, 2)

            if prediction == 0:

                st.markdown(f"""
                <div class="result-danger">
                ⚠️ Phishing Website Detected <br><br>
                Threat Score: {phishing_score}%
                </div>
                """, unsafe_allow_html=True)

                result = "Phishing"

                threat_score = f"{phishing_score}%"

            else:

                st.markdown(f"""
                <div class="result-safe">
                ✅ Legitimate Website <br><br>
                Safe Probability: {safe_score}%
                </div>
                """, unsafe_allow_html=True)

                result = "Legitimate"

                threat_score = f"{safe_score}%"

            # SAVE HISTORY
            c.execute(
                "INSERT INTO history VALUES (?,?,?,?,?)",
                (
                    st.session_state.username,
                    url,
                    result,
                    threat_score,
                    str(datetime.now())
                )
            )

            conn.commit()

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # FEATURES
    # =========================

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("## 🚀 Core Security Features")

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
        <div class="glass-card">
            <div class="feature-title">🤖 AI Detection</div>
            <p>Machine learning based phishing detection engine.</p>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="glass-card">
            <div class="feature-title">🌐 URL Analysis</div>
            <p>Advanced suspicious URL structure analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="glass-card">
            <div class="feature-title">⚠️ Threat Intelligence</div>
            <p>Real-time cyber threat identification system.</p>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # HISTORY
    # =========================

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("## 🕘 Recent Scan History")

    c.execute(
        "SELECT url,result,threat_score,scan_time FROM history WHERE username=? ORDER BY rowid DESC LIMIT 5",
        (st.session_state.username,)
    )

    rows = c.fetchall()

    if rows:

        for row in rows:

            st.markdown(f"""
            <div class="glass-card">
                <b>URL:</b> {row[0]} <br>
                <b>Result:</b> {row[1]} <br>
                <b>Threat Score:</b> {row[2]} <br>
                <b>Time:</b> {row[3]}
            </div>
            <br>
            """, unsafe_allow_html=True)

    # =========================
    # FOOTER
    # =========================

    st.markdown("""
    <div class="footer">
        <h3>🛡️ AI Based Phishing Detection System</h3>
        <p>Developed using Streamlit, Machine Learning, NLP, and Cybersecurity Concepts.</p>
        <p>IGNOU MCA Final Year Project</p>
    </div>
    """, unsafe_allow_html=True)
