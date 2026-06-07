"""
Chunking for The Unofficial Guide (Milestone 3, Checkpoint 3).

Turns the documents produced by ingest.load_raw_documents() into retrieval
chunks, following the chunking strategy in planning.md:

  * Long official / course documents (the catalog, major requirements, program
    map, faculty page) are split into readable ~300-500 word chunks with about
    50-100 words of overlap, preferring paragraph boundaries over mechanical
    character cuts.

  * Shorter review-style documents (Rate My Professor, Coursicle, Reddit,
    Quora) preserve complete sections. These files are already organized into
    self-contained blocks (separated by dashed lines, or a single short post),
    so each block becomes one chunk. This keeps one professor/course/opinion
    per chunk and avoids mixing unrelated ones.

Each chunk carries the parsed metadata from ingestion (filename, title,
source_type, url, category) plus a unique chunk_id and a word_count.

This module does NOT embed, store, retrieve, or generate. It only chunks.
It does not modify ingest.py or the raw .txt files.
"""

import re

from ingest import load_raw_documents

# Chunking parameters (words), from the planning.md chunking strategy.
TARGET_WORDS = 400      # aim for chunks around here for long documents
MAX_WORDS = 500         # flush a long-document chunk once it reaches this size
OVERLAP_WORDS = 75      # carry this many trailing words into the next chunk
MIN_WORDS = 50          # don't emit mechanically-split chunks smaller than this

# A line made only of dashes (e.g. "----------") separates sections in the
# review-style files. Matched on its own line.
SECTION_SEPARATOR = re.compile(r"(?m)^[ \t]*-{3,}[ \t]*$")

# Header labels that ingest.py already captured as metadata. We strip these
# from the body so they are not repeated inside every chunk.
HEADER_LABELS = ("Title:", "Source Type:", "URL:", "Document Category:")


def is_long_official(metadata):
    """Long official/course documents are the cse_* files.

    Their source_type wording varies ("Official Catalog", "Program Map PDF",
    "Department Website"), so we classify on the filename prefix, which is
    consistent and reliable.
    """
    return metadata["filename"].startswith("cse_")


def extract_body(text):
    """Return the document body with the repeated header lines removed.

    Per the chunking requirements: when a "Content:" line exists, use only the
    text after it. Otherwise (the RMP / Reddit / Quora files), drop the labeled
    header lines (Title / Source Type / URL / Document Category) and keep the
    rest, so the body still contains useful content such as the professor name.
    """
    match = re.search(r"(?m)^Content:[ \t]*$", text)
    if match:
        return text[match.end():].strip()

    kept = [
        line
        for line in text.splitlines()
        if not line.strip().startswith(HEADER_LABELS)
    ]
    return "\n".join(kept).strip()


def split_paragraphs(text):
    """Split text into non-empty paragraphs on blank lines."""
    return [p.strip() for p in re.split(r"\n[ \t]*\n", text) if p.strip()]


def chunk_long_text(text):
    """Split a long document into ~300-500 word, paragraph-aligned chunks.

    Paragraphs are accumulated until the chunk reaches MAX_WORDS, then flushed.
    Each new chunk begins with the last OVERLAP_WORDS words of the previous one
    so context that spans a boundary (e.g. a prerequisite chain) is not lost.
    A small trailing chunk is merged back into the previous one so we never
    emit a sub-MIN_WORDS fragment from a mechanical split.
    """
    paragraphs = split_paragraphs(text)
    chunks = []
    current = []          # paragraphs accumulating into the current chunk
    current_words = 0

    for para in paragraphs:
        para_words = len(para.split())
        if current_words + para_words > MAX_WORDS and current_words >= MIN_WORDS:
            chunk_text = "\n\n".join(current)
            chunks.append(chunk_text)
            # Seed the next chunk with overlapping context.
            carry = " ".join(chunk_text.split()[-OVERLAP_WORDS:])
            current = [carry]
            current_words = len(carry.split())
        current.append(para)
        current_words += para_words

    if current:
        chunk_text = "\n\n".join(current)
        if chunks and len(chunk_text.split()) < MIN_WORDS:
            chunks[-1] = chunks[-1] + "\n\n" + chunk_text
        else:
            chunks.append(chunk_text)

    return chunks


def chunk_review_sections(text):
    """Split a review-style document into one chunk per complete section.

    Sections are delimited by dashed-line separators. Files with no separators
    (short Reddit / Quora posts) are kept whole as a single section. A section
    that is unusually long is further split with the long-document splitter so
    no single chunk becomes oversized.
    """
    sections = [s.strip() for s in SECTION_SEPARATOR.split(text) if s.strip()]
    if not sections:
        sections = [text.strip()] if text.strip() else []

    chunks = []
    for section in sections:
        if len(section.split()) > MAX_WORDS:
            chunks.extend(chunk_long_text(section))
        else:
            chunks.append(section)
    return [c for c in chunks if c.strip()]


def chunk_document(doc):
    """Chunk a single ingested document into a list of chunk dictionaries.

    Each chunk dict mirrors the ingestion shape:
        {
            "text": <chunk text>,
            "metadata": {
                "filename", "title", "source_type", "url", "category",  # carried
                "chunk_id",     # unique across the whole corpus
                "word_count",
            },
        }
    """
    body = extract_body(doc["text"])
    metadata = doc["metadata"]

    if is_long_official(metadata):
        pieces = chunk_long_text(body)
    else:
        pieces = chunk_review_sections(body)

    stem = metadata["filename"].rsplit(".", 1)[0]
    chunks = []
    for i, piece in enumerate(pieces):
        if not piece.strip():
            continue
        chunk_metadata = {
            "filename": metadata.get("filename"),
            "title": metadata.get("title"),
            "source_type": metadata.get("source_type"),
            "url": metadata.get("url"),
            "category": metadata.get("category"),
            "chunk_id": f"{stem}-{i:03d}",
            "word_count": len(piece.split()),
        }
        chunks.append({"text": piece, "metadata": chunk_metadata})

    return chunks


def chunk_documents(documents):
    """Chunk every ingested document into one flat list of chunks."""
    chunks = []
    for doc in documents:
        chunks.extend(chunk_document(doc))
    return chunks


if __name__ == "__main__":
    documents = load_raw_documents()
    chunks = chunk_documents(documents)

    print(f"Total documents loaded: {len(documents)}")
    print(f"Total chunks created:   {len(chunks)}\n")

    # Show 5 sample chunks spread across the corpus so different source types
    # and documents are represented.
    print("Sample chunks")
    print("=" * 70)
    if chunks:
        step = max(1, len(chunks) // 5)
        sample_indices = list(range(0, len(chunks), step))[:5]
        for idx in sample_indices:
            chunk = chunks[idx]
            meta = chunk["metadata"]
            print(f"chunk_id:   {meta['chunk_id']}")
            print(f"filename:   {meta['filename']}")
            print(f"title:      {meta['title']}")
            print(f"word_count: {meta['word_count']}")
            preview = chunk["text"][:200].replace("\n", " ")
            print(f"preview:    {preview}...")
            print("-" * 70)
