"""
Agent definitions for the financial news analysis system.
"""
import autogen
from typing import Dict, List, Any, Optional
import os
import logging
from datetime import datetime
import json
from serpapi.google_search import GoogleSearch
import yfinance as yf
import pandas as pd
from textblob import TextBlob

# 设置日志
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

class YahooFinanceAgent(autogen.AssistantAgent):
    """Yahoo Finance新闻分析师Agent"""
    
    def __init__(self, name: str = "Yahoo_Analyst", **kwargs):
        system_message = """你是Yahoo Finance的专业分析师，负责：
1. 从Yahoo Finance获取和分析财经新闻
2. 提取关键财务指标和市场数据
3. 识别市场趋势和模式
4. 生成初步分析报告"""
        
        super().__init__(
            name=name,
            system_message=system_message,
            **kwargs
        )
        
    async def process_news(self, query: str, context: Optional['AnalysisContext'] = None) -> Dict[str, Any]:
        """处理Yahoo Finance新闻数据"""
        logger.info(f"Processing Yahoo Finance news for query: {query}")
        try:
            if context:
                context.log_agent_thought(
                    agent_name=self.name,
                    thought={
                        "action": "start_processing",
                        "query": query,
                        "description": "Starting to process Yahoo Finance data"
                    }
                )
            # 获取股票代码（假设查询包含股票代码）
            ticker = query.split()[0]
            stock = yf.Ticker(ticker)
            
            # 获取股票信息
            info = stock.info
            
            # 获取历史数据
            hist = stock.history(period="1mo")
            
            # 计算技术指标
            sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
            
            # 获取新闻
            news = stock.news
            
            # 处理新闻数据
            processed_news = []
            for article in news[:10]:  # 处理最新的10条新闻
                processed_news.append({
                    "title": article.get("title"),
                    "publisher": article.get("publisher"),
                    "link": article.get("link"),
                    "published": article.get("providerPublishTime"),
                    "type": article.get("type")
                })
            
            # 分析市场趋势
            current_price = hist['Close'].iloc[-1]
            price_change = ((current_price - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
            
            trends = [
                {
                    "indicator": "Price Trend",
                    "value": "Bullish" if price_change > 0 else "Bearish",
                    "change": f"{price_change:.2f}%"
                },
                {
                    "indicator": "SMA Crossover",
                    "value": "Bullish" if sma_20 > sma_50 else "Bearish",
                    "details": f"SMA20: {sma_20:.2f}, SMA50: {sma_50:.2f}"
                }
            ]
            
            # 准备结果
            result = {
                "source": "Yahoo Finance",
                "query": query,
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "news": processed_news,
                    "market_data": {
                        "current_price": current_price,
                        "volume": hist['Volume'].iloc[-1],
                        "market_cap": info.get('marketCap'),
                        "pe_ratio": info.get('forwardPE'),
                        "dividend_yield": info.get('dividendYield')
                    },
                    "trends": trends
                }
            }

            if context:
                # 记录市场数据分析思维
                context.log_agent_thought(
                    agent_name=self.name,
                    thought={
                        "action": "market_analysis",
                        "findings": {
                            "price_trend": f"Price changed by {price_change:.2f}%",
                            "technical_indicators": {
                                "sma20": f"{sma_20:.2f}",
                                "sma50": f"{sma_50:.2f}",
                                "trend": "Bullish" if sma_20 > sma_50 else "Bearish"
                            },
                            "news_count": len(processed_news)
                        }
                    }
                )
                
                # 更新上下文
                context.update_context(self.name, result)

            return result
        except Exception as e:
            logger.error(f"Error processing Yahoo Finance news: {str(e)}")
            raise

class GoogleNewsAgent(autogen.AssistantAgent):
    """Google新闻分析师Agent"""
    
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
            if context:
                context.log_agent_thought(
                    agent_name=self.name,
                    thought={
                        "action": "start_analysis",
                        "query": query,
                        "description": "Starting Google News analysis"
                    }
                )
            
            # 使用SerpAPI获取新闻
            search = GoogleSearch({
                "q": query,
                "tbm": "nws",
                "api_key": os.getenv("SERPAPI_API_KEY")
            })
            results = search.get_dict()
            
            # 处理新闻文章
            news_articles = []
            sentiments = []
            events = []
            
            if "news_results" in results:
                for article in results["news_results"]:
                    # 分析情感
                    sentiment = TextBlob(article.get("title", "") + " " + article.get("snippet", ""))
                    sentiment_score = sentiment.sentiment.polarity
                    
                    # 添加处理后的文章
                    news_articles.append({
                        "title": article.get("title"),
                        "source": article.get("source"),
                        "published": article.get("date"),
                        "snippet": article.get("snippet"),
                        "link": article.get("link"),
                        "sentiment_score": sentiment_score
                    })
                    
                    sentiments.append(sentiment_score)
                    
                    # 识别重要事件
                    if abs(sentiment_score) > 0.5:  # 显著正面或负面新闻
                        events.append({
                            "type": "Significant News",
                            "title": article.get("title"),
                            "sentiment": "Positive" if sentiment_score > 0 else "Negative",
                            "score": sentiment_score
                        })
            
            # 计算整体情感
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
            sentiment_analysis = {
                "average_score": avg_sentiment,
                "overall_sentiment": "Positive" if avg_sentiment > 0 else "Negative" if avg_sentiment < 0 else "Neutral",
                "confidence": abs(avg_sentiment)
            }
            
            # 准备结果
            result = {
                "source": "Google News",
                "query": query,
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "news_articles": news_articles,
                    "sentiment": sentiment_analysis,
                    "events": events
                }
            }

            if context:
                # 记录情感分析结果
                context.log_agent_thought(
                    agent_name=self.name,
                    thought={
                        "action": "sentiment_analysis",
                        "findings": {
                            "articles_analyzed": len(news_articles),
                            "significant_events": len(events),
                            "sentiment_summary": {
                                "average_score": avg_sentiment,
                                "overall_tone": sentiment_analysis["overall_sentiment"],
                                "confidence": sentiment_analysis["confidence"]
                            }
                        }
                    }
                )
                
                # 更新上下文
                context.update_context(self.name, result)

            return result
        except Exception as e:
            logger.error(f"Error analyzing Google news: {str(e)}")
            raise

