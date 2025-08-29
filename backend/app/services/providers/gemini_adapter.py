# app/services/providers/gemini_adapter.py
import time
import google.generativeai as genai
from app.config import settings

# Configure Gemini client
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

SYSTEM_PROMPT = (
    "You are a Python software engineer's assistant for a 3-level assignment.\n\n"
    "Your behavior depends on the LEVEL:\n\n"
    "🟢 LEVEL 1 (LLM-Only Assistant):\n"
    "- Always answer step-by-step.\n"
    "- For math calculations (like 2+2), DO NOT solve directly. Instead, say:\n"
    "  \"I cannot calculate this, please use the calculator tool.\"\n"
    "- Example:\n"
    "  User: What are the colors in a rainbow?\n"
    "  Assistant: Step 1: Sunlight... Step 2: Refraction... Step 3: The seven colors are ...\n\n"
    "🟡 LEVEL 2 (LLM + Calculator Tool):\n"
    "- Answer normally for non-math questions.\n"
    "- If the question involves a math calculation, CALL the calculator tool instead of solving it yourself.\n"
    "- If multiple tasks are combined (e.g., math + fact lookup), say you cannot yet handle multi-step queries.\n"
    "- Example:\n"
    "  User: What is 12 * 7?\n"
    "  Assistant: [Call calculator_tool(\"12*7\")] → \"The answer is 84.\"\n\n"
    "🔴 LEVEL 3 (Full Agentic AI):\n"
    "- Break down multi-step queries into smaller steps.\n"
    "- For math → call calculator_tool.\n"
    "- For translations → call translator_tool.\n"
    "- For knowledge/facts → answer directly.\n"
    "- Maintain memory of steps and chain results together.\n"
    "- Example:\n"
    "  User: Translate \"Good Morning\" into German and multiply 5 and 6.\n"
    "  Assistant:\n"
    "    Step 1: [translator_tool(\"Good Morning\")] → \"Guten Morgen\"\n"
    "    Step 2: [calculator_tool(\"5*6\")] → 30\n"
    "    Final Answer: \"In German: Guten Morgen. The multiplication result is 30.\"\n\n"
    "GENERAL RULES:\n"
    "- Always output in a clear structured format (steps + final answer).\n"
    "- Explicitly mention tool calls when used.\n"
    "- Never mix up the levels.\n"
    "- Respect refusals when required (Level 1 math problems).\n"
)

def query_gemini(prompt: str, level: int | None = None, max_retries: int = 1) -> str:
    """
    Query Gemini and return the text response.
    Handles quota exceeded errors gracefully.
    """
    if not settings.GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not set"

    for attempt in range(1, max_retries + 1):
        try:
            # Use a lighter model; inject system prompt and selected level
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                system_instruction=SYSTEM_PROMPT,
            )
            chosen_level = level if level in (1, 2, 3) else 3
            composed_prompt = f"LEVEL: {chosen_level}\nUser: {prompt}"
            response = model.generate_content(
                composed_prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                },
            )
            return response.text
        except Exception as e:
            err_msg = str(e)
            # Check if it's a quota error
            if "429" in err_msg or "quota" in err_msg.lower():
                wait_time = 5 * attempt  # shorter backoff to avoid long hangs
                print(f"Quota exceeded. Retrying in {wait_time}s (attempt {attempt}/{max_retries})...")
                time.sleep(wait_time)
                continue
            # For other errors, return immediately
            return f"Error querying Gemini: {e}"

    return "Error: Gemini API quota exceeded. Please try again later."
