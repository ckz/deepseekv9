# AI Agent with Search Capabilities

This project demonstrates the integration of SerpApi for web search and OpenRouter for AI analysis capabilities.

## Setup

1. Create a `.env` file based on `.env.template`:
```bash
cp .env.template .env
```

2. Add your API keys to the `.env` file:
```
SEARCH_API_KEY="de80447f7a71861ca7a198bd5fbfe8fe46d061afd02988200064f9cb76fc0372"
OPENROUTER_API_KEY="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"
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
python src/main.py
```

The script will prompt you for:
1. A search query
2. Number of results to analyze (optional, default=5)
3. Custom analysis prompt (optional)

### Example Usage:

```python
from ai_agent import AIAgent

# Initialize the agent
agent = AIAgent()

# Simple search and analysis
results = agent.search_and_analyze(
    query="Latest developments in AI",
    num_results=5
)

# Search with custom analysis prompt
results = agent.search_and_analyze(
    query="Climate change solutions",
    num_results=3,
    custom_prompt="Analyze these results focusing on technological innovations:"
)
```

## Features

- Web search using SerpApi
- AI analysis using OpenRouter API
- Customizable number of search results
- Custom analysis prompts
- Error handling and result formatting
- Interactive command-line interface

## API Reference

### AIAgent Class

#### Methods:

1. `search(query: str, num_results: int = 5) -> List[Dict[str, str]]`
   - Performs web search using SerpApi
   - Returns list of search results with title, snippet, and link

2. `analyze(content: List[Dict[str, str]], custom_prompt: Optional[str] = None) -> str`
   - Analyzes content using OpenRouter API
   - Returns AI-generated analysis

3. `search_and_analyze(query: str, num_results: int = 5, custom_prompt: Optional[str] = None) -> Dict[str, any]`
   - Combines search and analysis in one call
   - Returns dictionary with search results and analysis