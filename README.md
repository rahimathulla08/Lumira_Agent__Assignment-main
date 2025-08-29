# Python Software Engineer Assignment: LLM + Agentic Thinking

## 📌 Overview
This project is a **multi-level Python application** that demonstrates the use of **LLM APIs**, **basic tool integration**, and **agentic multi-step reasoning**.  
It progresses in complexity across three levels:

- 🟢 **Level 1 — LLM-Only Smart Assistant** (Prompt Engineering Focus)  
- 🟡 **Level 2 — LLM + Tool Integration** (Calculator)  
- 🔴 **Level 3 — Agentic AI with Multi-Step Tasks** (Translator + Calculator + LLM)  

The goal is to showcase **prompt engineering**, **tool usage**, and **multi-step reasoning**.

---

## 🟢 Level 1 — LLM-Only Smart Assistant
### Problem Statement
- Build a Python CLI program that takes a user question and sends it to an LLM (Gemini, OpenAI, etc.).
- Force the LLM to **think step-by-step** and structure answers clearly.

### Mandatory Use Cases
- `What are the colors in a rainbow?` → List step-by-step  
- `Tell me why the sky is blue?` → Step-by-step explanation  
- `Which planet is the hottest?` → Reason and explain  
- `What is 15 + 23?` → Refuse, suggest using calculator  

### Deliverables
- `chatbot.py`
- Example interactions
- Logs (`logs_level1.txt`)

---

## 🟡 Level 2 — LLM + Basic Tool (Calculator)
### Problem Statement
- Extend Level 1 program.  
- If a **math calculation** is detected, the chatbot calls a `calculator_tool.py` (instead of solving itself).

### Mandatory Use Cases
- `What is 12 times 7?` → Use calculator tool  
- `Add 45 and 30` → Use calculator tool  
- `What is the capital of France?` → LLM answers  
- `Multiply 9 and 8, and also tell me the capital of Japan.` → Graceful failure (no multi-step yet)  

### Deliverables
- `chatbot_with_tool.py`
- `calculator_tool.py`
- Logs (`logs_level2.json`)

---

## 🔴 Level 3 — Agentic AI with Multi-Step Tasks
### Problem Statement
- Extend Level 2 into a **full agent** that can:  
  - Break tasks into steps  
  - Call multiple tools (translator + calculator)  
  - Maintain memory across tasks  

### Tools
- `translator_tool.py` → English → German translation  
- `calculator_tool.py` → Addition + Multiplication  

### Mandatory Use Cases
- `Translate 'Good Morning' into German and then multiply 5 and 6.`  
- `Add 10 and 20, then translate 'Have a nice day' into German.`  
- `Tell me the capital of Italy, then multiply 12 and 12.`  
- `Translate 'Sunshine' into German.`  
- `Add 2 and 2 and multiply 3 and 3.`  
- `What is the distance between Earth and Mars?` (LLM direct answer)  

### Deliverables
- `full_agent.py`
- `translator_tool.py`
- `calculator_tool.py`
- Full logs (`logs_level3.json`)

---


## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/lasyagovindwar/Lumira_Agent__Assignment.git
cd Lumira_Agent__Assignment
