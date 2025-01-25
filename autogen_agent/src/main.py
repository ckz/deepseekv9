import os
from dotenv import load_dotenv
from ai_agent import AIAgent
import json

def format_results(results: dict) -> str:
    """Format the results in a readable way"""
    if not results["success"]:
        return f"Error: {results.get('error', 'Unknown error occurred')}"

    output = "=== Search Results ===\n\n"
    for idx, result in enumerate(results["search_results"], 1):
        output += f"{idx}. {result['title']}\n"
        output += f"   URL: {result['link']}\n"
        output += f"   Summary: {result['snippet'][:200]}...\n\n"

    output += "\n=== AI Analysis ===\n\n"
    output += results["analysis"]
    return output

def main():
    # Ensure environment variables are loaded
    load_dotenv()
    
    # Check for required API keys
    if not os.getenv('SEARCH_API_KEY') or not os.getenv('OPENROUTER_API_KEY'):
        print("Error: Missing required API keys. Please check your .env file.")
        print("Required keys: SEARCH_API_KEY, OPENROUTER_API_KEY")
        return

    # Initialize the AI agent
    agent = AIAgent()

    while True:
        try:
            # Get user input
            print("\n" + "="*50)
            query = input("Enter your search query (or 'quit' to exit): ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not query:
                print("Please enter a valid query.")
                continue

            # Optional parameters
            num_results = int(input("Number of results to analyze (1-10) [default=5]: ") or "5")
            num_results = max(1, min(10, num_results))  # Ensure between 1 and 10
            
            custom_prompt = input("Custom analysis prompt (press Enter to skip): ").strip() or None

            print("\nSearching and analyzing... Please wait.\n")

            # Perform search and analysis
            results = agent.search_and_analyze(
                query=query,
                num_results=num_results,
                custom_prompt=custom_prompt
            )

            # Display formatted results
            print(format_results(results))

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            continue

if __name__ == "__main__":
    main()
