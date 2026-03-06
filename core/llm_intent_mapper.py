import subprocess

ALLOWED_INTENTS = [
    "get_time",
    "search_google",
    "search_youtube",
    "open_notepad",
    "open_calculator",
    "open_whatsapp",
    "open_linkedin",
    "open_github",
    "open_spotify",
    "exit"
]

OLLAMA_MODEL = "mistral:7b-instruct-q4_K_M"

def llm_predict_intent(command: str) -> str:
    prompt = f"""
You are an intent classification engine.

Rules:
- Return ONLY one intent name from the list below
- If no intent matches, return: none
- Do NOT explain
- Do NOT add punctuation

Allowed intents:
{chr(10).join(ALLOWED_INTENTS)}

Command: {command}
"""

    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,   # ⬅ suppress noise
            encoding="utf-8",            # ⬅ CRITICAL FIX
            errors="ignore",             # ⬅ CRITICAL FIX
            timeout=20
        )

        output = result.stdout.strip().lower()

        for intent in ALLOWED_INTENTS:
            if output == intent:
                return intent

        return "none"

    except Exception as e:
        print(f"⚠️ LLM error: {e}")
        return "none"
