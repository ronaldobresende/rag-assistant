# from embeddings.retrievers.weaviate_retriever import WeaviateRetriever
# from prompts.chat_prompt_garantias import chat_prompt_garantias
# from data.preprocessors.guardrails import detect_and_preserve_pii, check_bank_name
# #from chains.conversational.ira_conversational_retrieval_chain import IraRetrievalChain
# #from chains.question_answering.ira_retrieval_chain import IraRetrievalChain
# from chains.question_answering.ira_retrieval_qa import IraRetrievalChain
# from memories.chat_history import get_chat_conversation_history_memory 
# from llms.open_ai_client import OpenAiClient

# # Inicializa a memória uma vez
# memory = get_chat_conversation_history_memory()

# def start_chat(user_input: str):
#     open_ai_client = OpenAiClient()

#     llm = open_ai_client.get_llm()

#     retriever = WeaviateRetriever()

#     #ira_chain = IraRetrievalChain(llm=llm, retriever=retriever, memory=memory)
#     ira_chain = IraRetrievalChain(llm=llm, retriever=retriever)

#     response = ira_chain.invoke(user_input)

#     return response
from embeddings.retrievers.weaviate_retriever import WeaviateRetriever
from chains.conversational.ira_conversational_retrieval_chain import IraRetrievalChain
# #from chains.question_answering.ira_retrieval_chain import IraRetrievalChain
# from chains.question_answering.ira_retrieval_qa import IraRetrievalChain
from memories.chat_history import get_chat_conversation_history_memory 
from llms.open_ai_client import OpenAiClient

memory = get_chat_conversation_history_memory()

class AVIChainAdaptor:
    def __init__(self):
        self.memory = memory
        self.open_ai_client = OpenAiClient()
        self.llm = self.open_ai_client.get_llm()
        self.retriever = WeaviateRetriever()
        self.ira_chain = IraRetrievalChain(llm=self.llm, retriever=self.retriever, memory=self.memory)

    def invoke(self, user_input: str):
        response = self.ira_chain.invoke(user_input)
        return response