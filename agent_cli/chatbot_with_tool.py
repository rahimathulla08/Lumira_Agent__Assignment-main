import os
import re
import json
from datetime import datetime
from calculator_tool import calculate

try:
    import google.generativeai as genai
except Exception:
    genai = None


SYSTEM_INSTRUCTION = (
    "You are Lumira, a helpful assistant. Think step-by-step and structure answers clearly. "
    "If arithmetic is requested, DO NOT compute it yourself. Instead, say you will call the calculator tool."
)


def find_arithmetic(query: str):
    m = re.search(r"(\d+)\s*([+\-*/xX])\s*(\d+)", query)
    if not m:
        return None
    a, op, b = m.groups()
    return int(a), op, int(b)


def init_llm():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment")
    if genai is None:
        raise RuntimeError("google-generativeai package not available")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_INSTRUCTION)


def ask_llm(model, prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text


def main():
    print("Lumira (Level 2) — type 'exit' to quit")
    model = init_llm()

    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"level2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl")

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

        parsed = find_arithmetic(query)
        if parsed:
            a, op, b = parsed
            try:
                result = calculate(a, op, b)
                answer = (
                    f"Using calculator tool: {a} {op} {b} = {result}\n"
                    "- Note: I used the calculator tool as required."
                )
            except Exception as e:
                answer = f"Calculator error: {e}"
        else:
            answer = ask_llm(model, query)

        print(f"Lumira: {answer}\n")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"timestamp": datetime.now().isoformat(), "user": query, "assistant": answer}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()


