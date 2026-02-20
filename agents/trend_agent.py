from dotenv import load_dotenv
from langchain_groq import ChatGroq
from ddgs import DDGS
import os
import json

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

def search_web(query: str, max_results: int = 10) -> list:
    """Search the web using DuckDuckGo"""
    print(f"🔍 Searching web for: {query}")
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title", ""),
                "body": r.get("body", ""),
                "url": r.get("href", "")
            })
    return results

def rank_results(results: list, domain: str, goal: str) -> str:
    """Use LLM to rank and summarize results by relevance"""
    
    # Format results for LLM
    results_text = ""
    for i, r in enumerate(results):
        results_text += f"\nResult {i+1}:\nTitle: {r['title']}\nSummary: {r['body']}\n"

    prompt = f"""You are an expert trend analyst for the domain: {domain}
User goal: {goal}

Here are web search results from today:
{results_text}

Your task:
1. Identify the TOP 5 most relevant and trending topics from these results
2. For each topic give:
   - A clear title
   - A 2 sentence summary of why it matters
   - A relevance score from 1-10 based on how relevant it is to the user's goal

Return your response in this exact JSON format:
{{
  "trends": [
    {{
      "title": "trend title here",
      "summary": "2 sentence summary here",
      "relevance_score": 8
    }}
  ]
}}

Return ONLY the JSON. No extra text."""

    response = llm.invoke(prompt)
    return response.content

def run_trend_agent(domain: str, goal: str) -> dict:
    """Main function — runs the full trend research pipeline"""
    
    print(f"\n🤖 Trend Agent Starting...")
    print(f"📌 Domain: {domain}")
    print(f"🎯 Goal: {goal}")
    print("-" * 50)

    # Step 1: Search the web
    query = f"{domain} latest trends news 2025"
    results = search_web(query, max_results=10)
    print(f"✅ Found {len(results)} web results")

    # Step 2: Rank and summarize with LLM
    print("🧠 Analyzing results with LLM...")
    ranked = rank_results(results, domain, goal)

    # Step 3: Parse JSON response
    try:
        # Clean the response in case LLM adds extra text
        cleaned = ranked.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0]
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0]
        
        trends_data = json.loads(cleaned)
        print("✅ Trends extracted successfully!")
        return trends_data
    
    except json.JSONDecodeError:
        print("⚠️ JSON parsing failed — returning raw response")
        return {"raw_response": ranked}


# ── Test the agent ─────────────────────────────────────────
if __name__ == "__main__":
    
    # Test with AI Engineering domain
    result = run_trend_agent(
        domain="AI Engineering and LLMs",
        goal="I want to become an AI engineer and grow my LinkedIn presence"
    )

    print("\n" + "="*50)
    print("📊 TOP TRENDING TOPICS TODAY:")
    print("="*50)
    
    if "trends" in result:
        for i, trend in enumerate(result["trends"], 1):
            print(f"\n#{i}: {trend['title']}")
            print(f"📝 {trend['summary']}")
            print(f"⭐ Relevance Score: {trend['relevance_score']}/10")
    else:
        print(result)