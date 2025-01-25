import requests
from typing import List, Dict, Optional
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

class AIAgent:
    def __init__(self):
        load_dotenv()
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        self.serpapi_key = os.getenv('SEARCH_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        self.system_prompt = """You are a helpful AI assistant with web search capabilities.
        Your task is to provide accurate and relevant information by combining web search results
        with your analytical capabilities. When analyzing content, focus on extracting key insights
        and maintaining factual accuracy."""

    def search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Perform web search using SerpApi"""
        try:
            search = GoogleSearch({
                "q": query,
                "api_key": self.serpapi_key,
                "num": num_results
            })
            results = search.get_dict()
            
            # Extract organic search results
            search_results = []
            if "organic_results" in results:
                for result in results["organic_results"][:num_results]:
                    search_results.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("snippet", ""),
                        "link": result.get("link", "")
                    })
            return search_results
        except Exception as e:
            print(f"Search failed: {str(e)}")
            return []

    def analyze(self, content: List[Dict[str, str]], custom_prompt: Optional[str] = None) -> str:
        """Analyze content using OpenRouter API"""
        if custom_prompt:
            analysis_prompt = custom_prompt
        else:
            analysis_prompt = "Analyze and summarize the following content, highlighting key points and insights:"

        formatted_content = "\n\n".join(
            f"Title: {item.get('title', '')}\nSnippet: {item.get('snippet', '')}\nURL: {item.get('link', '')}"
            for item in content
        )
        
        try:
            payload = {
                "model": "openai/gpt-3.5-turbo",  # Can be configured via env var
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"{analysis_prompt}\n\n{formatted_content}"}
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

    def search_and_analyze(self, query: str, num_results: int = 5, custom_prompt: Optional[str] = None) -> Dict[str, any]:
        """Combined search and analysis function"""
        search_results = self.search(query, num_results)
        if not search_results:
            return {
                "success": False,
                "error": "No search results found",
                "search_results": [],
                "analysis": None
            }

        analysis = self.analyze(search_results, custom_prompt)
        return {
            "success": True,
            "search_results": search_results,
            "analysis": analysis
        }
