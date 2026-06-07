"""
Document ingestion for The Unofficial Guide (Milestone 3, Checkpoint 1).

Loads every .txt file from documents/raw/, reads its full text, and extracts
the labeled metadata header (Title, Source Type, URL, Document Category) that
each raw document begins with. Returns a list of document dictionaries shaped
as { "text": <full file text>, "metadata": {...} } so later stages (chunking,
embedding) can carry source attribution along with each chunk.

This module does NOT chunk. It stops at "clean documents with metadata."
"""

import re
from pathlib import Path

# Default location of the raw corpus, relative to the project root.
RAW_DIR = Path(__file__).resolve().parent.parent / "documents" / "raw"

# Metadata labels we look for at the top of each file. The key is the label as
# it appears in the file; the value is the metadata dictionary key we store it under.
METADATA_LABELS = {
    "Title": "title",
    "Source Type": "source_type",
    "URL": "url",
    "Document Category": "category",
}


def extract_metadata(text, filename):
    """Pull the labeled header fields from the top of a raw document.

    Each raw file begins with lines like:
        Title: ...
        Source Type: ...
        URL: ...
        Document Category: ...

    We scan for those labels at the start of a line. Any field that is missing
    is simply left out (the caller can decide how to handle gaps). The source
    filename is always recorded so every chunk can be traced back to its file.
    """
    metadata = {"filename": filename}

    for label, key in METADATA_LABELS.items():
        # Match "Label: value" at the beginning of a line, capturing the rest
        # of that line as the value. re.MULTILINE makes ^ match line starts.
        match = re.search(rf"^{re.escape(label)}:\s*(.+)$", text, re.MULTILINE)
        if match:
            metadata[key] = match.group(1).strip()

    return metadata


def load_raw_documents(raw_dir=RAW_DIR):
    """Load every .txt file in raw_dir into a list of document dictionaries.

    Returns a list of:
        {
            "text": <full text of the file>,
            "metadata": {
                "filename": ...,
                "title": ...,        # when present
                "source_type": ...,  # when present
                "url": ...,          # when present
                "category": ...,     # when present
            },
        }

    Files are processed in sorted filename order so runs are reproducible.
    """
    raw_dir = Path(raw_dir)
    documents = []

    for path in sorted(raw_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        metadata = extract_metadata(text, filename=path.name)
        documents.append({"text": text, "metadata": metadata})

    return documents


if __name__ == "__main__":
    docs = load_raw_documents()

    print(f"Total documents loaded: {len(docs)}\n")

    print("Filename -> Title")
    print("-" * 60)
    for doc in docs:
        meta = doc["metadata"]
        title = meta.get("title", "(no title found)")
        print(f"{meta['filename']:<35} {title}")

    if docs:
        first = docs[0]
        print("\n" + "-" * 60)
        print(f"First 300 characters of: {first['metadata']['filename']}")
        print("-" * 60)
        print(first["text"][:300])
