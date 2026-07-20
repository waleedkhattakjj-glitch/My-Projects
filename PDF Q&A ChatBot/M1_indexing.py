from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
load_dotenv()
path = 'ENTER YOUR PDF PATH'
loader = PyPDFLoader(path)
doc = loader.load()

chunk = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = chunk.split_documents(doc)

embedding_model = OllamaEmbeddings(model='bge-m3:567m')

vectore_database = Chroma(
    embedding_function= embedding_model,
    persist_directory='chroma_db',
    collection_name='pdf_database'
)
vectore_database.add_documents(chunks)
print("PDF Embedded Succesfully")