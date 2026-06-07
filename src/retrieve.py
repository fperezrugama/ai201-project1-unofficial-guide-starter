"""
Retrieval for The Unofficial Guide (Milestone 4).

Loads the existing ChromaDB collection built by vector_store.py, embeds a user
query with the same sentence-transformers model, and returns the nearest stored
chunks. This module does not rebuild the vector store or generate answers.
"""

from pathlib import Path
import re

import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_PATH = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "uc_merced_cse_chunks"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = 4
COURSE_CODE_PATTERN = re.compile(r"\b[A-Z]{2,4}\s*\d{3}\b", re.IGNORECASE)
COMMON_TITLE_WORDS = {
    "course",
    "courses",
    "engineering",
    "information",
    "major",
    "merced",
    "my",
    "professor",
    "rate",
    "reviews",
    "the",
    "uc",
}


def load_embedding_model():
    """Load the same local embedding model used during indexing."""
    return SentenceTransformer(EMBEDDING_MODEL_NAME, local_files_only=True)


def get_collection():
    """Load the existing persistent ChromaDB collection from chroma_db/.

    PersistentClient points at the on-disk database created by vector_store.py.
    get_collection opens that existing collection without recreating or
    inserting any chunks.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return client.get_collection(name=COLLECTION_NAME)


def extract_course_codes(text):
    """Return normalized course codes such as CSE 022 from text."""
    codes = set()
    for match in COURSE_CODE_PATTERN.finditer(text):
        code = re.sub(r"\s+", " ", match.group(0).upper()).strip()
        codes.add(code)
    return codes


def extract_words(text):
    """Return lowercase alphanumeric words for simple exact-match reranking."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def rerank_bonus(query, document, metadata):
    """Boost exact course-code and professor/title matches after vector search."""
    bonus = 0.0
    query_codes = extract_course_codes(query)
    document_codes = extract_course_codes(document)
    metadata_text = " ".join(str(value) for value in metadata.values())
    all_candidate_codes = extract_course_codes(f"{document}\n{metadata_text}")

    first_line = next(
        (line.strip() for line in document.splitlines() if line.strip()),
        "",
    )
    first_line_codes = extract_course_codes(first_line)

    for code in query_codes:
        if code in all_candidate_codes:
            bonus += 0.15
        if code in document_codes:
            bonus += 0.10
        if code in first_line_codes:
            bonus += 0.35

    query_words = extract_words(query)
    title = metadata.get("title", "")
    if title.lower().startswith("rate my professor - "):
        professor_name = title.split(" - ", 1)[1]
        title_words = {
            word
            for word in extract_words(professor_name)
            if len(word) > 2 and word not in COMMON_TITLE_WORDS
        }
        if len(query_words.intersection(title_words)) >= 2:
            bonus += 0.15

    return bonus


def retrieve(query, top_k=DEFAULT_TOP_K):
    """Return the top-k most relevant stored chunks for a query string."""
    model = load_embedding_model()
    collection = get_collection()

    query_embedding = model.encode(query).tolist()
    candidate_count = min(collection.count(), max(top_k, collection.count()))

    # collection.query compares the query embedding against stored chunk
    # embeddings and returns the nearest documents plus metadata and distances.
    # This small corpus lets us pull all candidates, then rerank exact
    # professor/course-code matches while keeping the original cosine distance.
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=candidate_count,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    ids = results["ids"][0]

    retrieved_chunks = []
    for index, document in enumerate(documents):
        metadata = metadatas[index] or {}
        retrieved_chunks.append(
            {
                "distance": distances[index],
                "text": document,
                "filename": metadata.get("filename"),
                "title": metadata.get("title"),
                "chunk_id": metadata.get("chunk_id", ids[index]),
                "url": metadata.get("url"),
                "_rerank_score": distances[index]
                - rerank_bonus(query, document, metadata),
            }
        )

    retrieved_chunks.sort(key=lambda chunk: (chunk["_rerank_score"], chunk["distance"]))
    top_chunks = retrieved_chunks[:top_k]
    for index, chunk in enumerate(top_chunks):
        chunk["rank"] = index + 1
        del chunk["_rerank_score"]

    return top_chunks


def run_test_queries():
    """Run simple retrieval-only command-line tests."""
    test_queries = [
        "What courses are required for the UC Merced CSE major?",
        "Which CSE electives do students say are hardest or easiest?",
        "What do students say about Professor Angelo Kyrilov's programming courses?",
        "What do students say about CSE 022 with Angelo Kyrilov?",
        "What do students say about CSE 024 with Angelo Kyrilov?",
        "What do students say about CSE 030 with Angelo Kyrilov?",
    ]

    for query in test_queries:
        print("=" * 80)
        print(f"Query: {query}")
        print("=" * 80)

        for result in retrieve(query, top_k=DEFAULT_TOP_K):
            preview = result["text"][:400].replace("\n", " ")
            print(f"Rank:           {result['rank']}")
            print(f"Distance score: {result['distance']}")
            print(f"Filename:       {result['filename']}")
            print(f"Chunk ID:       {result['chunk_id']}")
            print(f"Title:          {result['title']}")
            print(f"Preview:        {preview}")
            print("-" * 80)


if __name__ == "__main__":
    run_test_queries()
