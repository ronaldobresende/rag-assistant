import weaviate
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.weaviate import Weaviate
from langchain.schema.vectorstore import VectorStoreRetriever  # Certifique-se de importar a classe BaseRetriever corretamente

WEAVIATE_URL = "http://localhost:8080/"

# Configura o cliente Weaviate
client = weaviate.Client(
    url=WEAVIATE_URL,
)

open_api_key = os.getenv('OPENAI_API_KEY')
modelo = "gpt-4o"

# Configure os embeddings
embeddings = OpenAIEmbeddings(openai_api_key=open_api_key)

# Configure o vectorstore
vectorstore = Weaviate(client=client, index_name="Document", text_key="content", embedding=embeddings)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

def get_relevant_documents_teste(query: str, k: int = 5):
    query_vector = embeddings.embed_query(query)  # Gera vetor da consulta
    results = vectorstore.similarity_search_by_vector(query_vector, k=k)  # Pesquisa por vetor
    return results

# Exemplo de uso
if __name__ == "__main__":
    query = "o que é devedor solidário?"
    documents = get_relevant_documents_teste(query)
    print("documentos ", documents)
    for doc in documents:
        print(doc)

# class CustomVectorRetriever(BaseRetriever):
#     def __init__(self, vectorstore, embeddings, k: int = 5):
#         self.vectorstore = vectorstore
#         self.embeddings = embeddings
#         self.k = k

#     def _get_relevant_documents(self, query: str):
#         query_vector = self.embeddings.embed_query(query)
#         return self.vectorstore.similarity_search_by_vector(query_vector, k=self.k)        