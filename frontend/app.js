const API_BASE = "http://127.0.0.1:8000";

async function request(path, method = "GET", body = null) {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json"
    }
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const res = await fetch(`${API_BASE}${path}`, options);
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Request failed");
  }

  return data;
}

function pretty(obj) {
  return JSON.stringify(obj, null, 2);
}

function show(elId, value) {
  document.getElementById(elId).textContent =
    typeof value === "string" ? value : pretty(value);
}

async function loadDashboard() {
  try {
    const data = await request("/dashboard");
    document.getElementById("statNotes").textContent = data.notes_count ?? 0;
    document.getElementById("statFlashcards").textContent = data.flashcards_count ?? 0;
    document.getElementById("statQuizzes").textContent = data.quizzes_count ?? 0;
    document.getElementById("statPlans").textContent = data.study_plans_count ?? 0;
  } catch (err) {
    console.error(err);
  }
}

async function createNote() {
  try {
    const payload = {
      subject: document.getElementById("subject").value.trim(),
      title: document.getElementById("title").value.trim() || "Untitled Note",
      content: document.getElementById("content").value.trim()
    };

    const data = await request("/notes", "POST", payload);
    show("noteOutput", data);
    loadDashboard();
  } catch (err) {
    show("noteOutput", err.message);
  }
}

async function loadNotes() {
  try {
    const data = await request("/notes");
    show("notesOutput", data);
  } catch (err) {
    show("notesOutput", err.message);
  }
}

async function summarizeNote() {
  try {
    const payload = {
      note_id: Number(document.getElementById("summaryNoteId").value)
    };

    const data = await request("/summarize", "POST", payload);
    show("summaryOutput", data.summary);
  } catch (err) {
    show("summaryOutput", err.message);
  }
}

async function askQuestion() {
  try {
    const payload = {
      question: document.getElementById("question").value.trim(),
      subject: document.getElementById("askSubject").value.trim() || null
    };

    const data = await request("/ask", "POST", payload);
    show("askOutput", data);
  } catch (err) {
    show("askOutput", err.message);
  }
}

async function generateFlashcards() {
  try {
    const payload = {
      note_id: Number(document.getElementById("flashcardNoteId").value),
      count: Number(document.getElementById("flashcardCount").value)
    };

    const data = await request("/flashcards/generate", "POST", payload);
    show("flashcardOutput", data.flashcards);
    loadDashboard();
  } catch (err) {
    show("flashcardOutput", err.message);
  }
}

async function generateQuiz() {
  try {
    const payload = {
      note_id: Number(document.getElementById("quizNoteId").value),
      difficulty: document.getElementById("quizDifficulty").value.trim() || "medium",
      count: Number(document.getElementById("quizCount").value)
    };

    const data = await request("/quiz/generate", "POST", payload);
    show("quizOutput", data.quiz);
    loadDashboard();
  } catch (err) {
    show("quizOutput", err.message);
  }
}

async function createStudyPlan() {
  try {
    const payload = {
      exam_date: document.getElementById("examDate").value.trim(),
      hours_per_day: Number(document.getElementById("hoursPerDay").value),
      subjects: document.getElementById("subjectsPlan").value
        .split(",")
        .map(x => x.trim())
        .filter(Boolean),
      weak_topics: document.getElementById("weakTopics").value
        .split(",")
        .map(x => x.trim())
        .filter(Boolean)
    };

    const data = await request("/study-plan", "POST", payload);
    show("planOutput", data.plan);
    loadDashboard();
  } catch (err) {
    show("planOutput", err.message);
  }
}

loadDashboard();