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

def search_discussions(domain: str) -> list:
    """Search for community discussions about the domain"""
    print(f"🔍 Searching discussions for: {domain}")
    results = []
    
    # Search multiple sources
    queries = [
        f"{domain} reddit discussion 2025",
        f"{domain} community opinions trends",
        f"what people think about {domain} 2025"
    ]
    
    with DDGS() as ddgs:
        for query in queries:
            for r in ddgs.text(query, max_results=4):
                results.append({
                    "title": r.get("title", ""),
                    "body": r.get("body", ""),
                    "url": r.get("href", "")
                })
    
    return results

def analyze_sentiment(results: list, domain: str, goal: str) -> dict:
    """Use LLM to analyze community sentiment"""
    
    results_text = ""
    for i, r in enumerate(results):
        results_text += f"\nSource {i+1}:\nTitle: {r['title']}\nContent: {r['body']}\n"

    prompt = f"""You are an expert community analyst for the domain: {domain}
User goal: {goal}

Here are community discussions and opinions from the web:
{results_text}

Analyze the sentiment and community pulse. Return in this exact JSON format:
{{
  "overall_sentiment": "positive/negative/neutral/mixed",
  "sentiment_score": 7,
  "hot_topics": [
    {{
      "topic": "topic people are excited about",
      "sentiment": "positive",
      "why_it_matters": "one sentence explanation"
    }}
  ],
  "pain_points": [
    "pain point 1 people are complaining about",
    "pain point 2"
  ],
  "opportunities": [
    "opportunity 1 based on what community needs",
    "opportunity 2"
  ],
  "content_angles": [
    "content idea 1 that would resonate with this community",
    "content idea 2"
  ]
}}

Return ONLY the JSON. No extra text."""

    response = llm.invoke(prompt)
    return response.content

def run_sentiment_agent(domain: str, goal: str) -> dict:
    """Main function — runs sentiment analysis pipeline"""
    
    print(f"\n🤖 Sentiment Agent Starting...")
    print(f"📌 Domain: {domain}")
    print(f"🎯 Goal: {goal}")
    print("-" * 50)

    # Search discussions
    results = search_discussions(domain)
    print(f"✅ Found {len(results)} community discussions")

    # Analyze sentiment
    print("🧠 Analyzing community sentiment...")
    sentiment_raw = analyze_sentiment(results, domain, goal)

    # Parse JSON
    try:
        cleaned = sentiment_raw.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0]
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0]
        
        sentiment_data = json.loads(cleaned)
        print("✅ Sentiment analysis complete!")
        return sentiment_data

    except json.JSONDecodeError:
        print("⚠️ JSON parsing failed — returning raw response")
        return {"raw_response": sentiment_raw}


# ── Test the agent ─────────────────────────────────────────
if __name__ == "__main__":
    
    result = run_sentiment_agent(
        domain="AI Engineering and LLMs",
        goal="I want to become an AI engineer and grow my LinkedIn presence"
    )

    print("\n" + "="*50)
    print("📊 COMMUNITY SENTIMENT ANALYSIS:")
    print("="*50)

    if "overall_sentiment" in result:
        print(f"\n🌡️  Overall Sentiment: {result['overall_sentiment'].upper()}")
        print(f"⭐ Sentiment Score: {result['sentiment_score']}/10")
        
        print("\n🔥 HOT TOPICS:")
        for t in result.get("hot_topics", []):
            print(f"  → {t['topic']} ({t['sentiment']})")
            print(f"     {t['why_it_matters']}")

        print("\n😤 PAIN POINTS:")
        for p in result.get("pain_points", []):
            print(f"  → {p}")

        print("\n💡 OPPORTUNITIES:")
        for o in result.get("opportunities", []):
            print(f"  → {o}")

        print("\n✍️  CONTENT ANGLES:")
        for c in result.get("content_angles", []):
            print(f"  → {c}")
    else:
        print(result)