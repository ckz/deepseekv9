from openai import OpenAI
from typing import List, Dict
import os

class AIAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
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
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Analyze this content:\n{formatted_content}"}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Analysis failed: {str(e)}"
