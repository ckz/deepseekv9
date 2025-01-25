import requests
from typing import List, Dict
import os

class AIAgent:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.system_prompt = """You are a helpful AI assistant that analyzes web content. 
        Your task is to summarize and analyze the provided content, extracting key insights 
        and providing a comprehensive analysis."""

    def analyze(self, content: List[Dict[str, str]]) -> str:
        """Analyze crawled content using AI"""
        formatted_content = "\n\n".join(
            f"Title: {item['title']}\nContent: {item['content'][:2000]}..."
            for item in content
        )
        
        try:
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Analyze this content:\n{formatted_content}"}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Analysis failed: {str(e)}"
