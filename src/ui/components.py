import streamlit as st

def render_chat_bubble(role, message):
    """
    Renders professional looking chat bubbles with a premium aesthetic.
    """
    if role == "User":
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 20px;">
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; 
                    padding: 14px 18px; 
                    border-radius: 20px 20px 4px 20px; 
                    max-width: 75%; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                    font-family: 'Inter', sans-serif;
                    line-height: 1.5;
                ">
                    <div style="font-size: 0.8rem; opacity: 0.8; margin-bottom: 4px; font-weight: 600;">YOU</div>
                    {message}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 20px;">
                <div style="
                    background-color: #1E293B; 
                    color: #F1F5F9; 
                    padding: 14px 18px; 
                    border-radius: 20px 20px 20px 4px; 
                    max-width: 75%; 
                    border: 1px solid #334155;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                    font-family: 'Inter', sans-serif;
                    line-height: 1.5;
                ">
                    <div style="font-size: 0.8rem; color: #38BDF8; margin-bottom: 4px; font-weight: 700; letter-spacing: 0.5px;">HIRING ASSISTANT</div>
                    {message}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

def apply_custom_css():
    st.markdown("""
        <style>
        /* Global Background and Text */
        .stApp {
            background-color: #0F172A;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #1E293B !important;
            border-right: 1px solid #334155;
        }
        
        section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] p {
            color: #E2E8F0 !important;
        }

        /* Typography */
        h1, h2, h3, h4, p, span {
            color: #F8FAFC !important;
            font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
        }

        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Chat Input Styling */
        .stChatInputContainer {
            background-color: #1E293B !important;
            padding: 10px !important;
            border-radius: 15px !important;
            border: 1px solid #334155 !important;
        }
        
        /* Expanders and Dividers */
        .stExpander, hr {
            border-color: #334155 !important;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0F172A;
        }
        ::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #475569;
        }
        </style>
    """, unsafe_allow_html=True)
