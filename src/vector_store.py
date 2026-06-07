"""
Vector store indexing for The Unofficial Guide (Milestone 4).

Loads chunks from the existing Milestone 3 pipeline, embeds each chunk with
sentence-transformers/all-MiniLM-L6-v2, and stores the chunk text, embedding,
and metadata in a local persistent ChromaDB collection.

This module only builds the vector index. It does not retrieve, generate
answers, call Groq, or modify the raw documents / ingestion / chunking code.
"""

from pathlib import Path
import re

import chromadb
from sentence_transformers import SentenceTransformer

from chunk import chunk_documents
from ingest import load_raw_documents


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_PATH = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "uc_merced_cse_chunks"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_METADATA = {"hnsw:space": "cosine"}
COURSE_HEADING = re.compile(r"^\s*(CSE\s+\d{3}\s*:[^\n]+)", re.IGNORECASE)


def load_chunks():
    """Load raw documents and chunk them using the existing chunk.py pipeline."""
    documents = load_raw_documents()
    return chunk_documents(documents)


def load_embedding_model():
    """Load the local sentence-transformers embedding model."""
    return SentenceTransformer(EMBEDDING_MODEL_NAME, local_files_only=True)


def get_chroma_client():
    """Create a persistent ChromaDB client stored under chroma_db/.

    PersistentClient writes the collection data to disk automatically at the
    configured path, so the index can be reused by later retrieval code.
    """
    return chromadb.PersistentClient(path=str(CHROMA_PATH))


def reset_collection(client):
    """Delete and recreate the Chroma collection so reruns avoid duplicates."""
    existing_collections = client.list_collections()
    existing_names = [
        collection if isinstance(collection, str) else collection.name
        for collection in existing_collections
    ]

    if COLLECTION_NAME in existing_names:
        client.delete_collection(name=COLLECTION_NAME)

    # create_collection starts a fresh empty collection for this indexing run.
    # hnsw:space="cosine" tells Chroma to rank MiniLM embeddings by cosine
    # distance instead of the default distance metric.
    return client.create_collection(
        name=COLLECTION_NAME,
        metadata=COLLECTION_METADATA,
    )


def build_embedding_text(chunk):
    """Add metadata context to the text used only for embeddings."""
    metadata = chunk["metadata"]
    course_match = COURSE_HEADING.search(chunk["text"])
    course_context = course_match.group(1) if course_match else ""
    metadata_lines = [
        f"Title: {metadata.get('title', '')}",
        f"Source: {metadata.get('filename', '')}",
        f"Source Type: {metadata.get('source_type', '')}",
        f"Category: {metadata.get('category', '')}",
        f"Chunk ID: {metadata.get('chunk_id', '')}",
    ]

    if course_context:
        metadata_lines.append(f"Course: {course_context}")

    return "\n".join(metadata_lines + ["", chunk["text"]])


def build_vector_store():
    """Embed all chunks and store text, embeddings, and metadata in ChromaDB."""
    chunks = load_chunks()
    model = load_embedding_model()
    client = get_chroma_client()
    collection = reset_collection(client)

    texts = [chunk["text"] for chunk in chunks]
    embedding_texts = [build_embedding_text(chunk) for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    ids = [metadata["chunk_id"] for metadata in metadatas]

    embeddings = model.encode(embedding_texts, show_progress_bar=True).tolist()
    embedding_dimension = len(embeddings[0]) if embeddings else 0

    # collection.add inserts each chunk into ChromaDB. We store:
    # - ids: stable chunk IDs from chunk.py
    # - documents: original chunk text
    # - embeddings: MiniLM vectors used for semantic search
    # - metadatas: filename/title/source/url/category/chunk_id/word_count
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Total chunks loaded:      {len(chunks)}")
    print(f"Embedding model name:     {EMBEDDING_MODEL_NAME}")
    print(f"Embedding dimension:      {embedding_dimension}")
    print(f"ChromaDB persist path:    {CHROMA_PATH}")
    print(f"Collection name:          {COLLECTION_NAME}")
    print(f"Collection metadata:      {collection.metadata}")
    print(f"Total documents stored:   {collection.count()}")

    return collection


if __name__ == "__main__":
    build_vector_store()
