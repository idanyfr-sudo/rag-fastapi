from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from database import conn



splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
model = SentenceTransformer('all-MiniLM-L6-v2')


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
    embeddings = model.encode(chunks)
    return embeddings.tolist()


def store_vectors(embeddings: list, chunks: list):
    
    cur = conn.cursor()
    counter = 0

    for value in embeddings:
        cur.execute(
            """ INSERT INTO vectors (embedding, chunk) VALUES (%s,%s)""",
            (value, chunks[counter]),
        )
        counter += 1
    conn.commit()
    cur.close()
    return True



