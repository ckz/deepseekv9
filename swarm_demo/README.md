# Multi-Agent Financial News Analysis System Based on AutoGen

## System Architecture Overview
This system is built on the AutoGen framework, utilizing GroupChat and GroupChatManager to implement a multi-agent financial news analysis system. The system leverages AutoGen's advanced abstraction capabilities to achieve flexible agent interaction and task coordination.

## AutoGen Agent Design

### 1. GroupChatManager (Coordinator)
- **Implementation Class**: `autogen.GroupChatManager`
- **Main Responsibilities**:
  - Manage interactions between all agents in GroupChat
  - Control message flow and conversation sequence
  - Ensure task completion and goal achievement
  - Handle exceptions and conflict resolution

- **Configuration Parameters**:
```python
manager_config = {
    "name": "Research_Manager",
    "system_message": "You are a professional research project manager responsible for coordinating news analysis tasks...",
    "llm_config": {
        "temperature": 0.7,
        "request_timeout": 300
    }
}
```

### 2. Yahoo Finance Analyst
- **Implementation Class**: `autogen.AssistantAgent`
- **Configuration Example**:
```python
yahoo_analyst_config = {
    "name": "Yahoo_Analyst",
    "system_message": "You are a Yahoo Finance professional analyst responsible for collecting and analyzing financial data...",
    "llm_config": {
        "temperature": 0.3,
        "request_timeout": 120
    }
}
```
- **Implementation**:
```python
class YahooFinanceAgent(autogen.AssistantAgent):
    async def process_news(self, query):
        # Implements Yahoo Finance news retrieval and analysis logic
        pass
```

### 3. Google News Analyst
- **Implementation Class**: `autogen.AssistantAgent`
- **Configuration Example**:
```python
google_analyst_config = {
    "name": "Google_Analyst",
    "system_message": "You are a Google News professional analyst responsible for retrieving and analyzing news through SerpAPI...",
    "llm_config": {
        "temperature": 0.3,
        "request_timeout": 120
    }
}
```
- **Implementation**:
```python
class GoogleNewsAgent(autogen.AssistantAgent):
    async def analyze_news(self, query):
        # Implements Google news analysis logic
        pass
```

### 4. Financial Report Writer
- **Implementation Class**: `autogen.AssistantAgent`
- **Configuration Example**:
```python
report_writer_config = {
    "name": "Report_Writer",
    "system_message": "You are a professional financial report writing expert responsible for integrating analysis results and generating reports...",
    "llm_config": {
        "temperature": 0.4,
        "request_timeout": 180
    }
}
```
- **Implementation**:
```python
class ReportWriterAgent(autogen.AssistantAgent):
    async def generate_report(self, analysis_results):
        # Implements report generation logic
        pass
```

## System Implementation Example

### 1. GroupChat Initialization
```python
from autogen import GroupChat, GroupChatManager

# Create Agents
manager = GroupChatManager(**manager_config)
yahoo_analyst = YahooFinanceAgent(**yahoo_analyst_config)
google_analyst = GoogleNewsAgent(**google_analyst_config)
report_writer = ReportWriterAgent(**report_writer_config)

# Create GroupChat
group_chat = GroupChat(
    agents=[manager, yahoo_analyst, google_analyst, report_writer],
    messages=[],
    max_round=50
)
```

### 2. Task Execution Flow
```python
async def run_analysis(topic: str):
    # Initialize task
    chat_manager = GroupChatManager(groupchat=group_chat)
    
    # Start analysis process
    await chat_manager.run(
        initial_message=f"Start analyzing topic: {topic}",
        sender=manager
    )
```

## Workflow Details

1. **Initialization Phase**
```python
# Configure environment variables
os.environ["SERPAPI_API_KEY"] = "your_serp_api_key"
os.environ["YAHOO_FINANCE_API_KEY"] = "your_yahoo_api_key"

# Initialize system
async def initialize_system():
    # Create all necessary Agent instances
    agents = create_agents()
    # Set up GroupChat
    group_chat = setup_group_chat(agents)
    return group_chat
```

2. **Data Collection Phase**
```python
async def collect_data(topic: str):
    # Yahoo Finance data collection
    yahoo_data = await yahoo_analyst.process_news(topic)
    
    # Google News data collection
    google_data = await google_analyst.analyze_news(topic)
    
    return yahoo_data, google_data
```

3. **Analysis and Report Generation**
```python
async def generate_final_report(yahoo_data, google_data):
    # Integrate data
    combined_data = {
        "yahoo_analysis": yahoo_data,
        "google_analysis": google_data
    }
    
    # Generate report
    final_report = await report_writer.generate_report(combined_data)
    return final_report
```

