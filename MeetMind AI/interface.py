"""
Streamlit interface for the AI meeting/video assistant.

Place this file in the same folder as main.py, audio/, and components/.
Run with:
    streamlit run interface.py
"""

import os
import re
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from main import run_pipeline
from components.rag_engine import ask_question


# -----------------------------
# App setup
# -----------------------------
load_dotenv()

UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="MeetMind AI",
    page_icon="🎙️",
    layout="wide",
)


# -----------------------------
# Helper functions
# -----------------------------
def safe_filename(filename: str) -> str:
    """Remove unsafe characters from uploaded filenames."""
    filename = filename.strip().replace(" ", "_")
    return re.sub(r"[^A-Za-z0-9_.-]", "_", filename)


def save_uploaded_file(uploaded_file) -> str:
    """Save Streamlit uploaded file and return local path."""
    file_path = UPLOAD_DIR / safe_filename(uploaded_file.name)
    file_path.write_bytes(uploaded_file.getbuffer())
    return str(file_path)


def make_markdown_report(result: dict) -> str:
    """Create a downloadable Markdown meeting report."""
    return f"""# {result.get('title', 'Meeting Report')}

## Summary
{result.get('summary', '')}

## Action Items
{result.get('action_items', '')}

## Key Decisions
{result.get('key_decisions', '')}

## Open Questions
{result.get('open_questions', '')}

## Transcript
{result.get('transcript', '')}
"""


def reset_app_state():
    """Clear current meeting results and chat messages."""
    for key in ["result", "source", "chat_messages"]:
        if key in st.session_state:
            del st.session_state[key]


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("🎙️ MeetMind AI")
    st.caption("Transcribe, summarize, extract insights, and chat with your meeting/video.")

    st.divider()

    input_type = st.radio(
        "Choose input type",
        options=["YouTube URL", "Upload audio/video file"],
    )

    source = None

    if input_type == "YouTube URL":
        youtube_url = st.text_input(
            "YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
        )
        if youtube_url.strip():
            source = youtube_url.strip()
    else:
        uploaded_file = st.file_uploader(
            "Upload audio/video",
            type=["mp3", "wav", "m4a", "aac", "ogg", "flac", "mp4", "mov", "mkv", "webm"],
        )
        if uploaded_file is not None:
            source = save_uploaded_file(uploaded_file)
            st.success(f"Uploaded: {uploaded_file.name}")

    language = st.selectbox(
        "Language",
        options=["english", "hinglish", "urdu", "hindi"],
        index=0,
        help="Your current pipeline accepts this argument, but transcription language is handled by Gemini automatically unless you add language-specific prompting.",
    )

    st.divider()

    run_button = st.button(
        "🚀 Process Meeting/Video",
        type="primary",
        use_container_width=True,
        disabled=not bool(source),
    )

    if st.button("🔄 Reset", use_container_width=True):
        reset_app_state()
        st.rerun()

    st.divider()

    if not os.getenv("GEMINI_API_KEY"):
        st.warning("GEMINI_API_KEY is not found. Add it to your .env file before processing.")

    st.info(
        "Make sure FFmpeg is installed for audio conversion and YouTube audio extraction."
    )


# -----------------------------
# Main page header
# -----------------------------
st.title("🎙️ MeetMind AI")
st.subheader("AI Meeting & Video Intelligence Assistant")
st.write(
    "Upload a meeting/video or paste a YouTube URL. The app will transcribe it, generate a summary, "
    "extract action items, decisions, open questions, and let you chat with the transcript."
)


# -----------------------------
# Run pipeline
# -----------------------------
if run_button:
    st.session_state["source"] = source
    st.session_state["chat_messages"] = []

    try:
        with st.status("Processing your meeting/video...", expanded=True) as status:
            st.write("1. Downloading/converting audio...")
            st.write("2. Chunking audio...")
            st.write("3. Transcribing with Gemini...")
            st.write("4. Generating summary and insights...")
            st.write("5. Building RAG chat engine...")

            result = run_pipeline(source, language)
            st.session_state["result"] = result

            status.update(label="Processing complete!", state="complete", expanded=False)

        st.success("Done! Your results are ready below.")

    except Exception as e:
        st.error("Something went wrong while processing.")
        st.exception(e)


# -----------------------------
# Display results
# -----------------------------
result = st.session_state.get("result")

if not result:
    st.info("Choose an input from the sidebar and click **Process Meeting/Video** to start.")
    st.stop()

st.divider()

meeting_title = result.get("title", "Untitled Meeting").strip()
st.header(f"📌 {meeting_title}")

report_md = make_markdown_report(result)

col1, col2, col3 = st.columns(3)
with col1:
    st.download_button(
        "⬇️ Download Full Report (.md)",
        data=report_md,
        file_name=f"{safe_filename(meeting_title) or 'meeting_report'}.md",
        mime="text/markdown",
        use_container_width=True,
    )
with col2:
    st.download_button(
        "⬇️ Download Transcript (.txt)",
        data=result.get("transcript", ""),
        file_name=f"{safe_filename(meeting_title) or 'transcript'}_transcript.txt",
        mime="text/plain",
        use_container_width=True,
    )
with col3:
    st.write("")
    st.write("")
    st.caption("Use the tabs below to view extracted meeting intelligence.")

summary_tab, actions_tab, decisions_tab, questions_tab, transcript_tab, chat_tab = st.tabs(
    [
        "📋 Summary",
        "✅ Action Items",
        "🔑 Key Decisions",
        "❓ Open Questions",
        "📝 Transcript",
        "💬 Chat",
    ]
)

with summary_tab:
    st.markdown(result.get("summary", "No summary generated."))

with actions_tab:
    st.markdown(result.get("action_items", "No action items found."))

with decisions_tab:
    st.markdown(result.get("key_decisions", "No key decisions found."))

with questions_tab:
    st.markdown(result.get("open_questions", "No open questions found."))

with transcript_tab:
    st.text_area(
        "Full transcript",
        value=result.get("transcript", ""),
        height=500,
    )

with chat_tab:
    st.subheader("Chat with your meeting")
    st.caption("Ask questions based only on the transcript context.")

    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []

    for message in st.session_state["chat_messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question about the meeting...")

    if question:
        st.session_state["chat_messages"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching transcript and generating answer..."):
                try:
                    answer = ask_question(result["rag_chain"], question)
                except Exception as e:
                    answer = f"Sorry, I could not answer this question. Error: {e}"

            st.markdown(answer)

        st.session_state["chat_messages"].append({"role": "assistant", "content": answer})
