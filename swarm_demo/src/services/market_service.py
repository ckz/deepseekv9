"""
Market data processing service.
"""
import yfinance as yf
from typing import Dict, Any, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MarketService:
    """Service for processing market data"""
    
    @staticmethod
    def get_stock_data(ticker: str) -> Dict[str, Any]:
        """Get stock market data from Yahoo Finance"""
        try:
            stock = yf.Ticker(ticker)
            
            # Get stock information
            info = stock.info
            
            # Get historical data
            hist = stock.history(period="1mo")
            
            # Calculate technical indicators
            sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
            
            # Calculate price change
            current_price = hist['Close'].iloc[-1]
            price_change = ((current_price - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
            
            # Process market trends
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
            
            return {
                "market_data": {
                    "current_price": current_price,
                    "volume": hist['Volume'].iloc[-1],
                    "market_cap": info.get('marketCap'),
                    "pe_ratio": info.get('forwardPE'),
                    "dividend_yield": info.get('dividendYield')
                },
                "trends": trends,
                "technical_indicators": {
                    "sma20": sma_20,
                    "sma50": sma_50
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting stock data: {str(e)}")
            raise

    @staticmethod
    def process_stock_news(stock: yf.Ticker) -> List[Dict[str, Any]]:
        """Process news data from Yahoo Finance"""
        try:
            news = stock.news
            processed_news = []
            
            for article in news[:10]:  # Process latest 10 news items
                processed_news.append({
                    "title": article.get("title"),
                    "publisher": article.get("publisher"),
                    "link": article.get("link"),
                    "published": article.get("providerPublishTime"),
                    "type": article.get("type")
                })
            
            return processed_news
            
        except Exception as e:
            logger.error(f"Error processing stock news: {str(e)}")
            raise