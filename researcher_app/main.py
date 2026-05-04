import sys
from agent import ResearchAgent

def main():
    if len(sys.argv) < 2:
        query = input("What would you like me to research? ")
    else:
        query = " ".join(sys.argv[1:])

    print(f"\n🚀 Starting research on: {query}\n")
    
    agent = ResearchAgent()
    report = agent.run(query)

    filename = "research_report.md"
    with open(filename, "w") as f:
        f.write(report)

    print(f"\n✅ Research Complete! Report saved to {filename}")
    print("-" * 30)
    print(report[:500] + "...") # Show preview

if __name__ == "__main__":
    main()
