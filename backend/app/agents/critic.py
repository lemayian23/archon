from .base import BaseAgent
from typing import Dict, Any

class CriticAgent(BaseAgent):
    async def process(self, session_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_query = input_data["query"]
        generated_code = input_data.get("code", "")
        execution_results = input_data.get("execution_results", {})
        
        system_message = """You are a code and analysis critic. Review the generated code and results for:
        1. Correctness - does it answer the user's query?
        2. Safety - any potential security issues?
        3. Efficiency - is the code well-structured?
        4. Completeness - does it handle edge cases?
        
        Provide constructive feedback and suggestions for improvement."""
        
        prompt = f"""
        User Query: {user_query}
        Generated Code: {generated_code}
        Execution Results: {execution_results}
        
        Review this analysis:
        """
        
        feedback = await self.call_llm(prompt, system_message)
        
        return {
            "agent": "critic", 
            "output": feedback,
            "status": "completed"
        }
