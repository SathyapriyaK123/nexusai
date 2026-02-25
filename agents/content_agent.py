import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import setup_logger, safe_parse_json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
logger = setup_logger("content_agent")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.8
)

def write_linkedin_post(domain: str, goal: str, content_angle: str, top_priority: str) -> str:
    """Write a LinkedIn post based on today's plan"""
    
    prompt = f"""You are an expert LinkedIn content writer for: {domain}
User goal: {goal}

Today's content angle: {content_angle}
Today's top priority topic: {top_priority}

Write a high-performing LinkedIn post that:
- Starts with a STRONG hook (first line must stop scrolling)
- Tells a short story or shares a surprising insight
- Provides 3-5 practical takeaways
- Ends with a clear CTA (call to action)
- Uses short paragraphs (2-3 lines max)
- Includes relevant emojis sparingly
- Is between 150-250 words

Return ONLY the post text. No extra commentary."""

    response = llm.invoke(prompt)
    logger.info("✅ LinkedIn post written!")
    return response.content

def write_twitter_thread(domain: str, goal: str, content_angle: str) -> list:
    """Write a Twitter/X thread based on today's plan"""
    
    prompt = f"""You are an expert Twitter/X content writer for: {domain}
User goal: {goal}

Today's content angle: {content_angle}

Write a Twitter thread with exactly 5 tweets that:
- Tweet 1: Strong hook that makes people click "show more"
- Tweet 2-4: Valuable insights or steps
- Tweet 5: Strong CTA with question to drive engagement

Each tweet must be under 280 characters.

Return in this exact JSON format:
{{
  "tweets": [
    "Tweet 1 text here",
    "Tweet 2 text here",
    "Tweet 3 text here",
    "Tweet 4 text here",
    "Tweet 5 text here"
  ]
}}

Return ONLY the JSON. No extra text."""

    response = llm.invoke(prompt)
    thread = safe_parse_json(response.content, fallback={"tweets": []})
    logger.info("✅ Twitter thread written!")
    return thread.get("tweets", [])

def write_networking_message(networking_opportunity: str, domain: str) -> str:
    """Write a short networking message"""
    
    prompt = f"""Write a short, genuine LinkedIn connection message for:
Opportunity: {networking_opportunity}
Domain: {domain}

Rules:
- Maximum 3 sentences
- Sound human and genuine — not salesy
- Mention a specific reason for connecting
- No generic phrases like "I'd love to connect"

Return ONLY the message text."""

    response = llm.invoke(prompt)
    logger.info("✅ Networking message written!")
    return response.content

def run_content_agent(domain: str, goal: str, plan: dict) -> dict:
    """Main function — generates all content from today's plan"""
    
    logger.info(f"🤖 Content Agent Starting | Domain: {domain}")
    
    content_angles = plan.get("content_angles", ["AI Engineering insights"])
    top_priority = plan.get("top_priority", "Share AI insights")
    networking = plan.get("networking_opportunity", "AI community")
    
    # Write all content
    linkedin_post = write_linkedin_post(
        domain=domain,
        goal=goal,
        content_angle=content_angles[0] if content_angles else "AI insights",
        top_priority=top_priority
    )
    
    twitter_thread = write_twitter_thread(
        domain=domain,
        goal=goal,
        content_angle=content_angles[1] if len(content_angles) > 1 else content_angles[0]
    )
    
    networking_message = write_networking_message(
        networking_opportunity=networking,
        domain=domain
    )
    
    content_package = {
        "linkedin_post": linkedin_post,
        "twitter_thread": twitter_thread,
        "networking_message": networking_message,
        "content_angles_used": content_angles
    }
    
    logger.info("✅ Full content package ready!")
    return content_package


# ── Test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    
    # Sample plan from planner agent
    sample_plan = {
        "top_priority": "Create practical hands-on content for LangGraph Agents",
        "content_angles": [
            "Beginner-friendly guides to LangGraph Agents",
            "Real-world examples of Agentic AI",
            "Simple tutorials on RAG Systems"
        ],
        "networking_opportunity": "Engage with Agentic AI community on LinkedIn",
        "learning_focus": "LangGraph multi-agent systems",
        "avoid_today": "Complex theoretical AI content"
    }
    
    result = run_content_agent(
        domain="AI Engineering and LLMs",
        goal="I want to become an AI engineer and grow my LinkedIn presence",
        plan=sample_plan
    )
    
    print("\n" + "="*50)
    print("📱 LINKEDIN POST:")
    print("="*50)
    print(result["linkedin_post"])
    
    print("\n" + "="*50)
    print("🐦 TWITTER THREAD:")
    print("="*50)
    for i, tweet in enumerate(result["twitter_thread"], 1):
        print(f"\nTweet {i}: {tweet}")
    
    print("\n" + "="*50)
    print("🤝 NETWORKING MESSAGE:")
    print("="*50)
    print(result["networking_message"])