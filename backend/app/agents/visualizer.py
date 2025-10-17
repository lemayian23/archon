from .base import BaseAgent
from typing import Dict, Any

class VisualizerAgent(BaseAgent):
    async def process(self, session_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        analysis_results = input_data.get("analysis_results", {})
        user_query = input_data["query"]
        
        system_message = """You are a data visualization expert. Create Plotly visualization code based on the analysis results.
        
        Rules:
        1. Use Plotly for interactive charts
        2. Make visualizations clean and professional
        3. Return ONLY the Python code
        4. Assume the analysis results are in 'results' variable"""
        
        prompt = f"""
        User Query: {user_query}
        Analysis Results: {analysis_results}
        
        Create visualization code:
        """
        
        viz_code = await self.call_llm(prompt, system_message)
        
        return {
            "agent": "visualizer",
            "output": viz_code,
            "code": viz_code,
            "status": "completed"
        }
