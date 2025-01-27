"""
Google News analysis agent.
"""
from typing import Dict, Any, Optional, List
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
        
        # 定义agent能力
        self.capabilities = {
            "analyze_news": "Analyze news articles from Google News",
            "analyze_sentiment": "Analyze sentiment of news articles",
            "identify_events": "Identify significant events from news",
            "generate_news_summary": "Generate a summary of news analysis"
        }
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tasks within the SWARM network"""
        action = task.get("action")
        params = task.get("params", {})
        context = params.get("context")
        
        if action == "analyze_news":
            return await self.analyze_news(params.get("topic"), context)
        elif action == "analyze_sentiment":
            return await self.analyze_sentiment(params.get("articles"), context)
        elif action == "identify_events":
            return await self.identify_events(params.get("articles"), context)
        elif action == "generate_news_summary":
            return await self.generate_news_summary(params.get("analysis_data"), context)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def analyze_news(self, query: str, context: Optional['AnalysisContext'] = None) -> Dict[str, Any]:
        """分析Google新闻数据"""
        logger.info(f"Analyzing Google news for query: {query}")
        try:
            self._log_context(context, "start_analysis", {
                "query": query,
                "description": "Starting Google News analysis"
            })
            
            # 使用NewsService获取新闻
            news_data = NewsService.get_google_news(query)
            
            # 分析情感
            sentiment_analysis = await self.analyze_sentiment(news_data["news_articles"], context)
            
            # 识别重要事件
            events_analysis = await self.identify_events(news_data["news_articles"], context)
            
            # 生成摘要
            summary = await self.generate_news_summary({
                "articles": news_data["news_articles"],
                "sentiment": sentiment_analysis,
                "events": events_analysis
            }, context)
            
            # 准备结果
            result = {
                "source": "Google News",
                "query": query,
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "news_articles": news_data["news_articles"],
                    "sentiment_analysis": sentiment_analysis,
                    "events": events_analysis,
                    "summary": summary
                }
            }

            if context:
                # 记录分析结果
                self._log_context(context, "analysis_complete", {
                    "findings": {
                        "articles_analyzed": len(news_data["news_articles"]),
                        "significant_events": len(events_analysis),
                        "sentiment_summary": sentiment_analysis["overall_sentiment"]
                    }
                })
                
                # 更新上下文
                self._update_context(context, result)

            return result
            
        except Exception as e:
            self._handle_error(e, "analyzing Google news")
    
    async def analyze_sentiment(self, articles: List[Dict[str, Any]], context: Optional['AnalysisContext'] = None) -> Dict[str, Any]:
        """分析新闻情感"""
        try:
            self._log_context(context, "analyze_sentiment", {
                "description": "Analyzing news sentiment",
                "article_count": len(articles)
            })
            
            # 使用NewsService分析情感
            sentiment_data = NewsService.analyze_sentiment(articles)
            
            return {
                "overall_sentiment": sentiment_data["overall"],
                "sentiment_breakdown": sentiment_data["breakdown"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self._handle_error(e, "analyzing sentiment")
    
    async def identify_events(self, articles: List[Dict[str, Any]], context: Optional['AnalysisContext'] = None) -> List[Dict[str, Any]]:
        """识别重要事件"""
        try:
            self._log_context(context, "identify_events", {
                "description": "Identifying significant events",
                "article_count": len(articles)
            })
            
            # 使用NewsService识别事件
            events = NewsService.extract_events(articles)
            
            return events
            
        except Exception as e:
            self._handle_error(e, "identifying events")
    
    async def generate_news_summary(self, analysis_data: Dict[str, Any], context: Optional['AnalysisContext'] = None) -> Dict[str, Any]:
        """生成新闻分析摘要"""
        try:
            self._log_context(context, "generate_summary", {
                "description": "Generating news analysis summary"
            })
            
            summary = {
                "main_topics": NewsService.extract_main_topics(analysis_data["articles"]),
                "key_events": [event["title"] for event in analysis_data["events"][:3]],
                "sentiment_overview": analysis_data["sentiment"]["overall_sentiment"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return summary
            
        except Exception as e:
            self._handle_error(e, "generating news summary")