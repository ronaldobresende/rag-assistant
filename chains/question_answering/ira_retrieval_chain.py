from typing import Optional
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables import Runnable
from langchain_core.runnables.utils import Input, Output
from langchain_core.language_models import BaseLanguageModel
from langchain_core.retrievers import BaseRetriever
from data.preprocessors.guardrails import detect_and_preserve_pii, check_bank_name
from prompts.document_prompt import document_prompt
from prompts.prompt_garantias import prompt_garantias
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.callbacks.tracers import ConsoleCallbackHandler


class IraRetrievalChain(Runnable[Input, Output]):
    def __init__(self, 
        llm: BaseLanguageModel, 
        retriever: BaseRetriever,
        memory: ConversationBufferMemory
    ) -> None:
        self.__llm = llm
        self.__retriever = retriever
        self.__memory = memory

    def invoke(
        self, 
        input: Input, 
        config: Optional[RunnableConfig] = None
    ) -> Output:
                 
        bank_check_result = check_bank_name(input)
        
        if bank_check_result != input:
            return {"answer": bank_check_result}
        
        question = detect_and_preserve_pii(input)

        prompt = prompt_garantias
     
        combine_docs_chain = create_stuff_documents_chain(
            llm=self.__llm,
            prompt=prompt,
            document_prompt=document_prompt,
            document_variable_name="context"

        )
 
        chain = create_retrieval_chain(
            retriever=self.__retriever,
            combine_docs_chain=combine_docs_chain
        )
 
        chat_history = self.__memory.load_memory_variables({})["chat_history"]

        # Combinar histórico com a nova pergunta
        combined_input = f"{chat_history}\nUsuário: {question}"
     
        response = chain.invoke({"input": combined_input}, config={'callbacks': [ConsoleCallbackHandler()]})
        self.__memory.save_context({"input": question}, {"output": response.get("answer")})
   
        return response