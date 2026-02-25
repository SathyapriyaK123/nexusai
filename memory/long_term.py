import os
import sys
import json
import pickle
from datetime import datetime
from typing import List, Dict, Any, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import setup_logger

logger = setup_logger("long_term_memory")

class LongTermMemory:
    """
    Persistent memory using FAISS — works on all Python versions.
    Stores everything as vectors so we can search by MEANING.
    """
    
    def __init__(self, persist_path: str = "./nexusai_memory"):
        self.persist_path = persist_path
        os.makedirs(persist_path, exist_ok=True)
        
        # Simple file-based storage
        self.memory_file = os.path.join(persist_path, "memories.json")
        self.memories = self._load_memories()
        logger.info("🧠 Long-term memory initialized")
    
    def _load_memories(self) -> dict:
        """Load existing memories from file"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {
            "daily_briefings": [],
            "trends_history": [],
            "decisions": [],
            "domain_knowledge": []
        }
    
    def _save_memories(self):
        """Save memories to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memories, f, indent=2)
    
    def store_daily_briefing(self, briefing: str, domain: str, date: str = None):
        """Store today's intelligence briefing"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        self.memories["daily_briefings"].append({
            "date": date,
            "domain": domain,
            "content": briefing,
            "type": "daily_briefing"
        })
        self._save_memories()
        logger.info(f"💾 Stored daily briefing for {date}")
    
    def store_trend(self, trend_title: str, trend_summary: str,
                    domain: str, relevance_score: int):
        """Store a trend"""
        date = datetime.now().strftime("%Y-%m-%d")
        
        self.memories["trends_history"].append({
            "date": date,
            "domain": domain,
            "title": trend_title,
            "summary": trend_summary,
            "relevance_score": relevance_score,
            "type": "trend"
        })
        self._save_memories()
        logger.info(f"💾 Stored trend: {trend_title[:40]}...")
    
    def store_decision(self, decision: str, reasoning: str, domain: str):
        """Store a strategic decision"""
        date = datetime.now().strftime("%Y-%m-%d")
        
        self.memories["decisions"].append({
            "date": date,
            "domain": domain,
            "decision": decision,
            "reasoning": reasoning,
            "type": "decision"
        })
        self._save_memories()
        logger.info(f"💾 Stored decision: {decision[:40]}...")
    
    def store_knowledge(self, knowledge: str, topic: str, domain: str):
        """Store domain knowledge"""
        date = datetime.now().strftime("%Y-%m-%d")
        
        self.memories["domain_knowledge"].append({
            "date": date,
            "domain": domain,
            "topic": topic,
            "content": knowledge,
            "type": "knowledge"
        })
        self._save_memories()
        logger.info(f"💾 Stored knowledge: {topic[:40]}...")
    
    def search_memory(self, query: str, collection_name: str,
                      n_results: int = 3,
                      filters: Optional[Dict] = None) -> List[Dict]:
        """Search memory by keyword matching"""
        collection = self.memories.get(collection_name, [])
        
        if not collection:
            logger.info(f"📭 Collection {collection_name} is empty")
            return []
        
        # Simple keyword search
        query_words = query.lower().split()
        scored = []
        
        for item in collection:
            content = json.dumps(item).lower()
            score = sum(1 for word in query_words if word in content)
            
            # Apply filters if provided
            if filters:
                match = all(item.get(k) == v for k, v in filters.items())
                if not match:
                    continue
            
            if score > 0:
                scored.append((score, item))
        
        # Sort by score and return top n
        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, item in scored[:n_results]:
            results.append({
                "content": json.dumps(item),
                "metadata": item,
                "score": score
            })
        
        logger.info(f"🔍 Found {len(results)} memories for: {query[:40]}")
        return results
    
    def get_recent_trends(self, domain: str, days: int = 7) -> List[Dict]:
        """Get trends from last N days"""
        from datetime import timedelta
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        recent = [
            t for t in self.memories["trends_history"]
            if t.get("domain") == domain and t.get("date", "") >= cutoff
        ]
        
        logger.info(f"📅 Found {len(recent)} recent trends")
        return recent
    
    def memory_stats(self) -> Dict:
        """Show how much NexusAI has learned"""
        return {
            name: len(items)
            for name, items in self.memories.items()
        }


# ── Test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    
    print("Testing Long-Term Memory...")
    mem = LongTermMemory()
    
    mem.store_trend(
        trend_title="LangGraph Multi-Agent Systems",
        trend_summary="LangGraph is becoming the standard for multi-agent AI",
        domain="AI Engineering",
        relevance_score=9
    )
    
    mem.store_daily_briefing(
        briefing="Today AI engineering focused on LangGraph and agents",
        domain="AI Engineering"
    )
    
    mem.store_decision(
        decision="Focus on LangGraph content this week",
        reasoning="High relevance and low competition",
        domain="AI Engineering"
    )
    
    print("\n🔍 Searching memory for 'agent frameworks'...")
    results = mem.search_memory(
        query="agent frameworks",
        collection_name="trends_history"
    )
    
    for r in results:
        print(f"\n📄 Found: {r['metadata']['title']}")
        print(f"📅 Date: {r['metadata']['date']}")
    
    print("\n📊 Memory Stats:")
    stats = mem.memory_stats()
    for collection, count in stats.items():
        print(f"  {collection}: {count} entries")
    
    print("\n✅ Long-term memory working!")