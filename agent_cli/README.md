# Lumira Agent CLI

Three levels of a Python assistant demonstrating LLM integration, tool use, and agentic multi-step reasoning.

## Setup
1) Python 3.10+
2) Install deps:
```
pip install google-generativeai
```
3) Set environment:
```
# Windows CMD
set GEMINI_API_KEY=your_key_here
# PowerShell
$env:GEMINI_API_KEY="your_key_here"
# Linux/macOS
export GEMINI_API_KEY=your_key_here
```

## Level 1 — LLM-Only (chatbot.py)
- Refuses arithmetic and suggests calculator tool
- Step-by-step, structured outputs
```
python agent_cli/chatbot.py
```

## Level 2 — LLM + One Tool (chatbot_with_tool.py)
- Detects arithmetic and uses calculator_tool.py
```
python agent_cli/chatbot_with_tool.py
```

## Level 3 — Agentic Multi-Step (full_agent.py)
- Plans steps, calls tools (calculator_tool.py, translator_tool.py), summarizes
```
python agent_cli/full_agent.py
```

Logs are written to agent_cli/logs/*.jsonl

## Mandatory Use Cases
Try the assignment prompts from your brief for each level and capture logs.