## Configuration Requirements

### 1. Environment Dependencies
```txt
pyautogen>=0.2.0
python-dotenv>=0.19.0
serpapi>=0.1.0
yfinance>=0.1.70
pandas>=1.3.0
```

### 2. API Configuration
```python
# .env file configuration
SERPAPI_API_KEY=your_serp_api_key
YAHOO_FINANCE_API_KEY=your_yahoo_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Error Handling Mechanism

```python
class ErrorHandler:
    @staticmethod
    async def handle_api_error(error, agent):
        # Implement error handling logic
        pass

    @staticmethod
    async def retry_operation(func, max_retries=3):
        # Implement retry logic
        pass
```

## Extensibility Design

1. **Adding New Agents**
```python
# Create new specialist Agent
class NewSpecialistAgent(autogen.AssistantAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add specific functionality
```

2. **Custom Analysis Rules**
```python
class AnalysisRules:
    @staticmethod
    def add_custom_rule(rule_name, rule_function):
        # Implement rule addition logic
        pass
```

## Monitoring and Logging

```python
class SystemMonitor:
    @staticmethod
    async def log_agent_activity(agent, action):
        # Implement logging
        pass

    @staticmethod
    async def monitor_performance():
        # Implement performance monitoring
        pass
```

## Agent Thought Chain Tracking System

The system implements a complete agent thought chain tracking mechanism that records and analyzes each agent's decision-making process.

### 1. Thought Chain Recorder

```python
from utils import ThoughtLogger, AnalysisContext

# Create analysis context
context = AnalysisContext("Tesla Q4 2024 Earnings")

# Record Agent thoughts
context.log_agent_thought(
    agent_name="Yahoo_Analyst",
    thought={
        "action": "market_analysis",
        "findings": {
            "price_trend": "Up 2.5%",
            "technical_indicators": {
                "sma20": "180.50",
                "sma50": "165.75",
                "trend": "Bullish"
            }
        }
    }
)
```

### 2. Thought Chain Storage Format

Thought chains are stored in JSON format in the logs directory, with file naming format:
```
YYYYMMDD_AgentName_AnalysisID_thoughts.json
```

Example content:
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
                    "price_trend": "Up 2.5%",
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

### 3. Usage Example

Basic usage:
```python
from main import run_sync

# Run analysis (automatically includes thought chain recording)
result = run_sync("TSLA")

# Access thought chain data
thought_chains = result["thought_chains"]

# View analysis steps for each Agent
print(f"Yahoo Finance analysis steps: {len(thought_chains['yahoo']['thoughts'])}")
print(f"Google News analysis steps: {len(thought_chains['google']['thoughts'])}")
print(f"Report generation steps: {len(thought_chains['writer']['thoughts'])}")

# View specific analysis process
for thought in thought_chains['yahoo']['thoughts']:
    print(f"Step {thought['step']}: {thought['content']['action']}")
    if 'findings' in thought['content']:
        print(f"Findings: {thought['content']['findings']}")
```

Advanced usage:
```python
# Custom analysis context
context = AnalysisContext("TSLA")

# Yahoo Finance analysis
yahoo_data = await agents["yahoo"].process_news("TSLA", context)

# Get Yahoo analysis thought chain
yahoo_thoughts = context.get_agent_thoughts("Yahoo_Analyst")

# Analyze decision process
for thought in yahoo_thoughts["thoughts"]:
    if thought["content"]["action"] == "market_analysis":
        print(f"Market trend: {thought['content']['findings']['price_trend']}")
        print(f"Technical indicators: {thought['content']['findings']['technical_indicators']}")
```

### 4. Thought Chain Analysis Tools

```python
class ThoughtChainAnalyzer:
    @staticmethod
    def analyze_decision_process(thought_chain):
        """Analyze key points in the decision process"""
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
        """Generate summary of multiple Agents' analyses"""
        return {
            agent: {
                "total_steps": len(chain["thoughts"]),
                "key_decisions": len([t for t in chain["thoughts"] if "findings" in t["content"]])
            }
            for agent, chain in thought_chains.items()
        }
```

## Usage Example

```python
async def main():
    # Initialize system
    group_chat = await initialize_system()
    
    # Set analysis topic
    topic = "Tesla Q4 2024 Earnings"
    
    # Run analysis
    await run_analysis(topic)
    
    # Get results
    final_report = await get_final_report()
    
    return final_report

if __name__ == "__main__":
    import asyncio
    report = asyncio.run(main())