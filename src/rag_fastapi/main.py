from database import conn
from ingest import load_file,vector_text,split_text,store_vectors
from openai import OpenAI
from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModelSS

client = OpenAI()
app = FastAPI()


def similiar_search(question: str) -> str:
    if not question:
        raise HTTPException(status_code = 400, detail = "No question was entered")

    result = ""
    
    # embedding question
    embedded_question = vector_text(question)

    with conn.cursor() as cur:                                #connection
        
        cur.execute("SELECT chunk FROM vectors WHERE embedding <=> %s:: vector < 1;",(embedded_question,))
        
        for chunk in cur.fetchall():
            result += "\n" + chunk[0]

    return result
 

    


def context_base_question(question: str, retrieved_chunks: str) -> str:
    response = client.responses.create(
        model="gpt-5.4",
        input=f"answer this {question} using this context only: {retrieved_chunks}",
    )

    return response.output_text


class Question(BaseModel):
    content: str

@app.post("/askme/")
def main(question: Question):
    retrieved_chunks = similiar_search(question.content)
    if not retrieved_chunks:
        return{"answer":"No relevant context found"}
    response = context_base_question(question.content, retrieved_chunks)

    return {"answer":response}
   

@app.post("/Upload/")
def process_file(file: UploadFile):
    if not file.content_type == "application/pdf" or not file.file:
        raise HTTPException(status_code = 415, detail = "Must be a non empty PDF file")
    uploded_file = load_file(file.file)

    splits = split_text(uploded_file)

    embeddings = vector_text(splits)

    stored = store_vectors(embeddings, splits)

    if stored:
        return{"message":"Success"}


