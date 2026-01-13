import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env from the parent root as requested
load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class LLMManager:
    def __init__(self):
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables.")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )

    def generate_response(self, prompt, system_prompt="You are a professional technical interviewer AI."):
        """
        Generates a response using OpenRouter. 
        Tries multiple free models to handle rate limiting.
        """
        models = [
            "openai/gpt-oss-120b:free"
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
                # Try all models in the list before giving up
                continue 
        
        return "I apologize for the inconvenience, but it seems our daily free screening credits have run out. Please come back later to interact or complete your assessment! Thank you for your patience."
