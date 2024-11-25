import google.generativeai as genai  # type: ignore
from dotenv import load_dotenv  # type: ignore
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiClient:
    def __init__(self, model_name: str, system: str, temperature: float):
        self.model_name = model_name
        self.system_instruction = system
        self.temperature = temperature
        self.generation_config = {
            "temperature": self.temperature,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config,
            system_instruction=self.system_instruction,
            safety_settings=self.safety_settings
        )

    def get_llm(self):
        return self.model

