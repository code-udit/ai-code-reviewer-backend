import requests
import ast
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# fetch configs from .env (instead of hardcoding)
API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL")
MODEL = os.getenv("OPENROUTER_MODEL")
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 20))


def is_valid_python(code: str):
    try:
        ast.parse(code)
        return True
    except Exception:
        return False


def get_ai_suggestions(code: str, issues: list):
    prompt = f"""
    You are a strict senior Python code reviewer.

    The code is written in Python. Always respond ONLY in Python.  

    Analyze this code carefully and detect ALL errors (syntax + logical + performance).  

    Code:  
    {code}  

    Issues detected:  
    {issues}  

    Rules:  
    - Do NOT miss any issue  
    - Always check for syntax errors (missing ':', operators, indentation, etc.)  
    - Detect logical issues, missing return, bad design  
    - Detect performance issues (like range(len()))  
    - Detect unused variables  
    - Be strict and detailed  
    - Suggest Pythonic improvements (e.g., avoid range(len()), use direct iteration)  

    🚨 VERY IMPORTANT:  
    - DO NOT change the original logic unnecessarily  
    - ONLY fix the issues  
    - Preserve structure unless absolutely required  
    - Prefer Pythonic improvements but DO NOT change behavior  
    - Do NOT over-optimize  

    Output format:  

    1. Explanation:  
    Explain ALL problems clearly in simple terms  

    2. Suggestions:  
    - Each issue must have a separate bullet point  
    - Include ALL fixes needed  

    3. Improved code:  
    Return ONLY correct Python code  
    No markdown  
    No explanation  
    """

    try:
        # simple safety check so we don't send request without API key
        if not API_KEY:
            return fallback()

        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=TIMEOUT
        )

        data = response.json()

        if "choices" not in data:
            return fallback()

        content = data["choices"][0]["message"]["content"]

        explanation = ""
        suggestions = []
        improved_code = ""
        mode = None

        for line in content.split("\n"):
            raw = line
            line = line.rstrip()
            lower = line.lower()

            if not line.strip():
                continue

            if "explanation" in lower:
                mode = "explanation"
                continue
            elif "suggestions" in lower:
                mode = "suggestions"
                continue
            elif "improved code" in lower:
                mode = "code"
                continue

            if mode == "explanation":
                explanation += line + " "

            elif mode == "suggestions":
                clean = line.replace("-", "").strip()
                if clean:
                    suggestions.append(clean)

            elif mode == "code":
                if "```" in line:
                    continue
                improved_code += raw + "\n"

        # validate AI output
        final_code = improved_code.strip()

        # fallback if AI gives invalid python
        if not final_code or not is_valid_python(final_code):
            final_code = code

            lines = final_code.split("\n")

            fixed_lines = []
            for line in lines:
                if line.strip().startswith("def ") and not line.strip().endswith(":"):
                    line = line + ":"

                if line.strip().startswith("return") and " " in line.strip() and "+" not in line:
                    parts = line.strip().split()
                    if len(parts) == 3:
                        line = f"    return {parts[1]} + {parts[2]}"

                fixed_lines.append(line)

            final_code = "\n".join(fixed_lines)

        # fix AI mistake where it converts "return x y" → "return x, y"
        if "return" in code:
            original_return_lines = [l for l in code.split("\n") if "return" in l]
            fixed_return_lines = [l for l in final_code.split("\n") if "return" in l]

            for o, f in zip(original_return_lines, fixed_return_lines):
                if " " in o and "," in f:
                    parts = o.strip().split()
                    if len(parts) == 3:
                        final_code = final_code.replace(f, f"    return {parts[1]} + {parts[2]}")

        # prevent AI from removing loops completely
        if ("for" in code or "while" in code) and ("for" not in final_code and "while" not in final_code):
            final_code = code

        # final safety fallback
        if not final_code.strip():
            final_code = code

        if not suggestions:
            suggestions = ["No suggestions generated"]

        return {
            "explanation": explanation.strip() or "No explanation",
            "suggestions": suggestions,
            "improved_code": final_code
        }

    except Exception:
        return fallback()


def fallback():
    return {
        "explanation": "AI failed",
        "suggestions": [],
        "improved_code": ""
    }