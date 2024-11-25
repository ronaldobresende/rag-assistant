import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class OpenAiClient:
    def __init__(self):
        self.open_api_key = os.getenv('OPENAI_API_KEY')
        self.modelo = "gpt-4o-mini"

    def get_llm(self):
        return ChatOpenAI(
            temperature=0,
            model=self.modelo,
            openai_api_key=self.open_api_key
        )