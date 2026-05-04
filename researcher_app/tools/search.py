from duckduckgo_search import DDGS

def search_web(query, max_results=5):
    """
    Searches the web for the given query and returns a list of results with title, href, and body.
    """
    print(f"Searching for: {query}")
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=max_results)]
        return results

if __name__ == "__main__":
    # Test
    res = search_web("Latest breakthroughs in battery technology 2024", max_results=2)
    for r in res:
        print(f"Title: {r['title']}\nLink: {r['href']}\n")
