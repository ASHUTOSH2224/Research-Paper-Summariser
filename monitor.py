import feedparser
import json
import os
import time
import requests
import config

class ResearchMonitor:
    def __init__(self):
        self.seen_papers_file = config.DB_PATH
        self.seen_papers = self.load_seen_papers()

    def load_seen_papers(self):
        """Load seen paper IDs from a JSON file."""
        if os.path.exists(self.seen_papers_file):
            try:
                with open(self.seen_papers_file, 'r') as f:
                    return set(json.load(f))
            except (json.JSONDecodeError, IOError):
                return set()
        return set()

    def save_seen_papers(self):
        """Save seen paper IDs to a JSON file."""
        try:
            with open(self.seen_papers_file, 'w') as f:
                json.dump(list(self.seen_papers), f)
        except IOError as e:
            print(f"Error saving seen papers: {e}")

    def fetch_arxiv_papers(self, query=None, max_results=None):
        """
        Fetch papers from arXiv API.
        Returns a list of NEW paper dictionaries.
        """
        if query is None:
            query = config.ARXIV_QUERY
        if max_results is None:
            max_results = config.MAX_PAPERS_PER_RUN

        # Handle spaces in query
        query = query.replace(" ", "+")
        
        base_url = 'https://export.arxiv.org/api/query?'
        search_query = f'search_query={query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending'
        
        print(f"Fetching from: {base_url + search_query}") # Debug
        
        try:
            # arXiv API requires a User-Agent to avoid 429s (Good Citizenship)
            headers = {
                'User-Agent': 'ResearchSummarizerBot/1.0 (mailto:study@example.com)'
            }
            response = requests.get(base_url + search_query, headers=headers)
            if response.status_code != 200:
                print(f"Error: arXiv API returned status {response.status_code}")
                return []
            
            feed = feedparser.parse(response.content)
        except Exception as e:
            print(f"Error fetching from arXiv: {e}")
            return []

        new_papers = []
        for entry in feed.entries:
            # Extract ID usually looking like http://arxiv.org/abs/2101.12345v1
            # We want just the versionless ID or the full URL as key. 
            # Using the full ID from entry.id matches strictly.
            paper_id = entry.id 
            
            if paper_id not in self.seen_papers:
                paper = {
                    'id': paper_id,
                    'title': entry.title.replace('\n', ' '),
                    'abstract': entry.summary.replace('\n', ' '),
                    'link': entry.link,
                    'published': entry.published
                }
                new_papers.append(paper)
                self.seen_papers.add(paper_id)
        
        if new_papers:
            self.save_seen_papers()
            
        return new_papers

if __name__ == "__main__":
    # Simple test
    monitor = ResearchMonitor()
    papers = monitor.fetch_arxiv_papers(max_results=3)
    print(f"Found {len(papers)} new papers.")
    for p in papers:
        print(f"- {p['title']}")
