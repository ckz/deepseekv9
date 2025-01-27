"""
Yahoo Finance analysis agent.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import yfinance as yf
from .base_agent import BaseAgent
from services.market_service import MarketService
import logging

logger = logging.getLogger(__name__)

class YahooFinanceAgent(BaseAgent):
    """Yahoo Finance news analyst Agent"""
    
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
        
        # 定义agent能力
        self.capabilities = {
            "process_news": "Analyze financial news and market data from Yahoo Finance",
            "get_market_data": "Retrieve specific market data for a given ticker",
            "analyze_trends": "Analyze market trends and patterns"
        }
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tasks within the SWARM network"""
        action = task.get("action")
        params = task.get("params", {})
        context = params.get("context")
        
        if action == "process_news":
            return await self.process_news(params.get("topic"), context)
        elif action == "get_market_data":
            return await self.get_market_data(params.get("ticker"), context)
        elif action == "analyze_trends":
            return await self.analyze_trends(params.get("data"), context)
        else:
            raise ValueError(f"Unknown action: {action}")

    async def process_news(self, query: str, context: Optional['AnalysisContext'] = None) -> Dict[str, Any]:
        """处理Yahoo Finance新闻数据"""
        logger.info(f"Processing Yahoo Finance news for query: {query}")
        try:
            self._log_context(context, "start_processing", {
                "query": query,
                "description": "Starting to process Yahoo Finance data"
            })
            
            # 获取股票代码
            company_to_ticker = {
                "Tesla": "TSLA",
                "Apple": "AAPL",
                "Microsoft": "MSFT",
                "Google": "GOOGL",
                "Amazon": "AMZN"
            }
            company = query.split()[0]
            ticker = company_to_ticker.get(company, company)
            
            # 使用MarketService获取市场数据
            market_data = await self.get_market_data(ticker, context)
            
            # 获取新闻数据
            stock = yf.Ticker(ticker)
            news = MarketService.process_stock_news(stock)
            
            # 分析趋势
            trends_analysis = await self.analyze_trends(market_data, context)
            
            # 准备结果
            result = {
                "source": "Yahoo Finance",
                "query": query,
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "news": news,
                    **market_data,
                    "trends_analysis": trends_analysis
                }
            }

            if context:
                # 记录市场数据分析思维
                self._log_context(context, "market_analysis", {
                    "findings": {
                        "price_trend": market_data["trends"][0]["change"],
                        "technical_indicators": market_data["technical_indicators"],
                        "news_count": len(news)
                    }
                })
                
                # 更新上下文
                self._update_context(context, result)

            return result
            
        except Exception as e:
            self._handle_error(e, "processing Yahoo Finance news")
    
    async def get_market_data(self, ticker: str, context: Optional['AnalysisContext'] = None) -> Dict[str, Any]:
        """获取市场数据"""
        try:
            self._log_context(context, "get_market_data", {
                "ticker": ticker,
                "description": "Retrieving market data"
            })
            
            market_data = MarketService.get_stock_data(ticker)
            return market_data
            
        except Exception as e:
            self._handle_error(e, "getting market data")
    
    async def analyze_trends(self, data: Dict[str, Any], context: Optional['AnalysisContext'] = None) -> Dict[str, Any]:
        """分析市场趋势"""
        try:
            self._log_context(context, "analyze_trends", {
                "description": "Analyzing market trends"
            })
            
            trends = data.get("trends", [])
            indicators = data.get("technical_indicators", {})
            
            analysis = {
                "trend_summary": self._summarize_trends(trends),
                "indicator_signals": self._analyze_indicators(indicators),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            self._handle_error(e, "analyzing trends")
    
    def _summarize_trends(self, trends: List[Dict[str, Any]]) -> str:
        """总结趋势"""
        if not trends:
            return "No trend data available"
            
        latest_trend = trends[0]
        return f"Price {latest_trend['direction']} by {latest_trend['change']}%"
    
    def _analyze_indicators(self, indicators: Dict[str, Any]) -> Dict[str, str]:
        """分析技术指标"""
        signals = {}
        for indicator, value in indicators.items():
            if indicator == "RSI":
                signals[indicator] = "Overbought" if value > 70 else "Oversold" if value < 30 else "Neutral"
            elif indicator == "MACD":
                signals[indicator] = "Bullish" if value > 0 else "Bearish"
        return signals