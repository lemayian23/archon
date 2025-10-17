from abc import ABC, abstractmethod
from typing import Dict, Any
import openai
from ..core.config import settings

class BaseAgent(ABC):
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    @abstractmethod
    async def process(self, session_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    async def call_llm(self, prompt: str, system_message: str = None) -> str:
        messages = []
        if system_message:
            messages.append({\"role\": \"system\", \"content\": system_message})
        messages.append({\"role\": \"user\", \"content\": prompt})
        
        response = self.client.chat.completions.create(
            model=\"gpt-4\",
            messages=messages,
            temperature=0.1
        )
        
        return response.choices[0].message.content
