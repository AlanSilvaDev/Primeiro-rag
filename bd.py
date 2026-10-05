
import os

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("GOOGLE_API_KEY não encontrada. Verifique o arquivo .env.")

pasta_base = "base"


def criar_db():
    documentos = carregar_documentos()
    chunks = dividir_chunks(documentos)
    vetorizar_chunks(chunks)


def carregar_documentos():
    carregador_doc = PyPDFDirectoryLoader(pasta_base)
    documentos = carregador_doc.load()
    return documentos


def dividir_chunks(documentos):
    separador_doc = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )
    chunks = separador_doc.split_documents(documentos)
    print(len(chunks))
    return chunks


def vetorizar_chunks(chunks):
    Chroma.from_documents(chunks, GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2"), persist_directory="db")


if __name__ == "__main__":
    criar_db()
