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
    --navy-soft: #e9f0f8;
    --soft-gray: #f5f7fb;
    --card-bg: #ffffff;
    --field-bg: #ffffff;
    --panel-border: #dbe4f0;
    --ink: #172033;
    --muted: #5f6b7a;
    --placeholder: #728196;
}

.gradio-container {
    background:
        radial-gradient(circle at top left, rgba(0, 40, 86, 0.10), transparent 32%),
        linear-gradient(180deg, #eef4fb 0%, #f8fafc 42%, #ffffff 100%);
    color: var(--ink);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.app-shell {
    max-width: 1080px;
    margin: 0 auto;
    padding: 22px 14px 34px;
}

.hero {
    position: relative;
    background: var(--card-bg);
    color: var(--ink);
    border-radius: 8px;
    padding: 28px 30px 24px;
    border: 1px solid var(--panel-border);
    box-shadow: 0 14px 36px rgba(0, 40, 86, 0.10);
    overflow: hidden;
}

.hero::before {
    content: "";
    position: absolute;
    inset: 0 auto 0 0;
    width: 7px;
    background: linear-gradient(180deg, var(--bobcat-gold), #ffd76a);
}

.hero::after {
    content: "";
    position: absolute;
    top: 18px;
    right: 22px;
    width: 54px;
    height: 5px;
    border-radius: 999px;
    background: var(--bobcat-gold);
    opacity: 0.85;
}

.hero h1 {
    color: var(--bobcat-navy);
    font-size: 38px;
    line-height: 1.08;
    margin: 0 0 8px;
    font-weight: 800;
}

.hero .tagline {
    color: var(--bobcat-navy);
    font-size: 15px;
    font-weight: 700;
    margin: 0 0 8px;
    letter-spacing: 0.02em;
}

.hero p {
    color: var(--muted);
    font-size: 16px;
    line-height: 1.55;
    margin: 0;
}

.panel-card {
    background: var(--card-bg) !important;
    color: var(--ink) !important;
    border: 1px solid var(--panel-border);
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 10px 24px rgba(0, 40, 86, 0.08);
}

.panel-card label,
.panel-card .label-wrap,
.question-card label,
.question-card .label-wrap {
    color: var(--bobcat-navy) !important;
    font-weight: 750 !important;
}

.question-card textarea,
.question-card input,
.answer-card textarea,
.answer-card input {
    background: var(--field-bg) !important;
    color: var(--ink) !important;
    border-color: var(--panel-border) !important;
    caret-color: var(--bobcat-navy) !important;
}

.answer-card textarea,
.answer-card input {
    line-height: 1.6 !important;
}

.question-card textarea::placeholder,
.question-card input::placeholder {
    color: var(--placeholder) !important;
    opacity: 1 !important;
}

.source-box {
    background: var(--card-bg) !important;
    color: var(--ink) !important;
}

.source-box h1,
.source-box h2,
.source-box h3,
.source-box h4,
.source-box label,
.source-box .label-wrap {
    color: var(--bobcat-navy) !important;
}

.source-box p,
.source-box li {
    color: var(--muted) !important;
    line-height: 1.5 !important;
}

.source-box strong {
    color: var(--bobcat-navy) !important;
}

.source-box ul {
    background: var(--soft-gray);
    border: 1px solid #e2e8f2;
    border-radius: 8px;
    padding: 10px 14px 10px 28px;
    margin: 8px 0 14px;
}

.source-box code {
    background: #edf2f7;
    color: var(--bobcat-navy) !important;
    border-radius: 4px;
    padding: 2px 5px;
}

.dark .hero,
.dark .panel-card,
.dark .source-box,
[data-theme="dark"] .hero,
[data-theme="dark"] .panel-card,
[data-theme="dark"] .source-box {
    background: #f8fafc !important;
    color: var(--ink) !important;
    border-color: #cbd7e6 !important;
}

.dark .question-card textarea,
.dark .question-card input,
.dark .answer-card textarea,
.dark .answer-card input,
[data-theme="dark"] .question-card textarea,
[data-theme="dark"] .question-card input,
[data-theme="dark"] .answer-card textarea,
[data-theme="dark"] .answer-card input {
    background: #ffffff !important;
    color: var(--ink) !important;
    border-color: #cbd7e6 !important;
}

.dark .source-box p,
.dark .source-box li,
[data-theme="dark"] .source-box p,
[data-theme="dark"] .source-box li {
    color: #4b5a6d !important;
}

.dark .source-box strong,
.dark .source-box label,
.dark .source-box .label-wrap,
.dark .panel-card label,
.dark .panel-card .label-wrap,
.dark .question-card label,
.dark .question-card .label-wrap,
[data-theme="dark"] .source-box strong,
[data-theme="dark"] .source-box label,
[data-theme="dark"] .source-box .label-wrap,
[data-theme="dark"] .panel-card label,
[data-theme="dark"] .panel-card .label-wrap,
[data-theme="dark"] .question-card label,
[data-theme="dark"] .question-card .label-wrap {
    color: var(--bobcat-navy) !important;
}

textarea,
input {
    border-radius: 8px !important;
}

.form label {
    color: var(--bobcat-navy) !important;
    font-weight: 750 !important;
}

button.primary {
    background: var(--bobcat-navy) !important;
    border-color: var(--bobcat-navy) !important;
    border-radius: 8px !important;
    font-weight: 750 !important;
    min-height: 44px;
    box-shadow: 0 8px 18px rgba(0, 40, 86, 0.18);
}

button.primary:hover {
    filter: brightness(1.08);
}

.examples {
    border-radius: 8px !important;
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
                <p class="tagline">Course Planning &bull; Professor Insights &bull; Student Experiences</p>
                <p>Ask questions grounded in collected CSE documents, student discussions, course reviews, and professor summaries.</p>
            </div>
            """
        )

        question = gr.Textbox(
            label="Ask a Question",
            placeholder="Ask about CSE requirements, electives, professors, or student experiences...",
            lines=3,
            elem_classes=["question-card"],
        )
        ask_button = gr.Button("Ask", variant="primary")

        with gr.Row():
            answer = gr.Textbox(
                label="Grounded Answer",
                lines=12,
                buttons=["copy"],
                interactive=False,
                elem_classes=["panel-card", "answer-card"],
            )
            sources = gr.Markdown(
                label="Retrieved Sources",
                elem_classes=["panel-card", "source-box"],
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
