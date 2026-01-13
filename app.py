import streamlit as st
import time
from src.interviewer.logic import Interviewer
from src.ui.components import render_chat_bubble, apply_custom_css

# Initialize modular interviewer
if "interviewer" not in st.session_state:
    st.session_state.interviewer = Interviewer()

st.set_page_config(page_title="TalentScout Pro", page_icon="💼", layout="centered")
apply_custom_css()

# --- HEADER SECTION ---
st.markdown("""
    <div style="text-align: center; padding: 20px 0; margin-bottom: 30px; border-bottom: 1px solid #334155;">
        <h1 style="margin: 0; color: #F8FAFC; font-size: 2.5rem; letter-spacing: -1px;">TalentScout <span style="color: #38BDF8;">Pro</span></h1>
        <p style="margin: 5px 0 0 0; color: #94A3B8; font-size: 1.1rem;">AI-Powered Technical Assessment Platform</p>
    </div>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Welcome to TalentScout Pro. I am your Hiring Assistant for today. We aim to make our screening process as smooth and professional as possible. Shall we begin with your background?"}
    ]
if "stage" not in st.session_state:
    st.session_state.stage = "collecting"
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {}
if "questions" not in st.session_state:
    st.session_state.questions = []
if "q_idx" not in st.session_state:
    st.session_state.q_idx = 0

# --- HELPERS ---
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- UI RENDERING (Chat Container) ---
chat_container = st.container()

# Draw existing history inside the container
with chat_container:
    for msg in st.session_state.messages:
        render_chat_bubble(msg["role"].capitalize(), msg["content"])

# --- INPUT HANDLING ---
user_input = st.chat_input("Enter your response here...")

if user_input:
    # 1. Immediately show user's message locally
    add_message("user", user_input)
    # Rerunning to update the history in the loop above
    
    # 2. Process logic
    with st.spinner("Processing..."):
        if st.session_state.stage == "collecting":
            st.session_state.candidate_data = st.session_state.interviewer.extract_info(
                user_input, 
                st.session_state.candidate_data
            )
            status, response = st.session_state.interviewer.get_conversation_response(
                st.session_state.messages,
                st.session_state.candidate_data
            )
            
            if status == "DONE":
                st.session_state.stage = "preparing_tech"
                add_message("bot", response)
                
                # Fetch questions
                st.session_state.questions = st.session_state.interviewer.get_technical_questions(
                    st.session_state.candidate_data.get("tech_stack", "")
                )
                if st.session_state.questions:
                    st.session_state.stage = "interviewing"
                    first_q = f"Excellent stack. Let's dive into some technical specifics:\n\n**{st.session_state.questions[0]}**"
                    add_message("bot", first_q)
                else:
                    st.session_state.stage = "collecting" # Fallback
                    add_message("bot", "I need a bit more detail about your tech stack to generate relevant questions. Could you elaborate on what tools you use daily?")
            else:
                add_message("bot", response)

        elif st.session_state.stage == "interviewing":
            q_idx = st.session_state.q_idx
            st.session_state.candidate_data[f"answer_{q_idx}"] = user_input
            
            if q_idx < len(st.session_state.questions) - 1:
                st.session_state.q_idx += 1
                next_q = st.session_state.questions[st.session_state.q_idx]
                add_message("bot", f"Understood. Moving on:\n\n**{next_q}**")
            else:
                st.session_state.stage = "finished"
                add_message("bot", "Perfect. I have all the data required for this stage. Our recruiting team will review your profile and reach out within 48 hours. Thank you for your time!")

    st.rerun()

# --- SIDEBAR (Premium Visuals) ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/business-group.png", width=60)
    st.markdown("### Hiring Assessment")
    
    # Progress Calculation
    total_steps = len(st.session_state.interviewer.required_info)
    captured = len([v for v in st.session_state.candidate_data.values() if v and not isinstance(v, dict)])
    progress = min(captured / total_steps, 1.0)
    
    st.write("Overall Progress")
    st.progress(progress)
    
    st.divider()
    
    if st.session_state.candidate_data:
        st.markdown("#### Captured Profile")
        for k in st.session_state.interviewer.required_info:
            val = st.session_state.candidate_data.get(k)
            if val:
                st.markdown(f"**{k.replace('_',' ').title()}**")
                st.markdown(f"<span style='color: #38BDF8;'>{val}</span>", unsafe_allow_html=True)
                st.write("")
    
    st.divider()
    if st.button("Reset Session", use_container_width=True):
        st.session_state.clear()
        st.rerun()
