"""
Agent creation utilities.
"""
import os
from typing import Dict, Any, List
from autogen import GroupChat, GroupChatManager
import logging
from .yahoo_agent import YahooFinanceAgent
from .google_agent import GoogleNewsAgent
from .report_agent import ReportWriterAgent

logger = logging.getLogger(__name__)

def create_swarm_network(
    manager_config: Dict[str, Any],
    agents: List[Any]
) -> Dict[str, Any]:
    """创建GroupChat实例"""
    try:
        # 创建GroupChat
        group_chat = GroupChat(
            agents=agents,
            messages=[],
            max_round=50
        )
        
        # 创建GroupChatManager
        manager = GroupChatManager(
            groupchat=group_chat,
            llm_config=manager_config["llm_config"]
        )
        
        return {
            "group_chat": group_chat,
            "manager": manager
        }
    except Exception as e:
        logger.error(f"Error creating swarm: {str(e)}")
        raise

def get_default_manager_config() -> Dict[str, Any]:
    """获取默认的Manager配置"""
    return {
        "name": "Research_Manager",
        "system_message": """你是一个专业的研究项目经理，负责：
1. 协调新闻分析任务
2. 管理工作流程
3. 确保任务完成
4. 处理异常情况""",
        "llm_config": {
            "config_list": [{
                "model": os.getenv("LLM_MODEL", "anthropic/claude-3-sonnet"),
                "api_key": os.getenv("OPENROUTER_API_KEY"),
                "base_url": os.getenv("OPENROUTER_BASE_URL"),
                "api_type": "openrouter"
            }],
            "temperature": float(os.getenv("TEMPERATURE", 0.7))
        }
    }

def create_analysis_agents(config: Dict[str, Any]) -> List[Any]:
    """创建分析Agent实例"""
    try:
        yahoo_agent = YahooFinanceAgent(**config.get("yahoo_analyst", {}))
        google_agent = GoogleNewsAgent(**config.get("google_analyst", {}))
        report_agent = ReportWriterAgent(**config.get("report_writer", {}))
        
        return [yahoo_agent, google_agent, report_agent]
    except Exception as e:
        logger.error(f"Error creating analysis agents: {str(e)}")
        raise