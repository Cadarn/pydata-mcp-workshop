# MCP Workshop - PyData Amsterdam

**Large Language Models (LLMs) are unlocking transformative capabilities  but integrating them into complex, real-world applications remains a major challenge.**

This workshop introduces the Model Context Protocol (MCP), an emerging open standard designed to simplify and standardise LLM integration with tools, structured data, and live context.

## Workshop Overview

We'll build from core concepts to a fully functional AI Research Assistant through hands-on examples covering:

- **Core MCP Concepts**: Client-server architecture, tools, and resources
- **Development Setup**: FastMCP, Typer, Streamlit with OpenAI API or Ollama
- **MCP Server Development**: Wikipedia search-and-summarisation example
- **Client Development**: CLI (Typer) interfaces with Web (Streamlit) as take-home
- **LLM Orchestration**: Autonomous tool selection and chaining
- **Final Project**: AI Research Assistant prototype

## Project Structure

```
├── solution/              # Complete working implementations
│   ├── examples/          # Core MCP demonstrations
│   ├── servers/          # Full MCP server implementations
│   ├── clients/          # Complete CLI and web clients
│   └── research_assistant/ # Final project solution
├── workshop/              # Starter code and exercises
│   ├── examples/          # Partial implementations to complete
│   ├── servers/          # Server templates with TODOs
│   ├── clients/          # Client starters with exercises
│   └── research_assistant/ # Final project scaffold
├── docs/                  # Workshop documentation
├── tutorials/             # Step-by-step guides with exercises
└── docker/               # Containerization configs
```

## Workshop Approach

- **`workshop/` folder**: Contains starter code, templates, and exercises for hands-on learning
- **`solution/` folder**: Complete working implementations for reference and comparison
- **Progressive building**: Each section builds on previous work with clear exercise points

## Prerequisites

- Python 3.13+ (managed with uv)
- Docker (recommended)
- LLM access (OpenAI API or local Ollama)
- Basic Python and command-line familiarity

## Setup Instructions

### 1. Clone and Setup Python Environment

```bash
# Clone the repository
git clone <repository-url>
cd pydata-mcp-workshop

# Create a new Python 3.13 virtual environment
uv venv --python 3.13

# Activate the virtual environment
source .venv/bin/activate

# Install all dependencies
uv sync
```

### 2. LLM Backend Setup

Choose **one** of the following options:

#### Option A: OpenAI API (Recommended for reliability)

1. Create a `.env` file from the template:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your_api_key_here
   ```

3. Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)

#### Option B: Local Ollama (Free alternative)

1. Install Ollama from [ollama.ai](https://ollama.ai)

2. Download the lightweight model:
   ```bash
   ollama pull qwen3:1.7b
   ```

3. Verify Ollama is running:
   ```bash
   ollama list
   ```

### 3. Verify Setup

Test your installation:
```bash
# Check Python version (using uv to ensure correct environment)
uv run python --version  # Should be 3.13+

# Test imports
uv run python -c "import fastmcp, pydantic_ai, typer, streamlit; print('✅ All imports successful')"

# Start Jupyter for tutorials
uv run jupyter lab
```

## Quick Start

1. **Follow the Tutorial**: Start with `tutorials/01-mcp-fundamentals.ipynb`

2. **Work in `workshop/`**: Complete exercises and compare with `solution/`

3. **Test Your Progress**: Run solution files to see expected behavior
   ```bash
   # Workshop focus: Run Wikipedia server
   uv run python solution/servers/wikipedia_server.py

   # Workshop focus: Run CLI client
   uv run python solution/clients/cli_client.py --help

   # Take-home: Run web client (solution provided)
   uv run streamlit run solution/clients/web_client.py
   ```

## Learning Path

1. **MCP Fundamentals** - Core concepts and architecture
2. **Server Development** - Build Wikipedia search tool
3. **Client Development** - CLI and web interfaces
4. **LLM Orchestration** - Autonomous tool usage
5. **Final Project** - AI Research Assistant

By the end, you'll have practical skills to build intelligent, modular, and extensible LLM-native applications using MCP.