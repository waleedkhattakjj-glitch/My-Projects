import os
from google import genai
from google.genai import types
import time
from dotenv import load_dotenv

load_dotenv()  # Loads .env file

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

_client = None


def load_client():
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not set in environment / .env")
        print(f"Configuring Gemini client: {GEMINI_MODEL} ...")
        _client = genai.Client(api_key=GEMINI_API_KEY)
        print("Gemini client loaded.")
    return _client


def transcribe_chunk_gemini(chunk_path: str) -> str:
    client = load_client()
    
    # Upload audio file to Gemini using the File API
    uploaded_file = client.files.upload(file=chunk_path)
    
    # Wait for processing
    while uploaded_file.state.name == "PROCESSING":
        print("  → Processing audio with Gemini...")
        time.sleep(2)
        uploaded_file = client.files.get(name=uploaded_file.name)
    
    if uploaded_file.state.name == "FAILED":
        raise ValueError("Audio processing failed")
    
    prompt = "Please transcribe this audio accurately. Provide the transcription as plain text with proper punctuation."
    
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[prompt, uploaded_file]
    )
    
    # Clean up uploaded file
    try:
        client.files.delete(name=uploaded_file.name)
    except:
        pass
    
    return response.text


def transcribe_chunk(chunk_path: str) -> str:
    """
    Transcribe one chunk using Gemini.
    """
    return transcribe_chunk_gemini(chunk_path)


def transcribe_all(chunks: list) -> str:  # ✅ Removed language parameter
    full_transcript = "" 

    print(f"Using Gemini ({GEMINI_MODEL}) for transcription.")

    for i, chunk in enumerate(chunks):  
        print(f"Transcribing chunk {i + 1}/{len(chunks)}...")
        text = transcribe_chunk(chunk)  
        full_transcript += text + " "  

    print("Transcription complete.")
    return full_transcript.strip()