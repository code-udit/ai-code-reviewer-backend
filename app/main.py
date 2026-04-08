from fastapi import FastAPI, HTTPException
from app.models.code_request import CodeRequest
from app.services.parser import parse_code
from app.services.analyzer import analyze_code
from app.services.scorer import calculate_score
from app.services.ai_service import get_ai_suggestions
from app.database import engine
from app.models.review import Review
from app.database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/health") 
def health():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Review.metadata.create_all(bind=engine)


@app.post("/analyze")
def analyze_code_endpoint(request: CodeRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    parsed_data = parse_code(request.code)
    error_message = parsed_data.get("error")

    issues = analyze_code(request.code)

    if error_message:
        issues.insert(0, {
            "type": "Syntax Error",
            "message": error_message
        })

    score = calculate_score(issues)
    ai_response = get_ai_suggestions(request.code, issues)

    db = SessionLocal()
    try:
        review = Review(
            code=request.code,
            issues=str(issues),
            score=score,
            ai_review=str(ai_response)
        )
        db.add(review)
        db.commit()
    finally:
        db.close()

    return {
        "success": True,
        "data": {
            "parsed": parsed_data,
            "issues": issues,
            "score": score,
            "ai_review": ai_response,
            "error": error_message
        }
    }