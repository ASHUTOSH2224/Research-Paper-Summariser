from openai import OpenAI
import config
from pdf_handler import get_paper_content


class Summarizer:
    def __init__(self):
        if config.OPENAI_API_KEY:
            self.client = OpenAI(api_key=config.OPENAI_API_KEY)
            self.model = config.OPENAI_MODEL
        else:
            print("Warning: OPENAI_API_KEY not found. Summarization will fail.")
            self.client = None

    def summarize(self, paper):
        """
        Summarizes a paper using the LLM (OpenAI).
        Downloads the actual PDF and extracts content for summarization.
        """
        if not self.client:
            return "Error: No API Key configured."

        # Get the actual paper content (downloads PDF and extracts text)
        print(f"Fetching full paper content for: {paper['title']}")
        paper_content = get_paper_content(paper)

        prompt = f"""
        You are an expert research assistant. Summarize the following research paper for a technical audience.
        
        Paper Title: {paper['title']}
        
        --- FULL PAPER CONTENT ---
        {paper_content}
        --- END OF PAPER ---
        
        Please provide a structured summary with the following sections. Use distinct emojis and *single asterisks* for bold headers (Slack style).
        
        :rocket: *Core Contribution*
        (1-2 sentences on what this paper contributes)
        
        :bulb: *Key Findings*
        (Bullet points of the main results, properties, or benchmarks)
        
        :dart: *Implications*
        (Why this matters)
        
        Keep it concise, high-quality, and visually clean for Slack.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant who summarizes academic papers."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {e}"


if __name__ == "__main__":
    # Test with a real paper
    s = Summarizer()
    test_paper = {
        'title': 'Attention Is All You Need',
        'abstract': 'The dominant sequence transduction models...',
        'link': 'https://arxiv.org/abs/1706.03762'
    }
    print("Testing summarizer with PDF content...")
    print(s.summarize(test_paper))

