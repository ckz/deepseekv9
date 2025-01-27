"""
Utility functions for the financial news analysis system.
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class ThoughtLogger:
    """Agent思维链记录器"""
    
    def __init__(self, log_dir: str = "logs"):
        """
        初始化思维链记录器
        
        Args:
            log_dir: 日志文件存储目录
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置日志记录器
        self.logger = logging.getLogger(__name__)
        
    def _get_log_path(self, agent_name: str, analysis_id: str) -> Path:
        """获取日志文件路径"""
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        return self.log_dir / f"{timestamp}_{agent_name}_{analysis_id}_thoughts.json"
    
    def log_thought(
        self,
        agent_name: str,
        analysis_id: str,
        thought: Dict[str, Any],
        step: Optional[int] = None
    ) -> None:
        """
        记录Agent的思维步骤
        
        Args:
            agent_name: Agent名称
            analysis_id: 分析任务ID
            thought: 思维内容
            step: 步骤编号（可选）
        """
        try:
            log_path = self._get_log_path(agent_name, analysis_id)
            
            # 读取现有日志
            if log_path.exists():
                with open(log_path, 'r', encoding='utf-8') as f:
                    thoughts = json.load(f)
            else:
                thoughts = {
                    "agent": agent_name,
                    "analysis_id": analysis_id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "thoughts": []
                }
            
            # 添加新思维
            thought_entry = {
                "step": step if step is not None else len(thoughts["thoughts"]) + 1,
                "timestamp": datetime.utcnow().isoformat(),
                "content": thought
            }
            thoughts["thoughts"].append(thought_entry)
            
            # 保存日志
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(thoughts, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"Thought logged for {agent_name} in {log_path}")
            
        except Exception as e:
            self.logger.error(f"Error logging thought: {str(e)}")
            raise

    def get_thought_chain(
        self,
        agent_name: str,
        analysis_id: str
    ) -> Dict[str, Any]:
        """
        获取Agent的完整思维链
        
        Args:
            agent_name: Agent名称
            analysis_id: 分析任务ID
            
        Returns:
            包含完整思维链的字典
        """
        try:
            log_path = self._get_log_path(agent_name, analysis_id)
            
            if not log_path.exists():
                return {
                    "agent": agent_name,
                    "analysis_id": analysis_id,
                    "thoughts": []
                }
            
            with open(log_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f"Error reading thought chain: {str(e)}")
            raise

class AnalysisContext:
    """分析上下文管理器"""
    
    def __init__(self, topic: str):
        """
        初始化分析上下文
        
        Args:
            topic: 分析主题
        """
        self.topic = topic
        self.analysis_id = self._generate_analysis_id()
        self.thought_logger = ThoughtLogger()
        self.context = {
            "analysis_id": self.analysis_id,
            "topic": topic,
            "start_time": datetime.utcnow().isoformat(),
            "agents": {}
        }
    
    def _generate_analysis_id(self) -> str:
        """生成分析任务ID"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{self.topic.replace(' ', '_')}"
    
    def log_agent_thought(
        self,
        agent_name: str,
        thought: Dict[str, Any],
        step: Optional[int] = None
    ) -> None:
        """记录Agent思维"""
        self.thought_logger.log_thought(
            agent_name=agent_name,
            analysis_id=self.analysis_id,
            thought=thought,
            step=step
        )
    
    def get_agent_thoughts(self, agent_name: str) -> Dict[str, Any]:
        """获取Agent思维链"""
        return self.thought_logger.get_thought_chain(
            agent_name=agent_name,
            analysis_id=self.analysis_id
        )
    
    def update_context(self, agent_name: str, data: Dict[str, Any]) -> None:
        """更新上下文数据"""
        self.context["agents"][agent_name] = {
            "last_update": datetime.utcnow().isoformat(),
            "data": data
        }
    
    def get_context(self) -> Dict[str, Any]:
        """获取完整上下文"""
        return self.context