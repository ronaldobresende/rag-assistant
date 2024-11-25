from typing import Optional
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_core.runnables.config import RunnableConfig
from langchain.chains import ConversationalRetrievalChain
from langchain_core.runnables import Runnable
from langchain_core.runnables.utils import Input, Output
from langchain_core.language_models import BaseLanguageModel
from langchain_core.retrievers import BaseRetriever
from data.preprocessors.guardrails import detect_and_preserve_pii, check_bank_name
from prompts.chat_prompt_garantias import chat_prompt_garantias 

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

        prompt = chat_prompt_garantias

        chain = ConversationalRetrievalChain.from_llm(
            llm=self.__llm,
            retriever=self.__retriever,
            memory=self.__memory,
            combine_docs_chain_kwargs={
                "prompt": prompt,
            },
            verbose=True  
        )

        question = detect_and_preserve_pii(input)
        bank_check_result = check_bank_name(question)

        if bank_check_result != question:
            return bank_check_result

        response = chain({"question": question})
   
        return response["answer"]