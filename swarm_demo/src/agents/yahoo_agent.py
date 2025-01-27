"""
Yahoo Finance analysis agent.
"""
from typing import Dict, Any, Optional
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
            market_data = MarketService.get_stock_data(ticker)
            
            # 获取新闻数据
            stock = yf.Ticker(ticker)
            news = MarketService.process_stock_news(stock)
            
            # 准备结果
            result = {
                "source": "Yahoo Finance",
                "query": query,
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "news": news,
                    **market_data
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