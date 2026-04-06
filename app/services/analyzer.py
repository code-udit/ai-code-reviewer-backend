import ast


def analyze_code(code: str):
    issues = []
    tree = None

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        issues.append({
            "type": "Syntax Error",
            "message": f"Syntax error: {e.msg} (line {e.lineno})"
        })

    if tree:
        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                # Long function
                if len(node.body) > 20:
                    issues.append({
                        "type": "Long Function",
                        "message": f"Function '{node.name}' is too long"
                    })

                # Too many parameters
                if len(node.args.args) > 5:
                    issues.append({
                        "type": "Too Many Parameters",
                        "message": f"Function '{node.name}' has too many parameters"
                    })

                # Missing return
                has_return = any(isinstance(n, ast.Return) for n in node.body)
                if not has_return:
                    issues.append({
                        "type": "Design",
                        "message": f"Function '{node.name}' has no return statement"
                    })

            # Division by zero
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                if isinstance(node.right, ast.Constant) and node.right.value == 0:
                    issues.append({
                        "type": "Runtime Risk",
                        "message": "Division by zero detected"
                    })

        if check_nesting(tree):
            issues.append({
                "type": "Deep Nesting",
                "message": "Code has deep nesting (>3 levels)"
            })

        issues.extend(detect_unused_variables(tree))
        issues.extend(detect_security_issues(tree))
        issues.extend(detect_performance_issues(tree))
        issues.extend(detect_style_issues(tree))

    issues.extend(detect_basic_errors(code))
    issues.extend(detect_indentation_issues(code))

    return issues


def check_nesting(node, level=0):
    if isinstance(node, (ast.If, ast.For, ast.While)):
        level += 1

    if level > 3:
        return True

    for child in ast.iter_child_nodes(node):
        if check_nesting(child, level):
            return True

    return False


def detect_basic_errors(code: str):
    issues = []

    lines = code.split("\n")

    for line in lines:
        stripped = line.strip()

        # Missing colon
        if stripped.startswith("def ") and not stripped.endswith(":"):
            issues.append({
                "type": "Syntax",
                "message": "Missing ':' at end of function definition"
            })

        # Missing operator
        if stripped.startswith("return"):
            content = stripped.replace("return", "").strip()

            # split words after return
            parts = content.split()

            # Only flag if multiple variables without operator (e.g. "return a b")
            if len(parts) >= 2 and not any(op in content for op in ["+", "-", "*", "/"]):
                issues.append({
                    "type": "Syntax",
                    "message": "Possible missing operator in return statement"
                })

        # ✅ NEW: Division by zero risk
        if "/" in stripped and "return" in stripped:
            issues.append({
                "type": "Runtime Risk",
                "message": "Possible division by zero"
            })

        # ✅ NEW: inefficient loop detection
        if "for" in stripped and "range(len(" in stripped:
            issues.append({
                "type": "Performance",
                "message": "Inefficient loop: use direct iteration instead of range(len())"
            })

        # Index error risk
        if "[" in stripped and "]" in stripped and "return" in stripped:
            issues.append({
                "type": "Runtime Risk",
                "message": "Possible index out of range access"
            })

    return issues


def detect_indentation_issues(code: str):
    issues = []
    lines = code.split("\n")

    for i, line in enumerate(lines):
        if line.startswith("def") and i + 1 < len(lines):
            next_line = lines[i + 1]
            if next_line and not next_line.startswith(" "):
                issues.append({
                    "type": "Indentation",
                    "message": "Expected indentation after function definition"
                })

    return issues


def detect_unused_variables(tree):
    assigned = set()
    used = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                assigned.add(node.id)
            elif isinstance(node.ctx, ast.Load):
                used.add(node.id)

    return [
        {
            "type": "Code Smell",
            "message": f"Variable '{var}' assigned but never used"
        }
        for var in (assigned - used)
    ]


def detect_security_issues(tree):
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "eval":
                issues.append({
                    "type": "Security",
                    "message": "Use of eval() is unsafe"
                })
    return issues


def detect_performance_issues(tree):
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            if isinstance(node.iter, ast.Call):
                if isinstance(node.iter.func, ast.Name) and node.iter.func.id == "range":
                    issues.append({
                        "type": "Performance",
                        "message": "Consider optimizing loop usage"
                    })
    return issues


def detect_style_issues(tree):
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name.isupper():
                issues.append({
                    "type": "Style",
                    "message": f"Function '{node.name}' should follow snake_case naming"
                })
    return issues