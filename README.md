# AI-Hiring-Assistant
An AI-powered hiring assistant chatbot built using Streamlit and Google Gemini's generative AI model. This app simulates an interactive technical interview by collecting candidate information, generating tailored technical questions based on the candidate’s tech stack, and anonymizing sensitive data to protect privacy.

---

## 1.Project Overview

TalentScout guides job candidates through a conversational interview workflow:

- Collects personal and professional details step-by-step.
- Dynamically generates **technical interview questions** using Google Gemini based on the candidate’s specified technologies.
- Records candidate answers to technical questions.
- Anonymizes sensitive data (email and phone) before temporarily storing it for demo purposes.
- Provides a friendly, chat-based experience to streamline hiring or screening processes.

---

## 2.Features

- AI-generated, personalized technical questions.
- Streamlit-powered chat UI for easy interaction.
- Privacy-first approach: data anonymization and temporary session storage.
- Clear, modular code organized for readability and maintainability.
- Ready to run locally or deploy on cloud platforms like AWS.

---

## 3.**Setup Instructions**
3.1 Download the `app.py` file and `requirements.txt` file to a folder on your local machine.

3.2 **Create a virtual environment** to keep dependencies isolated:
 


   Run this command in your terminal or command prompt to create a new virtual environment:
   ```python
   python -m venv myenv
   ```
3.3 Install Dependencies

Install all required Python packages by running:
```python
pip install -r requirements.txt
```

3.4 Navigate to the App Directory

Use the `cd` command to go to the folder where `app.py` is located. For example:
```python
cd /path/to/your/project/folder
```
3.5 Start the app by running:
```python
streamlit run app.py
```
After launching, Streamlit will provide a local URL, open this link in your web browser to interact with the bot.


## 4.Technical Details
4.1. Libraries Used:

- streamlit: For building the interactive web interface.
- google.generativeai: To access Google Gemini for content generation.
- os: For environment variable access (API keys).
- re: For basic validation and anonymization (regular expressions).

4.2 Model Details:
- Model Used: Google Gemini 2.5 Flash Lite (models/gemini-2.5-flash-lite)
- The model is accessed via the official google.generativeai Python package, configured at session start.
- Gemini is used both for generating technical interview questions tailored to the candidate's tech stack.

4.3 Architectural Decisions

- Chose a session-based flow using Streamlit’s st.session_state for tracking progress, storing candidate data, and managing chat history.
- An interactive conversational assistant mimics a chat, collecting information in stages and managing dynamic context.
- Privacy measures: Collected candidate data is anonymized (email and phone masked) and viewable only within the current demo session.
- All model prompts and inference are abstracted into helper functions (notably get_tech_questions), keeping logic modular and testable.

## 5.Propmpt Design:
- Information Gathering: The assistant walks users through a series of structured prompts (full name, contact, location, experience, tech stack). Prompts use plain language and offer clear guidance to maximize form completion quality.
- Technical Question Generation: Prompts sent to Gemini explicitly instruct it to return three intermediate-level technical questions per input technology, stressing that output must be only questions (no answers, no explanations), each on a single line.
Example prompt: " You are an experienced technical interviewer. For each of the following technologies, write exactly 3 intermediate-level interview questions. Each question must be a single line and should NOT include any explanations or answers. Only return the questions, nothing else."

## 6.Challenges and solution

6.1 Access to Free Generative Models:

- Challenge: Free-tier access to powerful generative models is limited—high-quality versions may have quotas, costs, or require approval, making unrestricted prototyping and broader deployment difficult.

- Solution: Evaluated whether relying on free or limited models is sustainable for the project’s scale and intended use. For ongoing or production use, consider budgeting for paid APIs, investigating open-source alternatives, or combining multiple model sources to mitigate cost and quota constraints.

6.2 Error Handling with Model API:

- Challenge: Unreliable connectivity, rate limits, or unexpected responses from the external model API could degrade user experience.
  
- Solution: Encapsulated every API call within try/except blocks. If errors occur, users receive a friendly fallback message (e.g., “Couldn't generate questions. Error: ...") without breaking the app.

6.3 Session Management & User Flow

- Challenge: Users may provide incomplete, ambiguous, or unexpected responses, disrupting the conversation flow. Ensuring progression and storing state was critical to a smooth experience.
  
- Solution: Leveraged Streamlit’s st.session_state to track progress and conversation context. This allowed the assistant to recover gracefully from partial inputs or interruptions, delivering a seamless, chat-like flow.

