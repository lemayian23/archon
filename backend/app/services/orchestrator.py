from typing import Dict, Any, AsyncGenerator
from ..agents.planner import PlannerAgent
from ..agents.coder import CoderAgent
from ..agents.visualizer import VisualizerAgent
from ..agents.critic import CriticAgent
from ..services.sandbox import SandboxExecutor

class Orchestrator:
    def __init__(self):
        self.planner = PlannerAgent()
        self.coder = CoderAgent()
        self.visualizer = VisualizerAgent()
        self.critic = CriticAgent()
        self.sandbox = SandboxExecutor()
        
    async def execute_workflow(self, session_id: str, user_query: str, 
                             file_info: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        
        # Step 1: Planning
        yield {"agent": "planner", "status": "started", "message": "Planning the analysis..."}
        plan_result = await self.planner.process(session_id, {
            "query": user_query,
            "file_info": file_info
        })
        yield plan_result
        
        # Step 2: Coding
        yield {"agent": "coder", "status": "started", "message": "Writing analysis code..."}
        code_result = await self.coder.process(session_id, {
            "query": user_query,
            "plan": plan_result["output"],
            "file_info": file_info
        })
        yield code_result
        
        # Step 3: Real Sandbox Execution
        yield {"agent": "executor", "status": "started", "message": "Executing code in secure sandbox..."}
        
        # Mock CSV content for now - in real implementation, this comes from uploaded file
        csv_content = "date,product,revenue,units_sold\n2024-01-01,Product A,1000,50\n2024-01-01,Product B,1500,75"
        
        execution_result = await self.sandbox.execute_code(
            code_result["code"], csv_content, session_id
        )
        yield {"agent": "executor", "status": "completed", "output": execution_result}
        
        # Step 4: Visualization (only if execution successful)
        if execution_result.get("success", False):
            yield {"agent": "visualizer", "status": "started", "message": "Creating visualizations..."}
            viz_result = await self.visualizer.process(session_id, {
                "query": user_query,
                "analysis_results": execution_result["results"],
                "file_info": file_info
            })
            yield viz_result
            
            # Execute visualization code if needed
            if viz_result.get("code"):
                viz_execution = await self.sandbox.execute_code(
                    viz_result["code"], csv_content, session_id
                )
                yield {"agent": "visualizer", "status": "completed", "output": viz_execution}
        
        # Step 5: Critic Review
        yield {"agent": "critic", "status": "started", "message": "Reviewing analysis..."}
        critic_result = await self.critic.process(session_id, {
            "query": user_query,
            "code": code_result["code"],
            "execution_results": execution_result
        })
        yield critic_result
        
        # Final summary
        yield {
            "agent": "orchestrator", 
            "status": "completed",
            "message": "Analysis complete!",
            "summary": {
                "session_id": session_id,
                "query": user_query,
                "plan": plan_result["output"],
                "code": code_result["code"],
                "results": execution_result.get("results", {}),
                "feedback": critic_result["output"],
                "execution_success": execution_result.get("success", False)
            }
        }
