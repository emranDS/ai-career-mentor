# AI Career Mentor

A single Streamlit application that combines three AI-powered career tools into one clean, modern interface:

1. **Analyze Resume** — structured feedback, section-level scores, ATS checks, and rewrite suggestions.
2. **Match Jobs** — compare a resume against a job description and get a match score, matched and missing skills, keyword coverage, and recommendations.
3. **Optimize Resume** — a multi-agent workflow with three specialists running in parallel:
   - Resume Optimizer
   - Skill Gap Analyzer
   - Interview Preparation Agent

Built for Deep Learning course project track "AI Career Mentor" (Project 1 + Project 2 + Project 3 combined).

---

## Tech Stack

- **UI**: Streamlit with a custom top-navigation layout (no sidebar), custom CSS design system
- **LLM**: [OpenRouter](https://openrouter.ai) with `arcee-ai/trinity-large-preview:free` (swap models via env var)
- **Parsing**: `pypdf`, `python-docx` for resume ingestion
- **Agents**: Python `concurrent.futures` pool for parallel multi-agent execution

---

## Project Structure

```
AI Career Mentor/
├── app.py                      # Entry point — top nav + page router
├── requirements.txt
├── .env.example
├── .gitignore
├── .streamlit/
│   ├── config.toml             # Theme + hides sidebar by default
│   └── secrets.toml.example    # For Streamlit Community Cloud
├── assets/
│   └── styles.css              # Design tokens, cards, score ring, chips
├── src/
│   ├── config.py               # Loads secrets/env settings
│   ├── llm.py                  # OpenRouter client + JSON-mode helper
│   ├── prompts.py              # Prompt templates for every agent
│   ├── agents.py               # analyze / match / optimize / gap / interview
│   ├── resume_parser.py        # PDF, DOCX, TXT ingestion
│   └── ui.py                   # Reusable cards, chips, score ring, bars
└── views/
    ├── _common.py              # Shared resume input tabs (upload / paste)
    ├── analyze_resume.py       # Page 1
    ├── match_jobs.py           # Page 2
    └── optimize_resume.py      # Page 3 (multi-agent)
```

---

## Getting Started (Local)

### 1. Clone and Install

```bash
git clone <your-repo-url>.git
cd "AI Career Mentor"

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Credentials

Copy the example and add your OpenRouter key:

```bash
cp .env.example .env
```

Edit `.env`:

```
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=arcee-ai/trinity-large-preview:free
APP_URL=http://localhost:8501
APP_NAME=AI Career Mentor
```

Get a free API key at https://openrouter.ai/keys.

### 3. Run

```bash
streamlit run app.py
```

Open http://localhost:8501.

---

## Academic Integrity

This project is submitted as combined deliverable for the Deep Learning (CSE638) course at Daffodil International University, covering Project 1 (Basic LLM Application), Project 2 (RAG + Vector Database), and Project 3 (Agentic AI/Multi-Agent System) of the AI Career Mentor track.
