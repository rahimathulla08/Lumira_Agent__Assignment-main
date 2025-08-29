import os
import re
import json
from datetime import datetime
from typing import List, Dict

from calculator_tool import calculate
from translator_tool import translate_en_to_de

try:
    import google.generativeai as genai
except Exception:
    genai = None


SYSTEM = (
    "You are Lumira, an agent that plans multi-step tasks."
    "Break the user request into ordered steps. For each step, decide if you can answer "
    "directly or need a tool (calculator or translator). Return a JSON plan with steps: "
    "[{step: number, action: 'llm'|'calculator'|'translator', input: string}]."
)


def init_llm():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment")
    if genai is None:
        raise RuntimeError("google-generativeai package not available")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM)


def propose_plan(model, query: str) -> List[Dict]:
    prompt = (
        "Given the user query, output ONLY JSON with 'steps' as a list. "
        "Each item: {step, action, input}. Use 'calculator' for arithmetic, 'translator' for "
        "English to German. Otherwise 'llm'.\n\n"
        f"User: {query}\n"
        "JSON:"
    )
    text = model.generate_content(prompt).text
    try:
        data = json.loads(text)
        return data.get("steps", [])
    except Exception:
        # fallback: naive single-step
        return [{"step": 1, "action": "llm", "input": query}]


def run_step(model, step):
    action = step.get("action")
    inp = step.get("input", "")
    if action == "calculator":
        m = re.search(r"(\d+)\s*([+\-*/xX])\s*(\d+)", inp)
        if not m:
            return "Calculator: could not parse input"
        a, op, b = m.groups()
        return str(calculate(int(a), op, int(b)))
    if action == "translator":
        return translate_en_to_de(inp)
    # default LLM
    return model.generate_content(inp).text


def main():
    print("Lumira (Level 3) — type 'exit' to quit")
    model = init_llm()
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"level3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl")

    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not query:
            continue
        if query.lower() in {"exit", "quit"}:
            break

        plan = propose_plan(model, query)
        results = []
        for step in plan:
            out = run_step(model, step)
            results.append({"step": step.get("step"), "action": step.get("action"), "input": step.get("input"), "output": out})

        # Summarize for the user
        summary_prompt = (
            "Summarize these step results clearly with headings and bullets.\n\n" + json.dumps(results, ensure_ascii=False)
        )
        final_answer = model.generate_content(summary_prompt).text
        print(f"Lumira: {final_answer}\n")

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"timestamp": datetime.now().isoformat(), "user": query, "plan": plan, "results": results, "final": final_answer}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()


