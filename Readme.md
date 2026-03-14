# Smart Study Assistant Agent

An AI-powered study workspace built to experiment with **AI Agents, Retrieval-Augmented Generation (RAG), and knowledge automation**.

The idea behind this project was simple:

> What if a study assistant could automatically turn raw notes into summaries, flashcards, quizzes, and study plans?

Instead of building a simple chatbot, this project explores how an **AI Agent system can interact with stored knowledge and generate useful learning artifacts**.

---

# Why I Built This

Students usually do a lot of manual work while studying:

* writing notes
* summarizing them
* making flashcards
* creating practice quizzes
* planning what to study before exams

Most tools help with **only one of these tasks**.

I wanted to build something that acts more like an **intelligent study assistant** — something that understands notes and can automatically generate useful study materials from them.

At the same time, this project was also a way to experiment with:

* AI Agent architectures
* Retrieval-Augmented Generation (RAG)
* API-driven applications
* connecting AI models with real workflows

---

# What This AI Agent Can Do

This system acts as a **multi-capability study assistant agent**.

Once you add notes, the agent can generate several useful outputs.

---

## 1. Store and Manage Notes

Users can save notes with:

* subject
* title
* content

These notes become the **knowledge base** for the AI assistant.

Later, the agent retrieves information from these notes when generating answers or study material.

---

## 2. Generate AI Summaries

The assistant can transform long notes into:

* short summaries
* key concepts
* important takeaways
* quick revision points

This helps students quickly review large amounts of material.

---

## 3. Ask Questions from Notes (RAG)

Users can ask questions like:

> “Explain this concept from my notes.”

The system then:

1. searches the stored notes
2. retrieves relevant sections
3. sends them as context to the language model
4. generates a grounded answer

This approach is called **Retrieval-Augmented Generation (RAG)**.

It ensures answers are based on the user’s notes instead of the model guessing.

---

## 4. Generate Flashcards

The assistant can automatically create flashcards from notes.

Flashcards help with:

* quick revision
* active recall
* spaced repetition learning

Example:

Question
What is Retrieval-Augmented Generation?

Answer
A technique where relevant documents are retrieved and provided as context to a language model to generate grounded responses.

---

## 5. Generate Practice Quizzes

The system can also generate quizzes from notes.

These quizzes may include:

* multiple choice questions
* short answer questions
* answer keys

This helps students test their understanding.

---

## 6. Create Study Plans

The assistant can generate a structured study plan based on:

* exam date
* available study hours
* subjects
* weak topics

The AI produces a **day-by-day study schedule**.

---

# AI Agent Architecture

Instead of one big prompt, the system behaves like a **task-oriented AI agent**.

Each user request triggers a specific capability.

```
User Request
      │
      ▼
Study Assistant Agent
      │
      ├── Retrieval Module
      │       Finds relevant notes
      │
      ├── Knowledge Processing
      │       Understands study content
      │
      ├── Generation Module
      │       Summaries
      │       Flashcards
      │       Quizzes
      │
      └── Planning Module
              Study schedules
```

This design mirrors how modern **AI agent systems coordinate multiple capabilities**.

---

# Retrieval-Augmented Generation (RAG)

This project implements a **lightweight RAG pipeline**.

Workflow:

```
User Question
      ↓
Retrieve relevant note chunks
      ↓
Send context + question to LLM
      ↓
Generate answer grounded in notes
```

The retrieval system:

1. splits notes into chunks
2. scores chunks against the query
3. returns the most relevant sections

These chunks are then passed to the AI model as context.

Currently the system uses **keyword-based retrieval**, which is simple but effective.

A future improvement would be using **vector embeddings with a vector database**.

---

# System Architecture

The application follows a simple layered architecture.

```
Frontend (Dashboard UI)
        │
        ▼
FastAPI Backend (API Layer)
        │
        ├── AI Agent Layer
        │       Summary Agent
        │       Q&A Agent
        │       Flashcard Agent
        │       Quiz Agent
        │       Study Planner Agent
        │
        ├── Retrieval Layer
        │       Note chunking
        │       Relevance scoring
        │
        └── Data Layer
                SQLite database
```

