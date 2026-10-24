# 🎫 AI-Powered Customer Support Ticket Intelligence System

An intelligent customer support application designed to automate ticket classification, analyze customer sentiment, recommend ticket priorities, and generate auto-responses using Natural Language Processing (NLP), Machine Learning, and an interactive Streamlit dashboard.

---

## 🚀 Features

- **Automated Ticket Classification:** Categorizes customer complaints into Billing, Technical Issues, Account Access, Refund Requests, and Product Complaints using TF-IDF and Machine Learning.
- **Sentiment Analysis:** Identifies customer sentiment (Positive, Neutral, Negative) to gauge customer mood.
- **Priority Recommendation:** Recommends ticket priority (High, Medium, Low) based on sentiment, category, and urgency rules.
- **Suggested Responses:** Generates draft responses for support agents using predefined templates.
- **Interactive Dashboard (Streamlit):** Visualizes trends with Plotly charts, key metrics, search filters, and CSV report downloads.
- **Database Integration (SQLite):** Persists ticket records, allowing agents to add new tickets and update ticket statuses (`Pending`, `In Progress`, `Resolved`, `Closed`).

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

## 📁 Project Structure

```text
AI-Powered-Customer-Support-Ticket-Intelligence-System/
│
├── app.py                             # Main Streamlit Dashboard application
├── tickets_database.db                # SQLite database storing ticket records
├── ticket_responses_results.csv       # Processed dataset with responses
├── ticket_priority_results.csv        # Processed dataset with priority analysis
├── AI-powered_customer_support_ticket_intelligence_system (1).ipynb # Data preprocessing & pipeline notebook
├── SENTIMENTAL_ANALYSISMODULE_3.ipynb # Sentiment analysis module notebook
├── TICKET_PRIORITY_RECOMMENDATION_MODULE_4.ipynb # Priority recommendation module
└── SUGGESTED_RESPONSES_MODULE_5.ipynb # Suggested responses generation module

---

## ⚙️ Installation & Setup

Markdown
1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/sreeharib92-creator/AI-Powered-Customer-Support-Ticket-Intelligence-System.git](https://github.com/sreeharib92-creator/AI-Powered-Customer-Support-Ticket-Intelligence-System.git)
   cd AI-Powered-Customer-Support-Ticket-Intelligence-System

Install Dependencies:

Bash

pip install streamlit pandas plotly scikit-learn
Run the Streamlit Application:

Bash

python -m streamlit run app.py
