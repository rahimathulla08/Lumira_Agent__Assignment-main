import os
import re
import json
from datetime import datetime

try:
    import google.generativeai as genai
except Exception:
    genai = None


SYSTEM_INSTRUCTION = (
    "You are Lumira, a helpful assistant. Always think step-by-step and present "
    "clear, structured answers with short headings and bullet points where helpful. "
    "If the user asks for arithmetic (addition, subtraction, multiplication, division), "
    "do NOT compute it. Politely refuse and suggest using the calculator tool instead."
)


def is_arithmetic(query: str) -> bool:
    pattern = r"\b(\d+\s*[+\-*/xX]\s*\d+|add\b|sum\b|plus\b|subtract\b|minus\b|multiply\b|times\b|divide\b)"
    return re.search(pattern, query, flags=re.IGNORECASE) is not None


def init_llm():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment")
    if genai is None:
        raise RuntimeError("google-generativeai package not available")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION,
    )


def ask_llm(model, prompt: str) -> str:
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.6,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 1024,
        },
    )
    return response.text


def main():
    print("Lumira (Level 1) — type 'exit' to quit")
    model = init_llm()

    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"level1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl")

    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()  # newline
            break
        if not query:
            continue
        if query.lower() in {"exit", "quit"}:
            break

        if is_arithmetic(query):
            answer = (
                "I won't solve arithmetic directly. Please use the calculator tool.\n"
                "- Tip: In Level 2, the assistant can call the calculator automatically."
            )
        else:
            answer = ask_llm(model, query)

        print(f"Lumira: {answer}\n")

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"timestamp": datetime.now().isoformat(), "user": query, "assistant": answer}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()


