# TalentScout Pro: AI Hiring Assistant

TalentScout Pro is a professional, modular technical screening platform built with Streamlit and powered by OpenRouter. It uses advanced Large Language Models to conduct natural, conversational interviews, extract candidate information dynamically, and generate tailored technical assessments.

---

## Project Overview

TalentScout Pro transforms the traditional recruitment process into an interactive experience:

- Dynamic Information Gathering: Instead of a rigid form, the AI agent engages in a natural conversation to collect personal and professional details.
- Intelligent Data Extraction: Uses LLMs to parse user intent and automatically populate candidate profiles.
- Custom Technical Screening: Generates high-quality technical questions based on the candidate's specific tech stack.
- Premium UI/UX: Features a calibrated dark-mode interface with professional conversation bubbles and real-time progress tracking.
- Robust Architecture: Built with a modular structure and a resilient backend that handles model fallbacks and rate limiting gracefully.

---

## Technical Architecture

The project is organized into a modular structure to ensure maintainability and scalability:

- src/utils/llm_manager.py: Manages all LLM communications via OpenRouter, including a resilient fallback system to handle API rate limits.
- src/interviewer/logic.py: Contains the core recruitment intelligence, including conversation state management and data extraction logic.
- src/ui/components.py: Defines the visual design system, including professional chat bubble components and custom CSS overrides.
- app.py: The main entry point that coordinates the UI and the recruitment logic.

---

## Features

- Conversational Intelligence: The assistant responds to user context and asks for missing information selectively.
- Profile Snapshot: A real-time sidebar view that shows the information captured by the AI during the conversation.
- Progress Tracking: Visual progress bars indicate the completion status of the screening process.
- Model Resilience: Automatically suppresses technical API errors and provides user-friendly fallback messages during service interruptions.
- Privacy Focused: Data is handled within the session and can be reset at any time by the user.

---

## Setup Instructions

### 1. Project Initialization

Navigate to the project directory and create a virtual environment:

```powershell
python -m venv venv
```

### 2. Activate the Environment

On Windows:
```powershell
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install the required packages using pip:

```powershell
pip install -r requirements.txt
```

### 4. Configuration

Create a .env file in the root directory (or parent directory as per your setup) and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_api_key_here
```

### 5. Launch the Application

Start the Streamlit server:

```powershell
streamlit run app.py
```

---

## Model Details

- Primary Model: Meta Llama 3.3 70B Instruct (via OpenRouter)
- Fallback Logic: The system is designed to exhaustive the model list before presenting a graceful downtime message.
- Context Management: The interviewer maintains a recent history of the conversation to ensure responses remain relevant and professional.

---

## Video Walkthrough

Access the complete video walkthrough explaining the project logic and features here:
https://www.loom.com/share/0ebdd93036d04b8c8f04668b2224e51e?sid=137ebc6b-f181-4fa9-bab9-dd24f6a59717  (Outdated)
