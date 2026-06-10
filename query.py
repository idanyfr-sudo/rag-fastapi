import ingest as ig
import base as db
from openai import OpenAI
from fastapi import FastAPI, File, UploadFile
from pypdf import PdfReader
from pydantic import BaseModel

client = OpenAI()
app = FastAPI()


def similiar_search(question: str) -> str:
    # embedding question
    embedded_question = ig.vector_text(question)

    #setting up connection
    
    cur = db.conn.cursor()

    #Querying db
    cur.execute("SELECT chunk FROM vectors WHERE embedding <=> %s:: vector < 1;",(embedded_question[0],))
    retrieved_chunks = cur.fetchall()
    result = ""

    for chunk in retrieved_chunks:
        result += "/n" + chunk[0]

    return result


def context_base_question(question: str, retrieved_chunks: str) -> str:
    response = client.responses.create(
        model="gpt-5.4",
        input=f"answer this {question} from this context only: {retrieved_chunks}",
    )

    return response.output_text


class Question(BaseModel):
    content: str

@app.post("/askme/")
def main(question:Question):
    retrieved_chunks = similiar_search(question.content)
    response = context_base_question(question, retrieved_chunks)

    return {"answer":response}
    #Ended up using "Annotated" since is just a singular value 

@app.post("/Upload/")
def process_file(file: UploadFile):
    uploded_file = ig.load_file(file.file)

    splits = ig.split_text(uploded_file)

    embeddings = ig.vector_text(splits)

    stored = ig.store_vectors(embeddings, splits)

    if stored:
        return{"message":"Success"}


