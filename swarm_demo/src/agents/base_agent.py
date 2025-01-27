"""
Base agent class with common functionality.
"""
import logging
from typing import Dict, Any, Optional
from autogen import AssistantAgent as Agent
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAgent(Agent):
    """Base agent class with common functionality"""
    
    def __init__(self, name: str, system_message: str, **kwargs):
        """Initialize base agent with common setup"""
        super().__init__(
            name=name,
            system_message=system_message,
            llm_config=kwargs.get('llm_config', {})
        )
        self._system_message = system_message
    
    def _log_context(self, context: Optional['AnalysisContext'], 
                    action: str, details: Dict[str, Any]) -> None:
        """Common context logging logic"""
        if context:
            context.log_agent_thought(
                agent_name=self.name,
                thought={
                    "action": action,
                    "timestamp": datetime.utcnow().isoformat(),
                    **details
                }
            )
    
    def _handle_error(self, error: Exception, action: str) -> None:
        """Common error handling logic"""
        error_msg = f"Error in {action}: {str(error)}"
        logger.error(error_msg)
        raise type(error)(error_msg) from error
    
    def _update_context(self, context: Optional['AnalysisContext'], 
                       result: Dict[str, Any]) -> None:
        """Common context update logic"""
        if context:
            context.update_context(self.name, result)
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task within the agent network"""
        try:
            action = task.get("action")
            context = task.get("context")
            
            if not action:
                raise ValueError("Task must specify an action")
            
            self._log_context(context, action, {"task_received": task})
            
            # Execute the specific action
            if hasattr(self, action):
                result = await getattr(self, action)(**task.get("params", {}))
                self._update_context(context, result)
                return result
            else:
                raise ValueError(f"Unknown action: {action}")
                
        except Exception as e:
            self._handle_error(e, f"execute_task - {task.get('action', 'unknown')}")
            return {"error": str(e)}