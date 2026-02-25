import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import setup_logger, safe_parse_json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
logger = setup_logger("planner_agent")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

def run_planner_agent(domain: str, goal: str,
                      trends: dict, sentiment: dict,
                      competitor_intel: dict,
                      past_memories: list = []) -> dict:
    """
    Takes all intelligence + memory and creates
    a strategic daily plan for the user.
    """
    
    logger.info(f"🤖 Planner Agent Starting | Domain: {domain}")
    
    # Format past memories
    memory_text = ""
    if past_memories:
        memory_text = "PAST MEMORY CONTEXT:\n"
        for m in past_memories[:3]:
            memory_text += f"- {m.get('content', '')[:100]}\n"
    
    prompt = f"""You are NexusAI's strategic planner for: {domain}
User goal: {goal}

INTELLIGENCE GATHERED TODAY:
Trends: {json.dumps(trends, indent=2)}
Community Sentiment: {json.dumps(sentiment, indent=2)}
Competitor Intelligence: {json.dumps(competitor_intel, indent=2)}

{memory_text}

Based on ALL of this intelligence, create today's strategic plan.
Return in this exact JSON format:
{{
  "top_priority": "The single most important thing to focus on today and why",
  "content_angles": [
    "Best content angle 1 based on trends",
    "Best content angle 2 based on sentiment",
    "Best content angle 3 based on competitor gaps"
  ],
  "networking_opportunity": "One specific person or community to engage with today",
  "learning_focus": "One topic to learn about based on what is emerging",
  "avoid_today": "What NOT to post about today based on competitor saturation",
  "rationale": "2 sentence explanation of why this plan makes sense today"
}}

Return ONLY the JSON. No extra text."""

    response = llm.invoke(prompt)
    plan = safe_parse_json(response.content, fallback={
        "top_priority": "Research and post about today's top trend",
        "content_angles": ["Educational content", "Personal story", "Industry insight"],
        "networking_opportunity": "Engage with AI engineering community",
        "learning_focus": "Latest LLM developments",
        "avoid_today": "Oversaturated topics",
        "rationale": "Based on available intelligence."
    })
    
    logger.info("✅ Daily plan created!")
    return plan


# ── Test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    
    # Test with sample data
    sample_trends = {
        "trends": [
            {"title": "LangGraph Agents", "summary": "Multi-agent systems trending", "relevance_score": 9},
            {"title": "RAG Systems", "summary": "RAG with metadata filtering", "relevance_score": 8}
        ]
    }
    
    sample_sentiment = {
        "overall_sentiment": "positive",
        "hot_topics": [{"topic": "Agentic AI", "sentiment": "positive"}],
        "pain_points": ["Complex setup", "Lack of tutorials"],
        "content_angles": ["Beginner friendly guides", "Real world examples"]
    }
    
    sample_competitor = {
        "overall_landscape": "Growing space with few practical guides",
        "your_best_opportunity": "Practical hands-on content",
        "content_gaps": ["Simple agent tutorials", "Free tool guides"]
    }
    
    result = run_planner_agent(
        domain="AI Engineering and LLMs",
        goal="I want to become an AI engineer and grow my LinkedIn presence",
        trends=sample_trends,
        sentiment=sample_sentiment,
        competitor_intel=sample_competitor
    )
    
    print("\n" + "="*50)
    print("📋 TODAY'S STRATEGIC PLAN:")
    print("="*50)
    print(f"\n🎯 TOP PRIORITY:\n{result.get('top_priority')}")
    print(f"\n✍️  CONTENT ANGLES:")
    for angle in result.get('content_angles', []):
        print(f"  → {angle}")
    print(f"\n🤝 NETWORKING:\n{result.get('networking_opportunity')}")
    print(f"\n📚 LEARNING FOCUS:\n{result.get('learning_focus')}")
    print(f"\n🚫 AVOID TODAY:\n{result.get('avoid_today')}")
    print(f"\n💡 RATIONALE:\n{result.get('rationale')}")