
import re
import sqlite3
from pathlib import Path
from datetime import datetime, date

import pandas as pd
import streamlit as st
from dateparser.search import search_dates

# ================= CONFIGURATION =================
st.set_page_config(
    page_title="TextRescue | Smart Text Analytics",
    page_icon="🛟",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "textrescue.db"


# ================= PROFESSIONAL LIGHT THEME =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    color-scheme: light;
    --navy: #102A43;
    --blue: #0F62FE;
    --background: #F4F7FB;
    --white: #FFFFFF;
    --text: #243B53;
    --muted: #52677D;
    --border: #CBD5E1;
}

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background-color: #F4F7FB !important;
    color: #243B53 !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] .main .block-container {
    max-width: 1400px;
    padding: 2rem 2.5rem 3rem;
}

/* Headings and normal text */
h1, h2, h3, h4, h5, h6 {
    color: #102A43 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 750 !important;
}

p, li, label, small,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {
    color: #243B53 !important;
}

.tr-label {
    color: #0F62FE !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}

.tr-subtitle {
    color: #52677D !important;
    font-size: 15px;
    margin-bottom: 20px;
}

.tr-line {
    width: 65px;
    height: 4px;
    background: #0F62FE;
    border-radius: 5px;
    margin: 8px 0 16px;
}

/* Dashboard metric cards */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 3px 10px rgba(16,42,67,0.04);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #102A43 !important;
}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #F4F7FB !important;
    gap: 10px;
    border-bottom: 1px solid #CBD5E1;
}

[data-testid="stTabs"] button[role="tab"],
[data-testid="stTabs"] button[role="tab"] * {
    color: #243B53 !important;
    background: transparent !important;
    font-weight: 650 !important;
    opacity: 1 !important;
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] * {
    color: #0F62FE !important;
}

/* Message input */
[data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    color: #243B53 !important;
    -webkit-text-fill-color: #243B53 !important;
    caret-color: #0F62FE !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    opacity: 1 !important;
}

[data-testid="stTextArea"] textarea::placeholder {
    color: #52677D !important;
    -webkit-text-fill-color: #52677D !important;
    opacity: 1 !important;
}

[data-testid="stTextArea"] label,
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stCheckbox"] label {
    color: #243B53 !important;
    font-weight: 600 !important;
}

/* Text inputs */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    background: #FFFFFF !important;
    color: #243B53 !important;
    -webkit-text-fill-color: #243B53 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 9px !important;
}

/* Dropdowns */
[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #243B53 !important;
    border-color: #CBD5E1 !important;
}

