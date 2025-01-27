# 基于AutoGen的多Agent财经新闻分析系统

## 系统架构概述
该系统基于AutoGen框架构建，利用GroupChat和GroupChatManager实现多Agent协作的财经新闻分析系统。系统采用AutoGen的高级抽象能力，实现灵活的Agent交互和任务协调。

## AutoGen Agent设计

### 1. GroupChatManager (调度员)
- **实现类**: `autogen.GroupChatManager`
- **主要职责**:
  - 管理GroupChat中所有Agent的交互
  - 控制消息流转和对话顺序
  - 确保任务完成和目标达成
  - 处理异常情况和冲突解决

- **配置参数**:
```python
manager_config = {
    "name": "Research_Manager",
    "system_message": "你是一个专业的研究项目经理，负责协调新闻分析任务...",
    "llm_config": {
        "temperature": 0.7,
        "request_timeout": 300
    }
}
```

### 2. Yahoo Finance分析师
- **实现类**: `autogen.AssistantAgent`
- **配置示例**:
```python
yahoo_analyst_config = {
    "name": "Yahoo_Analyst",
    "system_message": "你是Yahoo Finance的专业分析师，负责收集和分析财经数据...",
    "llm_config": {
        "temperature": 0.3,
        "request_timeout": 120
    }
}
```
- **功能实现**:
```python
class YahooFinanceAgent(autogen.AssistantAgent):
    async def process_news(self, query):
        # 实现Yahoo Finance新闻获取和分析逻辑
        pass
```

### 3. Google News分析师
- **实现类**: `autogen.AssistantAgent`
- **配置示例**:
```python
google_analyst_config = {
    "name": "Google_Analyst",
    "system_message": "你是Google新闻的专业分析师，负责通过SerpAPI获取和分析新闻...",
    "llm_config": {
        "temperature": 0.3,
        "request_timeout": 120
    }
}
```
- **功能实现**:
```python
class GoogleNewsAgent(autogen.AssistantAgent):
    async def analyze_news(self, query):
        # 实现Google新闻分析逻辑
        pass
```

### 4. 财经报告撰写员
- **实现类**: `autogen.AssistantAgent`
- **配置示例**:
```python
report_writer_config = {
    "name": "Report_Writer",
    "system_message": "你是专业的财经报告撰写专家，负责整合分析结果并生成报告...",
    "llm_config": {
        "temperature": 0.4,
        "request_timeout": 180
    }
}
```
- **功能实现**:
```python
class ReportWriterAgent(autogen.AssistantAgent):
    async def generate_report(self, analysis_results):
        # 实现报告生成逻辑
        pass
```

## 系统实现示例

### 1. GroupChat初始化
```python
from autogen import GroupChat, GroupChatManager

# 创建Agents
manager = GroupChatManager(**manager_config)
yahoo_analyst = YahooFinanceAgent(**yahoo_analyst_config)
google_analyst = GoogleNewsAgent(**google_analyst_config)
report_writer = ReportWriterAgent(**report_writer_config)

# 创建GroupChat
group_chat = GroupChat(
    agents=[manager, yahoo_analyst, google_analyst, report_writer],
    messages=[],
    max_round=50
)
```

### 2. 任务执行流程
```python
async def run_analysis(topic: str):
    # 初始化任务
    chat_manager = GroupChatManager(groupchat=group_chat)
    
    # 启动分析流程
    await chat_manager.run(
        initial_message=f"开始分析主题: {topic}",
        sender=manager
    )
```

## 工作流程详解

1. **初始化阶段**
```python
# 配置环境变量
os.environ["SERPAPI_API_KEY"] = "your_serp_api_key"
os.environ["YAHOO_FINANCE_API_KEY"] = "your_yahoo_api_key"

# 初始化系统
async def initialize_system():
    # 创建所有必要的Agent实例
    agents = create_agents()
    # 设置GroupChat
    group_chat = setup_group_chat(agents)
    return group_chat
```

2. **数据收集阶段**
```python
async def collect_data(topic: str):
    # Yahoo Finance数据收集
    yahoo_data = await yahoo_analyst.process_news(topic)
    
    # Google News数据收集
    google_data = await google_analyst.analyze_news(topic)
    
    return yahoo_data, google_data
```

3. **分析和报告生成**
```python
async def generate_final_report(yahoo_data, google_data):
    # 整合数据
    combined_data = {
        "yahoo_analysis": yahoo_data,
        "google_analysis": google_data
    }
    
    # 生成报告
    final_report = await report_writer.generate_report(combined_data)
    return final_report
```

## 配置要求

### 1. 环境依赖
```txt
pyautogen>=0.2.0
python-dotenv>=0.19.0
serpapi>=0.1.0
yfinance>=0.1.70
pandas>=1.3.0
```

### 2. API配置
```python
# .env文件配置
SERPAPI_API_KEY=your_serp_api_key
YAHOO_FINANCE_API_KEY=your_yahoo_api_key
OPENAI_API_KEY=your_openai_api_key
```

## 错误处理机制

