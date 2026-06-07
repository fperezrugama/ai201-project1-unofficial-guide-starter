"""
Gradio interface for The Unofficial Guide (Milestone 5).

This app uses src/query.py for grounded generation. It does not modify or
rebuild the document, chunking, embedding, or retrieval pipeline.
"""

import sys
from pathlib import Path

import gradio as gr


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from query import generate_answer  # noqa: E402


EXAMPLE_QUESTIONS = [
    "What courses are required for the UC Merced CSE major?",
    "Which CSE electives do students say are hardest or easiest?",
    "What do students say about CSE 030 with Angelo Kyrilov?",
    "What is the best dining hall at UC Merced?",
]

APP_CSS = """
:root {
    --bobcat-navy: #002856;
    --bobcat-gold: #fdb515;
    --soft-gray: #f5f7fb;
    --ink: #172033;
}

.gradio-container {
    background: linear-gradient(180deg, #f7f9fd 0%, #ffffff 42%);
    color: var(--ink);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.app-shell {
    max-width: 1080px;
    margin: 0 auto;
}

.hero {
    border-left: 6px solid var(--bobcat-gold);
    background: #ffffff;
    border-radius: 8px;
    padding: 22px 24px;
    box-shadow: 0 12px 30px rgba(0, 40, 86, 0.08);
}

.hero h1 {
    color: var(--bobcat-navy);
    font-size: 32px;
    margin-bottom: 6px;
}

.hero p {
    color: #4a5568;
    font-size: 16px;
    margin: 0;
}

.source-box {
    background: var(--soft-gray);
    border: 1px solid #d9e2ef;
    border-radius: 8px;
    padding: 12px;
}

button.primary {
    background: var(--bobcat-navy) !important;
    border-color: var(--bobcat-navy) !important;
}
"""


def format_sources(sources):
    """Render retrieved source metadata for the UI."""
    if not sources:
        return "No sources available."

    lines = []
    for source in sources:
        distance = source.get("distance")
        distance_text = f"{distance:.4f}" if isinstance(distance, float) else "N/A"
        url = source.get("url") or "N/A"
        lines.append(
            "\n".join(
                [
                    f"**[{source.get('source_label')}] {source.get('title')}**",
                    f"- File: `{source.get('filename')}`",
                    f"- Chunk: `{source.get('chunk_id')}`",
                    f"- Distance: `{distance_text}`",
                    f"- URL: {url}",
                ]
            )
        )
    return "\n\n".join(lines)


def answer_question(question):
    """Handle UI requests and return answer text plus source metadata."""
    if not question or not question.strip():
        return "Please enter a question first.", "No sources retrieved."

    try:
        result = generate_answer(question.strip())
    except RuntimeError as error:
        message = str(error)
        if "GROQ_API_KEY" in message:
            return (
                "Missing Groq API key. Add `GROQ_API_KEY=...` to your `.env` file, then restart the app.",
                "No sources retrieved.",
            )
        return f"Runtime error: {message}", "No sources retrieved."
    except Exception as error:
        message = str(error)
        if "does not exist" in message.lower() or "collection" in message.lower():
            return (
                "The vector store could not be loaded. Run `.venv/bin/python src/vector_store.py`, then restart the app.",
                "No sources retrieved.",
            )
        return (
            f"Something went wrong while answering. Details: {message}",
            "No sources retrieved.",
        )

    return result["answer"], format_sources(result["sources"])


with gr.Blocks(title="UC Merced CSE Unofficial Guide") as demo:
    with gr.Column(elem_classes=["app-shell"]):
        gr.HTML(
            """
            <div class="hero">
                <h1>UC Merced CSE Unofficial Guide</h1>
                <p>Ask questions grounded in collected CSE documents, student discussions, course reviews, and professor summaries.</p>
            </div>
            """
        )

        question = gr.Textbox(
            label="Question",
            placeholder="Ask about CSE requirements, electives, professors, or student experiences...",
            lines=3,
        )
        ask_button = gr.Button("Ask", variant="primary")

        with gr.Row():
            answer = gr.Textbox(
                label="Grounded Answer",
                lines=12,
                buttons=["copy"],
                interactive=False,
            )
            sources = gr.Markdown(
                label="Sources",
                elem_classes=["source-box"],
            )

        gr.Examples(
            examples=EXAMPLE_QUESTIONS,
            inputs=question,
            label="Example questions",
        )

    ask_button.click(answer_question, inputs=question, outputs=[answer, sources])
    question.submit(answer_question, inputs=question, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch(css=APP_CSS)
