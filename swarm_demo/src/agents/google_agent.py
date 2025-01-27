"""
Google News analysis agent.
"""
from typing import Dict, Any, Optional
from datetime import datetime
from .base_agent import BaseAgent
from services.news_service import NewsService
import logging

logger = logging.getLogger(__name__)

class GoogleNewsAgent(BaseAgent):
    """Google news analyst Agent"""
    
    def __init__(self, name: str = "Google_Analyst", **kwargs):
        system_message = """你是Google新闻的专业分析师，负责：
1. 通过SerpAPI获取和分析Google新闻
2. 分析媒体报道和市场情绪
3. 识别重要事件和公告
4. 生成新闻分析报告"""
        
        super().__init__(
            name=name,
            system_message=system_message,
            **kwargs
        )
    
    async def analyze_news(self, query: str, context: Optional['AnalysisContext'] = None) -> Dict[str, Any]:
        """分析Google新闻数据"""
        logger.info(f"Analyzing Google news for query: {query}")
        try:
            self._log_context(context, "start_analysis", {
                "query": query,
                "description": "Starting Google News analysis"
            })
            
            # 使用NewsService获取和分析新闻
            news_data = NewsService.get_google_news(query)
            
            # 准备结果
            result = {
                "source": "Google News",
                "query": query,
                "timestamp": datetime.utcnow().isoformat(),
                "data": news_data
            }

            if context:
                # 记录情感分析结果
                self._log_context(context, "sentiment_analysis", {
                    "findings": {
                        "articles_analyzed": len(news_data["news_articles"]),
                        "significant_events": len(news_data["events"]),
                        "sentiment_summary": news_data["sentiment"]
                    }
                })
                
                # 更新上下文
                self._update_context(context, result)

            return result
            
        except Exception as e:
            self._handle_error(e, "analyzing Google news")