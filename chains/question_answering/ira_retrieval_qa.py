from typing import Optional
from langchain.chains import LLMChain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables import Runnable
from langchain_core.runnables.utils import Input, Output
from langchain_core.language_models import BaseLanguageModel
from langchain_core.retrievers import BaseRetriever
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from data.preprocessors.guardrails import detect_and_preserve_pii, check_bank_name
from prompts.document_prompt import document_prompt
from prompts.prompt_qa_chain import prompt_qa_chain

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
       
        prompt = prompt_qa_chain

        llm_chain = LLMChain(
            llm=self.__llm,
            prompt=prompt,
            verbose=True,
        )

        combine_docs_chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_prompt=document_prompt,
            document_variable_name="context"
        )

        retrievalQA = RetrievalQA(
            retriever=self.__retriever,
            combine_documents_chain=combine_docs_chain
        )

        question = detect_and_preserve_pii(input)
        bank_check_result = check_bank_name(question)

        if bank_check_result != question:
            return bank_check_result

        response =  retrievalQA.invoke({"query": question})
   
        answer = response.get("result")

        return answer
