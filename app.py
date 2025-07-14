import streamlit as st
import time

st.set_page_config(page_title="Escape Room Quiz", layout="centered")
st.title("🔐 Clinical Escape Room Challenge")

# Questions and answers
questions = [
    {
        "question": "How higher is the risk of systemic ADRs with IVIG vs SCIG?",
        "options": [
            "Approximately 7-fold higher",
            "Approximately 10-fold higher",
            "Approximately 14-fold higher",
            "The difference is minimal"
        ],
        "answer": "Approximately 10-fold higher"
    },
    {
        "question": "Which group of patients is the biggest IGG consumer among PID?",
        "options": [
            "XLA (Bruton's disease) in pediatrics",
            "CVID in adults",
            "Hyper M syndrome + SCID (all ages)",
            "Hyper E syndrome (all ages)"
        ],
        "answer": "CVID in adults"
    },
    {
        "question": "Which preparation is most commonly used for fluid replacement in PLEX?",
        "options": [
            "FFP",
            "OctaplasLG",
            "Albumin",
            "Gelatin"
        ],
        "answer": "Albumin"
    },
    {
        "question": "Where is anticoagulant reversal needed most frequently?",
        "options": [
            "Trauma",
            "Liver surgery",
            "Intracranial hemorrhage",
            "Cardiac surgery"
        ],
        "answer": "Intracranial hemorrhage"
    },
    {
        "question": "Which specialty is number 1 in antithrombin consumption?",
        "options": [
            "Obstetrics",
            "Hematology",
            "Cardiac surgery",
            "Trauma and orthopedics"
        ],
        "answer": "Cardiac surgery"
    }
]

# Initialize session state
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'delay' not in st.session_state:
    st.session_state.delay = 0
if 'info_text' not in st.session_state:
    st.session_state.info_text = ""

# Helper: countdown display and blocking input
def countdown(seconds):
    # show stored info message
    if st.session_state.info_text:
        st.markdown(st.session_state.info_text)
    placeholder = st.empty()
    progress = st.progress(0)
    for i in range(seconds, 0, -1):
        placeholder.markdown(f"<h1 style='text-align:center'>⏳ Please wait <strong>{i}</strong> seconds...</h1>", unsafe_allow_html=True)
        progress.progress((seconds - i + 1) / seconds)
        time.sleep(1)
    placeholder.empty()
    progress.empty()
    # clear info and delay
    st.session_state.info_text = ""
    st.session_state.delay = 0
    st.rerun()

# Determine if input should be disabled
locked = st.session_state.delay > 0

# Display current question
current_q = questions[st.session_state.question_index]
st.subheader(f"Q{st.session_state.question_index+1}: {current_q['question']}")
choice = st.radio("", current_q['options'], key=f"q{st.session_state.question_index}", disabled=locked)

# Submit button (disabled during countdown)
submitted = st.button("Submit Answer", disabled=locked)

if submitted and not locked:
    if choice == current_q['answer']:
        st.success("✅ Correct answer!")
        st.session_state.attempts = 0
        st.session_state.info_text = ""
        time.sleep(5)
        if st.session_state.question_index + 1 < len(questions):
            st.session_state.question_index += 1
            st.rerun()
        else:
            st.balloons()
            st.success("🎉 All questions completed! Your code is: ESCAPE-2471")
    else:
        # First incorrect attempt
        if st.session_state.attempts == 0:
            st.session_state.info_text = "❌ Incorrect answer – you can try again after 45 seconds"
            st.session_state.attempts += 1
            st.session_state.delay = 45
            st.rerun()
        # Second incorrect attempt
        elif st.session_state.attempts == 1:
            st.session_state.info_text = "❌ Incorrect answer"
            st.session_state.attempts = 0
            # show correct answer message permanently during countdown
            st.session_state.info_text += f"\n✅ Correct answer is: **{current_q['answer']}**"
            st.session_state.delay = 45
            st.rerun()

# If delay active, show countdown and block input
if locked:
    countdown(st.session_state.delay)
