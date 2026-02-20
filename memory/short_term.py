import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import Dict, Any, List
from datetime import datetime
from utils import setup_logger

logger = setup_logger("short_term_memory")

class ShortTermMemory:
    """
    In-session memory — lives only during one run.
    Stores current context and passes it between agents.
    Think of it as NexusAI's working memory for today.
    """
    
    def __init__(self):
        self.memory = {
            "session_start": datetime.now().isoformat(),
            "current_domain": None,
            "current_goal": None,
            "today_trends": [],
            "today_sentiment": {},
            "today_competitor_intel": {},
            "conversation_history": [],
            "decisions_made": [],
            "errors": []
        }
        logger.info("🧠 Short-term memory initialized")
    
    def update(self, key: str, value: Any):
        """Store something in short-term memory"""
        self.memory[key] = value
        logger.info(f"💾 Short-term memory updated: {key}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve something from short-term memory"""
        return self.memory.get(key, default)
    
    def add_to_history(self, role: str, content: str):
        """Add a message to conversation history"""
        self.memory["conversation_history"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_decision(self, decision: str, reasoning: str):
        """Record a decision made during this session"""
        self.memory["decisions_made"].append({
            "decision": decision,
            "reasoning": reasoning,
            "timestamp": datetime.now().isoformat()
        })
        logger.info(f"📝 Decision recorded: {decision[:50]}...")
    
    def add_error(self, error: str):
        """Record an error that occurred"""
        self.memory["errors"].append({
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_full_context(self) -> Dict:
        """Get everything in short-term memory"""
        return self.memory
    
    def clear(self):
        """Clear memory at end of session"""
        self.memory["conversation_history"] = []
        self.memory["decisions_made"] = []
        logger.info("🗑️ Short-term memory cleared")
    
    def summary(self) -> str:
        """Return a readable summary of current session"""
        return f"""
Session started: {self.memory['session_start']}
Domain: {self.memory['current_domain']}
Goal: {self.memory['current_goal']}
Trends found: {len(self.memory['today_trends'])}
Decisions made: {len(self.memory['decisions_made'])}
Errors: {len(self.memory['errors'])}
        """.strip()


# ── Test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    
    # Test short term memory
    mem = ShortTermMemory()
    
    # Store some data
    mem.update("current_domain", "AI Engineering")
    mem.update("current_goal", "Grow LinkedIn presence")
    mem.add_to_history("user", "What is trending today?")
    mem.add_to_history("assistant", "LLMs and agents are trending")
    mem.add_decision(
        decision="Focus on LangGraph content today",
        reasoning="It is trending and has low competition"
    )
    
    # Retrieve data
    print("Domain:", mem.get("current_domain"))
    print("Goal:", mem.get("current_goal"))
    print("\nSummary:")
    print(mem.summary())
    print("\nFull context:")
    import json
    print(json.dumps(mem.get_full_context(), indent=2))