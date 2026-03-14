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

async function loadDashboard() {
  try {
    const data = await request("/dashboard");
    document.getElementById("dashboardOutput").textContent = pretty(data);
  } catch (err) {
    document.getElementById("dashboardOutput").textContent = err.message;
  }
}

async function createNote() {
  try {
    const payload = {
      subject: document.getElementById("subject").value,
      title: document.getElementById("title").value || "Untitled Note",
      content: document.getElementById("content").value
    };
    const data = await request("/notes", "POST", payload);
    document.getElementById("noteOutput").textContent = pretty(data);
  } catch (err) {
    document.getElementById("noteOutput").textContent = err.message;
  }
}

async function loadNotes() {
  try {
    const data = await request("/notes");
    document.getElementById("notesOutput").textContent = pretty(data);
  } catch (err) {
    document.getElementById("notesOutput").textContent = err.message;
  }
}

async function summarizeNote() {
  try {
    const payload = {
      note_id: Number(document.getElementById("summaryNoteId").value)
    };
    const data = await request("/summarize", "POST", payload);
    document.getElementById("summaryOutput").textContent = data.summary;
  } catch (err) {
    document.getElementById("summaryOutput").textContent = err.message;
  }
}

async function askQuestion() {
  try {
    const payload = {
      question: document.getElementById("question").value,
      subject: document.getElementById("askSubject").value || null
    };
    const data = await request("/ask", "POST", payload);
    document.getElementById("askOutput").textContent = pretty(data);
  } catch (err) {
    document.getElementById("askOutput").textContent = err.message;
  }
}

async function generateFlashcards() {
  try {
    const payload = {
      note_id: Number(document.getElementById("flashcardNoteId").value),
      count: Number(document.getElementById("flashcardCount").value)
    };
    const data = await request("/flashcards/generate", "POST", payload);
    document.getElementById("flashcardOutput").textContent = pretty(data.flashcards);
  } catch (err) {
    document.getElementById("flashcardOutput").textContent = err.message;
  }
}

async function generateQuiz() {
  try {
    const payload = {
      note_id: Number(document.getElementById("quizNoteId").value),
      difficulty: document.getElementById("quizDifficulty").value,
      count: Number(document.getElementById("quizCount").value)
    };
    const data = await request("/quiz/generate", "POST", payload);
    document.getElementById("quizOutput").textContent = pretty(data.quiz);
  } catch (err) {
    document.getElementById("quizOutput").textContent = err.message;
  }
}

async function createStudyPlan() {
  try {
    const payload = {
      exam_date: document.getElementById("examDate").value,
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
    document.getElementById("planOutput").textContent = pretty(data.plan);
  } catch (err) {
    document.getElementById("planOutput").textContent = err.message;
  }
}

loadDashboard();