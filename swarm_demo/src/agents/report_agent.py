"""
Financial report writer agent.
"""
from typing import Dict, Any, Optional, List
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
        
        # 定义agent能力
        self.capabilities = {
            "generate_report": "Generate comprehensive financial report",
            "analyze_market_data": "Analyze and summarize market data",
            "generate_recommendations": "Generate investment recommendations",
            "create_visualizations": "Create data visualizations",
            "integrate_analyses": "Integrate analyses from multiple sources"
        }
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tasks within the SWARM network"""
        action = task.get("action")
        params = task.get("params", {})
        context = params.get("context")
        
        if action == "generate_report":
            return await self.generate_report(params.get("analysis_results"), context)
        elif action == "analyze_market_data":
            return await self.analyze_market_data(params.get("market_data"), context)
        elif action == "generate_recommendations":
            return await self.generate_recommendations(params.get("trends"), params.get("sentiment"), context)
        elif action == "create_visualizations":
            return await self.create_visualizations(params.get("data"), context)
        elif action == "integrate_analyses":
            return await self.integrate_analyses(params.get("analyses"), context)
        else:
            raise ValueError(f"Unknown action: {action}")

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

            # 分析市场数据
            market_analysis = await self.analyze_market_data(
                analysis_results.get("yahoo_data", {}).get("data", {}),
                context
            )
            
            # 整合多源分析
            integrated_analysis = await self.integrate_analyses({
                "market": market_analysis,
                "yahoo_data": analysis_results.get("yahoo_data", {}),
                "google_data": analysis_results.get("google_data", {})
            }, context)
            
            # 生成投资建议
            recommendations = await self.generate_recommendations(
                integrated_analysis.get("trends", []),
                integrated_analysis.get("sentiment", {}),
                context
            )
            
            # 创建可视化
            visualizations = await self.create_visualizations(integrated_analysis, context)
            
            # 准备最终报告
            result = {
                "report_type": "Financial Analysis",
                "timestamp": datetime.utcnow().isoformat(),
                "content": {
                    "summary": integrated_analysis["summary"].strip(),
                    "detailed_analysis": integrated_analysis["detailed"],
                    "recommendations": recommendations,
                    "visualizations": visualizations
                }
            }

            if context:
                self._log_context(context, "report_completion", {
                    "summary": {
                        "report_sections": list(result["content"].keys()),
                        "total_recommendations": len(recommendations),
                        "analysis_completeness": integrated_analysis["completeness"]
                    }
                })
                
                self._update_context(context, result)

            return result
            
        except Exception as e:
            self._handle_error(e, "generating report")
    
    async def analyze_market_data(self, market_data: Dict[str, Any], context: Optional['AnalysisContext'] = None) -> Dict[str, Any]:
        """分析市场数据"""
        try:
            self._log_context(context, "analyze_market", {
                "description": "Analyzing market data"
            })
            
            return {
                "price_analysis": {
                    "current_price": market_data.get("current_price"),
                    "volume": market_data.get("volume"),
                    "pe_ratio": market_data.get("pe_ratio"),
                    "market_cap": market_data.get("market_cap")
                },
                "technical_indicators": market_data.get("technical_indicators", {}),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            self._handle_error(e, "analyzing market data")
    
    async def generate_recommendations(self, trends: List[Dict[str, Any]], 
                                    sentiment: Dict[str, Any], 
                                    context: Optional['AnalysisContext'] = None) -> List[str]:
        """生成投资建议"""
        try:
            self._log_context(context, "generate_recommendations", {
                "description": "Generating investment recommendations"
            })
            
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
            
        except Exception as e:
            self._handle_error(e, "generating recommendations")
    
    async def create_visualizations(self, data: Dict[str, Any], context: Optional['AnalysisContext'] = None) -> List[Dict[str, Any]]:
        """创建数据可视化"""
        try:
            self._log_context(context, "create_visualizations", {
                "description": "Creating data visualizations"
            })
            
            # 这里可以实现实际的可视化逻辑
            visualizations = []
            
            return visualizations
            
        except Exception as e:
            self._handle_error(e, "creating visualizations")
    
    async def integrate_analyses(self, analyses: Dict[str, Any], context: Optional['AnalysisContext'] = None) -> Dict[str, Any]:
        """整合多源分析"""
        try:
            self._log_context(context, "integrate_analyses", {
                "description": "Integrating analyses from multiple sources"
            })
            
            yahoo_data = analyses.get("yahoo_data", {})
            google_data = analyses.get("google_data", {})
            market_analysis = analyses.get("market", {})
            
            # 整合市场数据
            market_data = yahoo_data.get("data", {}).get("market_data", {})
            
            # 整合新闻分析
            yahoo_news = yahoo_data.get("data", {}).get("news", [])
            google_news = google_data.get("data", {}).get("news_articles", [])
            
            # 分析市场趋势
            trends = yahoo_data.get("data", {}).get("trends", [])
            
            # 分析市场情绪
            sentiment = google_data.get("data", {}).get("sentiment", {})
            
            # 生成摘要
            summary = self._generate_summary(
                yahoo_data.get("query", "Unknown"),
                market_data,
                sentiment,
                google_data
            )
            
            return {
                "summary": summary,
                "detailed": {
                    "market_data": market_analysis.get("price_analysis", {}),
                    "technical_indicators": market_analysis.get("technical_indicators", {}),
                    "trends": trends,
                    "sentiment": sentiment,
                    "news_coverage": {
                        "yahoo": len(yahoo_news),
                        "google": len(google_news)
                    }
                },
                "trends": trends,
                "sentiment": sentiment,
                "completeness": "Full" if all([market_data, trends, sentiment]) else "Partial",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self._handle_error(e, "integrating analyses")
    
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