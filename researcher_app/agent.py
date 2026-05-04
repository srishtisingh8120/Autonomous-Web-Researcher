import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools.search import search_web
from tools.scraper import scrape_url
from tracing import tracer

load_dotenv()

class ResearchAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        self.model = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
        self.history = []
        self.max_calls = 10
        self.calls_count = 0
        self.scrapes_count = 0
        self.max_scrapes = 3

    @tracer.trace(span_type="agent", name="Autonomous Web Researcher")
    def run(self, query):
        system_prompt = """You are an Autonomous Web Researcher. 
Your goal is to provide a comprehensive answer to the user's query by searching and reading web content.

TOOLS AVAILABLE:
1. search_web(query): Returns a list of search results (snippets and URLs).
2. scrape_url(url): Returns the full text content of a webpage. (Limit: 3 scrapes max).
3. finalize_report(content): Use this when you have gathered enough information to write the final detailed report.

PROCESS:
You must respond in valid JSON format only.
Example Response:
{
    "thought": "I need to find the latest info on X, so I will start with a web search.",
    "action": "search_web",
    "action_input": "latest developments in X 2024"
}

If you have all the information, use:
{
    "thought": "I have enough information to summarize the findings.",
    "action": "finalize_report",
    "action_input": "# Research Report on X\\n...detailed content..."
}

CRITICAL: 
- Stay focused on the query.
- If a URL fails to scrape, try another one or search again.
- Be concise in your thoughts.
"""
        self.history.append({"role": "system", "content": system_prompt})
        self.history.append({"role": "user", "content": f"Topic: {query}"})

        while self.calls_count < self.max_calls:
            self.calls_count += 1
            print(f"\n--- Iteration {self.calls_count} ---")
            
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.history,
                    response_format={"type": "json_object"}
                )
                
                content = response.choices[0].message.content
                data = json.loads(content)
                
                thought = data.get("thought", "")
                action = data.get("action", "")
                action_input = data.get("action_input", "")

                print(f"Thought: {thought}")
                
                if action == "finalize_report":
                    return action_input

                elif action == "search_web":
                    print(f"Action: Searching '{action_input}'")
                    results = search_web(action_input)
                    observation = json.dumps(results, indent=2)
                    self.history.append({"role": "assistant", "content": content})
                    self.history.append({"role": "user", "content": f"Observation (Search Results): {observation}"})

                elif action == "scrape_url":
                    if self.scrapes_count >= self.max_scrapes:
                        observation = "Error: Scrape limit reached. Please synthesize your report with existing info or do another search."
                    else:
                        self.scrapes_count += 1
                        print(f"Action: Scraping {action_input}")
                        content_scraped = scrape_url(action_input)
                        observation = f"Observation (Scraped Content): {content_scraped[:2000]}..." # Snippet
                    
                    self.history.append({"role": "assistant", "content": content})
                    self.history.append({"role": "user", "content": f"Observation: {observation}"})
                
                else:
                    print(f"Unknown action: {action}")
                    break

            except Exception as e:
                print(f"Error in agent loop: {e}")
                break

        result = "Failed to complete research within budget."
        return result

if __name__ == "__main__":
    agent = ResearchAgent()
    report = agent.run("What are the top 3 AI trends in 2024?")
    print("\n\nFINAL REPORT:\n")
    print(report)
