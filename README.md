🚀 AI Code Reviewer — Backend

🧠 Overview

This backend is a hybrid AI-powered Python code analysis engine that combines:

- AST-based static analysis
- Rule-based validation
- LLM-powered reasoning (OpenRouter)
- PostgreSQL database storage

It analyzes Python code, detects issues, assigns scores, and generates improved code.

---

⚙️ Tech Stack

- Python
- FastAPI
- AST (Abstract Syntax Tree)
- OpenRouter API (LLM)
- PostgreSQL
- SQLAlchemy

---

🏗️ Architecture

User Code
→ FastAPI API
→ AST Parser
→ Rule-Based Analyzer
→ Scoring Engine
→ AI Service (LLM)
→ Safety Layer
→ Database
→ Formatter
→ Response

---

📁 Project Structure

app/
├── main.py
├── database.py
├── models/
│   ├── code_request.py
│   └── review.py
├── routes/
├── services/
│   ├── parser.py
│   ├── analyzer.py
│   ├── scorer.py
│   ├── ai_service.py
│   └── formatter.py

---

🔁 Backend Flow

User Code
↓
Input Validation (Pydantic)
↓
AST Parsing
↓
Rule-Based Analysis
↓
Scoring Engine
↓
AI Review (LLM)
↓
Safety & Validation
↓
Save to Database
↓
Formatted Response

---

🔍 Features

✅ AST-Based Validation

- Detects syntax errors instantly
- Prevents invalid code execution

✅ Rule-Based Analysis
Detects:

- Missing ":"
- Invalid syntax
- Missing operators (e.g., "return x y")
- Inefficient loops ("range(len())")
- Unused variables
- Index out-of-range risks
- Division by zero
- Deep nesting / bad structure

---

📊 Scoring System

- Syntax Error → -50
- Logical Issue → -20
- Performance Issue → -10

---

🤖 AI Code Review

- Logical issue detection
- Performance suggestions
- Improved code generation

Prompt Used:
"You are a strict senior Python code reviewer..."

---

🧠 Response Parsing

AI output is converted into structured JSON:

{
"explanation": "...",
"suggestions": ["..."],
"improved_code": "..."
}

---

🛡️ Safety Layer

- Validates AI output using "ast.parse"
- Falls back to original code if needed
- Prevents empty or broken output
- Avoids over-optimization

---

🔧 Auto-Fix System

If AI fails:

- Adds missing ":"
- Fixes simple return issues
- Ensures valid Python output

---

🗄️ Database

- PostgreSQL + SQLAlchemy

Stores:

- Code
- Issues
- Score
- AI review

---

▶️ Run Backend

Command:
uvicorn app.main:app --reload

---
