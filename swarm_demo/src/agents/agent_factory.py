"""
Agent creation utilities.
"""
import os
from typing import Dict, Any, List
import autogen
import logging
from .yahoo_agent import YahooFinanceAgent
from .google_agent import GoogleNewsAgent
from .report_agent import ReportWriterAgent

logger = logging.getLogger(__name__)

def create_group_chat(
    manager_config: Dict[str, Any],
    agents: List[autogen.AssistantAgent]
) -> autogen.GroupChat:
    """创建GroupChat实例"""
    try:
        # 创建GroupChat
        group_chat = autogen.GroupChat(
            agents=agents,
            messages=[],
            max_round=50
        )
        
        # 创建GroupChatManager并关联GroupChat
        manager = autogen.GroupChatManager(
            groupchat=group_chat,
            **manager_config
        )
        
        # 将manager添加到agents列表
        group_chat.agents.insert(0, manager)
        
        return group_chat
    except Exception as e:
        logger.error(f"Error creating group chat: {str(e)}")
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
            "temperature": float(os.getenv("TEMPERATURE", 0.7)),
            "request_timeout": 300
        }
    }

def create_analysis_agents(config: Dict[str, Any]) -> List[autogen.AssistantAgent]:
    """创建分析Agent实例"""
    try:
        yahoo_agent = YahooFinanceAgent(**config.get("yahoo_analyst", {}))
        google_agent = GoogleNewsAgent(**config.get("google_analyst", {}))
        report_agent = ReportWriterAgent(**config.get("report_writer", {}))
        
        return [yahoo_agent, google_agent, report_agent]
    except Exception as e:
        logger.error(f"Error creating analysis agents: {str(e)}")
        raise