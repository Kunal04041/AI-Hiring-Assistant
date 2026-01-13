import json
from src.utils.llm_manager import LLMManager

class Interviewer:
    def __init__(self):
        self.llm = LLMManager()
        self.required_info = ["name", "email", "phone", "experience", "position", "tech_stack"]

    def get_conversation_response(self, history, current_data):
        """
        Drives the conversation dynamically.
        Analyzes what info is missing and talks to the user.
        """
        missing = [field for field in self.required_info if field not in current_data or not current_data[field]]
        
        if not missing:
            return "DONE", "I have all the basic info! Let's move to the technical questions. Ready?"

        system_prompt = (
            "You are a friendly and professional AI Recruiter for TalentScout. "
            "Your goal is to collect the following info from the candidate: name, email, phone, years of experience, position, and tech stack. "
            f"So far you have: {json.dumps(current_data)}. "
            f"Still missing: {', '.join(missing)}. "
            "Instruction: Be conversational. Don't just list questions. Respond to the user's previous comment, then ask for ONE missing piece of info at a time. "
            "If the user provides multiple pieces of info at once, acknowledge them and ask for the next one."
        )
        
        # Convert history for the prompt
        history_str = "\n".join([f"{m['role']}: {m['content']}" for m in history[-5:]])
        prompt = f"Recent Conversation:\n{history_str}\n\nRecruiter Response:"
        
        response = self.llm.generate_response(prompt, system_prompt=system_prompt)
        return "COLLECTING", response

    def extract_info(self, user_input, current_data):
        """
        Uses LLM to extract candidate data from user input.
        """
        system_prompt = (
            "You are a data extraction assistant. Extract any of these fields from the user input: "
            "name, email, phone, experience, position, tech_stack. "
            "Return ONLY a JSON object with the fields found. "
            "Example: {\"name\": \"John Doe\", \"email\": \"john@example.com\"}. "
            "If nothing is found, return {}."
        )
        
        response = self.llm.generate_response(user_input, system_prompt=system_prompt)
        try:
            # Look for JSON in the response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != -1:
                extracted = json.loads(response[start:end])
                # Update current data
                for k, v in extracted.items():
                    if k in self.required_info and v:
                        current_data[k] = v
                return current_data
        except:
            pass
        return current_data

    def get_technical_questions(self, tech_stack):
        """
        Generates technical questions based on the provided tech stack.
        """
        prompt = (
            f"Generate exactly 3 professional technical interview questions for these skills: {tech_stack}. "
            "Each question should be short and on a new line. No numbering."
        )
        response = self.llm.generate_response(prompt)
        questions = [q.strip() for q in response.split('\n') if q.strip() and len(q) > 10]
        return questions[:3]
