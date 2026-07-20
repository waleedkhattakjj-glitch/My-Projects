# PDF Q&A ChatBot

A Generative AI / Retrieval-Augmented Generation (RAG) project that lets users upload a PDF, preview it, and ask questions whose answers are grounded only in that document.

**Created by: Muhammad Waleed**

---

## Overview

PDF Q&A ChatBot turns a static PDF into an interactive question-answering experience. Instead of manually searching through long documents, a user uploads a PDF and asks questions in plain language. The application finds the most relevant parts of that PDF and uses Gemini to generate a concise answer.

This is a Generative AI project because it combines:

- Embedding generation with Ollama's bge-m3:567m model
- Semantic search with ChromaDB
- Generative answers with Google Gemini
- Retrieval-Augmented Generation (RAG) to keep answers tied to the uploaded document

---

## Problem It Solves

Reading large PDFs can be slow and frustrating. Finding one specific policy, definition, rule, or detail often means manually scanning many pages.

A general AI chatbot may also answer using information outside the document or make assumptions. This project solves both problems by:

1. Extracting text from the uploaded PDF.
2. Splitting the text into smaller searchable chunks.
3. Storing those chunks in a Chroma vector database.
4. Retrieving the most relevant chunks for each question.
5. Instructing Gemini to answer only from the retrieved PDF content.

If the document does not contain the answer, the chatbot responds:
I don't know based on the provided document.

---

## Features

- Upload and chat with PDF documents
- Professional Streamlit interface
- PDF preview in the left sidebar
- Download button for the uploaded PDF
- Semantic document search using ChromaDB
- Google Gemini-powered answers
- Ollama bge-m3:567m embeddings
- PDF-only answer policy to reduce hallucinations
- Chat history visible in the interface
- Persistent Chroma databases
- Reuses an existing database when the same PDF is uploaded again

---

## How the Application Works
Upload PDF
↓
Create SHA-256 hash of the PDF
↓
Check whether a Chroma database already exists for that PDF
↓
If no database exists: load PDF → split text → create embeddings → save in ChromaDB
↓
User asks a question
↓
Retrieve the 3 most relevant chunks
↓
Send retrieved context + question to Gemini
↓
Display a grounded answer in the Streamlit chat interface

### Why the PDF is not embedded again and again

The Streamlit interface creates a SHA-256 hash from the uploaded PDF file. It stores the vector database inside a folder like this:
chroma_db/<pdf-hash>/

When the identical PDF is uploaded again, the app finds the existing Chroma collection and loads it instead of generating embeddings again. This saves time and avoids duplicate documents in the database.

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| Streamlit | Web interface for uploading PDFs and chatting |
| LangChain | RAG workflow, prompt templates, retriever, and chains |
| PyPDF | Extracts text from PDF files |
| Ollama | Runs the embedding model locally |
| bge-m3:567m | Converts PDF text into vector embeddings |
| ChromaDB | Stores and searches document embeddings |
| Google Gemini | Generates final answers from retrieved context |
| python-dotenv | Loads the Google API key from .env |

---

## Project Structure
PDF-QA-ChatBot/
│
├── M1_indexing.py # Command-line PDF indexing script
├── M2_main.py # Command-line Q&A chatbot script
├── M3_interface.py # Main Streamlit web application
├── requirements.txt # Python libraries required by the project
├── .env # Local Google API key file (do not upload to GitHub)
├── chroma_db/ # Generated Chroma vector databases (do not upload)
└── README.md # Project documentation

### File Descriptions

#### M1_indexing.py
This is the standalone indexing script. It:
- Loads genai-principles.pdf
- Splits the PDF into chunks of 1000 characters with 200 character overlap
- Creates embeddings with bge-m3:567m
- Saves the embeddings in ChromaDB

#### M2_main.py
This is the terminal/command-line version of the chatbot. It:
- Opens the saved Chroma database
- Retrieves the top 3 similar chunks
- Sends the question and context to Gemini
- Prints the answer in the terminal

#### M3_interface.py
This is the main web application. It:
- Provides the Streamlit user interface
- Lets users upload their own PDFs
- Shows the PDF preview in the sidebar
- Creates or reuses a Chroma database for each unique PDF
- Lets users ask questions through a chat interface

> **Recommended:** Run M3_interface.py for the complete application experience. It performs its own indexing, so you do not need to run M1_indexing.py before using the interface.

---

## Prerequisites

Install these before running the project:

- Python 3.10 or newer
- Ollama — required for embeddings
- A Google Gemini API key
- Git (recommended for cloning the repository)

---

## Installation Guide

### 1. Clone or download the repository

Using Git:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git
cd https://github.com/waleedkhattakjj-glitch/My-Projects
Or, on GitHub, select Code → Download ZIP, extract the ZIP file, and open the extracted project folder in your terminal or VS Code.

### 2. Create a virtual environment
Windows (PowerShell):
python -m venv .venv
.\.venv\Scripts\Activate.ps1

### 3. Upgrade pip
python -m pip install --upgrade pip

### 4. Install the Python libraries
pip install -r requirements.txt

### 5. Install and prepare Ollama
Make sure ollama is locally install in your system

### 6. Add your Google Gemini API key
Create a file named .env in the project root folder and add:
GOOGLE_API_KEY=your_google_gemini_api_key_here

## Run the Streamlit Application
Start the main application with:
streamlit run M3_interface.py

## Using the application
1. Upload a PDF from the left sidebar.
2. Wait while the PDF is indexed for the first time.
3. Preview the uploaded PDF in the sidebar.
4. Type a question in the chat box.
5. Receive an answer based only on the uploaded document

## Future Improvements
Show source page numbers with each answer
Support multiple PDFs in one workspace
Add OCR support for scanned PDFs
Add a clear-chat and delete-document option
Add streaming responses
Deploy with an embedding solution suitable for cloud hosting

## Author
Muhammad Waleed
Built as a Generative AI PDF Question & Answering project using Python, LangChain, Ollama, ChromaDB, Google Gemini, and Streamlit.
