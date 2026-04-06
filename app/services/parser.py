import ast

def parse_code(code: str):
    try:
        tree = ast.parse(code)
    except Exception:
        return {
            "error": "Invalid Python code"
        }

    functions = []
    variables = []
    loops = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variables.append(target.id)

        elif isinstance(node, (ast.For, ast.While)):
            loops.append(type(node).__name__)

    return {
        "functions": functions,
        "variables": variables,
        "loops": loops
    }