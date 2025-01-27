"""
Main entry point for the financial news analysis system.
"""
import asyncio
import logging
from typing import Dict, Any
from datetime import datetime

from agents import (
    YahooFinanceAgent,
    GoogleNewsAgent,
    ReportWriterAgent,
    create_swarm_network,
    get_default_manager_config
)
from config import Config, validate_config, get_agent_configs
from utils import AnalysisContext

# 设置日志
logging.basicConfig(level=Config.get_system_config()["log_level"])
logger = logging.getLogger(__name__)

async def initialize_system() -> Dict[str, Any]:
    """初始化系统"""
    try:
        # 验证配置
        validate_config()
        
        # 获取Agent配置
        agent_configs = get_agent_configs()
        
        # 创建Agents
        agents = {
            "yahoo": YahooFinanceAgent(**agent_configs["yahoo_analyst"]),
            "google": GoogleNewsAgent(**agent_configs["google_analyst"]),
            "writer": ReportWriterAgent(**agent_configs["report_writer"])
        }
        
        # 创建GroupChat和Manager
        chat_system = create_swarm_network(
            manager_config=get_default_manager_config(),
            agents=list(agents.values())
        )
        
        return {
            "agents": agents,
            "group_chat": chat_system["group_chat"],
            "manager": chat_system["manager"]
        }
    
    except Exception as e:
        logger.error(f"System initialization failed: {str(e)}")
        raise

async def run_analysis(
    topic: str,
    agents: Dict[str, Any],
    group_chat: Any,
    manager: Any
) -> Dict[str, Any]:
    """运行新闻分析流程"""
    try:
        logger.info(f"Starting analysis for topic: {topic}")
        
        # 创建分析上下文
        context = AnalysisContext(topic)
        logger.info(f"Created analysis context with ID: {context.analysis_id}")
        
        # 设置初始消息
        initial_message = f"""请分析以下主题的财经新闻: {topic}
        
1. Yahoo Finance Agent: 请收集和分析相关的财务数据
2. Google News Agent: 请收集和分析相关的新闻文章
3. Report Writer: 根据收集到的信息生成综合报告

请确保报告包含:
- 市场数据分析
- 新闻情感分析
- 关键见解和建议"""

        # 启动对话
        result = await manager.initiate_chat(
            recipient=agents["yahoo"],
            message=initial_message,
            clear_history=True
        )
        logger.info("Group chat completed")
        
        # 整合结果
        final_report = {
            "timestamp": datetime.utcnow().isoformat(),
            "topic": topic,
            "content": result,
            "thought_chains": {
                "yahoo": context.get_agent_thoughts(agents["yahoo"].name),
                "google": context.get_agent_thoughts(agents["google"].name),
                "writer": context.get_agent_thoughts(agents["writer"].name)
            }
        }
        
        return final_report
    
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise

async def main(topic: str) -> Dict[str, Any]:
    """主程序入口"""
    try:
        # 初始化系统
        system = await initialize_system()
        logger.info("System initialized successfully")
        
        # 运行分析
        report = await run_analysis(
            topic=topic,
            agents=system["agents"],
            group_chat=system["group_chat"],
            manager=system["manager"]
        )
        
        logger.info("Analysis completed successfully")
        return report
    
    except Exception as e:
        logger.error(f"Program execution failed: {str(e)}")
        raise

def run_sync(topic: str) -> Dict[str, Any]:
    """同步运行入口"""
    return asyncio.run(main(topic))

if __name__ == "__main__":
    # 示例使用
    try:
        # 设置分析主题
        analysis_topic = "Tesla Q4 2024 Earnings"
        
        # 运行分析
        result = run_sync(analysis_topic)
        
        # 打印结果
        print("\nAnalysis Result:")
        print("=" * 50)
        print(f"Topic: {analysis_topic}")
        print(f"Timestamp: {result.get('timestamp', 'N/A')}")
        print("\nReport Content:")
        print("-" * 30)
        if "content" in result:
            print(result["content"])
        
    except Exception as e:
        logger.error(f"Program failed: {str(e)}")
        raise