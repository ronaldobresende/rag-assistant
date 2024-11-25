
from langchain.embeddings.openai import OpenAIEmbeddings

class OpenAIEmbeddingsHandler:
    def __init__(self, openai_api_key: str):
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)


    def get_embed_documentos(self, documents):
        return self.embeddings.embed_documents(documents)

    def get_embed_query(self, query: str):
        return self.embeddings.embed_query(query)