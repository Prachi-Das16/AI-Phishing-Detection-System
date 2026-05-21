import streamlit as st
import pickle
import sqlite3
import nltk

nltk.download('punkt')

from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="AI Phishing Detection System",
    page_icon="🛡️",
    layout="centered"
)

# Database Connection
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# Create Tables
c.execute('''
CREATE TABLE IF NOT EXISTS users(
username TEXT,
password TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS history(
username TEXT,
url TEXT,
result TEXT,
time TEXT
)
''')

conn.commit()

# Load ML Model
model = pickle.load(open('phishing_mnb.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

# Tokenizer and Stemmer
tokenizer = RegexpTokenizer(r'[A-Za-z]+')
stemmer = SnowballStemmer('english')

# URL Preprocessing
def preprocess_url(url):

    tokens = tokenizer.tokenize(url)

    stemmed = [stemmer.stem(word) for word in tokens]

    processed_url = ' '.join(stemmed)

    return processed_url


# Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = ""


# Sidebar
menu = st.sidebar.selectbox(
    "Navigation",
    ["Login", "Register", "Detection System", "History"]
)

# Register
if menu == "Register":

    st.title("📝 User Registration")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type='password')

    if st.button("Register"):

        c.execute(
            "INSERT INTO users VALUES (?,?)",
            (new_user, new_pass)
        )

        conn.commit()

        st.success("Registration Successful")


# Login
elif menu == "Login":

    st.title("🔐 User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

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
            st.error("Invalid Credentials")


# Detection System
elif menu == "Detection System":

    if st.session_state.logged_in:

        st.title("🛡️ AI Based Phishing Detection System")

        st.markdown("### Enter URL to Detect Phishing")

        url = st.text_input("Enter Website URL")

        if st.button("Check URL"):

            processed_url = preprocess_url(url)

            vector_input = vectorizer.transform([processed_url])

            result = model.predict(vector_input)[0]

            if result == 'bad':

                prediction = "⚠️ Phishing Website Detected"

                st.error(prediction)

            else:

                prediction = "✅ Legitimate Website"

                st.success(prediction)

            # Save History
            c.execute(
                "INSERT INTO history VALUES (?,?,?,?)",
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


# History
elif menu == "History":

    if st.session_state.logged_in:

        st.title("📜 Detection History")

        c.execute(
            "SELECT * FROM history WHERE username=?",
            (st.session_state.username,)
        )

        data = c.fetchall()

        for row in data:

            st.write(f"🌐 URL: {row[1]}")
            st.write(f"🛡️ Result: {row[2]}")
            st.write(f"⏰ Time: {row[3]}")
            st.markdown("---")

    else:
        st.warning("Please Login First")