---

# Folder Structure

```
smart-study-assistant
│
├── backend
│   │
│   ├── app
│   │   ├── main.py
│   │   ├── ai_service.py
│   │   ├── retriever.py
│   │   ├── schemas.py
│   │   └── db.py
│   │
│   ├── requirements.txt
│   └── study_assistant.db
│
├── frontend
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
└── README.md
```

---

# File Explanation

## backend/app/main.py

Main FastAPI application.

Responsibilities:

* define API endpoints
* handle requests
* call AI services
* interact with the database

---

## backend/app/ai_service.py

Contains the AI agent capabilities.

Functions include:

* note summarization
* question answering
* flashcard generation
* quiz generation
* study plan creation

---

## backend/app/retriever.py

Implements the retrieval system used in the RAG pipeline.

Steps include:

1. splitting notes into chunks
2. scoring chunks against a query
3. selecting the most relevant chunks

---

## backend/app/db.py

Handles database initialization and connections.

Stores:

* notes
* flashcards
* quizzes
* study plans

---

## backend/app/schemas.py

Defines structured request schemas using Pydantic.

This ensures API requests are validated before processing.

---

## frontend/index.html

Main user interface.

Provides controls for:

* creating notes
* generating summaries
* asking questions
* generating flashcards
* creating quizzes
* building study plans

---

## frontend/styles.css

Defines the visual layout and UI styling.

Includes:

* dashboard layout
* sidebar navigation
* responsive grid design

---

## frontend/app.js

Handles frontend logic.

Responsible for:

* sending API requests
* updating the dashboard
* displaying generated outputs

---

# How to Run the Project

## 1. Clone the repository

```
git clone https://github.com/yourusername/smart-study-assistant.git
cd smart-study-assistant
```

---

## 2. Create a virtual environment

```
python -m venv venv
```

Activate it.

Mac/Linux:

```
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

---

## 3. Install dependencies

```
cd backend
pip install -r requirements.txt
```

---

## 4. Add your API key

Create a `.env` file in the backend folder.

```
OPENAI_API_KEY=your_api_key_here
```

---

## 5. Start the backend

```
cd backend/app
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

API documentation is available at:

```
http://127.0.0.1:8000/docs
```

---

## 6. Run the frontend

Navigate to the frontend folder.

```
cd frontend
python -m http.server 3000
```

Open in your browser:

```
http://localhost:3000
```

---

# About the UI 😅

Yes… the UI could definitely be better.

If you're a designer, you might look at it and feel an uncontrollable urge to redesign everything in Figma — and honestly, that's fair.

But the main goal of this project wasn't to win a **frontend beauty contest**.

The focus was on experimenting with:

* AI agents
* retrieval systems
* connecting LLMs to real workflows

The UI just needed to be **functional enough to test the agent capabilities**.

Think of it more like a **control panel for the AI system** rather than a polished production interface.

If this were turned into a real product, the next steps would definitely include improving:

* UX flows
* interactive flashcards
* better quiz interfaces
* a more refined dashboard

But for now, the priority was making the **brains work, not the fashion.**

---

# Technologies Used

Backend

* Python
* FastAPI
* SQLite
* Pydantic

Frontend

* HTML
* CSS
* JavaScript

AI

* Large Language Models
* Retrieval-Augmented Generation (RAG)
* AI Agent architecture

---

# Future Improvements

Some ideas for extending this project:

* vector database retrieval
* embeddings-based search
* PDF / document upload
* multi-user authentication
* spaced repetition flashcards
* quiz scoring system
* adaptive study recommendations

---

# Final Thoughts

This project demonstrates how **AI agents can be integrated into practical applications** to automate knowledge workflows.

By combining:

* retrieval systems
* large language models
* structured APIs
* simple interfaces

we can build intelligent tools that help users learn more efficiently.
