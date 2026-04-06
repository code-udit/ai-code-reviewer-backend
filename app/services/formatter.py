def format_response(parsed, issues, score, ai_review):
    return {
        "success": True,
        "data": {
            "parsed": parsed,
            "issues": issues,
            "score": score,
            "ai_review": ai_review
        }
    }