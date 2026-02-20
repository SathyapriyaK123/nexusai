from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any
import os
import json

# Import our agents
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.trend_agent import run_trend_agent
from agents.sentiment_agent import run_sentiment_agent
from agents.competitor_agent import run_competitor_agent

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

# ── Define Shared State ───────────────────────────────────────
# This is the shared memory all agents read from and write to

class NexusState(TypedDict):
    # User inputs
    domain: str
    goal: str
    competitors: List[str]
    
    # Agent outputs
    trends: Dict[str, Any]
    sentiment: Dict[str, Any]
    competitor_intel: Dict[str, Any]
    
    # Final output
    intelligence_report: str
    errors: List[str]

# ── Define Agent Nodes ────────────────────────────────────────
# Each function is one node in the LangGraph

def trend_node(state: NexusState) -> NexusState:
    """Node 1 — Run Trend Research Agent"""
    print("\n" + "="*50)
    print("🔄 LANGGRAPH: Running Trend Agent...")
    print("="*50)
    
    try:
        trends = run_trend_agent(
            domain=state["domain"],
            goal=state["goal"]
        )
        state["trends"] = trends
    except Exception as e:
        print(f"⚠️ Trend Agent Error: {e}")
        state["errors"].append(f"Trend Agent: {str(e)}")
        state["trends"] = {}
    
    return state

def sentiment_node(state: NexusState) -> NexusState:
    """Node 2 — Run Sentiment Analysis Agent"""
    print("\n" + "="*50)
    print("🔄 LANGGRAPH: Running Sentiment Agent...")
    print("="*50)
    
    try:
        sentiment = run_sentiment_agent(
            domain=state["domain"],
            goal=state["goal"]
        )
        state["sentiment"] = sentiment
    except Exception as e:
        print(f"⚠️ Sentiment Agent Error: {e}")
        state["errors"].append(f"Sentiment Agent: {str(e)}")
        state["sentiment"] = {}
    
    return state

def competitor_node(state: NexusState) -> NexusState:
    """Node 3 — Run Competitor Intelligence Agent"""
    print("\n" + "="*50)
    print("🔄 LANGGRAPH: Running Competitor Agent...")
    print("="*50)
    
    try:
        competitor_intel = run_competitor_agent(
            competitors=state["competitors"],
            domain=state["domain"],
            goal=state["goal"]
        )
        state["competitor_intel"] = competitor_intel
    except Exception as e:
        print(f"⚠️ Competitor Agent Error: {e}")
        state["errors"].append(f"Competitor Agent: {str(e)}")
        state["competitor_intel"] = {}
    
    return state

def synthesizer_node(state: NexusState) -> NexusState:
    """Node 4 — Synthesize all intelligence into one report"""
    print("\n" + "="*50)
    print("🔄 LANGGRAPH: Synthesizing Intelligence Report...")
    print("="*50)

    prompt = f"""You are NexusAI — an autonomous intelligence system.

You have gathered the following intelligence for a user in the domain: {state['domain']}
User goal: {state['goal']}

TREND INTELLIGENCE:
{json.dumps(state.get('trends', {}), indent=2)}

COMMUNITY SENTIMENT:
{json.dumps(state.get('sentiment', {}), indent=2)}

COMPETITOR INTELLIGENCE:
{json.dumps(state.get('competitor_intel', {}), indent=2)}

Synthesize ALL of this into one clear, actionable intelligence briefing.
Format it as follows:

🌍 DOMAIN PULSE
[2-3 sentences on the overall state of the domain today]

🔥 TOP 3 TRENDS TO ACT ON
1. [trend + why it matters + what to do]
2. [trend + why it matters + what to do]
3. [trend + why it matters + what to do]

💬 COMMUNITY MOOD
[2 sentences on what the community is feeling and talking about]

🎯 YOUR BIGGEST OPPORTUNITY TODAY
[One clear, specific opportunity based on all intelligence combined]

✍️ RECOMMENDED CONTENT ANGLE FOR TODAY
[One specific content idea that combines trends + sentiment + competitor gaps]

⚡ ACTION ITEMS
1. [specific action to take today]
2. [specific action to take today]
3. [specific action to take today]"""

    response = llm.invoke(prompt)
    state["intelligence_report"] = response.content
    print("✅ Intelligence report synthesized!")
    return state

# ── Build the LangGraph ───────────────────────────────────────

def build_intelligence_graph():
    """Build and compile the LangGraph workflow"""
    
    # Create the graph
    graph = StateGraph(NexusState)
    
    # Add nodes (agents)
    graph.add_node("trend_researcher", trend_node)
    graph.add_node("sentiment_analyzer", sentiment_node)
    graph.add_node("competitor_tracker", competitor_node)
    graph.add_node("synthesizer", synthesizer_node)
    
    # Define the flow — agents run in sequence
    graph.set_entry_point("trend_researcher")
    graph.add_edge("trend_researcher", "sentiment_analyzer")
    graph.add_edge("sentiment_analyzer", "competitor_tracker")
    graph.add_edge("competitor_tracker", "synthesizer")
    graph.add_edge("synthesizer", END)
    
    # Compile and return
    return graph.compile()

def run_intelligence_layer(domain: str, goal: str, competitors: list) -> dict:
    """Run the complete intelligence layer"""
    
    print("\n" + "🚀 "*10)
    print("NEXUSAI INTELLIGENCE LAYER STARTING")
    print("🚀 "*10)
    
    # Build the graph
    intelligence_graph = build_intelligence_graph()
    
    # Define initial state
    initial_state = NexusState(
        domain=domain,
        goal=goal,
        competitors=competitors,
        trends={},
        sentiment={},
        competitor_intel={},
        intelligence_report="",
        errors=[]
    )
    
    # Run the graph
    final_state = intelligence_graph.invoke(initial_state)
    
    return final_state

# ── Test the full pipeline ────────────────────────────────────
if __name__ == "__main__":
    
    result = run_intelligence_layer(
        domain="AI Engineering and LLMs",
        goal="I want to become an AI engineer and grow my LinkedIn presence",
        competitors=["Andrej Karpathy", "Harrison Chase", "Swyx AI Engineer"]
    )
    
    print("\n" + "🌟"*25)
    print("\n📊 NEXUSAI FINAL INTELLIGENCE REPORT:")
    print("🌟"*25)
    print(result["intelligence_report"])
    
    if result["errors"]:
        print("\n⚠️ Errors encountered:")
        for e in result["errors"]:
            print(f"  → {e}")