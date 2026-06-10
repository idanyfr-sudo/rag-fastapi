from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import ollama
import base as db


splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)


def load_file(path: str) -> str:
    reader = PdfReader(path)
    pages = [page.extract_text() for page in reader.pages if page.extract_text()]
    file = "\n".join(pages)
    return file


def split_text(pages: str) -> list:
    if pages:

        chunks = splitter.split_text(pages)
        return chunks
    else:
        raise ValueError("No Value")


def vector_text(chunks):
    embeddings = ollama.embed(model ="snowflake-arctic-embed:22m", input = chunks)
    return embeddings["embeddings"]


def store_vectors(embeddings: list, chunks: list):
    
    cur = db.conn.cursor()
    counter = 0

    for value in embeddings:
        cur.execute(
            """ INSERT INTO vectors (embedding, chunk) VALUES (%s,%s)""",
            (value, chunks[counter]),
        )
        counter += 1
    db.conn.commit()
    cur.close()
    db.conn.close()
    return True

def process_document(path: str):
    file = load_file(path)

    splits = split_text(file)

    embeddings = vector_text(splits)

    store_vectors(embeddings, splits)

    print("Sucess")


if __name__ == "__main__":
    process_document("C:/Users/danyf/Documents/rag_project/mypdf.pdf")