class ReportWriterAgent(autogen.AssistantAgent):
    """财经报告撰写Agent"""
    
    def __init__(self, name: str = "Report_Writer", **kwargs):
        system_message = """你是专业的财经报告撰写专家，负责：
1. 整合所有分析结果
2. 撰写综合财经报告
3. 提供投资建议
4. 生成数据可视化"""
        
        super().__init__(
            name=name,
            system_message=system_message,
            **kwargs
        )
    
    async def generate_report(self, analysis_results: Dict[str, Any], context: Optional['AnalysisContext'] = None) -> Dict[str, Any]:
        """生成最终报告"""
        logger.info("Generating final financial report")
        try:
            if context:
                context.log_agent_thought(
                    agent_name=self.name,
                    thought={
                        "action": "start_report",
                        "description": "Starting to generate comprehensive financial report",
                        "input_sources": {
                            "yahoo_data": bool(analysis_results.get("yahoo_data")),
                            "google_data": bool(analysis_results.get("google_data"))
                        }
                    }
                )

            yahoo_data = analysis_results.get("yahoo_data", {})
            google_data = analysis_results.get("google_data", {})
            
            # 整合市场数据
            market_data = yahoo_data.get("data", {}).get("market_data", {})
            
            # 整合新闻分析
            yahoo_news = yahoo_data.get("data", {}).get("news", [])
            google_news = google_data.get("data", {}).get("news_articles", [])
            
            # 分析市场趋势
            trends = yahoo_data.get("data", {}).get("trends", [])
            
            # 分析市场情绪
            sentiment = google_data.get("data", {}).get("sentiment", {})
            
            # 生成投资建议
            recommendations = []
            
            # 基于技术指标的建议
            for trend in trends:
                if trend.get("indicator") == "Price Trend":
                    recommendations.append(
                        f"Based on price trend analysis: {trend.get('value')} momentum with {trend.get('change')} change"
                    )
                elif trend.get("indicator") == "SMA Crossover":
                    recommendations.append(
                        f"Technical Analysis: {trend.get('value')} signal from SMA crossover"
                    )
            
            # 基于情绪分析的建议
            sentiment_score = sentiment.get("average_score", 0)
            if abs(sentiment_score) > 0.3:
                recommendations.append(
                    f"Market Sentiment: {sentiment.get('overall_sentiment')} with {sentiment.get('confidence'):.2f} confidence"
                )

            if context:
                context.log_agent_thought(
                    agent_name=self.name,
                    thought={
                        "action": "analysis_integration",
                        "findings": {
                            "technical_indicators": len(trends),
                            "news_sources": {
                                "yahoo": len(yahoo_news),
                                "google": len(google_news)
                            },
                            "recommendations_generated": len(recommendations)
                        }
                    }
                )
            
            # 生成报告摘要
            summary = f"""
Market Analysis Report for {yahoo_data.get('query')}

Current Market Status:
- Price: ${market_data.get('current_price', 'N/A'):,.2f}
- Volume: {market_data.get('volume', 'N/A'):,.0f}
- P/E Ratio: {market_data.get('pe_ratio', 'N/A')}
- Market Cap: ${market_data.get('market_cap', 'N/A'):,.2f}

Market Sentiment: {sentiment.get('overall_sentiment')}
Confidence Score: {sentiment.get('confidence', 0):.2f}

Key Events: {len(google_data.get('data', {}).get('events', []))} significant developments identified
            """
            
            # 准备最终报告
            result = {
                "report_type": "Financial Analysis",
                "timestamp": datetime.utcnow().isoformat(),
                "content": {
                    "summary": summary.strip(),
                    "detailed_analysis": {
                        "market_data": market_data,
                        "trends": trends,
                        "sentiment": sentiment,
                        "news_coverage": {
                            "yahoo": len(yahoo_news),
                            "google": len(google_news)
                        }
                    },
                    "recommendations": recommendations,
                    "visualizations": []  # 可以添加图表数据
                }
            }

            if context:
                context.log_agent_thought(
                    agent_name=self.name,
                    thought={
                        "action": "report_completion",
                        "summary": {
                            "report_sections": list(result["content"].keys()),
                            "total_recommendations": len(recommendations),
                            "analysis_completeness": "Full" if all([market_data, trends, sentiment]) else "Partial"
                        }
                    }
                )
                
                # 更新上下文
                context.update_context(self.name, result)

            return result
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise

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