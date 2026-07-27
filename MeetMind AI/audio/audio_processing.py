import os
import re
import uuid
from pathlib import Path

import yt_dlp
from pydub import AudioSegment


DOWNLOAD_DIR = Path("downloades")
DOWNLOAD_DIR.mkdir(exist_ok=True)


def safe_name(text: str) -> str:
    """
    Make filename ASCII-safe for Windows, Gemini upload, and HTTP headers.
    """
    text = text.strip().replace(" ", "_")
    text = re.sub(r"[^A-Za-z0-9_.-]", "_", text)
    return text or "audio"


def download_youtube_audio(url: str) -> str:
    """
    Download YouTube audio as WAV.

    Important:
    We use video ID instead of title because some YouTube titles contain
    Unicode characters like '？', which can break Gemini file upload.
    """
    output_path = str(DOWNLOAD_DIR / "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,

        # These make filenames safer on Windows
        "restrictfilenames": True,
        "windowsfilenames": True,

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],

        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # prepare_filename returns the original downloaded extension like .webm/.m4a
        original_filename = ydl.prepare_filename(info)

        # After FFmpegExtractAudio, final file becomes .wav
        filename = os.path.splitext(original_filename)[0] + ".wav"

    return filename


def convert_to_wav(input_path: str) -> str:
    """
    Convert any audio/video file to WAV format using pydub.

    The output filename is made ASCII-safe to avoid Gemini upload errors.
    """
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path = DOWNLOAD_DIR / f"local_{uuid.uuid4().hex}_converted.wav"

    audio = AudioSegment.from_file(str(input_file))
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(str(output_path), format="wav")

    return str(output_path)


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    """
    Split WAV audio into smaller chunks.

    Chunk filenames are ASCII-safe.
    """
    wav_file = Path(wav_path)

    if not wav_file.exists():
        raise FileNotFoundError(f"WAV file not found: {wav_path}")

    audio = AudioSegment.from_wav(str(wav_file))

    # Normalize audio for transcription
    audio = audio.set_channels(1).set_frame_rate(16000)

    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    base_name = safe_name(wav_file.stem)

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start:start + chunk_ms]

        chunk_path = DOWNLOAD_DIR / f"{base_name}_chunk_{i:03d}.wav"

        chunk.export(str(chunk_path), format="wav")

        chunks.append(str(chunk_path))

    return chunks


def process_input(source: str) -> list:
    """
    Process either a YouTube URL or local audio/video file.

    Returns:
        list of WAV chunk file paths
    """
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)

    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks