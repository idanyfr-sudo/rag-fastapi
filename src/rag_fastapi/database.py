import psycopg2
import json


try:
   with open("config.json", "r") as config:
    data= json.load(config)
    connection_string = data["connection-string"]

except FileNotFoundError as e:
    print("Missing or Corrupted config File")
    raise


conn = psycopg2.connect(**connection_string)


def create_table():
    with conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS vectors( id BIGSERIAL PRIMARY KEY, chunk TEXT, embedding vector(384))"
            )

   


def create_index():
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE INDEX on vectors
            USING hnsw(embedding vector_cosine_ops);
               """)
    


if __name__ == "__main__":
    create_table()
    print("created")
