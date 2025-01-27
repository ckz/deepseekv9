"""
Agent definitions for the financial news analysis system.
This module re-exports components from the modular agent structure.
"""

from .agents import (
    BaseAgent,
    YahooFinanceAgent,
    GoogleNewsAgent,
    ReportWriterAgent,
    create_group_chat,
    get_default_manager_config,
    create_analysis_agents
)

__all__ = [
    'BaseAgent',
    'YahooFinanceAgent',
    'GoogleNewsAgent',
    'ReportWriterAgent',
    'create_group_chat',
    'get_default_manager_config',
    'create_analysis_agents'
]