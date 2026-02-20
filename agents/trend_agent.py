from dotenv import load_dotenv
from langchain_groq import ChatGroq
from ddgs import DDGS
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import setup_logger, retry, safe_parse_json, timer

load_dotenv()

logger = setup_logger("trend_agent")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

@retry(max_attempts=3, delay=2.0)
def search_web(query: str, max_results: int = 10) -> list:
    """Search the web — retries 3 times if it fails"""
    logger.info(f"🔍 Searching: {query}")
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title", ""),
                "body": r.get("body", ""),
                "url": r.get("href", "")
            })
    logger.info(f"✅ Found {len(results)} results")
    return results

def fallback_trends(domain: str, goal: str) -> dict:
    """Fallback — use LLM knowledge if web search fails"""
    logger.warning("⚠️ Using LLM fallback for trends (no web search)")
    
    prompt = f"""Web search is unavailable. Based on your training knowledge,
what are the top 5 trends in {domain} relevant to this goal: {goal}?

Return in this exact JSON format:
{{
  "trends": [
    {{
      "title": "trend title",
      "summary": "2 sentence summary",
      "relevance_score": 8
    }}
  ]
}}
Return ONLY the JSON."""
    
    response = llm.invoke(prompt)
    return safe_parse_json(response.content, fallback={"trends": []})

@timer
def run_trend_agent(domain: str, goal: str) -> dict:
    """Main function with error handling and fallback"""
    
    logger.info(f"🤖 Trend Agent Starting | Domain: {domain}")
    
    try:
        # Try web search first
        query = f"{domain} latest trends news 2025"
        results = search_web(query, max_results=10)
        
        if not results:
            logger.warning("⚠️ No web results — using fallback")
            return fallback_trends(domain, goal)
        
        # Rank with LLM
        results_text = ""
        for i, r in enumerate(results):
            results_text += f"\nResult {i+1}:\nTitle: {r['title']}\nSummary: {r['body']}\n"

        prompt = f"""You are an expert trend analyst for: {domain}
User goal: {goal}

Web search results:
{results_text}

Identify TOP 5 trending topics. Return this exact JSON:
{{
  "trends": [
    {{
      "title": "trend title",
      "summary": "2 sentence summary of why it matters",
      "relevance_score": 8
    }}
  ]
}}
Return ONLY the JSON."""

        response = llm.invoke(prompt)
        trends = safe_parse_json(response.content, fallback={"trends": []})
        logger.info("✅ Trend analysis complete")
        return trends

    except Exception as e:
        logger.error(f"❌ Trend Agent failed: {e} — using fallback")
        return fallback_trends(domain, goal)


# ── Test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    result = run_trend_agent(
        domain="AI Engineering and LLMs",
        goal="I want to become an AI engineer and grow my LinkedIn presence"
    )
    
    print("\n" + "="*50)
    print("📊 TOP TRENDING TOPICS:")
    print("="*50)
    if "trends" in result:
        for i, t in enumerate(result["trends"], 1):
            print(f"\n#{i}: {t['title']}")
            print(f"📝 {t['summary']}")
            print(f"⭐ Score: {t['relevance_score']}/10")