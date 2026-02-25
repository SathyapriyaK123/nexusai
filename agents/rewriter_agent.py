import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import setup_logger
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
logger = setup_logger("rewriter_agent")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.8
)

def rewrite_content(original_content: str, critiques: list,
                    platform: str, goal: str) -> str:
    """
    Takes original content + specific critiques
    and rewrites with targeted improvements.
    """
    
    # Format critiques clearly
    critique_text = ""
    for c in critiques:
        critique_text += f"\n- {c['metric']}: {c['problem']}"
        critique_text += f"\n  Fix: {c['fix']}\n"
    
    prompt = f"""You are an expert {platform} content rewriter.
User goal: {goal}

ORIGINAL CONTENT:
---
{original_content}
---

SPECIFIC ISSUES TO FIX:
{critique_text}

Rewrite the content fixing EXACTLY these issues.
Keep what was working. Only improve what was flagged.
Maintain the same topic and core message.

Return ONLY the rewritten content. No commentary."""

    response = llm.invoke(prompt)
    logger.info("✅ Content rewritten!")
    return response.content

def run_self_correction_loop(content: str, platform: str,
                              goal: str, domain: str,
                              max_attempts: int = 3) -> dict:
    """
    The full self-correction loop:
    Score → if fail → Rewrite → Score again
    Maximum 3 attempts before flagging for human review
    """
    
    # Import here to avoid circular imports
    from agents.scorer_agent import score_content
    
    logger.info(f"🔄 Self-correction loop starting | Max attempts: {max_attempts}")
    
    current_content = content
    attempt = 0
    history = []
    
    while attempt < max_attempts:
        attempt += 1
        logger.info(f"📝 Attempt {attempt}/{max_attempts}")
        
        # Score current content
        score_result = score_content(
            content=current_content,
            platform=platform,
            goal=goal,
            domain=domain
        )
        
        # Store attempt history
        history.append({
            "attempt": attempt,
            "content": current_content,
            "score": score_result["overall_score"],
            "passed": score_result["passed"]
        })
        
        # If passed — we're done!
        if score_result["passed"]:
            logger.info(f"✅ Content PASSED on attempt {attempt} with score {score_result['overall_score']}/10")
            return {
                "final_content": current_content,
                "final_score": score_result["overall_score"],
                "attempts": attempt,
                "passed": True,
                "history": history,
                "flagged_for_review": False
            }
        
        # If failed and we have attempts left — rewrite
        if attempt < max_attempts:
            logger.info(f"❌ Score {score_result['overall_score']}/10 — rewriting...")
            
            if score_result.get("critiques"):
                current_content = rewrite_content(
                    original_content=current_content,
                    critiques=score_result["critiques"],
                    platform=platform,
                    goal=goal
                )
            else:
                logger.warning("⚠️ No critiques found — stopping loop")
                break
    
    # If we exhausted all attempts — flag for human review
    final_score = history[-1]["score"] if history else 0
    logger.warning(f"⚠️ Content flagged for human review after {max_attempts} attempts")
    
    return {
        "final_content": current_content,
        "final_score": final_score,
        "attempts": attempt,
        "passed": False,
        "history": history,
        "flagged_for_review": True
    }


# ── Test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    
    # Start with weak content
    weak_content = """
    I built an AI agent today.
    It searches the web automatically.
    Pretty cool stuff.
    Follow me for more.
    """
    
    print("🔄 Starting Self-Correction Loop...")
    print("Starting with deliberately weak content...\n")
    
    result = run_self_correction_loop(
        content=weak_content,
        platform="LinkedIn",
        goal="Grow LinkedIn presence as AI engineer",
        domain="AI Engineering",
        max_attempts=3
    )
    
    print("\n" + "="*50)
    print("🎯 SELF-CORRECTION RESULTS:")
    print("="*50)
    print(f"\n📊 Attempts taken: {result['attempts']}")
    print(f"⭐ Final score: {result['final_score']}/10")
    print(f"{'✅ PASSED' if result['passed'] else '⚠️ FLAGGED FOR REVIEW'}")
    
    print("\n📈 SCORE PROGRESSION:")
    for h in result["history"]:
        status = "✅" if h["passed"] else "❌"
        print(f"  Attempt {h['attempt']}: {h['score']}/10 {status}")
    
    print("\n📝 FINAL CONTENT:")
    print("-"*50)
    print(result["final_content"])
    
    if result["flagged_for_review"]:
        print("\n⚠️ This content needs human review before posting!")