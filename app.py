import sqlite3
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# Page layout setup
st.set_page_config(
    page_title="AI Customer Support Dashboard", page_icon="🎫", layout="wide"
)

# ---------------------------------------------------------
# DATABASE & DATA LOADING (Module 7 Integration)
# ---------------------------------------------------------
DB_FILE = "tickets_database.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            complaint TEXT,
            category TEXT,
            sentiment TEXT,
            suggested_priority TEXT,
            suggested_response TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)
    conn.commit()

    # Check if 'status' column exists in existing DB, if not add it
    cursor.execute("PRAGMA table_info(tickets)")
    columns = [column[1] for column in cursor.fetchall()]
    if "status" not in columns:
        cursor.execute(
            "ALTER TABLE tickets ADD COLUMN status TEXT DEFAULT 'Pending'"
        )
        conn.commit()

    conn.close()


def load_data_to_db(df):
    conn = sqlite3.connect(DB_FILE)

    if "status" not in df.columns:
        df["status"] = "Pending"

    try:
        existing_df = pd.read_sql_query(
            "SELECT ticket_id, status FROM tickets", conn
        )
    except Exception:
        existing_df = pd.DataFrame(columns=["ticket_id", "status"])

    df.to_sql("tickets", conn, if_exists="replace", index=False)

    if not existing_df.empty and "ticket_id" in existing_df.columns:
        for _, row in existing_df.iterrows():
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tickets SET status = ? WHERE ticket_id = ?",
                (row["status"], row["ticket_id"]),
            )
            conn.commit()
    conn.close()


def fetch_data_from_db():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM tickets", conn)
    conn.close()
    return df


init_db()

# Check for processed CSV files
results_file = Path("ticket_responses_results.csv")
if not results_file.exists():
    results_file = Path("ticket_priority_results.csv")

if results_file.exists():
    df_file = pd.read_csv(results_file)
    if "text" in df_file.columns and "complaint" not in df_file.columns:
        df_file = df_file.rename(columns={"text": "complaint"})
    if "pred_sentiment" in df_file.columns and "sentiment" not in df_file.columns:
        df_file = df_file.rename(columns={"pred_sentiment": "sentiment"})
    load_data_to_db(df_file)

df = fetch_data_from_db()

# ---------------------------------------------------------
# MODULE 6 & 7: Streamlit Web Dashboard UI
# ---------------------------------------------------------
st.title("🎫 AI-Powered Customer Support Intelligence Dashboard")
st.markdown(
    "Automated Ticket Classification, Sentiment Analysis, Priority Recommendation & Auto-Responses"
)
st.divider()

# SIDEBAR: Actions & Management
st.sidebar.header("🛠️ Actions & Management")

# 1. Add New Ticket Form
with st.sidebar.expander("➕ Add New Ticket"):
    with st.form("new_ticket_form"):
        new_id = st.text_input("Ticket ID", value=f"TICK-{len(df)+1:03d}")
        new_complaint = st.text_area("Customer Complaint")
        new_category = st.selectbox(
            "Category",
            [
                "Billing and Payments",
                "Account Access",
                "Product or Service Complaints",
                "Refund Requests",
                "Technical Issues",
            ],
        )
        new_sentiment = st.selectbox(
            "Sentiment", ["Positive", "Neutral", "Negative"]
        )
        new_priority = st.selectbox(
            "Suggested Priority", ["High", "Medium", "Low"]
        )
        new_response = st.text_area(
            "Suggested Response",
            value="Hello, we have received your request and are looking into it.",
        )
        new_status = st.selectbox("Status", ["Pending", "In Progress", "Resolved"])

        submit_button = st.form_submit_button(label="Save Ticket to DB")

        if submit_button:
            if new_complaint:
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO tickets (ticket_id, complaint, category, sentiment, suggested_priority, suggested_response, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        new_id,
                        new_complaint,
                        new_category,
                        new_sentiment,
                        new_priority,
                        new_response,
                        new_status,
                    ),
                )
                conn.commit()
                conn.close()
                st.success("New ticket added successfully!")
                st.rerun()
            else:
                st.warning("Please enter the complaint text.")

