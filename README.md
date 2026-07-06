# RAG On FastApi

This is a Retrieval-Augmented Generation pipeline built with fastapi. This application can process PDF documents, store embeddings in a PostgreSQL database, and uses an OpenAI Model to deliver context-based answers.

----

# Installation & Setup

# 1.Set up Virtual Environment and set **OPENAI_API_KEY**.
```bash

##Create and activate virtual environment

python -m venv .venv

source.venv/bin/activate

## Set OPENAI KEY.

export OPENAI_API_KEY="YOUR_KEY"```
---

```PowerShell
## Create and activate virtual environment

python -m venv .venv

.venv/Scripts/activate

## Set OPENAI KEY

$env:OPENAI_API_KEY="YOUR_KEY"```

---

# 2.Clone the repository

```bash
git clone https://github.com/idanyfr-sudo/rag-fastapi.git```


---
#3.Set up your database:
You need a PostgreSQL database with the pgvector extension enabled in order to store embeddings.

1.Create a new PostgreSQL database and activate pgvector on it.

2.Open config.json file.

3.Replace place holder information with your database credentials.
---

#4.Run the App
```bash
fastapi dev src/rag_fastapi/main.py```



##Author
idanyfr-sudo






