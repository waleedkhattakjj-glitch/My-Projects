# MeetMind AI 🎙️🧠

**MeetMind AI** is an AI-powered meeting and video assistant that can transcribe audio/video content, generate professional summaries, extract action items, identify key decisions, list open questions, and let users chat with the transcript using RAG.

It supports both **YouTube URLs** and **local audio/video files** through a simple **Streamlit interface** and a CLI pipeline.

---

## ✨ Features

- 🎥 **YouTube audio extraction** using `yt-dlp`
- 📁 **Local audio/video file support**
- 🔊 **Audio conversion and chunking** using `pydub` and FFmpeg
- 📝 **Gemini-powered transcription**
- 📋 **Professional meeting summaries**
- ✅ **Action item extraction** with owner and deadline detection
- 🔑 **Key decision extraction**
- ❓ **Open question/follow-up extraction**
- 💬 **Chat with your meeting transcript** using RAG
- 🧠 **Vector search** using ChromaDB and Ollama embeddings
- 🌐 **Streamlit web interface**
- 📄 **Downloadable transcript and meeting report**

---

## 🧠 How It Works

```text
YouTube URL / Local Audio or Video
        ↓
Audio Download / Conversion
        ↓
Audio Chunking
        ↓
Gemini Transcription
        ↓
Summary + Action Items + Decisions + Questions
        ↓
Vector Store Creation with ChromaDB
        ↓
RAG-based Chat with Transcript
```

---

## 📁 Project Structure

```text
MeetMind-AI/
│
├── interface.py
├── main.py
├── README.md
├── .env
│
├── audio/
│   └── audio_processing.py
│
├── components/
│   ├── transcription_processing.py
│   ├── summerization.py
│   ├── extractor.py
│   ├── vector_store.py
│   └── rag_engine.py
│
├── downloades/
│   └── generated audio files and chunks
│
├── uploaded_files/
│   └── uploaded files from Streamlit
│
├── temp_uploads/
│   └── temporary safe upload copies
│
└── vector_db/
    └── Chroma vector database
```

> Note: `downloades/`, `uploaded_files/`, `temp_uploads/`, and `vector_db/` are generated automatically while running the app.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Google Gemini API**
- **LangChain**
- **ChromaDB**
- **Ollama Embeddings**
- **yt-dlp**
- **pydub**
- **FFmpeg**

---

## ✅ Requirements

Before running the project, make sure you have:

1. **Python 3.10+** installed
2. **FFmpeg** installed and added to PATH
3. **Google Gemini API key**
4. **Ollama** installed for embeddings/RAG
5. Required Python packages installed

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/MeetMind-AI.git
cd MeetMind-AI
```

---

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv aiva
aiva\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv aiva
source aiva/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install streamlit python-dotenv yt-dlp pydub google-genai langchain langchain-google-genai langchain-core langchain-community langchain-text-splitters langchain-ollama chromadb
```

If you want to save these dependencies:

```bash
pip freeze > requirements.txt
```

Then later anyone can install them with:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root folder:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.1-flash-lite
```

If your selected Gemini model is unavailable, replace it with another supported Gemini model available in your account.

Example:

```env
GEMINI_MODEL=gemini-2.0-flash
```

---

## 🎞️ Install FFmpeg

FFmpeg is required for audio conversion and YouTube audio extraction.

### Windows

1. Download FFmpeg from:
   
   https://ffmpeg.org/download.html

2. Extract it.
3. Add the `bin` folder to your system PATH.
4. Verify installation:

```bash
ffmpeg -version
```

### macOS

```bash
brew install ffmpeg
```

### Linux

```bash
sudo apt update
sudo apt install ffmpeg
```

---

## 🧠 Setup Ollama Embeddings

This project uses Ollama embeddings for the vector store.

Install Ollama from:

https://ollama.com/

Then pull the embedding model:

```bash
ollama pull bge-m3:567m
```

Make sure Ollama is running before using the RAG chat feature.

If this model name is unavailable on your system, pull another embedding model and update this line in `components/vector_store.py`:

```python
EMBEDDING_MODEL = "bge-m3:567m"
```

---

## 🚀 Run the Streamlit Interface

```bash
streamlit run interface.py
```

Then open the local URL shown in your terminal, usually:

```text
http://localhost:8501
```

---

## 🖥️ Run from CLI

You can also run the pipeline from the terminal:

```bash
python main.py
```

Then enter either:

- a YouTube URL, or
- a local audio/video file path

Example:

```text
Enter YouTube URL or local file path: https://www.youtube.com/watch?v=example
Language (english/hinglish): english
```

---

## 📌 Main Output

After processing, MeetMind AI generates:

- Meeting title
- Full transcript
- Professional summary
- Action items
- Key decisions
- Open questions
- RAG chat engine for transcript Q&A

---

## 🌐 Streamlit Interface Preview

The Streamlit interface allows you to:

1. Paste a YouTube URL
2. Upload an audio/video file
3. Process the content with one click
4. View extracted meeting intelligence in tabs
5. Download the full report
6. Download the transcript
7. Chat with the meeting transcript

---

## 🧩 Important Notes

### Filename Safety

Some YouTube titles contain Unicode characters like:

```text
？
```

These characters can cause upload errors with the Gemini File API. To prevent this, the audio processing file should use safe ASCII filenames, preferably based on the YouTube video ID instead of the title.

Recommended `yt-dlp` output template:

```python
output_path = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")
```

---

### Generated Folders

The following folders are generated automatically and should usually not be committed to GitHub:

```text
downloades/
uploaded_files/
temp_uploads/
vector_db/
```

You can add them to `.gitignore`.

Example `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc

# Virtual environment
aiva/
venv/
.env/

# Generated files
downloades/
uploaded_files/
temp_uploads/
vector_db/

# Chroma / local DB files
*.sqlite3
*.sqlite
```

---

## 🛠️ Troubleshooting

### 1. `GEMINI_API_KEY is not set`

Make sure your `.env` file exists in the root folder and contains:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

### 2. `UnicodeEncodeError: 'ascii' codec can't encode character`

This usually happens when the audio filename contains Unicode characters from a YouTube title.

Fix:

- Use video ID instead of title in `yt-dlp`
- Use safe ASCII filenames for uploaded/chunked files
- Delete old files from `downloades/` and run again

---

### 3. FFmpeg Error

If you get an FFmpeg-related error, verify FFmpeg is installed:

```bash
ffmpeg -version
```

If the command is not recognized, add FFmpeg to your PATH.

---

### 4. Ollama Embedding Error

Make sure Ollama is installed and running.

Then pull the embedding model:

```bash
ollama pull bge-m3:567m
```

---

### 5. ChromaDB / Vector Store Issues

If your RAG answers are incorrect or the vector database becomes corrupted, delete:

```text
vector_db/
```

Then process the meeting again.

---

## 🔮 Future Improvements

- Speaker diarization
- Multi-language transcription control
- PDF/DOCX report export
- Meeting timeline generation
- Sentiment analysis
- Better RAG memory management
- User authentication
- Cloud deployment
- Support for multiple meetings
- Dashboard analytics

---

## 🤝 Contributing

Contributions are welcome.

You can contribute by:

- Fixing bugs
- Improving prompts
- Adding new features
- Improving UI/UX
- Adding export formats
- Improving documentation

---

## 📄 License

This project is open-source and available under the **MIT License**.

---

## 👤 Author

Developed by **Waleed Khattak**.

GitHub: https://github.com/waleedkhattakjj-glitch
LinkedIn: www.linkedin.com/in/waleed-khattak-4ab6b733b

---

## ⭐ Support

If you like this project, please consider giving it a star on GitHub.
