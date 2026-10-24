# 🎫 AI-Powered Customer Support Ticket Intelligence System

An intelligent customer support application designed to automate ticket classification, analyze customer sentiment, recommend ticket priorities, and generate auto-responses using Natural Language Processing (NLP), Machine Learning, and an interactive Streamlit dashboard.

---

## 🚀 Features

- **Automated Ticket Classification:** Categorizes customer complaints into Billing, Technical Issues, Account Access, Refund Requests, and Product Complaints using TF-IDF and Machine Learning.
- **Sentiment Analysis:** Identifies customer sentiment (Positive, Neutral, Negative) to gauge customer mood.
- **Priority Recommendation:** Recommends ticket priority (High, Medium, Low) based on sentiment, category, and urgency rules.
- **Suggested Responses:** Generates draft responses for support agents using predefined templates.
- **Interactive Dashboard (Streamlit):** Visualizes trends with Plotly charts, key metrics, search filters, and CSV report downloads.
- **Database Integration (SQLite):** Persists ticket records, allowing agents to add new tickets and update ticket statuses.

---

## 🛠️ Technology Stack

- **Programming Language:** Python
- **Web Interface:** Streamlit
- **Data Analysis & Processing:** Pandas, NumPy
- **Machine Learning & NLP:** Scikit-learn, TF-IDF
- **Data Visualization:** Plotly
- **Database:** SQLite
- **Version Control:** Git & GitHub

---

## ⚙️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/sreeharib92-creator/AI-Powered-Customer-Support-Ticket-Intelligence-System.git](https://github.com/sreeharib92-creator/AI-Powered-Customer-Support-Ticket-Intelligence-System.git)
   cd AI-Powered-Customer-Support-Ticket-Intelligence-System
   ```
**Install Dependencies:**
```bash
pip install streamlit pandas plotly scikit-learn
```
**Run the Streamlit Application:**
```bash
python -m streamlit run app.py
```
