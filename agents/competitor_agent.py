from dotenv import load_dotenv
from langchain_groq import ChatGroq
from ddgs import DDGS
import os
import json

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

def search_competitor(competitor: str, domain: str) -> list:
    """Search for a competitor's recent activity"""
    print(f"🔍 Tracking: {competitor}")
    results = []
    
    queries = [
        f"{competitor} {domain} latest 2025",
        f"{competitor} recent posts content LinkedIn",
        f"what is {competitor} doing in {domain}"
    ]
    
    with DDGS() as ddgs:
        for query in queries:
            for r in ddgs.text(query, max_results=3):
                results.append({
                    "title": r.get("title", ""),
                    "body": r.get("body", ""),
                    "url": r.get("href", "")
                })
    
    return results

def analyze_competitors(all_results: dict, domain: str, goal: str) -> dict:
    """Use LLM to analyze competitor activity"""
    
    results_text = ""
    for competitor, results in all_results.items():
        results_text += f"\n\nCOMPETITOR: {competitor}\n"
        for r in results:
            results_text += f"Title: {r['title']}\nContent: {r['body']}\n"

    prompt = f"""You are an expert competitor analyst for the domain: {domain}
User goal: {goal}

Here is recent activity from key players in this domain:
{results_text}

Analyze what these key players are doing and identify opportunities.
Return in this exact JSON format:
{{
  "competitor_insights": [
    {{
      "name": "competitor name",
      "what_they_are_doing": "one sentence summary",
      "what_is_working": "what seems to be working for them",
      "gap_you_can_fill": "opportunity they are missing that you can exploit"
    }}
  ],
  "overall_landscape": "2 sentence summary of the competitive landscape",
  "your_best_opportunity": "the single best opportunity based on competitor analysis",
  "content_gaps": [
    "topic nobody is covering well that you could own",
    "another gap in the market"
  ]
}}

Return ONLY the JSON. No extra text."""

    response = llm.invoke(prompt)
    return response.content

def run_competitor_agent(competitors: list, domain: str, goal: str) -> dict:
    """Main function — tracks all competitors"""
    
    print(f"\n🤖 Competitor Agent Starting...")
    print(f"📌 Domain: {domain}")
    print(f"👥 Tracking: {', '.join(competitors)}")
    print("-" * 50)

    # Search each competitor
    all_results = {}
    for competitor in competitors:
        results = search_competitor(competitor, domain)
        all_results[competitor] = results
        print(f"✅ Found {len(results)} results for {competitor}")

    # Analyze all competitors together
    print("🧠 Analyzing competitor landscape...")
    analysis_raw = analyze_competitors(all_results, domain, goal)

    # Parse JSON
    try:
        cleaned = analysis_raw.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0]
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0]
        
        analysis_data = json.loads(cleaned)
        print("✅ Competitor analysis complete!")
        return analysis_data

    except json.JSONDecodeError:
        print("⚠️ JSON parsing failed — returning raw response")
        return {"raw_response": analysis_raw}


# ── Test the agent ─────────────────────────────────────────
if __name__ == "__main__":
    
    # Define your competitors or key players to track
    competitors = [
        "Andrej Karpathy",
        "Harrison Chase LangChain",
        "Swyx AI Engineer"
    ]
    
    result = run_competitor_agent(
        competitors=competitors,
        domain="AI Engineering and LLMs",
        goal="I want to become an AI engineer and grow my LinkedIn presence"
    )

    print("\n" + "="*50)
    print("📊 COMPETITOR INTELLIGENCE REPORT:")
    print("="*50)

    if "competitor_insights" in result:
        print(f"\n🌍 LANDSCAPE: {result['overall_landscape']}")
        
        print("\n👥 KEY PLAYER INSIGHTS:")
        for c in result.get("competitor_insights", []):
            print(f"\n  → {c['name']}")
            print(f"     Doing: {c['what_they_are_doing']}")
            print(f"     Working: {c['what_is_working']}")
            print(f"     Gap: {c['gap_you_can_fill']}")

        print(f"\n🎯 YOUR BEST OPPORTUNITY:")
        print(f"  → {result['best_opportunity'] if 'best_opportunity' in result else result.get('your_best_opportunity', '')}")

        print("\n📝 CONTENT GAPS YOU CAN OWN:")
        for gap in result.get("content_gaps", []):
            print(f"  → {gap}")
    else:
        print(result)