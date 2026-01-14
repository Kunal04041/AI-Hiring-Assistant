import os
from groq import Groq
from dotenv import load_dotenv

# Load .env - try current directory first, then legacy parent root
load_dotenv() 
if not os.getenv("GROQ_API_KEY"):
    load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class LLMManager:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        
        self.client = Groq(
            api_key=GROQ_API_KEY,
        )

    def generate_response(self, prompt, system_prompt="You are a professional technical interviewer AI."):
        """
        Generates a response using Groq. 
        Uses high-quality free models.
        """
        models = [
            "llama-3.3-70b-versatile",
            "llama-guard-3-8b"
        ]
        
        last_error = ""
        for model in models:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    timeout=15
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                last_error = str(e)
                continue 
        
        return "I apologize for the inconvenience, but it seems our daily free screening credits have run out. Please come back later to interact or complete your assessment! Thank you for your patience."
