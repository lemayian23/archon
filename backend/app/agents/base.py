from abc import ABC, abstractmethod
from typing import Dict, Any
import os

class BaseAgent(ABC):
    def __init__(self):
        # OpenAI client will be initialized when needed
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
    
    @abstractmethod
    async def process(self, session_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    async def call_llm(self, prompt: str, system_message: str = None) -> str:
        # Mock implementation for now - we'll add real OpenAI later
        if "plan" in prompt.lower():
            return """STEPS:
1. Load the CSV data and inspect structure
2. Check for missing values and data quality
3. Analyze monthly revenue trends
4. Create visualization of the trends
5. Generate summary insights"""
        elif "code" in prompt.lower():
            return """import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data.csv')

# Basic analysis
print(df.head())
print(df.info())
print(df.describe())

# Return simple results
results = {
    'data_shape': df.shape,
    'data_columns': list(df.columns),
    'analysis_complete': True
}
"""
        else:
            return "Analysis completed successfully."
