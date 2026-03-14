import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from db import init_db, get_connection
from schemas import (
    NoteCreate,
    AskRequest,
    FlashcardRequest,
    QuizRequest,
    StudyPlanRequest,
    SummaryRequest,
)
from ai_service import (
    summarize_note,
    answer_question,
    generate_flashcards,
    generate_quiz,
    generate_study_plan,
)
from retriever import retrieve_top_chunks

app = FastAPI(title="Smart Study Assistant Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {"message": "Smart Study Assistant Agent API is running"}


@app.get("/dashboard")
def dashboard():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as count FROM notes")
    notes_count = cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) as count FROM flashcards")
    flashcards_count = cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) as count FROM quizzes")
    quizzes_count = cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) as count FROM study_plans")
    plans_count = cur.fetchone()["count"]

    conn.close()

    return {
        "notes_count": notes_count,
        "flashcards_count": flashcards_count,
        "quizzes_count": quizzes_count,
        "study_plans_count": plans_count,
    }


@app.post("/notes")
def create_note(payload: NoteCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notes (subject, title, content) VALUES (?, ?, ?)",
        (payload.subject, payload.title, payload.content),
    )
    conn.commit()
    note_id = cur.lastrowid
    conn.close()

    return {"message": "Note created", "note_id": note_id}


@app.get("/notes")
def list_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, subject, title, content, created_at FROM notes ORDER BY id DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


@app.get("/notes/{note_id}")
def get_note(note_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Note not found")
    return dict(row)


@app.post("/summarize")
def summarize(payload: SummaryRequest):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes WHERE id = ?", (payload.note_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Note not found")

    summary = summarize_note(row["content"])
    return {"note_id": payload.note_id, "summary": summary}


@app.post("/ask")
def ask_question(payload: AskRequest):
    conn = get_connection()
    cur = conn.cursor()

    if payload.subject:
        cur.execute(
            "SELECT id, subject, title, content FROM notes WHERE subject = ?",
            (payload.subject,),
        )
    else:
        cur.execute("SELECT id, subject, title, content FROM notes")

    notes = [dict(r) for r in cur.fetchall()]
    conn.close()

    if not notes:
        raise HTTPException(status_code=404, detail="No notes found")

    contexts = retrieve_top_chunks(payload.question, notes)
    answer = answer_question(payload.question, contexts)

    return {
        "question": payload.question,
        "contexts_used": contexts,
        "answer": answer,
    }


@app.post("/flashcards/generate")
def create_flashcards(payload: FlashcardRequest):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes WHERE id = ?", (payload.note_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found")

    try:
        cards = generate_flashcards(row["content"], payload.count)
    except Exception as exc:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Flashcard generation failed: {str(exc)}")

    for card in cards:
        cur.execute(
            "INSERT INTO flashcards (note_id, question, answer) VALUES (?, ?, ?)",
            (payload.note_id, card["question"], card["answer"]),
        )

    conn.commit()
    conn.close()

    return {"note_id": payload.note_id, "flashcards": cards}


@app.get("/flashcards/{note_id}")
def get_flashcards(note_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, question, answer, created_at FROM flashcards WHERE note_id = ? ORDER BY id DESC",
        (note_id,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


@app.post("/quiz/generate")
def create_quiz(payload: QuizRequest):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes WHERE id = ?", (payload.note_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Note not found")

    try:
        quiz = generate_quiz(row["content"], payload.difficulty, payload.count)
    except Exception as exc:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {str(exc)}")

    cur.execute(
        "INSERT INTO quizzes (note_id, title, quiz_json) VALUES (?, ?, ?)",
        (payload.note_id, quiz.get("title", "Generated Quiz"), json.dumps(quiz)),
    )
    quiz_id = cur.lastrowid
    conn.commit()
    conn.close()

    return {"quiz_id": quiz_id, "quiz": quiz}


@app.get("/quizzes")
def get_quizzes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, note_id, title, quiz_json, created_at FROM quizzes ORDER BY id DESC")
    rows = []
    for r in cur.fetchall():
        item = dict(r)
        item["quiz_json"] = json.loads(item["quiz_json"])
        rows.append(item)
    conn.close()
    return rows


@app.post("/study-plan")
def create_study_plan(payload: StudyPlanRequest):
    try:
        plan = generate_study_plan(
            exam_date=payload.exam_date,
            hours_per_day=payload.hours_per_day,
            weak_topics=payload.weak_topics,
            subjects=payload.subjects,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Study plan generation failed: {str(exc)}")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO study_plans (title, exam_date, hours_per_day, weak_topics, plan_json) VALUES (?, ?, ?, ?, ?)",
        (
            plan.get("title", "Study Plan"),
            payload.exam_date,
            payload.hours_per_day,
            ", ".join(payload.weak_topics),
            json.dumps(plan),
        ),
    )
    plan_id = cur.lastrowid
    conn.commit()
    conn.close()

    return {"plan_id": plan_id, "plan": plan}


@app.get("/study-plans")
def get_study_plans():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM study_plans ORDER BY id DESC")
    rows = []
    for r in cur.fetchall():
        item = dict(r)
        item["plan_json"] = json.loads(item["plan_json"])
        rows.append(item)
    conn.close()
    return rows