[data-baseweb="select"] *,
[data-baseweb="select"] span {
    color: #243B53 !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"],
[role="option"] {
    background: #FFFFFF !important;
    color: #243B53 !important;
}

[role="option"] * {
    color: #243B53 !important;
}

/* Buttons */
.stButton > button,
[data-testid="stDownloadButton"] button {
    border-radius: 9px !important;
    font-weight: 700 !important;
    min-height: 42px;
    background: #FFFFFF !important;
    color: #0F62FE !important;
    border: 1px solid #C1D5F8 !important;
}

.stButton > button[kind="primary"] {
    background: #0F62FE !important;
    color: #FFFFFF !important;
    border-color: #0F62FE !important;
}

.stButton > button[kind="primary"] * {
    color: #FFFFFF !important;
}

/* Tables */
[data-testid="stDataFrame"],
[data-testid="stDataEditor"] {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* Streamlit data tables use an internal grid renderer */
[data-testid="stDataFrame"] iframe {
    background: #FFFFFF !important;
}

/* Checkboxes and radio labels */
[data-testid="stCheckbox"] *,
[data-testid="stRadio"] *,
[data-testid="stToggle"] * {
    color: #243B53 !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #243B53 !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 10px !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: #243B53 !important;
}

/* General layout */
hr {
    border-color: #CBD5E1 !important;
}

[data-testid="stHeader"] {
    background: #F4F7FB !important;
}

#MainMenu, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ================= DATABASE =================
def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            deadline TEXT,
            category TEXT,
            priority TEXT,
            source_text TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT
        )
    """)
    conn.commit()
    return conn


def add_task(task, deadline, category, priority, source):
    with connect_db() as conn:
        conn.execute("""
            INSERT INTO tasks
            (task, deadline, category, priority,
             source_text, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'Pending', ?)
        """, (
            task, deadline, category, priority, source,
            datetime.now().isoformat(timespec="seconds")
        ))


def get_tasks():
    with connect_db() as conn:
        return pd.read_sql_query("""
            SELECT * FROM tasks
            ORDER BY
                CASE WHEN deadline IS NULL OR deadline = ''
                     THEN 1 ELSE 0 END,
                deadline ASC, id DESC
        """, conn)


def update_status(task_id, status):
    with connect_db() as conn:
        conn.execute(
            "UPDATE tasks SET status=? WHERE id=?",
            (status, int(task_id))
        )


def delete_task(task_id):
    with connect_db() as conn:
        conn.execute(
            "DELETE FROM tasks WHERE id=?",
            (int(task_id),)
        )


# ================= TEXT ANALYSIS =================
TASK_VERBS = (
    "submit", "complete", "finish", "upload", "register",
    "attend", "pay", "bring", "prepare", "send", "review",
    "apply", "report", "collect", "present", "join", "fill",
    "confirm", "respond", "return", "read", "study", "revise",
    "download", "print", "book", "renew"
)

EVENT_WORDS = (
    "exam", "examination", "meeting", "workshop", "interview",
    "presentation", "class", "event", "webinar", "appointment",
    "test", "deadline", "assignment", "submission"
)

HIGH_WORDS = (
    "urgent", "immediately", "asap", "last date", "final date",
    "mandatory", "compulsory", "without fail",
    "as soon as possible"
)

MEDIUM_WORDS = (
    "please", "should", "required", "remember", "upcoming", "due"
)


def split_sentences(text):
    parts = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [
        part.strip(" \t•-")
        for part in parts if part.strip(" \t•-")
    ]


def find_date(sentence):
    try:
        matches = search_dates(
            sentence,
            settings={
                "RELATIVE_BASE": datetime.now(),
                "PREFER_DATES_FROM": "future",
                "RETURN_AS_TIMEZONE_AWARE": False
            }
        )
        if matches:
            expression, parsed = matches[0]
            return parsed.date().isoformat(), expression
    except Exception:
        pass

    return None, None


def classify_category(sentence):
    text = sentence.lower()

    if any(w in text for w in (
        "exam", "examination", "test", "quiz"
    )):
        return "Exam"

    if any(w in text for w in (
        "assignment", "homework", "project", "submit", "upload"
    )):
        return "Assignment"

    if any(w in text for w in (
        "meeting", "workshop", "webinar", "interview",
        "appointment", "event", "presentation"
    )):
        return "Event"

    if any(w in text for w in ("pay", "payment", "fee", "bill")):
        return "Payment"

    if any(w in text for w in (
        "register", "registration", "apply"
    )):
        return "Registration"

    if any(w in text for w in TASK_VERBS):
        return "Task"

    return "Announcement"


def classify_priority(sentence, deadline):
    text = sentence.lower()

    if any(w in text for w in HIGH_WORDS):
        return "High"

    if deadline:
        try:
            days_left = (
                date.fromisoformat(deadline) - date.today()
            ).days

            if days_left <= 2:
                return "High"
            if days_left <= 7:
                return "Medium"
        except ValueError:
            pass

    if any(w in text for w in (
        "exam", "examination", "assignment", "submission",
        "interview", "registration", "workshop", "presentation"
    )):
        return "Medium"

    if any(w in text for w in MEDIUM_WORDS):
        return "Medium"

    if any(w in text for w in TASK_VERBS):
        return "Medium"

    return "Low"


def extract_tasks(text):
    results = []

    for sentence in split_sentences(text):
        deadline, date_phrase = find_date(sentence)
        low = sentence.lower()

        has_task = any(w in low for w in TASK_VERBS)
        has_event = any(w in low for w in EVENT_WORDS)
        has_deadline = any(w in low for w in (
            "deadline", "due", "before", "until",
            "last date", "by "
        ))

        if not (has_task or has_event or deadline or has_deadline):
            continue

        results.append({
            "Task / Important Information": sentence,
            "Deadline": deadline or "Not detected",
            "Detected Date Phrase": date_phrase or "—",
            "Category": classify_category(sentence),
            "Priority": classify_priority(sentence, deadline),
            "Save": True
        })

    return results


# ================= HEADER =================
st.markdown(
    '<div class="tr-label">SMART TEXT ANALYTICS</div>',
    unsafe_allow_html=True
)
st.title("TextRescue")
st.markdown('<div class="tr-line"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="tr-subtitle">'
    'Important Message and Deadline Detector · '
    'Convert announcements into actionable tasks.'
    '</div>',
    unsafe_allow_html=True
)

with st.expander("About TextRescue"):
    st.write(
        "TextRescue uses date parsing and keyword rules to identify "
        "potentially important tasks and deadlines. Verify extracted "
        "information before acting on it."
    )


# ================= METRICS =================
tasks_df = get_tasks()
today = date.today().isoformat()

total = len(tasks_df)
pending = int((tasks_df["status"] == "Pending").sum()) if total else 0
completed = int((tasks_df["status"] == "Completed").sum()) if total else 0

overdue = 0
if total:
    overdue = int((
        tasks_df["deadline"].notna()
        & (tasks_df["deadline"] != "")
        & (tasks_df["deadline"] < today)
        & (tasks_df["status"] == "Pending")
    ).sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Tasks", total)
c2.metric("Pending", pending)
c3.metric("Completed", completed)
c4.metric("Overdue", overdue)

tab_analyze, tab_tasks, tab_about = st.tabs([
    "Analyze Message", "My Tasks", "About"
])


# ================= ANALYZE MESSAGE =================
with tab_analyze:
    st.subheader("Message Analyzer")
    st.write("Paste a message, college announcement, email, or notice.")

    sample = (
        "Dear students, submit your DBMS assignment before 18/10/2026. "
        "The internal examination will be held on October 22, 2026. "
        "Register for the workshop by October 15, 2026. This is mandatory."
    )

    message = st.text_area(
        "Announcement Text",
        value=sample,
        height=160,
        placeholder="Paste your message here..."
    )

    if st.button("Analyze Message", type="primary"):
        if not message.strip():
            st.warning("Please enter a message first.")
        else:
            st.session_state["analysis_results"] = extract_tasks(message)
            st.session_state["analysis_source"] = message

    if "analysis_results" in st.session_state:
        results = st.session_state["analysis_results"]

        if results:
            st.success(
                f"Found {len(results)} potentially important item(s). "
                "Review the results before saving."
            )

            edited = st.data_editor(
                pd.DataFrame(results),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Save": st.column_config.CheckboxColumn(
                        "Save Task", default=True
                    ),
                    "Priority": st.column_config.SelectboxColumn(
                        "Priority",
                        options=["High", "Medium", "Low"],
                        required=True
                    ),
                    "Category": st.column_config.SelectboxColumn(
                        "Category",
                        options=[
                            "Assignment", "Exam", "Event", "Payment",
                            "Registration", "Task", "Announcement"
                        ],
                        required=True
                    )
                },
                disabled=[
                    "Task / Important Information",
                    "Deadline",
                    "Detected Date Phrase"
                ],
                key="results_editor"
            )

            if st.button("Save Selected Tasks"):
                saved = 0

                for _, row in edited.iterrows():
                    if bool(row["Save"]):
                        deadline_value = row["Deadline"]

                        if deadline_value == "Not detected":
                            deadline_value = None

                        add_task(
                            str(row["Task / Important Information"]),
                            deadline_value,
                            str(row["Category"]),
                            str(row["Priority"]),
                            st.session_state.get("analysis_source", "")
                        )
                        saved += 1

                st.success(f"Saved {saved} task(s) successfully.")
                st.rerun()
        else:
            st.info(
                "No important items detected. Try words such as submit, "
                "register, exam, deadline, or include a date."
            )


# ================= MY TASKS =================
with tab_tasks:
    st.subheader("Task Management")
    df = get_tasks()

    if df.empty:
        st.info("No saved tasks yet. Analyze a message and save tasks first.")
    else:
        status_filter = st.selectbox(
            "Filter Tasks", ["All", "Pending", "Completed"]
        )

        view = df if status_filter == "All" else df[
            df["status"] == status_filter
        ]

        display = view[
            ["id", "task", "deadline", "category", "priority", "status"]
        ].copy()

        display.columns = [
            "ID", "Task / Information", "Deadline",
            "Category", "Priority", "Status"
        ]

        st.dataframe(display, use_container_width=True, hide_index=True)

        st.markdown("#### Update a Task")
        ids = view["id"].astype(int).tolist()

        if ids:
            selected_id = st.selectbox("Select Task ID", ids)
            selected = view[view["id"] == selected_id].iloc[0]

            new_status = st.selectbox(
                "Task Status",
                ["Pending", "Completed"],
                index=0 if selected["status"] == "Pending" else 1
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Update Status"):
                    update_status(selected_id, new_status)
                    st.success("Task status updated.")
                    st.rerun()

            with col2:
                if st.button("Delete Task"):
                    delete_task(selected_id)
                    st.success("Task deleted.")
                    st.rerun()

        st.download_button(
            "Download Tasks as CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="textrescue_tasks.csv",
            mime="text/csv"
        )


# ================= ABOUT =================
with tab_about:
    st.subheader("About the Project")

    st.markdown("""
    **Aim**

    Analyze text messages and announcements to extract important tasks,
    dates, deadlines, and reminders.

    **Workflow**

    1. User enters an announcement.
    2. The text is divided into sentences.
    3. Date parsing and keyword rules identify important information.
    4. Each item receives a category and priority.
    5. The user reviews and saves selected tasks.
    6. Tasks are stored in SQLite and can be tracked.

    **Technology Stack**

    - Python
    - Streamlit
    - dateparser
    - Pandas
    - SQLite
    - Regular expressions

    **Limitations**

    This prototype uses rule-based extraction, not a trained AI model.
    It may miss indirect instructions or misinterpret ambiguous dates.
    Users should verify extracted details.

    **Future Enhancements**

    - Advanced NLP models
    - PDF notice analysis
    - Email integration
    - Calendar synchronization
    - Automated reminders
    """)