```python
class ErrorHandler:
    @staticmethod
    async def handle_api_error(error, agent):
        # 实现错误处理逻辑
        pass

    @staticmethod
    async def retry_operation(func, max_retries=3):
        # 实现重试逻辑
        pass
```

## 扩展性设计

1. **添加新Agent**
```python
# 创建新的专业Agent
class NewSpecialistAgent(autogen.AssistantAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 添加特定功能
```

2. **自定义分析规则**
```python
class AnalysisRules:
    @staticmethod
    def add_custom_rule(rule_name, rule_function):
        # 实现规则添加逻辑
        pass
```

## 监控和日志

```python
class SystemMonitor:
    @staticmethod
    async def log_agent_activity(agent, action):
        # 实现日志记录
        pass

    @staticmethod
    async def monitor_performance():
        # 实现性能监控
        pass
```

## Agent思维链追踪系统

系统实现了完整的Agent思维链追踪机制，可以记录和分析每个Agent的决策过程。

### 1. 思维链记录器

```python
from utils import ThoughtLogger, AnalysisContext

# 创建分析上下文
context = AnalysisContext("Tesla Q4 2024 Earnings")

# 记录Agent思维
context.log_agent_thought(
    agent_name="Yahoo_Analyst",
    thought={
        "action": "market_analysis",
        "findings": {
            "price_trend": "上涨2.5%",
            "technical_indicators": {
                "sma20": "180.50",
                "sma50": "165.75",
                "trend": "Bullish"
            }
        }
    }
)
```

### 2. 思维链存储格式

思维链以JSON格式存储在logs目录下，文件命名格式：
```
YYYYMMDD_AgentName_AnalysisID_thoughts.json
```

示例内容：
```json
{
    "agent": "Yahoo_Analyst",
    "analysis_id": "20240127_042159_Tesla_Q4_2024_Earnings",
    "timestamp": "2024-01-27T04:21:59.123456",
    "thoughts": [
        {
            "step": 1,
            "timestamp": "2024-01-27T04:21:59.123456",
            "content": {
                "action": "start_processing",
                "query": "TSLA",
                "description": "Starting to process Yahoo Finance data"
            }
        },
        {
            "step": 2,
            "timestamp": "2024-01-27T04:22:00.234567",
            "content": {
                "action": "market_analysis",
                "findings": {
                    "price_trend": "上涨2.5%",
                    "technical_indicators": {
                        "sma20": "180.50",
                        "sma50": "165.75"
                    }
                }
            }
        }
    ]
}
```

### 3. 使用示例

基本使用：
```python
from main import run_sync

# 运行分析（自动包含思维链记录）
result = run_sync("TSLA")

# 访问思维链数据
thought_chains = result["thought_chains"]

# 查看各Agent的分析步骤
print(f"Yahoo Finance分析步骤: {len(thought_chains['yahoo']['thoughts'])}")
print(f"Google News分析步骤: {len(thought_chains['google']['thoughts'])}")
print(f"报告生成步骤: {len(thought_chains['writer']['thoughts'])}")

# 查看具体分析过程
for thought in thought_chains['yahoo']['thoughts']:
    print(f"步骤 {thought['step']}: {thought['content']['action']}")
    if 'findings' in thought['content']:
        print(f"发现: {thought['content']['findings']}")
```

高级用法：
```python
# 自定义分析上下文
context = AnalysisContext("TSLA")

# Yahoo Finance分析
yahoo_data = await agents["yahoo"].process_news("TSLA", context)

# 获取Yahoo分析思维链
yahoo_thoughts = context.get_agent_thoughts("Yahoo_Analyst")

# 分析决策过程
for thought in yahoo_thoughts["thoughts"]:
    if thought["content"]["action"] == "market_analysis":
        print(f"市场趋势: {thought['content']['findings']['price_trend']}")
        print(f"技术指标: {thought['content']['findings']['technical_indicators']}")
```

### 4. 思维链分析工具

```python
class ThoughtChainAnalyzer:
    @staticmethod
    def analyze_decision_process(thought_chain):
        """分析决策过程的关键节点"""
        key_decisions = []
        for thought in thought_chain["thoughts"]:
            if "findings" in thought["content"]:
                key_decisions.append({
                    "timestamp": thought["timestamp"],
                    "action": thought["content"]["action"],
                    "findings": thought["content"]["findings"]
                })
        return key_decisions

    @staticmethod
    def get_analysis_summary(thought_chains):
        """生成多个Agent的分析总结"""
        return {
            agent: {
                "total_steps": len(chain["thoughts"]),
                "key_decisions": len([t for t in chain["thoughts"] if "findings" in t["content"]])
            }
            for agent, chain in thought_chains.items()
        }
```

## 使用示例

```python
async def main():
    # 初始化系统
    group_chat = await initialize_system()
    
    # 设置分析主题
    topic = "Tesla Q4 2024 Earnings"
    
    # 运行分析
    await run_analysis(topic)
    
    # 获取结果
    final_report = await get_final_report()
    
    return final_report

if __name__ == "__main__":
    import asyncio
    report = asyncio.run(main())