"""
Grounded question answering for The Unofficial Guide (Milestone 5).

This module connects the existing retrieval pipeline to Groq generation. It
does not rebuild embeddings, modify documents, or create a UI.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from retrieve import retrieve


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_NAME = "llama-3.3-70b-versatile"
DEFAULT_TOP_K = 4

SYSTEM_PROMPT = """
Answer using only the provided context. If the context does not contain enough
information, say: I don't have enough information in the provided documents to
answer that.

Rules:
- Do not use outside knowledge.
- Do not guess or fill gaps beyond the retrieved context.
- Cite every factual claim with source labels like [S1], [S2], or [S3].
- If the context is relevant but incomplete, say what is known and what is not
  covered by the provided documents.
""".strip()


def load_groq_client():
    """Load GROQ_API_KEY from .env and return a Groq client."""
    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")
    return Groq(api_key=api_key)


def build_context(retrieved_chunks):
    """Format retrieved chunks as source-labeled context blocks."""
    context_blocks = []
    for index, chunk in enumerate(retrieved_chunks, start=1):
        url = chunk.get("url") or "N/A"
        context_blocks.append(
            "\n".join(
                [
                    f"[S{index}]",
                    f"Title: {chunk.get('title')}",
                    f"Filename: {chunk.get('filename')}",
                    f"Chunk ID: {chunk.get('chunk_id')}",
                    f"URL: {url}",
                    f"Distance: {chunk.get('distance')}",
                    "Text:",
                    chunk.get("text", ""),
                ]
            )
        )
    return "\n\n".join(context_blocks)


def build_sources(retrieved_chunks):
    """Build source attribution from retrieved metadata, not LLM output."""
    sources = []
    for index, chunk in enumerate(retrieved_chunks, start=1):
        sources.append(
            {
                "source_label": f"S{index}",
                "filename": chunk.get("filename"),
                "title": chunk.get("title"),
                "chunk_id": chunk.get("chunk_id"),
                "url": chunk.get("url"),
                "distance": chunk.get("distance"),
            }
        )
    return sources


def generate_answer(query, top_k=DEFAULT_TOP_K):
    """Retrieve context, generate a grounded answer, and return structured data."""
    retrieved_chunks = retrieve(query, top_k=top_k)
    context = build_context(retrieved_chunks)
    client = load_groq_client()

    user_prompt = f"""
Question:
{query}

Retrieved context:
{context}

Write a concise, grounded answer. Use source labels from the retrieved context.
""".strip()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
        max_tokens=700,
    )

    answer = response.choices[0].message.content.strip()
    return {
        "answer": answer,
        "sources": build_sources(retrieved_chunks),
        "retrieved_chunks": retrieved_chunks,
    }


def run_test_queries():
    """Run a small command-line grounded-generation test."""
    test_queries = [
        "What courses are required for the UC Merced CSE major?",
        "Which CSE electives do students say are hardest or easiest?",
        "What is the best dining hall at UC Merced?",
    ]

    for query in test_queries:
        result = generate_answer(query)
        print("=" * 80)
        print(f"Question: {query}")
        print("-" * 80)
        print("Answer:")
        print(result["answer"])
        print("\nSources:")
        for source in result["sources"]:
            print(
                f"[{source['source_label']}] {source['filename']} | "
                f"{source['chunk_id']} | {source['title']} | "
                f"distance={source['distance']}"
            )
        print()


if __name__ == "__main__":
    run_test_queries()
