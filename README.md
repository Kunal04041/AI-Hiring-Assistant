# AI-Hiring-Assistant
An AI-powered hiring assistant chatbot built using Streamlit and Google Gemini's generative AI model. This app simulates an interactive technical interview by collecting candidate information, generating tailored technical questions based on the candidate’s tech stack, and anonymizing sensitive data to protect privacy.

---

## Project Overview

TalentScout guides job candidates through a conversational interview workflow:

- Collects personal and professional details step-by-step.
- Dynamically generates **technical interview questions** using Google Gemini based on the candidate’s specified technologies.
- Records candidate answers to technical questions.
- Anonymizes sensitive data (email and phone) before temporarily storing it for demo purposes.
- Provides a friendly, chat-based experience to streamline hiring or screening processes.

---

## Features

- AI-generated, personalized technical questions.
- Streamlit-powered chat UI for easy interaction.
- Privacy-first approach: data anonymization and temporary session storage.
- Clear, modular code organized for readability and maintainability.
- Ready to run locally or deploy on cloud platforms like AWS.

---

##  Requirements

- Python 3.7+
- Streamlit
- google-generativeai

All dependencies are listed in `requirements.txt`.


## Setup Instructions
1. **Download** the `app.py` file and `requirements.txt` file to a folder on your local machine.

2. (Optional but recommended) **Create a virtual environment** to keep dependencies isolated:
 
3.(Optional but Recommended) Create a Virtual Environment

   Run this command in your terminal or command prompt to create a new virtual environment:
   ```python
   python -m venv myenv
```
