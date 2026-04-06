# Repository Analysis

## Overview

This repository is **Ed Donner's "Master AI Agentic Engineering"** course — a 6-week curriculum teaching how to build AI agents using five major frameworks: **OpenAI Agents SDK**, **CrewAI**, **LangGraph**, **AutoGen**, and **MCP (Model Context Protocol)**.

It is an educational monorepo organized by weekly modules, featuring Python scripts, Jupyter notebooks, and extensive community contributions. It is **not** a single deployable application but rather a collection of labs, demos, and small projects.

---

## Quick Stats

| Metric | Value |
|--------|-------|
| Language | Python 3.12+ |
| Core Python files | ~64 (excluding community contributions) |
| Jupyter notebooks | ~34 (excluding community contributions) |
| Package manager | uv (with `pyproject.toml`, `uv.lock`, compiled `requirements.txt`) |
| Root dependencies | ~40 direct, ~690 lines pinned |
| CI/CD | None configured |
| Tests | Sparse/localized (unittest, pytest in a few subprojects) |
| License | MIT (2025 Ed Donner) |

---

## Project Structure

```
/workspace
├── README.md              # Course introduction and setup instructions
├── LICENSE                 # MIT License
├── pyproject.toml          # Root project config (name: "agents", Python ≥3.12)
├── requirements.txt        # Pinned dependencies (auto-generated via uv)
├── uv.lock                 # UV lockfile for reproducible installs
├── .gitignore
│
├── guides/                 # Teaching notebooks (Python, git, CLI, APIs, Ollama, etc.)
├── setup/                  # Platform-specific setup docs + diagnostics.py
│
├── 1_foundations/           # Week 1: Gradio + OpenAI chatbot patterns, function calling
├── 2_openai/               # Week 2: OpenAI Agents SDK, deep research orchestrator
├── 3_crew/                 # Week 3: CrewAI projects (debate, engineering, stock picker, etc.)
├── 4_langgraph/            # Week 4: LangGraph state graphs, tool nodes, sidekick apps
├── 5_autogen/              # Week 5: Microsoft AutoGen, gRPC distributed agents
└── 6_mcp/                  # Week 6: MCP servers/clients, trading floor capstone
```

Each weekly folder contains:
- **Lab notebooks** (`1_lab1.ipynb`, `2_lab2.ipynb`, ...)
- **Python scripts** (entry points like `app.py`, `main.py`)
- **`community_contributions/`** subfolder with student-submitted extensions

---

## Weekly Module Breakdown

### Week 1 — Foundations (`1_foundations/`)
- **Focus:** Gradio UI + OpenAI Chat Completions + function calling (tools)
- **Key file:** `app.py` — loads a PDF resume via `PdfReader`, defines JSON-schema tools, integrates Pushover notifications
- **Pattern:** Single-agent chatbot with tool use

### Week 2 — OpenAI Agents SDK (`2_openai/`)
- **Focus:** OpenAI Agents SDK (`openai-agents`), multi-agent orchestration
- **Key package:** `deep_research/` — async Gradio UI with `ResearchManager` orchestrating a pipeline: planner → parallel search → writer → email (via SendGrid)
- **Pattern:** Multi-agent pipeline with streaming `yield` to Gradio

### Week 3 — CrewAI (`3_crew/`)
- **Focus:** CrewAI framework for team-based agents
- **Subprojects:** `debate/`, `engineering_team/`, `stock_picker/`, `financial_researcher/`, `coder/`
- **Pattern:** `@CrewBase` decorator + YAML-driven agent/task configs (`agents.yaml`, `tasks.yaml`)
- **Entry:** `crewai run` or `uv run main.py`
- Each subproject has its own `pyproject.toml` and `src/<package>/` layout

### Week 4 — LangGraph (`4_langgraph/`)
- **Focus:** LangGraph state graphs, tool nodes, LangSmith tracing
- **Key files:** `sidekick.py`, `sidekick_tools.py`, `app.py`
- **Pattern:** `StateGraph` with `ToolNode` / `tools_condition` (ReAct-style loops)
- **Persistence:** `langgraph-checkpoint-sqlite` for graph state

### Week 5 — AutoGen (`5_autogen/`)
- **Focus:** Microsoft AutoGen distributed agents
- **Key files:** `agent.py` (extends `RoutedAgent`), `creator.py`, `world.py` (gRPC runtime), `messages.py`
- **Pattern:** `GrpcWorkerAgentRuntime` with message routing between agents

### Week 6 — MCP & Capstone (`6_mcp/`)
- **Focus:** Model Context Protocol servers/clients, trading floor demo
- **Key files:**
  - `database.py` — SQLite helpers (accounts, logs, market tables)
  - `accounts.py` / `market.py` — Pydantic domain models, Polygon.io market data
  - `accounts_server.py` / `market_server.py` / `push_server.py` — FastMCP tool servers
  - `traders.py` — OpenAI Agents SDK + MCP, multi-provider model routing (OpenRouter, DeepSeek, Grok, Gemini)
  - `app.py` — Gradio UI with Plotly charts and trading logs
