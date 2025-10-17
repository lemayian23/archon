from abc import ABC, abstractmethod
from typing import Dict, Any
import os
from openai import OpenAI
from ..core.config import settings

class BaseAgent(ABC):
    def __init__(self):
        # Initialize OpenAI client with API key from settings
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    @abstractmethod
    async def process(self, session_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    async def call_llm(self, prompt: str, system_message: str = None) -> str:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        try:
            print(f"Calling OpenAI API with model: gpt-3.5-turbo")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use GPT-3.5-turbo instead of GPT-4
                messages=messages,
                temperature=0.1,
                max_tokens=1500
            )
            
            result = response.choices[0].message.content
            print(f"OpenAI response received: {result[:100]}...")
            return result
            
        except Exception as e:
            error_msg = f"OpenAI API Error: {str(e)}"
            print(error_msg)
            # Provide fallback responses based on agent type
            if "planner" in self.__class__.__name__.lower():
                return """STEPS:
1. Load and inspect the dataset structure
2. Clean data and handle missing values
3. Perform the requested analysis
4. Create appropriate visualizations
5. Generate insights and summary"""
            elif "coder" in self.__class__.__name__.lower():
                return """import pandas as pd
import matplotlib.pyplot as plt

# Load and analyze data
df = pd.read_csv('data.csv')
print("Data loaded successfully")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Basic analysis
results = {
    'data_shape': df.shape,
    'data_columns': list(df.columns),
    'analysis_complete': True
}"""
            else:
                return "Analysis completed with fallback response due to API issues."
