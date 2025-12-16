import unittest
from monitor import ResearchMonitor
from summarizer import Summarizer
import config
import os

class TestAgent(unittest.TestCase):
    def test_monitor_fetch(self):
        print("\nTesting arXiv fetch...")
        monitor = ResearchMonitor()
        # Use a small limit and a generic query to ensure results
        papers = monitor.fetch_arxiv_papers(query="cat:cs.AI", max_results=2)
        print(f"Fetched {len(papers)} papers.")
        self.assertTrue(len(papers) > 0, "Should fetch at least one paper")
        self.assertIn('title', papers[0])
        self.assertIn('abstract', papers[0])
        self.assertIn('link', papers[0])

    def test_summarizer_init(self):
        print("\nTesting Summarizer init...")
        # mocking key for init check if not present
        if not os.getenv("GOOGLE_API_KEY"):
            print("GOOGLE_API_KEY not set. Expecting warning/mock behavior.")
            
        s = Summarizer()
        self.assertIsNotNone(s)

    # We can't really test summarization or slack posting without keys
    # But monitors fetching proves the core data source works.

if __name__ == '__main__':
    unittest.main()
