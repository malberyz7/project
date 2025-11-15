from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pathlib import Path
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="IELTS Prep API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    id: int
    part: str
    prompt: str
    choices: List[str] = []
    answer: str | None = None


class AnswerPayload(BaseModel):
    answers: Dict[int, str]


SAMPLE_QUESTIONS = [
    Question(id=1, part="Listening", prompt="You will hear a short conversation. What is the main topic?", choices=["Travel", "Weather", "Job", "Sports"], answer="Travel"),
    Question(id=2, part="Reading", prompt="Choose the best summary of the paragraph.", choices=["A", "B", "C", "D"], answer="C"),
    Question(id=3, part="Writing", prompt="Write an essay about the advantages of studying abroad.", choices=[], answer=None),
    Question(id=4, part="Speaking", prompt="Describe a memorable trip you had.", choices=[], answer=None),
]


@app.get("/api/questions", response_model=List[Question])
def list_questions(part: str | None = None):
    if part:
        return [q for q in SAMPLE_QUESTIONS if q.part.lower() == part.lower()]
    return SAMPLE_QUESTIONS


@app.post("/api/score")
def score_answers(payload: AnswerPayload):
    # Simple scoring: for questions with known answers, compare
    correct = 0
    total = 0
    for q in SAMPLE_QUESTIONS:
        if q.answer is not None:
            total += 1
            ans = payload.answers.get(q.id)
            if ans and ans == q.answer:
                correct += 1
    if total == 0:
        return {"score": None, "message": "No auto-gradable questions available"}
    return {"score": correct, "total": total, "percent": round(correct / total * 100, 2)}


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Serve frontend static build if it exists (frontend/dist)
BASE_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = BASE_DIR / "frontend" / "dist"
if DIST_DIR.exists():
    # Mount the built frontend at the root. API routes take precedence.
    app.mount("/", StaticFiles(directory=str(DIST_DIR), html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return RedirectResponse(url="/docs")
