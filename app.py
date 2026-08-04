import streamlit as st
import json
from app.interview_manager import InterviewManager

# --- Initialization ---
def initialize_session_state():
    """Initializes all necessary session state variables safely."""
    defaults = {
        "candidate_name": "",
        "role": "",
        "skills": [],
        "difficulty": "Intermediate",
        "manager": None,
        "questions": [],
        "answers": [],
        "evaluations": [],
        "report": None,
        "current_question": 0,
        "interview_started": False,
        "interview_completed": False,
        "answer_submitted": False,
        "current_answer": "",
        "processing": False,
        "history_loaded": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    if st.session_state.manager is None:
        st.session_state.manager = InterviewManager()

# Call immediately
initialize_session_state()

# Page Configuration
st.set_page_config(
    page_title="AI Interview Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def reset_interview():
    """Resets the interview session."""
    st.session_state.candidate_name = ""
    st.session_state.role = ""
    st.session_state.skills = []
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.evaluations = []
    st.session_state.report = None
    st.session_state.interview_started = False
    st.session_state.interview_completed = False
    st.session_state.current_question = 0
    st.session_state.manager = InterviewManager()
    st.rerun()

# --- Sidebar ---
with st.sidebar:
    st.title("🤖 AI Interview Agent")
    st.markdown("---")
    nav = st.radio("Navigation", ["Interview", "History"], format_func=lambda x: f"🚀 {x}" if x=="Interview" else f"📜 {x}")
    st.markdown("---")
    
    status_map = {"Not Started": "⚪", "In Progress": "🟡", "Completed": "🟢"}
    status = "Not Started"
    if st.session_state.interview_started: status = "In Progress"
    if st.session_state.interview_completed: status = "Completed"
    st.write(f"**Status:** {status_map[status]} {status}")
    
    if st.button("🔄 Reset Interview", use_container_width=True):
        reset_interview()

def handle_api_error(e):
    """Handles API errors and shows user-friendly messages."""
    from app.exceptions import GeminiError
    if isinstance(e, GeminiError) and str(e) == "RESOURCE_EXHAUSTED":
        st.error("Gemini API quota has been exceeded. Please try again later or configure a new API key.")
    else:
        st.error(f"❌ Error: {e}")

def render_history():
    st.title("📜 Interview History")
    db = st.session_state.manager.db
    col_search, _ = st.columns([3, 1])
    search = col_search.text_input("🔍 Search Candidate Name...", "")
    interviews = db.get_all_interviews()
    if search:
        interviews = [i for i in interviews if search.lower() in i['candidate_name'].lower()]
    if not interviews:
        st.info("No interviews found.")
        return
    for i in interviews:
        with st.expander(f"{i['created_at']} | {i['candidate_name']} ({i['role']})"):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Score", f"{i['percentage']}%")
            c2.metric("Rec", i['recommendation'])
            if c3.button("👁️ View", key=f"view_{i['id']}", use_container_width=True):
                details = db.get_interview(i['id'])
                st.json(details)
            if c4.button("🗑️ Delete", key=f"del_{i['id']}", type="primary", use_container_width=True):
                db.delete_interview(i['id'])
                st.success("Interview deleted.")
                st.rerun()

def render_results():
    report = st.session_state.report
    st.title("🏆 Interview Results")
    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Score", f"{report['summary']['total_score']}/50")
    col2.metric("Percentage", f"{report['summary']['percentage']}%")
    col3.metric("Recommendation", report['overall_feedback']['recommendation'])
    st.markdown("---")
    st.subheader("🤖 AI Hiring Decision")
    c_h1, c_h2, c_h3 = st.columns(3)
    c_h1.metric("Hiring Decision", report['overall_feedback']['hiring_decision'])
    c_h2.metric("Fit Score", f"{report['overall_feedback']['fit_score']}/100")
    c_h3.metric("Salary Rec", report['overall_feedback']['salary_recommendation'])
    with st.expander("📝 Interviewer Final Notes"):
        st.info(report['overall_feedback']['final_notes'])
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.write(f"**👤 Candidate:** {report['candidate_name']}")
    c1.write(f"**💼 Role:** {report['role']}")
    c2.write(f"**🛠️ Skills:** {', '.join(report['skills'])}")
    c2.write(f"**🎯 Confidence:** {report['overall_feedback']['confidence']}")
    st.markdown("---")
    s1, s2 = st.columns(2)
    s1.write(f"**✅ Strengths:** {', '.join(report['overall_feedback']['strengths'])}")
    s2.write(f"**⚠️ Areas for Improvement:** {', '.join(report['overall_feedback']['areas_for_improvement'])}")
    with st.expander("📝 View Final Feedback", expanded=True):
        st.info(report['overall_feedback']['final_feedback'])
    st.subheader("🔍 Question Breakdown")
    for i, q in enumerate(report['questions']):
        with st.expander(f"Q{i+1}: {q['question'][:50]}... (Score: {q['score']}/10)"):
            st.write(f"**Your Answer:** {q['answer']}")
            st.write(f"**Ideal Answer:** {q['ideal_answer']}")
            st.write(f"**Feedback:** {q['feedback']}")
            c_s, c_w = st.columns(2)
            c_s.write(f"**Strengths:** {', '.join(q['strengths'])}")
            c_w.write(f"**Weaknesses:** {', '.join(q['weaknesses'])}")
    st.markdown("---")
    col_dl, col_reset = st.columns([1, 1])
    col_dl.download_button("💾 Download Report (JSON)", json.dumps(report, indent=2), "interview_report.json", "application/json", use_container_width=True)
    if col_reset.button("✨ Start New Interview", use_container_width=True):
        reset_interview()

def render_interview():
    if not st.session_state.interview_started:
        st.title("👋 Welcome to the AI Interview Agent")
        st.markdown("This system provides a structured, AI-driven technical interview experience.")
        with st.form("candidate_form", clear_on_submit=False):
            st.subheader("Candidate Details")
            name = st.text_input("Candidate Name", value=st.session_state.candidate_name, placeholder="e.g. John Doe")
            role = st.text_input("Target Role", value=st.session_state.role, placeholder="e.g. Senior Python Developer")
            skills = st.text_input("Skills (comma separated)", value=", ".join(st.session_state.skills), placeholder="e.g. Python, Django, Docker")
            difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"], index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.difficulty))
            submit = st.form_submit_button("🚀 Start Interview", use_container_width=True)
            if submit:
                if not all([name, role, skills]):
                    st.error("⚠️ Please fill in all fields.")
                else:
                    st.session_state.candidate_name = name
                    st.session_state.role = role
                    st.session_state.skills = [s.strip() for s in skills.split(",")]
                    st.session_state.difficulty = difficulty
                    with st.spinner("🧠 Generating your questions..."):
                        try:
                            st.session_state.manager.start_interview(name, role, st.session_state.skills)
                            st.session_state.questions = st.session_state.manager.questions
                            st.session_state.interview_started = True
                            st.rerun()
                        except Exception as e:
                            handle_api_error(e)
    elif not st.session_state.interview_completed:
        idx = st.session_state.current_question
        st.title(f"Q{idx + 1}: Question of 5")
        st.progress((idx) / 5)
        st.subheader(st.session_state.questions[idx])
        answer = st.text_area("Your Answer", height=200, key=f"ans_{idx}", placeholder="Type your answer here...")
        st.caption(f"Characters: {len(answer)}")
        if st.button("✅ Submit Answer", use_container_width=True):
            if not answer.strip():
                st.error("⚠️ Please provide an answer.")
            else:
                st.session_state.manager.submit_answer(st.session_state.questions[idx], answer)
                st.session_state.answers.append(answer)
                if idx < 4:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.session_state.interview_completed = True
                    st.rerun()
    elif not st.session_state.report:
        st.title("⏳ Processing Interview Results")
        with st.spinner("Evaluating your performance..."):
            try:
                st.session_state.report = st.session_state.manager.generate_report()
                st.rerun()
            except Exception as e:
                handle_api_error(e)
                if st.button("Retry"):
                    st.rerun()
    else:
        render_results()

def main():
    if nav == "History":
        render_history()
    else:
        render_interview()

if __name__ == "__main__":
    main()
