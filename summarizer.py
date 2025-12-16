from openai import OpenAI
import config
import os

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
        """
        if not self.client:
            return "Error: No API Key configured."

        prompt = f"""
        You are an expert research assistant. Summarize the following research paper for a technical audience.
        
        Title: {paper['title']}
        Abstract: {paper['abstract']}
        Link: {paper['link']}
        
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
                    {"role": "system", "content": "You are a helpful research assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {e}"

if __name__ == "__main__":
    # Simple Test
    s = Summarizer()
    dummy_paper = {
        'title': 'An Attention Free Transformer',
        'abstract': 'We propose an attention free transformer architecture...',
        'link': 'http://arxiv.org/abs/2105.14103'
    }
    print(s.summarize(dummy_paper))
