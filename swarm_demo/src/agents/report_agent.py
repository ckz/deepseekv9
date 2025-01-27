"""
Financial report writer agent.
"""
from typing import Dict, Any, Optional
from datetime import datetime
from .base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)

class ReportWriterAgent(BaseAgent):
    """Financial report writer Agent"""
    
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
            self._log_context(context, "start_report", {
                "description": "Starting to generate comprehensive financial report",
                "input_sources": {
                    "yahoo_data": bool(analysis_results.get("yahoo_data")),
                    "google_data": bool(analysis_results.get("google_data"))
                }
            })

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
            recommendations = self._generate_recommendations(trends, sentiment)
            
            # 生成报告摘要
            summary = self._generate_summary(yahoo_data.get("query"), market_data, sentiment, google_data)
            
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
                self._log_context(context, "report_completion", {
                    "summary": {
                        "report_sections": list(result["content"].keys()),
                        "total_recommendations": len(recommendations),
                        "analysis_completeness": "Full" if all([market_data, trends, sentiment]) else "Partial"
                    }
                })
                
                self._update_context(context, result)

            return result
            
        except Exception as e:
            self._handle_error(e, "generating report")
    
    def _generate_recommendations(self, trends: list, sentiment: Dict[str, Any]) -> list:
        """生成投资建议"""
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
        
        return recommendations
    
    def _generate_summary(self, query: str, market_data: Dict[str, Any], 
                         sentiment: Dict[str, Any], google_data: Dict[str, Any]) -> str:
        """生成报告摘要"""
        return f"""
Market Analysis Report for {query}

Current Market Status:
- Price: ${market_data.get('current_price', 'N/A'):,.2f}
- Volume: {market_data.get('volume', 'N/A'):,.0f}
- P/E Ratio: {market_data.get('pe_ratio', 'N/A')}
- Market Cap: ${market_data.get('market_cap', 'N/A'):,.2f}

Market Sentiment: {sentiment.get('overall_sentiment')}
Confidence Score: {sentiment.get('confidence', 0):.2f}

Key Events: {len(google_data.get('data', {}).get('events', []))} significant developments identified
"""