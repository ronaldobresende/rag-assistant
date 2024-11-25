from langchain_core.retrievers import BaseRetriever
from langchain.schema import Document
from data.ingestors.weaviate_setup import client

class WeaviateRetriever(BaseRetriever):
    
    def _get_relevant_documents(self, query):
        query = f"""
        {{
            Get {{
                Document(where: {{
                    path: ["title"],
                    operator: Equal,
                    valueString: "garantias"
                }}) {{
                    content
                }}
            }}
        }}
        """
        response = client.query.raw(query)

        if 'data' not in response or 'Get' not in response['data'] or 'Document' not in response['data']['Get']:
            return []
        documents = response['data']['Get']['Document']
        
        return [Document(page_content=doc['content'], metadata={"history": "", "question": query}) for doc in documents]

