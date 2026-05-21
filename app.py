import streamlit as st
import pickle
import sqlite3
import re
from datetime import datetime

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="AI Phishing Detection System",
    page_icon="🛡️",
    layout="centered"
)

# ================= DATABASE =================

conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# Create Users Table
c.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
)
""")

# Create History Table
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

menu = st.sidebar.selectbox(
    "Navigation Menu",
    ["Login", "Register", "Detection System", "History"]
)

# ================= REGISTER =================

if menu == "Register":

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

        st.success("Registration Successful")

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

            st.success("Login Successful")

        else:

            st.error("Invalid Username or Password")

# ================= DETECTION SYSTEM =================

elif menu == "Detection System":

    if st.session_state.logged_in:

        st.title("🛡️ AI Based Phishing Detection System")

        st.markdown("## Enter URL for Detection")

        url = st.text_input("Enter Website URL")

        if st.button("Check URL"):

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

            # Manual Rule Detection
            if is_suspicious:

                prediction = "⚠️ Phishing Website Detected"

                st.error(prediction)

            else:

                processed_url = preprocess_url(url)

                vector_input = vectorizer.transform([processed_url])

                prediction_result = model.predict(vector_input)[0]

                # Fixed Label Logic
                if prediction_result == 'bad':

                    prediction = "✅ Legitimate Website"

                    st.success(prediction)

                else:

                    prediction = "⚠️ Phishing Website Detected"

                    st.error(prediction)

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

        st.warning("Please Login First")

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

                st.markdown("### 🌐 URL")
                st.write(row[1])

                st.markdown("### 🛡️ Result")
                st.write(row[2])

                st.markdown("### ⏰ Time")
                st.write(row[3])

                st.markdown("---")

        else:

            st.info("No Detection History Found")

    else:

        st.warning("Please Login First")
