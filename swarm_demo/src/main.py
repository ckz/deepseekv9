"""
Main entry point for the financial news analysis system.
"""
import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

from agents import (
    YahooFinanceAgent,
    GoogleNewsAgent,
    ReportWriterAgent,
    create_group_chat,
    get_default_manager_config
)
from config import Config, validate_config, get_agent_configs

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
        
        # 创建GroupChat
        group_chat = create_group_chat(
            manager_config=get_default_manager_config(),
            agents=list(agents.values())
        )
        
        return {
            "agents": agents,
            "group_chat": group_chat
        }
    
    except Exception as e:
        logger.error(f"System initialization failed: {str(e)}")
        raise

async def run_analysis(
    topic: str,
    agents: Dict[str, Any],
    group_chat: Any
) -> Dict[str, Any]:
    """运行新闻分析流程"""
    try:
        logger.info(f"Starting analysis for topic: {topic}")
        
        # 收集Yahoo Finance数据
        yahoo_data = await agents["yahoo"].process_news(topic)
        logger.info("Yahoo Finance data collected")
        
        # 收集Google新闻数据
        google_data = await agents["google"].analyze_news(topic)
        logger.info("Google News data collected")
        
        # 生成报告
        analysis_results = {
            "yahoo_data": yahoo_data,
            "google_data": google_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        final_report = await agents["writer"].generate_report(analysis_results)
        logger.info("Final report generated")
        
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
            group_chat=system["group_chat"]
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
        print("\nReport Summary:")
        print("-" * 30)
        if "content" in result:
            print(f"Summary: {result['content'].get('summary', 'N/A')}")
            print("\nRecommendations:")
            for rec in result['content'].get('recommendations', []):
                print(f"- {rec}")
        
    except Exception as e:
        logger.error(f"Program failed: {str(e)}")
        raise