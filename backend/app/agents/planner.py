from .base import BaseAgent
from typing import Dict, Any

class PlannerAgent(BaseAgent):
    async def process(self, session_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_query = input_data[\"query\"]
        file_info = input_data.get(\"file_info\", {})
        
        system_message = \"\"\"You are a data analysis planner. Your job is to break down the user's natural language query into a step-by-step analysis plan.
        
        Output your plan in this format:
        STEPS:
        1. [Step 1: Data loading and basic inspection]
        2. [Step 2: Data cleaning if needed]
        3. [Step 3: Specific analysis step]
        4. [Step 4: Visualization planning]
        
        Keep steps clear and actionable for a data analyst.\"\"\"
        
        prompt = f\"\"\"
        User Query: {user_query}
        File: {file_info.get('filename', 'Unknown')}
        Columns: {file_info.get('columns', [])}
        
        Create an analysis plan:
        \"\"\"
        
        plan = await self.call_llm(prompt, system_message)
        
        return {
            \"agent\": \"planner\",
            \"output\": plan,
            \"status\": \"completed\"
        }
