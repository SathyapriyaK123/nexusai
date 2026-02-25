import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import setup_logger
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any

from agents.trend_agent import run_trend_agent
from agents.sentiment_agent import run_sentiment_agent
from agents.competitor_agent import run_competitor_agent
from agents.planner_agent import run_planner_agent
from agents.content_agent import run_content_agent
from agents.rewriter_agent import run_self_correction_loop
from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory

load_dotenv()
logger = setup_logger("orchestrator")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

# ── Shared State ──────────────────────────────────────────────

class NexusState(TypedDict):
    domain: str
    goal: str
    competitors: List[str]
    platforms: List[str]
    trends: Dict[str, Any]
    sentiment: Dict[str, Any]
    competitor_intel: Dict[str, Any]
    daily_plan: Dict[str, Any]
    raw_content: Dict[str, Any]
    final_content: Dict[str, Any]
    past_memories: List[Dict]
    daily_briefing: str
    errors: List[str]

# ── Agent Nodes ───────────────────────────────────────────────

def memory_retrieval_node(state: NexusState) -> NexusState:
    """Node 1 — Retrieve past memories before searching web"""
    logger.info("🧠 Retrieving past memories...")
    
    try:
        ltm = LongTermMemory()
        past_trends = ltm.search_memory(
            query=state["domain"],
            collection_name="trends_history",
            n_results=3
        )
        past_decisions = ltm.search_memory(
            query=state["goal"],
            collection_name="decisions",
            n_results=2
        )
        state["past_memories"] = past_trends + past_decisions
        logger.info(f"✅ Retrieved {len(state['past_memories'])} past memories")
    except Exception as e:
        logger.error(f"❌ Memory retrieval failed: {e}")
        state["past_memories"] = []
        state["errors"].append(f"Memory retrieval: {str(e)}")
    
    return state

def trend_node(state: NexusState) -> NexusState:
    """Node 2 — Trend Research"""
    logger.info("🔍 Running Trend Agent...")
    try:
        state["trends"] = run_trend_agent(
            domain=state["domain"],
            goal=state["goal"]
        )
    except Exception as e:
        logger.error(f"❌ Trend Agent failed: {e}")
        state["trends"] = {}
        state["errors"].append(f"Trend Agent: {str(e)}")
    return state

def sentiment_node(state: NexusState) -> NexusState:
    """Node 3 — Sentiment Analysis"""
    logger.info("💬 Running Sentiment Agent...")
    try:
        state["sentiment"] = run_sentiment_agent(
            domain=state["domain"],
            goal=state["goal"]
        )
    except Exception as e:
        logger.error(f"❌ Sentiment Agent failed: {e}")
        state["sentiment"] = {}
        state["errors"].append(f"Sentiment Agent: {str(e)}")
    return state

def competitor_node(state: NexusState) -> NexusState:
    """Node 4 — Competitor Intelligence"""
    logger.info("👥 Running Competitor Agent...")
    try:
        state["competitor_intel"] = run_competitor_agent(
            competitors=state["competitors"],
            domain=state["domain"],
            goal=state["goal"]
        )
    except Exception as e:
        logger.error(f"❌ Competitor Agent failed: {e}")
        state["competitor_intel"] = {}
        state["errors"].append(f"Competitor Agent: {str(e)}")
    return state

def planner_node(state: NexusState) -> NexusState:
    """Node 5 — Strategic Planning"""
    logger.info("📋 Running Planner Agent...")
    try:
        state["daily_plan"] = run_planner_agent(
            domain=state["domain"],
            goal=state["goal"],
            trends=state["trends"],
            sentiment=state["sentiment"],
            competitor_intel=state["competitor_intel"],
            past_memories=state["past_memories"]
        )
    except Exception as e:
        logger.error(f"❌ Planner Agent failed: {e}")
        state["daily_plan"] = {}
        state["errors"].append(f"Planner Agent: {str(e)}")
    return state

def content_node(state: NexusState) -> NexusState:
    """Node 6 — Content Generation"""
    logger.info("✍️ Running Content Agent...")
    try:
        state["raw_content"] = run_content_agent(
            domain=state["domain"],
            goal=state["goal"],
            plan=state["daily_plan"]
        )
    except Exception as e:
        logger.error(f"❌ Content Agent failed: {e}")
        state["raw_content"] = {}
        state["errors"].append(f"Content Agent: {str(e)}")
    return state

def correction_node(state: NexusState) -> NexusState:
    """Node 7 — Self-Correction Loop"""
    logger.info("🔄 Running Self-Correction Loop...")
    
    final_content = {}
    raw = state.get("raw_content", {})
    
    try:
        # Correct LinkedIn post
        if raw.get("linkedin_post"):
            linkedin_result = run_self_correction_loop(
                content=raw["linkedin_post"],
                platform="LinkedIn",
                goal=state["goal"],
                domain=state["domain"],
                max_attempts=3
            )
            final_content["linkedin_post"] = linkedin_result["final_content"]
            final_content["linkedin_score"] = linkedin_result["final_score"]
            final_content["linkedin_passed"] = linkedin_result["passed"]
        
        # Keep Twitter and networking as-is (already good quality)
        final_content["twitter_thread"] = raw.get("twitter_thread", [])
        final_content["networking_message"] = raw.get("networking_message", "")
        
        state["final_content"] = final_content
        logger.info("✅ Self-correction complete!")
    
    except Exception as e:
        logger.error(f"❌ Correction failed: {e}")
        state["final_content"] = raw
        state["errors"].append(f"Correction: {str(e)}")
    
    return state

