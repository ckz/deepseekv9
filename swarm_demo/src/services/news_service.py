"""
News processing and sentiment analysis service.
"""
import os
from typing import Dict, Any, List
import logging
from datetime import datetime
from serpapi.google_search import GoogleSearch
from textblob import TextBlob

logger = logging.getLogger(__name__)

class NewsService:
    """Service for processing news and analyzing sentiment"""
    
    @staticmethod
    def get_google_news(query: str) -> Dict[str, Any]:
        """Get and analyze news from Google"""
        try:
            # Use SerpAPI to get news
            search = GoogleSearch({
                "q": query,
                "tbm": "nws",
                "api_key": os.getenv("SERPAPI_API_KEY")
            })
            results = search.get_dict()
            
            # Process news articles and analyze sentiment
            news_articles = []
            sentiments = []
            events = []
            
            if "news_results" in results:
                for article in results["news_results"]:
                    # Analyze sentiment
                    sentiment = TextBlob(article.get("title", "") + " " + article.get("snippet", ""))
                    sentiment_score = sentiment.sentiment.polarity
                    
                    # Process article
                    news_articles.append({
                        "title": article.get("title"),
                        "source": article.get("source"),
                        "published": article.get("date"),
                        "snippet": article.get("snippet"),
                        "link": article.get("link"),
                        "sentiment_score": sentiment_score
                    })
                    
                    sentiments.append(sentiment_score)
                    
                    # Identify significant events
                    if abs(sentiment_score) > 0.5:
                        events.append({
                            "type": "Significant News",
                            "title": article.get("title"),
                            "sentiment": "Positive" if sentiment_score > 0 else "Negative",
                            "score": sentiment_score
                        })
            
            # Calculate overall sentiment
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
            sentiment_analysis = {
                "average_score": avg_sentiment,
                "overall_sentiment": "Positive" if avg_sentiment > 0 else "Negative" if avg_sentiment < 0 else "Neutral",
                "confidence": abs(avg_sentiment)
            }
            
            return {
                "news_articles": news_articles,
                "sentiment": sentiment_analysis,
                "events": events
            }
            
        except Exception as e:
            logger.error(f"Error processing Google news: {str(e)}")
            raise

    @staticmethod
    def analyze_sentiment(text: str) -> Dict[str, Any]:
        """Analyze sentiment of a text"""
        try:
            sentiment = TextBlob(text)
            score = sentiment.sentiment.polarity
            
            return {
                "score": score,
                "sentiment": "Positive" if score > 0 else "Negative" if score < 0 else "Neutral",
                "confidence": abs(score)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            raise