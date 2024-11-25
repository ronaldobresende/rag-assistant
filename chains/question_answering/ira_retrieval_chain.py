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

class IraRetrievalChain(Runnable[Input, Output]):
    def __init__(self, 
        llm: BaseLanguageModel, 
        retriever: BaseRetriever
    ) -> None:
        self.__llm = llm
        self.__retriever = retriever

    def invoke(
        self, 
        input: Input, 
        config: Optional[RunnableConfig] = None
    ) -> Output:
        
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

        question = detect_and_preserve_pii(input)
        bank_check_result = check_bank_name(question)

        if bank_check_result != question:
            return bank_check_result

        response = chain.invoke({"input": question})
        answer = response.get("answer")

        return answer