def memory_writer_node(state: NexusState) -> NexusState:
    """Node 8 — Save everything to long-term memory"""
    logger.info("💾 Writing to long-term memory...")
    
    try:
        ltm = LongTermMemory()
        
        # Store trends
        trends = state.get("trends", {}).get("trends", [])
        for trend in trends[:3]:
            ltm.store_trend(
                trend_title=trend.get("title", ""),
                trend_summary=trend.get("summary", ""),
                domain=state["domain"],
                relevance_score=trend.get("relevance_score", 5)
            )
        
        # Store today's plan as decision
        plan = state.get("daily_plan", {})
        if plan.get("top_priority"):
            ltm.store_decision(
                decision=plan.get("top_priority", ""),
                reasoning=plan.get("rationale", ""),
                domain=state["domain"]
            )
        
        logger.info("✅ Memory saved!")
    
    except Exception as e:
        logger.error(f"❌ Memory write failed: {e}")
        state["errors"].append(f"Memory write: {str(e)}")
    
    return state

def briefing_node(state: NexusState) -> NexusState:
    """Node 9 — Generate final daily briefing"""
    logger.info("📄 Generating daily briefing...")
    
    plan = state.get("daily_plan", {})
    content = state.get("final_content", {})
    trends = state.get("trends", {}).get("trends", [])
    
    briefing = f"""
╔══════════════════════════════════════════════════════════╗
║           NEXUSAI DAILY BRIEFING                        ║
╚══════════════════════════════════════════════════════════╝

📌 DOMAIN: {state['domain']}
🎯 GOAL: {state['goal']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 TOP TREND TODAY:
{trends[0]['title'] if trends else 'No trends found'}
{trends[0]['summary'] if trends else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 YOUR PLAN:
🎯 Priority: {plan.get('top_priority', 'N/A')}
📚 Learn: {plan.get('learning_focus', 'N/A')}
🚫 Avoid: {plan.get('avoid_today', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 LINKEDIN POST (Score: {content.get('linkedin_score', 'N/A')}/10):
{content.get('linkedin_post', 'Not generated')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐦 TWITTER THREAD:
"""
    
    for i, tweet in enumerate(content.get("twitter_thread", []), 1):
        briefing += f"Tweet {i}: {tweet}\n"
    
    briefing += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤝 NETWORKING MESSAGE:
{content.get('networking_message', 'Not generated')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    if state.get("errors"):
        briefing += f"\n⚠️ ERRORS: {len(state['errors'])} issues encountered\n"
    
    state["daily_briefing"] = briefing
    logger.info("✅ Daily briefing generated!")
    return state

# ── Build Full Pipeline ───────────────────────────────────────

def build_nexusai_pipeline():
    """Build the complete NexusAI LangGraph pipeline"""
    
    graph = StateGraph(NexusState)
    
    # Add all nodes
    graph.add_node("memory_retrieval", memory_retrieval_node)
    graph.add_node("trend_researcher", trend_node)
    graph.add_node("sentiment_analyzer", sentiment_node)
    graph.add_node("competitor_tracker", competitor_node)
    graph.add_node("planner", planner_node)
    graph.add_node("content_writer", content_node)
    graph.add_node("self_correction", correction_node)
    graph.add_node("memory_writer", memory_writer_node)
    graph.add_node("briefing_generator", briefing_node)
    
    # Define flow
    graph.set_entry_point("memory_retrieval")
    graph.add_edge("memory_retrieval", "trend_researcher")
    graph.add_edge("trend_researcher", "sentiment_analyzer")
    graph.add_edge("sentiment_analyzer", "competitor_tracker")
    graph.add_edge("competitor_tracker", "planner")
    graph.add_edge("planner", "content_writer")
    graph.add_edge("content_writer", "self_correction")
    graph.add_edge("self_correction", "memory_writer")
    graph.add_edge("memory_writer", "briefing_generator")
    graph.add_edge("briefing_generator", END)
    
    return graph.compile()

def run_nexusai(domain: str, goal: str,
                competitors: list, platforms: list) -> dict:
    """Run the complete NexusAI pipeline"""
    
    print("\n" + "🚀 "*15)
    print("NEXUSAI AUTONOMOUS PIPELINE STARTING")
    print("🚀 "*15 + "\n")
    
    pipeline = build_nexusai_pipeline()
    
    initial_state = NexusState(
        domain=domain,
        goal=goal,
        competitors=competitors,
        platforms=platforms,
        trends={},
        sentiment={},
        competitor_intel={},
        daily_plan={},
        raw_content={},
        final_content={},
        past_memories=[],
        daily_briefing="",
        errors=[]
    )
    
    final_state = pipeline.invoke(initial_state)
    return final_state


# ── Run NexusAI ───────────────────────────────────────────────
if __name__ == "__main__":
    
    result = run_nexusai(
        domain="AI Engineering and LLMs",
        goal="I want to become an AI engineer and grow my LinkedIn presence",
        competitors=["Andrej Karpathy", "Harrison Chase", "Swyx AI Engineer"],
        platforms=["LinkedIn", "Twitter"]
    )
    
    print(result["daily_briefing"])
    
    if result["errors"]:
        print("\n⚠️ ERRORS ENCOUNTERED:")
        for e in result["errors"]:
            print(f"  → {e}")