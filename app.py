import streamlit as st
import pickle
import sqlite3
import re
import pandas as pd
from datetime import datetime

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="AI Phishing Detection System",
    page_icon="🛡️",
    layout="wide"
)

# ================= CUSTOM CSS =================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #000428, #004e92);
    color: white;
}

section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #374151;
}

h1, h2, h3, h4 {
    color: white;
}

.stTextInput > div > div > input {
    background-color: #1f2937;
    color: white;
    border-radius: 12px;
    border: 1px solid #3b82f6;
    padding: 12px;
}

.stButton > button {
    background: linear-gradient(90deg, #2563eb, #06b6d4);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 28px;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #1d4ed8, #0891b2);
}

.metric-card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
}

.result-box {
    padding: 25px;
    border-radius: 20px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    margin-top: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    text-align: center;
}

.footer {
    text-align: center;
    margin-top: 50px;
    color: #d1d5db;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ================= DATABASE =================

conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# Users Table
c.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
)
""")

# History Table
c.execute("""
CREATE TABLE IF NOT EXISTS history(
    username TEXT,
    url TEXT,
    result TEXT,
    time TEXT
)
""")

conn.commit()

# ================= LOAD MODEL =================

model = pickle.load(open('phishing_mnb.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# ================= PREPROCESS FUNCTION =================

def preprocess_url(url):

    url = str(url)

    url = url.lower()

    url = re.sub(r'[^a-zA-Z]', ' ', url)

    url = url.split()

    url = ' '.join(url)

    return url

# ================= SESSION =================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = ""

# ================= SIDEBAR =================

st.sidebar.title("🛡️ Navigation")

menu = st.sidebar.selectbox(
    "Choose Option",
    [
        "Home",
        "Login",
        "Register",
        "Detection System",
        "Dashboard Analytics",
        "History"
    ]
)

# ================= HOME =================

if menu == "Home":

    st.markdown("""
    # 🛡️ AI Based Phishing Detection System

    ### Advanced Machine Learning Powered Cybersecurity Platform
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
        <h2>🔐</h2>
        <h3>Secure Detection</h3>
        <p>AI powered phishing URL analysis</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
        <h2>⚡</h2>
        <h3>Real Time Analysis</h3>
        <p>Instant phishing prediction system</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
        <h2>📊</h2>
        <h3>Analytics Dashboard</h3>
        <p>User history and threat insights</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.image(
        "https://images.unsplash.com/photo-1550751827-4bd374c3f58b",
        use_container_width=True
    )

# ================= REGISTER =================

elif menu == "Register":

    st.title("📝 User Registration")

    new_user = st.text_input("Create Username")

    new_pass = st.text_input(
        "Create Password",
        type="password"
    )

    if st.button("Register"):

        c.execute(
            "INSERT INTO users VALUES (?, ?)",
            (new_user, new_pass)
        )

        conn.commit()

        st.success("✅ Registration Successful")

# ================= LOGIN =================

elif menu == "Login":

    st.title("🔐 User Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        data = c.fetchone()

        if data:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success("✅ Login Successful")

        else:

            st.error("❌ Invalid Username or Password")

# ================= DETECTION SYSTEM =================

elif menu == "Detection System":

    if st.session_state.logged_in:

        st.markdown("""
        # 🛡️ AI Based Phishing Detection System

        ### Enter URL for Security Analysis
        """)

        url = st.text_input("🌐 Enter Website URL")

        if st.button("🚀 Check URL"):

            with st.spinner("Analyzing URL Security..."):

                suspicious_keywords = [
                    "login",
                    "verify",
                    "update",
                    "secure",
                    "bank",
                    "account",
                    "paypal"
                ]

                is_suspicious = False

                # Number Detection
                if any(char.isdigit() for char in url):

                    is_suspicious = True

                # Keyword Detection
                for word in suspicious_keywords:

                    if word in url.lower():

                        is_suspicious = True

                # Prediction
                if is_suspicious:

                    prediction = "⚠️ Phishing Website Detected"

                    st.markdown(f"""
                    <div class="result-box">
                    <h2>{prediction}</h2>
                    <p>This URL contains suspicious phishing indicators.</p>
                    </div>
                    """, unsafe_allow_html=True)

                else:

                    processed_url = preprocess_url(url)

                    vector_input = vectorizer.transform([processed_url])

                    prediction_result = model.predict(vector_input)[0]

                    if prediction_result == 'bad':

                        prediction = "✅ Legitimate Website"

                        st.markdown(f"""
                        <div class="result-box">
                        <h2>{prediction}</h2>
                        <p>No major phishing indicators detected.</p>
                        </div>
                        """, unsafe_allow_html=True)

                    else:

                        prediction = "⚠️ Phishing Website Detected"

                        st.markdown(f"""
                        <div class="result-box">
                        <h2>{prediction}</h2>
                        <p>Potential phishing activity detected.</p>
                        </div>
                        """, unsafe_allow_html=True)

                # Save History
                c.execute(
                    "INSERT INTO history VALUES (?, ?, ?, ?)",
                    (
                        st.session_state.username,
                        url,
                        prediction,
                        str(datetime.now())
                    )
                )

                conn.commit()

    else:

        st.warning("⚠️ Please Login First")

# ================= DASHBOARD =================

elif menu == "Dashboard Analytics":

    if st.session_state.logged_in:

        st.title("📊 Security Analytics Dashboard")

        c.execute(
            "SELECT * FROM history WHERE username=?",
            (st.session_state.username,)
        )

        data = c.fetchall()

        total_scans = len(data)

        phishing_count = len([
            row for row in data
            if "Phishing" in row[2]
        ])

        legit_count = len([
            row for row in data
            if "Legitimate" in row[2]
        ])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Scans",
                total_scans
            )

        with col2:
            st.metric(
                "Phishing URLs",
                phishing_count
            )

        with col3:
            st.metric(
                "Legitimate URLs",
                legit_count
            )

        if data:

            df = pd.DataFrame(
                data,
                columns=[
                    "Username",
                    "URL",
                    "Result",
                    "Time"
                ]
            )

            st.markdown("## 📋 Scan History Table")

            st.dataframe(df)

    else:

        st.warning("⚠️ Please Login First")

# ================= HISTORY =================

elif menu == "History":

    if st.session_state.logged_in:

        st.title("📜 Detection History")

        c.execute(
            "SELECT * FROM history WHERE username=?",
            (st.session_state.username,)
        )

        data = c.fetchall()

        if data:

            for row in data:

                st.markdown(f"""
                <div class="result-box">

                <h3>🌐 URL</h3>
                <p>{row[1]}</p>

                <h3>🛡️ Result</h3>
                <p>{row[2]}</p>

                <h3>⏰ Time</h3>
                <p>{row[3]}</p>

                </div>
                <br>
                """, unsafe_allow_html=True)

        else:

            st.info("No History Found")

    else:

        st.warning("⚠️ Please Login First")

# ================= FOOTER =================

st.markdown("""
<div class="footer">

Developed By Prachi Das | MCA Final Year Project  
AI Based Phishing Detection System using Machine Learning

</div>
""", unsafe_allow_html=True)
