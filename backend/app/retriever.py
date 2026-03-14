import re
from collections import Counter
from typing import List, Dict


def normalize(text: str) -> List[str]:
    tokens = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
    stop_words = {
        "the", "is", "a", "an", "of", "to", "and", "in", "on", "for", "with",
        "that", "this", "it", "as", "by", "at", "from", "be", "are", "was", "were"
    }
    return [t for t in tokens if t not in stop_words]


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 100) -> List[str]:
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def score_chunk(query: str, chunk: str) -> int:
    q_tokens = Counter(normalize(query))
    c_tokens = Counter(normalize(chunk))
    return sum(min(q_tokens[t], c_tokens[t]) for t in q_tokens)


def retrieve_top_chunks(query: str, notes: List[Dict], top_k: int = 4) -> List[str]:
    scored = []

    for note in notes:
        content = note["content"]
        for chunk in chunk_text(content):
            score = score_chunk(query, chunk)
            if score > 0:
                scored.append((score, chunk, note["subject"], note.get("title", "Untitled")))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, chunk, subject, title in scored[:top_k]:
        results.append(f"[Subject: {subject} | Title: {title}]\n{chunk}")

    return results