# 2. Update Ticket Status Form
with st.sidebar.expander("🔄 Update Ticket Status"):
    with st.form("update_status_form"):
        ticket_ids = (
            df["ticket_id"].tolist() if "ticket_id" in df.columns else []
        )
        selected_ticket = st.selectbox("Select Ticket ID", ticket_ids)
        updated_status = st.selectbox(
            "New Status", ["Pending", "In Progress", "Resolved", "Closed"]
        )

        update_button = st.form_submit_button(label="Update Status in DB")

        if update_button and selected_ticket:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tickets SET status = ? WHERE ticket_id = ?",
                (updated_status, selected_ticket),
            )
            conn.commit()
            conn.close()
            st.success(
                f"Ticket {selected_ticket} status updated to {updated_status}!"
            )
            st.rerun()

if df.empty:
    st.warning(
        "No data found! Please make sure your previous module CSV files are in the folder."
    )
else:
    # Search Filter definition
    st.subheader("📋 Ticket Details & Suggested Responses")
    col_search, col_download = st.columns([3, 1])
    with col_search:
        search_term = st.text_input(
            "🔍 Search Ticket by Complaint Keyword or ID:"
        )

    if search_term:
        filtered_df = df[
            df.astype(str)
            .apply(lambda row: row.str.contains(search_term, case=False))
            .any(axis=1)
        ]
    else:
        filtered_df = df

    with col_download:
        st.write("")
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="ticket_reports.csv",
            mime="text/csv",
        )

    # Format table headers to Capitalized Title Case for display
    display_df = filtered_df.copy()
    display_df.columns = [
        col.replace("_", " ").title() for col in display_df.columns
    ]
    st.dataframe(display_df, use_container_width=True)

    st.divider()

    # 1. TOP METRICS (Using filtered_df securely)
    st.subheader("📊 Dashboard Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tickets", len(filtered_df))
    with col2:
        high_prio = (
            len(
                filtered_df[
                    filtered_df["suggested_priority"].str.lower() == "high"
                ]
            )
            if "suggested_priority" in filtered_df.columns
            else 0
        )
        st.metric("High Priority", high_prio)
    with col3:
        neg_sent = (
            len(filtered_df[filtered_df["sentiment"].str.lower() == "negative"])
            if "sentiment" in filtered_df.columns
            else 0
        )
        st.metric("Negative Sentiment", neg_sent)
    with col4:
        categories_count = (
            filtered_df["category"].nunique()
            if "category" in filtered_df.columns
            else 0
        )
        st.metric("Categories", categories_count)

    st.divider()

    # 2. CHARTS & VISUALIZATIONS
    c1, c2 = st.columns(2)

    with c1:
        if "suggested_priority" in filtered_df.columns:
            prio_counts = (
                filtered_df["suggested_priority"].value_counts().reset_index()
            )
            prio_counts.columns = ["Priority", "Count"]
            fig_prio = px.pie(
                prio_counts,
                names="Priority",
                values="Count",
                title="Ticket Priority Distribution",
                color="Priority",
                color_discrete_map={
                    "High": "#e5484d",
                    "Medium": "#f0f921",
                    "Low": "#30a46c",
                },
            )
            st.plotly_chart(fig_prio, use_container_width=True)

    with c2:
        if "category" in filtered_df.columns:
            cat_counts = (
                filtered_df["category"].value_counts().reset_index()
            )
            cat_counts.columns = ["Category", "Count"]
            fig_cat = px.bar(
                cat_counts,
                x="Category",
                y="Count",
                title="Tickets by Category",
                color="Category",
            )
            st.plotly_chart(fig_cat, use_container_width=True)

    st.divider()

    # 4. DECISION SUPPORT DISCLAIMER
    st.info(
        "ℹ️ **Decision Support Notice:** All AI predictions, classifications, and priority recommendations are intended for decision-support purposes only and should be verified by support agents."
    )