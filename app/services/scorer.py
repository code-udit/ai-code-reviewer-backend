def calculate_score(issues):
    if not issues:
        return 100

    score = 100

    for issue in issues:
        t = issue.get("type", "")

        if t == "Syntax Error":
            score -= 40
        elif t == "Indentation":
            score -= 20
        elif t == "Runtime Risk":
            score -= 20
        elif t == "Security":
            score -= 25
        elif t == "Performance":
            score -= 10
        elif t == "Long Function":
            score -= 15
        elif t == "Too Many Parameters":
            score -= 10
        elif t == "Deep Nesting":
            score -= 15
        elif t == "Design":
            score -= 10
        elif t == "Code Smell":
            score -= 5
        elif t == "Style":
            score -= 5
        else:
            score -= 5

    return max(score, 0)