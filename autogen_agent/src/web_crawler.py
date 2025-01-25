from serpapi import GoogleSearch
from bs4 import BeautifulSoup
from typing import List, Dict
import os

class WebCrawler:
    def __init__(self):
        self.search_api_key = os.getenv('SEARCH_API_KEY')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def search_web(self, query: str) -> List[Dict[str, str]]:
        """Perform web search using SerpAPI"""
        try:
            search = GoogleSearch({
                "q": query,
                "api_key": self.search_api_key
            })
            results = search.get_dict().get('organic_results', [])
            return [{
                'title': r.get('title'),
                'link': r.get('link')
            } for r in results]
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def crawl_page(self, url: str) -> str:
        """Crawl a web page and extract main content"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer']):
                element.decompose()
                
            # Get main content
            main_content = soup.find('main') or soup.find('article') or soup.body
            return main_content.get_text(separator='\n', strip=True)
        except Exception as e:
            print(f"Crawling error: {e}")
            return ""
