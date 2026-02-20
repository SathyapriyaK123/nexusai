import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import setup_logger

logger = setup_logger("long_term_memory")

class LongTermMemory:
    """
    Persistent memory — survives restarts, grows every day.
    Stores everything as vectors so we can search by MEANING.
    Think of it as NexusAI's brain that never forgets.
    """
    
    def __init__(self, persist_path: str = "./nexusai_memory"):
        # Initialize ChromaDB with local persistence
        self.client = chromadb.PersistentClient(path=persist_path)
        
        # Use HuggingFace embeddings — free, runs locally
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create collections — like tables in a database
        self.collections = {
            "daily_briefings": self._get_or_create("daily_briefings"),
            "domain_knowledge": self._get_or_create("domain_knowledge"),
            "decisions": self._get_or_create("decisions"),
            "trends_history": self._get_or_create("trends_history"),
        }
        
        logger.info("🧠 Long-term memory initialized")
    
    def _get_or_create(self, name: str):
        """Get existing collection or create new one"""
        return self.client.get_or_create_collection(
            name=name,
            embedding_function=self.embedding_fn,
            metadata={"description": f"NexusAI {name} collection"}
        )
    
    def store_daily_briefing(self, briefing: str, domain: str, date: str = None):
        """Store today's intelligence briefing"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        doc_id = f"briefing_{date}_{domain.replace(' ', '_')}"
        
        self.collections["daily_briefings"].upsert(
            documents=[briefing],
            ids=[doc_id],
            metadatas=[{
                "date": date,
                "domain": domain,
                "type": "daily_briefing"
            }]
        )
        logger.info(f"💾 Stored daily briefing for {date}")
    
    def store_trend(self, trend_title: str, trend_summary: str, 
                    domain: str, relevance_score: int):
        """Store a trend to build historical trend knowledge"""
        date = datetime.now().strftime("%Y-%m-%d")
        doc_id = f"trend_{date}_{trend_title[:30].replace(' ', '_')}"
        
        content = f"Trend: {trend_title}\nSummary: {trend_summary}"
        
        self.collections["trends_history"].upsert(
            documents=[content],
            ids=[doc_id],
            metadatas=[{
                "date": date,
                "domain": domain,
                "relevance_score": relevance_score,
                "title": trend_title,
                "type": "trend"
            }]
        )
        logger.info(f"💾 Stored trend: {trend_title[:40]}...")
    
    def store_decision(self, decision: str, reasoning: str, domain: str):
        """Store a strategic decision and its reasoning"""
        date = datetime.now().strftime("%Y-%m-%d")
        doc_id = f"decision_{date}_{len(decision)}"
        
        content = f"Decision: {decision}\nReasoning: {reasoning}"
        
        self.collections["decisions"].upsert(
            documents=[content],
            ids=[doc_id],
            metadatas=[{
                "date": date,
                "domain": domain,
                "type": "decision"
            }]
        )
        logger.info(f"💾 Stored decision: {decision[:40]}...")
    
    def store_knowledge(self, knowledge: str, topic: str, domain: str):
        """Store a piece of domain knowledge"""
        date = datetime.now().strftime("%Y-%m-%d")
        doc_id = f"knowledge_{date}_{topic[:20].replace(' ', '_')}"
        
        self.collections["domain_knowledge"].upsert(
            documents=[knowledge],
            ids=[doc_id],
            metadatas=[{
                "date": date,
                "domain": domain,
                "topic": topic,
                "type": "knowledge"
            }]
        )
        logger.info(f"💾 Stored knowledge: {topic[:40]}...")
    
    def search_memory(self, query: str, collection_name: str,
                      n_results: int = 3,
                      filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search memory by MEANING — not just keywords.
        Example: searching 'LLM performance' also finds
        'model efficiency' and 'inference speed' results.
        """
        collection = self.collections.get(collection_name)
        if not collection:
            logger.warning(f"⚠️ Collection {collection_name} not found")
            return []
        
        try:
            # Check if collection has any documents
            if collection.count() == 0:
                logger.info(f"📭 Collection {collection_name} is empty")
                return []
            
            # Search with optional metadata filters
            kwargs = {
                "query_texts": [query],
                "n_results": min(n_results, collection.count())
            }
            if filters:
                kwargs["where"] = filters
            
            results = collection.query(**kwargs)
            
            # Format results cleanly
            formatted = []
            for i in range(len(results["documents"][0])):
                formatted.append({
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i]
                })
            
            logger.info(f"🔍 Found {len(formatted)} memories for: {query[:40]}")
            return formatted
        
        except Exception as e:
            logger.error(f"❌ Memory search failed: {e}")
            return []
    
    def get_recent_trends(self, domain: str, days: int = 7) -> List[Dict]:
        """Get trends from the last N days"""
        from datetime import timedelta
        
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        try:
            if self.collections["trends_history"].count() == 0:
                return []
            
            results = self.collections["trends_history"].query(
                query_texts=[f"trends in {domain}"],
                n_results=min(10, self.collections["trends_history"].count()),
                where={"domain": domain}
            )
            
            # Filter by date manually
            recent = []
            for i in range(len(results["documents"][0])):
                meta = results["metadatas"][0][i]
                if meta.get("date", "") >= cutoff:
                    recent.append({
                        "content": results["documents"][0][i],
                        "metadata": meta
                    })
            
            logger.info(f"📅 Found {len(recent)} recent trends")
            return recent
        
        except Exception as e:
            logger.error(f"❌ Recent trends search failed: {e}")
            return []
    
    def memory_stats(self) -> Dict:
        """Show how much NexusAI has learned"""
        stats = {}
        for name, collection in self.collections.items():
            stats[name] = collection.count()
        return stats


# ── Test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    
    print("Testing Long-Term Memory...")
    mem = LongTermMemory()
    
    # Store some test data
    mem.store_trend(
        trend_title="LangGraph Multi-Agent Systems",
        trend_summary="LangGraph is becoming the standard for building multi-agent AI systems",
        domain="AI Engineering",
        relevance_score=9
    )
    
    mem.store_daily_briefing(
        briefing="Today AI engineering focused on LangGraph and multi-agent systems",
        domain="AI Engineering"
    )
    
    mem.store_decision(
        decision="Focus on LangGraph content this week",
        reasoning="High relevance score and low competition in the space",
        domain="AI Engineering"
    )
    
    # Search memory
    print("\n🔍 Searching memory for 'agent frameworks'...")
    results = mem.search_memory(
        query="agent frameworks",
        collection_name="trends_history"
    )
    
    for r in results:
        print(f"\n📄 Found: {r['content'][:100]}...")
        print(f"📅 Date: {r['metadata']['date']}")
    
    # Show stats
    print("\n📊 Memory Stats:")
    stats = mem.memory_stats()
    for collection, count in stats.items():
        print(f"  {collection}: {count} entries")
    
    print("\n✅ Long-term memory working!")