- **Pattern:** Domain model + persistence + MCP tool servers + multi-agent trading

---

## Architecture & Design Patterns

Since this is a course repo, there is no single unified architecture. Instead, recurring patterns appear across modules:

| Pattern | Where Used |
|---------|------------|
| **Multi-agent pipeline/orchestrator** | `2_openai/deep_research/` (plan → search → write → email) |
| **Tool/function calling** | `1_foundations/` (OpenAI tools), `4_langgraph/` (ToolNode) |
| **MCP server/client** | `6_mcp/` (FastMCP servers exposing tools/resources) |
| **CrewAI team pattern** | `3_crew/` (@CrewBase + YAML agents/tasks) |
| **Distributed agent runtime** | `5_autogen/` (gRPC workers + message routing) |
| **Strategy pattern (model selection)** | `6_mcp/traders.py` — `get_model()` picks client by name |
| **Domain model + persistence** | `6_mcp/` — Pydantic models + SQLite via `database.py` |
| **Informal MVC** | `6_mcp/app.py` — `Trader` (model/state) + `TraderView` (Gradio UI) |

---

## Key Dependencies

| Category | Packages |
|----------|----------|
| **LLM Providers** | `openai`, `anthropic`, `langchain-openai`, `langchain-anthropic` |
| **Agent Frameworks** | `openai-agents`, `langgraph`, `autogen-agentchat`, `autogen-ext`, `semantic-kernel` |
| **LangChain Ecosystem** | `langchain-community`, `langchain-experimental`, `langsmith`, `langfuse` |
| **MCP** | `mcp[cli]`, `mcp-server-fetch`, `smithery` |
| **Web UI** | `gradio`, `plotly`, `ipywidgets` |
| **Data/Parsing** | `pypdf`, `pypdf2`, `bs4`, `lxml`, `wikipedia`, `playwright` |
| **APIs** | `polygon-api-client`, `sendgrid`, `requests`, `httpx` |
| **Utilities** | `python-dotenv`, `psutil`, `speedtest-cli`, `setuptools` |

---

## External Service Integrations

| Service | Purpose | Where |
|---------|---------|-------|
| **OpenAI** | Chat completions, Agents SDK, tracing | Throughout |
| **Anthropic (Claude)** | Alternative LLM provider | Root deps, notebooks |
| **Google Gemini** | Via OpenAI-compatible base URL | `6_mcp/traders.py` |
| **DeepSeek / Grok / OpenRouter** | Alternative model providers | `6_mcp/traders.py` |
| **Polygon.io** | Stock market data | `6_mcp/market.py` |
| **SendGrid** | Transactional email | `2_openai/deep_research/` |
| **Pushover** | Push notifications | `1_foundations/app.py`, `6_mcp/push_server.py` |
| **LangSmith** | LLM observability/tracing | `4_langgraph/` notebooks |
| **Langfuse** | LLM observability | `6_mcp/` notebooks |
| **Brave Search** | Web search via MCP | `6_mcp/mcp_params.py` |

---

## Storage

- **SQLite** (`accounts.db`) in `6_mcp/` — tables: `accounts`, `logs`, `market`
- **LangGraph checkpoint SQLite** — used in LangGraph labs for persistent graph state
- **File outputs** — CrewAI projects write to `output/` directories (markdown, JSON)
- No centralized production database

---

## Testing

Testing is minimal and localized:
- **unittest**: `3_crew/engineering_team/example_output_new/test_accounts.py` (generated example)
- **pytest**: `3_crew/community_contributions/ghost_writer/` has test files
- No root test configuration (`pytest.ini`, `tox.ini`, etc.)
- Primary verification is via **running notebooks** and **executing scripts**

---

## CI/CD

- **None configured** — no `.github/workflows/`, `.gitlab-ci.yml`, or other pipeline definitions
- No linting configuration (ruff, flake8, etc.) beyond `.gitignore` entries

---

## How to Run

1. **Setup:** Follow platform-specific guides in `setup/` (Mac, PC, Linux)
2. **Install:** `uv sync` at the root (or `uv pip install -r requirements.txt`)
3. **Environment:** Create `.env` with API keys (`OPENAI_API_KEY`, etc.)
4. **Run diagnostics:** `python setup/diagnostics.py`
5. **Week-specific:**
   - Notebooks: Open in Jupyter/VS Code
   - Scripts: `uv run app.py` or `python app.py`
   - CrewAI: `cd 3_crew/<project> && crewai run`

---

## Summary

This is a well-structured educational repository covering the major AI agent frameworks in Python. It emphasizes hands-on learning through Jupyter notebooks and runnable demos, with Gradio providing web UIs. The codebase demonstrates progressively more sophisticated agent patterns — from single chatbots with tool use, through multi-agent orchestration, to distributed systems with MCP and gRPC. Community contributions significantly extend the base material with alternative implementations and integrations.
