# 🛡️ AI-Based Phishing Detection System

> An AI-powered cybersecurity solution that detects phishing URLs in real time using Machine Learning, NLP-based URL analysis, and threat intelligence techniques.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red.svg)]()
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-green.svg)]()
[![Cybersecurity](https://img.shields.io/badge/Cybersecurity-Phishing%20Detection-orange.svg)]()

## 🚀 Live Demo

🔗 **Project Website:**
https://ai-phishing-detection-system.streamlit.app/

---

## 📌 Project Overview

Phishing attacks remain one of the most common and dangerous cybersecurity threats, targeting users through malicious URLs designed to steal credentials, financial information, and sensitive data.

This project presents an **AI-Based Phishing Detection System** that leverages Machine Learning and Natural Language Processing (NLP) techniques to automatically classify URLs as:

✅ Legitimate (Safe)

❌ Phishing (Malicious)

The system analyzes URL patterns using TF-IDF feature extraction and machine learning models to provide instant threat assessments through an interactive Streamlit web application.

---

## 🎯 Key Features

* 🔍 Real-Time URL Scanning
* 🤖 Machine Learning-Based Detection
* 📊 Threat Score Visualization
* 🔐 Login & Signup Authentication
* 📜 Scan History Dashboard
* 🧠 TF-IDF Feature Extraction
* 🚨 Phishing Keyword Detection
* 🎭 Fake Brand Impersonation Detection
* 🌙 Modern Cybersecurity Dashboard UI
* ⚡ Instant Prediction Results

---

## 🏗️ System Architecture

```text
User URL Input
      │
      ▼
URL Preprocessing
(Tokenization + Stemming)
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Machine Learning Model
(Multinomial Naive Bayes)
      │
      ▼
Threat Analysis Layer
      │
      ▼
Safe / Phishing Prediction
      │
      ▼
Streamlit Dashboard Output
```

## 🛠️ Technology Stack

### Programming Language

* Python

### Machine Learning

* Scikit-Learn
* Logistic Regression
* Multinomial Naive Bayes

### NLP & Data Processing

* NLTK
* RegexpTokenizer
* Snowball Stemmer
* TF-IDF Vectorizer

### Libraries

* Pandas
* NumPy
* Pickle

### Frontend & Deployment

* Streamlit
* Custom CSS

---

## 📂 Dataset Information

Dataset used:

**phishing_site_urls.csv**

Dataset Size:

| Category        |   Count |
| --------------- | ------: |
| Legitimate URLs | 392,924 |
| Phishing URLs   | 156,422 |
| Total URLs      | 549,346 |

The dataset contains real-world phishing and legitimate URLs used for model training and evaluation.

---

## 📈 Model Performance

Two machine learning models were trained and compared:

| Model                   | Accuracy |
| ----------------------- | -------: |
| Logistic Regression     |   95.75% |
| Multinomial Naive Bayes | 96.56% ✅ |

**Final Selected Model:** Multinomial Naive Bayes

Reason:

* Higher accuracy
* Faster inference
* Better suitability for TF-IDF text features

---

## 📸 Screenshots

### 🏠 Home Page

<img width="100%" src="screenshots/homepage.png">

### ✅ Legitimate URL Detection

<img width="100%" src="screenshots/safe-result.png">

### 🚨 Phishing URL Detection

<img width="100%" src="screenshots/phishing-result.png">

> Create a folder named **screenshots** and upload your images there.

---

## 📁 Repository Structure

```text
AI-Phishing-Detection-System/
│
├── AI_Phishing_Detection.ipynb
├── app.py
├── phishing_mnb.pkl
├── vectorizer.pkl
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Prachi-Das16/AI-Phishing-Detection-System.git
```

Navigate to project directory:

```bash
cd AI-Phishing-Detection-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 💡 How It Works

1. User enters a URL.
2. URL is preprocessed using NLP techniques.
3. TF-IDF converts URL text into numerical vectors.
4. Multinomial Naive Bayes analyzes URL patterns.
5. Additional phishing keyword and fake-brand checks are performed.
6. Threat score is generated.
7. User receives an instant phishing or safe verdict.

---

## 🔐 Security Highlights

* Detects suspicious URL patterns
* Identifies phishing keywords
* Detects fake brand impersonation
* Provides real-time threat scoring
* Supports cybersecurity awareness and safe browsing

---

## 🔮 Future Enhancements

* Browser Extension Integration
* Email Phishing Detection
* Deep Learning Models (LSTM/CNN)
* Threat Intelligence API Integration
* Real-Time URL Reputation Checks
* SOC Dashboard Integration
* User Reporting & Feedback Module

---

## 👩‍💻 Author

### Prachi Das | Cybersecurity Enthusiast

Passionate about Cybersecurity, Threat Detection, Network Security, Ethical Hacking, and AI-powered Security Solutions.

GitHub:
https://github.com/Prachi-Das16

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
It helps support future cybersecurity and open-source projects.
