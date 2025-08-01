import streamlit as st
import google.generativeai as genai
import os
import re

os.environ["GOOGLE_API_KEY"] = "AIzaSyASL66kKdQvKWJ1xcjH6xdmmT3h2YNakTU"
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google Gemini API key not found! Please set GOOGLE_API_KEY as an environment variable.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash-lite')

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title(" TalentScout - AI Hiring Assistant")
st.markdown("""
<small>Privacy Notice: All information you provide is used solely for this simulated hiring assistant demo.
Your data is temporarily stored in this session only, anonymized when saved, and not shared or persisted anywhere.</small>
""", unsafe_allow_html=True)

# Session state
if "stage" not in st.session_state:
    st.session_state.stage = "intro"
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "candidate" not in st.session_state:
    st.session_state.candidate = {}
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_q_index" not in st.session_state:
    st.session_state.current_q_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "stored_data" not in st.session_state:
    st.session_state.stored_data = []

stages = [
    ("full_name", "Please enter your full name."),
    ("email", "Great! What's your email?"),
    ("phone", "Your phone number?"),
    ("location", "Where are you based?"),
    ("experience", "How many years of experience do you have?"),
    ("position", "What position(s) are you applying for?"),
    ("tech_stack", "List your tech stack (languages, tools, DBs)."),
]

def is_valid(stage, val):
    val = val.strip()
    if stage == "email":
        return "@" in val and "." in val
    if stage == "phone":
        return any(c.isdigit() for c in val)
    if stage == "experience":
        return any(c.isdigit() for c in val)
    return len(val) > 1

def anonymize(candidate_dict):
    anon = candidate_dict.copy()
    email = anon.get("email", "")
    if email:
        parts = email.split("@")
        if len(parts) == 2:
            local, domain = parts
            anon["email"] = (local[:2] + "***@" + domain) if len(local) > 2 else "***@" + domain
    phone = anon.get("phone", "")
    if phone:
        digits = re.sub(r"\D", "", phone)
        anon["phone"] = "***" + digits[-3:] if len(digits) > 3 else "***"
    return anon

def get_tech_questions(tech_stack):
    if not tech_stack.strip():
        return "No tech stack provided."
    prompt = (f"You are an experienced technical interviewer. For each of the following technologies, "
              f"write exactly 3 intermediate-level interview questions. Each question must be a single line "
              f"and should NOT include any explanations or answers. Only return the questions, nothing else:\n{tech_stack}")
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Couldn't generate questions. Error: {str(e)}"

def bot_speak(message: str) -> str:
    return f"🟦🤖🟦 {message}"

# Stage initialization
if st.session_state.stage == "intro" and not st.session_state.conversation:
    st.session_state.conversation.append(
        ("Bot", bot_speak("Hi! I'm TalentScout, your AI hiring assistant. I will ask a few questions to help us streamline the process."))
    )
    st.session_state.conversation.append(
        ("Bot", bot_speak("Do you want to proceed? Type 'yes' to continue or 'no' to exit."))
    )
    st.session_state.stage = "consent"

progress_stages = [s[0] for s in stages]

def get_progress(stage, current_q_index, questions):
    if stage in progress_stages:
        idx = progress_stages.index(stage)
        total = len(progress_stages) + (len(questions) if questions else 0)
        return idx / total
    elif stage == "tech_qna":
        total = len(questions) if questions else 1
        return (len(progress_stages) + current_q_index) / (len(progress_stages) + total)
    else:
        return 0

user_input = st.chat_input("Type your response...")

