#  NexusAI — Autonomous AI Chief of Staff

> An autonomous multi-agent AI system that researches your domain, plans your day, writes platform-specific content, and self-corrects its outputs — all without being asked. Every day. Automatically.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green.svg)](https://langchain-ai.github.io/langgraph/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Cost](https://img.shields.io/badge/Cost-$0%20Forever-brightgreen.svg)]()

---

#  Live Demo

** Try it here: https://nexusai-ndyhpjg6x9nosh5c3bezvn.streamlit.app**

> Add your own Groq API key in the secrets to run the full pipeline.

---

##  What Is NexusAI?

Most AI tools wait for you to ask questions. **NexusAI is different.**

You tell NexusAI your professional goal once. From that point, every day it:

-  **Researches** your domain using real-time web intelligence
-  **Remembers** everything it has learned — getting smarter every day
-  **Plans** your daily priorities based on what is actually trending
-  **Writes** platform-specific LinkedIn posts, Twitter threads, and networking messages
-  **Self-corrects** every output until it meets a quality bar
-  **Stores** all findings to persistent memory for future sessions

**NexusAI does not wait for you. It works for you.**

---

##  System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    NEXUSAI PIPELINE                             │
│                                                                 │
│  USER INPUT (once)                                              │
│  Goal: "I want to become an AI engineer"                        │
│       ↓                                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │           LAYER 1 — MEMORY RETRIEVAL                    │    │
│  │  Long-Term Memory → What do we already know?            │    │
│  └─────────────────────────────────────────────────────────┘    │
│       ↓                                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │           LAYER 2 — INTELLIGENCE GATHERING              │    │
│  │  Trend Agent     → Live web search for today's trends   │    │
│  │  Sentiment Agent → Community discussions and feelings   │    │
│  │  Competitor Agent→ Key player activity tracking         │    │
│  └─────────────────────────────────────────────────────────┘    │
│       ↓                                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │           LAYER 3 — PLANNING                            │    │
│  │  Planner Agent  → Daily priority plan                   │    │
│  │  Content Agent  → LinkedIn + Twitter + Networking       │    │
│  └─────────────────────────────────────────────────────────┘    │
│       ↓                                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │           LAYER 4 — SELF-CORRECTION                     │    │
│  │  Quality Scorer → 6-metric rubric (0-10 each)           │    │
│  │  Rewriter Agent → Targeted improvements                 │    │
│  │  Max 3 attempts → Flag for human review if needed       │    │
│  └─────────────────────────────────────────────────────────┘    │
│       ↓                                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │           LAYER 5 — MEMORY + DELIVERY                   │    │
│  │  Memory Writer  → Store findings to long-term memory    │    │
│  │  Brief Generator→ Clean daily briefing                  │    │
│  │  Streamlit UI   → Beautiful dashboard                   │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

##  Key Features

###  Multi-Agent Orchestration
9 specialized agents coordinated by LangGraph — each expert at exactly one job. No single LLM doing everything poorly.

### 🧠 Two-Layer Memory System
- **Short-term:** In-session LangGraph state — agents share context within a run
- **Long-term:** Persistent JSON storage — survives restarts, grows every day

### 🔄 Self-Correction Loop (Reflexion Architecture)
Based on the Reflexion research paper. Every piece of content is scored on 6 metrics, rewritten with specific critiques, and re-evaluated. Maximum 3 correction attempts before flagging for human review.

### 🌐 Real-Time Web Intelligence
DuckDuckGo Search API (free, no key needed) powers live trend research, sentiment analysis, and competitor tracking every single day.

###  Cumulative Intelligence
```
Day 1:  Learns your domain basics
Day 7:  Knows patterns, key players, recurring themes
Day 14: Recognizes trends before they go mainstream
Day 30: More context than any human assistant could hold
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose | Cost |
|---|---|---|---|
| Agent Orchestration | LangGraph | Multi-agent state machine | $0 — MIT License |
| LLM | Groq + LLaMA 3.3 70B | All agent reasoning | $0 — Free tier |
| Web Search | DuckDuckGo API | Real-time intelligence | $0 — No key needed |
| Memory | JSON + File Storage | Persistent long-term memory | $0 — Local |
| UI | Streamlit | Multi-page dashboard | $0 — Open source |
| Deployment | Streamlit Cloud | Free public URL | $0 — Free tier |
| Code Hosting | GitHub | Version control | $0 — Free |

**Total Cost: $0 Forever**

---

##  Project Structure

```
nexusai/
├── agents/
│   ├── __init__.py
│   ├── trend_agent.py          # Web search + ranking
│   ├── sentiment_agent.py      # Community discussion scan
│   ├── competitor_agent.py     # Competitor tracking
│   ├── planner_agent.py        # Daily priority planning
│   ├── content_agent.py        # Platform-specific writing
│   ├── scorer_agent.py         # 6-metric quality evaluation
│   ├── rewriter_agent.py       # Self-correction rewriting
│   └── orchestrator.py         # LangGraph workflow graph
├── memory/
│   ├── __init__.py
│   ├── short_term.py           # In-session state management
│   └── long_term.py            # Persistent JSON memory
├── ui/
│   ├── __init__.py
│   ├── home.py                 # Daily briefing dashboard
│   ├── memory_view.py          # Memory timeline viewer
│   └── settings.py             # Goal and profile settings
├── app.py                      # Main Streamlit entry point
├── utils.py                    # Shared utilities and helpers
├── requirements.txt            # Package dependencies
├── .env.example                # Required API keys template
└── README.md                   # This file
```

---

## ⚙️ Installation & Local Setup

### Step 1 — Clone the Repository
```bash
git clone https://github.com/SathyapriyaK123/nexusai.git
cd nexusai
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install langchain langgraph langchain-groq langchain-community streamlit ddgs python-dotenv
```

### Step 4 — Set Up API Key
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at **console.groq.com** — no credit card needed.

### Step 5 — Run NexusAI Locally
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🚀 Deployment — Streamlit Cloud

This project is deployed for free on Streamlit Cloud.

### How to Deploy Your Own Copy

**Step 1 — Fork this repository** on GitHub

**Step 2 —** Go to **share.streamlit.io** and sign in with GitHub

**Step 3 —** Click **New App** and fill in:
```
Repository:     YOUR_USERNAME/nexusai
Branch:         main
Main file path: app.py
```

**Step 4 —** Click **Advanced Settings** → **Secrets** and add:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

**Step 5 —** Set Python version to **3.11**

**Step 6 —** Click **Deploy**

Your app will be live at:
```
https://your-app-name.streamlit.app
```

### Important Notes for Deployment
- Never push your `.env` file to GitHub
- Always add your API key through Streamlit Cloud Secrets
- The `nexusai_memory/` folder is local only — memory resets on each deployment
- For persistent memory in production, migrate to a cloud database

---

## 🚀 How to Use

### First Time Setup
1. Go to **⚙️ Settings** in the sidebar
2. Enter your domain (e.g. "AI Engineering and LLMs")
3. Enter your goal (e.g. "I want to grow my LinkedIn presence")
4. Add competitors or key players to track
5. Click **Save Settings**

### Daily Use
1. Go to **🏠 Home**
2. Click **🚀 Run NexusAI Now**
3. Wait 2-3 minutes while all 9 agents work
4. Get your complete daily briefing:
   - Top trends in your domain
   - Strategic daily plan
   - Ready-to-post LinkedIn content (quality scored)
   - Twitter thread with 5 tweets
   - Personalised networking message

### Memory Viewer
Go to **🧠 Memory** to see everything NexusAI has learned — search by topic, browse recent trends, and track decisions made.

---

## 🔄 Self-Correction Loop Detail

```
Content Generated by Content Agent
          ↓
Quality Scorer evaluates on 6 metrics:
  • Hook Strength     (does first line stop scrolling?)
  • Clarity           (easy to understand?)
  • Value Delivery    (teaches or helps reader?)
  • CTA Effectiveness (clear call to action?)
  • Platform Fit      (matches platform style?)
  • Goal Alignment    (serves stated goal?)
          ↓
Overall Score >= 7.0/10?
  YES → Content passes — deliver to user
  NO  → Generate specific critique per failing metric
          ↓
        Rewriter uses critique for targeted improvements
          ↓
        Re-score → Repeat max 3 times
          ↓
        Still failing → Flag for human review
```

---

## 📊 Agent Responsibilities

| Agent | Input | Output |
|---|---|---|
| Trend Agent | Domain + Goal | Top 5 trending topics with relevance scores |
| Sentiment Agent | Domain + Goal | Community mood, pain points, opportunities |
| Competitor Agent | Competitor names | Activity insights, gaps, opportunities |
| Planner Agent | All intelligence | Daily priority plan with rationale |
| Content Agent | Daily plan | LinkedIn post + Twitter thread + networking message |
| Quality Scorer | Content + Platform | 6-metric scores + specific critiques |
| Rewriter Agent | Content + Critiques | Improved content targeting exact issues |
| Memory Writer | Session findings | Stored to persistent long-term memory |
| Orchestrator | Everything | Coordinates all agents via LangGraph |

---

## 🧪 Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| Multi-Agent Orchestration | LangGraph StateGraph with 9 specialized agents |
| Agentic AI | Autonomous operation without user input |
| Self-Correction (Reflexion) | Score → Critique → Rewrite → Re-score loop |
| Two-Layer Memory | Short-term LangGraph state + Long-term JSON persistence |
| Real-Time Intelligence | DuckDuckGo API for live web search |
| Prompt Engineering | Specialized system prompts per agent role |
| Error Handling | Retry logic + fallbacks for every failure mode |
| State Management | Shared TypedDict state across all agents |

---

## 🔮 Future Improvements

- Migrate to Qdrant Cloud for vector-based semantic memory search
- Add scheduling — run NexusAI automatically every morning
- Support more platforms (Instagram, Newsletter)
- Add goal alignment score tracking over time
- Implement brand consistency checker across all content
- Add streaming output — watch agents work in real time
- Support multiple user profiles
- Add export to Google Docs / Notion

---

## 💡 What I Learned Building This

- How to design and orchestrate multi-agent AI systems with LangGraph
- How self-correction loops (Reflexion architecture) work in practice
- How to build two-layer memory systems for persistent AI state
- How to gather and synthesize real-time web intelligence
- How to engineer specialized prompts for distinct agent roles
- How to handle production errors gracefully with fallbacks
- How to build and deploy full-stack AI applications for free

---

## 🎤 Interview Talking Points

**30-second pitch:**
> "NexusAI is an autonomous AI chief of staff. You give it your professional goal once — from that point it runs every day without input. It researches your domain using multi-agent web intelligence, cross-references findings against persistent long-term memory that grows smarter daily, auto-plans your priorities, writes platform-specific content, and runs a self-correction loop based on the Reflexion architecture that rewrites anything below a quality threshold before delivering it."

**Key technical depth:**
- LangGraph multi-agent state machines with 9 specialized nodes
- Reflexion-based self-correction with 6-metric quality rubric
- Two-layer memory — session state + persistent JSON storage
- Real-time web intelligence with DuckDuckGo API
- Production error handling with retry and fallback logic
- Deployed on Streamlit Cloud at zero cost

---

## 👤 Author

**Sathyapriya K**
Fresher AI Engineer | Building real autonomous AI systems

🔗 GitHub: https://github.com/SathyapriyaK123

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## ⭐ If You Found This Useful

Give it a star on GitHub — it helps others discover the project!
