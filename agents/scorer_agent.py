import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import setup_logger, safe_parse_json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
logger = setup_logger("scorer_agent")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

def score_content(content: str, platform: str, goal: str, domain: str) -> dict:
    """
    Scores content on 6 metrics — each 0-10.
    Returns score + specific critique for anything below 7.
    """
    
    prompt = f"""You are an expert content quality evaluator for {platform}.
Domain: {domain}
User goal: {goal}

Evaluate this {platform} content:
---
{content}
---

Score it on these 6 metrics from 0-10:
1. Hook Strength — does the first line stop scrolling?
2. Clarity — is it easy to understand?
3. Value Delivery — does it teach or help the reader?
4. CTA Effectiveness — is the call to action clear and compelling?
5. Platform Fit — does it match {platform} style and format?
6. Goal Alignment — does it help achieve: {goal}?

For any metric below 7, give a SPECIFIC critique and fix suggestion.

Return in this exact JSON format:
{{
  "scores": {{
    "hook_strength": 8,
    "clarity": 7,
    "value_delivery": 9,
    "cta_effectiveness": 6,
    "platform_fit": 8,
    "goal_alignment": 9
  }},
  "overall_score": 7.8,
  "passed": true,
  "critiques": [
    {{
      "metric": "cta_effectiveness",
      "score": 6,
      "problem": "CTA is too vague — just says click link",
      "fix": "Replace with specific action like: Comment YES if you want the free guide"
    }}
  ],
  "summary": "One sentence overall assessment"
}}

Return ONLY the JSON. No extra text."""

    response = llm.invoke(prompt)
    result = safe_parse_json(response.content, fallback={
        "scores": {
            "hook_strength": 5, "clarity": 5, "value_delivery": 5,
            "cta_effectiveness": 5, "platform_fit": 5, "goal_alignment": 5
        },
        "overall_score": 5.0,
        "passed": False,
        "critiques": [],
        "summary": "Could not evaluate content"
    })
    
    # Auto-calculate passed based on overall score
    result["passed"] = result.get("overall_score", 0) >= 7.0
    logger.info(f"✅ Content scored: {result.get('overall_score')}/10 — {'PASSED' if result['passed'] else 'NEEDS IMPROVEMENT'}")
    return result


# ── Test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    
    test_content = """
    I built an AI agent today.
    It searches the web automatically.
    Pretty cool stuff.
    Follow me for more.
    """
    
    result = score_content(
        content=test_content,
        platform="LinkedIn",
        goal="Grow LinkedIn presence as AI engineer",
        domain="AI Engineering"
    )
    
    print("\n" + "="*50)
    print("📊 QUALITY SCORE REPORT:")
    print("="*50)
    
    print("\n📈 SCORES:")
    for metric, score in result["scores"].items():
        bar = "✅" if score >= 7 else "❌"
        print(f"  {bar} {metric}: {score}/10")
    
    print(f"\n⭐ OVERALL: {result['overall_score']}/10")
    print(f"{'✅ PASSED' if result['passed'] else '❌ NEEDS IMPROVEMENT'}")
    
    if result["critiques"]:
        print("\n🔧 CRITIQUES:")
        for c in result["critiques"]:
            print(f"\n  Metric: {c['metric']}")
            print(f"  Problem: {c['problem']}")
            print(f"  Fix: {c['fix']}")
    
    print(f"\n💬 SUMMARY: {result['summary']}")