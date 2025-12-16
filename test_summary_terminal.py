import os
from dotenv import load_dotenv
from monitor import ResearchMonitor
from summarizer import Summarizer

# Load env vars
load_dotenv()

def test_terminal_flow():
    print("--- 1. Checking Configuration ---")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in .env!")
        return
    print("✅ OPENAI_API_KEY found.")

    print("\n--- 2. Fetching Paper from arXiv ---")
    
    # Clear seen papers for this test to ensure we get a result
    if os.path.exists("seen_papers.json"):
        os.remove("seen_papers.json")
        
    monitor = ResearchMonitor()
    # Fetch just 1 paper to test
    papers = monitor.fetch_arxiv_papers(query="cat:cs.AI", max_results=1)
    
    if not papers:
        print("❌ No papers found. Check internet connection or arXiv API.")
        return

    paper = papers[0]
    print(f"✅ Fetched Paper: {paper['title']}")
    print(f"   Link: {paper['link']}")

    print("\n--- 3. Generating Summary (OpenAI) ---")
    summarizer = Summarizer()
    summary = summarizer.summarize(paper)
    
    print("\n" + "="*40)
    print("RESULTING SUMMARY:")
    print("="*40)
    print(summary)
    print("="*40)

if __name__ == "__main__":
    test_terminal_flow()
