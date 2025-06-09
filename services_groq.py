from groq import Groq
from utils import GROQ_API_KEY, GROQ_MODEL

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.system_prompt = """You are a helpful AI assistant. You are participating in a voice conversation.
        Keep your responses conversational, concise, and engaging. Respond naturally as if you're talking to someone."""
        
    def generate_response(self, prompt):
        try:
            # Create chat completion with system prompt
            response = self.client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq generation error: {e}")
            return "I'm sorry, I couldn't process that request."
    
    async def generate_response_async(self, prompt):
        # Async wrapper for response generation
        return self.generate_response(prompt)