if user_input:
    user_input = user_input.strip()
    stage = st.session_state.stage.lower()
    st.session_state.conversation.append(("User", user_input))

    if any(x in user_input.lower() for x in ["bye", "exit", "thank"]):
        st.session_state.conversation.append(("Bot", bot_speak("Thanks! We’ll be in touch soon. 👋")))
        st.session_state.stage = "completed"

    elif stage == "intro":
        # Should not be reached, just a fallback.
        st.session_state.conversation.append(("Bot", bot_speak("Do you want to proceed? Type 'yes' to continue or 'no' to exit.")))
        st.session_state.stage = "consent"

    elif stage == "consent":
        if user_input.lower() == "yes":
            st.session_state.stage = "full_name"
            st.session_state.conversation.append(("Bot", bot_speak("Awesome! Let's begin.")))
            st.session_state.conversation.append(("Bot", bot_speak(stages[0][1])))
        elif user_input.lower() == "no":
            st.session_state.conversation.append(("Bot", bot_speak("Okay, feel free to return anytime. 👋")))
            st.session_state.stage = "completed"
        else:
            st.session_state.conversation.append(("Bot", bot_speak("Please reply with 'yes' to continue or 'no' to exit.")))

    elif stage in [s[0] for s in stages if s[0] != "tech_stack"]:
        if not is_valid(stage, user_input):
            st.session_state.conversation.append(("Bot", bot_speak(f"That doesn't look like a valid {stage.replace('_', ' ')}. Try again?")))
        else:
            st.session_state.candidate[stage] = user_input
            next_index = [s[0] for s in stages].index(stage) + 1
            st.session_state.stage = stages[next_index][0]
            st.session_state.conversation.append(("Bot", bot_speak(stages[next_index][1])))

    elif stage == "tech_stack":
        if not is_valid(stage, user_input):
            st.session_state.conversation.append(("Bot", bot_speak("Please provide a valid tech stack to continue.")))
        else:
            st.session_state.candidate[stage] = user_input
            st.session_state.conversation.append(("Bot", bot_speak("Generating technical questions...")))
            questions_text = get_tech_questions(user_input)
            questions_list = [q.strip() for q in questions_text.split('\n') if q.strip()]
            if len(questions_list) == 0:
                st.session_state.conversation.append(("Bot", bot_speak("Couldn't parse questions from the response. Ending the session.")))
                st.session_state.stage = "completed"
            else:
                st.session_state.questions = questions_list
                st.session_state.current_q_index = 0
                st.session_state.answers = {}
                st.session_state.stage = "tech_qna"
                st.session_state.conversation.append(("Bot", bot_speak("Answer a few questions to help us understand you better.")))
                st.session_state.conversation.append(("Bot", bot_speak(st.session_state.questions[0])))

    elif stage == "tech_qna":
        idx = st.session_state.current_q_index
        st.session_state.answers[idx] = user_input
        next_idx = idx + 1
        if next_idx < len(st.session_state.questions):
            st.session_state.current_q_index = next_idx
            st.session_state.conversation.append(("Bot", bot_speak(st.session_state.questions[next_idx])))
        else:
            st.session_state.conversation.append(("Bot", bot_speak("Thank you for your responses. Our team will get in touch with you soon!")))
            candidate_anonymized = anonymize(st.session_state.candidate)
            stored_entry = {
                "candidate_info": candidate_anonymized,
                "technical_answers": st.session_state.answers.copy(),
            }
            st.session_state.stored_data.append(stored_entry)
            st.session_state.stage = "completed"

    elif stage == "completed":
        st.session_state.conversation.append(("Bot", bot_speak("The session is already complete.")))

# Progress bar shows above chat
progress = get_progress(
    st.session_state.stage,
    st.session_state.current_q_index if "current_q_index" in st.session_state else 0,
    st.session_state.questions if "questions" in st.session_state else []
)
st.progress(progress)

# Render styled chat bubbles
for role, msg in st.session_state.conversation:
    if role == "User":
        st.markdown(
            f"""
            <div style="
                background-color:#2779a7;
                color:#fff;
                padding:8px 12px;
                border-radius:10px;
                margin:5px 0;
                max-width:70%;
                float:right;
                clear:both;
                word-wrap: break-word;">
                {msg}
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="
                background-color:#384259;
                color:#fff;
                padding:8px 12px;
                border-radius:10px;
                margin:5px 0;
                max-width:70%;
                float:left;
                clear:both;
                word-wrap: break-word;">
                {msg}
            </div>""",
            unsafe_allow_html=True,
        )

with st.expander("View anonymized collected data (for demo only)"):
    st.json(st.session_state.stored_data)
