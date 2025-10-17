from .base import BaseAgent
from typing import Dict, Any

class CoderAgent(BaseAgent):
    async def process(self, session_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_query = input_data["query"]
        analysis_plan = input_data["plan"]
        file_info = input_data["file_info"]
        
        system_message = """You are a Python data analyst. Write clean, efficient pandas code to analyze data based on the user's query and analysis plan.
        
        IMPORTANT RULES:
        1. Only use: pandas, numpy, matplotlib, plotly
        2. Assume the CSV file is loaded as 'df'
        3. Return ONLY the Python code, no explanations
        4. Include code to handle potential errors
        5. Make sure to return the results in a way that can be used by other agents"""
        
        prompt = f"""
        User Query: {user_query}
        Analysis Plan: {analysis_plan}
        File: {file_info['filename']}
        Columns: {file_info['columns']}
        
        Write Python code to perform this analysis:
        """
        
        code = await self.call_llm(prompt, system_message)
        
        return {
            "agent": "coder",
            "output": code,
            "code": code,
            "status": "completed"
        }
