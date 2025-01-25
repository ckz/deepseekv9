import os
from dotenv import load_dotenv
from .web_crawler import WebCrawler
from .ai_agent import AIAgent

class AutogenAgent:
    def __init__(self):
        load_dotenv()
        self.crawler = WebCrawler()
        self.ai_agent = AIAgent()

    def search_and_analyze(self, query: str):
        # Step 1: Perform web search
        search_results = self.crawler.search_web(query)
        
        # Step 2: Crawl top results
        crawled_data = []
        for result in search_results[:3]:  # Limit to top 3 results
            content = self.crawler.crawl_page(result['link'])
            crawled_data.append({
                'title': result['title'],
                'content': content
            })
        
        # Step 3: Analyze with AI
        analysis = self.ai_analyze_content(crawled_data)
        return analysis

    def ai_analyze_content(self, content: list):
        return self.ai_agent.analyze(content)

if __name__ == "__main__":
    agent = AutogenAgent()
    query = input("Enter your search query: ")
    result = agent.search_and_analyze(query)
    print("Analysis Result:")
    print(result)
