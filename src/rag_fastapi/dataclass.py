import psycopg2

class VectorStorage:
    def __init__(self, conn_string):
        self.conn_string = conn_string

        def store(self, embeddings: list, chunks: list):
            with psycopg2.connect(self.conn_string) as conn:
                with conn.cursor() as cur:
                    counter = 0
                    for value in embeddings:
                        cur.execute(
                            """ INSERT INTO vectors (embedding, chunk) VALUES (%s,%s)""",
                            (value, chunks[counter])
                        )
                        counter += 1
                
            conn.close()
        
    def similar_search(self, embedded_question):

        result = ""
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
               
                cur.execute(
                    "SELECT chunk FROM vectors WHERE embedding <=> %s:: vector < 0.5;",
                    (embedded_question,)
                )
                
                for chunk in cur.fetchall():
                result += "\n" + chunk[0]
        conn.close()

        return result

    def create_table(self, vector_dim): 
        """use to create a new table"""
        with psycopg2.connect(self.conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE EXTENSION IF NOT EXISTS vectors;"
                )

                cur.execute("""
                        CREATE TABLE IF NOT EXISTS vectors(
                        id BIGSERIAL PRIMARY KEY, chunk TEXT, embedding VECTOR(%s);
                        """,
                        (vector_dim,)
                        )
        conn.close()

    

                



    
    
