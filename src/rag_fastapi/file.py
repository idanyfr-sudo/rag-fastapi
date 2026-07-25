

class FileProcessor:
    def __init__(self, doc_loader, doc_splitter, embedding_model):
        self.doc_loader = doc_loader
        self.doc_splitter = doc_splitter
        self.embedding_model = embedding_model


    def load_document(self, document_path: str) -> str:      
    """ Method used to load pdf file """
        
        reader = self.doc_loader(document_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    def split_document(self, document: str):
        """This method would split the documents into manageable chunks once loaded"""
        
        if document:
            splitter = self.doc_splitter
            chunks = splitter.split_text(document)
            return chunks
        else:
            raise ValueError("empty document")

    def vector_text(self, chunks:str): 
        vectors = self.embedding_model.encode(chunks)
        return vectors.tolist()