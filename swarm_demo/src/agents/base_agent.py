"""
Base agent class with common functionality.
"""
import logging
from typing import Dict, Any, Optional
import autogen
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAgent(autogen.AssistantAgent):
    """Base agent class with common functionality"""
    
    def __init__(self, name: str, system_message: str, **kwargs):
        """Initialize base agent with common setup"""
        super().__init__(
            name=name,
            system_message=system_message,
            **kwargs
        )
    
    def _log_context(self, context: Optional['AnalysisContext'], 
                    action: str, details: Dict[str, Any]) -> None:
        """Common context logging logic"""
        if context:
            context.log_agent_thought(
                agent_name=self.name,
                thought={
                    "action": action,
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